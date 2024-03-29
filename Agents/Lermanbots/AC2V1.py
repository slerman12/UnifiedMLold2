# Copyright (c) AGI.__init__. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# MIT_LICENSE file in the root directory of this source tree.
import time
import math

from hydra.utils import instantiate

import torch
from torch.nn.functional import cross_entropy

import Utils

from Blocks.Augmentations import IntensityAug, RandomShiftsAug
from Blocks.Encoders import CNNEncoder
from Blocks.Actors import EnsemblePiActor, CategoricalCriticActor
from Blocks.Critics import EnsembleQCritic

from Losses import QLearning, PolicyLearning


class AC2Agent(torch.nn.Module):
    """Actor Critic Creator (AC2)
    Does ensemble-learning with multiple critics and actors, for RL, classification, and generative modeling"""
    def __init__(self,
                 obs_shape, action_shape, trunk_dim, hidden_dim, data_stats, recipes,  # Architecture
                 lr, weight_decay, ema_decay, ema,  # Optimization
                 explore_steps, stddev_schedule, stddev_clip,  # Exploration
                 discrete, RL, supervise, generate, device, parallel, log,  # On-boarding
                 num_actors=5, num_actions=1, num_critics=2):  # AC2
        super().__init__()

        self.discrete = discrete and not generate  # Continuous supported!
        self.supervise = supervise  # And classification...
        self.RL = RL
        self.generate = generate  # And generative modeling, too
        self.device = device
        self.log = log
        self.birthday = time.time()
        self.step = self.episode = 0
        self.explore_steps = explore_steps
        self.ema = ema
        self.action_dim = math.prod(obs_shape) if generate else action_shape[-1]

        self.num_actors, self.num_actions = num_actors, num_actions  # Num actors in ensemble, actions sampled per actor

        self.encoder = Utils.Rand(trunk_dim) if generate \
            else CNNEncoder(obs_shape, data_stats=data_stats, recipe=recipes.encoder, parallel=parallel,
                            lr=lr, weight_decay=weight_decay, ema_decay=ema_decay if ema else None)

        repr_shape = (trunk_dim,) if generate \
            else self.encoder.repr_shape

        # Continuous actions
        self.actor = None if self.discrete \
            else EnsemblePiActor(repr_shape, trunk_dim, hidden_dim, self.action_dim, recipes.actor,
                                 ensemble_size=num_actors,
                                 stddev_schedule=stddev_schedule, stddev_clip=stddev_clip,
                                 lr=lr, weight_decay=weight_decay, ema_decay=ema_decay if ema else None)

        self.critic = EnsembleQCritic(repr_shape, trunk_dim, hidden_dim, self.action_dim, recipes.critic,
                                      ensemble_size=num_critics, discrete=self.discrete, ignore_obs=generate,
                                      lr=lr, weight_decay=weight_decay, ema_decay=ema_decay)

        self.creator = CategoricalCriticActor(stddev_schedule)

        # Image augmentation
        self.aug = instantiate(recipes.aug) if recipes.Aug is not None \
            else IntensityAug(0.05) if discrete else RandomShiftsAug(pad=4)

        # Birth

    def act(self, obs):
        with torch.no_grad(), Utils.act_mode(self.encoder, self.actor, self.critic):
            obs = torch.as_tensor(obs, device=self.device)

            # EMA targets
            encoder = self.encoder.ema if self.ema and not self.generate else self.encoder
            actor = self.actor.ema if self.ema and not self.discrete else self.actor

            # "See"
            obs = encoder(obs)

            actions = None if self.discrete \
                else actor(obs, self.step).sample(self.num_actions) if self.training \
                else actor(obs, self.step).mean

            # DQN action selector is based on critic
            Pi = self.creator(self.critic(obs, actions), self.step)

            action = Pi.sample() if self.training \
                else Pi.best

            if self.training:
                self.step += 1

                # Explore phase
                if self.step < self.explore_steps and not self.generate:
                    action = torch.randint(self.action_dim, size=action.shape) if self.discrete \
                        else action.uniform_(-1, 1)

            return action

    # "Dream"
    def learn(self, replay):
        # "Recollect"

        batch = next(replay)
        obs, action, reward, discount, next_obs, label, *traj, step = Utils.to_torch(
            batch, self.device)

        # Actor-Critic -> Generator-Discriminator conversion
        if self.generate:
            action, reward[:] = obs.flatten(-3) / 127.5 - 1, 1
            next_obs[:] = label[:] = float('nan')

        # "Envision" / "Perceive"

        # Augment and encode
        obs = self.aug(obs)
        obs = self.encoder(obs)

        # Augment and encode future
        if replay.nstep > 0 and not self.generate:
            with torch.no_grad():
                next_obs = self.aug(next_obs)
                next_obs = self.encoder(next_obs)

        # "Journal teachings"

        logs = {'time': time.time() - self.birthday,
                'step': self.step, 'episode': self.episode} if self.log \
            else None

        instruction = ~torch.isnan(label)

        # "Acquire Wisdom"

        # Classification
        if instruction.any():
            # "Via Example" / "Parental Support" / "School"

            # Inference
            candidates = self.actor(obs[instruction], self.step).mean
            y_predicted = self.creator(self.critic(obs[instruction], candidates), self.step).best

            mistake = cross_entropy(y_predicted, label[instruction].long(), reduction='none')

            # Supervised learning
            if self.supervise:
                # Supervised loss
                supervised_loss = mistake.mean()

                # Update supervised
                Utils.optimize(supervised_loss,
                               self.actor, retain_graph=True)

                if self.log:
                    correct = (torch.argmax(y_predicted, -1) == label[instruction]).float()

                    logs.update({'supervised_loss': supervised_loss.item(),
                                 'accuracy': correct.mean().item()})

            # (Auxiliary) reinforcement
            half = len(instruction) // 2
            mistake[:half] = cross_entropy(y_predicted[:half].uniform_(-1, 1),
                                           label[instruction][:half].long(), reduction='none')
            action[instruction] = y_predicted.detach()
            reward[instruction] = -mistake[:, None].detach()  # reward = -error
            next_obs[instruction] = float('nan')

        # "Imagine"

        # Generative modeling
        if self.generate:
            half = len(obs) // 2
            candidates = self.actor(obs[:half], self.step).mean
            generated_image = self.creator(self.critic(obs[:half], candidates), self.step).best

            action[:half], reward[:half] = generated_image, 0  # Discriminate

        # "Discern"

        # Critic loss
        critic_loss = QLearning.ensembleQLearning(self.critic, self.actor,
                                                  obs, action, reward, discount, next_obs,
                                                  self.step, self.num_actions, logs=logs)

        # Update critic
        Utils.optimize(critic_loss,
                       self.critic)

        # Update encoder
        if not self.generate:
            Utils.optimize(None,  # Using gradients from previous losses
                           self.encoder)

        # Reinforcement learning / generative modeling
        if self.RL and not self.discrete or self.generate:
            # "Change" / "Grow"

            # Actor loss
            actor_loss = PolicyLearning.deepPolicyGradient(self.actor, self.critic, obs.detach(),
                                                           self.step, self.num_actions, logs=logs)

            # Update actor
            Utils.optimize(actor_loss,
                           self.actor)

        return logs
