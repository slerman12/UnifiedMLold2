# Copyright (c) AGI.__init__. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# MIT_LICENSE file in the root directory of this source tree.
import time

import torch
from torch.nn.functional import cross_entropy

import Utils

from Blocks.Augmentations import IntensityAug, RandomShiftsAug
from Blocks.Encoders import CNNEncoder
from Blocks.Actors import EnsembleActor, CategoricalCriticActor
from Blocks.Critics import EnsembleQCritic

from Losses import QLearning, PolicyLearning


class ExperimentAgent(torch.nn.Module):
    """An Agent for evaluating computer vision + RL experiments"""
    def __init__(self,
                 obs_spec, action_spec, trunk_dim, hidden_dim, standardize, norm, recipes,  # Architecture
                 lr, lr_decay_epochs, weight_decay, ema_decay, ema,  # Optimization
                 explore_steps, stddev_schedule, stddev_clip,  # Exploration
                 discrete, RL, supervise, generate, device, parallel, log,  # On-boarding
                 half=False, third=False  # Experiment
                 ):
        super().__init__()

        self.discrete = discrete and not generate
        self.supervise = supervise
        self.RL = RL
        self.generate = generate
        self.device = device
        self.log = log
        self.birthday = time.time()
        self.step = self.frame = 0
        self.episode = self.epoch = 1
        self.explore_steps = explore_steps
        self.ema = ema

        self.num_actions = action_spec.num_actions or 1

        self.half, self.third = half, third  # Contrastive and ground truth RL examples

        if generate:
            action_spec.shape = obs_spec.shape
            action_spec.low, action_spec.high = -1, 1

        # Data stats
        self.low, self.high = obs_spec.low, obs_spec.high

        self.encoder = Utils.Rand(trunk_dim) if generate \
            else CNNEncoder(obs_spec, standardize=standardize, norm=norm, **recipes.encoder, parallel=parallel,
                            lr=lr, lr_decay_epochs=lr_decay_epochs, weight_decay=weight_decay,
                            ema_decay=ema_decay * ema)

        repr_shape = (trunk_dim,) if generate \
            else self.encoder.repr_shape

        self.actor = EnsembleActor(repr_shape, trunk_dim, hidden_dim, action_spec, **recipes.actor,
                                   ensemble_size=1, stddev_schedule=stddev_schedule, stddev_clip=stddev_clip,
                                   lr=lr, lr_decay_epochs=lr_decay_epochs, weight_decay=weight_decay,
                                   ema_decay=ema_decay * ema)

        self.critic = EnsembleQCritic(repr_shape, trunk_dim, hidden_dim, action_spec, **recipes.critic,
                                      ensemble_size=2, discrete=self.discrete, ignore_obs=generate,
                                      lr=lr, lr_decay_epochs=lr_decay_epochs, weight_decay=weight_decay,
                                      ema_decay=ema_decay)

        self.action_selector = CategoricalCriticActor(stddev_schedule)

        # Image augmentation
        self.aug = Utils.instantiate(recipes.aug) or (IntensityAug(0.05) if discrete
                                                      else RandomShiftsAug(pad=4))

        # Birth

    def act(self, obs):
        with torch.no_grad(), Utils.act_mode(self.encoder, self.actor, self.critic):
            obs = torch.as_tensor(obs, device=self.device).float()

            # EMA shadows
            encoder = self.encoder.ema if self.ema and not self.generate else self.encoder
            actor = self.actor.ema if self.ema and not self.discrete else self.actor
            critic = self.critic.ema if self.ema else self.critic

            # "See"
            obs = encoder(obs)

            Pi = self.action_selector(critic(obs), self.step) if self.discrete \
                else actor(obs, self.step)

            action = Pi.sample() if self.training \
                else Pi.best if self.discrete \
                else Pi.mean

            if self.training:
                self.step += 1
                self.frame += len(obs)

                # Explore phase
                if self.step < self.explore_steps and not self.generate:
                    action = torch.randint(self.num_actions, size=action.shape) if self.discrete \
                        else action.uniform_(-1, 1)

            return action

    # "Dream"
    def learn(self, replay):
        # "Recollect"

        batch = next(replay)
        obs, action, reward, discount, next_obs, label, step, ids, meta = Utils.to_torch(
            batch, self.device)

        # "Envision" / "Perceive"

        # Augment
        obs = self.aug(obs)

        # Actor-Critic -> Generator-Discriminator conversion
        if self.generate:
            obs = (obs - self.low) * 2 / (self.high - self.low) - 1  # Normalize first
            action, reward[:] = obs.flatten(-3), 1
            next_obs[:] = label[:] = float('nan')

        # Encode
        obs = self.encoder(obs)

        # Augment and encode future
        if replay.nstep > 0 and not self.generate:
            with torch.no_grad():
                next_obs = self.aug(next_obs)
                next_obs = self.encoder(next_obs)

        # "Journal teachings"

        offline = replay.offline

        logs = {'time': time.time() - self.birthday, 'step': self.step + offline, 'frame': self.frame + offline,
                'epoch' if offline else 'episode':  self.epoch if offline else self.episode} if self.log \
            else None

        if offline:
            self.step += 1
            self.frame += len(obs)
            self.epoch = replay.epoch

        instruction = ~torch.isnan(label)

        # "Acquire Wisdom"

        # Classification
        if instruction.any():
            # "Via Example" / "Parental Support" / "School"

            # Inference
            y_predicted = self.actor(obs[instruction], self.step).mean

            mistake = cross_entropy(y_predicted, label[instruction].long(), reduction='none')

            # Supervised learning
            if self.supervise:
                # Supervised loss
                supervised_loss = mistake.mean()

                # Update supervised
                Utils.optimize(supervised_loss,
                               self.actor, epoch=self.epoch if offline else self.episode, retain_graph=True)

                if self.log:
                    correct = (torch.argmax(y_predicted, -1) == label[instruction]).float()

                    logs.update({'supervised_loss': supervised_loss.item(),
                                 'accuracy': correct.mean().item()})

            # (Auxiliary) reinforcement
            if self.RL:
                ratio = len(instruction) // (2 + self.third)
                if self.half or self.third:
                    mistake[:ratio] = cross_entropy(y_predicted[:ratio].uniform_(-1, 1),
                                                    label[instruction][:ratio].long(), reduction='none')
                if self.third:
                    y_predicted[-ratio:], mistake[-ratio:] = Utils.one_hot(label[-ratio:], self.action_dim, -1), 0
                action[instruction] = y_predicted.detach()
                reward[instruction] = -mistake[:, None].detach()  # reward = -error
                next_obs[instruction] = float('nan')

        # Reinforcement learning / generative modeling
        if self.RL or self.generate:
            # "Imagine"

            # Generative modeling
            if self.generate:
                half = len(obs) // 2
                generated_image = self.actor(obs[:half], self.step).mean

                action[:half], reward[:half] = generated_image, 0  # Discriminate

            # "Discern"

            # Critic loss
            critic_loss = QLearning.ensembleQLearning(self.critic, self.actor,
                                                      obs, action, reward, discount, next_obs,
                                                      self.step, logs=logs)

            # Update critic
            Utils.optimize(critic_loss,
                           self.critic, epoch=self.epoch if offline else self.episode)

        # Update encoder
        if not self.generate:
            Utils.optimize(None,  # Using gradients from previous losses
                           self.encoder, epoch=self.epoch if offline else self.episode)

        if self.generate or self.RL and not self.discrete:
            # "Change" / "Grow"

            # Actor loss
            actor_loss = PolicyLearning.deepPolicyGradient(self.actor, self.critic, obs.detach(),
                                                           self.step, logs=logs)

            # Update actor
            Utils.optimize(actor_loss,
                           self.actor, epoch=self.epoch if offline else self.episode)

        return logs
