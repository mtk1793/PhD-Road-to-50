"""
federated_bess_real_data_config.py — Topic 1: HQI-SAC-Fed Configuration
=========================================================================
All hyperparameters, dataset paths, and grid model settings for the
federated BESS real-data training pipeline.

Paper: "Federated Deep RL for Privacy-Preserving Coordination of
        Provincial-Scale BESS in High-Wind Grids"
Algorithm: HQI-SAC-Fed = HQI-SAC + FedAvg + Differential Privacy (ε=1.0) + 2-layer GCN
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Dataset paths (parquet) ───────────────────────────────────────────────────
DATASETS = {
    "wind_toolkit":     BASE_DIR / "data" / "processed" / "wind_toolkit_ns.parquet",
    "nsrdb_solar":      BASE_DIR / "data" / "processed" / "nsrdb_solar_atlantic.parquet",
    "ieso_aeso":        BASE_DIR / "data" / "processed" / "ieso_aeso_markets.parquet",
    "acn_bess_ev":      BASE_DIR / "data" / "processed" / "acn_bess_ev_fleet.parquet",
    "elia_eirgrid":     BASE_DIR / "data" / "processed" / "elia_eirgrid_wind_5min.parquet",
    "nerc_agc":         BASE_DIR / "data" / "processed" / "nerc_agc_frequency.parquet",
    "eia_bess_econ":    BASE_DIR / "data" / "processed" / "eia_bess_economics.parquet",
}
TOTAL_RECORDS = 16_444_284

# ── Nova Scotia 2030 Grid Model ───────────────────────────────────────────────
GRID = {
    "model": "IEEE_118_bus_NS_scaled",
    "n_buses": 118,
    "n_branches": 186,
    "n_generators": 54,
    "peak_load_mw": 1700.0,
    "annual_load_growth_pct": 1.5,
    "export_limit_mw": 300.0,          # NB + Maine interconnections
    "base_mva": 100.0,
    "simulation_resolution_min": 5,    # 5-min timesteps
}

# ── BESS Sites ────────────────────────────────────────────────────────────────
BESS_SITES = [
    {
        "name": "Guysborough",
        "bus": 47,
        "capacity_mwh": 200.0,
        "power_mw": 100.0,
        "efficiency": 0.92,
        "soc_min": 0.10,
        "soc_max": 0.90,
        "soc_init": 0.50,
    },
    {
        "name": "Halifax",
        "bus": 89,
        "capacity_mwh": 120.0,
        "power_mw": 60.0,
        "efficiency": 0.92,
        "soc_min": 0.10,
        "soc_max": 0.90,
        "soc_init": 0.50,
    },
    {
        "name": "Cape_Breton",
        "bus": 112,
        "capacity_mwh": 200.0,
        "power_mw": 100.0,
        "efficiency": 0.92,
        "soc_min": 0.10,
        "soc_max": 0.90,
        "soc_init": 0.50,
    },
]
N_BESS_AGENTS = len(BESS_SITES)
TOTAL_BESS_MWH = sum(s["capacity_mwh"] for s in BESS_SITES)  # 520 MWh

# ── Wind / Solar Parameters ───────────────────────────────────────────────────
WIND = {
    "total_capacity_mw": 2100.0,
    "sites": {
        "Guysborough": {"bus": 47,  "capacity_mw": 700, "cf_mean": 0.48, "weibull_k": 2.3, "weibull_c": 10.2},
        "Halifax":     {"bus": 89,  "capacity_mw": 700, "cf_mean": 0.48, "weibull_k": 2.3, "weibull_c": 10.2},
        "Cape_Breton": {"bus": 112, "capacity_mw": 700, "cf_mean": 0.48, "weibull_k": 2.3, "weibull_c": 10.2},
    },
}
SOLAR = {
    "total_capacity_mw": 580.0,
    "distribution": "distributed",
    "cf_mean": 0.18,
    "cf_std": 0.042,
}

# ── Electricity Market ────────────────────────────────────────────────────────
MARKET = {
    "price_mean_cad_mwh": 42.0,
    "price_std_cad_mwh": 18.0,
    "price_dr_trigger_cad_mwh": 85.0,
    "carbon_price_cad_tonne": 75.0,
    "carbon_emission_factor_tco2_mwh_marginal": 0.49,  # NS marginal (gas peaker)
}

# ── HQI-SAC Hyperparameters ───────────────────────────────────────────────────
HQISAC = {
    "learning_rate": 3e-4,
    "batch_size": 256,
    "replay_buffer_size": 500_000,
    "discount_gamma": 0.99,
    "temperature_alpha": 0.02,
    "q_guidance_beta": 0.10,
    "target_update_tau": 0.005,
    "hidden_dims": [256, 256],
    "activation": "relu",
    "reward_weights": {
        "arbitrage": 0.40,
        "curtailment": 0.30,
        "frequency": 0.15,
        "carbon": 0.10,
        "penalty": 0.05,
    },
}

# ── GCN (Admittance-Weighted Graph Embedding) ─────────────────────────────────
GCN = {
    "n_layers": 2,
    "input_dim": 3,       # [SOC, P_wind, λ_price] per node
    "hidden_dim": 64,
    "output_dim": 64,
    "activation": "relu",
    "dropout": 0.0,
    "normalization": "admittance_normalized",  # D^{-1/2} Y D^{-1/2}
}

# ── Differential Privacy ──────────────────────────────────────────────────────
DP = {
    "epsilon": 1.0,         # privacy budget — acceptable for Canadian utility regs
    "delta": 1e-5,          # failure probability
    "gradient_clip_norm": 1.0,   # C in the paper
    "noise_sigma": 1.128,   # σ = C * sqrt(2*ln(1.25/δ)) / ε ≈ 1.128
    "mechanism": "gaussian",
}

# ── Federated Averaging ───────────────────────────────────────────────────────
FEDERATED = {
    "n_agents": 3,
    "federation_rounds": 100,
    "local_episodes_per_round": 50,
    "aggregation": "capacity_weighted",   # weight = E_b / sum(E_b')
    "weights": [200 / 520, 120 / 520, 200 / 520],  # Guysborough, Halifax, Cape Breton
    "eval_every_n_rounds": 5,
    "save_checkpoint_every": 10,
}

# ── Training Environment ──────────────────────────────────────────────────────
TRAINING = {
    "n_seeds": 20,                   # random seeds for statistical comparison
    "episode_length_steps": 288,     # 24h × 12 (5-min resolution)
    "max_local_episodes": 5000,
    "warm_up_episodes": 50,
    "eval_episodes": 20,
    "simulation_years": [2020, 2021, 2022],
    "validation_year": 2022,
    "state_dim": 64 + 5,             # GCN output (64) + local features (5)
    "action_dim": 2,                 # [P_charge_discharge, Q_reactive]
}

# ── Output Paths ──────────────────────────────────────────────────────────────
RESULTS = {
    "results_dir": BASE_DIR / "results",
    "checkpoints_dir": BASE_DIR / "results" / "checkpoints",
    "figures_dir": BASE_DIR / "figures",
    "training_results_json": BASE_DIR / "results" / "training_results_real_data.json",
    "convergence_csv": BASE_DIR / "results" / "convergence_curves.csv",
    "ablation_csv": BASE_DIR / "results" / "ablation_study.csv",
    "privacy_tradeoff_csv": BASE_DIR / "results" / "privacy_tradeoff.csv",
    "curtailment_monthly_csv": BASE_DIR / "results" / "curtailment_monthly.csv",
}


def print_summary():
    print("\n" + "=" * 60)
    print("  Topic 1 — HQI-SAC-Fed Configuration Summary")
    print("=" * 60)
    print(f"  Grid:       {GRID['model']}")
    print(f"  BESS:       {N_BESS_AGENTS} sites, {TOTAL_BESS_MWH} MWh total")
    print(f"  Wind:       {WIND['total_capacity_mw']} MW offshore")
    print(f"  Solar:      {SOLAR['total_capacity_mw']} MW distributed PV")
    print(f"  Algorithm:  HQI-SAC + FedAvg + DP (ε={DP['epsilon']})")
    print(f"  Fed rounds: {FEDERATED['federation_rounds']} × {FEDERATED['local_episodes_per_round']} local eps")
    print(f"  Datasets:   {TOTAL_RECORDS:,} total records from 7 sources")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    print_summary()
