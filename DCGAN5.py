# Template created by Sam Lerman, slerman@ur.rochester.edu.

from pathlib import Path

import matplotlib.pyplot as plt

import numpy as np

import torch
import torch.nn as nn
from torch.optim import Adam

import torchvision.transforms as transforms
import torchvision.utils as vutils
from CelebA import CelebA
# from torchvision.datasets.celeba import CelebA

from Discriminator import Discriminator
from Generator import Generator


torch.manual_seed(0)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(0)

batch_size = 128
num_epochs = 5
z_dim = 100
lr = 0.0002
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


dataset = CelebA(root="Datasets/ReplayBuffer/Classify/CelebA_Train/",
                 download=True,
                 transform=transforms.Compose([
                     transforms.Resize(64),
                     transforms.CenterCrop(64),
                     transforms.ToTensor(),
                     transforms.Normalize([0.5083452463150024, 0.42242321372032166, 0.37688034772872925],
                                          [0.30580446124076843, 0.2835234999656677, 0.28196951746940613])
                 ]))


dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=2)

discriminator = Discriminator().to(device)
generator = Generator().to(device)

criterion = nn.MSELoss()  # BCE sometimes causes CUDA errors. Idk why.

discriminator_optim = Adam(discriminator.parameters(), lr=lr, betas=(0.5, 0.999))  # Less momentum = 0.5
generator_optim = Adam(generator.parameters(), lr=lr)  # Slowing the Actor compared to the Critic


for epoch in range(num_epochs):
    for i, (obs, *_) in enumerate(dataloader):

        rand = torch.randn((len(obs), z_dim, 1, 1), device=device)
        action_ = generator(rand)

        action = torch.cat([obs.view_as(action_).to(device), action_], 0)  # Doesn't work. Hypoth. Reason: Batch norm.

        Qs = discriminator(action)
        reward = torch.zeros_like(Qs)
        reward[:len(obs)] = 1.0
        Q_target = reward

        loss = criterion(Qs, Q_target)

        discriminator_optim.zero_grad()
        generator_optim.zero_grad()
        loss.backward()
        discriminator_optim.step()
        # if i % 2 == 0:
        for param in generator.parameters():
            param.grad *= -2
        generator_optim.step()  # Doesn't work?  Maybe do this step once every two updates
        # My reason: The Actor is only as good as the Critic. If the Actor is as good as the Critic, then the Actor
        #   has nowhere to go. Those vanishing gradients lead to stagnation.

        if i % 50 == 0:
            print('[%d/%d][%d/%d]' % (epoch, num_epochs, i, len(dataloader)))


plt.figure(figsize=(15, 15))

plt.subplot(1, 2, 1)
plt.axis('off')
plt.title('Real')
plt.imshow(np.transpose(vutils.make_grid(obs[:64].detach(), padding=5, normalize=True).cpu(), (1, 2, 0)))

plt.subplot(1, 2, 2)
plt.axis('off')
plt.title('Plausible Not-Real')
action = generator(rand).view_as(obs)
plt.imshow(np.transpose(vutils.make_grid(action[:64].detach(), padding=2, normalize=True).cpu(), (1, 2, 0)))

path = Path('./Benchmarking/DCGAN/AC2Agent/classify/CelebA_1_Video_Image')
path.mkdir(parents=True, exist_ok=True)
plt.savefig(path / 'generated2.png')

plt.close()
