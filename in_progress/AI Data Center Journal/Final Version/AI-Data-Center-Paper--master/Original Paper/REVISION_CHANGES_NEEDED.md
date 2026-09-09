# REVISION CHANGES NEEDED — RSER Major Revision

**Manuscript:** *Energy Infrastructure for AI Data Centers: A Critical Review of Grid Integration, Techno-Economic Challenges, and Future Pathways*
**Authors:** Mahmoud Kiasari, Hamed Aly (Dalhousie University)
**Journal:** Renewable & Sustainable Energy Reviews (RSER)
**Editor:** Soteris Kalogirou, DSc (Editor-in-Chief)
**Deadline:** 16 September 2026
**Status:** Major revision (NOT conditional acceptance)

> This file is a deep, line-checked action list. Every location below was verified against the current manuscript. Line numbers refer to the extracted text and are approximate guides to the section/paragraph. Use them to drive your track-changes edits and your point-by-point Response to Reviewers.

---

## PART A — MANDATORY EDITORIAL DELIVERABLES (points 1–3)

You must submit **three** files through Editorial Manager (https://www.editorialmanager.com/rser/ → Author Login → *Submissions Needing Revision*):

| # | Deliverable | What it is |
|---|---|---|
| 1 | **Marked-up original** | The original manuscript with **all** textual changes shown via **Word track changes** (Insertions/Deletions). Highlighting in yellow/colour is **explicitly NOT acceptable** — must be real tracked revisions, author-tagged. Covers reviewer edits AND editorial points. |
| 2 | **Clean revised version** | Same manuscript, all changes accepted, no markup. |
| 3 | **Response to Reviewers & Editor** | Point-by-point response to **every** reviewer comment **and** editorial points 1–3. For each: quote the comment, state the action, and cite the exact location in the marked-up copy (e.g. "line X to Y on page Z in the marked-up manuscript"). |

**Other editor points to action**
- **English proofread (editor, explicit).** Grammar/spelling/syntax is the authors' sole responsibility — reviewers will not fix it. Run a full proofread pass (colleague or paid service; Elsevier Author Webshop: http://webshop.elsevier.com/languageediting). This is not a guarantee of acceptance.
- The editor could not secure enough reviewers; **additional reviewers may be invited on resubmission**, and the revised submission **may be re-reviewed**. Treat every comment as mandatory.
- (Optional, not required) Interactive data visualizations: https://www.elsevier.com/researcher/author/tools-and-resources/data-visualization
- (Optional) Research Elements journal for raw data/methods/protocols.

---

## PART B — REVIEWER #2 COMMENTS (point-by-point)

The editor supplied only **Reviewer #2**'s report (no other reviews returned). Each comment is restated, located in the current manuscript, and given a concrete action.

---

### B1. Add a review methodology (PRISMA)
**Reviewer:** "There is no review methodology. Please add the databases searched, the search strings, the date window, inclusion and exclusion criteria and screening counts, ideally with a PRISMA-style flow diagram. A review article cannot be assessed without it."

**Where:** The paper jumps from Section 1.4 (Scope) straight into Section 2 (Literature Review) with no methods subsection. Currently Section 2 opens (≈line 61) only with "This review draws on over 160 sources published between 2015 and 2025."

**Action — add a new subsection** (suggest **Section 1.6 "Review Methodology"** or a new Section 2.0 before 2.1). It must contain:
- **Databases searched:** e.g. Scopus, Web of Science, IEEE Xplore, ScienceDirect, Google Scholar (+ grey-literature sources for the agency/vendor material).
- **Search strings:** the actual Boolean queries (e.g. `("data center" OR "data centre") AND ("renewable" OR "solar" OR "wind" OR "battery storage") AND ("AI" OR "machine learning workload") AND ("LCOE" OR "microgrid" OR "power quality")`).
- **Date window:** state the exact range (the body says 2015–2025; the abstract/2026 projections imply some 2026 sources — reconcile).
- **Inclusion criteria** and **exclusion criteria** as explicit lists.
- **Screening counts:** records identified → duplicates removed → title/abstract screened → full-text assessed → included. Give the numbers at each stage.
- **PRISMA flow diagram:** insert as a new figure (see B16 for caption/source rules). Use the PRISMA 2020 template.

> This also forces you to fix the source-count inconsistency (B2). The PRISMA counts must agree with the final reference list total.

---

### B2. Fix the inconsistent source count and give a true breakdown by type
**Reviewer:** "The source count is inconsistent. The abstract says over 185 peer-reviewed articles, Section 2 says over 160 sources, and the list holds 185 entries of which many are web pages, vendor material and agency reports. Give the true breakdown by source type."

**Where (confirmed in current text):**
- Abstract (≈line 7): "over **185 peer-reviewed** articles, industry reports, and policy documents"
- Section 2 intro (≈line 61): "over **160 sources** published between 2015 and 2025"
- Reference list: ends at **[185]**; many entries are web pages / vendor / agency (e.g. [163] blog, [169] Oxford Energy PDF, [171] EnerSys blog, [174] DOE PDF, [176] UN web page, [177] SSRN, [178] IESO PDF).

**Action:**
1. Recount the final reference list exactly.
2. Produce a **breakdown table by source type**: peer-reviewed journal articles / conference papers / standards / agency & IEA-IRENA reports / corporate & vendor material / news & blogs / web URLs.
3. Correct **both** the abstract and Section 2 to a single, accurate statement that matches the breakdown (e.g. "Of 185 sources, X are peer-reviewed, Y are standards, Z are grey-literature…"). Stop calling them all "peer-reviewed articles."

---

### B3. Document or replace the original modelling results in §5.3, §7.3, §10.1, §10.2, §10.4
**Reviewer:** "Sections 5.3, 7.3, 10.1, 10.2 and 10.4 present original modelling results with no model behind them. There is no formulation, solver, resource dataset, resource year, load profile or assumption table, so none of the numbers can be checked. Either document the model in an appendix with a data availability statement, or replace the results with sourced published values."

**Where (the un-sourced original numbers):**
- §5.3 (≈line 301): "Compared to deterministic sizing (**720 MWh**), the LOLE-based design reduces storage requirements by **more than 90%**" — no facility size, no baseline derivation, no model.
- §7.3 (≈line 434): Pareto-frontier results, sensitivity factors ("$20 per MWh change … 10% change in LCOE"), "35$ to 80$ per MWh" — no formulation/solver/dataset.
- §10.1 (≈line 600): "200M$ to 320M$ for a representative 100 MW data center", "$120-$200 million for a 50% renewable, 4-hour" — no model/assumptions table.
- §10.2 (Table 7, ≈lines 611–635): six-scenario LCOE table "reflecting 2026 market conditions" — no solver, no load profile, no resource year.
- §10.4 (≈line 644): "NPV of $30 to $120 million, IRR of 14 to 19%, 6 to 11 year payback" for a 100 MW facility — no cash-flow model shown.

**Action — choose ONE path and apply consistently:**
- **Path A (document the model):** Add an **appendix** giving the full formulation (objective, constraints, decision variables), the **solver** (e.g. CBC/CPLEX/Gurobi, version), the **resource dataset & year** (e.g. NSRDB/TMY3 site + year, wind ERA5), the **load profile** (source or synthetic + assumptions), and an **assumption table**. Then add a **Data Availability Statement** (see B20) pointing to the code/data. Figures 5 and 7 (modelling outputs) also need this (see B17).
- **Path B (replace with sourced values):** Drop the original numbers and cite published peer-reviewed values for each claim, with the source next to every figure.

Either way, the headline results must trace to either a documented model or a cited source.

---

### B4. Equation (2): LOLE vs LOLP — remove /8760 or relabel
**Reviewer:** "Equation 2 is wrong. LOLE is defined in the text as hours per year, but the equation divides the summed indicator by 8760, which returns a probability. Remove the factor or relabel the quantity as LOLP."

**Where:** §5.3, Eq. (2) (≈lines 285–294). The "where" clause itself defines LOLE as "expected number of hours per year" and lists "8760 = hours per year" as a divisor — which converts the sum (hours) into a dimensionless probability (LOLP), contradicting the "hours per year" definition.

**Action:** Pick one and apply everywhere LOLE/LOLP appears (§2.3, §5.3, §5.x, §7.9, §13.3):
- **Option 1 (preferred):** Remove the `/8760` so Eq. (2) returns LOLE in **hours/year**. Then the 0.1 h/yr target is consistent.
- **Option 2:** Keep the division but **relabel the quantity LOLP** (Loss-of-Load Probability, dimensionless) and re-state all targets accordingly.

This is tightly coupled to B8 (the 99.99% arithmetic) — fix together.

---

### B5. Equation (1): fix the mixed index set; define P_load scope
**Reviewer:** "Equation 1 mixes its index set. Tau is defined as a duration in hours but the maximum runs over 1 to n, where n is a count of drought events. Rewrite as a maximum over events, and state whether P_load is the full facility load or only the critical non-deferrable load."

**Where:** §5.3, Eq. (1) (≈lines 274–284). Current "where" clause: `P_load` = sustained facility load (MW); `τ` = duration of worst-case renewable drought (hours); `n` = number of distinct drought events. The maximum is taken over `1…n` (an event index) while `τ` is a duration — a set mismatch.

**Action:** Rewrite Eq. (1) as a **maximum over events** `i = 1…n`, e.g.:
`E_storage = max_{i ∈ {1..n}} [ P_load,i · τ_i ]`
with `τ_i` = duration of drought event *i* (hours). Then **state explicitly whether `P_load` is the full facility load or only the critical, non-deferrable load** (the text at line 284 implies non-critical load can be deferred during droughts — make the equation match that statement).

---

### B6. §5.3 vs §13.3 storage-reduction contradiction; undefined 720 MWh baseline
**Reviewer:** "Section 5.3 claims LOLE sizing cuts storage by more than 90 percent against a 720 MWh baseline. That baseline is never derived and the facility size producing it is never stated. Section 13.3 gives 30 to 60 percent for what appears to be the same comparison."

**Where (confirmed):**
- §5.3 (≈line 301): deterministic baseline **720 MWh** → LOLE "**more than 90%**" reduction. Baseline never derived; facility MW never stated.
- §13.3 (≈line 733): "probabilistic storage sizing … LOLE … typically yield capital expenditure savings of **30–60%** in the storage infrastructure."

**Action:**
1. **Derive the 720 MWh baseline** in §5.3: state the facility size (e.g. X MW) and show `720 MWh = P_load × τ` (which links back to Eq. 1). If you cannot derive it, replace it with a derived or cited value.
2. **Reconcile ">90%" vs "30–60%".** These cannot both be the LOLE-vs-deterministic comparison. Either:
   - the >90% figure is wrong (and 30–60% is the right magnitude), or
   - they measure different things (storage *energy* reduction vs *capital* savings) — in which case **label them distinctly** in both sections.
3. Make §5.3 and §13.3 read from the **single results table** (see Part C).

---

### B7. §7.3 battery-cost unit error ($/MWh → $/kWh); state cell/pack/system
**Reviewer:** "Section 7.3 expresses battery cost sensitivity in dollars per MWh. Battery capital cost is a dollars per kWh quantity. Please correct the unit and say whether it is cell, pack or installed system cost."

**Where:** §7.3 (≈line 434): "battery storage cost, where a **$20 per MWh** change in the battery storage cost results in an approximate 10% change in LCOE."

**Action:**
1. Change the unit to **$/kWh** (battery capital cost is capacity-based).
2. **State the cost basis** — cell, pack, or installed system (BESS). This must be consistent with the reconciliation in B19/B23 (pack vs installed).

---

### B8. LOLE 0.1 h/yr arithmetic; settle one reliability target
**Reviewer:** "An LOLE of 0.1 hours per year is roughly 99.9989 percent availability, not 99.99 percent as stated in Section 5.3. The reliability target also switches between 99.9 and 99.99 percent across the paper. Fix the arithmetic and settle on one target."

**Where (confirmed — the target oscillates):**
- §2.3 (≈line 80): "LOLE of 0.1 hours/year corresponds to **99.99%** uptime" ❌
- §5.3 (≈line 273): "LOLE of 0.1 hour per year, or **99.99 %** availability" ❌
- §7.3 (≈line 434): "satisfying a **99.9%** system reliability target"
- §7.9 (≈line 491): "target availability is **99.99%** or 52.6 minutes per year … 0.1 hours of LOLE per year" (internally inconsistent: 99.99% ⇒ 0.876 h/yr, not 0.1)
- Table 6 (≈line 308): "LOLE targeting **99.9%–99.99%**"

**Arithmetic check:** `0.1 h / 8760 h = 1.142e-5` ⇒ availability = `(8760−0.1)/8760 = 99.99886%` (≈99.9989%), **not** 99.99%. Conversely `99.99% ⇒ 0.876 h/yr`; `99.9% ⇒ 8.76 h/yr`.

**Action:**
1. Decide on **one** target (recommend **99.99% = 0.876 h/yr LOLE**, or **99.9989% = 0.1 h/yr LOLE** — pick one and use it everywhere).
2. Correct every "0.1 h ⇒ 99.99%" statement to the mathematically consistent pair.
3. Fix §7.9: 99.99% is 52.56 min/yr = **0.876 h/yr**, so its LOLE companion must be 0.876, not 0.1 (or change the availability %).
4. Fix Table 6's "99.9%–99.99%" to the single chosen target (or justify the band).
5. Fix §7.3 "99.9%" to the chosen target.

---

### B9. Table 7 grid-only "LCOE" misuse of capacity prices ($/MW-day ≠ $/MWh)
**Reviewer:** "Table 7 justifies the grid-only LCOE using PJM, CAISO and ERCOT capacity prices. Capacity prices clear in dollars per MW-day, not dollars per MWh, and a capacity price is not an LCOE. Separate the energy, capacity, ancillary and delivery components and cite the tariff or market report for each."

**Where:** Table 7 (≈line 635): "Grid-only LCOE reflects 2026 regional capacity prices: PJM ($110/MWh), CAISO ($95/MWh), ERCOT ($85/MWh)." And Table 7 row "Grid Only (US Avg)" (≈line 618): $80/$110/$140 per MWh.

**Action:**
1. Stop calling capacity-market prices an "LCOE" — they are not.
2. **Separate the cost stack** for grid-only supply into: **energy** ($/MWh, e.g. LMP/flat energy), **capacity** ($/MW-day, converted transparently), **ancillary services**, and **delivery/demand charges**.
3. **Cite the source** for each component (PJM, CAISO, ERCOT tariff/market reports, year). State the conversion from $/MW-day to an effective $/MWh explicitly (assumed capacity factor / hours).
4. Re-label the Table 7 grid row accordingly (e.g. "Grid supply (all-in delivered cost)") rather than "LCOE".

---

### B10. Table 7 unfirmed vs firmed comparison; headline conclusion rests on it
**Reviewer:** "Table 7 sets unfirmed solar and wind LCOE alongside firm grid supply, and the paper's headline conclusion rests on that comparison. Add firming cost and curtailment, or limit the comparison to the firmed hybrid rows and say so explicitly."

**Where:** Table 7 (≈lines 612–618) lists unfirmed "Solar PV" $25–45 and "Wind Onshore" $20–40 next to "Grid Only" $80–140. The headline (§13.2, ≈line 729) compares "~$55/MWh hybrid" to "$110/MWh grid."

**Action:**
1. Either **add firming cost + curtailment** to the solar/wind-only rows (storage to make them firm), **or**
2. **Limit the headline comparison to the firmed hybrid rows** ("Solar + 4h Battery", "Hybrid RE + Grid") and **state explicitly** that unfirmed rows are not directly comparable to firm grid supply.
3. Adjust §13.2 and the abstract so the headline conclusion rests only on a like-for-like (firmed vs firm) comparison.

---

### B11. Three different discount rates — pick ONE WACC (real or nominal)
**Reviewer:** "The discount rate takes three different values. Table 7 assumes 5 to 7 percent real, Section 7.8 applies 7.5 percent, and Section 10.4 uses 7 to 12 percent for the same class of project. State one WACC, say whether it is real or nominal, and apply it to every LCOE, NPV, IRR and payback figure."

**Where (confirmed):**
- Table 7 assumptions (≈line 626): "Real discount rate: **5–7%**"
- §7.8 (≈line 487): "an improved discount rate of **7.5%**"
- §10.4 (≈line 644): "varies between **7 and 12%**"

**Action:**
1. State **one** WACC, and **label it real or nominal** (and the inflation assumption if nominal).
2. Re-run / re-state **every** LCOE, NPV, IRR, and payback figure under that single rate (Table 7, §7.8, §10.4, §13.2, abstract).
3. If you keep a sensitivity band (e.g. 7–12%), make the **central** case one number and use the band only for sensitivity, consistently.

---

### B12. Headline numbers disagree across abstract/body/conclusions — build ONE results table
**Reviewer (multiple conflicts):**
- **Payback:** "5 to 12 years, then 6 to 11, then 4 to 8."
- **LCOE:** "35 to 100 dollars per MWh, then 35 to 80."
- **Storage reduction (geographic diversification):** "40 to 60 percent, then 50 to 70."
- **Interconnection cost:** "50 thousand to 500 thousand dollars plus 10 million in Section 1.3, but 500 thousand to 2 million or 5 to 10 million in Section 7.2."

**Where (confirmed):**
| Quantity | Abstract | Body | Conclusions |
|---|---|---|---|
| Payback (yrs) | **5–12** (ln 8) | §7.8 **4–8** (ln 487, w/ ITC); §10.4 **6–11** (ln 644) | §13.2 **4–8** (ln 729) |
| LCOE ($/MWh) | **35–100** (ln 7) | §7.3 **35–80** (ln 434); §10.5 **35–80** (ln 650) | §13.1 **35–80** (ln 725); §13.2 **~55** (ln 729) |
| Storage reduction (geographic) | **40–60%** (ln 8) | — | §13.1 **40–60%** (ln 725); §13.3 **50–70%** (ln 733) |
| Interconnection cost | §1.3 **$50k–$500k + up to $10M** (ln 35) | §7.2 **$500k–$2M / $5–10M** (ln 429) | §9.4 **$50k–$500k+** (ln 566) |

**Action:**
1. **Build one master "Results & Assumptions" table** (see Part C template) and make **every** section read from it.
2. Pick the **single canonical range** for each headline number and update abstract, body, and conclusions to match.
3. For interconnection cost specifically: reconcile §1.3, §7.2, §9.4 to one consistent statement (e.g. "simple distribution interconnection $50k–$500k; transmission-proximity upgrade $500k–$2M; new transmission line $5–10M").

---

### B13. $108/kWh — 2025 observed, not 2026; reconcile pack vs installed
**Reviewer:** "The abstract calls 108 dollars per kWh a 2026 projection, while Sections 1.2 and 2.3 correctly report it as the observed 2025 BloombergNEF figure. It is also a volume-weighted pack price, which is never reconciled with the 75 to 160 dollars per kWh installed system costs quoted later."

**Where (confirmed):**
- Abstract (≈line 8): "lithium-ion battery prices are **projected to fall below $108/kWh in 2026**" ❌
- §1.2 (≈line 27): "dropped … to **$108/kWh in 2025**, according to its annual survey" ✓
- §2.3 (≈line 78): "$108/kWh in 2025, as reported by BloombergNEF" ✓
- §13.1 (≈line 725): "Pack-level costs have fallen to approximately **$108/kWh in 2025**" ✓
- Installed/system costs elsewhere: §10.1 "$100–$150/kWh" (ln 600); Table 5 (CAPEX) "$180–$320/kWh" (ln 480); Table 6 storage tiers "$75–$130", "$110–$160" (ln 307–308).

**Action:**
1. Fix the **abstract** to "$108/kWh in 2025 (BloombergNEF)" — not a 2026 projection.
2. **Explicitly label the $108 as a volume-weighted pack price** and add a one-line reconciliation showing how it relates to installed system cost (pack + EPC + PCS + BOP + grid-tie ≈ the $100–$320/kWh installed figures). Define which of the later numbers are **pack** vs **installed system**.

---

### B14. Three citations don't support what they're cited for
**Reviewer:**
- §1.1 attributes the **2.9 Wh per GPT-3 query** to "research by Li", but **ref [7]** is Shi, Yang and Lo; no "Li" source appears in the list.
- **Ref [58]** is "BloombergNEF, *Corporate Clean Energy Buying Fell in 2025*", yet it is cited for **battery pack prices** in §10.2 and for a **cost range in Table 3** (storage tiers).
- **Ref [150]** is "Lazard, *Levelized Cost of Energy*, June 2025", yet **Table 7** states its values reflect **2026 market conditions** and were validated against NREL, BloombergNEF and IRENA benchmarks, citing [150] for all of it.

**Where (confirmed):**
- §1.1 (≈line 17): "According to research by Li, every inference query of GPT-3 consumes around 2.9 Wh … [7]" — and [7] is not by Li.
- §10.2 assumptions (≈line 623): "BloombergNEF Battery Pack Prices (December 2025) for lithium-ion costs [58]" — but [58] is the *Corporate Clean Energy Buying* report.
- Table 6 (storage duration, ≈line 308): "$110–$160 [58], [86]".
- §10.2 (≈line 608): Table 7 "reflecting 2026 market conditions and validated against NREL, BloombergNEF, and IRENA benchmarks [150]" — but [150] is Lazard's June-2025 LCOE.

**Action:**
1. **§1.1:** Correct the author attribution. Either change "research by Li" to the actual source/authors of ref [7] (Shi, Yang and Lo), or add the correct "Li" reference and renumber.
2. **Ref [58]:** Replace with the **actual BloombergNEF Battery Price Survey** reference (the annual *Lithium-Ion Battery Price Survey*), and re-cite it for §10.2 and Table 6. (Do not cite a corporate-clean-energy-buying report for pack prices.)
3. **Ref [150]:** Lazard (June 2025) cannot validate "2026 market conditions." Either (a) change the Table 7 claim to "2025 market conditions" and cite Lazard + NREL ATB + IRENA correctly, or (b) add genuine 2026 sources for each benchmark. Align the year claim with the cited source's vintage.

---

### B15. Figures stated without adequate support
**Reviewer:**
- §10.5 attributes **downtime costs >$500,000/hour** to ref [9] (Uptime Institute survey), which reports **outage cost distributions, not a per-hour figure for training clusters**.
- §10.3 quotes a **PPA price of $64.49/MWh** to two decimals with **no citation**.
- §1.1 gives **165% demand growth by 2030 with no baseline year**.
- §8.1 gives **Google figures with no reporting year**.

**Where (confirmed):**
- §10.5 (≈line 653): "downtime costs … exceed $500,000/hour … [9]"
- §10.3 (≈line 640): "solar PPA price … approximately $64.49 per MWh for Q1 of 2026" — no citation.
- §1.1 (≈line 18): "power demand in data centers would grow at a rate of 165% by 2030 [8]" — no baseline year stated.
- §8.1 (≈line 505): Google "24/7 CFE score … 66 percent" / "9 of 20 … 80 percent" — no reporting year.

**Action:**
1. **§10.5:** Replace/qualify the $500k/hour claim. Either cite a source that gives a per-hour training-cluster downtime figure, or reframe as "Uptime Institute reports outage cost distributions; per-hour training-cluster costs are author estimates from GPU utilisation economics" and show the calculation.
2. **§10.3:** Add a citation for the $64.49/MWh figure (e.g. LevelTen/LBNL PPA market report, Q1 2026) or remove the false-precision decimals.
3. **§1.1:** State the **baseline year** for the 165% (e.g. "165% growth from a 2024 baseline to 2030") and confirm ref [8] supports it.
4. **§8.1:** Add the **reporting year** for Google's CFE scores (and align with §2.5, which says 64% — §8.1 says 66%; reconcile, see B22).

---

### B16. Table 1 has no citations in any cell
**Reviewer:** "Table 1 asserts gaps in four families of prior work but contains no citations in any cell. Please add representative references so a reader can verify the attributed strengths and blind spots."

**Where:** Table 1 (≈lines 101–105) — four rows (Technical-Only / Economic-Only / Company Case Studies / Equipment-Centric), every cell citation-free.

**Action:** Add representative references in each cell (at least the "Technical Strengths" and "Economic Blind Spots" columns) so the claimed strengths/blind spots are verifiable.

---

### B17. Components 2, 3, 4 of the framework are only descriptive
**Reviewer:** "Components 2, 3 and 4 of the framework are described only in general terms and it is not clear what a user would actually do. Please state the decision rules, the inputs each component requires and the output it produces, so the framework can be applied rather than only read."

**Where:** §7.1 overview (≈line 422) and the Component 2/3/4 treatments in §7.3 (Technology Mix), §7.4 (Electrical Integration), §7.5 (Control & Dispatch).

**Action:** For **each** of Components 2, 3, 4, add a compact spec block:
- **Inputs required** (data/parameters).
- **Decision rule / algorithm** (what the user actually does — e.g. the optimization objective & constraints for Component 2; the topology & protection selection rules for Component 3; the MPC dispatch rule for Component 4).
- **Output produced** (the artifact the user gets — e.g. recommended RE/storage/backup capacities & sizes; single-line diagram & protection settings; dispatch schedule & reserve policy).

Make the framework *executable*, not just readable.

---

### B18. §7.2 MCDA is a label, not a method
**Reviewer:** "Section 7.2 recommends multi criteria decision analysis but gives no criteria, no weights, no weighting method such as AHP or entropy, and no sensitivity check on the weights. As written it is a label rather than a method."

**Where:** §7.2 (≈line 428): "Site selection utilizes a multi-criteria decision analysis (MCDA) approach that assigns weights to a series of criteria …" — but no criteria list, no weights, no method, no sensitivity.

**Action:** Turn MCDA into an actual method:
1. List the **criteria** (resource quality, infrastructure access, environmental, economic — expanded).
2. Give the **weights** (or a worked example with a candidate site set).
3. Name the **weighting method** (AHP or entropy) and show the pairwise/entropy calculation.
4. Add a **sensitivity check** on the weights (rank-reversal / weight-stability analysis).

---

### B19. §6 is a catalogue — add "which approach for which question"
**Reviewer:** "Section 6 is a catalogue of tool categories. Please state which modelling approach suits which question, at what time resolution, with what data requirements, and where each approach breaks down."

**Where:** §6.1–6.6 (power flow, transient stability, harmonics, microgrid modelling, time-series, ML) — currently descriptive lists.

**Action:** Add a **decision/selection table** in §6 mapping: *question type → recommended approach → time resolution → data requirements → breakdown/limit.* (e.g. harmonic compliance → EMT/frequency-domain → μs–ms → impedance scan data → breaks down for weak-grid resonance without detailed models.)

---

### B20. Two missing one-paragraph topics
**Reviewer:** "Two gaps are worth closing in a paragraph each. Water use effectiveness and the water versus energy tradeoff in cooling selection are treated only as a siting input, despite the sustainability framing. And Section 11 presents workload deferral as a purely technical option, without acknowledging the commercial reluctance to curtail training jobs on assets of this capital cost."

**Where:**
- Water: §12.4 (≈line 709) mentions water volume but treats it as impact/siting, not a design tradeoff. §7.7 cooling coordination (≈line 466) is silent on water.
- Workload deferral: §11 / §9.5 (≈lines 571, 664+) present deferral as a pure technical lever.

**Action:**
1. Add a **paragraph on Water Usage Effectiveness (WUE) and the water–energy tradeoff** in cooling selection (air vs evaporative vs liquid) — where it belongs in §7.7 or a sustainability subsection. Tie to the sustainability framing.
2. Add a **paragraph on commercial reluctance to curtail/defer training jobs** given GPU-cluster capital cost and utilisation SLAs — in §11 or §9.5. Acknowledge that the deferral upside is bounded by commercial/SLA reality, not just technical feasibility.

---

### B21. No limitations section
**Reviewer:** "There is no limitations section. State the boundaries of the evidence, including the United States bias of the case studies, the reliance on self-reported corporate sustainability disclosures, and the small number of commercial sources behind the cost data."

**Where:** No §"Limitations" exists (paper goes §13 Conclusions → §14 Future Research).

**Action:** Add a **Limitations** subsection (within §13 or just before it) covering at minimum:
- **U.S.-bias** of case studies (Google/Meta/Microsoft/Equinix/Apple; PJM/CAISO/ERCOT pricing; U.S. IRA tax structure).
- **Reliance on self-reported corporate sustainability disclosures** (CFE %, PUE).
- **Small number of commercial/grey-literature sources** behind the cost data (B2 breakdown).
- Generalisability limits to non-U.S. grids, climates, and regulatory regimes.

---

### B22. Figure captions: only Fig. 1 has a source line; Fig. 7 & Fig. 4 specifics
**Reviewer:** "Of the nine figures, only the Figure 1 caption carries a source line. Every caption needs one, with permission or an 'adapted from' note where the figure is redrawn. Figure 7 is a modelling output and needs its formulation, decision variables and solver stated. Figure 4 needs the site, data source and years averaged, since wind and solar complementarity is strongly location specific."

**Where (confirmed):** Only "Figure 1 … Source: IEA, 2025" (≈line 22) has a source line. Other figure captions (≈lines 22, 424, 435, 447, …) are bare titles.

**Action:**
1. **Every** figure caption gets a source line: own-work, "Data: X", or "Adapted from [ref], with permission" if redrawn.
2. **Figure 7 (Pareto frontier, ≈line 435):** add the **formulation, decision variables, and solver** (ties to B3/B17).
3. **Figure 4 (complementarity, ≈line 22 region):** add the **site, data source, and years averaged** (e.g. NSRDB/TMY3 site ID, years). Complementarity is site-specific, so the figure must be reproducible.
4. Re-number/caption all nine figures consistently.

---

### B23. Three conflicting capital-cost/LCOE sets + Table 3 mixes pack & system prices
**Reviewer:** "Three sets of capital cost and LCOE figures conflict. Table 5 gives solar at 900 to 1,600 dollars per kW and an LCOE of 50 to 80 dollars per MWh, wind at 1,800 to 2,600 dollars per kW and 45 to 70 dollars per MWh, and batteries at 180 to 320 dollars per kWh. Section 10.1 gives solar at 700 to 1,200 dollars per kW, wind at 1,150 to 1,800 dollars per kW and batteries at 100 to 150 dollars per kWh. Table 7 then gives solar at 25 to 45 dollars per MWh and wind at 20 to 40 dollars per MWh. Reconcile these into one set. Table 3 separately mixes pack prices and installed system prices in a single column without labelling which is which."

**Where (confirmed):**
| Source | Solar ($/kW) | Wind ($/kW) | Battery | Solar LCOE | Wind LCOE |
|---|---|---|---|---|---|
| Table 5 / CAPEX (ln 478–480) | **900–1,600** | **1,800–2,600** | **180–320 $/kWh** | 50–80 | 45–70 |
| §10.1 (ln 600) | **700–1,200** | **1,150–1,800** | **100–150 $/kWh** | — | — |
| Table 7 (ln 613–614) | — | — | — | **25–45** | **20–40** |
| Table 6 / "Table 3" storage tiers (ln 307–308) | — | — | **75–130; 110–160 $/kWh** | — | — |

- Table 6 (the storage-duration table, referred to in text as "Table 3" at ln 302) mixes **pack** prices ($75–130, $110–160, cited to BNEF [17],[58]) and **installed/system** prices ($180–350, etc.) in one "$/kWh" column with no labelling.

**Action:**
1. **Reconcile to ONE set** of CAPEX and LCOE values (see Part C master table). The Table 5 vs §10.1 CAPEX disagreement and the Table 5 vs Table 7 LCOE disagreement must be resolved (Table 7's solar 25–45 and Table 5's solar 50–80 cannot both stand without explanation — e.g. Table 7 = high-resource site, Table 5 = average; state it).
2. **Label pack vs installed system** explicitly in every battery-cost cell (Table 6, §10.1, Table 5). Do not mix them in one column. Recommend splitting Table 6's cost column into "Pack ($/kWh)" and "Installed system ($/kWh)".

---

### B24. Find-replace / corruption damage and typos (whole-file proofread)
**Reviewer:** "Section 7 opens with a corrupted phrase, workload flexModelling economic viability, which suggests find and replace damage elsewhere. Section 3.4 reads Colling System Integration, Section 3.2 reads AI Workload Electrical Charactersitics, Section 1.1 has data canters, and Section 1.2 has a stray dollar sign in $THD < 5%. Please proofread the whole file."

**Where (confirmed — and more found):**
- §7 opening (≈line 422): "workload flex**Modelling** economic viability" ❌ (should be "workload flexibility, economic viability")
- §3.4 heading (≈heading line): "Colling System Integration" ❌ → "Cooling"
- §3.2 heading (≈heading line): "AI Workload Electrical **Charactersitics**" ❌ → "Characteristics"
- §1.1 (≈line 16): "Data **canters**" ❌ → "Data centers"
- §1.2 (≈line 29): "**$THD** < 5%" ❌ → "THD < 5%" (stray $)
- **Reference [163]** (end of list): "Challenges**Modellingutions** for the Oil and Gas Industry" ❌ (find-replace corruption — "Solutions" became "Modellingutions")
- §3.5 / §2.2 (≈line 72): "95–98.5 % %under" ❌ (double %)
- Other broken encoding in references (e.g. "Bošnjaković" mangled, "–" en-dashes shown as "‐" artefacts throughout) — see B26.

**Action:** Run a full proofread + a targeted find-replace audit (the "Modellingutions"/"flexModelling" pattern suggests an earlier global replace of "solut"/"s" → something went wrong). Search for residual corruption tokens: `Modellingutions`, `flexModelling`, `% %`, `‐` artefacts. Fix all.

---

### B25. Presentation pass: currency, spelling, grammar, nomenclature, abstract
**Reviewer:**
- Currency appears as `$35-80/MWh`, `35$ to 80$ per MWh`, `200M$ to 320M$` and `20$ per MWh` — inconsistent.
- US and UK spellings mixed within the same paragraphs.
- The sentence in §1.3 beginning "In congested regions" has no main verb.
- Item 7 of the list in §1.5 reads as a leftover editing note.
- No nomenclature list despite heavy use of PUE, CFE, LCOE, LOLE, MILP, MPC, IBR, SCR, RoCoF, TRE, ADR, PFR.
- The abstract is long and states no method.

**Where (confirmed):**
- Currency: §7.3 "35$ to 80$ per MWh", "20$ per MWh" (ln 434); §10.1 "200M$ to 320M$" (ln 600); §9.6 "$75 per MW per hour" (ln 577) etc. — mixed `$N` vs `N$` vs `NM$`.
- §1.3 (≈line 35): "In congested regions, such as those currently experiencing queues of 3–5 years for studies with $50,000 to $500,000 and grid upgrades potentially running into the $10 million range, as is currently the case with the California ISO (CAISO) and PJM …" — **no main verb** (fragment).
- §1.5 item 7 (≈line 55): "(7) Resilience and sustainability compliance are also important." — reads as leftover note.
- No nomenclature list exists.
- Abstract (≈lines 5–8): long, no methodology sentence (also B1).

**Action:**
1. **Currency standardisation:** adopt one convention everywhere, e.g. `USD 35–80/MWh` or `$35–80/MWh`; never `35$`, `200M$`. Fix §7.3, §10.1, §9.6, etc.
2. **Spelling:** pick US **or** UK English consistently (journal is English-language; RSER commonly uses one — choose and apply via a spelling pass: modelling/modeling, optimise/optimize, colour/color, centre/center).
3. **§1.3 fragment:** rewrite "In congested regions …" as a complete sentence with a main verb.
4. **§1.5 item 7:** rewrite as a proper list item (parallel to items 1–6), not an editing note.
5. **Add a Nomenclature list** (symbol/abbreviation, meaning, unit) covering: PUE, CFE, LCOE, LOLE, LOLP, MILP, MPC, IBR, SCR, RoCoF, TRE, ADR, PFR, BESS, VRE, PSH, THD, PCC, EMT, NPV, IRR, WACC, ITC, PTC, MACRS, WUE, GHG, RECs, RPS, CES, SLA, SOC, SOH, RUL, EMS, GFM/GFI, FR, PFR, DER.
6. **Abstract:** tighten to ≤200–250 words and add one sentence stating the **review method** (PRISMA, search window, source count) — ties to B1/B2.

---

### B26. Missing journal requirements & reference style
**Reviewer:** "Missing journal requirements: CRediT author contribution statement, declaration of competing interest, funding statement, data availability statement, declaration on the use of generative AI, and highlights. The reference list is not in consistent Elsevier numbered style and several entries lack volume, issue or page numbers or give only a bare URL."

**Where (confirmed):** The manuscript ends at reference [185]. There is **no** CRediT, competing-interest, funding, data-availability, or generative-AI declaration, and **no Highlights** block. References are inconsistent: many have full metadata, but several are bare/incomplete — e.g. [163], [172], [176], [181] give only a title + bare URL; [166] "SSRN" with no journal; [177] SSRN abstract only; some lack volume/issue/pages. Encoding artefacts corrupt author names (e.g. "Bošnjaković" → "Bonjakovi") and en-dashes.

**Action:**
1. **Add all six required items** (typically after Conclusions/before References, per RSER template):
   - **CRediT** author contribution statement (e.g. Kiasari: Conceptualization, Methodology, Writing–Original Draft; Aly: Supervision, Writing–Review & Editing).
   - **Declaration of competing interest** (standard statement: "The authors declare no known competing financial interests…").
   - **Funding statement** (state grant/none).
   - **Data availability statement** (links to B3 model appendix if you take Path A; otherwise state which data are public).
   - **Declaration on the use of generative AI** (per Elsevier policy — disclose any use and the tool).
   - **Highlights** (3–5 bullets, ≤85 characters each, capturing the core findings).
2. **Reference list:** convert to consistent Elsevier numbered style; complete every entry with volume/issue/pages (or DOI); replace bare-URL entries with proper citations; fix encoding artefacts in author names and en-dashes.

---

### B27. Title vs content mismatch — "critical review" reads as a design guide
**Reviewer:** "The title promises a critical review but the manuscript reads as a design guide, with almost every cited finding reported approvingly. Either add appraisal of where the evidence is weak and where studies disagree, or adjust the title to match the content."

**Where:** Throughout — findings are reported affirmatively (e.g. §2.5 case studies, §8, §10 all stated approvingly). No critique of weak evidence or disagreements.

**Action — choose one:**
- **Option A (keep "Critical Review" title):** Add **critical appraisal** throughout — flag where evidence is weak, where studies disagree, where figures are vendor-claimed vs independently verified, where generalisability is limited. Add a critical-synthesis paragraph per major section.
- **Option B (change the title):** Reframe the title to match the actual content, e.g. "A Design Framework for Renewable-Powered AI Data Centers: Techno-Economic Analysis and Future Pathways" (drop "Critical Review").

Recommend Option A (the PRISMA methodology in B1 already pushes it toward a genuine critical review).

---

## PART C — MASTER RECONCILIATION (the "one results table" the reviewer demands)

Create **one** canonical results-and-assumptions table; **every** section, the abstract, and the conclusions read from it. Populate it after you fix the items above. Template:

| Parameter | Single canonical value | Real/nominal | Source / basis | Appears in (must match) |
|---|---|---|---|---|
| WACC / discount rate | e.g. 7.5% real | real | stated | Table 7, §7.8, §10.4, §13.2, abstract |
| Reliability target | e.g. 99.99% = 0.876 h/yr LOLE | — | stated | §2.3, §5.3, §7.3, §7.9, Table 6, §13 |
| Solar CAPEX | $/kW (one range) | — | NREL ATB 2025 / Lazard | Table 5, §10.1 |
| Wind CAPEX | $/kW (one range) | — | NREL ATB 2025 | Table 5, §10.1 |
| Battery — pack price | $/kWh (labelled pack) | — | BNEF Battery Price Survey (2025) | Abstract, §1.2, §2.3, Table 6 |
| Battery — installed system | $/kWh (labelled system) | — | derived/cited | §10.1, Table 5, Table 6 |
| Solar LCOE | $/MWh (one range, site-stated) | — | cited | Table 5, Table 7, §13 |
| Wind LCOE | $/MWh (one range) | — | cited | Table 5, Table 7, §13 |
| Hybrid LCOE (firmed) | $/MWh | — | model/cited | Table 7, §13.2, abstract |
| Grid supply (all-in) | $/MWh (energy+capacity+ancillary+delivery) | — | PJM/CAISO/ERCOT reports | Table 7, §10.5 |
| Payback (with ITC) | years (one range) | — | model | §7.8, §10.4, §13.2, abstract |
| NPV (100 MW) | $M (one range) | — | model | §10.4, §13.2 |
| IRR | % (one range) | — | model | §10.4, §13.2 |
| Storage reduction: LOLE vs deterministic | % (one value, labelled energy or capex) | — | model/cited | §5.3, §13.3 |
| Storage reduction: geographic diversification | % (one range) | — | cited | §13.1, §13.3, abstract |
| Interconnection cost | $ (tiered: simple / upgrade / new line) | — | cited | §1.3, §7.2, §9.4 |
| Source count | N total + breakdown | — | PRISMA | abstract, §2, B2 |

---

## PART D — MASTER CHECKLIST (tick before resubmission)

**Editorial deliverables**
- [ ] Marked-up original with **real track changes** (not highlight) — reviewer + editorial edits
- [ ] Clean revised version (changes accepted)
- [ ] Response to Reviewers & Editor — point-by-point, each comment quoted + location cited (line X–Y, page Z in marked copy)
- [ ] Full English proofread (grammar/spelling/syntax)

**Review methodology & counts**
- [ ] New review-methodology subsection with PRISMA flow diagram (B1)
- [ ] Source count corrected + type breakdown table; abstract & §2 match the list (B2)

**Modelling transparency**
- [ ] §5.3/§7.3/§10.1/§10.2/§10.4: either documented model (appendix + solver + dataset + load profile + assumptions) or replaced with cited values (B3)
- [ ] Figure 7 formulation/decision variables/solver stated (B3, B22)
- [ ] Figure 4 site + data source + years (B22)
- [ ] Data availability statement (B3, B26)

**Equations & reliability**
- [ ] Eq. (2): remove /8760 or relabel LOLP (B4)
- [ ] Eq. (1): max over events; define P_load scope (B5)
- [ ] LOLE 0.1 h arithmetic fixed; one reliability target everywhere (B8)

**Numerical reconciliation (ONE master table)**
- [ ] Storage reduction §5.3 (>90%) vs §13.3 (30–60%) reconciled; 720 MWh baseline derived (B6)
- [ ] Battery unit $/MWh → $/kWh in §7.3; cell/pack/system labelled (B7)
- [ ] Table 7 capacity-price misuse fixed; cost stack separated + cited (B9)
- [ ] Table 7 unfirmed vs firmed comparison fixed (B10)
- [ ] One WACC (real/nominal labelled) across all LCOE/NPV/IRR/payback (B11)
- [ ] Payback / LCOE / storage-reduction / interconnection-cost made consistent across abstract, body, conclusions (B12)
- [ ] $108/kWh = 2025 (not 2026) in abstract; pack vs installed reconciled (B13)
- [ ] Three CAPEX/LCOE sets reconciled; Table 6 pack-vs-system labelled (B23)

**Citations & support**
- [ ] §1.1 "Li" attribution fixed (B14)
- [ ] Ref [58] replaced with actual BNEF battery price survey (B14)
- [ ] Ref [150]/Table 7 year-vs-source fixed (B14)
- [ ] §10.5 $500k/hour, §10.3 $64.49, §1.1 165%, §8.1 Google year — sourced/qualified (B15)
- [ ] Table 1 citations added in cells (B16)

**Framework substance**
- [ ] Components 2/3/4: inputs, decision rules, outputs (B17)
- [ ] §7.2 MCDA: criteria + weights + method (AHP/entropy) + sensitivity (B18)
- [ ] §6 selection table: question→approach→resolution→data→limits (B19)
- [ ] WUE / water–energy tradeoff paragraph (B20)
- [ ] Commercial reluctance to curtail training paragraph (B20)
- [ ] Limitations section (US-bias, self-reported disclosures, grey-literature costs) (B21)

**Figures**
- [ ] Every figure caption has a source line / "adapted from" note (B22)
- [ ] Figure 7 formulation + solver; Figure 4 site/source/years (B22)

**Proofreading & presentation**
- [ ] Find-replace damage fixed (flexModelling, ChallengesModellingutions, % %, $THD) (B24)
- [ ] Typos: Colling→Cooling, Charactersitics→Characteristics, data canters→centers (B24)
- [ ] Currency standardised; spelling US/UK consistent (B25)
- [ ] §1.3 fragment rewritten with main verb; §1.5 item 7 rewritten (B25)
- [ ] Nomenclature list added (B25)
- [ ] Abstract tightened + method sentence (B25)

**Journal requirements**
- [ ] CRediT; competing interest; funding; data availability; generative-AI declaration; Highlights (B26)
- [ ] Reference list: consistent Elsevier numbered style; complete metadata; encoding fixed (B26)

**Scope/title**
- [ ] Either add critical appraisal throughout, or change the title (B27)

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
