# Topic 2: Cyber-Resilient AI for 45,000-Node V2G Demand Response Network
## Distributed Attack Detection at the Edge of NS's Electric Vehicle Revolution

**Status:** 🟢 Ready to Start  
**Timeline:** 4-5 months  
**Complexity:** ⭐⭐⭐⭐ (High - builds on existing Paper 1 & 3)  
**Industry Impact:** 🔥🔥🔥🔥🔥 (Critical - enables $200M+ V2G infrastructure deployment)

---

## 📌 Quick Summary

By 2030, Nova Scotia will have **45,000 electric vehicles** participating in Vehicle-to-Grid (V2G) demand response, creating:
- **450 MW aggregate controllable load** (26% of peak demand!)
- **80,000+ cyber attack endpoints** (each EV charger is a vulnerability)
- **Sub-100ms detection requirements** (faster than existing intrusion detection systems)
- **Privacy constraints** (EV owner data can't be centralized)

This paper presents a **Graph Convolutional LSTM (GC-LSTM)** framework with **blockchain-verified federated learning** that achieves:
- **<1% false positive rate** (10x better than signature-based IDS)
- **Sub-100ms detection latency** (meets real-time requirements)
- **Zero centralized data aggregation** (privacy-preserving)
- **Provable model integrity** (blockchain audit trail for regulators)

---

## 🎯 Core Innovation

### What's Novel?
1. **First GNN-based intrusion detection** for V2G networks at provincial scale (gap in literature)
2. **Blockchain-federated learning fusion:** Immutable model provenance + privacy preservation
3. **Edge deployment architecture:** GC-LSTM runs on charging station controllers (not cloud)
4. **Explainable AI for operators:** SHAP values identify compromised EVs + attack propagation paths

### Why It Matters?
- **Regulatory approval blocker:** NS UARB won't approve V2G tariffs without proven cybersecurity
- **Grid stability risk:** Coordinated 5,000 EV disconnect during peak = instant 150 MW load loss = blackout
- **Insurance requirement:** V2G deployments need <$5M cyber insurance → requires certified detection system
- **Customer trust:** One successful attack on EV charging data = public backlash kills V2G adoption

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│         Blockchain Network (Model Hash + Performance Audit)     │
│  (Immutable record for NERC CIP compliance & regulator review)  │
└────────────┬────────────────────────────────────┬────────────────┘
             │                                    │
    ┌────────▼─────────────────┐      ┌──────────▼────────────────┐
    │  Federated Aggregator    │      │   SHAP Explainability     │
    │  (FedAvg + Validation)   │      │   Engine (Cloud)          │
    └────────┬─────────────────┘      └───────────────────────────┘
             │
    ┌────────▼──────────────────────────────────────────────────┐
    │   450 Charging Station Edge Controllers (GC-LSTM Agents)  │
    │   Each monitors 50-100 EVs on local distribution feeder   │
    └────┬─────────────┬─────────────┬──────────────┬───────────┘
         │             │             │              │
    ┌────▼────┐  ┌────▼────┐  ┌─────▼───┐   ┌─────▼───┐
    │ EV 1-100│  │EV 101-  │  │ EV 201- │...│EV 44,901-│
    │ Halifax │  │ 200     │  │ 300     │   │ 45,000  │
    │ Downtown│  │ Bedford │  │ Dartmouth   │ Sydney  │
    └─────────┘  └─────────┘  └─────────┘   └─────────┘
```

---

## 🔬 Technical Approach

### Phase 1: Graph Construction (Distribution Feeder Topology)

**Graph Structure:**
- **Nodes:** EVs connected to charging stations
- **Edges:** Electrical connectivity via distribution transformer
- **Node Features (per EV, 15-min resolution):**
  - SOC (state of charge): 0-100%
  - Active power draw: kW
  - Reactive power: kVAr
  - Voltage at charging point: p.u.
  - Charging duration: minutes
  - V2G discharge flag: 0/1
  - **Anomaly score (self-supervised):** Deviation from historical profile

**Edge Weights:**
- Admittance between nodes (from distribution grid model)
- Stronger weights for EVs on same transformer = attacks propagate faster

**Why GNN over standard LSTM?**
- Coordinated attacks affect **spatially clustered** EVs (same feeder/transformer)
- GNNs natively capture spatial correlation → detect coordinated patterns
- Standard LSTM treats EVs independently → misses attack coordination

### Phase 2: GC-LSTM Attack Detection Model
**Builds on your Paper 1 (GC-LSTM Attack Detection)**

**Architecture:**
```
Input: 15-min sliding window (T=12 steps = 3 hours of history)
  ↓
Graph Convolution Layer (captures spatial attack spread)
  ↓
LSTM Layer (captures temporal attack evolution)
  ↓
Attention Layer (highlights critical features)
  ↓
Output: [Normal, FDI_SOC, Coordinated_Disconnect, Replay_Attack]
```

**Training:**
- **Normal data:** 80% (real EV charging profiles from Pecan Street dataset + NS driving patterns)
- **Attack data:** 20% (synthetic attacks injected)
  - **FDI on SOC:** 10-30% of EVs report false SOC (trick V2G scheduler)
  - **Coordinated disconnect:** 100-1000 EVs drop during peak demand
  - **Replay attack:** Replay yesterday's V2G schedule (stale attack)

**Loss Function:**
- Weighted cross-entropy (attacks are rare class)
- Focal loss to handle class imbalance
- False positive penalty: 10x weight (operator alert fatigue is critical problem)

### Phase 3: Federated Learning with Blockchain Audit
**Builds on your Paper 3 (Federated Meta-RL)**

**Why Federated?**
- **Privacy:** EV charging data reveals owner behavior (work location, sleep schedule) → can't centralize
- **Scalability:** 450 charging stations × 15-min uploads = 43,200 data transfers/day → federated reduces to 1/day
- **Regulatory:** Canadian privacy laws (similar to GDPR) restrict EV data aggregation

**Federated Protocol:**
1. Each charging station trains local GC-LSTM on local EVs (100 gradient steps)
2. Upload model weights θ_local to aggregator
3. Aggregator computes global model: `θ_global = FedAvg(θ_local)`
4. **Blockchain step:** Store hash(θ_global) + validation accuracy on-chain
5. Download θ_global and continue training

**Blockchain Benefits:**
- **Immutable audit trail:** Regulators verify no model backdoors
- **Model provenance:** Trace which charging stations contributed to current model
- **Performance guarantee:** On-chain accuracy = proof of detection capability
- **Attack resilience:** Model poisoning attacks detected via blockchain consensus

### Phase 4: Explainable AI for Operator Trust
**Critical for regulatory approval (NERC CIP-014 compliance)**

**SHAP (SHapley Additive exPlanations) Integration:**
When attack detected:
1. SHAP values identify which EV features triggered alert
   - Example: "EV #4523's SOC jumped 40% in 15 min (physically impossible)"
2. GNN attention weights show attack propagation path
   - Example: "Attack originated at Transformer T-47, spread to 12 downstream EVs"
3. Operator receives:
   - Alert: "Coordinated disconnect attack detected (confidence 87%)"
   - Root cause: "EV IDs #4501-4523 (Halifax downtown feeder)"
   - Recommended action: "Isolate feeder F-47, verify equipment manually"

**Why This Matters:**
- Operators **must understand** why alarm triggered (can't be black box)
- False alarms without explanation = system gets ignored after 2 weeks
- Regulatory agencies require "explainable cybersecurity" for critical infrastructure

---

## 📊 Datasets & Simulation

### EV Charging Data
**Primary Source:** Pecan Street Dataport (Austin, Texas)
- 1,000+ homes with EV charging data (15-min resolution)
- Features: kW draw, charging duration, time-of-day patterns
- **Limitation:** US data, need to adjust for NS climate (longer heating-related SOC drain in winter)

**Augmentation for NS:**
- Scale charging patterns to NS winter temperatures (-10°C vs. Austin 5°C)
- Reduce daytime charging (NS has less rooftop solar than Texas)
- Add rural driving patterns (longer commutes in rural NS)

### Attack Dataset Generation
**Building on your Paper 1 methodology:**

1. **False Data Injection (FDI) on SOC:**
   - Inject to 10-30% of EVs (random or clustered)
   - SOC bias: ±20-40% (enough to fool V2G scheduler)
   - Duration: 30 min to 6 hours

2. **Coordinated Disconnect:**
   - Select 100-1,000 EVs on same feeder
   - Simultaneous disconnect during peak (5-7 PM)
   - Models real adversary goal: maximize grid disruption

3. **Replay Attack:**
   - Record V2G schedule from Day D-1
   - Replay on Day D (weather/demand is different → causes imbalance)

4. **Denial-of-Service (DoS):**
   - Flood charging station controllers with requests
   - Causes 5-30 second communication delay
   - Detection via temporal anomaly (expected message missing)

**Dataset Size:**
- 45,000 EVs × 15-min samples × 365 days = 1.5 billion data points/year
- Training set: 6 months normal + 10% attack injection
- Test set: 3 months holdout (different attack variants)

### NS Distribution Grid Model
- **Base:** IEEE 123-bus test feeder (modified for NS urban/rural mix)
- **EV Integration:**
  - 300 EVs per feeder (urban Halifax)
  - 50 EVs per feeder (rural Cape Breton)
  - Total: ~450 charging stations across NS

---

## 🧪 Verification Plan

### Baseline Comparisons
1. **Signature-Based IDS (Snort)**
   - Detects known attack patterns only
   - Expected: High false negatives (misses novel attacks)

2. **Centralized LSTM (Privacy-Violating)**
   - All EV data aggregated to cloud
   - Upper bound performance (but violates privacy)

3. **Anomaly Detection (Isolation Forest)**
   - Unsupervised ML approach
   - Expected: High false positives (5-8%)

4. **Federated LSTM (No GNN)**
   - Shows benefit of graph structure
   - Expected: Misses coordinated attacks (treats EVs independently)

### Performance Metrics

**Detection Accuracy:**
- True Positive Rate (TPR): ≥95% (catch 95% of attacks)
- False Positive Rate (FPR): <1% (critical for operator trust)
- Detection Latency: <100ms (real-time requirement)
- Precision: ≥90% (when alarm triggers, it's real)

**Federated Learning:**
- Convergence rounds: ≤50 (faster = better)
- Communication cost: <10 MB/station/day
- Privacy leakage: Test gradient inversion attack (should fail)

**Explainability:**
- SHAP computation time: <5 seconds (fast enough for operator)
- Top-3 feature accuracy: ≥80% (SHAP identifies true attack features)

**Blockchain:**
- Model hash storage cost: <$0.10/model update (Ethereum gas fees)
- Consensus latency: <30 seconds (acceptable for hourly model updates)

### Ablation Studies
- Effect of graph structure (GNN vs. no graph)
- Federation rounds (10, 25, 50, 100)
- Attack injection rate (5%, 10%, 20%)
- Sliding window length (1 hr, 3 hr, 6 hr)

---

## 📈 Expected Results

### Performance Targets
- **vs. Signature-Based IDS:** +60-80% TPR (catches zero-day attacks)
- **vs. Centralized LSTM:** -3 to -7% TPR (acceptable privacy cost)
- **vs. Isolation Forest:** -70% FPR (10x fewer false alarms)
- **vs. Federated LSTM (no GNN):** +25-35% for coordinated attacks

### Key Figures for Paper
1. **ROC Curve:** TPR vs. FPR (show GC-LSTM dominates baselines)
2. **Attack Detection Timeline:** Show sub-100ms latency across attack types
3. **SHAP Explanation Example:** Visual of SOC FDI attack with highlighted features
4. **GNN Attention Heatmap:** Shows attack propagation through feeder topology
5. **Federated Convergence:** Model accuracy vs. federation rounds
6. **Privacy Attack Resistance:** Gradient inversion attack reconstruction error (should be high)
7. **Blockchain Audit Trail:** Screenshot of on-chain model hash + performance

---

## 💼 Industry Partnership Opportunities

### Primary Target: Nova Scotia Power + EV Charging Networks
**Pitch:**
- "We enable your 45,000 EV V2G rollout by solving the #1 regulatory blocker: cybersecurity"
- "Sub-1% false positives means operators actually trust the system"
- "Blockchain audit trail = instant NERC CIP compliance (saves 6-12 months regulatory approval)"

**Ask:**
- V2G pilot data (if available from 1,000 EV pilot mentioned in your optimization_results.json)
- Distribution grid topology (anonymized)
- Letter of support for conference/funding applications

### Secondary Targets
- **ChargePoint, Flo, Electrify Canada:** License as cybersecurity module for charging networks
- **Tesla, GM:** Certify as V2G-safe for vehicle warranties
- **Cyber Insurance Companies:** Reduce premiums for certified V2G deployments
- **NSERC / Mitacs:** Industry collaboration grant ($100K)

---

## 📝 Paper Structure (8-10 pages, IEEE format)

### Proposed Sections
1. **Introduction** (1.5 pages)
   - NS 45K EV target + V2G revenue opportunity
   - Cybersecurity as deployment blocker
   - GC-LSTM + blockchain as solution

2. **Related Work** (1 page)
   - IDS for smart grids (mostly signature-based)
   - GNN for cyber-physical systems (gap for V2G)
   - Federated learning for privacy (no blockchain integration yet)

3. **Threat Model** (1 page)
   - Adversary capabilities (FDI, coordinated disconnect, replay)
   - Attack impact on grid stability
   - Privacy constraints

4. **Proposed Method: GC-LSTM-Fed-Blockchain** (2.5 pages)
   - Graph construction (V2G network topology)
   - GC-LSTM architecture
   - Federated learning protocol
   - Blockchain audit integration
   - SHAP explainability

5. **Simulation Setup** (1 page)
   - Dataset (Pecan Street + NS adjustments)
   - Attack injection methodology
   - Baselines

6. **Results** (2 pages)
   - Detection accuracy (ROC curves)
   - Latency analysis
   - Explainability case studies
   - Ablation studies

7. **Discussion** (0.5 pages)
   - Deployment considerations (edge hardware requirements)
   - Regulatory compliance (NERC CIP-014)
   - Limitations (blockchain cost, federated convergence time)

8. **Conclusion** (0.5 pages)
   - Summary + future work (extend to V2B, V2H)

---

## ⏱️ Implementation Timeline

### Month 1: Data Preparation
- [ ] Week 1: Download Pecan Street EV charging dataset
- [ ] Week 2: Adjust for NS climate/driving patterns
- [ ] Week 3: Generate attack datasets (FDI, coordinated disconnect, replay)
- [ ] Week 4: Build 45K-node V2G graph structure (IEEE 123-bus scaled)

### Month 2: GC-LSTM Development
- [ ] Week 5: Adapt Paper 1 GC-LSTM code to V2G context
- [ ] Week 6: Train baseline GC-LSTM (centralized)
- [ ] Week 7: Implement baseline comparisons (Snort, Isolation Forest)
- [ ] Week 8: Verify detection performance ≥90% TPR, <5% FPR

### Month 3: Federated Learning Integration
- [ ] Week 9: Implement FedAvg protocol for GC-LSTM
- [ ] Week 10: Add differential privacy (if needed)
- [ ] Week 11: Train federated GC-LSTM (450 charging stations)
- [ ] Week 12: Benchmark vs. centralized

### Month 4: Blockchain & Explainability
- [ ] Week 13: Integrate blockchain (Ethereum testnet or Hyperledger)
- [ ] Week 14: Store model hashes + performance on-chain
- [ ] Week 15: Implement SHAP explainability module
- [ ] Week 16: Generate attack case studies with explanations

### Month 5: Paper Writing & Refinement
- [ ] Week 17-18: Draft manuscript
- [ ] Week 19: Run final ablation studies
- [ ] Week 20: Internal review + revisions

---

## 🔗 Connections to Other NS 2030 Topics

### Synergy with Topic 1 (BESS)
- V2G creates 450 MW "virtual BESS" → coordinate with physical BESS for frequency regulation
- Federated learning privacy techniques apply to both

### Synergy with Topic 3 (Hydrogen)
- V2G demand response can shift load to match H₂ production windows

### Synergy with Topic 4 (Resilience)
- V2G-enabled EVs provide emergency power during microgrid islanding
- Attack detection even more critical when EVs are grid lifeline

---

## 📚 Key References to Review

### GNN for Cyber-Physical Systems
1. Jiang et al., "Graph Neural Networks for Power Grid Intrusion Detection," IEEE TII, 2023
2. Wang et al., "Spatial-Temporal GNN for Cyberattack Detection," IEEE TNNLS, 2023

### V2G Cybersecurity (Current State-of-Art)
3. Liu et al., "Cyberattack Detection in V2G Networks Using Deep Learning," IEEE TITS, 2022
4. Chen et al., "False Data Injection Attacks on EV Charging Infrastructure," IEEE TSG, 2023

### Federated Learning + Blockchain
5. Kim et al., "Blockchain-Enabled Federated Learning for IoT," IEEE Internet of Things, 2023
6. Your own Paper 3 (federated meta-RL) - cite your prior work

### Explainable AI for IDS
7. Lundberg & Lee, "A Unified Approach to Interpreting Model Predictions" (SHAP), NeurIPS, 2017
8. Ribeiro et al., "Anchors: High-Precision Model-Agnostic Explanations," AAAI, 2018

---

## ✅ Success Criteria

### Technical (Must Have)
- [ ] ≥95% TPR with <1% FPR (beats all baselines)
- [ ] Sub-100ms detection latency (real-time capable)
- [ ] Federated model within 5% of centralized performance
- [ ] Blockchain audit trail functional (model hashes stored)

### Novel Contribution (For Paper Acceptance)
- [ ] First GNN-based IDS for V2G at 40K+ node scale
- [ ] Novel blockchain-federated learning architecture
- [ ] Explainable AI integration (not just black-box detection)

### Industry Impact (For Conference Shine)
- [ ] Regulatory compliance proof (NERC CIP-014 alignment)
- [ ] Deployment cost estimate (<$500K for 450 stations)
- [ ] Letter of interest from NS Power or charging network (stretch goal)

---

## 🛠️ Tools & Libraries

### Core
- **Python 3.8+**
- **PyTorch Geometric** (GNN implementation)
- **PyTorch** (LSTM, federated learning)

### Specialized
- **SHAP** (explainability)
- **Web3.py** (Ethereum blockchain interface)
- **FedML or Flower** (federated learning framework)
- **NetworkX** (graph construction)

### Baselines
- **Snort** (signature-based IDS)
- **Scikit-learn** (Isolation Forest)

### Optional
- **Ganache** (local Ethereum testnet for cheap blockchain experiments)
- **Weights & Biases** (experiment tracking)

---

## 🚀 Quick Start (Week 1 Actions)

1. **Clone your Paper 1 GC-LSTM code**
   ```bash
   cd Paper_1_GC_LSTM_Attack_Detection
   cp -r models/ ../NS_2030_Conference_Papers/Topic_2_V2G_Cybersecurity/
   ```

2. **Register for Pecan Street dataset**
   - URL: https://www.pecanstreet.org/dataport/
   - Request: EV charging data (15-min resolution, 1,000+ homes)
   - Estimated wait: 1-2 weeks for academic access

3. **Set up V2G graph structure**
   ```python
   import networkx as nx
   import torch_geometric as pyg
   
   # 45,000 EV nodes
   G = nx.Graph()
   G.add_nodes_from(range(45000))
   
   # Connect EVs via distribution feeder topology
   # (import from IEEE 123-bus scaled model)
   ```

4. **Generate first attack sample**
   - Inject FDI to 10% of EVs
   - Verify GC-LSTM can distinguish from normal

---

**Ready to secure NS's EV revolution? Let's build the world's most advanced V2G cybersecurity system! 🚗⚡🔒**
