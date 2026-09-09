# quick smoke test for import and forward pass
import torch
from src.model import PINNViTFusionModel

if __name__ == '__main__':
    model = PINNViTFusionModel()
    x = torch.randn(2,3,64,64)
    s = torch.randn(2,2)
    out = model(x,s)
    print('output shape', out.shape)
