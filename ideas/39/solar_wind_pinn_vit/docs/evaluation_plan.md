# Evaluation Plan

## Metrics
- Point forecasts: RMSE, MAE, MAPE
- Probabilistic forecasts (future): CRPS, PIT
- Physical violations: count(pred < 0), count(pred > physical_max)

## Baselines
- Persistence (last observed)
- Simple MLP on scalars
- ViT without physics loss

## Ablations
- Remove solar physics loss
- Remove wind physics loss
- Remove image inputs
- Vary physics loss weights

## Cross-validation
- Spatial holdout: hold out subset of sites
- Temporal holdout: hold out contiguous periods (seasonal test)

## Real-time setup
- Inference latency target: <500ms per site on 1 GPU
- Data ingestion: stream ERA5/NSRDB updates and run model every hour

## Acceptance criteria
- RMSE reduction versus baseline >= 10%
- Physical violation rate < 0.5% of predictions

