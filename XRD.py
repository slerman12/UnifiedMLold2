import math
import os
import random
from collections.abc import Iterable

import numpy as np

import torch
from torch import nn
from torch.utils.data import Dataset

# from torchaudio.transforms import Spectrogram  # Failed on my MacBook for some reason
from torchvision.transforms import Compose, ToPILImage


class NoPoolCNN(nn.Module):
    def __init__(self, input_shape=(1,)):
        super().__init__()

        in_channels = input_shape if isinstance(input_shape, int) else \
            input_shape[0]

        self.CNN = \
            nn.Sequential(
                nn.Conv2d(in_channels, 80, 100, 5),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Conv2d(80, 80, 50, 5),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Conv2d(80, 80, 25, 2),
                nn.ReLU(),
                nn.Dropout(0.3),
            )

    def forward(self, obs):
        return self.CNN(obs)


class CNN(nn.Module):
    def __init__(self, input_shape=(1,)):
        super().__init__()

        in_channels = input_shape if isinstance(input_shape, int) else \
            input_shape[0]

        self.CNN = \
            nn.Sequential(
                nn.Conv2d(in_channels, 80, 100, 5),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.AvgPool2d(3, 2),
                nn.Conv2d(80, 80, 50, 5),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.AvgPool2d(3),
                nn.Conv2d(80, 80, 25, 2),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.AvgPool2d(3),
            )

    def forward(self, obs):
        return self.CNN(obs)


class Predictor(nn.Module):
    def __init__(self, input_shape=(1024,), output_dim=7):
        super().__init__()

        input_dim = input_shape if isinstance(input_shape, int) \
            else math.prod(input_shape)

        self.MLP = nn.Sequential(nn.Flatten(),
                                 nn.Linear(input_dim, 2300), nn.ReLU(), nn.Dropout(0.5),
                                 nn.Linear(2300, 1150), nn.ReLU(), nn.Dropout(0.5),
                                 nn.Linear(1150, output_dim))

    def forward(self, obs):
        return self.MLP(obs)


class MLP(nn.Module):
    def __init__(self, input_shape=(8500,), output_dim=7):
        super().__init__()

        in_channels = input_shape if isinstance(input_shape, int) \
            else math.prod(input_shape)

        self.MLP = nn.Sequential(nn.Flatten(),
                                 nn.Linear(in_channels, 4000), nn.ReLU(), nn.Dropout(0.6),
                                 nn.Linear(4000, 3000), nn.ReLU(), nn.Dropout(0.5),
                                 nn.Linear(3000, 1000), nn.ReLU(), nn.Dropout(0.4),
                                 nn.Linear(1000, 800), nn.ReLU(), nn.Dropout(0.3),
                                 nn.Linear(800, output_dim))

    def forward(self, obs):
        return self.MLP(obs)


# CPU-memory
# Easy local test:
# python Run.py task=classify/custom Dataset=XRD.XRD +dataset.roots='[Datasets/XRD/rruff/XY_DIF_noiseAll/]' Aug=Identity
class XRD(Dataset):
    def __init__(self, roots=('../XRDs/icsd_Datasets/icsd171k_mix/',), train=True, train_eval_splits=(0.9,),
                 num_classes=7, seed=0, transform=None, spectrogram=False, **kwargs):

        if not isinstance(roots, Iterable):
            roots = (roots,)
        if not isinstance(train_eval_splits, Iterable):
            train_eval_splits = (train_eval_splits,)

        assert len(roots) == len(train_eval_splits), 'Must provide train test split for each root dir'

        self.indices = []
        self.features = {}
        self.labels = {}

        for i, (root, split) in enumerate(zip(roots, train_eval_splits)):
            if not os.path.exists(root):
                pass  # <Download from Hugging Face>

            features_path = root + "features.csv"
            label_path = root + f"labels{num_classes}.csv"

            self.classes = list(range(num_classes))

            print(f'Loading [root={root}, split={split if train else 1 - split}, train={train}] to CPU...')

            # Store on CPU
            with open(features_path, "r") as f:
                self.features[i] = f.readlines()
            with open(label_path, "r") as f:
                self.labels[i] = f.readlines()
                full_size = len(self.labels[i])

            print('Data loaded ✓')

            train_size = round(full_size * split)

            full = range(full_size)

            # Each worker shares an indexing scheme
            random.seed(seed)
            train_indices = random.sample(full, train_size)
            eval_indices = set(full).difference(train_indices)

            indices = train_indices if train else eval_indices
            self.indices += zip([i] * len(indices), list(indices))

        self.transform = transform

        if spectrogram:
            self.spectrogram = Compose([Spectrogram(), ToPILImage()])

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, idx):
        root, idx = self.indices[idx]

        x = torch.FloatTensor(list(map(float, self.features[root][idx].strip().split(','))))
        y = np.array(list(map(float, self.labels[root][idx].strip().split(',')))).argmax()

        if hasattr(self, 'spectrogram'):
            x = self.spectrogram(x)

        # Data transforms
        if self.transform is not None:
            x = self.transform(x)

        return x, y


# python Run.py task=classify/custom Dataset=XRD.XRD +dataset.roots='[Datasets/XRD/rruff/XY_DIF_noiseAll/]' Aug=Identity Eyes=CoAtNet '+eyes.depths=[1,1,1,1,1]' '+eyes.dims=[2,2,2,2,2]'