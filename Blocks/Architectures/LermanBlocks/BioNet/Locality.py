# Copyright (c) AGI.__init__. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# MIT_LICENSE file in the root directory of this source tree.
import torch
from torch import nn, einsum
from torch.nn import functional as F

from Blocks.Architectures.MultiHeadAttention import SelfAttentionBlock
from Blocks.Architectures.Residual import Residual

import Utils


"""
A custom "where" pathway: Locality stream architectures for BioNet
"""


class Conv2DLocal(nn.Module):
    def __init__(self, input_shape, out_channels, kernel_size, stride=(1, 1), padding=(0, 0), dilation=(1, 1),
                 groups=1, patch_size=16):
        super().__init__()

        LN = lambda: nn.Sequential(Utils.ChSwap, nn.LayerNorm(out_channels), Utils.ChSwap)

        in_channels, height, width = input_shape

        self.conv_in = nn.Sequential(LN(),
                                     nn.Conv2d(in_channels, out_channels * 2, kernel_size, stride, padding, dilation,
                                               groups=groups),
                                     nn.GELU())

        height, width = Utils.cnn_layer_feature_shape(height, width, kernel_size,
                                                      stride, padding, dilation)

        assert height % patch_size == 0 and width % patch_size == 0, 'spatial dims must be divisible by patch size'

        self.ln = LN()

        # Note: Possible to change strides, out_channels to down-sample

        # Twice as time-intensive as fully-disjoint MLP convolution, but orders more memory efficient
        self.localize_h = nn.Conv2d(height, out_channels * height,  # Kernel transforms the height
                                    (1, out_channels), groups=patch_size)  # Over disjoint patches
        self.localize_w = nn.Conv2d(width, out_channels * width,
                                    (1, out_channels), groups=patch_size)

        self.conv_out = nn.Conv2d(out_channels, out_channels, kernel_size, stride, padding, dilation, groups=groups)

    def repr_shape(self, c, h, w):
        return Utils.cnn_feature_shape(c, h, w, self.conv)

    def forward(self, x):
        x = self.ln(self.conv_in(x))

        locality_h = self.localize_h(Utils.ChSwap(x))  # [out_channels * height, width, 1]
        locality_w = self.localize_w(x.transpose(-3, -2).transpose(-2, -1))  # [out_channels * width, height, 1]

        lead_shape = x.shape[:-3]
        patch_size = locality_h.shape[-2]

        # Assuming groups prioritized over channels in Conv2D... does it matter? Yes, want spatial inductive bias
        locality = (locality_h * locality_w).view(*lead_shape, patch_size, -1, patch_size).transpose(-3, -2)

        out = self.conv_out(locality)

        return out + x


class Conv2DLocalized(nn.Module):
    def __init__(self, input_shape, out_channels, kernel_size, stride=(1, 1), padding=(0, 0), dilation=(1, 1),
                 groups=1):
        super().__init__()

        LN = lambda: nn.Sequential(Utils.ChSwap, nn.LayerNorm(out_channels), Utils.ChSwap)

        in_channels, height, width = input_shape

        self.conv_in = nn.Sequential(LN(),
                                     nn.Conv2d(in_channels, out_channels * 2, kernel_size, stride, padding, dilation),
                                     nn.GELU())

        height, width = Utils.cnn_layer_feature_shape(height, width, kernel_size,
                                                      stride, padding, dilation)

        assert height % groups == 0 and width % groups == 0, 'spatial dims must be divisible by groups'

        self.ln = LN()

        self.localize_h = nn.Conv2d(height, out_channels * groups,  # Kernel transforms the height
                                    (width // groups, out_channels), width // groups,  # Over disjoint patches
                                    groups=groups)  # [out_channels * groups, groups, 1]

        self.localize_h = nn.Conv2d(width, out_channels * groups,  # Kernel transforms the height
                                    (height // groups, out_channels), height // groups,  # Over disjoint patches
                                    groups=groups)  # [out_channels * groups, groups, 1]

        self.conv_out = nn.Conv2d(out_channels, out_channels, kernel_size, stride, padding, dilation)

    def feature_shape(self, c, h, w):
        return Utils.cnn_feature_shape(c, h, w, self.conv)

    def forward(self, x):
        x = self.conv_in(x)
        x, locality = x.chunk(2, -3)

        locality = self.ln(locality)

        locality_h = self.localize_h(Utils.ChSwap(locality))
        locality_w = self.localize_w(locality.transpose(-3, -2).transpose(-2, -1))

        locality = locality_h * locality_w

        lead_shape = x.shape[:-3]
        out_channels = x.shape[-3]
        groups = locality_h.shape[-2]
        group_h = x.shape[-2] // groups
        group_w = x.shape[-1] // groups

        locality = locality.view(*lead_shape, out_channels, groups, groups).unsqueeze(-1).unsqueeze(-3)

        x = x.view(*lead_shape, out_channels, groups, group_h, groups, group_w)

        x = x * locality

        x = self.conv_out(x)
        return x
        # x = self.conv(x)
        # x = einsum('b c h w, h w d c, h w d -> b c h w', x, self.linear_W, self.linear_B)
        # x = F.gelu(x)
        # x = self.ln(x)
        # return x


# class Conv2DLocalized(nn.Module):
#     def __init__(self, input_shape, out_channels, kernel_size, stride=(1, 1), padding=(0, 0), dilation=(1, 1),
#                  groups=1, bias=True, padding_mode='zeros'):
#         super().__init__()
#
#         def layer_norm():
#             return nn.Sequential(Utils.ChannelSwap(),
#                                  nn.LayerNorm(out_channels),
#                                  Utils.ChannelSwap())
#
#         in_channels, height, width = input_shape
#
#         self.conv = nn.Sequential(nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding, dilation,
#                                             groups, bias, padding_mode),
#                                   nn.GELU(),
#                                   layer_norm())
#
#         height, width = Utils.cnn_layer_feature_shape(height, width, kernel_size,
#                                                      stride, padding, dilation)
#
#         self.shape = (out_channels, height, width)
#
#         # TODO could also try 'spatial' axis only like gMLP, i.e. spatial conv with groups!
#         #  Compared to gMLP: this is more params but, under sufficiently-parallel hardware, faster
#         self.linear_W = nn.Parameter(torch.empty(height, width, out_channels, out_channels))
#
#         self.linear_B = nn.Parameter(torch.empty(height, width, out_channels))
#
#         self.ln = layer_norm()
#
#     def feature_shape(self, c, h, w):
#         return Utils.cnn_feature_shape(c, h, w, self.conv)
#
#     def forward(self, input):
#         x = self.conv(input)
#         x = einsum('b c h w, h w d c, h w d -> b c h w', x, self.linear_W, self.linear_B)
#         x = F.gelu(x)
#         x = self.ln(x)
#         return x


class LocalityCNN(nn.Module):
    def __init__(self, input_shape, out_channels=32, depth=3):
        super().__init__()

        self.trunk = Conv2DLocalized(input_shape, out_channels, (8, 8))

        self.CNN = nn.Sequential(
            *[Residual(Conv2DLocalized(self.trunk.shape, out_channels, (4, 4), padding='same'))
              for _ in range(depth)])

    def feature_shape(self, c, h, w):
        c, h, w = Utils.cnn_feature_shape(c, h, w, self.trunk)
        return Utils.cnn_feature_shape(c, h, w, self.CNN)

    def forward(self, x):
        return self.CNN(self.trunk(x))


class LocalityViT(nn.Module):
    def __init__(self, input_shape, out_channels=32, depth=3):
        super().__init__()

        self.trunk = Conv2DLocalized(input_shape, out_channels, (16, 16), (16, 16))

        self.ViT = nn.Sequential(
            *[nn.Sequential(Utils.ChannelSwap(), SelfAttentionBlock(out_channels), Utils.ChannelSwap(),
                            Residual(Conv2DLocalized(self.trunk.shape, out_channels, (2, 2), padding='same')))
              for _ in range(depth)])

    def feature_shape(self, c, h, w):
        return Utils.cnn_feature_shape(c, h, w, self.trunk)

    def forward(self, x):
        return self.ViT(self.trunk(x))