# Research Proposal: Topic 10
## Zero-Shot N-k Contingency Screening via Deep Operator Learning (DeepONet)

### 1. Introduction & Motivation
Transmission System Operators (TSOs) must ensure the grid remains safe even if $k$ components fail (N-k security). Standard screening involves running Newton-Raphson (AC-OPF) for thousands of contingency scenarios, which is prohibitively slow for real-time assessment ($k \ge 2$). Use of "DC Power Flow" approximations sacrifices accuracy for speed.
**Research Gap**: Standard ML models (CNNs) are **resolution-dependent** and **topology-rigid**. If a new line is added or the grid discretization changes, the model must be retrained.
**Proposed Solution**: Use **Deep Operator Networks (DeepONet)** to learn the infinite-dimensional **solution operator** of the Power Flow PDEs. Once trained, the DeepONet acts as a super-fast physics solver that generalizes "Zero-Shot" to new load distributions and N-k topology changes without retraining.

### 2. Detailed Mathematical Framework
Let $D$ be the physical domain of the grid. We want to find the operator $\mathcal{G}$ such that:
$$ \mathcal{G}(u) = v $$
Input $u(x)$: Power injection profile (Load/Gen).
Output $v(x)$: Voltage magnitude profile.
Governing Physics: $\nabla \cdot (V \nabla V) = S \implies \mathcal{L}(v) = u$.

**DeepONet Architecture**:
Approximates $\mathcal{G}(u)(y)$ for any query point $y \in D$ (bus or line location):
$$ \mathcal{G}(u)(y) \approx \sum_{k=1}^{p} \underbrace{b_k(u_1, \dots, u_m)}_{\text{Branch Net}} \cdot \underbrace{t_k(y)}_{\text{Trunk Net}} + b_0 $$
- **Branch Net**: Encodes the grid state functions (Loads/Topologies).
- **Trunk Net**: Encodes the grid geometry (Positional Embeddings).

### 3. Implementation Roadmap

#### Phase 1: Function Space Sampling (Months 1-2)
- **Objective**: Create a dataset of operators, not just vectors.
- **Tool**: PyPower.
- **System**: IEEE 118-Bus (Standard) and 300-Bus (Scale).
- **Sampling**:
    - **Inputs ($u$)**: Generate 50,000 random load profiles using **Gaussian Random Fields** (GRF) to ensure spatial correlation (smoothness), which improves operator learning.
    - **Topologies**: For each load profile, apply random line outages (N-0, N-1, N-2). Mask the adjacency matrix.
    - **Outputs ($v$)**: Solve full AC Power Flow for each sample.
- **Data**: Pairs of $\{ (P_{load}, A_{adj}), V_{complex} \}$.

#### Phase 2: DeepONet Training (Months 3-4)
- **Library**: `DeepXDE` (Scientific ML library).
- **Architecture**:
    - Branch: PointNet or GNN (to handle permutation invariance of the grid graph).
    - Trunk: Sine-activation MLP (SIREN) for better gradients.
- **Loss**:
    - Data Loss: MSE between predicted voltages and PyPower truth.
    - **Physics Loss (PINN)**: Evaluate power mismatch residuals at grid nodes.
    $$ \mathcal{L} = \mathcal{L}_{data} + \lambda \mathcal{L}_{physics} $$

#### Phase 3: Benchmarking N-k Screening (Months 5-6)
- **Task**: Screen 10,000 random N-2 contingencies.
- **Baseline**: 
    1. PyPower `runpf` (Newton-Raphson).
    2. DC Power Flow (Linear approx).
    3. Standard ResNet (Image-based).
- **Metrics**:
    - **Speedup**: Goal is > 1000x faster than Newton-Raphson.
    - **Accuracy**: Violations detected vs. False Positives.
    - **Generalization**: Evaluate on a *modified* IEEE 118-bus system (add new lines) without retraining.

### 4. Key Deliverables & Metrics
| Deliverable | Description | Success Metric |
| :--- | :--- | :--- |
| **Operator Dataset** | 50k GRF Load Profiles + PF solutions | Validated distributions |
| **DeepONet Model** | Branch/Trunk architecture in DeepXDE | Training Error < 0.1% |
| **Screening Tool** | Python script for N-k assessment | > 10,000 cases/sec |
| **IEEE Paper** | Draft for IEEE Trans. Power Systems | Acceptance |

### 5. Risk Assessment & Mitigation
- **Risk**: DeepONet struggles with high-frequency components (sharp voltage drops).
    - **Mitigation**: Use "Fourier Feature Embeddings" in the Trunk net.
- **Risk**: Generalization to completely different mesh topologies is hard.
    - **Mitigation**: Use Graph Neural Operator (GNO) variant which is strictly discretization-invariant.

### 6. Resources & References
- **Libraries**: `DeepXDE`, `neuralop`, `pypower`, `scikit-learn`
- **Key Paper**: "DeepONet: Learning nonlinear operators for identifying differential equations based on the universal approximation theorem" (Nature MI, 2021).
- **Key Paper**: "Learning the Power Flow Operator" (arXiv 2023).
