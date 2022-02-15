# Copyright (c) AGI.__init__. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# MIT_LICENSE file in the root directory of this source tree.
import torch
from torch import nn

import Utils

from Blocks.Architectures.Residual import Residual


class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1, down_sample=None):
        super().__init__()

        pre_residual = nn.Sequential(nn.Conv2d(in_channels, out_channels,
                                               kernel_size=3, padding=1, stride=stride, bias=False),
                                     nn.BatchNorm2d(out_channels),
                                     nn.ReLU(inplace=True),
                                     nn.Conv2d(out_channels, out_channels,
                                               kernel_size=3, padding=1, bias=False),
                                     nn.BatchNorm2d(out_channels))

        self.Residual_block = nn.Sequential(Residual(pre_residual, down_sample),
                                            nn.ReLU(inplace=True))

    def feature_shape(self, h, w):
        return Utils.cnn_feature_shape(h, w, self.Residual_block)

    def forward(self, x):
        return self.Residual_block(x)


class MiniResNet(nn.Module):
    def __init__(self, input_shape, hidden_channels=32, out_channels=32, depth=3, pre_residual=False, output_dim=None):
        super().__init__()

        in_channels = input_shape[0]

        pre = nn.Sequential(nn.Conv2d(in_channels, hidden_channels, kernel_size=3, padding=1),
                            nn.BatchNorm2d(hidden_channels))

        # Add a concurrent stream to pre
        if pre_residual:
            pre = Residual(pre, down_sample=nn.Sequential(nn.Conv2d(in_channels, hidden_channels,
                                                                    kernel_size=3, padding=1),
                                                          nn.BatchNorm2d(hidden_channels)))

        # CNN ResNet-ish
        self.CNN = nn.Sequential(pre,
                                 nn.ReLU(inplace=True),  # MaxPool after this?
                                 *[ResidualBlock(hidden_channels, hidden_channels)
                                   for _ in range(depth)],
                                 nn.Conv2d(hidden_channels, out_channels, kernel_size=3, padding=1),
                                 nn.ReLU(inplace=True),
                                 nn.Sequential(nn.AdaptiveAvgPool2d((1,1)),
                                               nn.Flatten(),
                                               nn.Linear(out_channels, output_dim)) if output_dim is not None
                                 else nn.Identity())

    def feature_shape(self, h, w):
        return Utils.cnn_feature_shape(h, w, self.CNN)

    def forward(self, *x):
        # x = list(x)
        # x[0] = x[0].view(-1, *self.input_shape)
        #
        # # Optionally append context to channels assuming dimensions allow
        # if len(x) > 1:
        #     x[1:] = [context.reshape(x[0].shape[0], context.shape[-1], 1, 1).expand(-1, -1, *self.input_shape[1:])
        #              for context in x[1:]]

        x = torch.cat(x, 1)
        print(x.shape)
        return self.CNN(x)
