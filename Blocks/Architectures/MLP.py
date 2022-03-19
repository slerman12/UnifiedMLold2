# Copyright (c) AGI.__init__. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# MIT_LICENSE file in the root directory of this source tree.
import copy
import math

import torch
from torch import nn

import Utils


class MLP(nn.Module):
    def __init__(self, input_dim=128, output_dim=1024, hidden_dim=512, depth=1, non_linearity=nn.ReLU(inplace=True),
                 dropout=0, binary=False, l2_norm=False, input_shape=None):
        super().__init__()

        if input_shape is not None:
            input_dim = math.prod(input_shape)
        self.output_dim = output_dim

        self.MLP = nn.Sequential(*[nn.Sequential(
            # Optional L2 norm of penultimate
            # (See: https://openreview.net/pdf?id=9xhgmsNVHu)
            # Similarly, Efficient-Zero initializes 2nd-to-last layer as all 0s  TODO
            Utils.L2Norm() if l2_norm and i == depth else nn.Identity(),
            nn.Linear(input_dim if i == 0 else hidden_dim,
                      hidden_dim if i < depth else output_dim),
            non_linearity if i < depth else nn.Sigmoid() if binary else nn.Identity(),
            nn.Dropout(dropout) if i < depth else nn.Identity()
        )
            for i in range(depth + 1)]
        )

        self.apply(Utils.weight_init)

    def repr_shape(self, *_):
        return self.output_dim, *_[1:]

    def forward(self, *x):
        return self.MLP(torch.cat(x, -1))


class MLPBlock(nn.Module):
    """MLP block:  TODO move to Encoder.py

    With LayerNorm

    Can also l2-normalize penultimate layer (https://openreview.net/pdf?id=9xhgmsNVHu)"""

    def __init__(self, input_dim, output_dim, trunk_dim=512, hidden_dim=512, depth=1, non_linearity=nn.ReLU(inplace=True),
                 layer_norm=False, dropout=0, binary=False, l2_norm=False,
                 lr=None, weight_decay=0, ema_decay=None):
        super().__init__()

        self.trunk = nn.Sequential(nn.Linear(input_dim, trunk_dim),
                                   nn.LayerNorm(trunk_dim),
                                   nn.Tanh()) if layer_norm \
            else None

        in_features = trunk_dim if layer_norm else input_dim

        self.MLP = MLP(in_features, output_dim, hidden_dim, depth, non_linearity, dropout, binary, l2_norm)

        self.init(lr, weight_decay, ema_decay)

    def init(self, lr=None, weight_decay=0, ema_decay=None):
        # Initialize weights
        self.apply(Utils.weight_init)

        # Optimizer
        if lr is not None:
            self.optim = torch.optim.AdamW(self.parameters(), lr=lr, weight_decay=weight_decay)

        # EMA
        if ema_decay is not None:
            self.ema = copy.deepcopy(self).eval()
            self.ema_decay = ema_decay

    def update_ema_params(self):
        assert hasattr(self, 'ema_decay')
        Utils.param_copy(self, self.ema, self.ema_decay)

    def forward(self, *x):
        h = torch.cat(x, -1)

        if self.trunk is not None:
            h = self.trunk(h)

        return self.MLP(h)
