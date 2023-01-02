# Copyright (c) AGI.__init__. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# MIT_LICENSE file in the root directory of this source tree.
from torch import nn

from Blocks.Architectures import MLP
from Blocks.Architectures.Vision.ViT import LearnablePositionalEncodings
from Blocks.Architectures.Transformer import LearnableFourierPositionalEncodings, SelfAttentionBlock
from Blocks.Architectures.Residual import Residual
from Blocks.Architectures.Vision.CNN import AvgPool, cnn_broadcast

import Utils


"""NOTE: This architecture implementation is still in progress. Debugging 90% done. This is a SOTA ViT reproduced in 
full simply and elegantly in a short file. Thank you for your understanding."""


class MBConvBlock(nn.Module):
    """MobileNetV2 Block ("MBConv") used originally in EfficientNet. Unlike ResBlock, uses [Narrow -> Wide -> Narrow] 
    structure and depth-wise and point-wise convolutions."""
    def __init__(self, in_channels, out_channels, down_sample=None, stride=1, expansion=4):
        super().__init__()

        hidden_dim = int(in_channels * expansion)  # Width expansion in [Narrow -> Wide -> Narrow]

        if down_sample is None and (in_channels != out_channels or stride != 1):
            down_sample = nn.Sequential(nn.MaxPool2d(3, 2, 1),  # TODO adapt_cnn trigger an illegal reshaping due to pad
                                        nn.Conv2d(in_channels, out_channels, 1, bias=False))

        block = nn.Sequential(
            # Point-wise 
            *[nn.Conv2d(in_channels, hidden_dim, 1, stride, bias=False),
              nn.BatchNorm2d(hidden_dim),
              nn.GELU()] if expansion > 1 else (),

            # Depth-wise
            nn.Conv2d(hidden_dim, hidden_dim, 3, 1 if expansion > 1 else stride, 1, groups=hidden_dim, bias=False),
            nn.BatchNorm2d(hidden_dim),
            nn.GELU(),
            *[nn.AdaptiveAvgPool2d(1),
              Utils.ChSwap, MLP(hidden_dim, hidden_dim, max(in_channels // 4, 1), activation=nn.GELU(), binary=True,
                                bias=False), Utils.ChSwap] if expansion > 1 else (),

            # Point-wise
            nn.Conv2d(hidden_dim, out_channels, 1, bias=False),
            nn.BatchNorm2d(out_channels),
        )

        self.MBConvBlock = Residual(nn.Sequential(nn.BatchNorm2d(in_channels),
                                                  block), down_sample)

    def repr_shape(self, *_):
        return Utils.cnn_feature_shape(_, self.MBConvBlock)

    def forward(self, x):
        return self.MBConvBlock(x)


class CoAtNet(nn.Module):
    """
    An elegant CoAtNet backbone with support for dimensionality adaptivity. Assumes channels-first. Uses a
    general-purpose attention block with learnable fourier coordinates instead of relative coordinates.
    Will include support for relative coordinates eventually.
    """
    def __init__(self, input_shape, dims=(64, 96, 192, 384, 768), depths=(2, 2, 3, 5, 2),
                 num_heads=None, emb_dropout=0.1, query_key_dim=None, mlp_hidden_dim=None, dropout=0.1, fourier=True,
                 output_shape=None):
        super().__init__()

        self.input_shape, output_dim = Utils.to_tuple(input_shape), Utils.prod(output_shape)

        in_channels = self.input_shape[0]

        # Convolution layers
        self.Co = nn.Sequential(*[nn.Sequential(nn.Conv2d(in_channels if i == 0 else dims[0],
                                                          dims[0], 3, 1 + (not i), 1, bias=False),
                                                nn.BatchNorm2d(dims[0]),
                                                nn.GELU()
                                                ) for i in range(depths[0])],
                                *[MBConvBlock(dims[0], dims[1], stride=1 + (not i)) for i in range(depths[1])],
                                *[MBConvBlock(dims[1], dims[2], stride=1 + (not i)) for i in range(depths[2])])

        shape = Utils.cnn_feature_shape(input_shape, self.Co)

        positional_encodings = (LearnableFourierPositionalEncodings if fourier
                                else LearnablePositionalEncodings)(shape)

        reshape = [dims[3], *shape[1:]]  # After down-sampling

        # Positional encoding -> Attention layers with down-sampling nets
        self.At = nn.Sequential(positional_encodings,
                                nn.Dropout(emb_dropout),

                                # Transformer  TODO Should downsample when i == 0
                                *[SelfAttentionBlock(shape, num_heads, None, query_key_dim, mlp_hidden_dim, dropout)
                                  for i in range(depths[3])],
                                *[SelfAttentionBlock(shape,  # TODO should be "reshape" after downsampling
                                                     num_heads, None, query_key_dim, mlp_hidden_dim, dropout)
                                  for i in range(depths[4])],

                                # Can CLS-pool and project to a specified output dim, optional
                                nn.Identity() if output_dim is None else nn.Sequential(AvgPool(),
                                                                                       nn.Linear(dims[3],
                                                                                                 output_dim)))

    def repr_shape(self, *_):
        return Utils.cnn_feature_shape(_, self.Co, self.At)

    def forward(self, *x):
        # Concatenate inputs along channels assuming dimensions allow, broadcast across many possibilities
        lead_shape, x = cnn_broadcast(self.input_shape, x)

        x = self.Co(x)
        x = self.At(x)

        # Restore leading dims
        out = x.view(*lead_shape, *x.shape[1:])
        return out


# For debugging
class Print(nn.Module):
    def forward(self, x):
        print(x.shape)
        return x


class CoAtNet0(CoAtNet):
    """Pseudonym for Default CoAtNet"""


class CoAtNet1(CoAtNet):
    def __init__(self, input_shape, output_shape=None):
        super().__init__(input_shape, [64, 96, 192, 384, 768], [2, 2, 6, 14, 2], output_shape=output_shape)


class CoAtNet2(CoAtNet):
    def __init__(self, input_shape, output_shape=None):
        super().__init__(input_shape, [128, 128, 256, 512, 1026], [2, 2, 6, 14, 2], output_shape=output_shape)


class CoAtNet3(CoAtNet):
    def __init__(self, input_shape, output_shape=None):
        super().__init__(input_shape, [192, 192, 384, 768, 1536], [2, 2, 6, 14, 2], output_shape=output_shape)


class CoAtNet4(CoAtNet):
    def __init__(self, input_shape, output_shape=None):
        super().__init__(input_shape, [192, 192, 384, 768, 1536], [2, 2, 12, 28, 2], output_shape=output_shape)
