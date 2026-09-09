# Research Proposal: Topic 7
## The Shape of Failure: Topological Data Analysis (TDA) for Early Voltage Collapse Detection

### 1. Introduction & Motivation
Power system stability assessment typically uses **geometric metrics** (Singular Value Decomposition of the Jacobian). These metrics are computationally expensive ($O(N^3)$) and often drop sharply only *seconds* before voltage collapse (bifurcation), giving operators little warning.
**Research Gap**: Existing Graph Neural Networks (GNNs) capture local connectivity but fail to detect global *topological* holes or voids in the stability manifold that precede physical collapse.
**Proposed Solution**: Use **Topological Data Analysis (TDA)**, specifically **Persistent Homology**, to extract algebraic topological invariants (Betti Numbers) from real-time Wide-Area Measurement System (WAMS) data. These features detect the "birth" of instability voids in the voltage landscape *minutes* before the Jacobian becomes singular.

### 2. Detailed Mathematical Framework
We define a filtration on the grid graph $G=(V,E)$ based on voltage potentials.

**Filtration Function**:
Let $f: V \to \mathbb{R}$ be the voltage magnitude at each bus. We construct a **Sublevel Set Filtration**:
$$ G_t = \{ v \in V \mid f(v) \le t \} $$
As the threshold $t$ varies, subgraphs $G_t$ appear and merge.

**Homological Invariants (Betti Numbers)**:
- $\beta_0$: Number of connected components (Islands of low voltage).
- $\beta_1$: Number of cycles/holes (Voltage depression pockets surrounding healthy areas).

**Persistence Diagram**: This tracks the lifespan $(b_i, d_i)$ of each topological feature $i$ (born at $b_i$, dies at $d_i$).
**Peristence Landscape**: We transform the diagram into a vector function $\lambda: \mathbb{N} \times \mathbb{R} \to \mathbb{R}$ to make it suitable for Neural Network input.
$$ \text{TDA Index} = || \lambda(t) ||_p $$

### 3. Implementation Roadmap

#### Phase 1: Manifold Data Generation (Months 1-2)
- **Objective**: Generate grid snapshots tracing the path to collapse.
- **Tool**: PyPower with **Continuation Power Flow (CPF)**.
- **System**: IEEE 118-Bus (3 zones) and IEEE 300-Bus.
- **Method**:
    - Select load buses and increase $P_{load}, Q_{load}$ iteratively.
    - Solve Power Flow until convergence fails (Point of Collapse - PoC).
    - Save 500 snapshots along the P-V curve (stable $\to$ critical $\to$ collapse).
- **Data Volume**: 5,000 collapse trajectories (2.5M snapshots).

#### Phase 2: Topological Feature Extraction (Months 3-4)
- **Library**: `Gudhi` (C++) or `Ripser` (Python bindings) for speed.
- **Process**:
    - For each snapshot (vector of 118 voltages):
    - Compute Rips Filtration.
    - Calculate Persistence Diagram.
    - Vectorize into **Persistence Image** ($20 \times 20$ pixel grid).
- **Visualization**: Plot the evolution of $\beta_1$ (holes) as the system moves towards the "nose" of the P-V curve.

#### Phase 3: Early Warning Detector (Months 5-6)
- **Model**: **Topological CNN** (Topo-CNN).
    - Input: Persistence Image (Topology) + Raw Adjacency Matrix (Geometry).
    - Layers: Conv2D layers extracting shape features from the Persistence Image.
    - Output: **Load Margin Prediction** (Distance to collapse in MW).
- **Validation**: Compare against **L-Index** and **Voltage Stability Margin (VSM)**.

### 4. Key Deliverables & Metrics
| Deliverable | Description | Success Metric |
| :--- | :--- | :--- |
| **Collapse Manifold Dataset** | P-V curve traces for IEEE 118/300 | Validated nose points |
| **TDA Pipeline** | Code to valid Betti numbers from WAMS | Computation < 50ms per snapshot |
| **Detector Model** | Topo-CNN for margin prediction | Warning 10 mins before L-Index |
| **IEEE Paper** | Draft for IEEE Trans. Smart Grid | Acceptance |

### 5. Risk Assessment & Mitigation
- **Risk**: TDA computation is slow for large graphs ($N > 1000$).
    - **Mitigation**: Use "Witness Complex" or sparse filtrations to reduce complexes size.
- **Risk**: Topological signals are noisy due to measurement error.
    - **Mitigation**: Use "Stability Theorem of Persistence Diagrams" - small noise only moves points slightly.

### 6. Resources & References
- **Libraries**: `gudhi`, `scikit-tda`, `pypower`
- **Key Theory**: "Topological Data Analysis for Power Systems" (IEEE papers are rare, opportunity).
- **Key Math**: Edelsbrunner & Harer, "Computational Topology: An Introduction".
