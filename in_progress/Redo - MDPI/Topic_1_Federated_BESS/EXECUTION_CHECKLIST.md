# Execution Checklist — Topic 1: Federated BESS

Complete these steps **in order** to reproduce all results and figures.

---

## Prerequisites

- [ ] Python 3.8+ installed
- [ ] MATLAB R2020b+ installed (with Statistics & Optimization Toolboxes)
- [ ] Install Python dependencies: `pip install -r requirements.txt`
- [ ] Working directory: `Topic_1_Federated_BESS/`

---

## Step 1: Verify Dataset Inventory

```bash
python scripts/download_real_datasets.py --list
```

Expected output:
```
Available datasets (16,444,284 total records):
  1. wind_toolkit_ns        — 5,913,000 records (NREL Wind Toolkit NS Atlantic)
  2. nsrdb_solar_atlantic   — 2,628,900 records (NREL NSRDB Atlantic Solar TMY)
  3. ieso_aeso_markets      — 1,314,000 records (IESO/AESO Canadian Electricity Markets)
  4. acn_bess_ev_fleet      — 1,197,504 records (ACN-Data Fleet BESS/EV Charging)
  5. elia_eirgrid_wind_5min — 2,522,880 records (ELIA/EirGrid Offshore Wind 5-min)
  6. nerc_agc_frequency     — 2,628,000 records (NERC AGC Frequency Regulation)
  7. eia_bess_economics     —   240,000 records (EIA 861/923 + StatCan BESS Economics)
```

---

## Step 2: Download All Datasets

```bash
python scripts/download_real_datasets.py --all
```

- Output: `data/processed/*.parquet` (7 files)
- Manifest: `data/metadata/master_manifest.json`
- Expected time: 5-15 minutes

To download a single dataset:
```bash
python scripts/download_real_datasets.py --dataset wind_toolkit_ns
```

---

## Step 3: Validate Training (Fast Test)

```bash
python scripts/train_hqisac_fed_real_data.py --test
```

- Runs 1 seed, 5 rounds, 5 episodes (2-5 minutes)
- Expected: NPV in range $11-15M (stochastic; full result requires 20 seeds)
- Confirms data loading and federation loop work correctly

---

## Step 4: Run Full Experiment (20 Seeds)

```bash
python scripts/train_hqisac_fed_real_data.py --full
```

- 20 seeds × 100 rounds × 50 episodes = full statistical experiment
- Expected time: 2-4 hours on modern CPU
- Output: `results/training_results_real_data.json` (overwritten with updated results)

### Ablation Variants (Optional)

```bash
python scripts/train_hqisac_fed_real_data.py --ablate no_gcn
python scripts/train_hqisac_fed_real_data.py --ablate no_dp
python scripts/train_hqisac_fed_real_data.py --ablate no_federation
python scripts/train_hqisac_fed_real_data.py --ablate no_q_guidance
```

---

## Step 5: MATLAB Evaluation and Figures

Open MATLAB and run:

```matlab
cd('Topic_1_Federated_BESS/scripts')
evaluate_federated_bess('full')
```

- Loads real parquet datasets (R2022a+) or CSV fallback
- Simulates all 6 dispatch methods
- Runs statistical tests (t-test, Cohen's d)
- Computes NPV / IRR / payback
- Generates 6 publication figures in `figures/`:
  - `matlab_fig1_npv_comparison.pdf`
  - `matlab_fig2_privacy_tradeoff.pdf`
  - `matlab_fig3_ablation_study.pdf`
  - `matlab_fig4_curtailment_heatmap.pdf`
  - `matlab_fig5_convergence.pdf`
  - `matlab_fig6_dispatch_24h.pdf`
- Exports: `results/matlab_results.xlsx` + `results/matlab_tables.tex`

For quick figure generation only:
```matlab
evaluate_federated_bess('figures_only')
```

---

## Step 6: Compile LaTeX Paper

```bash
pdflatex IEEE_Federated_BESS.tex
bibtex IEEE_Federated_BESS
pdflatex IEEE_Federated_BESS.tex
pdflatex IEEE_Federated_BESS.tex
```

---

## Expected Final Results

After Step 4, verify `results/training_results_real_data.json` contains:

```json
"HQI_SAC_Fed": {
    "npv_mean": 13.2,
    "npv_std": 0.41,
    "curtailment_pct": 8.3,
    "co2_kt_yr": 162
}
```

After Step 5, verify `results/matlab_results.xlsx` exists with 4 sheets.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `parquet` files missing | Re-run Step 2 |
| MATLAB `parquetread` error | Upgrade to R2022a+ or use CSV fallback (auto) |
| NPV out of range (20-seed) | Check `config/federated_bess_real_data_config.py` DP parameters |
| LaTeX missing figures | Run Step 5 before Step 6 |
| Training too slow | Use `--fast` flag (10 seeds, 50 rounds) |

---

*All reproduced results must match values in `AI_PAPER_GENERATION_SUMMARY.md` within ±2σ*
