from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim

import torchvision.transforms as transforms
import torchvision.utils as vutils

import numpy as np

from Blocks.Architectures.Vision.DCGAN import Generator, Discriminator

from Blocks.Encoders import CNNEncoder
from Blocks.Actors import EnsemblePiActor
from Blocks.Critics import EnsembleQCritic

from Datasets.Suites._CelebA import CelebA
from Datasets.Suites.Classify import AttrDict

from Losses import QLearning

import Utils

import matplotlib.pyplot as plt


Utils.set_seeds(0)

batch_size = 256
num_epochs = 5
z_dim = 100
lr = 0.0002
beta1 = 0.5
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


dataset = CelebA(root="Datasets/ReplayBuffer/Classify/CelebA_Train/",
                 download=True,
                 transform=transforms.Compose([
                     transforms.Resize(64),
                     transforms.CenterCrop(64),
                     transforms.ToTensor(),
                     # transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),  # Encoder can standardize
                 ]))


dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=2)

obs_spec = AttrDict({'shape': [3, 64, 64], 'mean': 0.5, 'stddev': 0.5, 'low': 0, 'high': 1})
action_spec = AttrDict({'shape': obs_spec.shape, 'discrete_bins': None, 'low': -1, 'high': 1, 'discrete': False})

encoder = CNNEncoder(obs_spec, standardize=True, Eyes=nn.Identity)
actor = EnsemblePiActor(encoder.repr_shape, 100, -1, action_spec, trunk=Utils.Rand, Pi_head=Generator, ensemble_size=1,
                        lr=lr, optim={'_target_': 'Adam', 'betas': [beta1, 0.999]}).to(device)
critic = EnsembleQCritic(encoder.repr_shape, 100, -1, action_spec, Q_head=Discriminator, ensemble_size=1,
                         ignore_obs=True, lr=lr, optim={'_target_': 'Adam', 'betas': [beta1, 0.999]}).to(device)


optimizerG = optim.Adam(actor.parameters(), lr=lr, betas=(beta1, 0.999))
criterion = nn.BCELoss()


for epoch in range(num_epochs):
    for i, (obs, *_) in enumerate(dataloader):

        obs = obs.to(device)
        obs = encoder(obs)

        action_ = actor(obs).mean
        action = torch.cat([obs.view_as(action_), action_], 0)
        reward_ = torch.zeros((len(obs), 1)).to(obs)
        reward = torch.cat([torch.ones_like(reward_), reward_], 0)

        target_Q = reward

        Qs = critic(torch.cat([obs, obs], 0), action)  # Q-ensemble

        # Use BCE if Critic ends with Sigmoid
        # criterion = binary_cross_entropy if critic.binary else mse_loss

        # Temporal difference (TD) error (via MSE or BCE)
        critic_loss = criterion(Qs, target_Q.unsqueeze(1).expand_as(Qs))

        critic_loss.backward()

        critic.optim.step()

        # critic_loss = QLearning.ensembleQLearning(critic, actor, torch.cat([obs, obs], 0), action.detach(), reward, 1, torch.ones(0), 1)

        # Utils.optimize(critic_loss, critic)

        # Discriminate both
        # action_ = actor(obs).mean
        # action = torch.cat([obs.view_as(action_), action_], 0)
        # reward_ = torch.zeros((len(obs), 1)).to(obs)
        # reward = torch.cat([torch.ones_like(reward_), reward_], 0)
        #
        # critic_loss = QLearning.ensembleQLearning(critic, actor, torch.cat([obs, obs], 0), action.detach(), reward, 1, torch.ones(0), 1)
        #
        # Utils.optimize(critic_loss, critic)

        # Discriminate real
        # action_ = actor(obs).mean
        # action = obs.view_as(action_)
        # reward = torch.ones((len(obs), 1)).to(obs)
        # critic_loss = QLearning.ensembleQLearning(critic, actor, obs, action, reward, 1, torch.ones(0), 1)
        #
        # # Utils.optimize(critic_loss, critic)
        #
        # # Discriminate plausible
        # reward = torch.zeros_like(reward)
        # # Action must be detached
        # critic_loss += QLearning.ensembleQLearning(critic, actor, obs, action_.detach(), reward, 1, torch.ones(0), 1)
        #
        # # This is an interesting discovery. Stepping them independently makes a big difference
        # # Intuition - zig-zag is better than contradiction
        # # Alternate - maybe batch size being uneven or halved...
        # # Try: step once but compute gradients separately and add
        # # Nonsense
        # Utils.optimize(critic_loss, critic)  # Note: I wonder if it always helps to train unique classes independently
        #
        # # Generate
        # # action = actor(obs).mean  # Redundant to action_
        # Qs = critic(obs, action_)
        # Q_target = torch.ones_like(Qs)
        # actor_loss = criterion(Qs, Q_target)
        #
        # Utils.optimize(actor_loss, actor)

        if i % 50 == 0:
            print('[%d/%d][%d/%d]' % (epoch, num_epochs, i, len(dataloader)))


obs, *_ = next(iter(dataloader))

plt.figure(figsize=(15, 15))

plt.subplot(1, 2, 1)
plt.axis('off')
plt.title('Real')
plt.imshow(np.transpose(vutils.make_grid(obs[:64].detach(), padding=5, normalize=True).cpu(), (1, 2, 0)))

plt.subplot(1, 2, 2)
plt.axis('off')
plt.title('Plausible Not-Real')
action = actor(obs.to(device)).mean.view_as(obs)
plt.imshow(np.transpose(vutils.make_grid(action[:64].detach(), padding=2, normalize=True).cpu(), (1, 2, 0)))

path = Path('./Benchmarking/DCGAN/AC2Agent/classify/CelebA_1_Video_Image')
path.mkdir(parents=True, exist_ok=True)
plt.savefig(path / 'generated.png')

plt.close()
