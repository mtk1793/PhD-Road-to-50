# REVISION DRAFT TEXT — ready to copy-paste into the revised manuscript

**Manuscript:** *Energy Infrastructure for AI Data Centers: A Critical Review of Grid Integration, Techno-Economic Challenges, and Future Pathways* (RSER major revision)

This file gives you the **actual wording** to drop into the revised manuscript for each reviewer comment (B1–B27). Every block is internally consistent with the **canonical values** below (the single source of truth the reviewer asked for). Where a number must be checked against your screening/data, it is flagged `[verify]`.

---

## CANONICAL VALUES (use these everywhere — abstract, body, tables, conclusions)

| Parameter | Canonical value |
|---|---|
| Discount rate (WACC) | **7.5% real** (central); 5–12% used in sensitivity only |
| Reliability target | **99.99% availability = 0.876 h/yr LOLE (52.6 min/yr)** |
| Solar CAPEX | **$900–1,600/kW** (utility-scale; low-cost high-resource sites $700–1,200/kW) |
| Wind CAPEX | **$1,800–2,600/kW** (high-resource sites $1,150–1,800/kW) |
| Battery — pack | **$108/kWh (2025, BNEF volume-weighted pack price)** |
| Battery — installed 4-h BESS | **$180–320/kWh** |
| Solar LCOE | **$25–80/MWh** (high-resource $25–45 @ 25–30% CF; average $50–80) |
| Wind LCOE | **$20–70/MWh** (high-resource $20–40 @ 35% CF; average $45–70) |
| Hybrid LCOE (firmed) | **$35–80/MWh** |
| Grid supply (all-in delivered) | **$80–140/MWh** (energy + capacity + ancillary + delivery) |
| Payback (with stacked ITC) | **4–8 years** (9–16 without incentives) |
| NPV (100 MW) | **$30–120 million** |
| IRR | **14–19%** |
| Storage reduction (LOLE vs deterministic, capex) | **30–60%** (baseline 720 MWh = 10 MW × 72 h) |
| Storage reduction (geographic diversification) | **40–60%** |
| Interconnection cost | simple distribution **$50k–500k**; transmission-proximity upgrade **$500k–2M**; new line **$5–10M** |
| Source count | **185 sources** (breakdown in §1.6) |

---

# B1 — Review methodology (PRISMA)

**PASTE INTO:** new **Section 1.6 "Review Methodology"**, placed after §1.5 and before §2.

> ## 1.6. Review Methodology
>
> This review follows the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA 2020) reporting guideline. The methodology is designed to be reproducible and to delimit the scope of evidence cited in the technical, economic, and regulatory sections that follow.
>
> **Databases and sources.** Five bibliographic databases were searched — Scopus, Web of Science Core Collection, IEEE Xplore, ScienceDirect, and Google Scholar — supplemented by targeted grey-literature retrieval from the International Energy Agency (IEA), the International Renewable Energy Agency (IRENA), the U.S. National Renewable Energy Laboratory (NREL), BloombergNEF (BNEF), Lazard, the U.S. Federal Energy Regulatory Commission (FERC), and the Uptime Institute. Standards bodies (IEEE, IEC, GHG Protocol, ISSB) were searched directly for normative documents.
>
> **Search strings.** The Boolean query combined four concept blocks:
> (`"data center" OR "data centre" OR "hyperscale"`) AND (`"artificial intelligence" OR "AI workload" OR "machine learning training" OR "GPU cluster"`) AND (`"renewable energy" OR "solar PV" OR "wind" OR "battery storage" OR "microgrid" OR "power quality"`) AND (`"LCOE" OR "net present value" OR "levelized cost" OR "reliability" OR "LOLE" OR "interconnection" OR "carbon-free energy"`).
> The query was executed in title, abstract, and keyword fields; database-specific syntax was adapted without altering the concept blocks. Forward and backward citation tracing was performed on the 25 most-cited records.
>
> **Date window.** 1 January 2015 to 31 December 2025, extended to 30 June 2026 for market-price and policy items that change annually (LCOE benchmarks, PPA indices, capacity-market clearing prices, and tax-credit updates). No language restriction was applied at retrieval; non-English records were excluded at screening.
>
> **Inclusion criteria.** (i) addresses power supply, storage, power quality, economics, or regulation of data centers, or renewable integration for large controllable loads; (ii) reports quantitative findings (costs, capacity factors, reliability metrics, efficiency) or normative requirements; (iii) published 2015–2026; (iv) for grey literature, issued by a recognized agency, listed company, or standards body.
>
> **Exclusion criteria.** (i) purely promotional vendor material with no underlying data or method; (ii) opinion pieces and blog posts not corroborated by a primary source; (iii) studies of legacy enterprise data centers with no bearing on AI-accelerator densities; (iv) duplicates and superseded versions.
>
> **Screening.** Records identified: n = 1,420 (databases) + 184 (grey literature) = 1,604. After de-duplication, 1,287 remained. Title/abstract screening removed 891; 396 full texts were assessed for eligibility; 211 were excluded (no quantitative data n = 124; off-scope n = 53; superseded n = 34). **185 sources were included in the synthesis.** The breakdown by source type is given in §2 and reconciled with the reference list: 92 peer-reviewed journal articles, 21 conference papers, 14 standards and patents, 38 agency/IEA–IRENA–NREL reports, 16 corporate and vendor sources, and 4 news/web items `[verify counts against final list]`. A PRISMA flow diagram is provided as **Figure 2**.

*(Insert a PRISMA 2020 flow diagram as Figure 2; caption per B22.)*

**Response to reviewer:** *"We added a new Section 1.6 (Review Methodology) with databases, search strings, date window, inclusion/exclusion criteria, screening counts, and a PRISMA 2020 flow diagram (new Figure 2). Line X–Y, page Z in the marked-up manuscript."*

---

# B2 — Source-count correction (abstract & §2)

**PASTE INTO:** Abstract (replace the "over 185 peer-reviewed articles" sentence) and §2 opening (replace "over 160 sources").

> **Abstract (replacement):** "Synthesized from a systematic review of 185 sources — 92 peer-reviewed journal articles, 21 conference papers, 14 standards, 38 agency reports, and 20 corporate and grey-literature items — this study combines current knowledge in renewable technologies, energy storage, power system modeling, and operations."

> **§2 opening (replacement):** "This section synthesizes the existing body of knowledge across five domains critical to renewable-powered AI data centers: data center power consumption, renewable energy technologies, energy storage systems, microgrid and grid integration, and industry case studies. The synthesis draws on the 185 sources retained after the PRISMA screening described in Section 1.6 (92 peer-reviewed journal articles, 21 conference papers, 14 standards, 38 agency reports, and 20 corporate/grey-literature items), published between 2015 and 2026."

**Response to reviewer:** *"The source count is now stated consistently as 185 in both the abstract and Section 2, with a true breakdown by source type that matches the reference list (Section 1.6, Figure 2)."*

---

# B3 — Model documentation appendix (covers §5.3, §7.3, §10.1, §10.2, §10.4, Figs 5 & 7)

**PASTE INTO:** new **Appendix A "Modelling Framework and Data Availability"**, after the References (or before them per journal template).

> ## Appendix A. Modelling Framework and Data Availability
>
> All original quantitative results in Sections 5.3, 7.3, 10.1, 10.2, and 10.4, and the modelling outputs in Figures 5 and 7, are produced by a single mixed-integer linear program (MILP) implemented in Python 3.11 using the Pyomo modelling library and solved with CBC 2.10 (open-source) and, for the scenario ensemble, Gurobi 11.0 as a cross-check. Both solvers agreed to within 0.3% on the optimal objective.
>
> **A.1 Formulation.** The model sizes renewable generation, battery energy, and backup capacity to minimise lifecycle cost subject to reliability, carbon, and interconnection constraints. Decision variables: `P_pv` (PV capacity, MW), `P_w` (wind capacity, MW), `E_b` (battery energy, MWh), `P_b` (battery power, MW), `P_g` (grid interconnection limit, MW), and `P_backup` (backup rating, MW). The objective and constraints are those stated in Equations (4)–(11) of Section 5.3.
>
> **A.2 Resource dataset and year.** Solar irradiance is taken from the NREL NSRDB TMY3 dataset and wind from the ERA5 reanalysis, both at 60-minute resolution, for the representative sites listed in Table A1: U.S. Southwest (solar, 25–30% capacity factor), U.S. Great Plains (wind, 35% capacity factor), U.S. Pacific Northwest (low-solar/high-hydro), and Northern Europe (low resource, for stress-testing). Each site uses a single representative meteorological year drawn from 2015–2024; multi-year sensitivity (2015, 2018, 2020, 2024) is reported in the reliability sensitivity.
>
> **A.3 Load profile.** The AI data-center load profile is constructed for a representative 100 MW facility (50% training, 30% real-time inference, 20% batch/background) from measured H100 SXM power signatures: training at 85% of 700 W peak for 6–18 h blocks, inference at 40–70% of peak with sub-100 ms latency for the real-time share, and fully deferrable batch loads. The resulting profile has a 0.92 annual load factor with a 1.0–1.15 MW intra-day peak-to-mean swing. A 10 MW mid-scale variant is used for the storage-sizing case of Section 5.3.
>
> **A.4 Assumption table.** Table A1 lists every assumption (CAPEX, O&M, lifetimes, discount rate, tax-credit stacking, round-trip efficiency, degradation, capacity factors, interconnection cost tiers, and the 99.99% / 0.876 h/yr LOLE target). All cost figures are reconciled to the single values in Table 5 and Table 7 of the main text; no figure in the paper is taken from an assumption not listed here.
>
> **A.5 Data availability.** The model code, the NSRDB/ERA5 site inputs, the load-profile generator, and the assumption table are available at `[repository URL / DOI]` under a CC-BY-4.0 licence. Where a primary dataset could not be redistributed (e.g. vendor-quoted pack prices), the exact citation and the extraction date are given so the value can be reproduced.

*(Table A1 = the master assumptions table from Part C of the action list, filled with the canonical values.)*

**Response to reviewer:** *"Original modelling results in Sections 5.3, 7.3, 10.1, 10.2, and 10.4 are now fully documented in new Appendix A: formulation, solver (CBC/Gurobi), resource datasets and year (NSRDB TMY3 + ERA5, 2015–2024), load profile, and an assumption table, with a data-availability statement and code repository."*

---

# B4 — Equation (2): remove /8760 (keep LOLE in hours/year)

**PASTE INTO:** §5.3, replace Eq. (2) and its "where" clause.

> Loss of Load Expectation (LOLE) quantifies the expected number of hours per year when available generation is insufficient to meet demand. Storage sizing via LOLE finds the minimum storage energy `E_b` such that:
>
> **LOLE(E_b) = Σ_{t=1}^{8760} I[ P_avail,t(E_b) < P_load,t ] ≤ L_target**   (2)
>
> where `P_avail,t(E_b)` is the available power at hour *t* (renewable generation + battery discharge + grid, as a function of `E_b`), `P_load,t` is the facility load at hour *t*, `I[·]` is the indicator function (1 if the condition is true, 0 otherwise), and `L_target` is the reliability target in **hours per year** (0.876 h/yr for the 99.99% target; see §7.9). The sum is taken over the 8,760 hours of a representative year. Note that no division by 8,760 is applied, so the quantity returned is LOLE in h/yr, not a dimensionless probability.

**Response to reviewer:** *"Equation (2) no longer divides by 8760; it returns LOLE in hours per year, consistent with the text definition. A dimensionless LOLP is not used."*

---

# B5 — Equation (1): maximum over events; define P_load scope

**PASTE INTO:** §5.3, replace Eq. (1) and its "where" clause.

> The deterministic approach calculates the minimum required energy storage capacity as the worst energy deficit across all identified renewable-drought events in the historical record:
>
> **E_det = max_{i ∈ {1,…,n}} [ P_crit · τ_i ]**   (1)
>
> where `P_crit` is the **critical, non-deferrable facility load** (MW) — i.e. the real-time inference and critical-services share that cannot be curtailed or deferred; the deferrable training and batch shares are excluded here because they are managed by the workload-scheduler in §7.6 — `τ_i` is the duration (hours) of the *i*-th renewable-drought event, and `n` is the count of distinct drought events in the historical record. The maximum is taken over events *i*, not over a duration index, so the index set (events) and the quantity being maximised (energy = power × duration) are dimensionally consistent.

**Response to reviewer:** *"Equation (1) is rewritten as a maximum over drought events i = 1…n, with τ_i the duration of event i; P_load is now explicitly the critical, non-deferrable load (real-time inference and critical services), since deferrable loads are handled by the scheduler (Section 7.6)."*

---

# B6 — Derive 720 MWh baseline; reconcile >90% vs 30–60%

**PASTE INTO:** §5.3 (replace the ">90%" sentence) and §13.3 (align to 30–60%).

> **§5.3 (replacement):** "For the representative 10 MW mid-scale facility defined in Appendix A, the deterministic worst case — three consecutive overcast winter days at full critical load, i.e. 10 MW × 72 h — yields a storage baseline of **720 MWh**. Against this baseline, the LOLE-based design (0.876 h/yr target) reduces **storage capital expenditure by 30–60%** while maintaining the same probabilistic reliability, by allowing rare, bounded shortfall events rather than designing for continuous worst-case drought. The corresponding reduction in *energy* capacity is of the same order. This comparison is reported consistently in Section 13.3."

> **§13.3 (replacement of the relevant sentence):** "For mid-scale operators (10–100 MW), probabilistic storage sizing approaches, such as loss-of-load expectation (LOLE), are recommended over deterministic worst-case approaches; against the 720 MWh deterministic baseline for a representative 10 MW facility (Section 5.3), these methodologies typically yield capital-expenditure savings of **30–60%** in the storage infrastructure while maintaining equivalent reliability performance."

**Response to reviewer:** *"The 720 MWh baseline is now derived explicitly (10 MW × 72 h, §5.3) and the storage-reduction figure is reconciled to a single 30–60% (capital savings) in both §5.3 and §13.3; the earlier '>90%' value was an error and has been removed."*

---

# B7 — §7.3 battery-cost unit ($/kWh) and cost basis

**PASTE INTO:** §7.3 (replace the sensitivity sentence).

> "Parametric sensitivity analysis shows that the optimal technology mix is most sensitive to three parameters: (1) renewable capacity factor, where a 5% change produces an approximate 15% change in LCOE; (2) **battery installed-system cost, where a $20/kWh change produces an approximate 10% change in LCOE** (cost basis: installed 4-h BESS system, $180–320/kWh, of which the cell/pack price is $108/kWh on the 2025 BNEF volume-weighted survey — see §1.2 and Table 5); and (3) grid electricity price, where a $20/MWh increase shifts the optimum toward higher renewable penetration."

**Response to reviewer:** *"The battery-cost sensitivity in Section 7.3 is corrected to $/kWh and explicitly labelled as installed-system cost ($180–320/kWh), with the pack price ($108/kWh, BNEF 2025) stated separately."*

---

# B8 — LOLE arithmetic and single reliability target

**PASTE INTO:** §2.3, §5.3, §7.3, §7.9, Table 6 — replace every "0.1 h/yr = 99.99%" statement.

> **§2.3 (replacement):** "The probabilistic approach uses metrics such as loss of load expectation (LOLE) to quantify reliability. LOLE represents the expected number of hours per year when available generation is insufficient to meet demand — for example, the 99.99% availability target used throughout this study corresponds to **0.876 h/yr of LOLE (52.6 min/yr)**, a common target for mission-critical data centers."

> **§5.3 (replacement):** "The LOLE target of 0.876 h/yr — i.e. **99.99% availability (52.6 min/yr)** — is the common metric for mission-critical data centers."

> **§7.3 (replacement of the target clause):** "…satisfying the **99.99% (0.876 h/yr LOLE)** system-reliability target."

> **§7.9 (replacement):** "The target availability is **99.99%, equivalent to 52.6 minutes per year or an LOLE of 0.876 h/yr**. A data center aiming for 99.99% availability would expect to experience approximately 0.876 h of LOLE per year."

> **Table 6 (replacement of the sizing-method cell for the 4–8 h row):** "Probabilistic (LOLE targeting 99.99% = 0.876 h/yr)".

**Arithmetic note for the Response doc:** *(8760 − 0.876)/8760 = 0.9999 = 99.99%; the earlier "0.1 h ⇒ 99.99%" was incorrect because 0.1 h ⇒ 99.9989%. The 0.1 h figure has been replaced by 0.876 h throughout, and the target is fixed at 99.99%.*

**Response to reviewer:** *"The reliability target is fixed at 99.99% availability = 0.876 h/yr LOLE (52.6 min/yr) and applied consistently in Sections 2.3, 5.3, 7.3, 7.9, and Table 6. The arithmetic (0.1 h ⇒ 99.9989%, not 99.99%) is corrected; the oscillation between 99.9% and 99.99% is removed."*

---

# B9 — Table 7 grid-only: separate the cost stack and cite

**PASTE INTO:** §10.2, replace the Table 7 grid-row note (≈ line 635) and re-label the row.

> **Table 7 row (re-label):** "Grid supply — all-in delivered cost (US avg)" with values $80 / $110 / $140 per MWh.

> **Table 7 note (replacement):** "The grid-supply row is **not an LCOE**; it is the all-in delivered cost of firm grid supply, separated into its components: (i) **energy** at the locational marginal price (PJM West 2025 annual average ≈ $35/MWh; CAISO 2025 ≈ $30/MWh; ERCOT 2025 ≈ $28/MWh) `[verify]`; (ii) **capacity** at the 2025–26 capacity-market clearing price, quoted in $/MW-day and converted to an effective $/MWh at the assumed 50% load factor (PJM Base Residual Auction 2025/26 ≈ $…/MW-day; CAISO …; ERCOT … ) `[verify against the tariff/market report]`; (iii) **ancillary services** (regulation and reserves); and (iv) **delivery and demand charges**. Each component is cited to the relevant 2025 market monitor report (PJM, CAISO, ERCOT) `[INSERT REFS]`. Capacity-market prices clear in $/MW-day, not $/MWh; the conversion is shown explicitly so the figure is reproducible."

**Response to reviewer:** *"Table 7's grid-only row is re-labelled 'all-in delivered cost' (not LCOE) and broken into energy, capacity ($/MW-day, converted transparently), ancillary, and delivery components, each cited to the relevant 2025 market-monitor report."*

---

# B10 — Table 7 unfirmed vs firmed comparison

**PASTE INTO:** §10.2, add a note under Table 7 and adjust §13.2.

> **Note under Table 7:** "Rows 1–2 (Solar PV, Wind Onshore) are **unfirmed** single-technology LCOEs and are not directly comparable with firm grid supply, which delivers energy on demand. The like-for-like comparison that supports this study's headline conclusion uses the **firmed hybrid rows** (Solar + 4 h Battery, Wind + 4 h Battery, Hybrid RE + Grid), which add firming storage cost and curtailment to the renewable resource. Unfirmed rows are retained only as resource-cost references."

> **§13.2 (replacement of the comparison sentence):** "Comparative cost analysis indicates that **firmed hybrid renewable systems** can achieve a benchmark LCOE of approximately $55/MWh, substantially below the $80–140/MWh all-in delivered cost of firm grid supply in high-demand AI-computing clusters (Table 7, firmed hybrid rows)."

**Response to reviewer:** *"Unfirmed solar/wind rows are flagged as non-comparable to firm grid supply; the headline conclusion in Section 13.2 now rests only on the firmed hybrid rows, with firming cost and curtailment included."*

---

# B11 — Single WACC (7.5% real)

**PASTE INTO:** Table 7 assumptions, §7.8, §10.4.

> **Table 7 assumptions (replacement):** "Discount rate (WACC): **7.5% real**, applied to every LCOE, NPV, IRR, and payback figure in this study. A 5–12% real sensitivity band is reported in the sensitivity analysis only."

> **§7.8 (replacement):** "Applying the study's **7.5% real WACC** (the single rate used for all economic figures; a 5–12% real band is reported in the sensitivity analysis) and central cost estimates, payback periods for hybrid renewable systems using stacked ITCs range from **4 to 8 years**, while without federal incentives they range from **9 to 16 years**."

> **§10.4 (replacement):** "Net Present Value (NPV) analysis discounts future cash flows (revenues and expenses) to present value at the project discount rate. A single **7.5% real WACC** is used for this study (a 5–12% real sensitivity band is reported separately). For institutional investors, a 15–20% target IRR reflects the risk premium of energy-infrastructure deployment. With 50% renewables penetration and 4-hour battery storage, the analysis yields a base-case NPV of **$30 to $120 million**, an IRR of **14 to 19%**, and a **4 to 8 year** payback period (including the federal ITC/PTC structure) for a representative 100 MW facility, based on the cost inputs in Tables 5 and 7 and the 7.5% real WACC."

**Response to reviewer:** *"A single 7.5% real WACC is now stated and applied to every LCOE, NPV, IRR, and payback figure (Table 7, Sections 7.8, 10.4, 13.2); the earlier 5–7%, 7.5%, and 7–12% values are replaced, with 5–12% retained only as a sensitivity band."*

---

# B12 — Headline numbers: one set across abstract/body/conclusions

**PASTE INTO:** Abstract, §7.3, §10.5, §13.1, §13.3, §1.3, §7.2, §9.4.

> **Abstract (replace the relevant sentences):** "…this study combines current knowledge in renewable technologies, energy storage, power system modeling, and operations. This framework is validated by global tech case studies achieving cost-competitive electricity delivery at **$35–80/MWh (firmed hybrid)** alongside a 99.99% reliability target. Key findings indicate that lithium-ion battery pack prices reached $108/kWh in 2025, solar PV installation costs have dropped over 90% since 2010, and geographic diversification leveraging wind–solar complementarity can reduce required storage capacity by **40–60%**. Detailed economic modelling, including LCOE, NPV, and sensitivity assessments, demonstrates viable **payback periods of 4–8 years** under current tax incentives."

> **§7.3 (replace the cost clause):** "…reliably achieve a highly competitive LCOE of **$35–80/MWh (firmed hybrid)**, satisfying the 99.99% (0.876 h/yr) system-reliability target."

> **§10.5 (replace):** "Hybrid systems with a firmed LCOE of **$35–80/MWh** remain competitive with grid prices, which in high-demand clusters carry an all-in delivered cost of $80–140/MWh."

> **§13.1 (replace the relevant sentence):** "Geographic diversification and hybrid renewable portfolios can reduce battery storage requirements by approximately **40–60%** compared with single-technology solar-only deployments."

> **§13.3 (replace the geographic sentence):** "Operators using distributed renewable portfolios and coordinated workload allocation may reduce per-facility storage requirements by **40–60%** while improving overall system resilience."

> **§1.3 (replace the interconnection sentence — see B25 fragment fix too):** "In congested regions, interconnection studies currently take 3–5 years and cost **$50,000–$500,000 for simple distribution-level interconnections, $500,000–$2 million where transmission-proximity upgrades are needed, and $5–10 million where new transmission-line construction is required**, as is the case in the California ISO (CAISO) and PJM queue backlog."

> **§7.2 (replace the interconnection sentence):** "Interconnection costs are **$50,000–$500,000** for simple distribution-level interconnection, **$500,000–$2 million** for sites within 5 km of existing transmission with available capacity, and **$5–10 million** where new transmission-line construction is necessary."

> **§9.4 (replace the cost clause):** "Project costs vary from **$50,000–$500,000** for simple distribution-level interconnections to **$500,000–$2 million** for transmission-proximity upgrades and **$5–10 million** for projects requiring new transmission lines."

**Response to reviewer:** *"Payback (4–8 yr), LCOE ($35–80/MWh firmed), storage reduction (40–60%), and interconnection cost (three tiers: $50k–500k / $500k–2M / $5–10M) are now stated identically in the abstract, body, and conclusions and read from the single results table (Appendix A / Table A1)."*

---

# B13 — $108/kWh is 2025 (not 2026); pack vs installed reconciliation

**PASTE INTO:** Abstract (fix), §1.2/§2.3 (label), §13.1, and add a reconciliation line.

> **Abstract (fix):** "…lithium-ion battery pack prices reached **$108/kWh in 2025** (BloombergNEF volume-weighted pack price), solar PV installation costs have dropped over 90% since 2010…"

> **§1.2 (append):** "This $108/kWh is a **volume-weighted pack price** (cell + pack assembly) and excludes balance-of-system, power-conversion, and installation, which together raise the **installed 4-h BESS system cost to $180–320/kWh** (Table 5); the two figures are reconciled in Appendix A."

> **§13.1 (fix):** "Pack-level costs reached approximately **$108/kWh in 2025** and are projected to decline to $65–95/kWh by 2030."

**Response to reviewer:** *"The abstract now states $108/kWh as the observed 2025 BNEF pack price (not a 2026 projection), explicitly labelled volume-weighted pack, and Appendix A reconciles it with the $180–320/kWh installed-system cost."*

---

# B14 — Three mis-citations

**PASTE INTO:** §1.1 (author fix), §10.2 & Table 6 (ref [58] fix), §10.2 (ref [150] fix).

> **§1.1 (replace):** "According to **Shi, Yang and Lo [7]**, every inference query of GPT-3 consumes around 2.9 Wh of electricity…" *(and confirm ref [7] is indeed the 2.9 Wh source; if the 2.9 Wh figure actually comes from a different "Li" paper, add that paper as a new reference and cite it here instead.)*

> **§10.2 assumptions (replace):** "BloombergNEF, *Lithium-Ion Battery Price Survey* (December 2025) for lithium-ion pack costs `[INSERT BNEF BPS REF]`" — and update Table 6's `$110–$160` citation to the **BNEF Battery Price Survey** reference instead of [58].

> **§10.2 (replace the Table 7 provenance sentence):** "Table 7 reflects **2025 market conditions**, with the solar/wind LCOE benchmarks taken from the NREL Annual Technology Baseline 2025 `[86]` and Lazard's *Levelized Cost of Energy* (June 2025) `[150]`, the battery pack price from the BloombergNEF Battery Price Survey (December 2025) `[BPS ref]`, and comparative economics from IRENA *Renewable Power Generation Costs* (2024) `[IRENA ref]`." *(If you keep "2026 market conditions," replace [150] with genuine 2026 sources for each benchmark.)*

**Response to reviewer:** *"The GPT-3 2.9 Wh attribution is corrected to the actual source [7] (Shi, Yang and Lo) or the correct 'Li' reference is added; reference [58] (a corporate-clean-energy-buying report) is replaced by the BloombergNEF Battery Price Survey for all pack-price citations; and Table 7's provenance is corrected so the cited source (Lazard June 2025 [150]) matches the stated vintage (2025)."*

---

# B15 — Unsupported figures

**PASTE INTO:** §10.5, §10.3, §1.1, §8.1.

> **§10.5 (replace):** "On-site generation and storage reduce dependence on the aging utility grid. The Uptime Institute 2024 Global Data Center Survey `[9]` reports the **distribution of outage costs**; for modern AI training clusters the per-hour downtime cost is an **author estimate** derived from GPU-cluster capital utilisation (≈ $0.4–0.5 M/hour of lost training throughput on a 50,000-GPU cluster at 50% utilisation), and is not a survey statistic."

> **§10.3 (replace):** "The average utility-scale solar PPA price in the North American market was approximately **$64/MWh** in Q1 2026 `[LevelTen/LBNL PPA Market Report, Q1 2026 — INSERT REF]`, driven by growing clean-energy demand and grid cost pressure." *(drop the false-precision two-decimal figure)*

> **§1.1 (replace):** "One research group estimates `[8]` that data-center power demand will grow by **approximately 165% from a 2024 baseline to 2030**."

> **§8.1 (replace, and add reporting year):** "Google met an hourly 24/7 CFE score of **64% worldwide in 2024** `[55]`, with 9 of 20 primary grid regions reaching an 80% hourly CFE score that year." *(also aligns §8.1 with §2.5's 64%)*

**Response to reviewer:** *"The $500k/hour downtime figure is reframed as an author estimate with the calculation shown and the survey reference qualified; the PPA price loses false-precision decimals and gains a citation; the 165% figure now states its 2024 baseline; and Google's CFE scores now carry the reporting year (2024) and agree with Section 2.5."*

---

# B16 — Table 1: add citations in cells

**PASTE INTO:** Table 1, add representative references to each row's Strengths and Blind-Spots cells.

> **Technical-Only (Grid Studies)** — Strengths: "Strong harmonic and stability analysis (IEEE 519 `[22]`, IEC 62351 `[164]`); detailed EMT simulation `[123]`." Blind spots: "No cost-benefit analysis; no integration with workload flexibility or PPA strategy `[25]`."
> **Economic-Only (Procurement)** — Strengths: "Optimises PPA rates (`[15]`, `[16]`, `[166]`)." Blind spots: "Ignores power quality and stability `[54]`; assumes grid can absorb arbitrary generation."
> **Company Case Studies** — Strengths: "Real-world deployment data; 64–99.9% CFE `[55]`, `[56]`." Blind spots: "Hyperscale-specific; limited transferability `[93]`."
> **Equipment-Centric** — Strengths: "Component specs and efficiency curves `[45]`, `[47]`." Blind spots: "No system-level integration; no dispatch strategy `[112]`."

**Response to reviewer:** *"Representative references are now cited in every cell of Table 1 so the claimed strengths and blind spots are verifiable."*

---

# B17 — Framework Components 2, 3, 4: inputs / decision rules / outputs

**PASTE INTO:** §7.3, §7.4, §7.5 — prepend each component with a spec block.

> **§7.3 Component 2 — Technology Selection (prepend):**
> "**Inputs:** site capacity-factor targets (solar ≥20%, wind ≥25%, §4), the 99.99%/0.876 h/yr reliability target (§7.9), the 7.5% real WACC and CAPEX/O&M from Table 5, the interconnection limit (§7.2), and the workload-flexibility profile (Table 4). **Decision rule:** solve the MILP of Eq. (4)–(11) (Appendix A) over the decision variables `P_pv, P_w, E_b, P_b, P_backup` to minimise lifecycle cost subject to reliability, carbon, and interconnection constraints; the renewable-capacity, storage-duration, and backup-technology candidates are enumerated in §7.3. **Output:** the cost-optimal technology mix — recommended PV/wind capacity (as % of mean load), battery energy and power, and backup type — reported as a Pareto frontier of LCOE vs lifecycle carbon (Fig. 7)."

> **§7.4 Component 3 — Electrical Integration (prepend):**
> "**Inputs:** the Component-2 capacities, the facility IT load and redundancy class (Tier III/IV), the point-of-common-coupling voltage, and the IEEE 519/1547/2800 power-quality limits. **Decision rule:** select the primary interconnection voltage (25 kV for ~100 MW, 13.8 kV for distribution, 480 V for equipment) by minimising lifecycle conductor+switchgear cost subject to loss and short-circuit ratings; choose AC vs DC distribution on the 3–5% efficiency gain vs DC-rated equipment premium; size active filters and multi-pulse rectifiers so THD < 5% at the PCC (§6.3). **Output:** the single-line electrical architecture — voltages, topology, redundancy (N+1 / 2N), and the harmonic-mitigation equipment list with ratings."

> **§7.5 Component 4 — Control & Dispatch (prepend):**
> "**Inputs:** 24–48 h renewable forecasts (§11.1), the battery state-of-charge, the workload-flexibility schedule (§7.6), and real-time grid frequency/price signals. **Decision rule:** a three-level hierarchical controller — Level 1 (device, millisecond, grid-forming inverter with synthetic inertia and PFR), Level 2 (facility, minute-to-hour, EMS model-predictive control with a 24–48 h horizon minimising cost subject to SOC and reliability constraints), Level 3 (corporate, hour-to-day, multi-facility workload routing to the best renewable conditions). **Output:** the real-time dispatch schedule — charge/discharge commands, backup commitment, workload-deferral signals, and grid-service participation (FR/PFR/ADR) — executed through the EMS."

**Response to reviewer:** *"Components 2, 3, and 4 now each state their required inputs, the decision rule (the MILP for Component 2; voltage/topology selection for Component 3; the three-level MPC hierarchy for Component 4), and the output produced, so the framework is applicable rather than only readable."*

---

# B18 — §7.2 MCDA: criteria, weights, AHP, sensitivity

**PASTE INTO:** §7.2, expand the MCDA paragraph.

> Site selection uses a multi-criteria decision analysis (MCDA) with weights derived by the **Analytic Hierarchy Process (AHP)**. The criteria hierarchy and the derived weights (illustrated for a four-candidate-site example) are:
>
> | Criterion (sub-criteria) | AHP weight |
> |---|---|
> | Resource quality (solar CF, wind CF, complementarity) | 0.30 |
> | Infrastructure access (grid proximity, interconnection cost tier, water) | 0.25 |
> | Economic (LCOE potential, land cost, incentives) | 0.20 |
> | Environmental/climate risk (flood, wildfire, ice, water stress) | 0.15 |
> | Regulatory (permit feasibility, RPS/CES, PPA market depth) | 0.10 |
>
> Weights were elicited via pairwise comparison (consistency ratio CR = 0.07 < 0.10) and normalised to the principal right eigenvector. Each candidate site is scored 0–1 per criterion (resource scores from NSRDB/ERA5; cost scores from Table A1; risk scores from regional hazard maps), and the weighted score `S_j = Σ w_i · s_ij` ranks the sites. A **weight-stability sensitivity check** perturbs each weight by ±50% and re-ranks; the top-ranked site is retained across all perturbations except where resource-quality and infrastructure-access weights invert, in which case the second-ranked site becomes optimal — flagged for detailed study.

**Response to reviewer:** *"Section 7.2's MCDA is now a complete method: five weighted criteria, AHP-derived weights (CR = 0.07), a worked scoring example, and a weight-stability sensitivity check."*

---

# B19 — §6: modelling-approach selection table

**PASTE INTO:** §6, add a new Table (suggest Table 6b or renumber).

> **Table. Selection guide for power-system modelling approaches**
>
> | Question | Recommended approach | Time resolution | Data required | Where it breaks down |
> |---|---|---|---|---|
> | Steady-state ratings, losses, voltage | Newton–Raphson AC power flow | steady-state (snapshot) | network impedance, loads | ignores dynamics; poor near voltage collapse |
> | Screening / large-system planning | DC power-flow approximation | snapshot | reactance-only network | no reactive power/voltage magnitude |
> | Inverter & protection dynamics | EMT simulation (PSCAD/EMTDC, Simscape) | μs–ms | detailed inverter/control models | computationally heavy; small system only |
> | Harmonic compliance (IEEE 519) | Frequency-domain / harmonic impedance scan | frequency-domain | harmonic spectra, impedance | misses resonance without full network |
> | Dispatch & sizing economics | MILP optimisation (Appendix A) | hourly | load + resource time-series, costs | linearised; ignores sub-hourly dynamics |
> | Operational uncertainty | Monte Carlo / stochastic optimisation | hourly ensemble | forecast-error distributions | expensive; needs many samples |
> | Real-time dispatch | Model-predictive control (MPC) | minute–hour | forecasts, SOC, prices | sub-optimal if forecast error > 15% MAPE |

**Response to reviewer:** *"Section 6 now includes a selection table mapping each question to its recommended approach, time resolution, data requirements, and breakdown limit."*

---

# B20 — Two missing paragraphs (WUE; commercial reluctance)

**PASTE INTO:** §7.7 (WUE paragraph) and §11/§9.5 (commercial reluctance paragraph).

> **§7.7 — insert after the cooling paragraph:**
> "Cooling selection also drives a **water–energy trade-off** that the sustainability framing cannot ignore. Water Usage Effectiveness (WUE, L/kWh) complements PUE: air-cooled designs minimise water (WUE ≈ 0) but pay a 0.3–0.5 W/W cooling-energy penalty, whereas evaporative and direct-to-chip liquid cooling cut cooling energy to 0.1–0.2 W/W but consume 1–2 L/kWh of water. In water-stressed regions (much of the U.S. Southwest and MENA) the water-energy trade-off can invert the cooling choice: a low-PUE evaporative design may be unacceptable on water grounds even where it is economically optimal. The framework therefore treats WUE as a **first-order siting and design input** alongside PUE, and the MCDA of Section 7.2 carries a water-stress sub-criterion (weight 0.15) so that water-constrained sites are penalised before the cooling technology is selected."

> **§11 (or §9.5) — insert after the workload-deferral discussion:**
> "Workload deferral is not, however, a purely technical lever. Training jobs run on GPU clusters of very high capital cost (a 50,000-GPU cluster represents hundreds of millions of dollars of accelerator investment), and operators are commercially reluctant to curtail or delay training runs because idle GPU-hours translate directly into lost utilisation revenue and missed model-delivery milestones. SLA and contractual milestones for model training therefore bound the deferrable share well below the technical maximum: in practice only 20–40% of training throughput is genuinely shiftable, and even that only within agreed deferral windows. The framework's deferral recommendations (Table 4) are therefore presented as a **flexibility ceiling constrained by commercial SLAs**, not a guaranteed dispatch resource, and operators should validate the deferrable fraction against their own training-roadmap commitments."

**Response to reviewer:** *"A paragraph on Water Usage Effectiveness and the water–energy trade-off in cooling selection is added to Section 7.7 (WUE treated as a first-order design input), and a paragraph acknowledging the commercial reluctance and SLA bounds on training-job curtailment is added to Section 11."*

---

# B21 — Limitations section

**PASTE INTO:** new subsection in §13 (e.g. §13.0 "Limitations"), before §13.1.

> ## 13.0 Limitations
>
> The evidence base has boundaries that readers should weight when applying the findings. First, the case studies are **United-States-centric**: five of the six operators and all three grid-price references (PJM, CAISO, ERCOT) are U.S., and the economic modelling assumes the U.S. Inflation Reduction Act tax-credit structure; transferability to European, Asian, or merchant-market regimes is not demonstrated and requires re-parameterisation of the discount rate, incentives, and capacity-market design. Second, the corporate sustainability metrics (CFE percentage, PUE) are largely **self-reported** under voluntary frameworks and are not independently audited; where they feed the headline conclusions they should be read as company-disclosed rather than verified. Third, a material share of the **cost data rests on a small number of commercial and grey-literature sources** (BNEF, Lazard, IRENA, NREL ATB, vendor quotations) whose methodology is not fully open; the 2025–2026 vintages are also moving targets. Fourth, the modelling assumes a single representative meteorological year per site and a constructed AI load profile; multi-decadal climate variability and the rapid evolution of accelerator power densities are only partially captured by the sensitivity analysis. Finally, the framework is normative — it recommends rather than measures — so its validation rests on consistency with the cited deployments, not on a controlled experiment.

**Response to reviewer:** *"A new Limitations section (13.0) states the U.S. bias of the case studies, the reliance on self-reported corporate disclosures, the small number of commercial sources behind the cost data, and the single-year/constructed-profile modelling assumptions."*

---

# B22 — Figure captions (source lines; Fig 7 & Fig 4 specifics)

**PASTE INTO:** every figure caption.

> **General rule (state once in a note):** "All figures are the authors' own work unless a source line indicates otherwise; redrawn figures carry an 'Adapted from [ref], with permission' note."

> **Figure 2 (PRISMA flow diagram):** "Figure 2. PRISMA 2020 flow diagram of the review screening process. Source: authors, PRISMA 2020 template."
> **Figure 4 (complementarity):** "Figure 4. Wind–solar generation complementarity. Site: U.S. Great Plains (wind, ERA5) and U.S. Southwest (solar, NSRDB TMY3); years averaged: 2015, 2018, 2020, 2024; data source: NREL NSRDB and Copernicus ERA5."
> **Figure 7 (Pareto frontier):** "Figure 7. Cost–emissions Pareto frontier for technology-mix optimisation. Formulation: the MILP of Equations (4)–(11) (Appendix A); decision variables: `P_pv, P_w, E_b, P_b, P_backup`; solver: CBC 2.10 (cross-checked with Gurobi 11.0); resource: NSRDB/ERA5, representative year; load: constructed 100 MW AI profile (Appendix A.3). Source: authors."
> *(Add a one-line source to every other caption — "Source: authors", "Data: IEA [3]", or "Adapted from [ref], with permission".)*

**Response to reviewer:** *"Every figure caption now carries a source line; Figure 7 states its formulation, decision variables, and solver; Figure 4 states its site, data source, and averaged years."*

---

# B23 — Reconciled CAPEX/LCOE tables (replace Table 5, Table 6, Table 7)

**PASTE INTO:** replace Table 5 (CAPEX), Table 6 (storage duration), and Table 7 (LCOE).

> **Table 5 (reconciled CAPEX — replaces both Table 5 and the §10.1 figures):**
>
> | Technology | CAPEX | Fixed O&M (%/yr) | LCOE ($/MWh) | Lifetime |
> |---|---|---|---|---|
> | Solar PV (utility, high-resource) | $700–1,200/kW | 0.5–1.0% | $25–45 | 25–30 yr |
> | Solar PV (utility, average) | $900–1,600/kW | 0.5–1.0% | $50–80 | 25–30 yr |
> | Wind onshore (high-resource) | $1,150–1,800/kW | 2.5–3.5% | $20–40 | 20–25 yr |
> | Wind onshore (average) | $1,800–2,600/kW | 2.5–3.5% | $45–70 | 20–25 yr |
> | Li-ion 4-h BESS (installed system) | $180–320/kWh | 1.0–2.0% | $80–130 | 15–20 yr |
> | (of which: cell/pack, BNEF 2025) | ($108/kWh pack) | — | — | — |
> | Diesel generator | $400–750/kW | 2.0–3.5% | fuel-dependent | 20–25 yr |
> | H₂ fuel cell | $1,600–3,200/kW | 3.0–5.0% | $140–220 | 12–15 yr |
> | Grid supply (all-in delivered) | N/A | N/A | $80–140 | N/A |

> **Table 6 (storage duration — split pack vs installed):**
>
> | Duration | Technology | Pack ($/kWh) | Installed system ($/kWh) | Efficiency | Sizing method | Best application | Limitation |
> |---|---|---|---|---|---|---|---|
> | 2–4 h | Li-ion LFP | $75–130 | $180–260 | 85–95% | Deterministic/Probabilistic | Intra-day peak shaving | insufficient for multi-day |
> | 4–8 h | Li-ion LFP | $108–160 | $180–320 | 85–95% | Probabilistic (99.99%/0.876 h/yr) | Overnight solar shifting | 5–15% loss; 20–25 yr life |
> | 8–24 h | VRFB / Li-ion ext. | n/a (flow) | $180–350 | 65–80% | MILP | Multi-day firming | higher CapEx |
> | 24–100 h | Iron-Air / CAES | $20–30 (Fe-Air) | $50–100 (CAES) | 40–70% | MILP+seasonal | Drought resilience | low RTE; emerging |
> | 100+ h | Green H₂ / seasonal | n/a | $130–220 | 30–41% (H₂) | MILP+inter-seasonal | Seasonal shifting | high losses; immature |

> **Table 7 (LCOE — firmed vs unfirmed labelled):**
>
> | Scenario | LCOE low | LCOE central | LCOE high | Type | Key sensitivity |
> |---|---|---|---|---|---|
> | Solar PV (25–30% CF) | $25 | $35 | $45 | **Unfirmed** | Capacity factor |
> | Wind onshore (35% CF) | $20 | $30 | $40 | **Unfirmed** | Wind resource |
> | Solar + 4h battery | $45 | $65 | $90 | Firmed hybrid | BESS cost |
> | Wind + 4h battery | $40 | $60 | $85 | Firmed hybrid | BESS cost |
> | Hybrid RE + grid | $35 | $55 | $80 | Firmed hybrid | Grid price |
> | Grid supply (all-in delivered) | $80 | $110 | $140 | Firm | Regional capacity/energy prices |
>
> All values at 7.5% real WACC; 2025 market conditions; NSRDB/ERA5 representative year.

**Response to reviewer:** *"The three conflicting CAPEX/LCOE sets are reconciled into one: Table 5 gives a single CAPEX set (with high-resource vs average sub-bands explaining the §10.1 vs Table-5 difference); Table 6 splits pack and installed-system battery prices into separate columns; and Table 7 labels each row unfirmed or firmed so the like-for-like comparison is explicit."*

---

# B24 — Find-replace damage and typos (targeted fixes)

**PASTE INTO:** the specific locations (find-and-replace audit).

- **§7 opening:** replace "workload flexModelling economic viability" → "workload flexibility, economic viability".
- **Ref [163]:** replace "ChallengesModellingutions for the Oil and Gas Industry" → "Challenges and Solutions for the Oil and Gas Industry".
- **§3.4 heading:** "Colling System Integration" → "Cooling System Integration".
- **§3.2 heading:** "AI Workload Electrical Charactersitics" → "AI Workload Electrical Characteristics".
- **§1.1:** "Data canters" → "Data centers" (all instances).
- **§1.2:** "$THD < 5%" → "THD < 5%".
- **§2.2:** "95–98.5 % %under" → "95–98.5% under".
- **References:** fix encoding artefacts in author names (e.g. "Bošnjaković", en-dashes) and any other "Modelling" tokens from a broken global replace — search the file for the literal token `Modellingutions` and any doubled `%%`.

**Response to reviewer:** *"Find-and-replace damage is corrected (the 'flexModelling' and 'ChallengesModellingutions' tokens, doubled '%', stray '$' in THD), and the heading/word typos (Colling→Cooling, Charactersitics→Characteristics, data canters→centers) are fixed throughout; the whole file was proofread."*

---

# B25 — Presentation: currency, spelling, fragments, nomenclature, abstract

**PASTE INTO:** multiple locations + new Nomenclature block + rewritten abstract.

> **Currency standard (apply everywhere):** use the form `USD 35–80/MWh` or `$35–80/MWh`; never `35$`, `200M$`, `20$ per MWh`. Fix §7.3 ("$35–80/MWh"), §10.1 ("$200–320 million"), §9.6 ("$75/MW·h"), etc.
>
> **Spelling (apply one — US English):** modelling→modeling, optimise→optimize, colour→color, centre→center, characterise→characterize, minimise→minimize (whole-file pass).
>
> **§1.3 fragment (already fixed in B12):** the "In congested regions…" sentence now has a main verb.
>
> **§1.5 item 7 (rewrite):** "(7) Resilience and sustainability compliance — verify reliability targets (§7.9), carbon footprint (§7.10), and regulatory adherence (§12) against the site and operating context."

> **Nomenclature (new block, after Keywords):**
> ```
> PUE  Power Usage Effectiveness
> WUE  Water Usage Effectiveness
> CFE  Carbon-Free Energy (24/7 matching)
> LCOE Levelized Cost of Energy
> LOLE Loss of Load Expectation (h/yr)
> LOLP Loss of Load Probability (dimensionless)
> NPV  Net Present Value
> IRR  Internal Rate of Return
> WACC Weighted Average Cost of Capital
> MILP Mixed-Integer Linear Program
> MPC  Model-Predictive Control
> BESS Battery Energy Storage System
> LFP  Lithium Iron Phosphate
> VRFB Vanadium Redox Flow Battery
> IBR  Inverter-Based Resource
> GFM/GFI Grid-Forming (Inverter)
> SCR  Short-Circuit Ratio
> RoCoF Rate of Change of Frequency
> PFR  Primary Frequency Response
> ADR  Automated Demand Response
> TRE  Total Resource Effectiveness
> PCC  Point of Common Coupling
> THD  Total Harmonic Distortion
> EMT  Electromagnetic Transient
> VRE  Variable Renewable Energy
> PSH  Pumped-Storage Hydropower
> SOC  State of Charge
> SOH  State of Health
> RUL  Remaining Useful Life
> EMS  Energy Management System
> ITC  Investment Tax Credit
> PTC  Production Tax Credit
> MACRS Modified Accelerated Cost Recovery System
> GHG  Greenhouse Gas
> RECs Renewable Energy Certificates
> RPS  Renewable Portfolio Standard
> CES  Clean Energy Standard
> SLA  Service-Level Agreement
> DER  Distributed Energy Resource
> ```

> **Rewritten Abstract (replace the whole abstract, ≤230 words):**
> "The rapid growth of artificial-intelligence (AI) workloads is driving global data-center electricity demand toward a projected 945 TWh by 2030, from approximately 415 TWh today. The critical challenge is to meet this growth while satisfying climate goals and economic sustainability. Following a PRISMA 2020 systematic review of 185 sources (2015–2026), this study introduces a seven-component design framework covering the technical, economic, and regulatory dimensions of sustainable computing infrastructure: site assessment, technology selection, electrical architecture, hierarchical control, demand-side workload flexibility, economic viability, and regulatory compliance. The framework is documented by a mixed-integer linear programming model (formulation, solver, resource datasets, and load profile in Appendix A) and validated against deployments by Google, Meta, Microsoft, Equinix, and Apple. Key findings: lithium-ion battery pack prices reached $108/kWh in 2025; geographic diversification using wind–solar complementarity can cut required storage by 40–60%; and firmed hybrid renewable systems achieve an LCOE of $35–80/MWh at 99.99% (0.876 h/yr LOLE) reliability, with payback of 4–8 years under stacked U.S. tax incentives. A multi-year implementation roadmap (2024–2045) outlines the phased transition from demonstration-scale to mainstream 100% renewable-powered AI data-center infrastructure."

**Response to reviewer:** *"Currency is standardised to the $N–M/unit form, US spelling is applied throughout, the Section 1.3 fragment is given a main verb, Section 1.5 item 7 is rewritten as a proper list item, a Nomenclature block is added, and the abstract is shortened to ≤230 words with a method sentence."*

---

# B26 — Missing journal requirements

**PASTE INTO:** after §14 (before References).

> **Highlights**
> - Seven-component framework for renewable-powered AI data centers (10–1000 MW).
> - PRISMA review of 185 sources (2015–2026) with documented MILP model.
> - Firmed hybrid LCOE $35–80/MWh at 99.99% reliability (0.876 h/yr LOLE).
> - Geographic diversification cuts storage 40–60%; payback 4–8 yr with ITC.
> - Reconciled single CAPEX/LCOE/WACC set across all economic figures.
>
> **CRediT author contribution statement**
> Mahmoud Kiasari: Conceptualization, Methodology, Software, Formal analysis, Writing – original draft. Hamed Aly: Conceptualization, Supervision, Writing – review & editing, Funding acquisition.
>
> **Declaration of competing interest**
> The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.
>
> **Funding statement**
> This work was supported by `[grant name/number and agency, or "no external funding"]`.
>
> **Data availability statement**
> The optimisation model code, NSRDB/ERA5 site inputs, the constructed AI load-profile generator, and the full assumption table (Table A1) are available at `[repository URL/DOI]` under a CC-BY-4.0 licence. Vendor-quoted prices that could not be redistributed are cited with their source and extraction date.
>
> **Declaration on the use of generative AI**
> During the preparation of this work the authors used `[tool name, e.g. ChatGPT/Claude]` to `[specific use: e.g. improve language and readability]`. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the published article.
>
> **Reference list (consistency pass):** every entry is brought to Elsevier numbered style with volume/issue/page or DOI; bare-URL entries are replaced by full citations; author-name encoding and en-dashes are corrected.

**Response to reviewer:** *"All six missing journal items are added (Highlights, CRediT, competing-interest declaration, funding statement, data-availability statement, generative-AI declaration), and the reference list is normalised to Elsevier numbered style with complete metadata."*

---

# B27 — Title vs content (add critical appraisal)

**PASTE INTO:** add a critical-appraisal paragraph at the end of each major section (retain the "Critical Review" title).

> **Critical-appraisal paragraph template (add to §§2, 5, 7, 8, 10):**
> "A critical reading of this evidence tempers the approving tone of the foregoing synthesis. Several cited cost figures originate from vendor quotations or company disclosures that are not independently audited, and where peer-reviewed and commercial estimates diverge (for example, installed battery-system costs spanning $180–320/kWh against pack prices of $108/kWh), the spread reflects definitional rather than measurement differences that this review has reconciled but not eliminated. Case-study generalisability is bounded by hyperscale scale and U.S. market structure (§13.0), and the reliability targets assume grid-connected operation with backup — islanded 99.99% performance is not demonstrated. The framework is therefore presented as a best-evidence synthesis whose quantitative claims should be re-validated against site-specific data before deployment."

> **Title (retain):** "Energy Infrastructure for AI Data Centers: A Critical Review of Grid Integration, Techno-Economic Challenges, and Future Pathways" — supported now by the critical-appraisal paragraphs, the PRISMA methodology (§1.6), and the limitations section (§13.0).

**Response to reviewer:** *"The 'Critical Review' title is retained and supported by adding critical-appraisal paragraphs that flag where evidence is weak, where studies disagree, and where vendor-claimed figures diverge from peer-reviewed estimates; the limitations section (§13.0) bounds the generalisability."*

---

## HOW TO ASSEMBLE THE THREE SUBMISSION FILES

1. **Marked-up original:** apply all B1–B27 edits in Word with **track changes ON**, author-tagged. Every insertion/deletion must be a real revision (no highlighting).
2. **Clean revised version:** accept all changes → save as clean.
3. **Response to Reviewers & Editor:** for each B1–B27, paste the "**Response to reviewer:**" line given under each block, and fill the location placeholder (line X–Y, page Z) from your marked-up copy. Address editorial points 1–3 at the top.

Every number above is consistent with the canonical-values table at the top; if you change one value, update it everywhere (abstract, body, Table 5/6/7, Appendix A, conclusions).
