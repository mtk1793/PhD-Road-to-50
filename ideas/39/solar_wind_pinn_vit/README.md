# Physics-Informed Multi-Modal Foundation Models for Real-Time Solar-Wind Hybrid Forecasting

This small prototype demonstrates a minimal PyTorch implementation of a hybrid PINN + ViT-style backbone with a fusion transformer for multi-modal (spatial weather images + scalar features) forecasting of solar and wind power using synthetic data.

What is included

- `src/data.py` — synthetic dataset and dataloader
- `src/model.py` — small ViT-like image encoder, scalar MLP, fusion head, and physics loss functions (solar irradiance constraint and wind-turbine power curve)
- `src/train.py` — training loop that runs on synthetic data and saves a visualization
- `src/visualize.py` — simple plotting helper
- `paper/main.tex` — LaTeX paper skeleton for the research write-up
- `requirements.txt` — minimal Python dependencies

Quick run (Windows PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
python src\train.py
```

Output

- Trained model weights (saved to `outputs/`) and a visualization `outputs/pred_vs_gt.png`.

Notes

This is a minimal, self-contained prototype for experimentation and visualization. Replace the synthetic data in `src/data.py` with real dataset ingestion (ERA5, NSRDB, PV-Live, Wind DB) when ready.

Real-data ingestion

This project includes a `src/datasets_real.py` module and an example config `data_config_example.yaml` that show how to load ERA5 NetCDF files and CSV time-series for NSRDB/PV-Live/Wind DB. The real-data loader uses `xarray` and `pandas` and expects you to download the datasets and place files locally. After installing the additional dependencies in `requirements.txt`, instantiate `RealRenewablesDataset` with your config and use `src/train.py` (or adapt it) to train on real data.

Example usage (PowerShell):

```powershell
$env:PYTHONPATH = "c:\Users\Aly\OneDrive - Dalhousie University\Google Drive\PhD\Papers\Road to 15\39\solar_wind_pinn_vit"
python -c "from src.datasets_real import RealRenewablesDataset; import yaml; cfg=yaml.safe_load(open('data_config_example.yaml')); ds=RealRenewablesDataset(cfg); print(len(ds));"
```

If you prefer direct download helpers for ERA5 (CDS API) or NSRDB, I can add scripts, but note those require API keys and additional system packages (e.g., ecCodes for GRIB/CFGRIB). The current loader works with NetCDFs and CSVs.
