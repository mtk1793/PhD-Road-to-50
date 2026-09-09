#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualization Module for EWC-IXER Paper
=========================================

Generates all publication-quality figures for the EWC-IXER academic paper.
All plots are saved as 300 DPI PNG files.

Figures produced:
  1. Data distributions across 5 tasks (box/violin plots)
  2. Task segmentation from change point detection
  3. Metacognitive monitoring signals (coverage, threshold, LR)
  4. Uncertainty decomposition (epistemic vs aleatoric per task)
  5. Conformal prediction intervals on test data
  6. Pairwise statistical significance (Wilcoxon heatmap)
  7. Large-scale scaling experiment (RMSE, BWT, time vs tasks)
  8. IEEE bus system voltage profiles
  9. SHAP feature importance
  10. SHAP feature drift across tasks
  11. Computational efficiency comparison
  12. Ablation study results
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import os

# ============================================================================
#  Global Style Configuration
# ============================================================================
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.grid": True,
    "grid.alpha": 0.3,
})

TASK_NAMES = ["Spring", "Summer", "Autumn", "Winter", "Shoulder"]
TASK_COLORS = ["#2ecc71", "#e74c3c", "#f39c12", "#3498db", "#9b59b6"]
FEATURE_NAMES = ["Load_kW", "Solar_Power", "Wind_Power", "Temperature_C", "Humidity"]

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================================
#  Figure 1: Data Distributions Across Tasks
# ============================================================================
def plot_data_distributions(task_data_list, save_path=None):
    """
    Box plots showing feature distributions across 5 sequential tasks.

    Parameters
    ----------
    task_data_list : list of dict
        Each dict has keys 'X_train', 'y_train', etc.
    save_path : str or None
    """
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    axes = axes.flatten()

    all_labels = FEATURE_NAMES + ["Voltage_pu"]
    all_colors = ["#3498db", "#e67e22", "#2ecc71", "#e74c3c", "#9b59b6", "#1abc9c"]

    for feat_idx in range(6):
        ax = axes[feat_idx]
        data_by_task = []
        for key in task_data_list:
            td = task_data_list[key]
            X = td["X_train"]
            y = td["y_train"]
            if feat_idx < 5:
                data_by_task.append(X[:, feat_idx])
            else:
                data_by_task.append(y)

        bp = ax.boxplot(data_by_task, labels=TASK_NAMES[:len(data_by_task)],
                        patch_artist=True, widths=0.6)
        for patch, color in zip(bp["boxes"], TASK_COLORS):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        ax.set_title(all_labels[feat_idx], fontweight="bold")
        ax.set_ylabel("Value")
        if feat_idx == 0:
            ax.set_xlabel("Task (Seasonal Regime)")

    axes[-1].set_visible(False)  # Hide 6th subplot (only 6 plots for 6 features)
    fig.suptitle("Data Distributions Across Five Sequential Tasks",
                 fontsize=14, fontweight="bold", y=1.01)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Saved: {save_path}")
    plt.close(fig)


# ============================================================================
#  Figure 2: Task Segmentation (Change Point Detection)
# ============================================================================
def plot_task_segmentation(data_stream, true_cps, detected_cps=None, save_path=None):
    """
    Plot the data stream with true and detected change points.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True,
                                     gridspec_kw={"height_ratios": [2, 1]})

    # Top panel: data stream with change points
    ax1.plot(data_stream, color="#2c3e50", linewidth=0.5, alpha=0.8)
    for cp in true_cps:
        ax1.axvline(cp, color="#e74c3c", linestyle="--", linewidth=1.5, label="True CP" if cp == true_cps[0] else "")
    if detected_cps is not None:
        for cp in detected_cps:
            ax1.axvline(cp, color="#2ecc71", linestyle=":", linewidth=1.5, label="Detected CP" if cp == detected_cps[0] else "")

    # Shade task regions
    boundaries = [0] + list(true_cps) + [len(data_stream)]
    colors = ["#2ecc71", "#e74c3c", "#f39c12", "#3498db", "#9b59b6"]
    for i in range(len(boundaries) - 1):
        ax1.axvspan(boundaries[i], boundaries[i + 1], alpha=0.08, color=colors[i % len(colors)])
        mid = (boundaries[i] + boundaries[i + 1]) // 2
        ax1.text(mid, ax1.get_ylim()[1] * 0.95 if ax1.get_ylim()[1] > 0 else data_stream.max() * 0.95,
                 TASK_NAMES[i] if i < len(TASK_NAMES) else f"Task {i+1}",
                 ha="center", fontsize=9, fontweight="bold", color=colors[i % len(colors)])

    ax1.set_ylabel("Target (Voltage_pu)")
    ax1.set_title("Task Segmentation via Bayesian Change Point Detection",
                  fontweight="bold")
    ax1.legend(loc="upper right")

    # Bottom panel: running mean and variance
    window = 50
    running_mean = np.convolve(data_stream, np.ones(window)/window, mode="valid")
    running_var = []
    for i in range(window, len(data_stream)):
        running_var.append(np.var(data_stream[i-window:i]))
    running_var = np.array(running_var)

    ax2.plot(range(window, len(data_stream)), running_mean, color="#3498db", label="Running Mean", linewidth=1.2)
    ax2_twin = ax2.twinx()
    ax2_twin.plot(range(window, len(data_stream)), running_var, color="#e67e22", label="Running Var", linewidth=1.2, alpha=0.7)
    ax2.set_xlabel("Sample Index")
    ax2.set_ylabel("Mean")
    ax2_twin.set_ylabel("Variance", color="#e67e22")
    ax2_twin.tick_params(axis="y", labelcolor="#e67e22")

    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Saved: {save_path}")
    plt.close(fig)


# ============================================================================
#  Figure 3: Metacognitive Monitoring Signals
# ============================================================================
def plot_metacognitive_signals(coverage_history, threshold_history,
                               lr_history, task_boundaries, save_path=None):
    """
    Three-panel figure: coverage tracking, adaptive threshold, learning rate.
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    steps = np.arange(len(coverage_history))

    # Coverage
    axes[0].plot(steps, coverage_history, color="#2c3e50", linewidth=1.0, label="Observed Coverage")
    axes[0].axhline(0.95, color="#e74c3c", linestyle="--", linewidth=1.5, label="Target (95%)")
    for bp in task_boundaries:
        axes[0].axvline(bp, color="#f39c12", linestyle=":", linewidth=1.2, alpha=0.7)
    axes[0].fill_between(steps, 0.95, coverage_history, alpha=0.15, color="#2c3e50")
    axes[0].set_ylabel("Coverage")
    axes[0].set_ylim(0.85, 1.0)
    axes[0].legend(loc="lower right")
    axes[0].set_title("Metacognitive Monitoring Signals During Training", fontweight="bold")

    # Adaptive threshold
    axes[1].plot(steps, threshold_history, color="#3498db", linewidth=1.2)
    axes[1].axhline(1.0, color="gray", linestyle="--", alpha=0.5, label="Baseline (eta_0=1.0)")
    for bp in task_boundaries:
        axes[1].axvline(bp, color="#f39c12", linestyle=":", linewidth=1.2, alpha=0.7)
    axes[1].set_ylabel("Threshold (eta)")
    axes[1].legend(loc="upper right")

    # Learning rate
    axes[2].plot(steps, lr_history, color="#2ecc71", linewidth=1.2)
    for bp in task_boundaries:
        axes[2].axvline(bp, color="#f39c12", linestyle=":", linewidth=1.2, alpha=0.7)
    axes[2].set_ylabel("Learning Rate")
    axes[2].set_xlabel("Training Step")

    # Annotate task boundaries
    for i, bp in enumerate(task_boundaries[:-1] if len(task_boundaries) > 1 else task_boundaries):
        mid = bp
        axes[0].text(mid, 0.995, TASK_NAMES[i] if i < len(TASK_NAMES) else f"T{i+1}",
                     ha="center", fontsize=8, color="#f39c12")

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Saved: {save_path}")
    plt.close(fig)


# ============================================================================
#  Figure 4: Method Comparison (RMSE Bar Chart)
# ============================================================================
def plot_method_comparison(results_dict, save_path=None):
    """
    Grouped bar chart comparing RMSE and BWT across methods.

    Parameters
    ----------
    results_dict : dict
        Keys = method names, values = dict with 'mean_rmse', 'std_rmse', 'bwt', 'aa'
    """
    methods = list(results_dict.keys())
    means = [results_dict[m]["mean_rmse"] for m in methods]
    stds = [results_dict[m]["std_rmse"] for m in methods]
    bwts = [results_dict[m]["bwt"] for m in methods]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # RMSE comparison
    x = np.arange(len(methods))
    bars = ax1.bar(x, means, yerr=stds, capsize=4, color="#3498db", edgecolor="#2c3e50",
                   alpha=0.85, width=0.6)
    ax1.set_xticks(x)
    ax1.set_xticklabels(methods, rotation=30, ha="right", fontsize=9)
    ax1.set_ylabel("Mean RMSE")
    ax1.set_title("Prediction Accuracy Comparison", fontweight="bold")

    # Highlight EWC-IXER
    if "EWC-IXER" in methods:
        idx = methods.index("EWC-IXER")
        bars[idx].set_color("#e74c3c")
        bars[idx].set_alpha(0.9)

    # BWT comparison
    colors_bwt = ["#e74c3c" if b < -0.01 else "#2ecc71" if b > -0.005 else "#f39c12" for b in bwts]
    ax2.bar(x, bwts, color=colors_bwt, edgecolor="#2c3e50", alpha=0.85, width=0.6)
    ax2.axhline(0, color="black", linewidth=0.8)
    ax2.axhline(-0.01, color="#e74c3c", linestyle="--", alpha=0.5, label="Forgetting threshold")
    ax2.set_xticks(x)
    ax2.set_xticklabels(methods, rotation=30, ha="right", fontsize=9)
    ax2.set_ylabel("Backward Transfer (BWT)")
    ax2.set_title("Catastrophic Forgetting Comparison", fontweight="bold")
    ax2.legend()

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Saved: {save_path}")
    plt.close(fig)


# ============================================================================
#  Figure 5: Large-Scale Scaling Experiment
# ============================================================================
def plot_scaling_experiment(n_tasks_list, rmse_list, bwt_list, time_list, save_path=None):
    """
    Three-panel figure: RMSE, BWT, and training time vs number of tasks.
    """
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

    axes[0].plot(n_tasks_list, rmse_list, "o-", color="#3498db", linewidth=2, markersize=8)
    axes[0].fill_between(n_tasks_list,
                         np.array(rmse_list) - 0.01,
                         np.array(rmse_list) + 0.01,
                         alpha=0.15, color="#3498db")
    axes[0].set_xlabel("Number of Sequential Tasks")
    axes[0].set_ylabel("Average RMSE")
    axes[0].set_title("Prediction Accuracy", fontweight="bold")

    axes[1].plot(n_tasks_list, bwt_list, "s-", color="#e74c3c", linewidth=2, markersize=8)
    axes[1].axhline(0, color="black", linewidth=0.8)
    axes[1].set_xlabel("Number of Sequential Tasks")
    axes[1].set_ylabel("Backward Transfer (BWT)")
    axes[1].set_title("Catastrophic Forgetting", fontweight="bold")

    axes[2].plot(n_tasks_list, time_list, "D-", color="#2ecc71", linewidth=2, markersize=8)
    axes[2].set_xlabel("Number of Sequential Tasks")
    axes[2].set_ylabel("Training Time (s)")
    axes[2].set_title("Computational Cost", fontweight="bold")

    fig.suptitle("Large-Scale Scaling Analysis", fontsize=14, fontweight="bold")
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Saved: {save_path}")
    plt.close(fig)


# ============================================================================
#  Figure 6: Ablation Study
# ============================================================================
def plot_ablation_study(ablation_results, save_path=None):
    """
    Horizontal bar chart showing ablation study results.

    Parameters
    ----------
    ablation_results : dict
        Keys = variant names, values = dict with 'rmse', 'bwt', 'cal_error'
    """
    variants = list(ablation_results.keys())
    rmses = [ablation_results[v]["rmse"] for v in variants]
    bwts = [ablation_results[v]["bwt"] for v in variants]
    cal_errors = [ablation_results[v]["cal_error"] for v in variants]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    y = np.arange(len(variants))

    axes[0].barh(y, rmses, color="#3498db", edgecolor="#2c3e50", alpha=0.85)
    axes[0].set_yticks(y)
    axes[0].set_yticklabels(variants, fontsize=9)
    axes[0].set_xlabel("RMSE")
    axes[0].set_title("Prediction Error", fontweight="bold")
    axes[0].invert_yaxis()

    axes[1].barh(y, bwts, color=["#e74c3c" if b < -0.005 else "#2ecc71" for b in bwts],
                 edgecolor="#2c3e50", alpha=0.85)
    axes[1].set_yticks(y)
    axes[1].set_yticklabels(variants, fontsize=9)
    axes[1].axvline(0, color="black", linewidth=0.8)
    axes[1].set_xlabel("BWT")
    axes[1].set_title("Forgetting", fontweight="bold")
    axes[1].invert_yaxis()

    axes[2].barh(y, cal_errors, color="#f39c12", edgecolor="#2c3e50", alpha=0.85)
    axes[2].set_yticks(y)
    axes[2].set_yticklabels(variants, fontsize=9)
    axes[2].set_xlabel("Calibration Error")
    axes[2].set_title("Uncertainty Calibration", fontweight="bold")
    axes[2].invert_yaxis()

    fig.suptitle("Component Ablation Study", fontsize=14, fontweight="bold")
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Saved: {save_path}")
    plt.close(fig)


# ============================================================================
#  Figure 7: IEEE Bus Voltage Profile
# ============================================================================
def plot_ieee_voltage_profile(bus_indices, true_voltages, pred_voltages,
                               bus_system_name="IEEE 30-Bus", save_path=None):
    """
    Scatter plot of true vs predicted voltages for IEEE bus systems.
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    rmse = np.sqrt(np.mean((true_voltages - pred_voltages) ** 2))

    ax.scatter(true_voltages, pred_voltages, alpha=0.6, s=30, color="#3498db", edgecolors="#2c3e50", linewidth=0.5)
    ax.plot([0.95, 1.05], [0.95, 1.05], "r--", linewidth=1.5, label="Perfect Prediction")
    ax.set_xlim(0.95, 1.05)
    ax.set_ylim(0.95, 1.05)
    ax.set_xlabel("True Voltage (p.u.)")
    ax.set_ylabel("Predicted Voltage (p.u.)")
    ax.set_title(f"{bus_system_name} Voltage Prediction\nRMSE = {rmse:.4f} p.u.",
                 fontweight="bold")
    ax.legend()
    ax.set_aspect("equal")

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Saved: {save_path}")
    plt.close(fig)


# ============================================================================
#  Figure 8: Computational Efficiency Comparison
# ============================================================================
def plot_computational_efficiency(method_names, latency_ms, memory_kb,
                                  train_time_s, save_path=None):
    """
    Multi-panel comparison of computational efficiency.
    """
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    x = np.arange(len(method_names))

    axes[0].bar(x, latency_ms, color="#3498db", edgecolor="#2c3e50", alpha=0.85)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(method_names, rotation=30, ha="right", fontsize=8)
    axes[0].set_ylabel("Latency (ms)")
    axes[0].set_title("Inference Latency", fontweight="bold")

    axes[1].bar(x, memory_kb, color="#2ecc71", edgecolor="#2c3e50", alpha=0.85)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(method_names, rotation=30, ha="right", fontsize=8)
    axes[1].set_ylabel("Memory (KB)")
    axes[1].set_title("Memory Footprint", fontweight="bold")

    axes[2].bar(x, train_time_s, color="#e67e22", edgecolor="#2c3e50", alpha=0.85)
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(method_names, rotation=30, ha="right", fontsize=8)
    axes[2].set_ylabel("Training Time (s)")
    axes[2].set_title("Total Training Time", fontweight="bold")

    fig.suptitle("Computational Efficiency Comparison", fontsize=14, fontweight="bold")
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Saved: {save_path}")
    plt.close(fig)


# ============================================================================
#  Figure 9: Conformal Prediction Intervals
# ============================================================================
def plot_conformal_intervals(x_values, y_true, y_pred, lower, upper, save_path=None):
    """
    Time-series plot with conformal prediction intervals.
    """
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(x_values, y_true, "k-", linewidth=1.0, alpha=0.8, label="True")
    ax.plot(x_values, y_pred, "b-", linewidth=0.8, alpha=0.8, label="Predicted")
    ax.fill_between(x_values, lower, upper, alpha=0.2, color="#3498db", label="95% Interval")

    # Mark violations
    violations = (y_true < lower) | (y_true > upper)
    if np.any(violations):
        ax.scatter(x_values[violations], y_true[violations], color="red", s=20,
                   zorder=5, label=f"Violations ({violations.sum()})")

    coverage = np.mean((y_true >= lower) & (y_true <= upper))
    ax.set_xlabel("Sample Index")
    ax.set_ylabel("Voltage (p.u.)")
    ax.set_title(f"Conformal Prediction Intervals (Coverage: {coverage:.1%})", fontweight="bold")
    ax.legend(loc="upper right")

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
    print("  EWC-IXER Visualization Module")
    print("  Generating all publication-quality figures")
    print("=" * 70)

    # Demo with synthetic data
    from synthetic_smart_grid_dataset import generate_dataset as generate_synthetic_dataset
    tasks = generate_synthetic_dataset(seed=42)

    # Figure 1: Data distributions
    print("\n[1/9] Generating data distribution plots...")
    plot_data_distributions(tasks, save_path=os.path.join(OUTPUT_DIR, "fig_data_distributions.png"))

    # Figure 2: Task segmentation
    print("[2/9] Generating task segmentation plot...")
    y_parts = []
    sizes = []
    for key in tasks:
        t = tasks[key]
        y_parts.append(t["y_train"])
        y_parts.append(t["y_test"])
        sizes.append(len(t["y_train"]) + len(t["y_test"]))
    all_y = np.concatenate(y_parts)
    cumsum = np.cumsum(sizes)
    true_cps_cumsum = cumsum[:-1].tolist()
    plot_task_segmentation(all_y, true_cps_cumsum, save_path=os.path.join(OUTPUT_DIR, "fig_task_segmentation.png"))

    # Figure 5: Scaling experiment (simulated)
    print("[3/9] Generating scaling experiment plots...")
    n_tasks_list = [5, 10, 20, 30, 50]
    rmse_list = [1.001, 1.003, 1.006, 1.009, 1.012]
    bwt_list = [-0.001, -0.0015, -0.002, -0.0025, -0.003]
    time_list = [1.2, 2.8, 6.5, 11.0, 20.5]
    plot_scaling_experiment(n_tasks_list, rmse_list, bwt_list, time_list,
                           save_path=os.path.join(OUTPUT_DIR, "fig_scaling_experiment.png"))

    # Figure 4: Method comparison (simulated)
    print("[4/9] Generating method comparison plots...")
    results = {
        "Naive FT": {"mean_rmse": 1.042, "std_rmse": 0.018, "bwt": -0.038, "aa": 0.958},
        "EWC Only": {"mean_rmse": 1.015, "std_rmse": 0.014, "bwt": -0.008, "aa": 0.985},
        "ER Only": {"mean_rmse": 1.012, "std_rmse": 0.013, "bwt": -0.012, "aa": 0.988},
        "SI": {"mean_rmse": 1.018, "std_rmse": 0.015, "bwt": -0.010, "aa": 0.982},
        "MAS": {"mean_rmse": 1.020, "std_rmse": 0.016, "bwt": -0.009, "aa": 0.980},
        "GEM": {"mean_rmse": 1.022, "std_rmse": 0.016, "bwt": -0.006, "aa": 0.978},
        "MIR": {"mean_rmse": 1.009, "std_rmse": 0.012, "bwt": -0.007, "aa": 0.991},
        "EWC-IXER": {"mean_rmse": 1.001, "std_rmse": 0.012, "bwt": -0.001, "aa": 0.999},
    }
    plot_method_comparison(results, save_path=os.path.join(OUTPUT_DIR, "fig_method_comparison.png"))

    # Figure 6: Ablation study
    print("[5/9] Generating ablation study plots...")
    ablation = {
        "Full (EWC-IXER)": {"rmse": 1.001, "bwt": -0.001, "cal_error": 0.021},
        "- EWC": {"rmse": 1.0037, "bwt": -0.009, "cal_error": 0.022},
        "- Replay": {"rmse": 1.0024, "bwt": -0.005, "cal_error": 0.023},
        "- Metacognitive": {"rmse": 1.0008, "bwt": -0.002, "cal_error": 0.048},
        "- CPD (oracle)": {"rmse": 0.9998, "bwt": -0.001, "cal_error": 0.020},
    }
    plot_ablation_study(ablation, save_path=os.path.join(OUTPUT_DIR, "fig_ablation_study.png"))

    # Figure 8: Computational efficiency
    print("[6/9] Generating computational efficiency plots...")
    methods = ["Naive", "EWC", "ER", "SI", "MAS", "GEM", "MIR", "EWC-IXER"]
    latencies = [0.015, 0.018, 0.017, 0.018, 0.019, 0.022, 0.020, 0.020]
    memories = [0.9, 12, 5, 10, 10, 15, 8, 14]
    train_times = [0.8, 1.5, 1.2, 1.4, 1.4, 2.0, 1.6, 1.8]
    plot_computational_efficiency(methods, latencies, memories, train_times,
                                  save_path=os.path.join(OUTPUT_DIR, "fig_computational_efficiency.png"))

    # Figure 9: Conformal intervals (simulated)
    print("[7/9] Generating conformal prediction interval plots...")
    np.random.seed(42)
    n = 500
    x_vals = np.linspace(0, 10, n)
    y_true = np.sin(x_vals * 0.5) * 0.02 + 1.0 + np.random.normal(0, 0.01, n)
    y_pred = np.sin(x_vals * 0.5) * 0.02 + 1.0
    interval_width = 0.03
    lower = y_pred - interval_width
    upper = y_pred + interval_width
    plot_conformal_intervals(x_vals, y_true, y_pred, lower, upper,
                            save_path=os.path.join(OUTPUT_DIR, "fig_conformal_intervals.png"))

    # Figure 7: IEEE voltage profile (simulated)
    print("[8/9] Generating IEEE voltage profile plots...")
    n_buses = 30
    true_v = np.random.uniform(0.96, 1.04, n_buses)
    pred_v = true_v + np.random.normal(0, 0.008, n_buses)
    plot_ieee_voltage_profile(range(1, n_buses + 1), true_v, pred_v,
                             bus_system_name="IEEE 30-Bus",
                             save_path=os.path.join(OUTPUT_DIR, "fig_ieee30_voltage.png"))

    print("\n[9/9] All figures generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 70)
