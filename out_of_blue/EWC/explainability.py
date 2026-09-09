#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Explainability Analysis for EWC-IXER Paper
==========================================
SHAP-based feature importance analysis for continual smart grid voltage prediction.

This module provides:
  - SHAP feature importance computation for the trained EWC-IXER model
  - Feature importance drift analysis across sequential tasks
  - Publication-quality visualization (bar plots, drift plots)

Expected results from the paper:
  - Load_kW:       mean SHAP ~ 0.0347 (highest)
  - Temperature_C: mean SHAP ~ 0.0307
  - Wind_Power:    mean SHAP ~ 0.0265
  - Solar_Power:   mean SHAP ~ 0.0213
  - Humidity:      mean SHAP ~ 0.0138

Reference:
  Lundberg, S.M. and Lee, S.I. "A unified approach to interpreting model
  predictions." NeurIPS, pp. 4765-4774, 2017.
"""

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

# ---------- Attempt to import SHAP; provide a fallback if unavailable ----------
try:
    import shap
    HAS_SHAP = True
except ImportError:
    HAS_SHAP = False
    print("[WARNING] shap package not found. Install with: pip install shap")
    print("[WARNING] Falling back to a gradient-based surrogate for SHAP values.")


# ============================================================================
#  MLP Model (same architecture as in ewc_ixer_model.py)
# ============================================================================
class MLPPredictor(nn.Module):
    """Two-layer MLP: 5 -> 32 (ReLU, 20% dropout) -> 1 (linear)."""
    def __init__(self, input_dim=5, hidden_dim=32, dropout=0.2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)


# ============================================================================
#  SHAP-Based Feature Importance
# ============================================================================
def compute_shap_values(model, X_background, X_eval, device="cpu"):
    """
    Compute SHAP values using DeepExplainer (if shap available)
    or a gradient-based surrogate.

    Parameters
    ----------
    model : nn.Module
        Trained neural network model.
    X_background : np.ndarray, shape (n_bg, n_features)
        Background dataset for SHAP DeepExplainer.
    X_eval : np.ndarray, shape (n_eval, n_features)
        Evaluation dataset.
    device : str
        'cpu' or 'cuda'.

    Returns
    -------
    shap_values : np.ndarray, shape (n_eval, n_features)
    base_value : float
    """
    model.eval()
    model.to(device)

    if HAS_SHAP:
        # --- Use the real SHAP DeepExplainer ---
        bg_tensor = torch.FloatTensor(X_background).to(device)
        eval_tensor = torch.FloatTensor(X_eval).to(device)

        explainer = shap.DeepExplainer(model, bg_tensor)
        shap_vals = explainer.shap_values(eval_tensor)

        if isinstance(shap_vals, list):
            shap_vals = shap_vals[0]  # DeepExplainer may return list

        base_val = explainer.expected_value
        if isinstance(base_val, (list, np.ndarray)):
            base_val = float(base_val[0]) if len(base_val) > 1 else float(base_val)
        else:
            base_val = float(base_val)

        return np.array(shap_vals), base_val
    else:
        # --- Gradient-based surrogate for SHAP values ---
        # Approximate feature importance via Integrated Gradients
        eval_tensor = torch.FloatTensor(X_eval).to(device).requires_grad_(True)
        bg_tensor = torch.FloatTensor(X_background).mean(dim=0).to(device)

        n_steps = 50
        alphas = np.linspace(0, 1, n_steps)
        integrated_grads = np.zeros_like(X_eval)

        for alpha in alphas:
            interpolated = bg_tensor.unsqueeze(0) + alpha * (eval_tensor - bg_tensor.unsqueeze(0))
            interpolated.requires_grad_(True)
            outputs = model(interpolated)
            outputs.backward(torch.ones_like(outputs), retain_graph=True)
            if eval_tensor.grad is not None:
                integrated_grads += (eval_tensor.grad.detach().cpu().numpy())
            eval_tensor.grad = None

        integrated_grads /= n_steps
        # SHAP-like values: IG * (x - x_baseline)
        shap_surrogate = integrated_grads * (X_eval - X_background.mean(axis=0))
        base_val = float(model(bg_tensor.unsqueeze(0)).detach().cpu().numpy())
        return shap_surrogate, base_val


def compute_per_task_shap(model, task_datasets, n_background=50, device="cpu"):
    """
    Compute SHAP values for each task and aggregate feature importance.

    Parameters
    ----------
    model : nn.Module
    task_datasets : list of (X_train, y_train, X_test, y_test) tuples
    n_background : int
        Number of background samples for SHAP.
    device : str

    Returns
    -------
    task_shap_importance : dict[int, np.ndarray]
        Mean absolute SHAP value per feature for each task.
    task_shap_values : dict[int, np.ndarray]
        Full SHAP value matrix per task.
    """
    feature_names = ["Load_kW", "Solar_Power", "Wind_Power", "Temperature_C", "Humidity"]
    task_shap_importance = {}
    task_shap_values = {}

    for task_id, (X_train, y_train, X_test, y_test) in enumerate(task_datasets):
        # Subsample background
        idx = np.random.choice(len(X_train), min(n_background, len(X_train)), replace=False)
        X_bg = X_train[idx]

        shap_vals, base_val = compute_shap_values(model, X_bg, X_test, device)

        # Mean absolute SHAP value per feature
        mean_abs_shap = np.mean(np.abs(shap_vals), axis=0)
        task_shap_importance[task_id] = mean_abs_shap
        task_shap_values[task_id] = shap_vals

        print(f"Task {task_id + 1}: mean |SHAP| = {mean_abs_shap}")
        for fn, sv in zip(feature_names, mean_abs_shap):
            print(f"  {fn:15s}: {sv:.4f}")

    return task_shap_importance, task_shap_values


# ============================================================================
#  Visualization
# ============================================================================
FEATURE_NAMES = ["Load_kW", "Solar_Power", "Wind_Power", "Temperature_C", "Humidity"]
TASK_NAMES = ["Spring", "Summer", "Autumn", "Winter", "Shoulder"]
TASK_COLORS = ["#2ecc71", "#e74c3c", "#f39c12", "#3498db", "#9b59b6"]


def plot_shap_importance_bar(task_shap_importance, save_path=None):
    """
    Bar plot of mean |SHAP| values across all tasks (aggregated).
    Expected ranking: Load_kW > Temperature_C > Wind_Power > Solar_Power > Humidity.
    """
    all_vals = np.array(list(task_shap_importance.values()))  # (n_tasks, n_features)
    mean_importance = all_vals.mean(axis=0)
    std_importance = all_vals.std(axis=0)

    # Sort by mean importance
    sorted_idx = np.argsort(mean_importance)[::-1]
    sorted_names = [FEATURE_NAMES[i] for i in sorted_idx]
    sorted_means = mean_importance[sorted_idx]
    sorted_stds = std_importance[sorted_idx]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(range(len(sorted_names)), sorted_means, xerr=sorted_stds,
                   color=["#2c3e50"], edgecolor="#1a252f", alpha=0.85, capsize=4)
    ax.set_yticks(range(len(sorted_names)))
    ax.set_yticklabels(sorted_names, fontsize=11)
    ax.set_xlabel("Mean |SHAP Value|", fontsize=12)
    ax.set_title("Feature Importance (SHAP)\nAcross All Sequential Tasks", fontsize=13, fontweight="bold")
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Saved: {save_path}")
    plt.close(fig)


def plot_shap_drift_across_tasks(task_shap_importance, save_path=None):
    """
    Line plot showing how SHAP feature importance drifts across tasks.
    Expected: Load_kW importance increases monotonically (10% per-task load growth),
    Temperature shows seasonal pattern (peaks in summer/winter tasks).
    """
    n_tasks = len(task_shap_importance)
    task_ids = list(range(1, n_tasks + 1))

    fig, ax = plt.subplots(figsize=(10, 6))
    for feat_idx, fname in enumerate(FEATURE_NAMES):
        vals = [task_shap_importance[t][feat_idx] for t in range(n_tasks)]
        ax.plot(task_ids, vals, marker="o", linewidth=2, markersize=7,
                label=fname, color=TASK_COLORS[feat_idx] if feat_idx < len(TASK_COLORS) else None)

    ax.set_xlabel("Task ID (Seasonal Regime)", fontsize=12)
    ax.set_ylabel("Mean |SHAP Value|", fontsize=12)
    ax.set_title("Feature Importance Drift Across Sequential Tasks\n(SHAP Analysis)",
                 fontsize=13, fontweight="bold")
    ax.set_xticks(task_ids)
    ax.set_xticklabels(TASK_NAMES[:n_tasks], fontsize=10)
    ax.legend(loc="upper left", fontsize=9, framealpha=0.9)
    ax.grid(alpha=0.3)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Saved: {save_path}")
    plt.close(fig)


def plot_shap_heatmap(task_shap_importance, save_path=None):
    """
    Heatmap of feature importance across tasks.
    Rows = features, Columns = tasks.
    """
    n_tasks = len(task_shap_importance)
    matrix = np.array([task_shap_importance[t] for t in range(n_tasks)]).T  # (n_features, n_tasks)

    fig, ax = plt.subplots(figsize=(8, 4))
    im = ax.imshow(matrix, cmap="YlOrRd", aspect="auto")
    ax.set_xticks(range(n_tasks))
    ax.set_xticklabels(TASK_NAMES[:n_tasks], fontsize=10)
    ax.set_yticks(range(len(FEATURE_NAMES)))
    ax.set_yticklabels(FEATURE_NAMES, fontsize=10)
    ax.set_title("Feature Importance Heatmap (Mean |SHAP|)", fontsize=13, fontweight="bold")

    # Annotate cells
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            ax.text(j, i, f"{matrix[i, j]:.4f}", ha="center", va="center",
                    fontsize=8, color="white" if matrix[i, j] > matrix.max() * 0.6 else "black")

    fig.colorbar(im, ax=ax, label="Mean |SHAP Value|")
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Saved: {save_path}")
    plt.close(fig)


# ============================================================================
#  Main Demo
# ============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("  Explainability Analysis for EWC-IXER")
    print("  SHAP Feature Importance & Drift Across Tasks")
    print("=" * 70)

    np.random.seed(42)
    torch.manual_seed(42)
    device = "cpu"
    output_dir = os.path.dirname(os.path.abspath(__file__))

    # --- 1. Generate synthetic smart grid data (5 tasks) ---
    from synthetic_smart_grid_dataset import generate_dataset as generate_synthetic_dataset
    tasks = generate_synthetic_dataset(seed=42)

    task_datasets = []
    for key in tasks:
        task_data = tasks[key]
        X_train = task_data["X_train"]
        y_train = task_data["y_train"]
        X_test = task_data["X_test"]
        y_test = task_data["y_test"]
        task_datasets.append((X_train, y_train, X_test, y_test))
        print(f"Task {task_data['task_id'] + 1}: train={X_train.shape[0]}, test={X_test.shape[0]}")

    # --- 2. Train a simple model on all tasks sequentially (naive for demo) ---
    model = MLPPredictor(input_dim=5, hidden_dim=32, dropout=0.2).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    print("\nTraining MLP on all tasks sequentially...")
    for task_id, (X_train, y_train, _, _) in enumerate(task_datasets):
        train_ds = TensorDataset(torch.FloatTensor(X_train), torch.FloatTensor(y_train))
        train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)

        for epoch in range(50):
            model.train()
            epoch_loss = 0.0
            for X_batch, y_batch in train_loader:
                X_batch, y_batch = X_batch.to(device), y_batch.to(device)
                optimizer.zero_grad()
                y_pred = model(X_batch)
                loss = criterion(y_pred, y_batch)
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item() * len(X_batch)
            if (epoch + 1) % 10 == 0:
                print(f"  Task {task_id + 1}, Epoch {epoch + 1}/50, Loss: {epoch_loss / len(X_train):.6f}")

    # --- 3. Compute SHAP values per task ---
    print("\nComputing SHAP feature importance per task...")
    model.eval()
    task_shap_importance, task_shap_values = compute_per_task_shap(
        model, task_datasets, n_background=50, device=device
    )

    # --- 4. Print summary ---
    print("\n" + "=" * 70)
    print("  FEATURE IMPORTANCE SUMMARY (Mean |SHAP|)")
    print("=" * 70)
    all_vals = np.array(list(task_shap_importance.values()))
    overall_mean = all_vals.mean(axis=0)
    ranking = np.argsort(overall_mean)[::-1]
    print(f"{'Rank':<5}{'Feature':<18}{'Mean |SHAP|':<15}{'Std':<10}")
    print("-" * 48)
    for rank, idx in enumerate(ranking):
        print(f"{rank + 1:<5}{FEATURE_NAMES[idx]:<18}{overall_mean[idx]:<15.4f}{all_vals[:, idx].std():<10.4f}")

    # --- 5. Generate all plots ---
    print("\nGenerating plots...")
    plot_shap_importance_bar(
        task_shap_importance,
        save_path=os.path.join(output_dir, "shap_feature_importance.png")
    )
    plot_shap_drift_across_tasks(
        task_shap_importance,
        save_path=os.path.join(output_dir, "shap_feature_drift.png")
    )
    plot_shap_heatmap(
        task_shap_importance,
        save_path=os.path.join(output_dir, "shap_heatmap.png")
    )

    print("\n" + "=" * 70)
    print("  Explainability analysis complete.")
    print(f"  Plots saved to: {output_dir}/")
    print("=" * 70)
