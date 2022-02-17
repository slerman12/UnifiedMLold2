# Copyright (c) AGI.__init__. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# MIT_LICENSE file in the root directory of this source tree.
import torch
from torch import nn
from torch import einsum

import copy
from einops import rearrange

from Blocks.Architectures.MLP import MLP

import Utils


class CrossAttention(nn.Module):
    def __init__(self, dim=32, heads=8, context_dim=None, talk_h=False):
        super().__init__()

        assert dim % heads == 0
        self.dim = dim
        self.heads = heads

        context_dim = dim if context_dim is None \
            else context_dim

        self.to_q = nn.Linear(dim, dim, bias=False)
        self.to_kv = nn.Linear(context_dim, dim * 2, bias=False)

        # "Talking heads" (https://arxiv.org/abs/2003.02436)
        self.talk_h = nn.Sequential(Utils.ChannelSwap(),
                                    nn.Linear(heads, heads, bias=False),
                                    nn.LayerNorm(heads), Utils.ChannelSwap()) if talk_h else nn.Identity()

    def forward(self, x, context):
        # Conserves shape
        shape = x.shape
        assert shape[-1] == self.dim

        x = x.flatten(1, -2)
        context = context.flatten(1, -2)

        q = self.to_q(x)
        k, v = self.to_kv(context).chunk(2, dim=-1)

        q, k, v = map(lambda t: rearrange(t, 'b n (h d) -> b h n d', h=self.heads), (q, k, v))

        dots = einsum('b h i d, b h j d -> b h i j', q, k) * self.dim ** -0.5

        attn = dots.softmax(dim=-1)

        # "Talking heads"
        attn = self.talk_h(attn)

        out = einsum('b h i j, b h j d -> b h i d', attn, v)
        out = rearrange(out, 'b h n d -> b n (h d)')

        # Restores original shape
        return out.view(shape)


class SelfAttention(CrossAttention):
    def forward(self, x, *args):
        return super().forward(x, x)


class CrossAttentionBlock(nn.Module):
    def __init__(self, dim=32, heads=8, context_dim=None, talk_h=False, optim_lr=None, ema_tau=None):
        super().__init__()

        self.dim = dim
        self.heads = heads

        self.ln1 = nn.LayerNorm(dim)
        self.ln2 = nn.LayerNorm(dim)
        self.attn = CrossAttention(dim, heads, context_dim, talk_h)
        self.mlp = MLP(dim, dim, dim, 2, nn.GELU())

        self.init(optim_lr, ema_tau)

    def init(self, optim_lr=None, ema_tau=None):
        # Initialize weights
        self.apply(Utils.weight_init)

        # Optimizer
        if optim_lr is not None:
            self.optim = torch.optim.Adam(self.parameters(), lr=optim_lr)

        # EMA
        if ema_tau is not None:
            self.ema = copy.deepcopy(self)
            self.ema_tau = ema_tau

    def forward(self, x, context):
        attn = self.ln1(self.attn(x, context)) + x
        out = self.ln2(self.mlp(attn)) + attn

        return out


class SelfAttentionBlock(CrossAttentionBlock):
    def forward(self, x, *_):
        return super().forward(x, x)


class AttentionPool(nn.Module):
    def __init__(self, channels_in=32, heads=4, output_dim=None, input_shape=None):
        super().__init__()

        channels_in = Utils.default(input_shape, [channels_in])[-1]

        self.pool = nn.Sequential(Utils.ChannelSwap(),
                                  SelfAttentionBlock(dim=channels_in, heads=heads),
                                  Utils.ChannelSwap(),
                                  nn.AdaptiveAvgPool2d((1, 1)),
                                  nn.Flatten(),
                                  nn.Linear(channels_in, channels_in if output_dim is None else output_dim))

    def forward(self, x):
        return self.pool(x)
