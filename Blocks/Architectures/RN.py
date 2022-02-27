# Copyright (c) AGI.__init__. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# MIT_LICENSE file in the root directory of this source tree.
import torch
from torch import nn

from Blocks.Architectures import MLP


class RN(nn.Module):
    """Relation Network https://arxiv.org/abs/1706.01427"""
    def __init__(self, dim, context_dim=None, inner_depth=3, outer_depth=2, hidden_dim=None,
                 output_dim=None, input_shape=None, mid_nonlinearity=nn.Identity()):
        super().__init__()

        if input_shape is not None:
            dim = input_shape[-3]

        if context_dim is None:
            context_dim = dim

        if hidden_dim is None:
            hidden_dim = dim

        self.output_dim = dim if output_dim is None \
            else output_dim

        self.inner = MLP(dim + context_dim, hidden_dim, hidden_dim, inner_depth)
        self.mid_nonlinearity = mid_nonlinearity
        self.outer = MLP(hidden_dim, self.output_dim, hidden_dim, outer_depth) \
            if outer_depth else None

    def repr_shape(self, c, h, w):
        return self.output_dim, 1, 1

    def forward(self, x, context=None):
        x = x.flatten(1, -2)

        if context is None:
            context = x

        context = context.flatten(1, -2)

        x = x.unsqueeze(1).expand(-1, context.shape[1], -1, -1)
        context = context.unsqueeze(2).expand(-1, -1, x.shape[1], -1)
        pair = torch.cat([x, context], -1)

        relations = self.inner(pair)

        mid = self.mid_nonlinearity(relations.sum(1).sum(1))

        out = mid if self.outer is None \
            else self.outer(mid)

        return out