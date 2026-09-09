# Research Plan: Physics-Informed Multi-Modal Foundation Models for Real-Time Solar-Wind Hybrid Forecasting

## Goal
Build a hybrid physics-informed foundation model that ingests gridded meteorological fields and scalar station measurements to jointly forecast solar PV generation and wind turbine power at multiple sites in real time. The architecture should combine Vision Transformer (ViT) encoders for spatial fields, PINN-style physics constraints in the loss, and fusion transformers to model spatio-temporal cross-attention across modalities.

## High-level architecture
- Image encoder: ViT-style patch embedding + lightweight transformer encoder to extract spatial features from gridded inputs (e.g., ERA5 cloud/irradiance fields).
- Scalar encoder: small MLP for local measurements (irradiance, wind speed, temperature, surface pressure, etc.).
- Fusion module: multi-level transformer layers that attend across image patches, scalar tokens, and temporal tokens (for short history windows).
- Output heads: per-site regression heads for solar and wind power; optionally uncertainty head (aleatoric) producing sigma for Gaussian NLL.

## Physics integration (hybrid loss)
Use a composite loss:
L = L_data + alpha_solar * L_solar_phys + alpha_wind * L_wind_phys + beta_reg * L_reg

- L_data: MSE or MAE between predicted and observed generation (optionally heteroscedastic NLL).
- L_solar_phys: physics constraints for solar PV:
  - Bound constraints: predicted_power >= 0 and predicted_power <= A * G_cs * eta_max
  - Guidance term: (pred - eta * G_meas)^2 to nudge model toward irradiance-driven power
- L_wind_phys: wind power curve regularization via MSE to a canonical power curve P_curve(v) computed from measured wind speed and turbine specs.

Weighting strategy:
- Start with alpha_solar and alpha_wind small (0.01–0.1) and ramp up over epochs (curriculum) to prevent overpowering data loss.
- Use validation-based tuning or automated weight search (e.g., grid or Bayesian).

## Temporal-spatial attention
- Represent time history as extra tokens (positional encoding for time), and implement multi-scale attention:
  - Local attention within small patches for high-res features
  - Global cross-patch attention for synoptic-scale patterns
- Use dilated temporal attention kernels or stacked temporal transformer layers to capture hourly-to-daily dependencies.

## Cross-domain pretraining
- Pretrain the image encoder and fusion layers on large-scale reanalysis tasks (cloud motion prediction, irradiance forecasting) using self-supervised objectives (masked patch prediction, contrastive losses).
- Fine-tune on target PV/Wind generation tasks with physics losses.

## Data pipeline
- Ingest ERA5 (gridded), NSRDB (irradiance), PV-Live (PV output), Wind Power DB (turbine output).
- Spatial/temporal alignment: reproject and resample ERA5 fields to a common grid and hourly intervals; match station/turbine coordinates to nearest grid cells.
- Feature engineering: derive clear-sky irradiance estimates, sun zenith/azimuth, panel orientation corrections, turbine hub-height wind speeds (log-profile), and upstream smoothing.
- Augmentations: random rotations/flips for data augmentation (careful with geolocation), noise injection on scalar sensors, and limited time warps.

## Evaluation and experiments
- Metrics: RMSE, MAE, MAPE, CRPS (if probabilistic), and physical violation counts (pred<0, pred>phys_max).
- Baselines: persistence, standard MLP, pure ViT without physics loss, and state-of-the-art forecasting models.
- Ablations: remove physics losses, remove image inputs, vary alpha weights, test transfer learning from pretraining.
- Cross-validation: spatial split (holdout sites), temporal split (holdout periods), and transfer experiments across countries.

## Compute and timeline (prototype)
- Prototype (this repo): small ViT, synthetic data, single-GPU or CPU runnable (3–10 epochs).
- Scale-up: multi-GPU training with mixed precision, dataset pre-processing cluster for ERA5/NSRDB.

## Next steps
- Replace synthetic dataset with ERA5 + NSRDB ingestion; implement dataset readers and alignment scripts.
- Add multi-site temporal tokens and build fusion transformer stack.
- Implement pretraining tasks and run ablations.
- Prepare figures and LaTeX paper based on experimental results.

