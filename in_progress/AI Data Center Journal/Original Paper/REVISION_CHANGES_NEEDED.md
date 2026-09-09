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
