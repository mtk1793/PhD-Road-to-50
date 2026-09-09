#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Synthetic Smart Grid Dataset Generator for EWC-IXER Continual Learning Experiments.

This module generates a synthetic smart grid dataset comprising multiple sequential
tasks, each representing a distinct seasonal operating regime. The dataset is
designed to evaluate continual learning methods (e.g., Elastic Weight Consolidation
with Import-Weighted Experience Replay, EWC-IXER) under distribution shift.

Each task is characterized by a unique multivariate Gaussian distribution over five
bus-level features (Load_kW, Solar_Power, Wind_Power, Temperature_C, Humidity),
correlated through a physically-motivated correlation structure enforced via
Cholesky decomposition. The per-unit bus voltage (Voltage_pu) is synthesized as
a linear combination of these features plus Gaussian noise.

Author: EWC-IXER Project
"""

from __future__ import annotations

import warnings
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy.stats import multivariate_normal

# ============================================================================
# Global Configuration
# ============================================================================

# Feature names used throughout the dataset
FEATURE_NAMES: List[str] = [
    "Load_kW",
    "Solar_Power",
    "Wind_Power",
    "Temperature_C",
    "Humidity",
]

# Target column name
TARGET_NAME: str = "Voltage_pu"

# Number of samples per task (default)
SAMPLES_PER_TASK: int = 500

# Train/test split ratio (fraction allocated to training)
TRAIN_RATIO: float = 0.8

# Random seed for reproducibility
RANDOM_SEED: int = 42

# Standard deviation multiplier for observational noise on each feature.
# Noise sigma = OBS_NOISE_FACTOR * max(feature_range_across_tasks)
OBS_NOISE_FACTOR: float = 0.05

# ============================================================================
# Seasonal Task Definitions (5 Tasks)
# ============================================================================

# Each task is defined by: (name, means, stds) where means and stds are
# 5-element vectors corresponding to [Load_kW, Solar_Power, Wind_Power,
# Temperature_C, Humidity].
#
# Distributions were chosen to reflect realistic seasonal variation in a
# mid-latitude power system with significant renewable penetration.

TASK_DEFINITIONS: List[Tuple[str, np.ndarray, np.ndarray]] = [
    # Task 0 – Spring: moderate load, rising solar, moderate wind
    (
        "Spring",
        np.array([500.0, 200.0, 150.0, 15.0, 60.0]),  # means
        np.array([50.0, 40.0, 30.0, 5.0, 10.0]),      # stds
    ),
    # Task 1 – Summer: elevated load (cooling), peak solar, low wind
    (
        "Summer",
        np.array([550.0, 350.0, 100.0, 28.0, 45.0]),  # means
        np.array([55.0, 50.0, 25.0, 4.0, 8.0]),       # stds
    ),
    # Task 2 – Autumn: high load (heating onset), declining solar, strong wind
    (
        "Autumn",
        np.array([600.0, 150.0, 200.0, 10.0, 65.0]),  # means
        np.array([60.0, 35.0, 35.0, 6.0, 12.0]),      # stds
    ),
    # Task 3 – Winter: peak load (heating), minimal solar, strongest wind
    (
        "Winter",
        np.array([700.0, 80.0, 250.0, 2.0, 70.0]),    # means
        np.array([70.0, 20.0, 40.0, 4.0, 10.0]),      # stds
    ),
    # Task 4 – Shoulder: transitional season with blended characteristics
    (
        "Shoulder",
        np.array([650.0, 250.0, 180.0, 12.0, 55.0]),  # means
        np.array([65.0, 45.0, 30.0, 5.0, 10.0]),      # stds
    ),
]

# ============================================================================
# Correlation Matrix
# ============================================================================

def _build_correlation_matrix() -> np.ndarray:
    """
    Construct the 5x5 inter-feature correlation matrix.

    The off-diagonal entries encode physically-motivated relationships:
      - Load ↔ Solar (−0.3): higher PV output coincides with reduced net load.
      - Load ↔ Wind  (−0.1): weak negative coupling via wind-driven demand
        reduction (e.g., evaporative cooling).
      - Load ↔ Temp  (+0.4): positive due to temperature-dependent cooling load.
      - Load ↔ Humidity (+0.2): humidity amplifies perceived temperature,
        increasing air-conditioning demand.
      - Solar ↔ Temp (+0.5): strong positive — clear-sky days are both
        hot and irradiant.
      - Solar ↔ Wind (−0.4): anti-correlated — stable high-pressure systems
        favor solar but suppress wind.
      - Solar ↔ Humidity (−0.3): clear skies imply lower humidity.
      - Wind ↔ Temp  (−0.2): windy conditions often accompany frontal
        passages with cooler air.
      - Wind ↔ Humidity (−0.1): weak negative coupling.
      - Temp ↔ Humidity (−0.6): strong negative — hot dry vs. cool humid.

    Returns
    -------
    np.ndarray
        A 5x5 symmetric positive-definite correlation matrix.
    """
    # Feature order: Load, Solar, Wind, Temperature, Humidity
    corr = np.array(
        [
            #          Load   Solar  Wind   Temp   Hum
            [ 1.00, -0.30, -0.10,  0.40,  0.20],  # Load
            [-0.30,  1.00, -0.40,  0.50, -0.30],  # Solar
            [-0.10, -0.40,  1.00, -0.20, -0.10],  # Wind
            [ 0.40,  0.50, -0.20,  1.00, -0.60],  # Temp
            [ 0.20, -0.30, -0.10, -0.60,  1.00],  # Humidity
        ]
    )
    return corr


def _ensure_positive_definite(corr: np.ndarray) -> np.ndarray:
    """
    Ensure the correlation matrix is positive-definite for Cholesky
    decomposition.  If the supplied matrix has eigenvalues very close to
    zero or slightly negative (possible due to floating-point rounding of
    hand-specified correlations), we apply the nearest positive-definite
    matrix projection via eigenvalue clipping.

    Parameters
    ----------
    corr : np.ndarray
        Symmetric correlation matrix (5×5).

    Returns
    -------
    np.ndarray
        A valid positive-definite correlation matrix.
    """
    eigvals, eigvecs = np.linalg.eigh(corr)
    min_eigval = eigvals.min()
    if min_eigval < 1e-8:
        warnings.warn(
            f"Correlation matrix has minimum eigenvalue {min_eigval:.6f}. "
            f"Clipping to 1e-8 to ensure positive definiteness."
        )
        eigvals = np.maximum(eigvals, 1e-8)
        corr = eigvecs @ np.diag(eigvals) @ eigvecs.T
        # Re-normalize to unit diagonal
        d = np.sqrt(np.diag(corr))
        corr = corr / np.outer(d, d)
    return corr


# ============================================================================
# Target (Voltage) Generation
# ============================================================================

# Linear coefficients mapping features → Voltage_pu.
#   Voltage = 1.0
#           - 0.0001 × Load_kW
#           + 0.00005 × Solar_Power
#           - 0.00002 × Wind_Power
#           - 0.0003  × Temperature_C
#           + 0.00001 × Humidity
#           + N(0, 0.02)
#
# Interpretation:
#   - Higher load depresses voltage (IR-drop / IZ-drop along feeders).
#   - Distributed solar provides local voltage support.
#   - Wind has a minor depressive effect (reactive power consumption).
#   - Higher temperature increases conductor resistance, lowering voltage.
#   - Humidity has a negligible positive effect.

VOLTAGE_COEFFICIENTS: np.ndarray = np.array(
    [-0.0001,   # Load_kW
      0.00005,  # Solar_Power
     -0.00002,  # Wind_Power
     -0.0003,   # Temperature_C
      0.00001]  # Humidity
)

VOLTAGE_INTERCEPT: float = 1.0
VOLTAGE_NOISE_STD: float = 0.02  # Intrinsic target noise σ_y


def compute_voltage(features: np.ndarray) -> np.ndarray:
    """
    Compute per-unit bus voltage from feature matrix.

    Parameters
    ----------
    features : np.ndarray, shape (n_samples, 5)
        Matrix of [Load_kW, Solar_Power, Wind_Power, Temperature_C, Humidity].

    Returns
    -------
    np.ndarray, shape (n_samples,)
        Synthesized Voltage_pu values.
    """
    linear_part = features @ VOLTAGE_COEFFICIENTS + VOLTAGE_INTERCEPT
    noise = np.random.normal(loc=0.0, scale=VOLTAGE_NOISE_STD, size=features.shape[0])
    return linear_part + noise


# ============================================================================
# Observational Noise
# ============================================================================

def compute_observational_noise(
    task_means_all: np.ndarray,  # (n_tasks, 5)
    task_stds_all: np.ndarray,   # (n_tasks, 5)
    n_samples: int,
) -> np.ndarray:
    """
    Compute the standard deviation of additive Gaussian observational noise
    for each feature across all tasks.

    For feature j:
        σ_obs_j = 0.05 × max_j(μ_j + 2σ_j)  across all tasks

    This represents sensor measurement noise and unmodeled stochastic
    fluctuations in real-world smart-grid SCADA systems.

    Parameters
    ----------
    task_means_all : np.ndarray, shape (n_tasks, 5)
        Feature means for every task.
    task_stds_all : np.ndarray, shape (n_tasks, 5)
        Feature standard deviations for every task.
    n_samples : int
        Number of samples per task.

    Returns
    -------
    np.ndarray, shape (n_samples, 5)
        Noise matrix to be added to the features.
    """
    # Approximate upper bound of each feature's range across tasks
    # as mean + 2*std for each task, then take the max across tasks.
    upper_bounds = task_means_all + 2.0 * task_stds_all  # (n_tasks, 5)
    feature_max = upper_bounds.max(axis=0)  # (5,)
    noise_std = OBS_NOISE_FACTOR * feature_max  # (5,)
    noise = np.random.normal(loc=0.0, scale=noise_std, size=(n_samples, 5))
    return noise, noise_std


# ============================================================================
# Core Dataset Generation
# ============================================================================

def generate_task_samples(
    means: np.ndarray,
    stds: np.ndarray,
    cholesky_L: np.ndarray,
    n_samples: int,
    obs_noise: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate correlated feature samples for a single task and compute targets.

    The procedure:
      1. Draw n_samples independent standard-normal vectors z ~ N(0, I).
      2. Transform to correlated standard normals: x = L · z, where L is
         the lower-triangular Cholesky factor of the correlation matrix.
      3. Scale to task-specific marginals: x_j ← μ_j + σ_j · x_j.
      4. Optionally add observational noise.
      5. Compute Voltage_pu via the linear model.

    Parameters
    ----------
    means : np.ndarray, shape (5,)
        Task-specific feature means.
    stds : np.ndarray, shape (5,)
        Task-specific feature standard deviations.
    cholesky_L : np.ndarray, shape (5, 5)
        Lower-triangular Cholesky factor of the correlation matrix.
    n_samples : int
        Number of samples for this task.
    obs_noise : np.ndarray or None, shape (n_samples, 5)
        Pre-generated observational noise.  If None, no noise is added.

    Returns
    -------
    features : np.ndarray, shape (n_samples, 5)
        Generated feature matrix.
    targets : np.ndarray, shape (n_samples,)
        Corresponding Voltage_pu values.
    """
    # Step 1: Independent standard-normal samples
    z = np.random.standard_normal(size=(n_samples, len(means)))

    # Step 2: Impose correlation via Cholesky factor
    x_correlated = z @ cholesky_L.T  # (n_samples, 5)

    # Step 3: Scale to task marginals
    features = means[np.newaxis, :] + stds[np.newaxis, :] * x_correlated

    # Step 4: Add observational noise if provided
    if obs_noise is not None:
        features = features + obs_noise

    # Step 5: Compute target
    targets = compute_voltage(features)

    return features, targets


def generate_dataset(
    n_samples_per_task: int = SAMPLES_PER_TASK,
    seed: int = RANDOM_SEED,
) -> Dict[str, Dict[str, object]]:
    """
    Generate the full synthetic smart grid dataset with 5 seasonal tasks.

    For each task, the function:
      1. Constructs the correlation matrix and its Cholesky decomposition.
      2. Generates correlated feature samples with observational noise.
      3. Computes the Voltage_pu target.
      4. Splits into 80% training and 20% test sets.

    Parameters
    ----------
    n_samples_per_task : int
        Number of samples to generate per task (default 500).
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    Dict[str, Dict[str, object]]
        A dictionary keyed by task name, each containing:
          - "task_id"       : int
          - "name"          : str
          - "n_samples"     : int
          - "X_train"       : np.ndarray, shape (n_train, 5)
          - "X_test"        : np.ndarray, shape (n_test, 5)
          - "y_train"       : np.ndarray, shape (n_train,)
          - "y_test"        : np.ndarray, shape (n_test,)
          - "df"            : pd.DataFrame (full task data)
          - "means"         : np.ndarray (5,)
          - "stds"          : np.ndarray (5,)
          - "obs_noise_std" : np.ndarray (5,)
    """
    np.random.seed(seed)

    # Build and validate correlation matrix
    corr = _build_correlation_matrix()
    corr = _ensure_positive_definite(corr)
    cholesky_L = np.linalg.cholesky(corr)  # Lower-triangular (5, 5)

    # Collect task means/stds across all tasks for observational noise computation
    task_means_all = np.array([td[1] for td in TASK_DEFINITIONS])  # (5, 5)
    task_stds_all = np.array([td[2] for td in TASK_DEFINITIONS])   # (5, 5)

    # Compute observational noise parameters (shared across tasks)
    obs_noise_matrix, obs_noise_std = compute_observational_noise(
        task_means_all, task_stds_all, n_samples_per_task
    )

    dataset: Dict[str, Dict[str, object]] = {}

    for task_id, (name, means, stds) in enumerate(TASK_DEFINITIONS):
        # Generate fresh observational noise for each task (different realization)
        task_obs_noise = np.random.normal(
            loc=0.0, scale=obs_noise_std, size=(n_samples_per_task, 5)
        )

        # Generate correlated features and targets
        features, targets = generate_task_samples(
            means=means,
            stds=stds,
            cholesky_L=cholesky_L,
            n_samples=n_samples_per_task,
            obs_noise=task_obs_noise,
        )

        # Build DataFrame
        df = pd.DataFrame(features, columns=FEATURE_NAMES)
        df[TARGET_NAME] = targets
        df["Task_ID"] = task_id
        df["Season"] = name

        # 80/20 train/test split (stratified is unnecessary for regression)
        n_train = int(n_samples_per_task * TRAIN_RATIO)
        indices = np.random.permutation(n_samples_per_task)
        train_idx = indices[:n_train]
        test_idx = indices[n_train:]

        dataset[name] = {
            "task_id": task_id,
            "name": name,
            "n_samples": n_samples_per_task,
            "X_train": features[train_idx],
            "X_test": features[test_idx],
            "y_train": targets[train_idx],
            "y_test": targets[test_idx],
            "df": df,
            "means": means,
            "stds": stds,
            "obs_noise_std": obs_noise_std,
        }

    return dataset


# ============================================================================
# Scaling Experiments: Variable Number of Tasks
# ============================================================================

def generate_scaled_dataset(
    n_tasks: int = 5,
    n_samples_per_task: int = SAMPLES_PER_TASK,
    seed: int = RANDOM_SEED,
) -> Dict[str, Dict[str, object]]:
    """
    Generate a synthetic dataset with a variable number of tasks for
    scaling experiments (e.g., 5, 10, 20, 30, 50 tasks).

    When n_tasks > 5, the base 5 seasonal regimes are cyclically repeated
    with incremental distributional shifts to simulate ongoing temporal
    evolution.  Specifically, for cycle k (k = 0, 1, 2, ...):

      μ_j^{(k)} = μ_j^{(base)} + k × δμ_j
      σ_j^{(k)} = σ_j^{(base)} × (1 + 0.02 × k)

    where δμ is a small drift vector:
      δμ = [10, -5, 3, 0.5, -1]  (Load↑, Solar↓, Wind↑, Temp↑, Humidity↓)

    This models realistic long-term trends such as load growth, PV
    degradation, and climate change effects.

    Parameters
    ----------
    n_tasks : int
        Total number of tasks to generate.  Supported: 5, 10, 20, 30, 50.
    n_samples_per_task : int
        Samples per individual task.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    Dict[str, Dict[str, object]]
        Same structure as ``generate_dataset``, but with n_tasks entries.
    """
    if n_tasks < 1:
        raise ValueError("n_tasks must be at least 1.")

    np.random.seed(seed)

    # Build correlation matrix
    corr = _build_correlation_matrix()
    corr = _ensure_positive_definite(corr)
    cholesky_L = np.linalg.cholesky(corr)

    # Long-term drift vector per cycle
    drift_mu = np.array([10.0, -5.0, 3.0, 0.5, -1.0])

    # Collect all task parameters first (for observational noise computation)
    all_means = []
    all_stds = []
    task_params = []  # (task_name, means, stds)

    for t in range(n_tasks):
        base_idx = t % len(TASK_DEFINITIONS)
        cycle = t // len(TASK_DEFINITIONS)
        base_name, base_means, base_stds = TASK_DEFINITIONS[base_idx]

        # Apply cyclic drift
        shifted_means = base_means + cycle * drift_mu
        shifted_stds = base_stds * (1.0 + 0.02 * cycle)

        task_name = f"{base_name}_C{cycle}" if cycle > 0 else base_name
        all_means.append(shifted_means)
        all_stds.append(shifted_stds)
        task_params.append((task_name, shifted_means, shifted_stds))

    all_means_arr = np.array(all_means)  # (n_tasks, 5)
    all_stds_arr = np.array(all_stds)    # (n_tasks, 5)

    # Observational noise
    _, obs_noise_std = compute_observational_noise(
        all_means_arr, all_stds_arr, n_samples_per_task
    )

    dataset: Dict[str, Dict[str, object]] = {}

    for task_id, (name, means, stds) in enumerate(task_params):
        task_obs_noise = np.random.normal(
            loc=0.0, scale=obs_noise_std, size=(n_samples_per_task, 5)
        )

        features, targets = generate_task_samples(
            means=means,
            stds=stds,
            cholesky_L=cholesky_L,
            n_samples=n_samples_per_task,
            obs_noise=task_obs_noise,
        )

        df = pd.DataFrame(features, columns=FEATURE_NAMES)
        df[TARGET_NAME] = targets
        df["Task_ID"] = task_id
        df["Season"] = name

        n_train = int(n_samples_per_task * TRAIN_RATIO)
        indices = np.random.permutation(n_samples_per_task)
        train_idx = indices[:n_train]
        test_idx = indices[n_train:]

        dataset[name] = {
            "task_id": task_id,
            "name": name,
            "n_samples": n_samples_per_task,
            "X_train": features[train_idx],
            "X_test": features[test_idx],
            "y_train": targets[train_idx],
            "y_test": targets[test_idx],
            "df": df,
            "means": means,
            "stds": stds,
            "obs_noise_std": obs_noise_std,
        }

    return dataset


# ============================================================================
# Utility: Print Dataset Statistics
# ============================================================================

def print_dataset_statistics(
    dataset: Dict[str, Dict[str, object]],
    title: str = "Synthetic Smart Grid Dataset",
) -> None:
    """
    Print a formatted summary of the generated dataset, including per-task
    sample counts, feature means, and feature standard deviations.

    Parameters
    ----------
    dataset : Dict[str, Dict[str, object]]
        Output of ``generate_dataset`` or ``generate_scaled_dataset``.
    title : str
        Header title for the printed summary.
    """
    separator = "=" * 80
    print(f"\n{separator}")
    print(f"  {title}")
    print(f"  Total tasks: {len(dataset)}")
    total_samples = sum(v["n_samples"] for v in dataset.values())
    print(f"  Total samples: {total_samples}")
    print(f"  Features: {FEATURE_NAMES}")
    print(f"  Target: {TARGET_NAME}")
    print(f"  Train/Test split: {int(TRAIN_RATIO*100)}%/{int((1-TRAIN_RATIO)*100)}%")
    print(separator)

    for task_name, task_data in dataset.items():
        tid = task_data["task_id"]
        n = task_data["n_samples"]
        means = task_data["means"]
        stds = task_data["stds"]
        obs_std = task_data["obs_noise_std"]

        print(f"\n  Task {tid}: {task_name}  (n = {n})")
        print(f"  {'Feature':<16} {'Mean':>10} {'Std':>10} {'Obs Noise σ':>14}")
        print(f"  {'-'*52}")
        for j, feat in enumerate(FEATURE_NAMES):
            print(
                f"  {feat:<16} {means[j]:>10.2f} {stds[j]:>10.2f} {obs_std[j]:>14.4f}"
            )

    # Aggregate DataFrame statistics
    all_dfs = [v["df"] for v in dataset.values()]
    full_df = pd.concat(all_dfs, ignore_index=True)
    print(f"\n{separator}")
    print("  Aggregate Statistics (all tasks combined)")
    print(f"  {'Feature':<16} {'Global Mean':>12} {'Global Std':>12} {'Min':>10} {'Max':>10}")
    print(f"  {'-'*62}")
    for col in FEATURE_NAMES + [TARGET_NAME]:
        print(
            f"  {col:<16} {full_df[col].mean():>12.4f} "
            f"{full_df[col].std():>12.4f} "
            f"{full_df[col].min():>10.4f} {full_df[col].max():>10.4f}"
        )
    print(f"{separator}\n")


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import os

    # ------------------------------------------------------------------
    # 1. Generate the standard 5-task seasonal dataset
    # ------------------------------------------------------------------
    print("Generating synthetic smart grid dataset (5 seasonal tasks)...")
    dataset = generate_dataset(n_samples_per_task=SAMPLES_PER_TASK, seed=RANDOM_SEED)

    # ------------------------------------------------------------------
    # 2. Print detailed statistics
    # ------------------------------------------------------------------
    print_dataset_statistics(dataset, title="EWC-IXER Synthetic Smart Grid Dataset")

    # ------------------------------------------------------------------
    # 3. Save to CSV
    # ------------------------------------------------------------------
    output_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(output_dir, "synthetic_smart_grid_data.csv")

    all_dfs = [task["df"] for task in dataset.values()]
    full_df = pd.concat(all_dfs, ignore_index=True)

    # Reorder columns for readability
    col_order = ["Task_ID", "Season"] + FEATURE_NAMES + [TARGET_NAME]
    full_df = full_df[col_order]
    full_df.to_csv(csv_path, index=False)
    print(f"  Dataset saved to: {csv_path}")
    print(f"  Shape: {full_df.shape[0]} rows × {full_df.shape[1]} columns\n")

    # ------------------------------------------------------------------
    # 4. Verify correlation structure (sample correlation)
    # ------------------------------------------------------------------
    print("  Sample correlation matrix (all tasks pooled):")
    sample_corr = full_df[FEATURE_NAMES].corr().to_numpy()
    print(f"  {'':>16}", end="")
    for f in FEATURE_NAMES:
        short = f[:8]
        print(f"{short:>10}", end="")
    print()
    for i, f in enumerate(FEATURE_NAMES):
        short = f[:8]
        print(f"  {short:>16}", end="")
        for j in range(len(FEATURE_NAMES)):
            print(f"{sample_corr[i, j]:>10.4f}", end="")
        print()
    print()

    # ------------------------------------------------------------------
    # 5. Verify Cholesky decomposition and target distribution
    # ------------------------------------------------------------------
    print("  Target (Voltage_pu) distribution per task:")
    for task_name, task_data in dataset.items():
        y_all = np.concatenate([task_data["y_train"], task_data["y_test"]])
        print(
            f"    Task {task_data['task_id']} ({task_name:>8}): "
            f"mean = {y_all.mean():.6f}, std = {y_all.std():.6f}, "
            f"min = {y_all.min():.6f}, max = {y_all.max():.6f}"
        )
    print()

    # ------------------------------------------------------------------
    # 6. Quick scaling experiment demonstration
    # ------------------------------------------------------------------
    print("  Scaling experiment: generating 10-task variant...")
    scaled_dataset = generate_scaled_dataset(
        n_tasks=10, n_samples_per_task=SAMPLES_PER_TASK, seed=RANDOM_SEED
    )
    print_dataset_statistics(
        scaled_dataset, title="EWC-IXER Scaled Dataset (10 Tasks)"
    )

    print("Done.")
