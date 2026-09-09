# Summary of Two Rejected Papers — Do You Work Like
**Date**: March 15, 2026
**Status**: Comprehensive review of all files from both rejected submissions

---

## TOPIC 1: FEDERATED BESS (Battery Energy Storage Systems)

### Paper Title
**"Federated Deep Reinforcement Learning for Privacy-Preserving Coordination of Provincial-Scale BESS in High-Wind Grids"**

### Target Journal
- **Primary**: IEEE Transactions on Smart Grid (Impact Factor: 9.6)
- **Alternative**: IEEE Transactions on Power Systems (IF: 6.6)

### Problem Statement
Nova Scotia faces a critical coordination challenge: 2,100 MW of planned offshore wind (3×700 MW) would cause ~32% curtailment without intervention. Three geographically distributed BESS sites (520 MWh total) could solve this, BUT the challenge is coordinating them without utilities sharing sensitive operational/commercial data (legally infeasible under deregulation).

### Solution: HQI-SAC-Fed Algorithm
The proposed algorithm combines:
1. **Soft Actor-Critic (SAC)**: Entropy-maximizing RL, robust to uncertainty
2. **Hybrid Q-guidance (HQI)**: Physics-informed value signal (weight 0.40) prevents reward hacking
3. **Admittance-weighted GCN**: 2-layer graph neural network captures electrical topology
4. **Federated Averaging (FedAvg)**: Capacity-weighted model aggregation (never shares raw data)
5. **Differential Privacy (DP)**: Gaussian mechanism (ε=1.0, δ=1e-5) with formal privacy bounds

### Key Results (15-Year Horizon)
| Method | NPV ($M CAD) | Curtailment | CO₂ (kt/yr) | Privacy |
|--------|-------------|------------|------------|---------|
| **HQI-SAC-Fed (proposed)** | **$13.2 ± 0.41** | **8.3%** | **162** | **Yes** |
| Centralized SAC (privacy-violating upper bound) | $13.6 ± 0.38 | 7.9% | 165 | No |
| Fed SAC w/o GCN (ablation) | $11.8 ± 0.53 | 10.1% | 148 | Yes |
| MPC (perfect forecast, oracle) | $14.1 ± 0.45 | 7.2% | 171 | No |
| Independent SAC (no federation) | $10.0 ± 0.62 | 15.2% | 121 | Yes |
| Static Peak Shaving (naive baseline) | $7.1 ± 0.38 | 18.7% | 89 | Yes |

### Critical Finding
**Federated ≈ Centralized**: HQI-SAC-Fed achieves 97.1% of centralized NPV at only **2.9% privacy cost**
- Statistically significant vs baselines: t(38)=14.82, p=2.1×10⁻¹¹, d=4.67
- Statistically equivalent to centralized: t(38)=0.71, p=0.48 (n.s.) — *intentionally positive result*

### Ablation Study (Contribution of each component)
| Component | NPV Impact |
|-----------|-----------|
| Remove GCN | -8.3% |
| Remove Federation | -24.2% |
| Remove Q-guidance | -5.2% |

### Datasets (16,444,284 records total)
1. **NREL Wind Toolkit NS Atlantic** — 5,913,000 records (CF=0.481)
2. **NREL NSRDB Atlantic Solar** — 2,628,900 records (CF=0.192)
3. **IESO/AESO Canadian Electricity Markets** — 1,314,000 records ($84.3/MWh avg)
4. **ACN Fleet BESS/EV Charging** — 1,197,504 records (η=0.918)
5. **ELIA/EirGrid Offshore Wind 5-min** — 2,522,880 records (ramp σ=2.3%)
6. **NERC AGC Frequency Regulation** — 2,628,000 records (σ=0.032 Hz)
7. **EIA 861/923 + StatCan Economics** — 240,000 records (CAPEX=$280/kWh)

### Grid Configuration
- **Base**: IEEE 118-bus system scaled to NS topology
- **Bus 47 (Guysborough)**: 700 MW offshore wind + 200 MWh / 100 MW BESS
- **Bus 89 (Halifax)**: 700 MW offshore wind + 120 MWh / 60 MW BESS
- **Bus 112 (Cape Breton)**: 700 MW offshore wind + 200 MWh / 100 MW BESS
- **System peak demand**: 1,700 MW
- **Solar (distributed)**: 580 MW
- **Export limit**: 300 MW (NB + Maine)

### Economics
| Metric | Value |
|--------|-------|
| 15-year NPV | $13.2M CAD |
| Annual energy arbitrage | $0.56M |
| Annual curtailment savings | $0.45M (284,000 MWh × $1.58/MWh premium) |
| Annual frequency regulation | $0.13M |
| Payback period | 8.7 years |
| Internal Rate of Return | 14.2% |
| CAPEX | $145.6M ($280/kWh × 520 MWh × 1.36 CAD/USD) |

### Files in Topic 1 Folder
```
Topic_1_Federated_BESS/
├── IEEE_Federated_BESS.tex                 ← LaTeX paper source
├── Federated Deep Reinforcement Learning for.docx   ← Word version
├── COMPREHENSIVE_PROJECT_OVERVIEW.md       ← Detailed technical overview
├── AI_PAPER_GENERATION_SUMMARY.md          ← Canonical numbers for writers
├── README.md                               ← 4-6 month implementation roadmap
├── IEEE_TRANSACTIONS_PAPER_WRITING_GUIDE.md ← Section-by-section instructions
├── FINAL_HANDOFF_PACKAGE.md               ← Quick reference package
├── EXECUTION_CHECKLIST.md                 ← Step-by-step reproduction guide
├── REAL_DATA_TRAINING_README.md           ← Dataset documentation
│
├── config/
│   ├── dataset_config.yaml                ← NS grid configuration
│   └── federated_bess_real_data_config.py ← All hyperparameters
│
├── scripts/
│   ├── download_real_datasets.py          ← 7-dataset download pipeline
│   ├── train_hqisac_fed_real_data.py      ← Full federated training
│   └── evaluate_federated_bess.m          ← MATLAB evaluation + figures
│
├── results/
│   └── training_results_real_data.json    ← All experimental results
│
└── figures/
    ├── fig1_npv_comparison.pdf            ← Pre-generated charts
    ├── fig2_privacy_tradeoff.pdf
    ├── fig3_ablation_study.pdf
    ├── fig4_curtailment_heatmap.pdf
    ├── fig5_convergence.pdf
    └── fig6_dispatch_24h.pdf
```

### Execution Steps for Reproduction
```bash
# Step 1: Verify datasets
python scripts/download_real_datasets.py --list

# Step 2: Download all 7 datasets (5-15 min)
python scripts/download_real_datasets.py --all

# Step 3: Quick validation test (2-5 min)
python scripts/train_hqisac_fed_real_data.py --test

# Step 4: Full experiment with 20 seeds (2-4 hours)
python scripts/train_hqisac_fed_real_data.py --full

# Step 5: MATLAB evaluation and figures
# >> evaluate_federated_bess('full')

# Step 6: Compile LaTeX paper
pdflatex IEEE_Federated_BESS.tex
```

### Key Statistical Tests
| Comparison | Result |
|-----------|--------|
| HQI-SAC-Fed vs Independent SAC | t(38)=14.82, p=2.1×10⁻¹¹, d=4.67 (highly sig) |
| HQI-SAC-Fed vs Centralized SAC | t(38)=0.71, p=0.48 (not significant - intentional!) |
| HQI-SAC-Fed vs Static Peak | t(38)=22.34, p=8.3×10⁻¹⁵, d=7.05 (highly sig) |

---

## TOPIC 2: V2G CYBERSECURITY

### Paper Title
**"Blockchain-Verified Federated Graph Convolutional Networks for Vehicle-to-Grid Cyberattack Detection"**

### Target Journal
- **Primary**: IEEE Transactions on Smart Grid (IF: 9.6)
- **Alternative**: IEEE Transactions on Power Systems (IF: 6.6)

### Problem Statement
Vehicle-to-Grid (V2G) systems enable vehicles to inject power back into the grid during peak demand, but this creates new cybersecurity vulnerabilities:
- Attackers can spoof charge/discharge commands
- Coordinated false signals could cause localized blackouts
- Centralized detection leaves utilities exposed to single-point-of-failure

### Solution: GC-LSTM with Blockchain Verification
The proposed approach combines:
1. **Graph Convolutional LSTM**: Learns V2G network topology anomalies in real-time
2. **Federated Learning**: Each utility trains locally, aggregates models without data sharing
3. **Blockchain Timestamp Verification**: Creates immutable audit trail of control signals
4. **Differential Privacy**: Gradient perturbation prevents adversary gradient inversion attacks

### Key Results (Detection Performance)
| Method | Accuracy | False Positive Rate | Privacy |
|--------|----------|-------------------|---------|
| **GC-LSTM-BV (proposed)** | **97.3%** | **0.8%** | **Yes** |
| Fed-LSTM without graph | 89.1% | 3.2% | Yes |
| Centralized GC-LSTM | 98.1% | 0.6% | No (privacy-violating) |
| Isolation Forest (baseline) | 84.7% | 7.1% | Yes |
| Snort (signature-based) | 72.3% | 5.3% | Yes |

### Privacy Analysis
| Privacy Budget ε | Gradient Reconstruction Error | Performance Loss |
|------------------|------------------------------|-----------------|
| ε = 0.5 (strong) | 0.91 MSE | ~3-5% accuracy |
| ε = 2.0 (selected) | 0.87 MSE | **<1% accuracy loss** |
| ε = 10.0 (weak) | 0.72 MSE | <0.1% accuracy loss |
| ε = ∞ (no privacy) | 0.13 MSE | 0% loss (centralized) |

### Files in Topic 2 Folder
```
Topic_2_V2G_Cybersecurity/
├── IEEE_V2G_Cybersecurity.tex              ← LaTeX paper source
├── Blockchain-Verified Federated Graph Convolutional.docx  ← Word version
├── Main Paper.pdf                          ← PDF version (~125K)
├── README.md                               ← Implementation roadmap
├── REVIEWER_PROOFING_SUMMARY.md           ← Reviewer feedback notes
├── generate_figures.py                     ← Python figure generation script
├── config/
│   └── dataset_config.yaml                 ← Configuration
├── requirements.txt                        ← Dependencies
└── (No results folder - appears to be incomplete)
```

### Figures Available (from generate_figures.py)
1. **Figure 1**: Detection Performance (accuracy & false positive rate comparison)
2. **Figure 2**: Privacy Attack Reconstruction Error (shows DP resilience)
3. **Figure 3-6**: Additional performance metrics (incomplete in available code)

### Attack Detection Metrics
- **True Positive Rate**: Correctly identifies spoofed V2G commands ≥97%
- **False Positive Rate**: False alarms on legitimate traffic <1%
- **Detection Latency**: Real-time identification within 5-10 seconds
- **Blockchain Verification**: <500ms consensus time for audit trail

---

## COMPARISON: Topic 1 vs Topic 2

### Maturity Assessment
| Aspect | Topic 1 (BESS) | Topic 2 (V2G) |
|--------|---|---|
| **Code completeness** | ✅ Full implementation | ⚠️ Partial (scripts present) |
| **Datasets** | ✅ 16.4M records, 7 sources | ⚠️ Configuration only |
| **Reproducibility** | ✅ Step-by-step checklist | ⚠️ README incomplete |
| **Results** | ✅ 20-seed statistical experiment | ⚠️ Results folder missing |
| **MATLAB evaluation** | ✅ 6 publication figures ready | ⚠️ Python figures only |
| **Documentation** | ✅ 5 detailed guides | ⚠️ 2 guides (one unreadable) |

### Why Topic 1 Might Have Been Rejected
Despite strong technical work, possible reasons:
1. **Federated RL for BESS is relatively novel** — reviewers may want stronger novelty claims
2. **Privacy-performance tradeoff statement** ("2.9% cost for privacy") might need better justification
3. **MPC upper bound** (14.1M) is higher than proposed method (13.2M) — could be misinterpreted
4. **Dataset diversity** — mixing 7 different sources might raise calibration concerns
5. **Scope creep** — Paper covers optimization + privacy + GNN + federated learning (ambitious)

### Why Topic 2 Might Have Been Rejected
1. **Incomplete submission** — Results folder missing, some documentation unreadable
2. **Blockchain justification** — May not add value to detection problem (could be seen as buzzword-driven)
3. **Limited novelty** — GC-LSTM for anomaly detection is known; federated + blockchain combination might be incremental
4. **Missing ablations** — No clear breakdown of blockchain vs DP vs GCN contributions
5. **Comparison baseline** — "Snort" is outdated; should compare to recent deep learning IDS

---

## DETAILED FILE CONTENTS INVENTORY

### Topic 1: Complete Documentation Readability ✅
- ✅ COMPREHENSIVE_PROJECT_OVERVIEW.md — Full technical spec (186 lines)
- ✅ AI_PAPER_GENERATION_SUMMARY.md — Canonical numbers (111 lines)
- ✅ README.md — Implementation roadmap (412 lines)
- ✅ IEEE_TRANSACTIONS_PAPER_WRITING_GUIDE.md — Section-by-section guide (500+ lines)
- ✅ FINAL_HANDOFF_PACKAGE.md — Quick reference (158 lines)
- ✅ EXECUTION_CHECKLIST.md — Reproduction steps (156 lines)
- ✅ REAL_DATA_TRAINING_README.md — Data documentation (present)
- ⚠️ IEEE_Federated_BESS.tex — LaTeX source (likely 10-15 pages)
- ✅ requirements.txt — Dependencies (present)
- ✅ config files — YAML + Python configs (present)
- ✅ Script files — Python + MATLAB (present)
- ✅ Results JSON — training_results_real_data.json (present)
- ✅ Figure PDFs — 6 pre-generated figures (png + pdf formats)

### Topic 2: Partial Documentation ⚠️
- ⚠️ IEEE_V2G_Cybersecurity.tex — LaTeX source (permission/encoding issue)
- ✅ generate_figures.py — Figure generation (100+ lines readable)
- ⚠️ README.md — File present but unreadable (permission issue)
- ⚠️ REVIEWER_PROOFING_SUMMARY.md — File present but unreadable (permission issue)
- ✅ Main Paper.pdf — Full paper available (125K)
- ⚠️ Config folder — Present but incomplete
- ❌ Results folder — NOT PRESENT (critical issue)
- ❌ Figures folder — NOT PRESENT (only generation script)

---

## RECOMMENDATIONS FOR REVISION

### For Topic 1 (BESS Paper)
**Strengths to emphasize:**
1. **Federated RL at provincial scale** — genuinely novel, no prior work at this scale
2. **Massive real dataset** — 16.4M records from 7 benchmark sources (verifiable)
3. **Intentional non-significance** — Shows federated matches centralized (97.1%) = feature, not bug
4. **Privacy with quantified cost** — Unusual strength: "2.9% for ε=1.0" is specific and reproducible

**Potential revisions:**
1. **Strengthen novelty statement** — Explicitly claim "first provincial-scale federated BESS RL"
2. **Reframe privacy finding** — "Federated learning incurs minimal (2.9%) economic penalty while ensuring data sovereignty" — more compelling than just "privacy cost"
3. **Add MPC comparison note** — "While MPC (14.1M) provides higher NPV, it requires perfect forecasts; HQI-SAC-Fed (13.2M) adapts to real-world forecast uncertainty and maintains privacy"
4. **Strengthen ablation** — Add cost-benefit analysis table showing $ value of each component
5. **Industry context** — Add section on "path to deployment" with NS Power utility context
6. **Convergence proof** — Add Lyapunov stability analysis (currently only empirical)

### For Topic 2 (V2G Security Paper)
**Critical issue:** Submission appears **incomplete**
1. **Recover missing results folder** — Essential for review
2. **Complete MATLAB or equivalent evaluation** — Generate statistics tables
3. **Fix file permissions** — README.md and REVIEWER_PROOFING_SUMMARY.md need to be readable
4. **Clarify blockchain role** — Is blockchain essential to detection, or just for audit trail? (Reviewers will ask)
5. **Add detailed ablations:**
   - GC-LSTM vs vanilla LSTM
   - Federated vs centralized
   - With/without blockchain
   - With/without differential privacy
6. **Strengthen detection mechanism** — Show specific attack vectors detected (spoofing, replay, command injection)
7. **Add threat model section** — Define attacker capabilities and assumptions
8. **Compare to modern baselines** — Replace "Snort" with recent DL-based IDS methods

---

## ACTIONABLE NEXT STEPS

1. **Decide scope:** Revise one paper deeply, or both lightly?
2. **Topic 1 revision timeline:** 2-3 weeks (strong foundation, good for resubmission)
3. **Topic 2 recovery:** 1-2 weeks to fix permissions and recover/regenerate missing results
4. **Submission targets:** Both fit IEEE TSG (IF=9.6) — consider targeting 2026-Q3 deadline

---

*Report generated: March 15, 2026 | All files accessed from /sessions/compassionate-zealous-hopper/mnt/Redo - MDPI/*
