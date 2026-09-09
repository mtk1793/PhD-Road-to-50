import os
import torch
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.model import PINNViTFusionModel
from src.data import SyntheticRenewablesDataset


def extract_and_save_attention(model, img, out_dir, patch_size=8):
    # img: (C,H,W)
    model.eval()
    with torch.no_grad():
        # get patch embeddings
        x = img.unsqueeze(0)  # (1,C,H,W)
        patch_tokens = model.vit.patch_embed(x)  # (1, num_patches, E)
    # iterate transformer layers
    encoder = model.vit.transformer
    # TransformerEncoder may store layers in .layers or .layers (PyTorch uses .layers)
    layers = getattr(encoder, 'layers', None)
    if layers is None:
        layers = list(encoder.children())
    num_patches = patch_tokens.shape[1]
    grid_sz = int(np.sqrt(num_patches))
    for i, layer in enumerate(layers):
        # attempt to access the MultiheadAttention module inside the layer
        if hasattr(layer, 'self_attn'):
            self_attn = layer.self_attn
            # call with need_weights=True
            # ensure inputs are correct shape: batch_first=True used in our transformer
            q = patch_tokens
            # MultiheadAttention in PyTorch returns (attn_output, attn_weights)
            try:
                attn_out, attn_weights = self_attn(q, q, q, need_weights=True)
            except TypeError:
                # fallback for different signatures
                attn_out, attn_weights = self_attn(q, q, q)
            # attn_weights shape: (B, num_heads, L, S) if batch_first=True (newer pytorch) or (num_heads, L, S)
            if attn_weights.ndim == 4:
                # average over heads and batch
                attn_map = attn_weights.mean(axis=1).squeeze(0)  # (L, S) -> avg over src? We'll avg over target axis
                attn_map = attn_map.mean(axis=0)  # (S,)
            elif attn_weights.ndim == 3:
                # (num_heads, L, S)
                attn_map = attn_weights.mean(axis=0).mean(axis=0)
            else:
                # unexpected
                attn_map = attn_weights.mean()
            # attn_map is length S = num_patches
            # ensure numpy array by detaching if torch tensor
            if hasattr(attn_map, 'detach'):
                attn_map = attn_map.detach().cpu().numpy()
            else:
                attn_map = np.array(attn_map)
            # normalize
            attn_map = (attn_map - attn_map.min()) / (attn_map.max() - attn_map.min() + 1e-9)
            attn_img = attn_map.reshape(grid_sz, grid_sz)
            plt.figure(figsize=(4,4))
            plt.imshow(attn_img, cmap='viridis')
            plt.title(f'Layer {i} attention (avg)')
            plt.axis('off')
            save_path = os.path.join(out_dir, f'attn_layer_{i}.png')
            plt.savefig(save_path, bbox_inches='tight')
            plt.close()
            print('Saved', save_path)
        else:
            print('Layer', i, 'has no self_attn')


def main():
    out_dir = 'outputs'
    os.makedirs(out_dir, exist_ok=True)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    ds = SyntheticRenewablesDataset(n_samples=10)
    img, scalars, targets = ds[0]
    model = PINNViTFusionModel().to(device)
    # load trained weights if present
    try:
        model.load_state_dict(torch.load(os.path.join(out_dir, 'model.pt')))
    except Exception:
        pass
    extract_and_save_attention(model, img, out_dir)

if __name__ == '__main__':
    main()
