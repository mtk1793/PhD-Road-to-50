import os
import torch
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.model import PINNViTFusionModel
from src.data import SyntheticRenewablesDataset
import torchvision.transforms.functional as TF


def normalize_image(img):
    # img: (C,H,W) numpy
    img = img.copy()
    # simple percentile-based normalization per channel
    for c in range(img.shape[0]):
        p1 = np.percentile(img[c], 1)
        p99 = np.percentile(img[c], 99)
        img[c] = np.clip((img[c] - p1) / (p99 - p1 + 1e-9), 0.0, 1.0)
    return img


def refine_and_save_overlays(model, img, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    model.eval()
    img_np = img.numpy()
    img_norm = normalize_image(img_np)
    x = torch.from_numpy(img_np).unsqueeze(0)
    patch_tokens = model.vit.patch_embed(x)
    encoder = model.vit.transformer
    layers = getattr(encoder, 'layers', None) or list(encoder.children())
    num_patches = patch_tokens.shape[1]
    grid_sz = int(np.sqrt(num_patches))
    H, W = img_np.shape[1], img_np.shape[2]
    for i, layer in enumerate(layers):
        if hasattr(layer, 'self_attn'):
            self_attn = layer.self_attn
            attn_out, attn_weights = self_attn(patch_tokens, patch_tokens, patch_tokens, need_weights=True)
            aw = attn_weights.detach().cpu().numpy()
            if aw.ndim == 4:
                aw = aw[0]
            num_heads = aw.shape[0]
            # average heads for a cleaner map
            mean_map = aw.mean(axis=0).mean(axis=0)
            mean_map = mean_map.reshape(grid_sz, grid_sz)
            # upsample to image
            heat = TF.resize(torch.from_numpy(mean_map[np.newaxis,...]), [H,W], interpolation=TF.InterpolationMode.BILINEAR).squeeze(0).numpy()
            heat = (heat - heat.min()) / (heat.max() - heat.min() + 1e-9)
            # plot overlay with normalized background
            fig, ax = plt.subplots(1,1,figsize=(4,4))
            ax.imshow(np.moveaxis(img_norm,0,2))
            ax.imshow(heat, cmap='magma', alpha=0.5)
            ax.axis('off')
            plt.savefig(os.path.join(out_dir, f'attn_refined_layer_{i}.png'), bbox_inches='tight')
            plt.close()
            # save SVG as vector overlay
            fig, ax = plt.subplots(1,1,figsize=(4,4))
            ax.imshow(np.moveaxis(img_norm,0,2))
            ax.imshow(heat, cmap='magma', alpha=0.5)
            ax.axis('off')
            plt.savefig(os.path.join(out_dir, f'attn_refined_layer_{i}.svg'), bbox_inches='tight')
            plt.close()
            print('Saved refined overlays for layer', i)


def main():
    out_dir = 'outputs'
    ds = SyntheticRenewablesDataset(n_samples=10)
    img, scalars, targets = ds[0]
    model = PINNViTFusionModel()
    try:
        model.load_state_dict(torch.load(os.path.join(out_dir, 'model.pt')))
    except Exception:
        pass
    refine_and_save_overlays(model, img, out_dir)

if __name__ == '__main__':
    main()
