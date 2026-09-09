import os
import argparse
import yaml
import torch
from torch.utils.data import DataLoader
from src.data import SyntheticRenewablesDataset
from src.model import PINNViTFusionModel, solar_physics_loss, wind_physics_loss
from src.visualize import plot_pred_vs_gt

from src.datasets_real import RealRenewablesDataset

def train_one_epoch(model, dataloader, optim, device, lambda_solar=1.0, lambda_wind=1.0):
    model.train()
    total_loss = 0.0
    for imgs, scalars, targets in dataloader:
        imgs = imgs.to(device)
        scalars = scalars.to(device)
        targets = targets.to(device)
        optim.zero_grad()
        out = model(imgs, scalars)
        data_loss = torch.nn.functional.mse_loss(out, targets)
        # physics losses
        pred_solar = out[:,0]
        pred_wind = out[:,1]
        # be robust to missing scalar columns in real datasets
        if scalars.ndim == 1 or scalars.shape[1] < 1:
            irr = torch.zeros(pred_solar.shape, device=device)
        else:
            irr = scalars[:,0]
        if scalars.ndim == 1 or scalars.shape[1] < 2:
            wind_speed = torch.zeros(pred_wind.shape, device=device)
        else:
            wind_speed = scalars[:,1]
        p_solar = solar_physics_loss(pred_solar, irr)
        p_wind = wind_physics_loss(pred_wind, wind_speed)
        loss = data_loss + lambda_solar * p_solar + lambda_wind * p_wind
        loss.backward()
        optim.step()
        total_loss += loss.item() * imgs.size(0)
    return total_loss / len(dataloader.dataset)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default=None, help='Optional YAML config for real dataset')
    args = parser.parse_args()

    out_dir = 'outputs'
    os.makedirs(out_dir, exist_ok=True)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # Prepare dataset and model based on whether a config is provided
    if args.config is None:
        ds = SyntheticRenewablesDataset(n_samples=500)
        img_ch = 3
        scalar_dim = 2
        out_dim = 2
    else:
        cfg = yaml.safe_load(open(args.config))
        ds = RealRenewablesDataset(cfg)
        img_ch = len(cfg['era5'].get('variables', {})) or 1
        scalar_dim = 0
        if 'nsrdb' in cfg:
            scalar_dim += len(cfg['nsrdb'].get('cols', []))
        if 'wind_db' in cfg:
            scalar_dim += len(cfg['wind_db'].get('cols', []))
        # ensure at least two scalar dims for physics losses (irradiance, wind_speed)
        scalar_dim = max(scalar_dim, 2)
        out_dim = 0
        if 'pv_live' in cfg:
            out_dim += len(cfg['pv_live'].get('cols', []))
        if 'wind_db' in cfg:
            out_dim += len(cfg['wind_db'].get('cols', []))
        out_dim = max(out_dim, 2)

    dl = DataLoader(ds, batch_size=32, shuffle=True)
    model = PINNViTFusionModel(img_channels=img_ch, scalar_dim=scalar_dim, out_dim=out_dim).to(device)
    optim = torch.optim.Adam(model.parameters(), lr=1e-3)
    epochs = 5
    for ep in range(epochs):
        loss = train_one_epoch(model, dl, optim, device)
        print(f"Epoch {ep+1}/{epochs} loss={loss:.4f}")

    # run evaluation on a sample batch and save plot + metrics
    model.eval()
    imgs, scalars, targets = next(iter(dl))
    with torch.no_grad():
        preds = model(imgs.to(device), scalars.to(device)).cpu().numpy()
    gts = targets.numpy()
    plot_pred_vs_gt(preds, gts, os.path.join(out_dir, 'pred_vs_gt.png'))
    # compute RMSE and MAE per output dim
    import numpy as _np
    rmse = _np.sqrt(_np.mean((preds - gts)**2, axis=0))
    mae = _np.mean(_np.abs(preds - gts), axis=0)
    with open(os.path.join(out_dir, 'metrics.txt'), 'w') as fh:
        fh.write('rmse,' + ','.join([f"{v:.4f}" for v in rmse]) + '\n')
        fh.write('mae,' + ','.join([f"{v:.4f}" for v in mae]) + '\n')
    torch.save(model.state_dict(), os.path.join(out_dir, 'model.pt'))
    print('Saved outputs to', out_dir)

if __name__ == '__main__':
    main()
