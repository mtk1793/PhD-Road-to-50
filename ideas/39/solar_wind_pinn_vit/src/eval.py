import os
import csv
import torch
import numpy as np
from torch.utils.data import DataLoader
from src.data import SyntheticRenewablesDataset
from src.model import PINNViTFusionModel


def evaluate_model(model, dataloader, device):
    model.eval()
    preds = []
    gts = []
    with torch.no_grad():
        for imgs, scalars, targets in dataloader:
            imgs = imgs.to(device)
            scalars = scalars.to(device)
            out = model(imgs, scalars).cpu().numpy()
            preds.append(out)
            gts.append(targets.numpy())
    preds = np.vstack(preds)
    gts = np.vstack(gts)
    return preds, gts


def main():
    out_dir = 'outputs'
    os.makedirs(out_dir, exist_ok=True)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    ds = SyntheticRenewablesDataset(n_samples=200)
    dl = DataLoader(ds, batch_size=32, shuffle=False)
    model = PINNViTFusionModel()
    model.load_state_dict(torch.load(os.path.join(out_dir, 'model.pt')))
    preds, gts = evaluate_model(model, dl, device)
    # save predictions to CSV
    rows = []
    for i in range(preds.shape[0]):
        row = list(gts[i]) + list(preds[i])
        rows.append(row)
    with open(os.path.join(out_dir, 'predictions.csv'), 'w', newline='') as fh:
        writer = csv.writer(fh)
        writer.writerow(['gt_solar','gt_wind','pred_solar','pred_wind'])
        writer.writerows(rows)
    print('Saved predictions to', os.path.join(out_dir, 'predictions.csv'))

if __name__ == '__main__':
    main()
