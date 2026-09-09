#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bayesian Change Point Detection Module for EWC-IXER Paper
===========================================================

Implements two complementary change point detection strategies:

1. **Sliding-Window F/T-Test Detector** — Combines an F-test (sensitive to
   variance shifts) and a T-test (sensitive to mean shifts) into a single
   combined score, scanned across the data stream via a sliding window.

2. **Bayesian Online Changepoint Detection (BOCPD)** — The Adams-MacKay
   [Adams & MacKay, 2007] algorithm that maintains a run-length posterior
   using Gaussian conjugate priors and computes the marginal probability of
   a changepoint at every time step in an online, incremental fashion.

Both detectors are evaluated on synthetic non-stationary time series with
known ground-truth change points, and segmentation quality is reported via
precision / recall / F1 metrics.

References
----------
Adams, R. P. & MacKay, D. J. C. (2007). "Bayesian Online Changepoint
Detection." *arXiv:0710.3742*.
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import gammaln
from typing import List, Tuple, Optional

# ============================================================================
# 1. Sliding-Window F/T-Test Change Point Detector
# ============================================================================

def compute_cp_score(
    data: np.ndarray,
    t: int,
    W: int = 50,
) -> float:
    """
    Compute the combined F-test / T-test change point score at position *t*.

    Two adjacent windows are compared:
        Left  window:  data[t-W : t]
        Right window:  data[t   : t+W]

    The combined score is defined as:

        CP_score(t) = omega * p_F(t) + (1 - omega) * p_T(t)

    where
        - p_F(t) is the p-value of a two-tailed F-test for equal variances
          (sensitive to variance shifts);
        - p_T(t) is the p-value of a two-sample T-test for equal means
          (sensitive to mean shifts);
        - omega balances the two components (default 0.5).

    Parameters
    ----------
    data : np.ndarray, shape (N,)
        Univariate time series.
    t : int
        Candidate change point index (boundary between the two windows).
    W : int, optional (default=50)
        Half-window size. Each window contains *W* samples.

    Returns
    -------
    float
        Combined score in [0, 1]. Higher values indicate greater evidence
        of a change point. A value above *threshold* (e.g. 0.95) declares
        a change point.
    """
    omega = 0.5  # Equal weighting of F-test and T-test contributions

    # Guard against out-of-range indices
    if t - W < 0 or t + W > len(data):
        return 0.0

    left_win = data[t - W : t]
    right_win = data[t : t + W]

    # Both windows must have enough samples for the tests
    if len(left_win) < 2 or len(right_win) < 2:
        return 0.0

    # --- F-test for equality of variances ---
    # scipy.stats.f requires F = var(left) / var(right); the larger variance
    # is placed in the numerator to yield a right-tailed p-value, which we
    # double for a two-tailed test.
    var_left = np.var(left_win, ddof=1)
    var_right = np.var(right_win, ddof=1)

    if var_left == 0.0 and var_right == 0.0:
        sig_F = 0.0  # No evidence of a variance change
    elif var_left == 0.0 or var_right == 0.0:
        # One window has zero variance while the other does not — strong
        # evidence of a variance change.
        sig_F = 1.0
    else:
        if var_left >= var_right:
            F_stat = var_left / var_right
            dfn = len(left_win) - 1
            dfd = len(right_win) - 1
        else:
            F_stat = var_right / var_left
            dfn = len(right_win) - 1
            dfd = len(left_win) - 1
        # Two-tailed p-value
        p_F = 2.0 * min(stats.f.sf(F_stat, dfn, dfd), 1.0 - stats.f.sf(F_stat, dfn, dfd))
        p_F = np.clip(p_F, 0.0, 1.0)
        # Convert to significance measure: high = strong evidence of change
        sig_F = 1.0 - p_F

    # --- T-test for equality of means ---
    # Welch's T-test (equal_var=False) for robustness when variances differ.
    _, p_T = stats.ttest_ind(left_win, right_win, equal_var=False)
    p_T = float(np.clip(p_T, 0.0, 1.0))
    # Convert to significance measure
    sig_T = 1.0 - p_T

    # Combined score: higher values = stronger evidence of a change point
    # Exceeds threshold (e.g. 0.95) to declare a change point.
    cp_score = omega * sig_F + (1.0 - omega) * sig_T
    return float(cp_score)


def detect_change_points(
    data: np.ndarray,
    W: int = 50,
    threshold: float = 0.05,
    omega: float = 0.5,
    min_distance: int = 50,
) -> List[int]:
    """
    Scan the full data stream with a sliding window and detect change points
    where the combined F/T-test score exceeds *threshold*.

    The scan ranges over valid positions t where both windows fit within the
    data, i.e.  W <= t <= N - W.

    Non-maximum suppression with *min_distance* ensures detected change
    points are sufficiently separated.

    Parameters
    ----------
    data : np.ndarray, shape (N,)
        Univariate time series.
    W : int, optional (default=50)
        Half-window size.
    threshold : float, optional (default=0.05)
        Significance threshold. A change point is declared when
        CP_score(t) > threshold.  Note: the score is a *significance*
        measure (1 − p-value), so a high threshold (e.g. 0.95) corresponds
        to the conventional p < 0.05 criterion.
    omega : float, optional (default=0.5)
        Weight for the F-test component. Not used directly here (omega is
        fixed inside ``compute_cp_score``) but kept for API consistency.
    min_distance : int, optional (default=50)
        Minimum distance (in samples) between consecutive detected change
        points. When two candidates fall within this distance, the one with
        the higher score is retained.

    Returns
    -------
    List[int]
        Sorted list of detected change point indices.
    """
    N = len(data)
    candidates = []

    for t in range(W, N - W):
        score = compute_cp_score(data, t, W)
        if score > threshold:
            candidates.append((t, score))

    if not candidates:
        return []

    # Sort candidates by score (descending) for greedy non-maximum suppression
    candidates.sort(key=lambda x: x[1], reverse=True)

    # Greedy NMS: keep the highest-scoring candidate, then discard all
    # candidates within min_distance, and repeat.
    selected = []
    for t, s in candidates:
        if all(abs(t - sel) >= min_distance for sel in selected):
            selected.append(t)

    selected.sort()
    return selected


def segment_data(
    data: np.ndarray,
    change_points: List[int],
) -> List[np.ndarray]:
    """
    Split *data* into contiguous task segments based on detected change
    points.

    Each change point marks the **start** of a new segment (i.e. the
    boundary at which the data distribution shifts). The segment boundaries
    are therefore::

        [0, cp_0), [cp_0, cp_1), ..., [cp_K, N)

    Parameters
    ----------
    data : np.ndarray, shape (N,)
        Univariate time series.
    change_points : List[int]
        Sorted list of change point indices.

    Returns
    -------
    List[np.ndarray]
        List of data segments.
    """
    if not change_points:
        return [data]

    boundaries = [0] + list(change_points) + [len(data)]
    segments = []
    for i in range(len(boundaries) - 1):
        seg = data[boundaries[i] : boundaries[i + 1]]
        segments.append(seg)
    return segments


def evaluate_segmentation(
    detected_cps: List[int],
    true_cps: List[int],
    tolerance: int = 30,
) -> dict:
    """
    Compute precision, recall, and F1 score for boundary detection.

    A detected change point is a **true positive** if it falls within
    ±tolerance of a true change point. Each true change point can match at
    most one detected point (greedy, nearest-first matching).

    Parameters
    ----------
    detected_cps : List[int]
        Detected change point indices.
    true_cps : List[int]
        Ground-truth change point indices.
    tolerance : int, optional (default=30)
        Maximum allowed deviation (in samples) for a match.

    Returns
    -------
    dict
        Dictionary with keys 'precision', 'recall', 'f1', each a float.
    """
    if len(detected_cps) == 0 and len(true_cps) == 0:
        return {"precision": 1.0, "recall": 1.0, "f1": 1.0}
    if len(detected_cps) == 0:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    if len(true_cps) == 0:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    # Sort copies
    det = sorted(detected_cps)
    tru = sorted(true_cps)

    tp = 0
    matched_true = set()

    # Greedy matching: for each true CP, find the nearest detected CP within
    # tolerance that hasn't been matched yet.
    for tc in tru:
        best_idx = None
        best_dist = float("inf")
        for i, dc in enumerate(det):
            if i in matched_true:
                continue
            dist = abs(dc - tc)
            if dist <= tolerance and dist < best_dist:
                best_dist = dist
                best_idx = i
        if best_idx is not None:
            tp += 1
            matched_true.add(best_idx)

    precision = tp / len(det)
    recall = tp / len(tru)
    f1 = 2.0 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


# ============================================================================
# 2. Bayesian Online Changepoint Detection (Adams-MacKay BOCPD)
# ============================================================================

class GaussianLikelihood:
    """
    Gaussian conjugate-prior model for the BOCPD algorithm.

    The prior on the data-generating distribution within a run is:
        mu | tau  ~  Normal(mu0, 1 / (kappa0 * tau))
        tau        ~  Gamma(alpha0, beta0)

    As data arrive the posterior parameters (mu, kappa, alpha, beta) are
    updated in closed form.  The Student-t predictive distribution is used
    to evaluate the log marginal probability of each new observation.

    All internal computations use log-space to avoid floating-point
    underflow with long run-length posteriors.
    """

    def __init__(
        self,
        mu0: float = 0.0,
        kappa0: float = 1.0,
        alpha0: float = 1.0,
        beta0: float = 1.0,
    ):
        self.mu0 = mu0
        self.kappa0 = kappa0
        self.alpha0 = alpha0
        self.beta0 = beta0

    @staticmethod
    def _log_pdf_student_t(
        x: np.ndarray,
        mu: np.ndarray,
        kappa: np.ndarray,
        alpha: np.ndarray,
        beta: np.ndarray,
    ) -> np.ndarray:
        """
        Vectorised log-pdf of the Student-t predictive distribution.

        The predictive distribution for each run-length hypothesis has:
            df    = 2 * alpha
            loc   = mu
            scale = sqrt(beta * (kappa + 1) / (alpha * kappa))

        Parameters
        ----------
        x : scalar or array broadcastable to *mu*
            Observed data point(s).
        mu, kappa, alpha, beta : np.ndarray of same shape
            Posterior parameters for each run-length hypothesis.

        Returns
        -------
        np.ndarray
            Log-predictive probabilities, same shape as *mu*.
        """
        df = 2.0 * alpha
        scale = np.sqrt(beta * (kappa + 1.0) / (alpha * kappa))
        # Student-t log-pdf:  log Gamma((df+1)/2) - log Gamma(df/2)
        #                    - 0.5*log(df*pi) - log(scale) - (df+1)/2 * log(1 + ((x-mu)/scale)^2)
        z = (x - mu) / scale
        log_pdf = (
            gammaln((df + 1.0) / 2.0)
            - gammaln(df / 2.0)
            - 0.5 * np.log(df * np.pi)
            - np.log(scale)
            - (df + 1.0) / 2.0 * np.log(1.0 + z ** 2)
        )
        return log_pdf


def bocpd(
    data: np.ndarray,
    hazard_lambda: float = 100.0,
    mu0: float = 0.0,
    kappa0: float = 1.0,
    alpha0: float = 1.0,
    beta0: float = 0.001,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Bayesian Online Changepoint Detection (Adams & MacKay, 2007).

    Maintains a run-length posterior distribution  R[t, :]  where
    R[t, r] = P(run length at time t = r | data_{1:t}).

    Implementation notes:
        - All internal arithmetic is performed in **log-space** to prevent
          floating-point underflow for long data sequences.
        - Predictive probabilities are computed via a vectorised Student-t
          log-pdf over all active run lengths simultaneously.
        - The marginal changepoint probability at time *t* is the
          posterior mass on run length 0: cp_prob[t] = R[t, 0].

    Parameters
    ----------
    data : np.ndarray, shape (N,)
        Univariate time series (processed one sample at a time).
    hazard_lambda : float, optional (default=100)
        Expected run length (prior on changepoint frequency).  The constant
        hazard function is  H(r) = 1 / hazard_lambda.
    mu0, kappa0, alpha0, beta0 : float
        Hyper-parameters of the Gaussian-Normal-Gamma conjugate prior.

    Returns
    -------
    R : np.ndarray, shape (N, N)
        Full run-length posterior matrix.  R[t, r] gives the posterior
        probability that the run length is *r* at time *t*.
    cp_prob : np.ndarray, shape (N,)
        Marginal probability of a changepoint at each time step,
        i.e. cp_prob[t] = R[t, 0].
    """
    N = len(data)
    max_run = N

    # Allocate output arrays
    R = np.zeros((N, max_run))
    cp_prob = np.zeros(N)

    # ---- Log-space run-length posterior ----
    # pi_log[r] = log P(r_t = r | data_{1:t})
    pi_log = np.full(max_run, -np.inf)
    pi_log[0] = 0.0  # log(1) — initial run length is 0 with certainty

    # ---- Posterior sufficient statistics per run-length hypothesis ----
    mu_post    = np.full(max_run, mu0)
    kappa_post = np.full(max_run, kappa0)
    alpha_post = np.full(max_run, alpha0)
    beta_post  = np.full(max_run, beta0)

    # Constant hazard: log H = log(1 / lambda)
    log_hazard = np.log(1.0 / hazard_lambda)
    log_one_minus_hazard = np.log(1.0 - 1.0 / hazard_lambda)

    # Initialisation: t = 0
    R[0, 0] = 1.0
    cp_prob[0] = 1.0

    for t in range(1, N):
        x = float(data[t])
        n_active = t  # number of active run-length hypotheses (0..t-1)

        # -- Step 1: Vectorised log-predictive probabilities --
        log_pred = GaussianLikelihood._log_pdf_student_t(
            x,
            mu_post[:n_active],
            kappa_post[:n_active],
            alpha_post[:n_active],
            beta_post[:n_active],
        )

        # -- Step 2: Growth and changepoint probabilities (log-space) --
        # Growth:  log P(r_t = r+1, x_t) = log(1-H) + pi_log[r] + log_pred[r]
        log_growth = log_one_minus_hazard + pi_log[:n_active] + log_pred

        # Changepoint: log P(r_t = 0, x_t) = logsumexp_r[log(H) + pi_log[r] + log_pred[r]]
        log_cp_messages = log_hazard + pi_log[:n_active] + log_pred
        log_cp_raw = _logsumexp(log_cp_messages)

        # -- Step 3: Assemble and normalise --
        new_pi_log = np.full(max_run, -np.inf)
        new_pi_log[0] = log_cp_raw
        new_pi_log[1 : n_active + 1] = log_growth

        # Log-sum-exp normalisation
        log_norm = _logsumexp(new_pi_log[: n_active + 1])
        new_pi_log[: n_active + 1] -= log_norm

        # Store in linear-space output
        pi_probs = np.exp(new_pi_log[: n_active + 1])
        R[t, : n_active + 1] = pi_probs
        cp_prob[t] = R[t, 0]

        # -- Step 4: Update sufficient statistics --
        # Reset run length 0 to the prior
        mu_post[0] = mu0
        kappa_post[0] = kappa0
        alpha_post[0] = alpha0
        beta_post[0] = beta0

        # For continuing runs (r → r+1), update with the new observation.
        # We must use the PRE-update values of run length r to compute the
        # POST-update values of run length r+1.  Hence we copy the slices
        # before the in-place write.
        mu_old    = mu_post[:n_active].copy()
        k_old     = kappa_post[:n_active].copy()
        a_old     = alpha_post[:n_active].copy()
        b_old     = beta_post[:n_active].copy()

        mu_post[1 : n_active + 1]    = (k_old * mu_old + x) / (k_old + 1.0)
        kappa_post[1 : n_active + 1] = k_old + 1.0
        alpha_post[1 : n_active + 1] = a_old + 0.5
        beta_post[1 : n_active + 1]  = b_old + 0.5 * k_old * (x - mu_old) ** 2 / (k_old + 1.0)

        # Update the active posterior
        pi_log = new_pi_log

    return R, cp_prob


def _logsumexp(a: np.ndarray) -> float:
    """Numerically stable log-sum-exp."""
    a_max = np.max(a)
    if not np.isfinite(a_max):
        return -np.inf
    return float(a_max + np.log(np.sum(np.exp(a - a_max))))


def detect_change_points_bocpd(
    cp_prob: np.ndarray,
    R: Optional[np.ndarray] = None,
    threshold: float = 0.1,
    min_distance: int = 30,
    method: str = "map",
) -> List[int]:
    """
    Extract discrete change point indices from BOCPD output.

    Two detection strategies are supported:

    **"map"** (default):
        Uses the MAP (maximum a posteriori) run length estimate.
        A change point is declared at time *t* when the MAP run length
        drops below *threshold* (interpreted as a run-length cutoff) AND
        the MAP run length at *t-1* was above that cutoff.  This detects
        "resets" in the run-length posterior.

    **"marginal"**:
        Uses the marginal changepoint probability cp_prob[t] = R[t, 0].
        A change point is declared when this probability exceeds
        *threshold*.

    In both cases, non-maximum suppression with *min_distance* removes
    redundant detections.

    Parameters
    ----------
    cp_prob : np.ndarray, shape (N,)
        Marginal probability of a changepoint at each time step (from
        ``bocpd()``).
    R : np.ndarray, shape (N, N) or None
        Full run-length posterior matrix (needed for ``method='map'``).
    threshold : float, optional (default=0.1)
        Detection threshold — run-length cutoff (MAP method) or
        probability threshold (marginal method).
    min_distance : int, optional (default=30)
        Minimum separation between consecutive change points.
    method : str, optional (default='map')
        Detection strategy: ``'map'`` or ``'margial'``.

    Returns
    -------
    List[int]
        Sorted list of detected change point indices.
    """
    N = len(cp_prob)
    candidates = []

    if method == "map" and R is not None:
        # MAP run-length detection: look for drops in the MAP estimate
        map_rl = np.argmax(R, axis=1).astype(int)
        rl_threshold = max(int(threshold), 1)  # ensure at least 1
        for t in range(1, N):
            # A changepoint is signalled when the MAP run length resets
            # to a small value after having been large.
            if map_rl[t] <= rl_threshold and map_rl[t - 1] > rl_threshold:
                # Score = drop magnitude (higher = more confident)
                score = float(map_rl[t - 1] - map_rl[t])
                candidates.append((t, score))
    else:
        # Marginal probability detection
        for t in range(1, N):
            if cp_prob[t] > threshold:
                candidates.append((t, cp_prob[t]))

    if not candidates:
        return []

    # Non-maximum suppression (greedy, highest score first)
    candidates.sort(key=lambda x: x[1], reverse=True)
    selected = []
    for t, s in candidates:
        if all(abs(t - sel) >= min_distance for sel in selected):
            selected.append(t)

    selected.sort()
    return selected


# ============================================================================
# 3. Synthetic Data Generation
# ============================================================================

def generate_synthetic_data(
    N: int = 1000,
    true_change_points: Optional[List[int]] = None,
    seed: int = 42,
) -> Tuple[np.ndarray, List[int]]:
    """
    Generate a synthetic non-stationary time series with known change points.

    Each segment between consecutive change points has a different mean
    and/or variance, simulating distribution shifts encountered in
    continual learning scenarios.

    Parameters
    ----------
    N : int, optional (default=1000)
        Total length of the time series.
    true_change_points : List[int] or None
        Ground-truth change point positions. If None, 4 equally spaced
        change points are used.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    data : np.ndarray, shape (N,)
        Synthetic time series.
    true_change_points : List[int]
        Ground-truth change point positions.
    """
    rng = np.random.RandomState(seed)

    if true_change_points is None:
        # Default: 4 change points at roughly 200, 400, 600, 800
        true_change_points = [200, 400, 600, 800]

    # Define segment parameters: (mean, std) for each segment
    # 5 segments for 4 change points
    segment_params = [
        (0.0, 1.0),    # Segment 0: mean=0, std=1
        (3.0, 1.0),    # Segment 1: mean=3, std=1  (mean shift)
        (3.0, 3.0),    # Segment 2: mean=3, std=3  (variance shift)
        (-2.0, 2.0),   # Segment 3: mean=-2, std=2 (mean + variance shift)
        (1.0, 0.5),    # Segment 4: mean=1, std=0.5 (mean + variance shift)
    ]

    data = np.zeros(N)
    boundaries = [0] + true_change_points + [N]

    for i in range(len(boundaries) - 1):
        start = boundaries[i]
        end = boundaries[i + 1]
        mu, sigma = segment_params[i]
        data[start:end] = rng.normal(loc=mu, scale=sigma, size=end - start)

    return data, true_change_points


# ============================================================================
# 4. Plotting Utilities
# ============================================================================

def plot_results(
    data: np.ndarray,
    true_cps: List[int],
    ft_cps: List[int],
    cp_scores: np.ndarray,
    bocpd_probs: np.ndarray,
    bocpd_cps: List[int],
    bocpd_R: Optional[np.ndarray] = None,
    W: int = 50,
) -> plt.Figure:
    """
    Create a 3-panel figure comparing both detectors.

    Panel 1 — Raw data with true and detected change points.
    Panel 2 — F/T-test combined score with threshold line.
    Panel 3 — BOCPD marginal changepoint probability.

    Parameters
    ----------
    data : np.ndarray
        Time series data.
    true_cps : List[int]
        Ground-truth change point indices.
    ft_cps : List[int]
        Change points detected by the F/T-test method.
    cp_scores : np.ndarray
        Combined F/T-test scores at each valid position.
    bocpd_probs : np.ndarray
        BOCPD marginal changepoint probabilities.
    bocpd_cps : List[int]
        Change points detected by BOCPD.
    W : int
        Window half-size (used for x-axis offset of scores).

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
    fig.suptitle(
        "Change Point Detection — EWC-IXER Paper Module\n"
        "Sliding-Window F/T-Test vs Bayesian Online (Adams-MacKay)",
        fontsize=13,
        fontweight="bold",
    )

    time = np.arange(len(data))

    # --- Panel 1: Raw data ---
    ax = axes[0]
    ax.plot(time, data, linewidth=0.6, color="steelblue", alpha=0.85, label="Data")
    for cp in true_cps:
        ax.axvline(cp, color="red", linestyle="--", linewidth=1.2, alpha=0.8, label="True CP" if cp == true_cps[0] else None)
    for cp in ft_cps:
        ax.axvline(cp, color="green", linestyle="-", linewidth=1.5, alpha=0.7, label="F/T Detect" if cp == ft_cps[0] else None)
    for cp in bocpd_cps:
        ax.axvline(cp, color="orange", linestyle=":", linewidth=2.0, alpha=0.8, label="BOCPD Detect" if cp == bocpd_cps[0] else None)
    ax.set_ylabel("Value")
    ax.set_title("Time Series with Detected Change Points")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)

    # --- Panel 2: F/T-test combined score ---
    ax = axes[1]
    score_times = np.arange(W, len(data) - W)
    ax.plot(score_times, cp_scores[W:N-W], linewidth=0.8, color="purple", alpha=0.8)
    ax.axhline(0.95, color="black", linestyle="--", linewidth=1.0, alpha=0.6, label="Threshold = 0.95")
    for cp in true_cps:
        ax.axvline(cp, color="red", linestyle="--", linewidth=1.0, alpha=0.5)
    for cp in ft_cps:
        ax.axvline(cp, color="green", linestyle="-", linewidth=1.2, alpha=0.6)
    ax.set_ylabel("CP Score")
    ax.set_title("Sliding-Window F/T-Test Combined Score  [ω·p_F + (1−ω)·p_T]")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)

    # --- Panel 3: BOCPD MAP run length ---
    ax = axes[2]
    map_rl = np.argmax(bocpd_R, axis=1) if bocpd_R is not None else np.zeros(len(data))
    ax.fill_between(time, 0, map_rl, color="darkorange", alpha=0.4)
    ax.plot(time, map_rl, linewidth=0.8, color="darkorange", alpha=0.9, label="MAP run length")
    if bocpd_R is not None:
        ax.plot(time, bocpd_probs, linewidth=0.6, color="gray", alpha=0.6, label="P(CP | data)")
    for cp in true_cps:
        ax.axvline(cp, color="red", linestyle="--", linewidth=1.0, alpha=0.5)
    for cp in bocpd_cps:
        ax.axvline(cp, color="orange", linestyle=":", linewidth=1.5, alpha=0.7)
    ax.set_ylabel("Run Length")
    ax.set_xlabel("Time Step")
    ax.set_title("BOCPD MAP Run Length (Adams-MacKay) — drops indicate change points")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


# ============================================================================
# 5. Main Entry Point
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  Bayesian Change Point Detection — EWC-IXER Paper Module")
    print("=" * 70)

    # ------------------------------------------------------------------
    # (a) Generate synthetic non-stationary time series with 4 true CPs
    # ------------------------------------------------------------------
    print("\n[1] Generating synthetic data (N=1000, 4 true change points)...")
    true_cps = [200, 400, 600, 800]
    data, true_cps = generate_synthetic_data(N=1000, true_change_points=true_cps, seed=42)
    print(f"    Data shape: {data.shape}")
    print(f"    True change points: {true_cps}")

    segments = segment_data(data, true_cps)
    print(f"    Number of segments (ground truth): {len(segments)}")
    for i, seg in enumerate(segments):
        print(f"      Segment {i}: len={len(seg)}, mean={np.mean(seg):.3f}, std={np.std(seg):.3f}")

    # ------------------------------------------------------------------
    # (b) Run F/T-test detector
    # ------------------------------------------------------------------
    W = 50
    threshold_ft = 0.95
    print(f"\n[2] Running Sliding-Window F/T-Test Detector (W={W}, threshold={threshold_ft})...")

    # Compute full score profile for plotting
    N = len(data)
    cp_scores = np.zeros(N)
    for t in range(W, N - W):
        cp_scores[t] = compute_cp_score(data, t, W)

    ft_detected = detect_change_points(
        data, W=W, threshold=threshold_ft, omega=0.5, min_distance=50
    )
    print(f"    Detected change points: {ft_detected}")

    ft_eval = evaluate_segmentation(ft_detected, true_cps, tolerance=30)
    print(f"    Segmentation evaluation:")
    print(f"      Precision: {ft_eval['precision']:.4f}")
    print(f"      Recall:    {ft_eval['recall']:.4f}")
    print(f"      F1:        {ft_eval['f1']:.4f}")

    ft_segments = segment_data(data, ft_detected)
    print(f"    Number of detected segments: {len(ft_segments)}")

    # ------------------------------------------------------------------
    # (b) Run BOCPD
    # ------------------------------------------------------------------
    hazard_lambda = 250.0
    bocpd_alpha0 = 100.0
    bocpd_threshold = 50.0  # MAP run-length cutoff
    print(f"\n[3] Running BOCPD (Adams-MacKay, λ={hazard_lambda}, α0={bocpd_alpha0}, MAP threshold={bocpd_threshold})...")

    R, cp_prob = bocpd(
        data,
        hazard_lambda=hazard_lambda,
        mu0=float(np.mean(data[:W])),
        kappa0=1.0,
        alpha0=bocpd_alpha0,
        beta0=float(np.var(data[:W]) * 0.1),
    )

    bocpd_detected = detect_change_points_bocpd(
        cp_prob, R=R, threshold=bocpd_threshold, min_distance=50, method="map"
    )
    print(f"    Detected change points: {bocpd_detected}")

    bocpd_eval = evaluate_segmentation(bocpd_detected, true_cps, tolerance=30)
    print(f"    Segmentation evaluation:")
    print(f"      Precision: {bocpd_eval['precision']:.4f}")
    print(f"      Recall:    {bocpd_eval['recall']:.4f}")
    print(f"      F1:        {bocpd_eval['f1']:.4f}")

    bocpd_segments = segment_data(data, bocpd_detected)
    print(f"    Number of detected segments: {len(bocpd_segments)}")

    # ------------------------------------------------------------------
    # (c) Summary comparison
    # ------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("  SUMMARY COMPARISON")
    print("-" * 70)
    print(f"  {'Method':<35s} {'P':>6s} {'R':>6s} {'F1':>6s} {'#CPs':>5s}")
    print(f"  {'-'*35} {'-'*6} {'-'*6} {'-'*6} {'-'*5}")
    print(
        f"  {'Sliding-Window F/T-Test':<35s} "
        f"{ft_eval['precision']:6.4f} {ft_eval['recall']:6.4f} {ft_eval['f1']:6.4f} {len(ft_detected):5d}"
    )
    print(
        f"  {'BOCPD (Adams-MacKay)':<35s} "
        f"{bocpd_eval['precision']:6.4f} {bocpd_eval['recall']:6.4f} {bocpd_eval['f1']:6.4f} {len(bocpd_detected):5d}"
    )
    print(f"  {'True (ground truth)':<35s} {'---':>6s} {'---':>6s} {'---':>6s} {len(true_cps):5d}")
    print("-" * 70)

    # ------------------------------------------------------------------
    # (d) Plot results
    # ------------------------------------------------------------------
    print("\n[4] Generating plots...")
    fig = plot_results(
        data=data,
        true_cps=true_cps,
        ft_cps=ft_detected,
        cp_scores=cp_scores,
        bocpd_probs=cp_prob,
        bocpd_cps=bocpd_detected,
        bocpd_R=R,
        W=W,
    )

    # Save figure
    fig_path = "/home/z/my-project/download/change_point_detection_results.png"
    fig.savefig(fig_path, dpi=150, bbox_inches="tight")
    print(f"    Figure saved to: {fig_path}")

    plt.show()
    print("\nDone.")
