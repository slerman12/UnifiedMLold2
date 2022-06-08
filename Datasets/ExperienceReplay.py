# Copyright (c) AGI.__init__. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# MIT_LICENSE file in the root directory of this source tree.
import os
import random
import glob
import shutil
import atexit
import warnings
from pathlib import Path
import datetime
import io
import traceback

from omegaconf import OmegaConf

import numpy as np

import torch
from torch.utils.data import IterableDataset, Dataset

from torchvision.transforms import transforms


class ExperienceReplay:
    def __init__(self, batch_size, num_workers, capacity, action_spec, suite, task, offline, generate, save, load, path,
                 obs_spec=None, nstep=0, discount=1, metadata_shape=None, transform=None):
        # Path and loading

        exists = glob.glob(path + '*/')

        offline = offline or generate

        if load or offline:
            if suite == 'classify':
                standard = f'./Datasets/ReplayBuffer/Classify/{task}_Buffer'
                if len(exists) == 0:
                    exists = [standard + '/']
                    print('All data loaded. Training of classifier underway.')
                else:
                    if path != standard:
                        warnings.warn(f'Loading a saved replay of a classify task from a previous online session.'
                                      f'For the standard offline dataset, set replay.path="{standard}" '  # If exists
                                      f'or delete the saved buffer in {path}.')
            assert len(exists) > 0, f'No existing replay buffer found in path: {path}'
            self.path = Path(sorted(exists)[-1])
            save = offline or save
        else:
            self.path = Path(path + '_' + str(datetime.datetime.now()))
            self.path.mkdir(exist_ok=True, parents=True)

        # Directory for sending updates to replay workers
        (self.path / 'Updates').mkdir(exist_ok=True, parents=True)

        # Delete any pre-existing ones
        update_names = (self.path / 'Updates').glob('*.npz')
        for update_name in update_names:
            update_name.unlink(missing_ok=True)  # Deletes file

        if not save:
            # Delete replay on terminate
            atexit.register(lambda p: (shutil.rmtree(p), print('Deleting replay')), self.path)

        # Data specs

        if obs_spec is None:
            obs_spec = {'name': 'obs', 'shape': (1,)}

        # todo obs_shape, action_shape, meta_shape, no specs
        self.specs = (obs_spec, action_spec, *[{'name': name, 'shape': (1,)}
                                               for name in ['reward', 'discount', 'label', 'step']],
                      {'name': 'meta', 'shape': metadata_shape or (0,)},)

        # Episode traces (temporary in-RAM buffer until full episode ready to be stored)

        self.episode = {spec['name']: [] for spec in self.specs}
        self.episode_len = 0
        self.episodes_stored = len(list(self.path.glob('*.npz')))
        self.save = save
        self.offline = offline

        # Data transform

        if transform is not None:
            if isinstance(transform, str):
                transform = OmegaConf.create(transform)
            if 'RandomCrop' in transform and 'size' not in transform['RandomCrop']:
                transform['RandomCrop']['size'] = obs_spec['shape'][-2:]
            # Can pass in a dict of torchvision transform names and args
            transform = transforms.Compose([getattr(transforms, t)(**transform[t]) for t in transform])

        # Parallelized experience loading, either online or offline

        self.nstep = nstep

        self.num_workers = max(1, min(num_workers, os.cpu_count()))

        self.experiences = (Offline if offline else Online)(path=self.path,
                                                            capacity=np.inf if save else capacity // self.num_workers,
                                                            num_workers=self.num_workers,  # don't need todo
                                                            fetch_per=1000,
                                                            save=save,
                                                            nstep=nstep,
                                                            discount=discount,
                                                            transform=transform)

        # Batch loading

        self.epoch = 1

        self.batches = torch.utils.data.DataLoader(dataset=self.experiences,
                                                   batch_size=batch_size,
                                                   shuffle=offline,
                                                   num_workers=self.num_workers,
                                                   pin_memory=True,
                                                   worker_init_fn=worker_init_fn,
                                                   persistent_workers=True  #Testing todo
                                                   )
        # Replay

        self._replay = None

    # Returns a batch of experiences
    def sample(self):
        return next(self)  # Can iterate via next

    # Allows iteration
    def __next__(self):
        try:
            return next(self.replay)
        except StopIteration:
            self.epoch += 1
            self._replay = None
            return next(self)

    # Allows iteration
    def __iter__(self):
        self._replay = iter(self.batches)
        return self.replay

    @property
    def replay(self):
        if self._replay is None:
            self._replay = iter(self.batches)
        return self._replay

    # Tracks single episode "trace" in memory buffer
    def add(self, experiences=None, store=False):
        if experiences is None:
            experiences = []

        # An "episode" or part of episode of experiences
        assert isinstance(experiences, (list, tuple))

        for exp in experiences:
            for spec in self.specs:
                # Missing data
                if not hasattr(exp, spec['name']):
                    setattr(exp, spec['name'], None)

                # Add batch dimension
                if np.isscalar(exp[spec['name']]) or exp[spec['name']] is None:
                    exp[spec['name']] = np.full((1,) + tuple(spec['shape']), exp[spec['name']])
                if len(exp[spec['name']].shape) == len(spec['shape']):
                    exp[spec['name']] = np.expand_dims(exp[spec['name']], 0)

                # Validate consistency
                assert spec['shape'] == exp[spec['name']].shape[1:], \
                    f'Unexpected {spec["name"]} shape: {spec["shape"]} vs. {exp[spec["name"]].shape}'

                # Add the experience
                self.episode[spec['name']].append(exp[spec['name']])

        self.episode_len += len(experiences)

        if store:
            self.store_episode()  # Stores them in file system

    # Stores episode (to file in system)
    def store_episode(self):
        if self.episode_len == 0:
            return

        for spec in self.specs:
            # Concatenate into one big episode batch
            self.episode[spec['name']] = np.concatenate(self.episode[spec['name']], axis=0)

        self.episode_len = self.episode['observation'].shape[0]

        # Expands attributes that are unique per batch (such as 'step')
        for spec in self.specs:
            if self.episode[spec['name']].shape[0] == 1:
                self.episode[spec['name']] = np.repeat(self.episode[spec['name']], self.episode_len, axis=0)

        timestamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
        num_episodes = len(self)
        episode_name = f'{timestamp}_{num_episodes}_{self.episode_len}.npz'

        # Save episode
        save_path = self.path / episode_name
        with io.BytesIO() as buffer:
            np.savez_compressed(buffer, **self.episode)
            buffer.seek(0)
            with save_path.open('wb') as f:
                f.write(buffer.read())

        self.episode = {spec['name']: [] for spec in self.specs}
        self.episode_len = 0
        self.episodes_stored += 1

    # Updates experiences (in workers) by storing dicts of update values for corresponding experience IDs to file system
    def rewrite(self, updates, ids):  # todo should updates be stored in a buffer until sufficiently big per worker?
        assert isinstance(updates[0], dict), f'expected \'updates\' as list of dicts, got {type(updates)}'

        # Store into replay buffer
        for update, exp_id, worker_id in zip(updates, *ids.T):

            # In the offline setting, each worker has a copy of all the data
            for worker in range(self.num_workers):

                timestamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
                update_name = f'{exp_id}_{worker if self.offline else worker_id}_{timestamp}.npz'
                path = self.path / 'Updates'

                # Send update to workers todo group by worker
                with io.BytesIO() as buffer:
                    np.savez_compressed(buffer, update)
                    buffer.seek(0)
                    with (path / update_name).open('wb') as f:
                        f.write(buffer.read())

                if not self.offline:
                    break

    def __len__(self):
        return self.episodes_stored if self.offline or not self.save \
            else len(list(self.path.glob('*.npz')))


# How to initialize each worker
def worker_init_fn(worker_id):
    seed = np.random.get_state()[1][0] + worker_id
    np.random.seed(seed)
    random.seed(seed)


# A CPU worker that can iteratively and efficiently build/update batches of experience in parallel (from files)
class Experiences:
    def __init__(self, path, capacity, num_workers, fetch_per, save, offline=True, nstep=0, discount=1, transform=None):

        # Dataset construction via parallel workers

        self.path = path

        self.episode_names = []
        self.episodes = dict()

        self.num_experiences_loaded = 0
        self.capacity = capacity
        self.index = []  # Maps stored experiences to episodes' names
        self.deleted_indices = 0

        self.num_workers = num_workers

        self.fetch_per = fetch_per
        self.samples_since_last_fetch = fetch_per

        self.save = save
        self.offline = offline

        # Load in existing data
        list(map(self.load_episode, sorted(path.glob('*.npz'))))

        self.nstep = nstep
        self.discount = discount

        self.transform = transform

    @property
    def worker_id(self):
        # todo do i need the try clause?
        try:
            return torch.utils.data.get_worker_info().id
        except:
            return 0
        # todo can get num_workers same way

    def load_episode(self, episode_name):
        try:
            with episode_name.open('rb') as episode_file:
                episode = np.load(episode_file)
                episode = {key: episode[key] for key in episode.keys()}
        except:
            return False

        episode_len = next(iter(episode.values())).shape[0] - 1  # todo should it be minus nstep for unique epochs?

        while episode_len + self.num_experiences_loaded > self.capacity:
            early_episode_name = self.episode_names.pop(0)
            early_episode = self.episodes.pop(early_episode_name)
            early_episode_len = next(iter(early_episode.values())).shape[0] - 1
            self.index = self.index[early_episode_len:]
            self.deleted_indices += early_episode_len  # To derive a consistent experience index even as data deleted
            self.num_experiences_loaded -= early_episode_len
            if not self.offline:
                # Deletes early episode file
                early_episode_name.unlink(missing_ok=True)

        episode['id'] = len(self.index) + self.deleted_indices  # IDs remain unique even as experiences deleted

        self.episode_names.append(episode_name)
        self.episode_names.sort()
        self.episodes[episode_name] = episode
        self.num_experiences_loaded += episode_len
        self.index += list(enumerate([episode_name] * episode_len))

        if self.num_experiences_loaded != len(self.index):
            print('wahhhhhhhhhwbbbabababa')
        assert self.num_experiences_loaded == len(self.index)  # TODO delete, just checking

        if not self.save:
            episode_name.unlink(missing_ok=True)  # Deletes file

        return True

    # Populates workers with new data
    def worker_fetch_episodes(self):
        if self.samples_since_last_fetch < self.fetch_per:
            return

        self.samples_since_last_fetch = 0

        episode_names = sorted(self.path.glob('*.npz'), reverse=True)  # Episodes
        num_fetched = 0
        # Find new episodes
        for episode_name in episode_names:
            episode_idx, episode_len = [int(x) for x in episode_name.stem.split('_')[1:]]
            if episode_idx % self.num_workers != self.worker_id:  # Each worker stores their own dedicated data
                continue
            if episode_name in self.episodes.keys():  # Don't store redundantly
                break
            # if num_fetched + episode_len > self.capacity:  # Don't overfill  (This is already accounted for)
            #     break
            num_fetched += episode_len
            if not self.load_episode(episode_name):
                break  # Resolve conflicts

    # Workers can update/write-to their own data based on file-stored update specs
    def worker_fetch_updates(self):
        update_names = (self.path / 'Updates').glob('*.npz')

        # Fetch update specs  TODO check for MetaShape_[], update and set meta
        for update_name in update_names:
            exp_id, worker_id = [int(ids) for ids in update_name.stem.split('_')[:1]]

            if worker_id != self.worker_id:  # Each worker updates own dedicated data
                continue

            # Get corresponding experience and episode
            idx, episode_name = self.index[exp_id - self.deleted_indices]

            try:
                with update_name.open('rb') as update_file:
                    update = np.load(update_file)
                    # Iterate through each update spec
                    for key in update.keys():
                        # Update experience in replay
                        self.episodes[episode_name][key][idx] = update[key]
                        # todo first set meta by the meta shape in storage
                update_name.unlink(missing_ok=True)  # Delete update spec when stored
            except:
                continue

    def sample(self, episode_names, metrics=None):
        episode_name = random.choice(episode_names)  # Uniform sampling of experiences
        return episode_name

    # N-step cumulative discounted rewards
    def process(self, episode, idx=None):
        episode_len = len(episode['observation'])
        limit = episode_len - (self.nstep or 1)
        # TODO think, i guess last nstep is ignored? then maybe offline idx and index should reflect that.
        #  we're getting redundant epochs, unles the minus-1 in episode-len accounts for that... minus-nstep ?
        #     might not need this paragraph at all
        assert idx % limit == idx, 'checking in offline or nstep == 1 setting. then test in nstep. ' \
                                   'then test in episode_len-=nstep'
        idx = np.random.randint(limit) if idx is None else idx % limit

        # Transition
        obs = episode['observation'][idx]
        action = episode['action'][idx + 1]
        next_obs = episode['observation'][idx + self.nstep]
        reward = np.full_like(episode['reward'][idx + 1], np.NaN)
        print(np.full_like(episode['reward'][idx + 1], np.NaN), np.NaN, 'np.NaN suffices?',
              np.full_like(episode['reward'][idx + 1], np.NaN).shape)
        discount = np.ones_like(episode['discount'][idx + 1])
        label = episode['label'][idx].squeeze()
        step = episode['step'][idx]
        exp_id, worker_id = episode['id'] + idx, self.worker_id
        ids = np.array([exp_id, worker_id])
        meta = episode['meta'][idx]

        # Trajectory
        if self.nstep > 0:
            traj_o = episode['observation'][idx:idx + self.nstep + 1]
            traj_a = episode['action'][idx + 1:idx + self.nstep + 1]  # 1 len smaller than traj_o
            traj_r = episode['reward'][idx + 1:idx + self.nstep + 1]  # 1 len smaller than traj_o
            traj_l = episode['label'][idx:idx + self.nstep + 1]
        else:
            traj_o = traj_a = traj_r = traj_l = np.NaN

        # Compute cumulative discounted reward
        for i in range(1, self.nstep + 1):
            if episode['reward'][idx + i] != np.NaN:
                step_reward = episode['reward'][idx + i]
                if np.isnan(reward):
                    reward = np.zeros(1)
                reward += discount * step_reward
                discount *= episode['discount'][idx + i] * self.discount

        # Transform
        if self.transform is not None:  # todo audio
            obs = self.transform(torch.as_tensor(obs).div(255)) * 255

        return obs, action, reward, discount, next_obs, label, traj_o, traj_a, traj_r, traj_l, step, ids, meta

    def fetch_sample_process(self, idx=None):
        try:
            # Populate workers with up-to-date data
            if not self.offline:
                self.worker_fetch_episodes()
            self.worker_fetch_updates()
        except:
            traceback.print_exc()

        self.samples_since_last_fetch += 1

        # Sample or index an episode
        if idx is None:
            episode_name = self.sample(self.episode_names)
        else:
            idx, episode_name = self.index[idx]

        episode = self.episodes[episode_name]

        return self.process(episode, idx)  # Process episode into a compact experience


# Loads Experiences with an Iterable Dataset
class Online(Experiences, IterableDataset):
    def __init__(self, path, capacity, num_workers, fetch_per, save, nstep=0, discount=1, transform=None):
        super().__init__(path, capacity, num_workers, fetch_per, save, False, nstep, discount, transform)

    def __iter__(self):
        # Keep fetching, sampling, and building batches
        while True:
            yield self.fetch_sample_process()  # Yields a single experience


# Loads Experiences with a standard Dataset
class Offline(Experiences, Dataset):
    def __init__(self, path, capacity, num_workers, fetch_per, save, nstep=0, discount=1, transform=None):
        super().__init__(path, capacity, num_workers, fetch_per, save, True, nstep, discount, transform)

    def __getitem__(self, idx):
        return self.fetch_sample_process(idx)  # Get single experience by index

    def __len__(self):
        return self.num_experiences_loaded
