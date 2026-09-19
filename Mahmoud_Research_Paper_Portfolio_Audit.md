# Research Paper Portfolio Audit — Google Drive

**Audit date:** 2026-09-18  
**Primary folder audited:** [Google Drive research folder](https://drive.google.com/drive/folders/12xxM0UkegtGeFHmOwNkmcmVtiokOueu9)

> Stage assessments are artifact-based. A full manuscript means a substantial manuscript exists; it does not imply submission or acceptance unless reviewer, acceptance, or publication evidence was found.

## Stage Scale

| Stage | Meaning |
|---|---|
| **S5** | Complete / published / accepted / final-review stage |
| **S4** | Full manuscript / submission-ready after focused validation |
| **S3** | Advanced draft / needs consolidation |
| **S2** | Structured concept / extended abstract |
| **S1** | Technical seed / model / dataset / idea |
| **S0** | Placeholder / venue target |

# Executive Portfolio Summary

After collapsing duplicate versions and predecessor drafts, the supplied Drive folder contains **14 substantive manuscript/research tracks**, plus technical seeds and venue placeholders. A Drive-wide cross-check also identified several newer manuscripts and large future-paper idea banks stored elsewhere.

| # | Research track | Stage | Current status |
|---:|---|---|---|
| 1 | Smart Grid Technologies Review | **S5** | final reviewer/publication-stage files |
| 2 | EV Battery Fire/Thermal Protection | **S5** | reviewer-response + final manuscript |
| 3 | Solar Power Forecasting Robustness | **S5** | conference acceptance + final paper/presentation |
| 4 | Hybrid Wind Power Forecasting | **S5** | conference acceptance + final-version branch |
| 5 | Real-Time EV Battery Fleet Management | **S4/S5** | final-revision manuscript + Simulink model |
| 6 | One-Hour-Ahead EV SoC / State Forecasting + XAI | **S4** | advanced journal manuscript |
| 7 | MATLAB V2G SoC Prediction Comparison | **S3** | full manuscript, overlaps later EV work |
| 8 | Day-Ahead EV Condition Prediction | **S3 / historical** | predecessor lineage, largely superseded |
| 9 | SVC Firing-Angle Optimization with CatBoost-LightGBM | **S4** | full manuscript + Simulink + data + notebook |
| 10 | GA-Driven THD Feature Selection | **S4** | full manuscript + code + THD data |
| 11 | PINN-LSTM THD Prediction | **S4** | full manuscript; scope lineage needs consolidation |
| 12 | Solar + Hydrogen + EV Charging + AI | **S2** | structured short paper/concept |
| 13 | Net-Zero / Renewable Grid Integration + AI | **S2** | abstract + presentation |
| 14 | Microgrid Demand Response / Imperialist + GA (Mahdi-led) | **S4/S5** | reviewer-response stage |

## Additional active manuscripts elsewhere in Drive

- **Energy Infrastructure for AI Data Centers: A Critical Review of Grid Integration, Techno-Economic Challenges, and Future Pathways** — **S5 / reviewer revision**
- **Protection and Control Reliability Standards in Canada: NERC PRC Compliance Across Provincial Jurisdictions** — **S3/S4**
- **Intelligent Control of FACTS Devices for Power System Stability Enhancement: A Machine Learning and Simulation-Based Approach** — **S3**
- **Hybrid Wavelet Neural Network–ANN–Kalman Filter Framework with Dynamic Ensemble Weighting for Short-Term Load Forecasting** — **S4**
- **Road to 15** — 15 future IEEE-oriented research directions, mostly **S0/S1**
- **First 5 Papers** — five additional AI/FACTS/cyber/EV concepts, **S0/S1**
- **EV research idea bank** — nine future EV-grid directions, **S0/S1**

# Detailed Paper Audit

## 1. Smart Grid Technologies Review

**Title:** *A Comprehensive Review of the Current Status of Smart Grid Technologies for Renewable Energies Integration and Future Trends: The Role of Machine Learning and Energy Storage Systems*

**Directory:** [MDPI Review Smart Grid](https://drive.google.com/drive/folders/1t039LfP421-pDQ2PRAYbsE7vwMbtDxuG)

**Stage:** **S5 — complete/publication stage**

**Evidence:** full review, final revised manuscript, Reviewer 1/2 material, figures, case-study diagrams, MDPI formatting.

**Complete by:** treat as finished; preserve one canonical final manuscript/PDF, reviewer responses, figures and bibliography. Move intermediate files to Archive.

**Status:** `COMPLETE — ARCHIVE`

---

## 2. EV Battery Fire/Thermal Protection

**Title:** *Enhancing Fire Protection in Electric Vehicle Batteries Based on Thermal Energy Storage Systems Using Machine Learning and Feature Engineering*

**Directory:** [MDPIThermalPaper](https://drive.google.com/drive/folders/1JtD_7feTlb6wlk-K-zbwwzJnonrY1zRQ)

**Stage:** **S5**

**Evidence:** final/revised manuscript, Reviewer 1–4 files, Simulink models, Python notebooks, battery/grid datasets, thermal and electrical results.

**Complete by:** preserve accepted/final version; create a reproducibility package containing final simulation, notebook, raw/processed data and figure-generation code.

**Status:** `COMPLETE — ARCHIVE / EXTENSION SOURCE`

---

## 3. Solar Power Forecasting Robustness

**Directory:** [Solar Forecasting](https://drive.google.com/drive/folders/1kPaWT3CAJlACUg0XOl9xE7e4ttjYDJTK)

**Stage:** **S5 — accepted conference paper**

**Evidence:** manuscripts/PDF, code, data, Results.xlsx, presentation, acceptance evidence and certificate.

**Journal extension:** multi-site/multi-season validation, probabilistic forecasting, concept drift, calibration, latency comparison, transformer/TCN baselines and walk-forward testing.

**Status:** `COMPLETE — JOURNAL EXTENSION OPTIONAL`

---

## 4. Hybrid Wind Power Forecasting

**Directory:** [Wind Forecasting](https://drive.google.com/drive/folders/14m63TuoRDeqdi23i8ik7dn3aW-fKe40Q)

**Stage:** **S5**

**Evidence:** multiple manuscript versions, V6/V7 PDFs, figures, presentation, acceptance evidence and final-version branch.

**Complete by:** consolidate the title lineage into one canonical publication. A journal extension should add new sites/years, probabilistic forecasting, weather-regime analysis, horizon sensitivity and ablation.

**Status:** `COMPLETE — JOURNAL EXTENSION OPTIONAL`

---

## 5. Real-Time EV Battery Fleet Management

**Directory:** [Real-Time EV Battery Fleet](https://drive.google.com/drive/folders/1UMhuKAKuoY3a81MR54xX0MZn2Yyxtz1y)

**Final revision:** [Final Version Revision](https://drive.google.com/drive/folders/1Uoy46r1mcyM4ewweoV61Fs6MnlXKeKjd)

**Stage:** **S4/S5 boundary**

**Evidence:** Ver. 1–8/X lineage, final-revision manuscript, revision steps, V2G Simulink model and visual results.

**Completion path:**
1. Verify actual publication status and canonical final manuscript.
2. Synchronize Table 1 and all parameters with the final Simulink model.
3. Correct V2G/G2V/idle sign conventions.
4. Document the `from3to12` load dataset and reproduce Q1/Q3 thresholds.
5. Add controlled-vs-uncontrolled quantitative metrics: peak demand, load variability, imported energy, V2G/G2V energy, SoC violations and owner-constraint violations.
6. Remove unsupported voltage/frequency/THD/loss claims unless corresponding results are added.
7. Make the model self-contained with data + README.
8. Correct figure references, time horizon, equations and bibliography.

**Status:** `MAJOR TECHNICAL REVISION / VERIFY PUBLICATION STATUS`

---

## 6. EV SoC / State Forecasting + Explainable AI

**Primary directory:** [EV Forecasting](https://drive.google.com/drive/folders/1Y3tWRLY6-Vn91NoqNKXN8OOTsxmZAuVN)

**Elsevier branch:** [Elsevir](https://drive.google.com/drive/folders/1YmCQ1B96Q0S3keSmPOLG6HMHGpg-7652)

**Stage:** **S4 — advanced journal manuscript**

**Completion path:**
1. Freeze the final target: SoC regression, state classification, or explicitly multi-task.
2. Use leakage-safe temporal splitting and true external validation.
3. Run all baselines on identical splits.
4. Add ablation for lagged features, noise handling, feature engineering and hybridization.
5. Add robustness to noise, missing data, unseen SoC/owner profiles and distribution shift.
6. Add SHAP/global + local interpretability and explanation stability.
7. Report latency/model size.
8. Create one canonical `FINAL_JOURNAL/` branch and archive predecessors.

**Status:** `HIGH PRIORITY — FINISH AND SUBMIT`

---

## 7. MATLAB V2G SoC Prediction Comparison

**Directory:** [SoC Prediction Matlab](https://drive.google.com/drive/folders/16HU4dnDC00nBQ4-U9VHOxbNiViRIQ4nN)

**Stage:** **S3**

**Issue:** scientifically overlaps the newer EV SoC/XAI manuscript.

**Recommended action:** merge unique experiments into the current EV SoC/XAI paper unless this paper is reframed around a clearly different contribution such as aging/temperature robustness, online estimation, physics-informed estimation or cross-chemistry generalization.

**Status:** `MERGE OR REFRAME`

---

## 8. Day-Ahead EV Condition Prediction

**Directory:** same EV forecasting lineage.

**Stage:** **S3 / historical**

**Evidence:** versions 2–10, final-version branch, IEEE feedback, datasets, feature selection, results and coding.

**Recommended action:** archive as predecessor/source material. Reuse legitimate baseline experiments and development history in the newer paper/thesis rather than submitting an obsolete overlapping version.

**Status:** `ARCHIVE AS PREDECESSOR`

---

## 9. SVC CatBoost-LightGBM

**Title:** *Hybrid Machine Learning-Based Optimization of SVC Firing Angles: A CatBoost-LightGBM Approach for Enhanced Grid Stability*

**Directory:** [SVC ML Paper](https://drive.google.com/drive/folders/1zGuy1oTsOOsJSx3tiORkQVU9cnr0oCKB)

**Stage:** **S4**

**Completion path:**
1. Separate ML prediction accuracy from closed-loop control performance.
2. Benchmark PI, CatBoost, LightGBM, XGBoost and relevant neural models.
3. Add voltage recovery time, maximum deviation, Q error, overshoot, damping, losses and latency.
4. Test unseen load steps, SLG/LL/3PH faults, renewable ramps and operating-point shifts.
5. Prove how the optimal firing-angle target is generated.
6. Add hybrid-model ablation.
7. Use temporal/out-of-distribution validation.
8. Package the notebook, data and Simulink model reproducibly.

**Status:** `HIGH PRIORITY — TECHNICAL VALIDATION THEN SUBMIT`

---

## 10. GA-Driven THD Feature Selection

**Directory:** [GA THD](https://drive.google.com/drive/folders/1IQpCbEtM4Tvp9s92ks4hsfF4WWkOLbp2)

**Stage:** **S4**

**Completion path:**
1. Use identical feature budgets for GA/RFE/PCA.
2. Use time-series/walk-forward evaluation.
3. Report feature count, training/inference time, RMSE, MAE, R² and feature-selection cost.
4. Repeat stochastic GA runs and report uncertainty.
5. Freeze GA hyperparameters/random seeds.
6. Ensure feature selection occurs inside training folds.
7. Add sensor-noise and missing-channel robustness.
8. Clarify THD definition, measurement location and sampling.

**Status:** `HIGH PRIORITY — FINISH VALIDATION AND SUBMIT`

---

## 11. PINN-LSTM THD Prediction

**Directory:** [PINN-LSTM THD](https://drive.google.com/drive/folders/1IZaFdvXwLLAmpWfEuS_tLufpTgT3xZ6S)

**Stage:** **S4**

**Issue:** project lineage shifted from PINN + reinforcement-learning mitigation to PINN-LSTM prediction.

**Completion path:** choose prediction or mitigation as the paper's single contribution. For prediction, define the physics constraint/loss explicitly, add LSTM/PINN/PINN-LSTM ablations, modern baselines, noise/missing-data/shift tests and real-time latency. Keep RL mitigation as a separate future paper if retained.

**Status:** `HIGH PRIORITY — CONSOLIDATE SCOPE THEN SUBMIT`

---

## 12. Solar + Hydrogen + EV Charging + AI

**Directory:** [Solar + Hydrogen + EV + AI](https://drive.google.com/drive/folders/1Wjmk39HBznhEduUGwBvFj4iHtacK6PyO)

**Stage:** **S2**

**Completion path:** formulate PV/electrolyzer/H₂/fuel-cell/grid/EV energy balances; use real temporal solar and EV demand data; compare grid-only, PV+BESS, PV+H₂ rule-based, MPC/optimization and proposed AI; report peak reduction, renewable utilization, unmet EV demand, losses, cost and emissions; add efficiency/storage-size sensitivity.

**Status:** `MEDIUM PRIORITY — NEEDS MODEL + RESULTS`

---

## 13. Net-Zero / Renewable Grid Integration + AI

**Directory:** [Net Zero](https://drive.google.com/drive/folders/1khgQT0HtB6jyYulgmJviB5hEjn-xX4mn)

**Stage:** **S2**

**Evidence:** abstract + presentation only.

**Completion path:** first decide whether this is a review, empirical grid/market study, or AI control paper. Narrow to one research question before further writing.

**Status:** `HOLD — DEFINE A SINGLE RESEARCH QUESTION`

---

## 14. Microgrid Demand Response — Imperialist + GA

**Directory:** [Mehdi's Paper](https://drive.google.com/drive/folders/14wdEzNj4CHj_KxTO-mOW_UsZHSsyZjfv)

**Stage:** **S4/S5 reviewer-response stage**

**Note:** appears Mahdi Ghaffari-led; track separately from the first-author pipeline.

**Completion path:** point-by-point reviewer matrix, exact manuscript-location mapping, verify new claims, rerun optimization if required and perform final equations/units/tables/figures audit.

**Status:** `COLLABORATOR PAPER — COMPLETE REVIEW CYCLE`

# Technical Seeds Inside the Supplied Folder

## UPFC / FACTS

**Directory:** [UPFC Matlab](https://drive.google.com/drive/folders/1-KygSvNY0mjKMfm2NIPHDEKV4XIVhBDH)

**Stage:** **S1**

Contains UPFC/fuzzy/impedance-emulation models. Convert to a paper only after choosing a precise controller problem, baseline, network, contingency matrix and quantitative stability metrics.

## PSCAD Ideas

**Directory:** [PSCAD Ideas](https://drive.google.com/drive/folders/15lkcqozAFqky1ThiVqXBDOTc39N0_7nY)

**Stage:** **S1**

Contains cable, cross-bond fault, mutual coupling, transposition, differential-protection and IEEE test-system assets. Split future work by research question rather than combining all models into one paper.

## PV-MPPT

**Directory:** [PV_MPPT](https://drive.google.com/drive/folders/1LIhJ7reXZ8-Sopvu4bDMvJw1WsL1DK4n)

**Stage:** **S1**

A basic MPPT model alone is insufficient for a paper; add a novel controller, uncertainty/partial-shading problem, grid-support function, cyber-resilience or validation contribution.

# Additional Manuscripts Elsewhere in Drive

## A. AI Data-Center Critical Review

**Stage:** **S5 — reviewer revision / near final**

Finish reviewer-source traceability, verify every quantitative statement, harmonize methodology/search counts, source every figure/table and close bibliography/cross-reference issues.

**Status:** `VERY HIGH PRIORITY — CLOSE REVIEW CYCLE`

## B. NERC PRC Compliance Across Canadian Jurisdictions

**Stage:** **S3/S4**

Complete by verifying current PRC versions/effective dates, separating NERC requirements from provincial adoption/enforcement, building a province-by-standard matrix, completing methodology and bibliography, and performing a final regulatory fact check immediately before submission.

**Status:** `HIGH PRIORITY — FACT CHECK + BIBLIOGRAPHY + FINAL SYNTHESIS`

## C. Intelligent FACTS Control

**Stage:** **S3**

The current scope is too broad across devices, AI methods and simulation platforms. Narrow to one or two FACTS devices and one stability objective; verify simulations, add control baselines/ablation and distinguish it from the SVC CatBoost-LightGBM paper.

**Status:** `RESTRUCTURE BEFORE SUBMISSION`

## D. Wavelet–ANN–Kalman Short-Term Load Forecasting

**Stage:** **S4**

Critical first task: audit the reported 41.23% MAPE and inverse scaling. Then recompute MAE/RMSE/nRMSE/R², use chronological splits, add seasonal breakdowns and component ablations, significance testing, conclusion/limitations and reproducible preprocessing.

**Status:** `HIGH PRIORITY — METRIC AUDIT BEFORE SUBMISSION`

# Idea Bank

## Road to 15

1. Pareto-Optimal FACTS Deployment in Hybrid AC/DC Grids using NSGA-III
2. Stochastic MPC for STATCOM under Asymmetrical Faults and Solar Ramps
3. Dynamic Var Reserve Allocation via UPFC with Lyapunov Adaptive Control
4. Impedance Reshaping in TCSC-Compensated Hybrid Grids for SSR
5. Hierarchical RL for Coordinated FACTS Control
6. ADMM-Based Distributed FACTS Placement
7. Grid-Forming UPFC using VSM + Q-V Droop
8. FACTS + BESS Bilevel Co-optimization
9. Adversarial Robustness of ML FACTS Controllers
10. Quantum Annealing for FACTS Placement
11. Differential Flatness-Based UPFC Control for MT-HVDC
12. SDDP for Risk-Averse FACTS Operation under Wind Uncertainty
13. Sparse/GNN RL for Topology-Aware FACTS Control
14. Hybrid TCSC-APLC Harmonic Resonance Suppression with MOEA/D
15. Digital-Twin FACTS Health Monitoring with Federated Learning

All are **S0/S1**. Best immediate reuse: UPFC ideas 3/7, THD idea 14 and adversarial FACTS idea 9.

## First 5 Papers

1. AI-Driven Multi-Objective Optimization for Coordinated FACTS Control
2. Federated Learning-Based Cybersecurity for False Data Injection Attack Detection
3. Hybrid Quantum-Inspired Stochastic Optimization for Renewable-Aware Power-System Operations
4. AI-Driven Grid-Aware EV Charging Infrastructure with PV-DSTATCOM
5. Self-Supervised Transformer Models for Wideband Impedance Estimation and Stability Assessment

All are **S0/S1**.

## EV Future Ideas

Nine themes were found: SoC prediction with aging/environment, intelligent charge/discharge optimization, BMS cybersecurity, EV+DER integration, real-time V2G/G2V power-flow optimization, renewable-rich grid stability, ancillary services, communication/protocol standards and economic/environmental assessment.

# Recommended Completion Order

## Priority A — Close first

1. AI Data-Center Critical Review
2. EV SoC/XAI Journal Manuscript
3. SVC CatBoost-LightGBM
4. GA-THD
5. PINN-LSTM THD
6. Wavelet–ANN–Kalman STLF

## Priority B — Consolidate / verify

1. Real-Time EV Battery Fleet
2. NERC PRC Canada Review
3. Intelligent FACTS Control
4. MATLAB SoC Comparative Paper

## Priority C — Build after Priority A

1. Solar + Hydrogen + EV + AI
2. Net-Zero / AI Renewable Integration
3. UPFC paper from Road-to-15

# Recommended Repository / Drive Structure

```text
Publications/
├── 01_AI_Data_Center_Critical_Review/
│   ├── 01_Manuscript/
│   ├── 02_Reviewer_Response/
│   ├── 03_Data_Sources/
│   ├── 04_Figures/
│   ├── 05_References/
│   └── 99_Archive/
├── 02_EV_SoC_XAI/
│   ├── 01_Manuscript/
│   ├── 02_Code/
│   ├── 03_Data/
│   ├── 04_Results/
│   ├── 05_Figures/
│   └── 99_Archive/
├── 03_SVC_CatBoost_LightGBM/
├── 04_GA_THD/
├── 05_PINN_LSTM_THD/
├── 06_STLF_Wavelet_ANN_KF/
├── Published/
│   ├── Smart_Grid_Review/
│   ├── EV_Fire_Thermal/
│   ├── Solar_Forecasting/
│   └── Wind_Forecasting/
└── Idea_Bank/
    ├── Road_to_15/
    ├── First_5_Papers/
    ├── EV_Ideas/
    ├── PSCAD_Ideas/
    └── Future_FACTS/
```

Each active project should include a `STATUS.md` with target venue, current manuscript/code/data/figures state, blockers, reproducibility entry point, environment, seed, dataset source and main results file.

# Immediate Technical Actions

| Paper | Next action |
|---|---|
| AI Data Center Review | close reviewer/source verification matrix |
| EV SoC/XAI | freeze temporal split + final baselines/ablation |
| SVC CatBoost-LightGBM | closed-loop fault/contingency validation |
| GA-THD | leakage-safe repeated GA/RFE/PCA comparison |
| PINN-LSTM THD | formalize physics loss + ablation |
| Wavelet–ANN–Kalman STLF | audit MAPE and inverse scaling |
| Real-Time EV Fleet | synchronize manuscript/model + quantitative baseline comparison |
| NERC PRC Canada | verify standards versions + provincial mapping + references |
| Intelligent FACTS | narrow scope and verify simulations |
| Solar-H₂-EV-AI | build energy-balance simulation and baselines |
| Net-Zero AI | choose one research question |
| UPFC seed | select one controller problem and benchmark |

# Bottom Line

The portfolio is larger than the number of apparent top-level folders because many active manuscripts are stored outside the original research root, while many files inside the root are duplicate generations of the same lineage.

The strongest productivity path is to **close the existing S4 manuscripts before opening additional S0/S1 topics**. There is already enough partially completed work for a substantial publication pipeline.
