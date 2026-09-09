import os
import torch
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.model import PINNViTFusionModel
from src.data import SyntheticRenewablesDataset
import torchvision.transforms.functional as TF


def upsample_patch_to_image(patch_map, img_shape, patch_size=8):
    # patch_map: (H_p, W_p)
    H, W = img_shape
    return TF.resize(torch.from_numpy(patch_map[np.newaxis,...]), [H, W], interpolation=TF.InterpolationMode.BILINEAR).squeeze(0).numpy()


def overlay_heatmap_on_image(img, heatmap, alpha=0.5, cmap='jet'):
    plt.figure(figsize=(4,4))
    plt.imshow(np.moveaxis(img,0,2))
    plt.imshow(heatmap, cmap=cmap, alpha=alpha)
    plt.axis('off')


def extract_heads_and_overlay(model, img, out_dir, patch_size=8):
    model.eval()
    x = img.unsqueeze(0)
    patch_tokens = model.vit.patch_embed(x)  # (1, P, E)
    encoder = model.vit.transformer
    layers = getattr(encoder, 'layers', None)
    if layers is None:
        layers = list(encoder.children())
    num_patches = patch_tokens.shape[1]
    grid_sz = int(np.sqrt(num_patches))
    # get original image shape
    _, H, W = img.shape
    for i, layer in enumerate(layers):
        if hasattr(layer, 'self_attn'):
            self_attn = layer.self_attn
            # run attention with gradients off but capture weights
            q = patch_tokens
            # many MultiheadAttention implementations accept need_weights flag
            attn_out, attn_weights = self_attn(q, q, q, need_weights=True)
            # attn_weights: (B, num_heads, L, S) or (num_heads, L, S)
            aw = attn_weights.detach().cpu().numpy()
            if aw.ndim == 4:
                # B, H, L, S
                aw = aw[0]
            # aw: (num_heads, L, S)
            num_heads = aw.shape[0]
            for h in range(num_heads):
                head_map = aw[h].mean(axis=0)  # average over target tokens -> (S,)
                head_map = head_map.reshape(grid_sz, grid_sz)
                # upsample
                up = upsample_patch_to_image(head_map, (H, W), patch_size)
                # overlay
                overlay_heatmap_on_image(img.numpy(), up, alpha=0.5)
                save_path = os.path.join(out_dir, f'attn_layer_{i}_head_{h}.png')
                plt.savefig(save_path, bbox_inches='tight')
                plt.close()
                print('Saved', save_path)
        else:
            print('Layer', i, 'has no self_attn')


def main():
    out_dir = 'outputs'
    os.makedirs(out_dir, exist_ok=True)
    ds = SyntheticRenewablesDataset(n_samples=10)
    img, scalars, targets = ds[0]
    model = PINNViTFusionModel()
    try:
        model.load_state_dict(torch.load(os.path.join(out_dir, 'model.pt')))
    except Exception:
        pass
    extract_heads_and_overlay(model, img, out_dir)

if __name__ == '__main__':
    main()
