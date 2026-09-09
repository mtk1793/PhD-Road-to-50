"""
EWC-IXER: Elastic Weight Consolidation with Importance-Weighted Experience Replay
===================================================================================

Core algorithm implementation for continual learning on regression tasks.

This module implements the EWC-IXER method which combines:
  1. Elastic Weight Consolidation (EWC) for parameter-based regularization
  2. Importance-Weighted Experience Replay (IXER) for data-based retention

Architecture:  MLP  Input(5) -> Hidden(32, ReLU, 20% dropout) -> Output(1)
Total trainable parameters: 225

Classes:
    - MLPPredictor    : Small regression MLP (225 parameters)
    - ReplayBuffer    : Priority-based experience replay buffer
    - EWCIXERAgent    : Combined EWC + IXER continual learning agent

Usage:
    python ewc_ixer_model.py
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from collections import OrderedDict
import copy
import warnings

warnings.filterwarnings('ignore')


# ============================================================================
#  1.  MLP  PREDICTOR  ARCHITECTURE
# ============================================================================

class MLPPredictor(nn.Module):
    """
    Simple MLP for regression tasks.

    Architecture
    -------------
        Input(5) -> Linear(5,32) -> ReLU -> Dropout(0.2) -> Linear(32,1) -> Output

    Parameter count
    ----------------
        Layer 1 weight : 5  x 32 = 160
        Layer 1 bias   : 32
        Layer 2 weight : 32 x 1  = 32
        Layer 2 bias   : 1
        Total          : 160 + 32 + 32 + 1 = **225**

    Parameters
    ----------
        input_dim    : int, default 5
        hidden_dim   : int, default 32
        output_dim   : int, default 1
        dropout_rate : float, default 0.2  (20 % dropout)
    """

    def __init__(self, input_dim=5, hidden_dim=32,
                 output_dim=1, dropout_rate=0.2):
        super(MLPPredictor, self).__init__()

        # Layer 1: input -> hidden (192 parameters: 160 weights + 32 biases)
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=dropout_rate)

        # Layer 2: hidden -> output (33 parameters: 32 weights + 1 bias)
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        """
        Forward pass  x -> y_hat.

        Parameters
        ----------
            x : (batch_size, input_dim)

        Returns
        -------
            y_hat : (batch_size, output_dim)
        """
        x = self.fc1(x)       # (B, 32)
        x = self.relu(x)      # (B, 32)
        x = self.dropout(x)   # (B, 32)
        x = self.fc2(x)       # (B, 1)
        return x


# ============================================================================
#  2.  IMPORTANCE-WEIGHTED  EXPERIENCE  REPLAY  BUFFER
# ============================================================================

class ReplayBuffer:
    """
    Priority-based Experience Replay Buffer for continual learning.

    Priority rule (from the paper)
    -------------------------------
        P(x_i) proportional to (e_i)^alpha + epsilon
    where
        e_i = |y_i - f_theta(x_i)|   absolute prediction error
        alpha   = 0.6                    priority exponent
        epsilon   = 0.001                  small constant (avoids zero priority)

    Buffer policy
    --------------
        * Maximum capacity: **200** samples.
        * When full, the sample with the **lowest** priority is evicted.
        * The buffer is updated **once per task** after training on that task.

    Parameters
    ----------
        buffer_size : int   - maximum number of stored experiences (default 200)
        alpha       : float - priority exponent              (default 0.6)
        epsilon     : float - priority floor                  (default 0.001)
    """

    def __init__(self, buffer_size=200, alpha=0.6, epsilon=0.001):
        self.buffer_size = buffer_size
        self.alpha = alpha
        self.epsilon = epsilon

        # Per-experience storage
        self._states = []       # input  tensors
        self._targets = []      # target tensors
        self._priorities = []   # priority values (float)

    # ------------------------------------------------------------------
    #  Priority helpers
    # ------------------------------------------------------------------

    def _compute_priority(self, error):
        """P proportional to (|e|)^alpha + epsilon"""
        return np.abs(error) ** self.alpha + self.epsilon

    # ------------------------------------------------------------------
    #  Add / sample
    # ------------------------------------------------------------------

    def add(self, states, targets, model):
        """
        Add a batch of experiences to the buffer.

        Prediction errors are computed with *model* to derive priorities.
        If the buffer exceeds its capacity the **lowest-priority** sample is
        evicted before insertion.

        Parameters
        ----------
            states  : (N, input_dim)  torch.Tensor
            targets : (N,) or (N, 1)  torch.Tensor
            model   : nn.Module used to compute prediction errors
        """
        model.eval()
        with torch.no_grad():
            preds = model(states).squeeze(-1)              # (N,)
            tgt = targets.squeeze(-1) if targets.dim() > 1 else targets
            errors = (tgt - preds).cpu().numpy()            # (N,)

        priorities = self._compute_priority(errors)

        for i in range(len(states)):
            # Evict lowest-priority sample when buffer is full
            if len(self._states) >= self.buffer_size:
                min_idx = int(np.argmin(self._priorities))
                self._states.pop(min_idx)
                self._targets.pop(min_idx)
                self._priorities.pop(min_idx)

            self._states.append(states[i].cpu().clone())
            self._targets.append(targets[i].cpu().clone())
            self._priorities.append(float(priorities[i]))

    def sample(self, batch_size):
        """
        Draw a mini-batch using **priority-weighted** sampling.

        Importance-sampling weights correct for the biased distribution:
            w_i = (N * P(i))^(-beta),   beta = 0.4
        normalised by max(w) for numerical stability.

        Returns
        -------
            (states, targets, weights)  or  (None, None, None) if empty
        """
        n = len(self._states)
        if n == 0:
            return None, None, None

        probs = np.array(self._priorities, dtype=np.float64)
        probs /= probs.sum()                            # normalise to distribution

        k = min(batch_size, n)
        indices = np.random.choice(n, size=k, replace=False, p=probs)

        # Importance-sampling weights  w_i = (N * P(i))^(-0.4)
        beta_is = 0.4
        weights = (n * probs[indices]) ** (-beta_is)
        weights /= weights.max()

        batch_s = torch.stack([self._states[i] for i in indices])
        batch_t = torch.stack([self._targets[i] for i in indices])
        batch_w = torch.tensor(weights, dtype=torch.float32)

        return batch_s, batch_t, batch_w

    def update_priorities(self, indices, errors):
        """Re-compute priorities for specific buffer entries."""
        new_pri = self._compute_priority(errors)
        for idx, p in zip(indices, new_pri):
            self._priorities[idx] = float(p)

    # ------------------------------------------------------------------
    #  Misc
    # ------------------------------------------------------------------

    def __len__(self):
        return len(self._states)

    def __repr__(self):
        return (f"ReplayBuffer(size={len(self)}/{self.buffer_size}, "
                f"alpha={self.alpha}, epsilon={self.epsilon})")


# ============================================================================
#  3.  EWC-IXER  AGENT
# ============================================================================

class EWCIXERAgent:
    """
    EWC-IXER:  Elastic Weight Consolidation  +  Importance-Weighted
               Experience Replay.

    Combined loss for task k
    ---------------------------
        L_k(theta) = L_task(theta)
                   + lambda * sum_{j<k} sum_i  F_i^(j) (theta_i - theta_i^(j*))^2
                   + beta  * L_replay(theta)

    Defaults from the paper
    -----------------------
        lambda (lambda_ewc)   = 500     EWC regularisation strength
        beta  (beta_replay) = 0.5     replay loss weight
        EWC damping         = 1e-4    added to every diagonal Fisher entry
        Buffer size         = 200

    Training loop per task k
    ----------------------------
        (a) Compute EWC penalty  (current theta vs. all previous snapshots)
        (b) Sample from replay buffer with priority weights
        (c) Combined SGD step:  MSE + lambda*EWC + beta*replay
        (d) Compute diagonal Fisher on the task training set
        (e) Update replay buffer with priority-sampled task data
        (f) Store parameter snapshot theta^(k*)

    Parameters
    ----------
        input_dim     : int
        hidden_dim    : int
        output_dim    : int
        lambda_ewc    : float  - EWC weight (default 500)
        beta_replay   : float  - replay weight (default 0.5)
        lr            : float  - learning rate (default 0.001)
        buffer_size   : int    - replay buffer capacity (default 200)
        ewc_damping   : float  - Fisher damping (default 1e-4)
        device        : str    - 'cpu' or 'cuda'
    """

    def __init__(self, input_dim=5, hidden_dim=32,
                 output_dim=1, lambda_ewc=500.0,
                 beta_replay=0.5, lr=0.001,
                 buffer_size=200, ewc_damping=1e-4,
                 device='cpu'):

        self.device = torch.device(device)
        self.lambda_ewc = lambda_ewc
        self.beta_replay = beta_replay
        self.lr = lr
        self.ewc_damping = ewc_damping

        # -- Neural network --
        self.model = MLPPredictor(input_dim, hidden_dim, output_dim).to(self.device)

        # -- EWC bookkeeping (one entry per *completed* task) --
        #    Each entry: (fisher_diag: OrderedDict, param_snapshot: state_dict)
        self.ewc_tasks = []

        # -- Replay buffer --
        self.replay_buffer = ReplayBuffer(buffer_size=buffer_size,
                                           alpha=0.6, epsilon=0.001)

    # ------------------------------------------------------------------
    #  Utility
    # ------------------------------------------------------------------

    def count_parameters(self):
        """Return the total number of trainable parameters."""
        return sum(p.numel() for p in self.model.parameters()
                   if p.requires_grad)

    # ------------------------------------------------------------------
    #  Diagonal Fisher Information Matrix
    # ------------------------------------------------------------------

    def _compute_diagonal_fisher(self, dataloader, max_samples=None):
        r"""
        Compute the **diagonal** Fisher Information Matrix.

        For regression with Gaussian likelihood (sigma^2 = 1):

            log p(y | x, theta) = -1/2 (y - f_theta(x))^2 - 1/2 log(2 pi)

        so

            d log p / d theta_i  =  (y - f_theta(x)) * df / d theta_i

        The diagonal Fisher entry is:

            F_i = (1/|S|) sum_{(x,y) in S}
                  [ (y - f(x)) * df(x)/d theta_i ]^2

        A small damping term (1e-4) is added for numerical stability:
            F_i <- F_i + damping

        Implementation note
        -------------------
        A single forward pass per mini-batch is performed, then per-sample
        gradients are extracted via ``torch.autograd.grad`` with
        ``retain_graph=True`` (except for the last sample in the batch).
        This avoids redundant forward passes while still yielding true
        per-sample Fisher diagonal entries.

        Parameters
        ----------
            dataloader   : training-set DataLoader for the task
            max_samples  : if set, at most this many samples are used

        Returns
        -------
            OrderedDict  {param_name: diagonal_fisher_tensor}
        """
        self.model.eval()

        # Zero-initialise accumulators
        fisher = OrderedDict()
        for name, param in self.model.named_parameters():
            fisher[name] = torch.zeros_like(param.data, device=self.device)

        n_samples = 0

        for x_batch, y_batch in dataloader:
            x_batch = x_batch.to(self.device)
            y_batch = y_batch.to(self.device)
            if y_batch.dim() > 1:
                y_batch = y_batch.squeeze(-1)       # (B,)

            B = x_batch.size(0)
            if max_samples is not None and n_samples + B > max_samples:
                B = max_samples - n_samples
                x_batch = x_batch[:B]
                y_batch = y_batch[:B]

            # Single forward pass for the whole mini-batch
            outputs = self.model(x_batch)             # (B, 1)

            for i in range(B):
                # Per-sample gradient of the scalar output w.r.t. parameters
                grads = torch.autograd.grad(
                    outputs=outputs[i, 0],            # scalar
                    inputs=self.model.parameters(),
                    retain_graph=(i < B - 1),         # keep graph for next iter
                )

                # Residual  r = y - f(x)
                residual = (y_batch[i].item() - outputs[i, 0].item())

                # Accumulate  (r * df/d theta_i)^2
                for (name, _), g in zip(self.model.named_parameters(), grads):
                    fisher[name] += (residual * g.detach()) ** 2

            n_samples += B
            if max_samples is not None and n_samples >= max_samples:
                break

        # Normalise + damp
        n_samples = max(n_samples, 1)
        for name in fisher:
            fisher[name] = fisher[name] / n_samples + self.ewc_damping

        return fisher

    # ------------------------------------------------------------------
    #  EWC penalty
    # ------------------------------------------------------------------

    def _compute_ewc_penalty(self):
        r"""
        Sum of EWC penalties over all previously learned tasks.

            penalty = sum_{j<k} sum_i  F_i^(j) * (theta_i - theta_i^(j*))^2

        Returns
        -------
            scalar tensor
        """
        penalty = torch.tensor(0.0, device=self.device)

        for fisher_diag, param_snap in self.ewc_tasks:
            for name, param in self.model.named_parameters():
                if name in fisher_diag and name in param_snap:
                    penalty += (
                        fisher_diag[name] * (param - param_snap[name]) ** 2
                    ).sum()

        return penalty

    # ------------------------------------------------------------------
    #  Train on a single task
    # ------------------------------------------------------------------

    def train_on_task(self, task_id, train_loader,
                      epochs=100, batch_size=32):
        """
        Execute the full EWC-IXER training procedure for one task.

        Steps (matching the paper)
        --------------------------
        (a) Compute EWC penalty  theta vs. all previous snapshots
        (b) Sample mini-batch from replay buffer (priority weighted)
        (c) Combined SGD:  L_task + lambda*EWC + beta*L_replay
        (d) After training  ->  compute diagonal Fisher on task data
        (e) Update replay buffer with priority-sampled task data
        (f) Store parameter snapshot theta^(k*)

        Parameters
        ----------
            task_id     : current task index (0-based)
            train_loader: DataLoader for this task's training set
            epochs      : number of training epochs (default 100)
            batch_size  : mini-batch size          (default 32)

        Returns
        -------
            The trained ``nn.Module`` model.
        """
        optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        mse_fn = nn.MSELoss()

        header = (f"  Task {task_id} | prev_tasks={task_id} | "
                  f"buffer={len(self.replay_buffer)} | "
                  f"ewc_stored={len(self.ewc_tasks)}")
        print(f"\n{'=' * 65}")
        print(header)
        print(f"{'=' * 65}")

        # =====================  EPOCH LOOP  =====================
        for epoch in range(epochs):
            self.model.train()
            sum_total = sum_task = sum_ewc = sum_replay = 0.0
            n_batches = 0

            for x_batch, y_batch in train_loader:
                x_batch = x_batch.to(self.device)
                y_batch = y_batch.to(self.device)
                if y_batch.dim() > 1:
                    y_batch = y_batch.squeeze(-1)

                # ---- (a) EWC penalty on current theta ----
                ewc_penalty = self._compute_ewc_penalty()

                # ---- (b) Sample from replay buffer ----
                rep_x, rep_y, rep_w = self.replay_buffer.sample(batch_size)

                # ---- (c) Combined loss + back-prop ----
                optimizer.zero_grad()

                # Current-task MSE
                pred = self.model(x_batch).squeeze(-1)   # (B,)
                task_loss = mse_fn(pred, y_batch)

                # Total = task + lambda * EWC
                total_loss = task_loss + self.lambda_ewc * ewc_penalty

                # + beta * replay  (if buffer non-empty)
                replay_loss_val = 0.0
                if rep_x is not None:
                    rep_x = rep_x.to(self.device)
                    rep_y = rep_y.to(self.device)
                    rep_w = rep_w.to(self.device)
                    rep_pred = self.model(rep_x).squeeze(-1)
                    replay_loss_val = (rep_w * (rep_y - rep_pred) ** 2).mean()
                    total_loss = total_loss + self.beta_replay * replay_loss_val

                total_loss.backward()
                optimizer.step()

                # Book-keeping
                sum_total += total_loss.item()
                sum_task += task_loss.item()
                sum_ewc += ewc_penalty.item()
                sum_replay += (replay_loss_val.item()
                               if isinstance(replay_loss_val, torch.Tensor)
                               else replay_loss_val)
                n_batches += 1

            # ---- Print every 10 epochs ----
            if (epoch + 1) % 10 == 0:
                nb = max(n_batches, 1)
                print(f"  Task {task_id} | Epoch {epoch + 1:3d}/{epochs} | "
                      f"Total: {sum_total / nb:.4f}  | "
                      f"Task: {sum_task / nb:.4f}  | "
                      f"EWC: {sum_ewc / nb:.6f}  | "
                      f"Replay: {sum_replay / nb:.4f}")

        # ==============  POST-TRAINING  BOOK-KEEPING  ==============

        # (d) Fisher Information Matrix
        print(f"  [Task {task_id}] Computing diagonal Fisher Information Matrix...")
        fisher_diag = self._compute_diagonal_fisher(train_loader)

        # (e) Update replay buffer
        print(f"  [Task {task_id}] Updating replay buffer with task data...")
        all_x, all_y = [], []
        for xb, yb in train_loader:
            all_x.append(xb)
            all_y.append(yb)
        all_x = torch.cat(all_x, dim=0)
        all_y = torch.cat(all_y, dim=0)
        self.replay_buffer.add(all_x, all_y, self.model)

        # (f) Store snapshot theta^(k*) alongside Fisher
        param_snapshot = copy.deepcopy(self.model.state_dict())
        self.ewc_tasks.append((fisher_diag, param_snapshot))

        print(f"  [Task {task_id}] Buffer size = {len(self.replay_buffer)}")
        print(f"  Task {task_id} complete.\n")
        return self.model

    # ------------------------------------------------------------------
    #  Evaluation
    # ------------------------------------------------------------------

    def evaluate(self, dataloader):
        """
        Compute RMSE on a dataset.

        Parameters
        ----------
            dataloader : evaluation DataLoader

        Returns
        -------
            float  -  RMSE (root mean squared error)
        """
        self.model.eval()
        preds_list, targets_list = [], []

        with torch.no_grad():
            for xb, yb in dataloader:
                xb = xb.to(self.device)
                p = self.model(xb).squeeze(-1).cpu()
                if yb.dim() > 1:
                    yb = yb.squeeze(-1)
                preds_list.append(p)
                targets_list.append(yb)

        all_pred = torch.cat(preds_list)
        all_tgt = torch.cat(targets_list)
        mse = nn.MSELoss()(all_pred, all_tgt).item()
        return float(np.sqrt(mse))

    def evaluate_all_tasks(self, task_loaders):
        """Return a list of RMSE values, one per task."""
        return [self.evaluate(loader) for loader in task_loaders]


# ============================================================================
#  4.  CONTINUAL  LEARNING  METRICS
# ============================================================================

def compute_cl_metrics(results_matrix, K):
    r"""
    Compute Backward Transfer, Average Accuracy, and Forward Transfer.

    Convention:  R = -RMSE  (higher is better, consistent with
    classification accuracy).  All formulas below follow the paper.

    Parameters
    ----------
        results_matrix : 2-D list  results[t][k] = RMSE on task *k*
                         after training on tasks 0 ... t-1.
                         Row 0 = random-model baseline.
        K              : total number of tasks

    Returns
    -------
        dict with keys  'BWT', 'AA', 'FWT', 'RMSE_per_task', 'Remembered'.

    Formulas
    --------
        BWT = (1/(K-1)) * sum_{k=1}^{K-1} (R_{K,k} - R_{k,k})

        AA  = (1/K) * sum_{k=1}^{K} R_{K,k}

        FWT = (1/(K-1)) * sum_{k=2}^{K} (R_{k-1,k} - R_{0,k})

    With 0-based indexing the summation bounds shift accordingly.
    """
    # Build the R matrix  (R = -RMSE, higher is better)
    R = np.zeros((K + 1, K))
    for t in range(K + 1):
        for k in range(min(t + 1, K)):
            R[t][k] = -results_matrix[t][k]

    # ---- Backward Transfer (BWT) ----
    # BWT = (1/(K-1)) * sum_{k=0}^{K-2} (R[K][k] - R[k+1][k])
    bwt_sum = 0.0
    for k in range(K - 1):
        bwt_sum += R[K][k] - R[k + 1][k]
    bwt = bwt_sum / max(K - 1, 1)

    # ---- Average Accuracy (AA) ----
    # AA = (1/K) * sum_{k=0}^{K-1} R[K][k]
    aa = float(np.mean([R[K][k] for k in range(K)]))

    # ---- Forward Transfer (FWT) ----
    # FWT = (1/(K-1)) * sum_{k=1}^{K-1} (R[k][k] - R[0][k])
    fwt_sum = 0.0
    for k in range(1, K):
        fwt_sum += R[k][k] - R[0][k]
    fwt = fwt_sum / max(K - 1, 1)

    # Per-task detail
    remembered = []
    for k in range(K):
        rmse_imm = results_matrix[k + 1][k]    # RMSE right after learning
        rmse_fin = results_matrix[K][k]        # RMSE after all tasks
        delta = rmse_fin - rmse_imm             # positive => forgetting
        remembered.append((k, rmse_imm, rmse_fin, delta))

    return {
        'BWT': bwt,
        'AA': aa,
        'FWT': fwt,
        'RMSE_per_task': [results_matrix[K][k] for k in range(K)],
        'Remembered': remembered,
    }


# ============================================================================
#  5.  SYNTHETIC  DATA  GENERATION
# ============================================================================

def generate_synthetic_tasks(n_tasks=5, n_samples=500,
                              input_dim=5, test_ratio=0.2,
                              batch_size=32, seed=42):
    r"""
    Generate *n_tasks* sequential regression tasks.

    Each task follows  y = w^T x + N(0, 0.1^2)  with a different
    coefficient vector **w** to simulate task distribution shift.

    Parameters
    ----------
        n_tasks    : number of tasks (default 5)
        n_samples  : samples per task (default 500)
        input_dim  : feature dimension (default 5)
        test_ratio : fraction held out for testing (default 0.2)
        batch_size : DataLoader batch size (default 32)
        seed       : reproducibility (default 42)

    Returns
    -------
        list of dicts, each with  'train_loader', 'test_loader',
        'coefficients'.
    """
    rng = np.random.RandomState(seed)
    torch.manual_seed(seed)

    # Distinct coefficient vectors (enough for > 5 tasks)
    _coeff_bank = [
        [ 2.0,  3.0, -1.0,  0.5, -1.0],   # Task 0
        [-1.0,  2.0,  3.0, -1.0,  0.5],   # Task 1
        [ 0.5, -2.0,  1.0,  3.0, -1.0],   # Task 2
        [ 1.0,  1.0, -3.0,  2.0,  0.5],   # Task 3
        [-2.0,  1.0,  1.0, -0.5,  3.0],   # Task 4
        [ 3.0, -1.5,  0.5,  1.0, -2.0],   # Task 5
        [-0.5,  2.5, -2.0,  1.5,  1.0],   # Task 6
        [ 1.5, -1.0,  2.5, -1.5,  0.5],   # Task 7
        [ 2.5,  0.5, -0.5, -2.0,  1.5],   # Task 8
        [-1.5,  1.5,  1.5,  0.5, -2.5],   # Task 9
    ]

    noise_std = 0.1
    tasks = []

    for t in range(n_tasks):
        coeffs = np.array(_coeff_bank[t % len(_coeff_bank)], dtype=np.float32)
        X = rng.randn(n_samples, input_dim).astype(np.float32)
        y = (X @ coeffs + rng.randn(n_samples) * noise_std).astype(np.float32)

        # Train / test split
        n_test = int(n_samples * test_ratio)
        perm = rng.permutation(n_samples)
        tr_idx, te_idx = perm[:-n_test], perm[-n_test:]

        train_ds = TensorDataset(torch.tensor(X[tr_idx]),
                                  torch.tensor(y[tr_idx]))
        test_ds = TensorDataset(torch.tensor(X[te_idx]),
                                 torch.tensor(y[te_idx]))

        tasks.append({
            'train_loader': DataLoader(train_ds, batch_size=batch_size,
                                       shuffle=True),
            'test_loader': DataLoader(test_ds, batch_size=batch_size,
                                      shuffle=False),
            'coefficients': coeffs,
        })
        print(f"  Task {t}: w = {coeffs.tolist()},  "
              f"train={len(tr_idx)}, test={n_test}")

    return tasks


# ============================================================================
#  6.  MAIN  DEMONSTRATION
# ============================================================================

def main():
    """
    Demonstrate EWC-IXER on **5** synthetic continual-learning tasks.

    Procedure
    ---------
    1. Generate 5 sequential regression tasks (different linear mappings).
    2. Evaluate the *random* model on every task  (R_0,k  for FWT).
    3. For each task  k = 0 ... 4:
       a. Train with EWC-IXER.
       b. Evaluate on **all** tasks.
    4. Print RMSE per task and compute BWT / AA / FWT.
    """
    # ---------- configuration ----------
    SEED = 42
    N_TASKS = 5
    N_SAMPLES = 500
    INPUT_DIM = 5
    EPOCHS = 100
    LR = 0.001
    BATCH_SIZE = 32
    LAMBDA_EWC = 500.0
    BETA_REPLAY = 0.5
    BUFFER_SIZE = 200
    EWC_DAMPING = 1e-4
    DEVICE = 'cpu'

    np.random.seed(SEED)
    torch.manual_seed(SEED)

    print("=" * 65)
    print("  EWC-IXER  (Elastic Weight Consolidation +")
    print("             Importance-Weighted Experience Replay)")
    print("=" * 65)
    print(f"\n  Config:  tasks={N_TASKS}  samples={N_SAMPLES}  dim={INPUT_DIM}")
    print(f"          epochs={EPOCHS}  lr={LR}  batch={BATCH_SIZE}")
    print(f"          lambda(EWC)={LAMBDA_EWC}  beta(replay)={BETA_REPLAY}")
    print(f"          buffer={BUFFER_SIZE}  damping={EWC_DAMPING}  device={DEVICE}")

    # ---------- generate tasks ----------
    print(f"\n  Generating {N_TASKS} synthetic regression tasks...")
    tasks = generate_synthetic_tasks(n_tasks=N_TASKS, n_samples=N_SAMPLES,
                                      input_dim=INPUT_DIM,
                                      batch_size=BATCH_SIZE, seed=SEED)
    task_test_loaders = [t['test_loader'] for t in tasks]

    # ---------- create agent ----------
    agent = EWCIXERAgent(input_dim=INPUT_DIM,
                         lambda_ewc=LAMBDA_EWC,
                         beta_replay=BETA_REPLAY,
                         lr=LR,
                         buffer_size=BUFFER_SIZE,
                         ewc_damping=EWC_DAMPING,
                         device=DEVICE)
    print(f"\n  Model : MLPPredictor(5 -> 32 -> 1)")
    print(f"  Parameters : {agent.count_parameters()}  (expected 225)")

    # ---------- results matrix ----------
    # results[eval_step][task_k] = RMSE
    # eval_step 0 = random model;  eval_step t = after tasks 0..t-1
    results = []

    # Random-model baseline (R_0,k for all k)
    print("\n  Evaluating random model on all tasks...")
    random_rmse = agent.evaluate_all_tasks(task_test_loaders)
    results.append(random_rmse)
    print(f"  Random RMSE: {[f'{r:.4f}' for r in random_rmse]}")

    # ---------- sequential training ----------
    for t in range(N_TASKS):
        agent.train_on_task(task_id=t,
                            train_loader=tasks[t]['train_loader'],
                            epochs=EPOCHS,
                            batch_size=BATCH_SIZE)

        # Evaluate on ALL tasks (including unseen - useful for FWT)
        all_rmse = agent.evaluate_all_tasks(task_test_loaders)
        results.append(all_rmse)
        print(f"  Post-Task {t} RMSE: {[f'{r:.4f}' for r in all_rmse]}")

    # ---------- compute & report metrics ----------
    print(f"\n{'=' * 65}")
    print(f"  FINAL  EVALUATION")
    print(f"{'=' * 65}")

    metrics = compute_cl_metrics(results, N_TASKS)

    print(f"\n  RMSE per task (after all {N_TASKS} tasks):")
    for k, rmse in enumerate(metrics['RMSE_per_task']):
        print(f"    Task {k}: RMSE = {rmse:.4f}")

    print(f"\n  Per-Task Forgetting Analysis:")
    print(f"    {'Task':<8}{'RMSE@Learn':<16}{'RMSE@Final':<16}{'Delta':<12}")
    print(f"    {'-' * 52}")
    for tid, rmse_imm, rmse_fin, delta in metrics['Remembered']:
        sign = '+' if delta >= 0 else ''
        print(f"    {tid:<8}{rmse_imm:<16.4f}{rmse_fin:<16.4f}{sign}{delta:<11.4f}")

    print(f"\n  Continual Learning Metrics:")
    print(f"    Average Accuracy  (AA) : {metrics['AA']:.4f}")
    print(f"    Backward Transfer (BWT): {metrics['BWT']:.4f}")
    print(f"    Forward Transfer  (FWT): {metrics['FWT']:.4f}")

    print(f"\n  Interpretation:")
    if metrics['BWT'] > 0:
        print("    * BWT > 0 => positive backward transfer (improvement on past tasks)")
    else:
        print("    * BWT <= 0 => negative backward transfer (forgetting of past tasks)")
    if metrics['FWT'] > 0:
        print("    * FWT > 0 => prior knowledge helped new-task learning")
    else:
        print("    * FWT <= 0 => no positive forward transfer observed")

    print(f"\n{'=' * 65}")
    print(f"  EWC-IXER demonstration complete.")
    print(f"{'=' * 65}")

    return agent, metrics, results


# ============================================================================
if __name__ == '__main__':
    agent, metrics, results = main()
