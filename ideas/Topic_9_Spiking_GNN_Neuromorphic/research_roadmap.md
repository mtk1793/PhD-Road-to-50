# Research Proposal: Topic 9
## Ultra-Low Power Edge Intelligence: Event-Driven Spiking Graph Neural Networks (S-GNN)

### 1. Introduction & Motivation
Standard Artificial Neural Networks (ANNs) are frame-based and require continuous, energy-intensive Matrix-Multiply-Accumulate (MAC) operations. This creates a bottleneck for **grid edge intelligence** (e.g., IoT smart meters, distributed sensors) which have strict power budgets (< 1 Watt).
**Research Gap**: Grid anomalies (faults) are sparse events in time. Processing continuous waveforms when "nothing is happening" is wasteful.
**Proposed Solution**: Utilize **Spiking Neural Networks (SNNs)** on neuromorphic principles. SNNs remain "silent" (consuming micro-watts) and only compute/spike when a relevant event is triggered by a change in grid state ($|V_t - V_{t-1}| > \delta$). We propose a Spiking Graph Neural Network (S-GNN) to learn spatial dependencies efficiently.

### 2. Detailed Mathematical Framework
We model the grid as a graph where nodes are Leaky Integrate-and-Fire (LIF) neurons.

**LIF Neuron Dynamics**:
The membrane potential $u_i(t)$ of neuron $i$ is described by the differential equation:
$$ \tau \frac{du_i(t)}{dt} = -(u_i(t) - u_{rest}) + I_{in}(t) $$
where $I_{in}(t) = \sum_{j \in \mathcal{N}(i)} w_{ij} \cdot S_j(t)$ is the synaptic current from neighbors.

**Spike Generation**:
$$ S_i(t) = \begin{cases} 1 & \text{if } u_i(t) \ge V_{th} \\ 0 & \text{otherwise} \end{cases} $$
After a spike, $u_i(t)$ is reset to $u_{rest}$.

**Learning Rule (Surrogate Gradient)**:
Since the spike function is non-differentiable, we use a surrogate gradient for backpropagation (e.g., sigmoid derivative):
$$ \frac{\partial S}{\partial u} \approx \sigma'(u) $$

### 3. Implementation Roadmap

#### Phase 1: Asynchronous Event Encoding (Months 1-2)
- **Objective**: Convert continuous PyPower simulation traces into sparse spike trains.
- **Tool**: PyPower (Dynamic Simulation mode).
- **Encoding Scheme**: **Delta Modulation (DM)**.
    - Monitor variable $x(t)$.
    - Generate positive spike if $x(t) \ge x_{last\_spike} + \delta$.
    - Generate negative spike if $x(t) \le x_{last\_spike} - \delta$.
- **Data**: IEEE 123-Bus Feeder. 10 minutes of operation. 99% Sparsity (activity factor < 0.01).

#### Phase 2: S-GNN Development (Months 3-4)
- **Library**: `SpikingJelly` or `snntorch` (PyTorch based).
- **Architecture**:
    - **S-GCN Layer**: Integrates spikes from neighbors over time $T$.
    - **Readout**: Integrate voltage over window $T$. If $\int V > Threshold \to$ Fault Detected.
- **Training**:
    - Loss: CrossEntropy on the accumulated membrane potential of the output class neuron.
    - Optimizer: Adam with Time-Through-Backpropagation (BPTT).

#### Phase 3: Energy Efficiency Benchmarking (Months 5-6)
- **Metric**: Synaptic Operations (SynOps).
    - ANN Cost: $N_{neurons} \times N_{inputs} \times 4.6 pJ$ (FP32 MAC).
    - SNN Cost: $N_{spikes} \times 0.9 pJ$ (Accumulate only).
- **Hardware Simulation**: Use **Intel Loihi** energy model or deploy to **Nvidia Jetson Nano** (measuring power draw).
- **Goal**: Demonstrate > 20x energy reduction for same accuracy.

### 4. Key Deliverables & Metrics
| Deliverable | Description | Success Metric |
| :--- | :--- | :--- |
| **Spiking Dataset** | Event-based encoding of grid faults | >99% Sparsity |
| **S-GNN Model** | Spiking Graph Model (PyTorch) | Accuracy > 95% on Fault Class |
| **Energy Report** | FLOPs vs SynOps Comparison | >20x Efficiency Gain |
| **IEEE Paper** | Draft for IEEE Trans. Emerging Topics in Comput. | Acceptance |

### 5. Risk Assessment & Mitigation
- **Risk**: "Vanishing Spikes" - activity dies out in deep layers.
    - **Mitigation**: Use BatchNorm for SNNs (Threshold Dependent Batch Normalization - TDBN).
- **Risk**: Training is extremely slow (time steps $T$).
    - **Mitigation**: Use small time windows ($T=16$) and "Direct Encoding".

### 6. Resources & References
- **Libraries**: `spikingjelly`, `snntorch`, `pypower`
- **Key Paper**: "Deep Learning With Spiking Neurons: The Equivalence of Specialized Spiking Models and ANNs" (Frontiers in Neurosci, 2018).
- **Key Hardware**: Intel Loihi, IBM TrueNorth (simulators available).
