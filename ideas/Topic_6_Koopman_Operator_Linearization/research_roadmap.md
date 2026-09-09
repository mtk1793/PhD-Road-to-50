# Research Proposal: Topic 6
## Infinite-Dimensional Koopman Operator Linearization for Data-Driven Grid Control

### 1. Introduction & Motivation
Current power system control relies on **Jacobian linearization** (small-signal stability), which creates a linear approximation around a single operating point. This fails during large disturbances (transient stability), where the non-linear dynamics of synchronous generators and inverters dominate.
**Research Gap**: Deep Learning (RNN/LSTM) can model non-linearities but lacks control-theoretic guarantees (stability, optimality).
**Proposed Solution**: Use **Koopman Operator Theory** to find a coordinate transformation $\psi(x)$ where the non-linear dynamics $x_{t+1} = f(x_t)$ become globally linear $z_{t+1} = K z_t$. This enables the use of fast, convex **Model Predictive Control (MPC)** on the linear latent space to stabilize the grid during faults.

### 2. Detailed Mathematical Framework
The Koopman Operator $\mathcal{K}$ is an infinite-dimensional linear operator acting on observable functions $g$:
$$ \mathcal{K}g(x_t) = g(f(x_t)) $$

We approximate this finite-dimensionally using a **Deep Auto-Encoder**:
- **Encoder (Lifting Function)**: $z_t = \psi(x_t; \theta_{enc})$
- **Dynamics (Koopman Matrix)**: $z_{t+1} = K(\theta_{K}) z_t + B(\theta_{B}) u_t$
- **Decoder (Reconstruction)**: $\hat{x}_t = \phi(z_t; \theta_{dec})$

**Training Objective**:
$$ \min_{\theta} \sum_{t} \underbrace{||x_{t+1} - \hat{x}_{t+1}||^2}_{\text{Reconstruction}} + \lambda_1 \underbrace{||z_{t+1} - (K z_t + B u_t)||^2}_{\text{Linear Prediction}} + \lambda_2 \underbrace{||z_t - \psi(\phi(z_t))||^2}_{\text{Consistency}} $$

### 3. Implementation Roadmap

#### Phase 1: High-Fidelity Data Generation (Months 1-2)
- **Objective**: Generate a dense dataset of non-linear grid trajectories.
- **Tool**: PyPower (extended with `run_dynamics` or stepwise `runpf`).
- **System**: IEEE 39-Bus (New England System) - highly prone to inter-area oscillations.
- **Scenarios**:
    - Load Steps: Random $\pm 20\%$ changes at 1000 locations.
    - Faults: 3-phase short circuits at lines 4-14, 16-19 (critical corridors).
    - Duration: 20 seconds at 60Hz (1200 steps per trajectory).
- **Data Volume**: 10,000 trajectories. Total samples $\approx 1.2 \times 10^7$.

#### Phase 2: Deep Koopman Training (Months 3-5)
- **Architecture**:
    - Input: $x = [V, \theta, \omega]$ (Voltage, Angle, Frequency) $\in \mathbb{R}^{117}$.
    - Encoder: 4-layer MLP with Swish activation. Hidden dims: [256, 128, 64].
    - Lifted State: $z \in \mathbb{R}^{64}$ (Dimension > Input Dimension to unravel non-linearity).
    - Koopman Matrix $K$: Constrained to be stable ($\rho(K) \le 1$) during training via parameterization.
- **Validation**:
    - N-step prediction error vs. PyPower ground truth.
    - Eigenvalue analysis: Do the learned eigenvalues of $K$ match the electromechanical modes of the physics?

#### Phase 3: Koopman-MPC Design (Months 6-7)
- **Control Law**:
$$ \min_{u_0, \dots, u_{N-1}} \sum_{k=0}^{N-1} (z_k^T Q z_k + u_k^T R u_k) $$
$$ \text{s.t. } z_{k+1} = K z_k + B u_k, \quad u_{min} \le u_k \le u_{max} $$
- **Solver**: **OSQP** (Operator Splitting Quadratic Program) - solves in microseconds.
- **Integration**: At each time step $t$, encode measurement $x_t \to z_t$, solve QP for $u^*$, apply to PyPower.

### 4. Key Deliverables & Metrics
| Deliverable | Description | Success Metric |
| :--- | :--- | :--- |
| **GridKoopman Dataset** | 10k trajectories of IEEE 39-bus | Validated against PSSE |
| **Model Codebase** | PyTorch implementation of Deep Koopman | Prediction Error < 1% over 5 seconds |
| **Controller** | Python-based MPC (cvxpy/OSQP) | Stabilize Critical Clearing Time (CCT) +50ms |
| **IEEE Paper** | Draft for IEEE Trans. Power Systems | Acceptance |

### 5. Risk Assessment & Mitigation
- **Risk**: "Curse of Dimensionality" - $K$ matrix becomes too large.
    - **Mitigation**: Use Block-Diagonal Koopman Operator (decouple grid areas).
- **Risk**: Koopman invariant subspace does not exist.
    - **Mitigation**: Add "forcing" terms or use Extended DMD (EDMD) with dictionary learning.
- **Risk**: PyPower dynamic simulation is slow.
    - **Mitigation**: Parallelize data gen across 64 CPU cores.

### 6. Resources & References
- **Libraries**: `deep-koopman`, `cvxpy`, `pypower`, `torch`
- **Key Paper**: "Deep learning for universal linear embeddings of nonlinear dynamics" (Lusch et al., Nature Comm 2018).
- **Key Paper**: "Koopman Operator-Based Model Predictive Control for Power System Stability" (IEEE Access, 2021).
