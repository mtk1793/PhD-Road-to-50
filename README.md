# PhD Road to 50

A personal research hub — tracking the full lifecycle of my PhD publications: finished manuscripts, work in progress, paper ideas, datasets, and out-of-the-blue side projects. Goal: **50 publications**.

**Status:** 3 published &nbsp;·&nbsp; 6+ in progress &nbsp;·&nbsp; 30+ ideas/topics &nbsp;·&nbsp; 774 curated files (~360 MB)

---

## Repository structure

```
.
├── published/     Final, publication-ready manuscripts + reviewer responses
├── in_progress/   Papers currently being written, revised, or resubmitted
├── ideas/         Research ideas & topic explorations (numbered + themed)
├── out_of_blue/   Sudden/unplanned side projects that became papers
└── datasets/      Datasets and supporting data for the papers
```

### published/
Completed papers that are accepted, submitted, or done.

| Paper | Folder |
|---|---|
| Agentic AI (Paper 1) | `Paper 1 - done/` |
| CCECE papers (Papers 2 & 3) — Short-Term Load Forecasting & PINN+LSTM | `Papers 2 and 3 CCECE - done/` |

### in_progress/
Active writing streams, each with its own review status:

- `AI Data Center Journal/`
- `Data Center Review Paper/`
- `EV Review PAper/`
- `Redo - MDPI/` (`Topic_1_Federated_BESS`, `Topic_2_V2G_Cybersecurity`)
- `Smart Grid and Data Center Consumption Comprehensive Review/`
- `Priorities/`

### ideas/
Two kinds of exploration:

- **Numbered experiments** (`14`, `15`, …, `39`) — Load Frequency Control (LFC), Automatic Generation Control (AGC), FACTs coordination, optimization, and control-theory deep dives, each with manuscript drafts, simulations, and figures.
- **Themed research topics** (`Topic_1_Federated_Physics_Informed_Graph_Learning`, `Topic_1_Metacognitive_Continual_Learning`, `Topic_2_Causal_Reinforcement_Learning`, … `Topic_10_DeepONet_Operator_Learning`) — physics-informed AI, continual learning, explainable AI, GNNs, Koopman operators, and neuromorphic approaches for power systems.
- `Second Paper/` — Neuro-OptimaFACTS (IEEE-39 bus work).

### out_of_blue/
Unplanned projects that took off on their own:

- `EWC/` — Elastic Weight Consolidation + continual learning for smart grids
- EWC_IXER continual-learning academic papers (accepted track / IEEE TPWRS format)

### datasets/
- `SoC Prediction Matlab/` — battery SoC prediction data & MATLAB work

---

## Organization notes

- Excluded from this repo (kept out to stay Git-friendly): virtual environments (`.venv/`), Python caches (`__pycache__/`, `.pyc`), shortcuts (`.lnk`), archives (`.zip`/`.rar`/`.tar`), installers (`.exe`), raw large arrays (`.npy`), oversized spreadsheets, and HEIC photos.
- Files larger than 25 MB are generally left out of the repo.

## Keeping this repo updated

Any new manuscript, revision, idea, or dataset can be dropped into its matching folder and committed — the structure above is the canonical layout. If a paper moves from `ideas/` to `in_progress/` to `published/`, move its folder accordingly so the index always reflects reality.