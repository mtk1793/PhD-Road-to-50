#!/usr/bin/env python3
"""
=============================================================================
 Uncertainty Decomposition Module for EWC-IXER
=============================================================================

This module implements Monte Carlo (MC) Dropout-based uncertainty decomposition
for regression networks, as described in the EWC-IXER paper.

Core idea:
    sigma^2_total(x) = sigma^2_epistemic(x) + sigma^2_aleatoric(x)

where:
    - Epistemic uncertainty:  variance of M MC predictions
        (uncertainty in model parameters → reducible with more data)
    - Aleatoric uncertainty:  mean of M individual squared residuals minus
        the epistemic variance (inherent data noise → irreducible)

Reference:
    Gal, Y. & Ghahramani, Z. (2016). Dropout as a Bayesian Approximation:
    Representing Model Uncertainty in Deep Learning. ICML.

Usage:
    python uncertainty_decomposition.py
=============================================================================
"""

import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ---------------------------------------------------------------------------
# Global configuration
# ---------------------------------------------------------------------------
MC_N_PASSES = 30            # Number of stochastic forward passes (M = 30)
DROPOUT_RATE = 0.15         # Dropout probability used in the MLP
SEED = 42                   # Reproducibility seed
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Publication-quality plot defaults
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "legend.fontsize": 9.5,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.grid": True,
    "grid.alpha": 0.35,
})

# ---------------------------------------------------------------------------
# MLP with Dropout (used for MC Dropout inference)
# ---------------------------------------------------------------------------

class MLPWithDropout(nn.Module):
    """
    Simple Multi-Layer Perceptron with dropout layers.

    Architecture:
        Input(n_features) → FC(64) → ReLU → Dropout(p)
        → FC(32) → ReLU → Dropout(p)
        → FC(1)  (scalar regression output)

    Dropout is enabled at BOTH training and inference time for MC Dropout.
    """

    def __init__(self, n_features: int = 1, hidden_sizes=(64, 32),
                 dropout_rate: float = DROPOUT_RATE):
        super().__init__()
        layers = []
        in_dim = n_features
        for h_dim in hidden_sizes:
            layers.append(nn.Linear(in_dim, h_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(p=dropout_rate))
            in_dim = h_dim
        layers.append(nn.Linear(in_dim, 1))       # scalar output
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass (dropout active when model is in train mode)."""
        return self.net(x).squeeze(-1)             # (batch,)


# ---------------------------------------------------------------------------
# 1. MC Dropout single-sample prediction
# ---------------------------------------------------------------------------

def mc_dropout_predict(
    model: nn.Module,
    x: torch.Tensor,
    n_passes: int = MC_N_PASSES,
) -> tuple:
    """
    Perform M stochastic forward passes with dropout enabled and decompose
    the predictive uncertainty.

    Parameters
    ----------
    model : nn.Module
        Trained neural network with Dropout layers.
    x : torch.Tensor
        Input tensor of shape (n_samples, n_features) or (n_features,).
    n_passes : int
        Number of Monte Carlo stochastic forward passes (default M = 30).

    Returns
    -------
    mean_pred : np.ndarray, shape (n_samples,)
        Mean of the M MC predictions:  E_m[f_m(x)].
    epistemic_var : np.ndarray, shape (n_samples,)
        Variance of the M MC predictions: Var_m[f_m(x)].
        Represents uncertainty due to model parameters (reducible).
    aleatoric_var : np.ndarray, shape (n_samples,)
        Mean squared residual minus epistemic variance:
        E_m[(f_m(x) - y)^2] - Var_m[f_m(x)] ≈ (E_m[f_m(x)] - y)^2.
        Represents inherent data noise (irreducible).
        NOTE: When y_true is not provided this defaults to zero; use
        ``decompose_uncertainty`` for data-driven aleatoric estimates.
    total_var : np.ndarray, shape (n_samples,)
        epistemic_var + aleatoric_var.
    all_predictions : np.ndarray, shape (n_passes, n_samples,)
        Raw M predictions for downstream analysis.
    """
    was_training = model.training
    model.train()                   # <-- ENABLE dropout for MC sampling
    predictions = []
    with torch.no_grad():
        for _ in range(n_passes):
            pred = model(x).cpu().numpy()
            predictions.append(pred)
    model.train(was_training)      # restore original mode

    all_predictions = np.stack(predictions, axis=0)       # (M, n_samples)
    mean_pred = all_predictions.mean(axis=0)            # (n_samples,)
    epistemic_var = all_predictions.var(axis=0)           # Var across MC passes

    # Aleatoric = total predictive variance - epistemic
    # When true labels are unavailable we report epistemic as the total.
    total_var = epistemic_var.copy()
    aleatoric_var = np.zeros_like(epistemic_var)

    return mean_pred, epistemic_var, aleatoric_var, total_var, all_predictions


# ---------------------------------------------------------------------------
# 2. Full-dataset uncertainty decomposition
# ---------------------------------------------------------------------------

def decompose_uncertainty(
    model: nn.Module,
    dataloader,
    n_passes: int = MC_N_PASSES,
) -> dict:
    """
    Run MC Dropout uncertainty decomposition over an entire dataset.

    For every sample the decomposition follows:

        sigma^2_total  = E_m[(f_m(x) - y)^2]
        sigma^2_epi    = Var_m[f_m(x)]
        sigma^2_alea   = sigma^2_total - sigma^2_epi

    so that  sigma^2_total = sigma^2_epi + sigma^2_alea  exactly.

    Parameters
    ----------
    model : nn.Module
        Trained model with Dropout layers.
    dataloader : torch.utils.data.DataLoader
        DataLoader yielding (x, y) batches.
    n_passes : int
        Number of MC forward passes.

    Returns
    -------
    results : dict
        Keys:
            'mean_pred'       : np.ndarray (N,)  — mean MC prediction
            'epistemic_var'   : np.ndarray (N,)  — epistemic uncertainty
            'aleatoric_var'   : np.ndarray (N,)  — aleatoric uncertainty
            'total_var'       : np.ndarray (N,)  — total predictive variance
            'y_true'          : np.ndarray (N,)  — ground-truth targets
            'all_predictions'  : np.ndarray (M, N) — raw MC predictions
            'epistemic_pct'   : float — mean epistemic / mean total × 100
            'aleatoric_pct'   : float — mean aleatoric / mean total × 100
    """
    was_training = model.training
    model.train()                   # enable dropout
    all_preds, all_y = [], []

    with torch.no_grad():
        for xb, yb in dataloader:
            xb = xb.to(DEVICE)
            batch_preds = []
            for _ in range(n_passes):
                pred = model(xb).cpu().numpy()
                batch_preds.append(pred)
            # batch_preds: list of length n_passes, each (batch_size,)
            all_preds.append(np.stack(batch_preds, axis=0))   # (M, B)
            all_y.append(yb.numpy() if isinstance(yb, torch.Tensor) else yb)

    model.train(was_training)

    # Concatenate across batches → (M, N) and (N,)
    all_preds = np.concatenate(all_preds, axis=1)
    y_true = np.concatenate(all_y, axis=0)

    M = all_preds.shape[0]
    mean_pred = all_preds.mean(axis=0)                        # (N,)
    epistemic_var = all_preds.var(axis=0)                       # Var across M

    # Total predictive variance = E_m[(f_m - y)^2]
    squared_residuals = (all_preds - y_true[np.newaxis, :]) ** 2  # (M, N)
    total_var = squared_residuals.mean(axis=0)                   # (N,)

    # Aleatoric = total - epistemic (may be clipped to >= 0)
    aleatoric_var = total_var - epistemic_var
    aleatoric_var = np.maximum(aleatoric_var, 0.0)

    # Ensure identity: total = epi + alea
    total_var = epistemic_var + aleatoric_var

    # Percentage split (averaged over all samples)
    mean_total = total_var.mean()
    epi_pct = (epistemic_var.mean() / mean_total) * 100.0 if mean_total > 0 else 0.0
    alea_pct = (aleatoric_var.mean() / mean_total) * 100.0 if mean_total > 0 else 0.0

    return {
        "mean_pred": mean_pred,
        "epistemic_var": epistemic_var,
        "aleatoric_var": aleatoric_var,
        "total_var": total_var,
        "y_true": y_true,
        "all_predictions": all_preds,
        "epistemic_pct": epi_pct,
        "aleatoric_pct": alea_pct,
    }


# ---------------------------------------------------------------------------
# 3. Plot: epistemic vs aleatoric bar chart (per task)
# ---------------------------------------------------------------------------

def plot_uncertainty_decomposition(
    task_results: list,
    task_labels: list,
    save_path: str = None,
):
    """
    Bar chart comparing mean epistemic and aleatoric uncertainty per task.

    Parameters
    ----------
    task_results : list of dict
        Each element is the dict returned by ``decompose_uncertainty`` for
        one task / data segment.
    task_labels : list of str
        Human-readable task names (e.g., ['Task 1', 'Task 2', ...]).
    save_path : str or None
        If provided, saves the figure to this path.
    """
    n_tasks = len(task_results)
    epi_means = [np.mean(r["epistemic_var"]) for r in task_results]
    alea_means = [np.mean(r["aleatoric_var"]) for r in task_results]
    total_means = [e + a for e, a in zip(epi_means, alea_means)]

    # Percentages per task
    epi_pcts = [e / t * 100 if t > 0 else 0 for e, t in zip(epi_means, total_means)]
    alea_pcts = [a / t * 100 if t > 0 else 0 for a, t in zip(alea_means, total_means)]

    x = np.arange(n_tasks)
    width = 0.35

    fig, ax1 = plt.subplots(figsize=(10, 5.5))

    # --- Absolute values (left y-axis) ---
    bars1 = ax1.bar(x - width / 2, epi_means, width, label="Epistemic",
                    color="#4C72B0", edgecolor="white", linewidth=0.5)
    bars2 = ax1.bar(x + width / 2, alea_means, width, label="Aleatoric",
                    color="#DD8452", edgecolor="white", linewidth=0.5)
    ax1.set_ylabel("Mean Variance", fontsize=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(task_labels, fontsize=10)
    ax1.legend(loc="upper left", framealpha=0.9)

    # --- Percentage annotations on bars ---
    for bar, pct in zip(bars1, epi_pcts):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                 f"{pct:.1f}%", ha="center", va="bottom", fontsize=8,
                 fontweight="bold", color="#4C72B0")
    for bar, pct in zip(bars2, alea_pcts):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                 f"{pct:.1f}%", ha="center", va="bottom", fontsize=8,
                 fontweight="bold", color="#DD8452")

    # --- Secondary axis: total uncertainty line ---
    ax2 = ax1.twinx()
    ax2.plot(x, total_means, "k--o", markersize=6, linewidth=1.2,
             alpha=0.7, label="Total")
    ax2.set_ylabel("Total Variance", fontsize=12, color="gray")
    ax2.tick_params(axis="y", labelcolor="gray")
    ax2.legend(loc="upper right", framealpha=0.9)

    ax1.set_title("Uncertainty Decomposition: Epistemic vs Aleatoric per Task",
                  fontsize=13, fontweight="bold", pad=12)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path)
        print(f"[saved] {save_path}")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 4. Plot: time-series with uncertainty bands
# ---------------------------------------------------------------------------

def plot_prediction_with_uncertainty(
    x: np.ndarray,
    y_true: np.ndarray,
    mean_pred: np.ndarray,
    epistemic: np.ndarray,
    aleatoric: np.ndarray,
    title: str = "Prediction with Uncertainty Bands",
    save_path: str = None,
):
    """
    Plot a time-series (or 1-D regression) with shaded uncertainty bands.

    Three nested bands are drawn:
        1. Total uncertainty    (aleatoric + epistemic) — lightest shade
        2. Epistemic only       — medium shade
        3. Mean prediction line — solid

    Parameters
    ----------
    x : np.ndarray, shape (N,)
        x-axis values (e.g., time steps or sorted input).
    y_true : np.ndarray, shape (N,)
        Ground-truth targets.
    mean_pred : np.ndarray, shape (N,)
        Mean of MC predictions.
    epistemic : np.ndarray, shape (N,)
        Epistemic variance per sample.
    aleatoric : np.ndarray, shape (N,)
        Aleatoric variance per sample.
    title : str
        Plot title.
    save_path : str or None
        If provided, saves the figure.
    """
    total_std = np.sqrt(epistemic + aleatoric)
    epi_std = np.sqrt(epistemic)

    fig, ax = plt.subplots(figsize=(12, 5))

    # True signal
    ax.plot(x, y_true, "k-", linewidth=1.0, alpha=0.6, label="True")

    # Total uncertainty band (±2σ)
    ax.fill_between(x, mean_pred - 2 * total_std, mean_pred + 2 * total_std,
                    color="#C44E52", alpha=0.12, label="Total ±2σ")

    # Epistemic uncertainty band (±2σ)
    ax.fill_between(x, mean_pred - 2 * epi_std, mean_pred + 2 * epi_std,
                    color="#4C72B0", alpha=0.25, label="Epistemic ±2σ")

    # Mean prediction
    ax.plot(x, mean_pred, color="#4C72B0", linewidth=1.5, label="Mean Prediction")

    # Mark high-epistemic regions (epistemic > 75th percentile)
    epi_threshold = np.percentile(epistemic, 75)
    high_epi = epistemic > epi_threshold
    if high_epi.any():
        ax.scatter(x[high_epi], mean_pred[high_epi], c="red", s=10,
                   zorder=5, alpha=0.6, label=f"High Epistemic (>P75)")

    ax.set_xlabel("Sample Index / Time", fontsize=12)
    ax.set_ylabel("Value", fontsize=12)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.legend(loc="upper left", fontsize=9, framealpha=0.9)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path)
        print(f"[saved] {save_path}")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Synthetic data generation (multi-task regime for EWC-IXER experiments)
# ---------------------------------------------------------------------------

def generate_synthetic_multitask_data(
    n_tasks: int = 5,
    n_samples_per_task: int = 200,
    noise_std: float = 0.4,
    seed: int = SEED,
):
    """
    Generate a synthetic regression dataset with distinct tasks / regimes.

    Each task has a different underlying function of the form:
        y = a * sin(b * x + phase) + c * x + noise

    Task boundaries introduce distribution shift, which is expected to
    manifest as elevated epistemic uncertainty (the model is uncertain about
    the new regime before adapting).

    Parameters
    ----------
    n_tasks : int
        Number of sequential tasks / regimes.
    n_samples_per_task : int
        Number of data points per task.
    noise_std : float
        Standard deviation of Gaussian observation noise (aleatoric source).
    seed : int
        Random seed.

    Returns
    -------
    x_all : np.ndarray (N,)
        Input feature.
    y_all : np.ndarray (N,)
        Noisy targets.
    task_indices : list of (start, end)
        Slice indices for each task.
    """
    rng = np.random.RandomState(seed)
    x_all, y_all = [], []
    task_indices = []

    # Per-task function parameters (amplitude, frequency, phase, linear trend)
    task_params = [
        (1.0,  1.0,  0.0,  0.2),    # Task 1
        (1.5,  0.8,  1.5, -0.1),    # Task 2
        (0.7,  1.3,  3.0,  0.3),    # Task 3
        (1.2,  0.5,  4.5, -0.2),    # Task 4
        (0.9,  1.1,  2.0,  0.15),   # Task 5
    ]
    if n_tasks > len(task_params):
        # Generate additional random params if needed
        extra = [(rng.uniform(0.5, 1.5), rng.uniform(0.3, 1.5),
                  rng.uniform(0, 2 * np.pi), rng.uniform(-0.3, 0.3))
                 for _ in range(n_tasks - len(task_params))]
        task_params.extend(extra)
    task_params = task_params[:n_tasks]

    for t_idx in range(n_tasks):
        start = len(x_all)
        x_task = np.linspace(t_idx * 2 * np.pi, (t_idx + 1) * 2 * np.pi,
                             n_samples_per_task)
        a, b, phase, c = task_params[t_idx]
        y_task = (a * np.sin(b * x_task + phase) + c * x_task
                  + rng.normal(0, noise_std, size=n_samples_per_task))
        x_all.append(x_task)
        y_all.append(y_task)
        task_indices.append((start, start + n_samples_per_task))

    x_all = np.concatenate(x_all)
    y_all = np.concatenate(y_all)
    return x_all, y_all, task_indices


# ---------------------------------------------------------------------------
# Training routine
# ---------------------------------------------------------------------------

def train_model(
    model: nn.Module,
    x_train: torch.Tensor,
    y_train: torch.Tensor,
    n_epochs: int = 200,
    lr: float = 1e-3,
    batch_size: int = 64,
    verbose: bool = True,
):
    """
    Train an MLP with standard MSE loss.

    Parameters
    ----------
    model : nn.Module
    x_train : torch.Tensor, shape (N, 1)
    y_train : torch.Tensor, shape (N,)
    n_epochs : int
    lr : float
    batch_size : int
    verbose : bool

    Returns
    -------
    model : nn.Module  (trained, in eval mode)
    losses : list of float
    """
    model.train()
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-5)
    criterion = nn.MSELoss()
    dataset = torch.utils.data.TensorDataset(x_train, y_train)
    loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size,
                                         shuffle=True)
    losses = []

    for epoch in range(1, n_epochs + 1):
        epoch_loss = 0.0
        for xb, yb in loader:
            xb, yb = xb.to(DEVICE), yb.to(DEVICE)
            optimizer.zero_grad()
            pred = model(xb)
            loss = criterion(pred, yb)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * xb.size(0)
        epoch_loss /= len(dataset)
        losses.append(epoch_loss)
        if verbose and (epoch % 50 == 0 or epoch == 1):
            print(f"  Epoch {epoch:>4d}/{n_epochs}  |  MSE Loss = {epoch_loss:.6f}")

    model.eval()
    return model, losses


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 72)
    print("  Uncertainty Decomposition — EWC-IXER Module")
    print("  MC Dropout: M = {} passes, dropout rate = {}".format(
        MC_N_PASSES, DROPOUT_RATE))
    print("  Device: {}".format(DEVICE))
    print("=" * 72)

    # ------------------------------------------------------------------
    # (a) Generate synthetic multi-task data
    # ------------------------------------------------------------------
    n_tasks = 5
    n_per_task = 200
    noise_std = 0.40     # Controls aleatoric noise level
    n_total = n_tasks * n_per_task

    x_data, y_data, task_slices = generate_synthetic_multitask_data(
        n_tasks=n_tasks,
        n_samples_per_task=n_per_task,
        noise_std=noise_std,
    )
    print(f"\n[1] Synthetic data: {n_total} samples across {n_tasks} tasks "
          f"({n_per_task}/task, noise_std={noise_std})")

    # Normalise inputs for stable training
    x_mean, x_std = x_data.mean(), x_data.std()
    y_mean, y_std = y_data.mean(), y_data.std()
    x_norm = (x_data - x_mean) / (x_std + 1e-8)
    y_norm = (y_data - y_mean) / (y_std + 1e-8)

    x_tensor = torch.tensor(x_norm, dtype=torch.float32).unsqueeze(1).to(DEVICE)
    y_tensor = torch.tensor(y_norm, dtype=torch.float32).to(DEVICE)
    full_loader = torch.utils.data.DataLoader(
        torch.utils.data.TensorDataset(x_tensor, y_tensor), batch_size=256)

    # ------------------------------------------------------------------
    # (b) Create and train MLP with dropout
    # ------------------------------------------------------------------
    torch.manual_seed(SEED)
    np.random.seed(SEED)

    model = MLPWithDropout(n_features=1, hidden_sizes=(64, 32),
                           dropout_rate=DROPOUT_RATE).to(DEVICE)

    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"\n[2] MLP architecture: {sum(1 for m in model.modules() if isinstance(m, nn.Linear))} linear layers, "
          f"{n_params} trainable parameters")
    print("    Training ...")

    model, losses = train_model(model, x_tensor, y_tensor,
                                n_epochs=300, lr=2e-3, batch_size=64)
    print(f"    Final MSE Loss = {losses[-1]:.6f}")

    # ------------------------------------------------------------------
    # (c) Run MC Dropout uncertainty decomposition
    # ------------------------------------------------------------------
    print(f"\n[3] Running MC Dropout inference ({MC_N_PASSES} passes) ...")
    results = decompose_uncertainty(model, full_loader, n_passes=MC_N_PASSES)

    epi_pct = results["epistemic_pct"]
    alea_pct = results["aleatoric_pct"]

    print(f"\n    {'─' * 46}")
    print(f"    EPISTEMIC  UNCERTAINTY :  {epi_pct:6.2f}%  of total")
    print(f"    ALEATORIC  UNCERTAINTY :  {alea_pct:6.2f}%  of total")
    print(f"    TOTAL               : 100.00%")
    print(f"    {'─' * 46}")

    # Per-task breakdown
    print(f"\n[4] Per-task uncertainty decomposition:")
    print(f"    {'Task':<10} {'Epistemic':>12} {'Aleatoric':>12} {'Total':>12} {'Epi%':>8}")
    print(f"    {'─' * 56}")

    task_labels = []
    task_results_list = []

    for t in range(n_tasks):
        s, e = task_slices[t]
        epi_t = results["epistemic_var"][s:e].mean()
        alea_t = results["aleatoric_var"][s:e].mean()
        tot_t = epi_t + alea_t
        epi_pct_t = (epi_t / tot_t * 100) if tot_t > 0 else 0
        label = f"Task {t + 1}"
        task_labels.append(label)
        print(f"    {label:<10} {epi_t:>12.6f} {alea_t:>12.6f} "
              f"{tot_t:>12.6f} {epi_pct_t:>7.1f}%")
        task_results_list.append({
            "epistemic_var": results["epistemic_var"][s:e],
            "aleatoric_var": results["aleatoric_var"][s:e],
            "total_var": results["total_var"][s:e],
        })

    # ------------------------------------------------------------------
    # (d) Verify expected paper results
    # ------------------------------------------------------------------
    print(f"\n[5] Validation against EWC-IXER paper expectations:")
    print(f"    Paper target:  Epistemic ≈ 50.8%,  Aleatoric ≈ 49.2%")
    print(f"    Observed   :  Epistemic ≈ {epi_pct:.1f}%,  Aleatoric ≈ {alea_pct:.1f}%")
    delta = abs(epi_pct - 50.8)
    status = "✓ Within tolerance" if delta < 10 else "⚠ Outside tolerance"
    print(f"    Deviation from 50.8%: {delta:+.1f}pp  → {status}")

    # Verify epistemic spikes at task boundaries
    boundary_epistemic = []
    within_epistemic = []
    for t in range(n_tasks):
        s, e = task_slices[t]
        segment_epi = results["epistemic_var"][s:e]
        # First 10% of task (boundary region)
        n_boundary = max(1, int(0.10 * (e - s)))
        boundary_epistemic.append(segment_epi[:n_boundary].mean())
        within_epistemic.append(segment_epi[n_boundary:].mean())

    mean_boundary = np.mean(boundary_epistemic)
    mean_within = np.mean(within_epistemic)
    print(f"\n    Epistemic at boundaries (first 10%):  {mean_boundary:.6f}")
    print(f"    Epistemic within tasks  (rest 90%):   {mean_within:.6f}")
    if mean_boundary > mean_within:
        print(f"    → Epistemic HIGHER at boundaries ✓ (as expected)")
    else:
        print(f"    → Epistemic not higher at boundaries (model may be well-calibrated)")

    # ------------------------------------------------------------------
    # (e) Generate publication-quality plots
    # ------------------------------------------------------------------
    out_dir = os.path.dirname(os.path.abspath(__file__))

    # Plot A: Bar chart — epistemic vs aleatoric per task
    bar_path = os.path.join(out_dir, "uncertainty_decomposition_bar.png")
    print(f"\n[6] Generating plots ...")
    plot_uncertainty_decomposition(task_results_list, task_labels,
                                   save_path=bar_path)

    # Plot B: Time-series with uncertainty bands
    ts_path = os.path.join(out_dir, "uncertainty_timeseries.png")
    plot_prediction_with_uncertainty(
        x=np.arange(n_total),
        y_true=y_data,  # use original (unnormalised) y for readability
        mean_pred=results["mean_pred"] * y_std + y_mean,
        epistemic=results["epistemic_var"] * y_std ** 2,
        aleatoric=results["aleatoric_var"] * y_std ** 2,
        title="MC Dropout Prediction with Epistemic & Aleatoric Uncertainty",
        save_path=ts_path,
    )

    # Plot C: Epistemic uncertainty profile ( highlighting task boundaries )
    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True,
                              gridspec_kw={"height_ratios": [1, 1, 0.6]})

    # Panel 1 — True signal + prediction
    axes[0].plot(x_data, y_data, "k-", lw=0.8, alpha=0.5, label="True")
    axes[0].plot(x_data, results["mean_pred"] * y_std + y_mean,
                 "b-", lw=1.2, alpha=0.8, label="Mean Pred")
    for t in range(n_tasks):
        s, e = task_slices[t]
        axes[0].axvline(x_data[s], color="red", ls="--", lw=0.7, alpha=0.5)
    axes[0].set_ylabel("Value")
    axes[0].legend(loc="upper left", fontsize=8)
    axes[0].set_title("EWC-IXER Uncertainty Decomposition (MC Dropout, M={})".format(
        MC_N_PASSES), fontweight="bold", fontsize=13)

    # Panel 2 — Epistemic and Aleatoric traces
    epi_trace = results["epistemic_var"] * y_std ** 2
    alea_trace = results["aleatoric_var"] * y_std ** 2
    axes[1].plot(x_data, epi_trace, color="#4C72B0", lw=1.0, alpha=0.8,
                 label="Epistemic")
    axes[1].plot(x_data, alea_trace, color="#DD8452", lw=1.0, alpha=0.8,
                 label="Aleatoric")
    axes[1].plot(x_data, epi_trace + alea_trace, "k--", lw=0.8, alpha=0.5,
                 label="Total")
    for t in range(n_tasks):
        s, e = task_slices[t]
        axes[1].axvline(x_data[s], color="red", ls="--", lw=0.7, alpha=0.5)
    axes[1].set_ylabel("Variance")
    axes[1].legend(loc="upper left", fontsize=8)

    # Panel 3 — Epistemic ratio (% of total)
    total_trace = epi_trace + alea_trace + 1e-12
    ratio = epi_trace / total_trace * 100
    axes[2].fill_between(x_data, 0, ratio, color="#4C72B0", alpha=0.3)
    axes[2].plot(x_data, ratio, color="#4C72B0", lw=0.8)
    axes[2].axhline(50.8, color="gray", ls=":", lw=0.8, alpha=0.6)
    axes[2].text(x_data[-1], 50.8 + 1, "paper target 50.8%",
                 ha="right", fontsize=8, color="gray")
    for t in range(n_tasks):
        s, e = task_slices[t]
        axes[2].axvline(x_data[s], color="red", ls="--", lw=0.7, alpha=0.5)
        mid = (s + e) // 2
        axes[2].text(x_data[mid], 95, f"T{t+1}", ha="center", fontsize=9,
                     fontweight="bold", color="red")
    axes[2].set_ylabel("Epi %")
    axes[2].set_xlabel("Sample Index")
    axes[2].set_ylim(0, 105)

    fig.tight_layout()
    profile_path = os.path.join(out_dir, "uncertainty_profile.png")
    fig.savefig(profile_path, dpi=300)
    plt.close(fig)
    print(f"    [saved] {profile_path}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print(f"\n{'=' * 72}")
    print(f"  SUMMARY")
    print(f"{'=' * 72}")
    print(f"  Total samples      : {n_total}")
    print(f"  MC passes (M)      : {MC_N_PASSES}")
    print(f"  Dropout rate       : {DROPOUT_RATE}")
    print(f"  Epistemic  (mean)  : {epi_pct:.2f}%")
    print(f"  Aleatoric  (mean)  : {alea_pct:.2f}%")
    print(f"  Boundary epistemic: {mean_boundary:.6f}")
    print(f"  Within-task epi    : {mean_within:.6f}")
    print(f"  Output plots       :")
    print(f"    → {bar_path}")
    print(f"    → {ts_path}")
    print(f"    → {profile_path}")
    print(f"{'=' * 72}\n")
