# Copyright (c) AGI.__init__. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# MIT_LICENSE file in the root directory of this source tree.
import time
import warnings

import torch
from torch.nn.functional import cross_entropy

from Blocks.Architectures import MLP, Residual
from Blocks.Architectures.Vision.CNN import CNN
from Blocks.Architectures.Vision.ResNet import MiniResNet

import Utils

from Blocks.Augmentations import RandomShiftsAug
from Blocks.Encoders import CNNEncoder
from Blocks.Actors import EnsemblePiActor, CategoricalCriticActor
from Blocks.Critics import EnsembleQCritic

from Losses import QLearning, PolicyLearning, SelfSupervisedLearning


class AC2Agent(torch.nn.Module):
    """Actor Critic Creator (AC2) - Best of all worlds (paper link)
    Dynamics-learning w/ multiple critics/actors for RL, classification, and generative modeling; deux-sampling"""
    def __init__(self,
                 obs_spec, action_spec, num_actions, trunk_dim, hidden_dim, standardize, norm, recipes,  # Architecture
                 lr, lr_decay_epochs, weight_decay, ema_decay, ema,  # Optimization
                 explore_steps, stddev_schedule, stddev_clip,  # Exploration
                 discrete, RL, supervise, generate, device, parallel, log,  # On-boarding
                 num_critics=2, num_actors=1, depth=0  # AC2
                 ):
        super().__init__()

        self.discrete = discrete and not generate  # Continuous supported!
        self.supervise = supervise  # And classification...
        self.RL = RL or generate
        self.generate = generate  # And generative modeling, too
        self.device = device
        self.log = log
        self.birthday = time.time()
        self.step = self.frame = 0
        self.episode = self.epoch = 1
        self.explore_steps = explore_steps
        self.ema = ema

        self.num_actions = num_actions
        self.num_actors = max(num_critics, num_actors) if self.discrete and self.RL else num_actors

        self.depth = depth  # Dynamics prediction depth

        # Image augmentation
        self.aug = Utils.instantiate(recipes.aug) or RandomShiftsAug(pad=4)

        # RL -> generate conversion
        if self.generate:
            standardize = False
            norm = True  # Normalize Obs to range [-1, 1]

            # Action = Imagined Obs
            action_spec.update({'shape': obs_spec.shape, 'discrete_bins': None,
                                'low': -1, 'high': 1, 'discrete': False})

            # Remove encoder, replace trunk with random noise
            recipes.encoder.Eyes = torch.nn.Identity()  # Generate "imagines" — no need for "seeing" with Eyes
            recipes.actor.trunk = Utils.Rand(size=trunk_dim)  # Generator observes random Gaussian noise as input

        self.discrete_as_continuous = action_spec.discrete and not self.discrete

        # Discrete -> continuous conversion
        if self.discrete_as_continuous:
            # Normalizing actions to range [-1, 1] significantly helps continuous RL
            action_spec.low, action_spec.high = (-1, 1) if self.RL else (None, None)

        # Continuous -> discrete conversion
        if self.discrete and not action_spec.discrete:
            assert self.num_actions > 1, 'Num actions cannot be 1 when discrete; try the "num_actions=" flag (>1) to ' \
                                         'divide each action dimension into discrete bins, or specify "discrete=false".'

            action_spec.discrete_bins = self.num_actions  # Continuous env has no discrete bins by default, must specify

        self.encoder = CNNEncoder(obs_spec, standardize=standardize, norm=norm, **recipes.encoder, parallel=parallel,
                                  lr=lr, lr_decay_epochs=lr_decay_epochs, weight_decay=weight_decay, ema_decay=ema_decay)

        self.actor = EnsemblePiActor(self.encoder.repr_shape, trunk_dim, hidden_dim, action_spec, **recipes.actor,
                                     ensemble_size=self.num_actors,
                                     discrete=self.discrete, stddev_schedule=stddev_schedule, stddev_clip=stddev_clip,
                                     lr=lr, lr_decay_epochs=lr_decay_epochs, weight_decay=weight_decay,
                                     ema_decay=ema_decay * ema)

        # Dynamics
        if self.depth and not self.generate:
            in_shape = list(self.encoder.feature_shape)
            in_shape[0] += self.action_dim  # Predicting from obs and action

            cnn = Residual(CNN(in_shape, self.encoder.feature_shape[0], padding=1, stride=1, depth=2))

            # Action -> One-Hot, if single-dim discrete, otherwise action shape
            self.action_dim = action_spec.discrete_bins if self.discrete and action_spec.shape == (1,) \
                else self.actor.num_actions * self.actor.action_dim if self.discrete_as_continuous \
                else self.actor.action_dim

            self.dynamics = CNNEncoder(self.encoder.feature_shape, context_dim=self.action_dim,  # TODO Debug
                                       Eyes=cnn, parallel=parallel,
                                       lr=lr, lr_decay_epochs=lr_decay_epochs, weight_decay=weight_decay)

            # Self supervisors
            self.projector = CNNEncoder(self.encoder.feature_shape,
                                        Eyes=MLP(self.encoder.feature_shape, hidden_dim, hidden_dim, 2),
                                        lr=lr, lr_decay_epochs=lr_decay_epochs, weight_decay=weight_decay,
                                        ema_decay=ema_decay)

            self.predictor = CNNEncoder(self.projector.repr_shape,
                                        Eyes=MLP(self.projector.repr_shape, hidden_dim, hidden_dim, 2),
                                        lr=lr, lr_decay_epochs=lr_decay_epochs, weight_decay=weight_decay)

        # When discrete, Critic <- Actor
        if self.discrete:
            recipes.critic.trunk = self.actor.trunk
            recipes.critic.Q_head = self.actor.Pi_head.ensemble

        self.critic = EnsembleQCritic(self.encoder.repr_shape, trunk_dim, hidden_dim, action_spec, **recipes.critic,
                                      ensemble_size=self.num_actors if self.discrete else num_critics,
                                      discrete=self.discrete, ignore_obs=self.generate,
                                      lr=lr, lr_decay_epochs=lr_decay_epochs, weight_decay=weight_decay,
                                      ema_decay=ema_decay)

        self.creator = CategoricalCriticActor(stddev_schedule)

        # Birth

    def act(self, obs):
        with torch.no_grad(), Utils.act_mode(self.encoder, self.actor, self.critic):
            obs = torch.as_tensor(obs, device=self.device).float()

            # Exponential moving average (EMA) shadows
            encoder = self.encoder.ema if self.ema else self.encoder
            actor = self.actor.ema if self.ema else self.actor
            critic = self.critic.ema if self.ema else self.critic

            # See
            obs = encoder(obs)

            # Act
            Pi = actor(obs, self.step)

            action = Pi.sample(self.num_actions) if self.training \
                else Pi.best if self.discrete \
                else Pi.mean

            # Select among candidate actions based on Q-value
            if self.num_actors > 1 and not self.discrete or self.training and self.num_actions > 1:
                All_Qs = getattr(Pi, 'All_Qs', None)  # Discrete Actor policy already knows all Q-values

                Psi = self.creator(critic(obs, action, All_Qs), self.step, action)

                action = Psi.sample() if self.training \
                    else Psi.best

            store = {}

            if self.training:
                self.step += 1
                self.frame += len(obs)

                if self.step < self.explore_steps and not self.generate:
                    # Explore
                    action.uniform_(actor.low or 1, actor.high or 9)  # Env will automatically round if discrete

                store = {'action': action.cpu().numpy()}  # Store action logits

                if self.discrete_as_continuous:  # Re-sample, however store logits
                    action = self.creator(action.transpose(-1, -2), self.step).sample()

            store.update({'step': self.step})

            return action, store

    # "Dream"
    def learn(self, replay):
        # "Recollect"

        batch = replay.sample(trajectories=True)
        obs, action, reward, discount, next_obs, label, *traj, step, ids, meta = Utils.to_torch(
            batch, self.device)
        traj_o, traj_a, traj_r, traj_l = traj

        # "Envision" / "Perceive"

        # Augment, encode present
        obs = self.aug(obs)
        features = self.encoder(obs, pool=False)
        obs = self.encoder.pool(features)

        if replay.nstep > 0 and not self.generate:
            with torch.no_grad():
                # Augment, encode future
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

        instruct = not self.generate and ~torch.isnan(label).any()

        # "Acquire Wisdom"

        # Classification
        if instruct:
            # "Via Example" / "Parental Support" / "School"

            # Inference
            Pi = self.actor(obs)

            y_predicted = (Pi.All_Qs if self.discrete else Pi.mean).mean(1)  # Average over ensembles

            mistake = cross_entropy(y_predicted, label.long(), reduction='none')
            correct = (y_predicted.argmax(1) == label).float()
            accuracy = correct.mean()

            if self.log:
                logs.update({'accuracy': accuracy})

            # Supervised learning
            if self.supervise:
                # Supervised loss
                supervised_loss = mistake.mean()

                # Update supervised
                Utils.optimize(supervised_loss,
                               self.actor, epoch=self.epoch if offline else self.episode, retain_graph=True)

                if self.log:
                    logs.update({'supervised_loss': supervised_loss})

            # (Auxiliary) reinforcement
            if self.RL:
                half = len(obs) // 2
                mistake[:half] = cross_entropy(y_predicted[:half].uniform_(-1, 1),
                                               label[:half].long(), reduction='none')
                action = (y_predicted.argmax(1, keepdim=True) if self.discrete else y_predicted).detach()
                reward = -mistake.detach()  # reward = -error
                next_obs[:] = float('nan')

                if self.log:
                    logs.update({'reward': reward})

        # Reinforcement learning / generative modeling
        if self.RL:
            # "Imagine"

            # Generative modeling
            if self.generate:
                half = len(obs) // 2

                actions = self.actor(obs[:half]).mean

                generated_image = (actions if self.num_actors == 1
                                   else self.creator(self.critic(obs[:half], actions), 1, actions).best).flatten(1)

                action, reward[:] = obs, 1  # "Real"
                action[:half], reward[:half] = generated_image, 0  # Discriminate "fake"

                next_obs[:] = float('nan')

            # "Discern"

            # Critic loss
            critic_loss = QLearning.ensembleQLearning(self.critic, self.actor,
                                                      obs, action, reward, discount, next_obs,
                                                      self.step, self.num_actions, logs=logs)

            # Can only predict dynamics from available trajectories
            if self.depth > replay.nstep:
                warnings.warn(f"Dynamics 'depth' cannot exceed trajectory 'nstep'. Lowering 'depth' to {replay.nstep}. "
                              f"You can increase 'nstep' with the 'nstep={self.depth}' flag.")
                self.depth = replay.nstep

            # Dynamics loss
            dynamics_loss = 0 if self.depth == 0 or self.generate \
                else SelfSupervisedLearning.dynamicsLearning(features, traj_o, traj_a, traj_r,
                                                             self.encoder, self.dynamics, self.projector,
                                                             self.predictor, depth=self.depth,
                                                             action_dim=self.action_dim, logs=logs)

            models = () if self.generate or not self.depth else (self.dynamics, self.projector, self.predictor)

            # Update critic, dynamics
            Utils.optimize(critic_loss + dynamics_loss,
                           self.critic, *models,
                           epoch=self.epoch if offline else self.episode)

        # Update encoder
        Utils.optimize(None,  # Using gradients from previous losses
                       self.encoder, epoch=self.epoch if offline else self.episode)

        if self.RL and not self.discrete:
            # "Change" / "Grow"

            # Actor loss
            actor_loss = PolicyLearning.deepPolicyGradient(self.actor, self.critic, obs.detach(),
                                                           self.step, self.num_actions, logs=logs)

            # Update actor
            Utils.optimize(actor_loss,
                           self.actor, epoch=self.epoch if offline else self.episode)

        return logs
