# Copyright (c) AGI.__init__. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# MIT_LICENSE file in the root directory of this source tree.
from Blocks.Architectures.MLP import MLP
from Blocks.Architectures.MultiHeadAttention import AttentionPool
from Blocks.Architectures.Vision.ViT import CLSPool
from Blocks.Architectures.Vision.CNN import CNN
from Blocks.Architectures.Vision.ViT import ViT
from Blocks.Architectures.Vision.ResNet import MiniResNet, ResNet18, ResNet50
from Blocks.Architectures.Vision.ResNet import MiniResNet as ResNet
from Blocks.Architectures.Vision.ConvMixer import ConvMixer
from Blocks.Architectures.Vision.ConvNeXt import ConvNeXt, ConvNeXtTiny
from Blocks.Architectures.Vision.ViPer import ViPer


from torch import nn
from torch.nn import functional as F


class Null(nn.Module):
    def __init__(self, input_shape=None, **_):
        super().__init__()

        self.input_shape = input_shape
        self.output_dim = None

    def repr_shape(self, c, h, w):
        return c, h, w

    def forward(self, x):
        return x


class AvgPool(nn.Module):
    def repr_shape(self, c, h, w):
        return c, 1, 1

    def forward(self, x):
        return F.adaptive_avg_pool2d(x, (1, 1)).flatten(-3)
