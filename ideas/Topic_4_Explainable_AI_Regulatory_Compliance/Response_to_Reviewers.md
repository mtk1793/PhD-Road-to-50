# Response to Reviewers
**Paper Title:** Counterfactual Explanations for Neural Network-Based Optimal Power Flow: A PyPower-Validated Approach for Regulatory Compliance
**Target Venue:** IEEE Transactions on Power Systems

---

## Editor / Overview
We thank the reviewers for their constructive and rigorous feedback. We have performed a comprehensive revision of the manuscript to address all concerns, specifically:
1.  **Clarified the Novelty:** Explicitly positioned the work as the first *physics-validated* XAI framework, moving beyond generic application of SHAP.
2.  **Hardened the Dataset:** Added a detailed dataset mechanics section and master table (Table II) ensuring reproducibility.
3.  **Expanded OPF Formulation:** Explicitly listed all constraints (Eqs 1-8) including thermal limits.
4.  **Defined Operational Value:** Added a "So What?" operational impact summary mapping XAI to control room actions.
5.  **Benchmarked rigorously:** Added 3 baselines (Classical, Black-box, LIME) and comparison metrics (Table IV).

---

## Reviewer 1 (Interpretation & Methods)

**Point 1: "Novelty is unclear. Applying SHAP to OPF is not new."**
> **Response:** We agree that basic SHAP application is common. However, our contribution is the *coupling* of SHAP with **physics-in-the-loop counterfactual validation**, ensuring that explanations are not just mathematically sound but physically realizable. We have rewritten the **Abstract** and **Introduction** (Contributions 1-5) to forcefully articulate this differentiator. We explicitly state: *"Unlike prior work... our framework guarantees that every 'what-if' scenario presented to operators is physically realizable."*

**Point 3: "OPF formulation is implicit."**
> **Response:** We have expanded the **Methodology** section to explicitly state the AC OPF formulation. **Equations 1-8** now define the objective function, power balance, generator limits, voltage constraints, and crucially, **line thermal limits** (Eq. 7), which were previously omitted.

**Point 4: "XAI results feel decorative. How does this help an operator?"**
> **Response:** We have added a new subsection: **"Operational Interpretation of XAI Results."** This section translates abstract SHAP values into three concrete operator actions: (1) Demand Response Targeting, (2) Congestion Warning, and (3) Control Hierarchy. We also added a boxed **"Operational Impact Summary"** (Page 4) to highlight these practical benefits.

**Point 5: "Where are the baselines?"**
> **Response:** We have introduced **three baselines**: (1) Classical OPF Sensitivity (Lagrange multipliers), (2) Black-box NN, and (3) LIME. A new **"Why These Baselines?"** paragraph justifies their selection.

**Point 6: "Metrics are missing."**
> **Response:** We added a **Comprehensive Evaluation Metrics** table (**Table IV**). This reports **Fidelity** (91%), **Stability/CoV** (0.12), and **Runtime**, quantitatively demonstrating SHAP's superiority over LIME (which showed only 68% fidelity and poor stability).

---

## Reviewer 2 (Data & Rigor)

**Point 2: "Dataset description is weak. Real or synthetic?"**
> **Response:** We have completely overhauled the **Experimental Setup**. A new **Dataset Description Table (Table II)** explicitly details:
> *   **Source:** Real ERCOT Native Load (2023-2024).
> *   **Topology:** IEEE 30-bus.
> *   **Leakage Prevention:** Stratified temporal split (Train: Jan '23-Sep '24; Test: Oct-Dec '24).
> *   **Mechanics:** A new "How the Dataset Was Generated" section details the load scaling ($P_{new} = \lambda P_{base}$) and reactive power logic ($Q=0.4P$).

**Point 9: "Reproducibility is impossible with current text."**
> **Response:** We added a dedicated **Reproducibility** subsection and **Table VII**, which lists the exact software versions (PyPower 5.1.4, PyTorch 2.0.1), hardware specs, execution time, and random seed (42).

---

## Reviewer 3 (Presentation)

**Point 7: "Figures and formatting need polish."**
> **Response:** We performed a full pass on all tables to ensure IEEE compliance (proper headers, units, captions).

**Point 8: "Too many marketing words."**
> **Response:** We replaced vague terms like "novel" and "cutting-edge" with quantified claims. For example, instead of "improved performance," we now state "**23% higher fidelity**" and "**500x speedup**."

**Point 10: "Conclusion is weak."**
> **Response:** The **Conclusion** has been rewritten to mirror the Introduction's numbered contributions, summarizing the quantitative gains and the fundamental value of physics-validated explainability.

---
**Conclusion:** We believe these revisions have transformed the manuscript into a rigorous, reproducible, and operationally relevant contribution suitable for IEEE Transactions.
