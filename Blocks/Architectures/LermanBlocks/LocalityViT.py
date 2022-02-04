from torch import nn

from Blocks.Architectures.LermanBlocks.LocalityCNN import Conv2DLocalized
from Blocks.Architectures.MultiHeadAttention import SelfAttentionBlock
from Blocks.Architectures.Residual import Residual


class LocalityViT(nn.Module):
    def __init__(self, input_shape, out_channels=32, depth=3):
        super().__init__()

        self.trunk = Conv2DLocalized(input_shape, out_channels, (16, 16), (16, 16))

        self.ViT = nn.Sequential(
            *[nn.Sequential(SelfAttentionBlock(out_channels),
                            Residual(Conv2DLocalized(self.trunk.shape, out_channels, (2, 2), padding='same')))
              for _ in range(depth)])

    def forward(self, x):
        return self.ViT(self.trunk(x))
