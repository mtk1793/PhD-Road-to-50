# Research Proposal: Topic 8
## Neuro-Symbolic AI: Differentiable Logic for Protection Coordination

### 1. Introduction & Motivation
Deep Learning (DL) models are increasingly proposed for power system fault detection. However, DL models are probabilistic and "black boxes," making them unsuitable for safety-critical **protection relaying** where strict adherence to logic rules (grid codes) is mandatory.
**Research Gap**: There is no existing framework that combines the speed and pattern recognition of Deep Learning with the **provable guarantees** of symbolic logic (Boolean satisfiability) for grid protection.
**Proposed Solution**: A **Neuro-Symbolic Agent** that integrates a Differentiable Logic Layer (e.g., SatNet or MAX-SAT). The neural network perceives the waveform, while the logic layer enforces hard constraints like "If current > 500A AND Zone 2 Timer > 300ms THEN Trip Breaker B".

### 2. Detailed Mathematical Framework
We define the problem as learning a function $f_\theta(x) \to y$ subject to a set of logical constraints $\phi(y) = \text{True}$.

**Joint Loss Function**:
$$ \mathcal{L}(\theta) = \underbrace{\text{CrossEntropy}(f_\theta(x), y_{true})}_{\text{Accuracy}} + \lambda \underbrace{\mathcal{L}_{logic}(f_\theta(x), \phi)}_{\text{Consistency}} $$

**Differentiable Logic (MAX-SAT Relaxation)**:
We map boolean variables $y_i \in \{0, 1\}$ to continuous probabilities $p_i \in [0, 1]$.
A clause $C_j = y_1 \lor \neg y_2$ is satisfied if $\max(p_1, 1-p_2) \approx 1$.
We use a **Semidefinite Programming (SDP)** relaxation (as in SatNet) to backpropagate gradients *through* the logic solver:
$$ \frac{\partial \mathcal{L}}{\partial \theta} = \frac{\partial \mathcal{L}}{\partial y^*} \cdot \frac{\partial y^*}{\partial \theta} $$
where $y^*$ is the solution to the satisfiability problem.

### 3. Implementation Roadmap

#### Phase 1: Protective Relay Simulation (Months 1-2)
- **Objective**: Create a dataset of faults and "correct" relay operations.
- **Tool**: PyPower (using $Z_{bus}$ impedance matrix for Short Circuit Analysis).
- **System**: IEEE 33-Bus Radial Distribution System.
- **Scenarios**:
    - Fault Types: L-G, L-L, L-L-G, 3-Phase.
    - Impedances: $0.01\Omega$ to $50\Omega$ (High Impedance Faults).
    - Locations: Every 5% of line length.
- **Output**: 50,000 cases. Input: Current/Voltage phasors. Output: Trip/No-Trip Decisions for Breakers B1-B33.

#### Phase 2: Neuro-Symbolic Architecture (Months 3-4)
- **Perception Module**:
    - 1D-CNN (ResNet-18 modified for 1D time-series).
    - Input: raw current waveforms sampled at 128 samples/cycle.
    - Output: Fault Class Probabilities (A-G, B-C, etc.).
- **Symbolic Module**:
    - Library: `SatNet` (runs on GPU) or `cvxpylayers`.
    - Logic Rules encoded as CNF (Conjunctive Normal Form).
    - Example Rule: `Trip_B2 implies (Fault_Loc_Zone2 AND Timer_Expired)`.

#### Phase 3: Verification & Hardware-in-Loop (Months 5-6)
- **Training**: Train end-to-end minimizing the joint loss.
- **Verification**: Run an SMT solver (Z3) on the trained model's output to formally prove that no illegal trip commands can be issued for a defined set of inputs.
- **Comparison**: Compare Neural-Only accuracy vs. Neuro-Symbolic consistency. Show that Neural-Only achieves 99% accuracy but 5% logic violations, while Neuro-Sym achieves 98.5% accuracy but 0% logic violations.

### 4. Key Deliverables & Metrics
| Deliverable | Description | Success Metric |
| :--- | :--- | :--- |
| **Fault-Waveform DB** | 50k short-circuit simulations | Accurate per IEEE definition |
| **NeuroSym Logic Code** | Python implementation of Relay Logic | 100% Satisfiability |
| **Integrated Agent** | PyTorch + SatNet model | Logic Violation Rate < 0.1% |
| **IEEE Paper** | Draft for IEEE Trans. Power Delivery | Acceptance |

### 5. Risk Assessment & Mitigation
- **Risk**: Training convergence is unstable with logic layers.
    - **Mitigation**: Use "Curriculum Learning" - train Perception first, then turn on Logic Loss.
- **Risk**: Logic solver is too slow for real-time (should be < 4ms).
    - **Mitigation**: Use a distilled "Student" network that approximates the "Teacher" solver for deployment.

### 6. Resources & References
- **Libraries**: `satnet`, `z3-solver`, `cvxpylayers`, `pypower`
- **Key Paper**: "SatNet: Bridging deep learning and logical reasoning using a differentiable satisfiability solver" (ICML 2019).
- **Key Standard**: IEEE C37.112 (Inverse-Time Overcurrent Relays).
