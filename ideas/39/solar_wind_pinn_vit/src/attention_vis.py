import os
import torch
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.model import PINNViTFusionModel
from src.data import SyntheticRenewablesDataset


def simple_gradient_saliency(model, img, scalar, device):
    model.eval()
    img = img.to(device).unsqueeze(0).requires_grad_(True)
    scalar = scalar.to(device).unsqueeze(0)
    out = model(img, scalar)
    # score: sum of solar and wind outputs
    score = out.sum()
    score.backward()
    sal = img.grad.abs().mean(dim=1).squeeze(0).cpu().numpy()  # (H, W)
    sal = (sal - sal.min()) / (sal.max() - sal.min() + 1e-9)
    return sal


def main():
    out_dir = 'outputs'
    os.makedirs(out_dir, exist_ok=True)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    ds = SyntheticRenewablesDataset(n_samples=20)
    img, scalars, targets = ds[0]
    model = PINNViTFusionModel().to(device)
    # load trained weights if present
    try:
        model.load_state_dict(torch.load(os.path.join(out_dir, 'model.pt')))
    except Exception:
        pass
    sal = simple_gradient_saliency(model, img, scalars, device)
    plt.imshow(sal, cmap='inferno')
    plt.colorbar()
    plt.title('Saliency (avg channels)')
    plt.axis('off')
    plt.savefig(os.path.join(out_dir, 'attention_saliency.png'))
    print('Saved saliency to', os.path.join(out_dir, 'attention_saliency.png'))

if __name__ == '__main__':
    main()
