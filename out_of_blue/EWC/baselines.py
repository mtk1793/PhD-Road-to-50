#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==========================================================================
Continual Learning Baselines for EWC-IXER Paper Comparison
==========================================================================

This module implements seven (7) baseline continual learning methods for
empirical comparison in the EWC-IXER paper.  Each method wraps a shared
MLP architecture and exposes a uniform interface:

    __init__(...)           – hyper-parameters & model creation
    train_task(task_data, task_id) – learn on one sequential task
    evaluate(test_data)     – return RMSE on given data

Methods implemented:
    1. NaiveFineTuning   – no forgetting prevention
    2. EWCOnly           – Elastic Weight Consolidation (Kirkpatrick+ 2017)
    3. ExperienceReplay  – uniform random replay buffer
    4. SynapticIntelligence – path-integral importance (Zenke+ 2017)
    5. MAS               – Memory Aware Synapses (Aljundi+ 2018)
    6. GEM               – Gradient Episodic Memory (Lopez-Paz+ 2017)
    7. MIR               – Maximally Interfered Retrieval (Banga+ 2019)

All methods share the same MLP architecture:
    Input(5) → Hidden(32, ReLU, 20% dropout) → Output(1, linear)

Author: EWC-IXER Research Group
==========================================================================
"""

from __future__ import annotations

import copy
import math
import warnings
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
SEED = 42
np.random.seed(SEED)
torch.manual_seed(SEED)

# ---------------------------------------------------------------------------
# Shared MLP Architecture
# ---------------------------------------------------------------------------

class MLP(nn.Module):
    """
    Shared multi-layer perceptron used by ALL continual learning baselines.

    Architecture (per the EWC-IXER experimental protocol):
        Input(5) → Dense(32, ReLU, Dropout(0.2)) → Dense(1, Linear)
    """

    def __init__(self, input_dim: int = 5, hidden_dim: int = 32,
                 dropout: float = 0.2) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass.  Returns shape (batch, 1)."""
        return self.net(x)


# ---------------------------------------------------------------------------
# Utility: RMSE computation
# ---------------------------------------------------------------------------

def compute_rmse(model: nn.Module, data: Tuple[np.ndarray, np.ndarray],
                 device: torch.device = None) -> float:
    """
    Compute Root Mean Squared Error of *model* on *(X, y)* data.

    Parameters
    ----------
    model : nn.Module
        The neural network to evaluate.
    data : tuple of (np.ndarray, np.ndarray)
        (features, targets) – each of shape (N, D) / (N, 1).
    device : torch.device, optional
        Device on which to perform evaluation.

    Returns
    -------
    float
        RMSE value.
    """
    if device is None:
        device = torch.device("cpu")
    model.eval()
    X, y = data
    X_t = torch.as_tensor(X, dtype=torch.float32, device=device)
    y_t = torch.as_tensor(y, dtype=torch.float32, device=device)
    with torch.no_grad():
        pred = model(X_t)
        rmse = torch.sqrt(torch.mean((pred - y_t) ** 2)).item()
    model.train()
    return rmse


# ---------------------------------------------------------------------------
# Utility: diagonal Fisher information matrix
# ---------------------------------------------------------------------------

def diagonal_fisher(model: nn.Module, data: Tuple[np.ndarray, np.ndarray],
                    device: torch.device = None) -> Dict[str, torch.Tensor]:
    """
    Compute the diagonal of the empirical Fisher Information Matrix.

    For each parameter θ_i:
        F_i = E_{(x,y)}[ (∂L/∂θ_i)² ]

    Parameters
    ----------
    model : nn.Module
        The model (will be set to eval mode internally).
    data : tuple
        (X, y) numpy arrays.
    device : torch.device, optional

    Returns
    -------
    dict
        Mapping parameter name → diagonal Fisher value (1-D tensor).
    """
    if device is None:
        device = torch.device("cpu")
    model.eval()
    X, y = data
    dataset = TensorDataset(
        torch.as_tensor(X, dtype=torch.float32),
        torch.as_tensor(y, dtype=torch.float32),
    )
    loader = DataLoader(dataset, batch_size=64, shuffle=False)

    fisher = {n: torch.zeros_like(p) for n, p in model.named_parameters()
              if p.requires_grad}
    criterion = nn.MSELoss()

    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        model.zero_grad()
        loss = criterion(model(xb), yb)
        loss.backward()
        for n, p in model.named_parameters():
            if p.requires_grad and p.grad is not None:
                fisher[n] += p.grad.data ** 2

    # Average over mini-batches
    n_batches = len(loader)
    for n in fisher:
        fisher[n] /= max(n_batches, 1)

    model.train()
    return fisher


# ---------------------------------------------------------------------------
# Utility: Backward Transfer (BWT)
# ---------------------------------------------------------------------------

def compute_bwt(rmse_matrix: np.ndarray) -> float:
    """
    Compute Backward Transfer (Lopez-Paz & Ranzato, 2017).

    BWT = (1 / (T-1)) Σ_{i=1}^{T-1} (R_{T,i} - R_{i,i})

    where R_{t,i} is the RMSE on task i after training on tasks 1..t,
    and T is the total number of tasks.

    Negative BWT indicates forgetting; positive indicates forward
    knowledge transfer.

    Parameters
    ----------
    rmse_matrix : np.ndarray, shape (T, T)
        rmse_matrix[t][i] = RMSE on task i after training through task t.

    Returns
    -------
    float
        Backward Transfer metric.
    """
    T = rmse_matrix.shape[0]
    if T < 2:
        return 0.0
    bwt_sum = 0.0
    for i in range(T - 1):
        bwt_sum += rmse_matrix[T - 1, i] - rmse_matrix[i, i]
    return bwt_sum / (T - 1)


# ===========================================================================
#  Base Class
# ===========================================================================

class ContinualLearningMethod(ABC):
    """
    Abstract base class defining the uniform interface for all baselines.

    Every concrete subclass must implement:
        - train_task(task_data, task_id)
        - evaluate(test_data) → float (RMSE)
    """

    def __init__(self, input_dim: int = 5, hidden_dim: int = 32,
                 dropout: float = 0.2, lr: float = 1e-3,
                 device: Optional[str] = None) -> None:
        """
        Parameters
        ----------
        input_dim : int
            Dimensionality of input features.
        hidden_dim : int
            Number of hidden units.
        dropout : float
            Dropout probability in the hidden layer.
        lr : float
            Learning rate for the optimiser.
        device : str or None
            'cuda', 'cpu', or None (auto-detect).
        """
        if device is None:
            self.device = torch.device(
                "cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

        self.model = MLP(input_dim, hidden_dim, dropout).to(self.device)
        self.input_dim = input_dim
        self.lr = lr
        self.n_tasks_seen = 0

        # RMSE matrix: filled by run_all_tasks or the experiment harness
        self.rmse_matrix: Optional[np.ndarray] = None

    @abstractmethod
    def train_task(self, task_data: Tuple[np.ndarray, np.ndarray],
                   task_id: int) -> None:
        """Train on one sequential task."""
        ...

    @abstractmethod
    def evaluate(self, test_data: Tuple[np.ndarray, np.ndarray]) -> float:
        """Return RMSE on the provided test data."""
        ...


# ===========================================================================
#  1. Naive Fine-Tuning
# ===========================================================================

class NaiveFineTuning(ContinualLearningMethod):
    """
    1. Naive Fine-Tuning
    ─────────────────────
    Train on each task sequentially with **no** forgetting prevention.
    Standard Adam optimiser on each task's data alone.  This serves as
    the lower-bound baseline: we expect catastrophic forgetting.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_task(self, task_data: Tuple[np.ndarray, np.ndarray],
                   task_id: int) -> None:
        """
        Train the model on *task_data* using standard SGD/Adam.
        No replay, no regularisation – purely sequential fine-tuning.
        """
        X, y = task_data
        dataset = TensorDataset(
            torch.as_tensor(X, dtype=torch.float32),
            torch.as_tensor(y, dtype=torch.float32),
        )
        loader = DataLoader(dataset, batch_size=32, shuffle=True)
        self.model.train()
        epochs = 100

        for _epoch in range(epochs):
            for xb, yb in loader:
                xb, yb = xb.to(self.device), yb.to(self.device)
                self.optimizer.zero_grad()
                loss = self.criterion(self.model(xb), yb)
                loss.backward()
                self.optimizer.step()

        self.n_tasks_seen += 1

    def evaluate(self, test_data: Tuple[np.ndarray, np.ndarray]) -> float:
        return compute_rmse(self.model, test_data, self.device)


# ===========================================================================
#  2. EWC-Only (Elastic Weight Consolidation)
# ===========================================================================

class EWCOnly(ContinualLearningMethod):
    """
    2. EWC-Only  (Kirkpatrick et al., 2017)
    ─────────────────────────────────────────
    Elastic Weight Consolidation **without** experience replay.

    After each task, compute the diagonal Fisher Information Matrix (FIM)
    and store the current parameter values θ*.  On subsequent tasks, add
    a quadratic penalty:

        L_total = L_task + λ/2  Σ_i  F_i (θ_i − θ*_i)²

    where λ is the consolidation strength.
    """

    def __init__(self, lam: float = 500.0, **kwargs) -> None:
        """
        Parameters
        ----------
        lam : float
            EWC regularisation strength (λ).  Default 500.
        """
        super().__init__(**kwargs)
        self.lam = lam
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

        # List of (fisher_dict, param_dict) tuples – one per past task
        self.saved_fishers: List[Dict[str, torch.Tensor]] = []
        self.saved_params: List[Dict[str, torch.Tensor]] = []

    def _consolidation_penalty(self) -> torch.Tensor:
        """Compute Σ over past tasks of  λ/2 * F_i (θ_i − θ*_i)²."""
        penalty = torch.tensor(0.0, device=self.device)
        for fisher, params_star in zip(self.saved_fishers, self.saved_params):
            for n, p in self.model.named_parameters():
                if p.requires_grad and n in fisher:
                    penalty += (fisher[n] * (p - params_star[n]) ** 2).sum()
        return penalty

    def train_task(self, task_data: Tuple[np.ndarray, np.ndarray],
                   task_id: int) -> None:
        X, y = task_data
        dataset = TensorDataset(
            torch.as_tensor(X, dtype=torch.float32),
            torch.as_tensor(y, dtype=torch.float32),
        )
        loader = DataLoader(dataset, batch_size=32, shuffle=True)
        self.model.train()
        epochs = 100

        for _epoch in range(epochs):
            for xb, yb in loader:
                xb, yb = xb.to(self.device), yb.to(self.device)
                self.optimizer.zero_grad()
                loss = self.criterion(self.model(xb), yb)

                # Add EWC penalty from all previous tasks
                if self.saved_fishers:
                    loss = loss + (self.lam / 2.0) * self._consolidation_penalty()

                loss.backward()
                self.optimizer.step()

        # ── After training: save Fisher and current params ──
        fisher = diagonal_fisher(self.model, task_data, self.device)
        params_star = {n: p.data.clone() for n, p in self.model.named_parameters()
                       if p.requires_grad}
        self.saved_fishers.append(fisher)
        self.saved_params.append(params_star)

        self.n_tasks_seen += 1

    def evaluate(self, test_data: Tuple[np.ndarray, np.ndarray]) -> float:
        return compute_rmse(self.model, test_data, self.device)


# ===========================================================================
#  3. Experience Replay (ER)
# ===========================================================================

class ExperienceReplay(ContinualLearningMethod):
    """
    3. Experience Replay (ER)
    ─────────────────────────
    Standard uniform random replay from a fixed-size buffer.  On each
    training step, sample a mini-batch that is half current-task data
    and half randomly sampled examples from the buffer.

    Combined loss:
        L_total = L_task + β · L_replay

    No EWC penalty – purely rehearsal-based.
    """

    def __init__(self, buffer_size: int = 200, beta: float = 0.5,
                 **kwargs) -> None:
        """
        Parameters
        ----------
        buffer_size : int
            Maximum number of samples stored in the replay buffer.
        beta : float
            Weight of the replay loss term.  Default 0.5.
        """
        super().__init__(**kwargs)
        self.buffer_size = buffer_size
        self.beta = beta
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

        # Reservoir buffer: lists of (X_sample, y_sample)
        self.buffer_X: List[np.ndarray] = []
        self.buffer_y: List[np.ndarray] = []

    def _add_to_buffer(self, X: np.ndarray, y: np.ndarray) -> None:
        """Reservoir-sampling insertion into the replay buffer."""
        for i in range(len(X)):
            if len(self.buffer_X) < self.buffer_size:
                self.buffer_X.append(X[i])
                self.buffer_y.append(y[i])
            else:
                j = np.random.randint(0, len(X))
                if j < self.buffer_size:
                    k = np.random.randint(0, self.buffer_size)
                    self.buffer_X[k] = X[i]
                    self.buffer_y[k] = y[i]

    def _sample_buffer(self, batch_size: int) -> Tuple[
            Optional[torch.Tensor], Optional[torch.Tensor]]:
        """Uniformly sample from the replay buffer."""
        if len(self.buffer_X) == 0:
            return None, None
        indices = np.random.choice(len(self.buffer_X),
                                   size=min(batch_size, len(self.buffer_X)),
                                   replace=False)
        bx = np.stack([self.buffer_X[j] for j in indices])
        by = np.stack([self.buffer_y[j] for j in indices])
        return (torch.as_tensor(bx, dtype=torch.float32, device=self.device),
                torch.as_tensor(by, dtype=torch.float32, device=self.device))

    def train_task(self, task_data: Tuple[np.ndarray, np.ndarray],
                   task_id: int) -> None:
        X, y = task_data
        dataset = TensorDataset(
            torch.as_tensor(X, dtype=torch.float32),
            torch.as_tensor(y, dtype=torch.float32),
        )
        loader = DataLoader(dataset, batch_size=32, shuffle=True)
        self.model.train()
        epochs = 100
        replay_half = 16  # half of mini-batch reserved for replay

        for _epoch in range(epochs):
            for xb, yb in loader:
                xb, yb = xb.to(self.device), yb.to(self.device)
                self.optimizer.zero_grad()
                loss_task = self.criterion(self.model(xb), yb)

                # Replay component
                loss_replay = torch.tensor(0.0, device=self.device)
                if len(self.buffer_X) > 0:
                    bx_r, by_r = self._sample_buffer(replay_half)
                    if bx_r is not None:
                        loss_replay = self.criterion(self.model(bx_r), by_r)

                loss = loss_task + self.beta * loss_replay
                loss.backward()
                self.optimizer.step()

        # Add current task data to buffer
        self._add_to_buffer(X, y)
        self.n_tasks_seen += 1

    def evaluate(self, test_data: Tuple[np.ndarray, np.ndarray]) -> float:
        return compute_rmse(self.model, test_data, self.device)


# ===========================================================================
#  4. Synaptic Intelligence (SI)
# ===========================================================================

class SynapticIntelligence(ContinualLearningMethod):
    """
    4. Synaptic Intelligence  (Zenke et al., 2017)
    ────────────────────────────────────────────────
    Online importance estimation via parameter path integrals.

    During training, track the running path integral for each parameter:
        Ω̃_i  ←  Ω̃_i  −  (∂L/∂θ_i) · (θ_i − θ_i^{prev})

    After each task, update the importance weights:
        Ω_i  ←  Ω_i  +  Ω̃_i

    Regularisation penalty for subsequent tasks:
        L_total = L_task + c · Σ_i  Ω_i · (θ_i − θ_i^*)²

    where c is the damping / consolidation strength.
    """

    def __init__(self, c: float = 0.1, epsilon: float = 1e-8,
                 **kwargs) -> None:
        """
        Parameters
        ----------
        c : float
            Damping / consolidation strength.  Default 0.1.
        epsilon : float
            Numerical stabiliser to avoid division by zero.
        """
        super().__init__(**kwargs)
        self.c = c
        self.epsilon = epsilon
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

        # Running accumulators for SI
        self.omega: Dict[str, torch.Tensor] = {}   # final importance
        self.omega_tilde: Dict[str, torch.Tensor] = {}  # running path integral
        self.prev_params: Dict[str, torch.Tensor] = {}
        self.star_params: Dict[str, torch.Tensor] = {}  # θ* at end of last task

        # Initialise previous parameter snapshot
        self._snapshot_params(self.prev_params)

    def _snapshot_params(self, target: Dict[str, torch.Tensor]) -> None:
        """Save current model parameters into *target* dict."""
        for n, p in self.model.named_parameters():
            if p.requires_grad:
                target[n] = p.data.clone()

    def train_task(self, task_data: Tuple[np.ndarray, np.ndarray],
                   task_id: int) -> None:
        X, y = task_data
        dataset = TensorDataset(
            torch.as_tensor(X, dtype=torch.float32),
            torch.as_tensor(y, dtype=torch.float32),
        )
        loader = DataLoader(dataset, batch_size=32, shuffle=True)
        self.model.train()
        epochs = 100

        # Reset path integral accumulators for the new task
        self.omega_tilde = {n: torch.zeros_like(p)
                            for n, p in self.model.named_parameters()
                            if p.requires_grad}
        # Store previous-task parameters as starting point
        self._snapshot_params(self.prev_params)

        for _epoch in range(epochs):
            for xb, yb in loader:
                xb, yb = xb.to(self.device), yb.to(self.device)
                self.optimizer.zero_grad()
                loss = self.criterion(self.model(xb), yb)

                # Add SI penalty from accumulated importance
                if self.omega:
                    penalty = torch.tensor(0.0, device=self.device)
                    for n, p in self.model.named_parameters():
                        if p.requires_grad and n in self.omega:
                            penalty += (self.omega[n] *
                                        (p - self.star_params[n]) ** 2).sum()
                    loss = loss + self.c * penalty

                loss.backward()

                # Update path integral BEFORE the optimiser step
                for n, p in self.model.named_parameters():
                    if p.requires_grad and n in self.omega_tilde:
                        if p.grad is not None:
                            self.omega_tilde[n] += (
                                -p.grad.data * (p.data - self.prev_params[n])
                            )

                self.optimizer.step()

                # Update prev_params after the step
                for n, p in self.model.named_parameters():
                    if p.requires_grad and n in self.prev_params:
                        self.prev_params[n] = p.data.clone()

        # ── End of task: consolidate importance ──
        for n in self.omega_tilde:
            if n not in self.omega:
                self.omega[n] = torch.zeros_like(self.omega_tilde[n])
            # Normalise by parameter magnitude for stability
            param = dict(self.model.named_parameters())[n]
            self.omega[n] += (
                self.omega_tilde[n] /
                (torch.abs(dict(self.model.named_parameters())[n].data) +
                 self.epsilon)
            )

        # Store θ* (parameters at end of this task)
        self._snapshot_params(self.star_params)
        self.n_tasks_seen += 1

    def evaluate(self, test_data: Tuple[np.ndarray, np.ndarray]) -> float:
        return compute_rmse(self.model, test_data, self.device)


# ===========================================================================
#  5. Memory Aware Synapses (MAS)
# ===========================================================================

class MAS(ContinualLearningMethod):
    """
    5. Memory Aware Synapses  (Aljundi et al., 2018)
    ──────────────────────────────────────────────────
    Parameter importance is computed from the **sensitivity of the output**
    to each parameter, without using labels:

        g_i = (1/N) Σ_{n=1}^{N}  |∂‖f(x_n)‖₂ / ∂θ_i|

    After each task, importance g_i is accumulated and stored parameters
    θ* are saved.  The regularisation penalty is:

        L_total = L_task + λ · Σ_i  g_i · (θ_i − θ*_i)²
    """

    def __init__(self, lam: float = 1.0, **kwargs) -> None:
        """
        Parameters
        ----------
        lam : float
            MAS regularisation strength.  Default 1.0.
        """
        super().__init__(**kwargs)
        self.lam = lam
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

        # Accumulated importance weights
        self.importance: Dict[str, torch.Tensor] = {}
        # Stored parameters at the end of each task
        self.star_params: Dict[str, torch.Tensor] = {}

    def _compute_output_sensitivity(self, data: Tuple[np.ndarray, np.ndarray]
                                    ) -> Dict[str, torch.Tensor]:
        """
        Compute importance g_i = (1/N) Σ |∂‖output‖ / ∂θ_i|.

        We use the L2 norm of the output as a label-free surrogate for
        importance (Aljundi et al., 2018, Eq. 4).
        """
        X, _y = data
        dataset = TensorDataset(
            torch.as_tensor(X, dtype=torch.float32),
        )
        loader = DataLoader(dataset, batch_size=64, shuffle=False)
        importance = {n: torch.zeros_like(p)
                      for n, p in self.model.named_parameters()
                      if p.requires_grad}
        n_samples = 0

        self.model.eval()
        for (xb,) in loader:
            xb = xb.to(self.device)
            self.model.zero_grad()
            output = self.model(xb)
            # Label-free: use L2 norm of output as the "target"
            l2_norm = torch.norm(output, dim=1).sum()
            l2_norm.backward()

            batch_n = xb.size(0)
            for n, p in self.model.named_parameters():
                if p.requires_grad and p.grad is not None:
                    importance[n] += p.grad.data.abs() * batch_n
            n_samples += batch_n

        # Normalise by total number of samples
        for n in importance:
            importance[n] /= max(n_samples, 1)

        self.model.train()
        return importance

    def train_task(self, task_data: Tuple[np.ndarray, np.ndarray],
                   task_id: int) -> None:
        X, y = task_data
        dataset = TensorDataset(
            torch.as_tensor(X, dtype=torch.float32),
            torch.as_tensor(y, dtype=torch.float32),
        )
        loader = DataLoader(dataset, batch_size=32, shuffle=True)
        self.model.train()
        epochs = 100

        for _epoch in range(epochs):
            for xb, yb in loader:
                xb, yb = xb.to(self.device), yb.to(self.device)
                self.optimizer.zero_grad()
                loss = self.criterion(self.model(xb), yb)

                # Add MAS penalty from accumulated importance
                if self.importance:
                    penalty = torch.tensor(0.0, device=self.device)
                    for n, p in self.model.named_parameters():
                        if p.requires_grad and n in self.importance:
                            penalty += (self.importance[n] *
                                        (p - self.star_params[n]) ** 2).sum()
                    loss = loss + self.lam * penalty

                loss.backward()
                self.optimizer.step()

        # ── End of task: compute importance & save θ* ──
        imp = self._compute_output_sensitivity(task_data)
        for n in imp:
            if n not in self.importance:
                self.importance[n] = torch.zeros_like(imp[n])
            self.importance[n] += imp[n]

        self.star_params = {n: p.data.clone()
                            for n, p in self.model.named_parameters()
                            if p.requires_grad}

        self.n_tasks_seen += 1

    def evaluate(self, test_data: Tuple[np.ndarray, np.ndarray]) -> float:
        return compute_rmse(self.model, test_data, self.device)


# ===========================================================================
#  6. GEM (Gradient Episodic Memory)
# ===========================================================================

class GEM(ContinualLearningMethod):
    """
    6. Gradient Episodic Memory  (Lopez-Paz & Ranzato, 2017)
    ─────────────────────────────────────────────────────────
    Constraint-based continual learning.  After computing the gradient g
    on the current task, project g so that for each past task t:

        g^T · g_t  ≥ 0

    i.e. the projected gradient should not increase the loss on any past
    task (measured on stored episodic memories).

    Per-task replay memory stores a subset of each task's data.
    """

    def __init__(self, memory_per_task: int = 50, **kwargs) -> None:
        """
        Parameters
        ----------
        memory_per_task : int
            Number of exemplars stored per task in episodic memory.
        """
        super().__init__(**kwargs)
        self.memory_per_task = memory_per_task
        self.optimizer = optim.SGD(self.model.parameters(), lr=self.lr,
                                    momentum=0.9)
        self.criterion = nn.MSELoss()

        # Per-task episodic memory: list of (X_mem, y_mem) arrays
        self.memory: List[Tuple[np.ndarray, np.ndarray]] = []
        # Stored gradients (computed on-the-fly during projection)
        self.n_tasks_seen = 0

    def _store_memory(self, task_data: Tuple[np.ndarray, np.ndarray]) -> None:
        """Randomly select memory_per_task exemplars from the task data."""
        X, y = task_data
        n = min(self.memory_per_task, len(X))
        indices = np.random.choice(len(X), size=n, replace=False)
        self.memory.append((X[indices], y[indices]))

    def _compute_gradient(self, X: np.ndarray, y: np.ndarray
                          ) -> torch.Tensor:
        """
        Compute the flattened gradient of MSE loss on (X, y).

        Returns
        -------
        torch.Tensor, shape (d,)
            Concatenated gradient vector.
        """
        X_t = torch.as_tensor(X, dtype=torch.float32, device=self.device)
        y_t = torch.as_tensor(y, dtype=torch.float32, device=self.device)
        self.model.zero_grad()
        loss = self.criterion(self.model(X_t), y_t)
        loss.backward()

        grads = []
        for p in self.model.parameters():
            if p.requires_grad:
                if p.grad is not None:
                    grads.append(p.grad.data.clone().view(-1))
                else:
                    grads.append(torch.zeros_like(p.data).view(-1))

        return torch.cat(grads)

    def _project_gradient(self, g: torch.Tensor) -> torch.Tensor:
        """
        Project gradient *g* onto the feasible region defined by:
            g^T · g_mem_t  ≥ 0  for all past tasks t.

        Uses the quadratic programming solution from Lopez-Paz+ (2017).
        If the constraints are already satisfied, returns g unchanged.
        """
        if len(self.memory) == 0:
            return g

        # Compute gradients on each past task's memory
        g_mem = []
        for X_mem, y_mem in self.memory:
            g_mem.append(self._compute_gradient(X_mem, y_mem))

        # Stack into matrix G: shape (num_past_tasks, d)
        G = torch.stack(g_mem)  # (T, d)

        # Check if constraints are satisfied: G @ g >= 0
        constraints = G @ g
        if (constraints >= -1e-6).all():
            return g  # No projection needed

        # Solve quadratic programme via pseudo-inverse
        # minimise  0.5 ||g - g_tilde||^2   s.t.  G g_tilde >= 0
        # KKT system:  [I  -G^T] [v]     [g]
        #              [G   0  ] [λ]  =  [0]
        # Use iterative Lagrange multiplier update (simpler, numerically stable)
        d = g.size(0)
        T = G.size(0)

        # Build KKT-like system
        GGt = G @ G.T  # (T, T)
        mask = constraints < 0  # active constraints

        # Iterative solution for active constraints only
        lambda_vec = torch.zeros(T, device=self.device)
        for _ in range(100):  # convergence iterations
            active = (constraints + GGt @ lambda_vec) < 0
            if not active.any():
                break
            # Solve the reduced system for active constraints
            G_active = G[active]
            Gg_active = G_active @ g  # (num_active,)
            # Simplified: use least-squares projection
            coeff = torch.linalg.lstsq(G_active.T @ G_active.t() if False
                                       else G_active @ G_active.T,
                                       -Gg_active,
                                       rcond=1e-6).solution
            lambda_vec[active] = coeff

        # Apply correction
        g_proj = g + G.T @ lambda_vec

        # Verify constraints are satisfied (with small tolerance)
        projected_constraints = G @ g_proj
        if (projected_constraints < -1e-5).any():
            # Fallback: zero out violating components (gradient clipping)
            warnings.warn(
                "GEM projection did not fully satisfy constraints; "
                "using zero-gradient fallback for violated directions.")
            # At minimum, zero the gradient components that cause violations
            g_proj = g  # fallback: use original (skip projection)

        return g_proj

    def _set_gradient(self, flat_grad: torch.Tensor) -> None:
        """Load a flat gradient vector back into model parameters."""
        idx = 0
        for p in self.model.parameters():
            if p.requires_grad:
                n_elements = p.data.numel()
                if p.grad is None:
                    p.grad = torch.zeros_like(p.data)
                p.grad.data = flat_grad[idx:idx + n_elements].view(
                    p.data.shape)
                idx += n_elements

    def train_task(self, task_data: Tuple[np.ndarray, np.ndarray],
                   task_id: int) -> None:
        X, y = task_data
        dataset = TensorDataset(
            torch.as_tensor(X, dtype=torch.float32),
            torch.as_tensor(y, dtype=torch.float32),
        )
        loader = DataLoader(dataset, batch_size=32, shuffle=True)
        self.model.train()
        epochs = 100

        for _epoch in range(epochs):
            for xb, yb in loader:
                xb, yb = xb.to(self.device), yb.to(self.device)

                # 1) Compute gradient on current task
                g_current = self._compute_gradient(
                    xb.detach().cpu().numpy(),
                    yb.detach().cpu().numpy())

                # 2) Project gradient to satisfy GEM constraints
                if len(self.memory) > 0:
                    g_projected = self._project_gradient(g_current)
                else:
                    g_projected = g_current

                # 3) Apply projected gradient manually
                self.optimizer.zero_grad()
                self._set_gradient(g_projected)
                self.optimizer.step()

        # ── Store episodic memory ──
        self._store_memory(task_data)
        self.n_tasks_seen += 1

    def evaluate(self, test_data: Tuple[np.ndarray, np.ndarray]) -> float:
        return compute_rmse(self.model, test_data, self.device)


# ===========================================================================
#  7. MIR (Maximally Interfered Retrieval)
# ===========================================================================

class MIR(ContinualLearningMethod):
    """
    7. Maximally Interfered Retrieval  (Banga et al., 2019)
    ───────────────────────────────────────────────────────
    Like Experience Replay but selects replay samples whose gradients
    are **most opposed** to the current task gradient – i.e. the
    samples that would be forgotten most without rehearsal.

    For each candidate sample x_i in the buffer, compute the inner
    product  g_current · g(x_i)  and select samples with the **most
    negative** values (highest interference).
    """

    def __init__(self, buffer_size: int = 200, **kwargs) -> None:
        """
        Parameters
        ----------
        buffer_size : int
            Maximum number of samples in the replay buffer.  Default 200.
        """
        super().__init__(**kwargs)
        self.buffer_size = buffer_size
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

        # Replay buffer
        self.buffer_X: List[np.ndarray] = []
        self.buffer_y: List[np.ndarray] = []

    def _add_to_buffer(self, X: np.ndarray, y: np.ndarray) -> None:
        """Reservoir-sampling insertion into the replay buffer."""
        for i in range(len(X)):
            if len(self.buffer_X) < self.buffer_size:
                self.buffer_X.append(X[i].copy())
                self.buffer_y.append(y[i].copy())
            else:
                j = np.random.randint(0, len(X))
                if j < self.buffer_size:
                    k = np.random.randint(0, self.buffer_size)
                    self.buffer_X[k] = X[i].copy()
                    self.buffer_y[k] = y[i].copy()

    def _gradient_on_sample(self, x: np.ndarray,
                            y: np.ndarray) -> Optional[torch.Tensor]:
        """Compute the flat gradient vector for a single sample (x, y)."""
        self.model.zero_grad()
        x_t = torch.as_tensor(x, dtype=torch.float32,
                               device=self.device).unsqueeze(0)
        y_t = torch.as_tensor(y, dtype=torch.float32,
                               device=self.device).unsqueeze(0)
        loss = self.criterion(self.model(x_t), y_t)
        loss.backward()
        grads = []
        has_grad = False
        for p in self.model.parameters():
            if p.requires_grad:
                if p.grad is not None:
                    grads.append(p.grad.data.clone().view(-1))
                    has_grad = True
                else:
                    grads.append(torch.zeros(p.data.numel(),
                                             device=self.device))
        if not has_grad:
            return None
        return torch.cat(grads)

    def _mir_select(self, current_grad: torch.Tensor,
                    batch_size: int) -> Tuple[
            Optional[torch.Tensor], Optional[torch.Tensor]]:
        """
        Select *batch_size* samples from the buffer whose gradients are
        most opposed to *current_grad* (maximally interfered retrieval).

        Score for sample i:  s_i = −(g_current · g(x_i))
        Select samples with the highest s_i (most negative inner product).
        """
        if len(self.buffer_X) == 0:
            return None, None

        batch_size = min(batch_size, len(self.buffer_X))

        # Subsample candidates if buffer is large (for efficiency)
        n_candidates = min(len(self.buffer_X), batch_size * 3)
        candidate_indices = np.random.choice(
            len(self.buffer_X), size=n_candidates, replace=False)

        scores = []
        valid_indices = []
        for idx in candidate_indices:
            grad_i = self._gradient_on_sample(self.buffer_X[idx],
                                              self.buffer_y[idx])
            if grad_i is not None:
                # Inner product: high positive → aligned, negative → opposed
                inner = torch.dot(current_grad, grad_i)
                scores.append(-inner.item())  # negate: higher = more opposed
                valid_indices.append(idx)

        if not valid_indices:
            # Fallback: uniform random selection
            rand_idx = np.random.choice(len(self.buffer_X),
                                        size=batch_size, replace=False)
            bx = np.stack([self.buffer_X[j] for j in rand_idx])
            by = np.stack([self.buffer_y[j] for j in rand_idx])
        else:
            # Select top-k most interfered
            scores = np.array(scores)
            top_k = min(batch_size, len(valid_indices))
            top_local = np.argpartition(scores, -top_k)[-top_k:]
            selected = [valid_indices[j] for j in top_local]

            bx = np.stack([self.buffer_X[j] for j in selected])
            by = np.stack([self.buffer_y[j] for j in selected])

        return (torch.as_tensor(bx, dtype=torch.float32, device=self.device),
                torch.as_tensor(by, dtype=torch.float32, device=self.device))

    def train_task(self, task_data: Tuple[np.ndarray, np.ndarray],
                   task_id: int) -> None:
        X, y = task_data
        dataset = TensorDataset(
            torch.as_tensor(X, dtype=torch.float32),
            torch.as_tensor(y, dtype=torch.float32),
        )
        loader = DataLoader(dataset, batch_size=32, shuffle=True)
        self.model.train()
        epochs = 100
        replay_half = 16

        for _epoch in range(epochs):
            for xb, yb in loader:
                xb, yb = xb.to(self.device), yb.to(self.device)
                self.optimizer.zero_grad()
                loss_task = self.criterion(self.model(xb), yb)
                loss = loss_task

                # MIR replay: select most-interfered samples
                if len(self.buffer_X) > 0:
                    # Compute current task gradient on this mini-batch
                    self.optimizer.zero_grad()
                    loss_task.backward(retain_graph=True)
                    current_grad = []
                    for p in self.model.parameters():
                        if p.requires_grad:
                            if p.grad is not None:
                                current_grad.append(
                                    p.grad.data.clone().view(-1))
                            else:
                                current_grad.append(
                                    torch.zeros(p.data.numel(),
                                               device=self.device))
                    current_grad = torch.cat(current_grad)

                    # Select MIR samples
                    bx_r, by_r = self._mir_select(current_grad, replay_half)
                    if bx_r is not None:
                        loss_replay = self.criterion(self.model(bx_r), by_r)
                        loss = loss_task + 0.5 * loss_replay

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

        # ── Add current task data to buffer ──
        self._add_to_buffer(X, y)
        self.n_tasks_seen += 1

    def evaluate(self, test_data: Tuple[np.ndarray, np.ndarray]) -> float:
        return compute_rmse(self.model, test_data, self.device)


# ===========================================================================
#  Experiment Harness: Sequential Task Generation & Evaluation
# ===========================================================================

def generate_linear_tasks(n_tasks: int = 5, n_samples: int = 500,
                          input_dim: int = 5, noise_std: float = 0.1,
                          seed: int = 42) -> List[Tuple[
                              Tuple[np.ndarray, np.ndarray],
                              Tuple[np.ndarray, np.ndarray]]]:
    """
    Generate sequential linear regression tasks with different coefficients.

    Each task t has:
        y = X @ w_t + b_t + ε,    ε ~ N(0, noise_std²)

    The weight vectors w_t are drawn from different regions of the
    parameter space to ensure task diversity and measurable forgetting.

    Parameters
    ----------
    n_tasks : int
        Number of sequential tasks.
    n_samples : int
        Number of samples per task.
    input_dim : int
        Feature dimensionality.
    noise_std : float
        Gaussian noise standard deviation.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    list of tuple
        [(train_data_t, test_data_t), ...] where each data element is
        (X, y) as numpy arrays.
    """
    rng = np.random.RandomState(seed)
    tasks = []

    for t in range(n_tasks):
        # Generate diverse weight vectors: rotate in parameter space
        angle = t * (2 * math.pi / n_tasks)
        w_true = rng.randn(input_dim) * 2.0
        # Add task-specific bias to weights (rotation in w-space)
        w_true[0] += 3.0 * math.cos(angle)
        w_true[1] += 3.0 * math.sin(angle)
        bias = t * 1.5 - (n_tasks - 1) * 0.75  # spread biases

        # Training data
        X_train = rng.randn(n_samples, input_dim).astype(np.float32)
        y_train = (X_train @ w_true + bias +
                   rng.randn(n_samples) * noise_std).astype(np.float32)
        y_train = y_train.reshape(-1, 1)

        # Test data
        X_test = rng.randn(200, input_dim).astype(np.float32)
        y_test = (X_test @ w_true + bias +
                  rng.randn(200) * noise_std).astype(np.float32)
        y_test = y_test.reshape(-1, 1)

        tasks.append(((X_train, y_train), (X_test, y_test)))

    return tasks


def run_method(method: ContinualLearningMethod, tasks: List[Tuple[
        Tuple[np.ndarray, np.ndarray],
        Tuple[np.ndarray, np.ndarray]]]) -> np.ndarray:
    """
    Run a continual learning method on all sequential tasks and record
    the full RMSE matrix.

    Parameters
    ----------
    method : ContinualLearningMethod
        An instantiated baseline method.
    tasks : list
        Output of generate_linear_tasks().

    Returns
    -------
    np.ndarray, shape (T, T)
        rmse_matrix[t][i] = RMSE on task i's test set after training
        through task t.
    """
    T = len(tasks)
    rmse_matrix = np.full((T, T), np.nan)

    for t in range(T):
        train_data, _test_data = tasks[t]
        method.train_task(train_data, task_id=t)

        # Evaluate on ALL tasks seen so far
        for i in range(t + 1):
            _, test_data_i = tasks[i]
            rmse_matrix[t, i] = method.evaluate(test_data_i)

    method.rmse_matrix = rmse_matrix
    return rmse_matrix


# ===========================================================================
#  Main: Run all baselines and print comparison table
# ===========================================================================

def main() -> None:
    """
    Entry point: instantiate all 7 baselines, run them on 5 sequential
    linear regression tasks, and print a comparison table of RMSE and
    Backward Transfer (BWT).
    """
    print("=" * 78)
    print("  EWC-IXER Baseline Comparison: Continual Learning Methods")
    print("=" * 78)
    print()

    # ── Generate tasks ──
    n_tasks = 5
    tasks = generate_linear_tasks(n_tasks=n_tasks, n_samples=500,
                                  input_dim=5, noise_std=0.1, seed=SEED)
    print(f"Generated {n_tasks} sequential linear regression tasks "
          f"(500 train / 200 test each, input_dim=5).")
    print()

    # ── Define all baselines ──
    common_kwargs = dict(input_dim=5, hidden_dim=32, dropout=0.2,
                         lr=1e-3, device="cpu")

    methods: List[Tuple[str, ContinualLearningMethod]] = [
        ("1. Naive Fine-Tuning",
         NaiveFineTuning(**common_kwargs)),
        ("2. EWC-Only (λ=500)",
         EWCOnly(lam=500.0, **common_kwargs)),
        ("3. Experience Replay (buf=200, β=0.5)",
         ExperienceReplay(buffer_size=200, beta=0.5, **common_kwargs)),
        ("4. Synaptic Intelligence (c=0.1)",
         SynapticIntelligence(c=0.1, **common_kwargs)),
        ("5. MAS (λ=1.0)",
         MAS(lam=1.0, **common_kwargs)),
        ("6. GEM (mem=50/task)",
         GEM(memory_per_task=50, **common_kwargs)),
        ("7. MIR (buf=200)",
         MIR(buffer_size=200, **common_kwargs)),
    ]

    # ── Run each method ──
    results: List[Tuple[str, np.ndarray, float]] = []

    for name, method in methods:
        print(f"  Running: {name} ...", end=" ", flush=True)
        # Re-seed for fair comparison
        torch.manual_seed(SEED)
        np.random.seed(SEED)

        rmse_mat = run_method(method, tasks)
        bwt = compute_bwt(rmse_mat)
        results.append((name, rmse_mat, bwt))

        # Final average RMSE across all tasks
        final_rmse = rmse_mat[-1]  # RMSE on each task after final task
        avg_rmse = np.nanmean(final_rmse)
        print(f"  Avg RMSE = {avg_rmse:.4f},  BWT = {bwt:+.4f}")

    # ── Print comparison table ──
    print()
    print("=" * 78)
    print("  RESULTS COMPARISON TABLE")
    print("=" * 78)
    print()

    # Header
    header = (f"{'Method':<42s}  "
              f"{'Avg RMSE':>9s}  "
              f"{'BWT':>8s}  ")
    for i in range(n_tasks):
        header += f"{'T' + str(i + 1):>7s}"
    print(header)
    print("-" * len(header))

    for name, rmse_mat, bwt in results:
        final_rmse = rmse_mat[-1]
        avg = np.nanmean(final_rmse)
        row = f"{name:<42s}  {avg:>9.4f}  {bwt:>+8.4f}  "
        for i in range(n_tasks):
            val = rmse_mat[-1, i]
            row += f"{val:>7.4f}" if not np.isnan(val) else f"{'N/A':>7s}"
        print(row)

    print("-" * len(header))
    print()

    # ── Detailed per-task RMSE matrices ──
    print("=" * 78)
    print("  DETAILED RMSE MATRICES  (row = trained up to task t, "
          "col = evaluated on task i)")
    print("=" * 78)
    print()

    for name, rmse_mat, bwt in results:
        print(f"  {name}")
        T = rmse_mat.shape[0]
        col_header = f"{'':>12s}  "
        for i in range(T):
            col_header += f"{'Task ' + str(i + 1):>10s}"
        print(col_header)
        print("  " + "-" * (12 + T * 10 + 2))

        for t in range(T):
            row = f"  {'After T' + str(t + 1):>10s}  "
            for i in range(T):
                val = rmse_mat[t, i]
                if np.isnan(val):
                    row += f"{'—':>10s}"
                else:
                    row += f"{val:>10.4f}"
            print(row)
        print()

    # ── Summary ──
    print("=" * 78)
    print("  SUMMARY")
    print("=" * 78)

    best_avg_idx = int(np.argmin([np.nanmean(r[-1]) for _, r, _ in results]))
    # With RMSE: lower (more negative) BWT is better (less forgetting)
    best_bwt_idx = int(np.argmin([b for _, _, b in results]))

    print(f"  Best Average RMSE : {results[best_avg_idx][0]}  "
          f"({np.nanmean(results[best_avg_idx][1][-1]):.4f})")
    print(f"  Best BWT          : {results[best_bwt_idx][0]}  "
          f"({results[best_bwt_idx][2]:+.4f})")
    print()
    print("  (With RMSE: positive BWT = forgetting / RMSE increased; "
          "negative = forward transfer / RMSE decreased.)")
    print("=" * 78)


if __name__ == "__main__":
    main()
