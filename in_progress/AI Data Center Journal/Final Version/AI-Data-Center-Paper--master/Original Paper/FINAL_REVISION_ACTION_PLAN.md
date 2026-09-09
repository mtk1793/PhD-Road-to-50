# Final Revision Action Plan for the AI Data Center Paper

## Purpose of this document

This action plan compares the original manuscript with the current revised manuscript and evaluates the revised manuscript against the reviewer-action file. It identifies what has been improved, what remains incomplete or technically unsafe, and how to complete the revision so the paper is clearer, more defensible, reproducible, and suitable for resubmission to *Renewable and Sustainable Energy Reviews*.

## Overall assessment

The revised manuscript is substantially stronger than the original. It correctly moves away from presenting unsupported optimization outputs as established results, adds a PRISMA-style methodology, corrects the LOLE formulation, distinguishes battery-pack prices from installed BESS costs, separates unfirmed generation LCOE from firm delivered electricity, expands the framework into inputs/decision rules/outputs, adds a modeling-method selection table, introduces WUE, acknowledges commercial limits on workload shifting, and adds a limitations section.

However, the revised manuscript is **not yet publication-ready**. The largest remaining risks are:

1. The PRISMA counts and source-type classification appear asserted rather than demonstrably audited.
2. The references were renumbered extensively, but several citations are mismatched, incomplete, weak, duplicated, or inconsistent with the claims.
3. The manuscript still contains major language, grammar, equation-formatting, numbering, and copy-editing problems.
4. Several reviewer requirements remain incomplete, especially figure-source lines, journal declarations, Highlights, nomenclature, reference normalization, and a point-by-point response.
5. Some revised passages introduce new factual statements, cost values, equations, or examples without sufficient verification.
6. The revised manuscript sometimes overcorrects by deleting quantitative conclusions without replacing them with a clear, critical synthesis.
7. The article still alternates between being a systematic critical review, a design framework, and a modeling paper. Its contribution and evidence boundaries must be stated more consistently.

The recommended publication strategy is to retain the **critical-review** title, clearly label the mathematical framework as a **literature-synthesized conceptual framework**, avoid claiming original model outputs unless a complete reproducible model is supplied, and base all quantitative findings on traceable published evidence.

---

# 1. High-priority decisions to make before editing

## 1.1 Choose and consistently apply the evidence pathway

The new manuscript has largely selected the safer pathway: remove unsupported original model results and replace them with literature-based benchmarks and conceptual equations. Keep this approach.

Do **not** restore the original claims concerning:

- a 720 MWh deterministic baseline;
- more than 90% storage reduction;
- a universal 30–60% storage-capital reduction;
- a universal $35–80/MWh firmed hybrid LCOE;
- a $30–120 million NPV;
- a 14–19% IRR;
- a 4–8 or 6–11 year payback;
- definitive Pareto-frontier results;
- universal ancillary-service revenue values.

These figures should appear only if the authors provide a complete model, input datasets, solver information, scenario definitions, cash-flow assumptions, and reproducible output files. Otherwise, retain the revised manuscript's literature-based and site-specific framing.

## 1.2 Define the paper's exact contribution

Use one consistent contribution statement throughout the abstract, Introduction, Scope, Framework, Conclusions, Highlights, and response letter:

> This paper is a systematic critical review that synthesizes technical, economic, operational, and sustainability evidence into a seven-component decision framework. The equations and decision rules are literature-synthesized planning formulations, not the output of a new site-specific optimization study.

Avoid saying the framework is “validated” by corporate case studies. The case studies do not validate the full framework experimentally. Use:

> The framework is illustrated and critically compared against publicly reported industry practices.

## 1.3 Adopt one language convention

Use **US English** throughout because the manuscript already predominantly uses “data center,” “modeling,” and “optimization.” Apply a full spelling pass:

- modeling, not modelling;
- optimize, not optimise;
- center, not centre;
- behavior, not behaviour;
- organization, not organisation;
- characterized, not characterised;
- minimized, not minimised;
- utilization, not utilisation.

Do not switch spelling inside quotations or official publication titles.

## 1.4 Adopt one numerical and currency convention

Use:

- USD 108/kWh in prose where currency ambiguity may exist;
- $43/MWh in tables after defining all monetary values as 2024 or 2025 USD;
- $1.6 million, not 1.6M$, $1.6M, or $1,600,000 unless table precision requires it;
- 4–8 h, 10–100 MW, and 2015–2026 using en dashes;
- a space between values and units: 100 MW, 0.876 h/year, 700 W;
- no space before %: 99.99%;
- CO2 or CO₂ consistently, preferably CO₂ in text if the journal workflow preserves Unicode.

---

# 2. Detailed comparison of the revised manuscript with the original

## 2.1 Abstract

### Improvements already made

The revised abstract now:

- states that the review follows PRISMA 2020;
- gives a total source count;
- avoids calling all 185 sources peer-reviewed;
- removes unsupported NPV, IRR, payback, and universal firmed-LCOE claims;
- correctly treats USD 108/kWh as a 2025 pack-level value;
- emphasizes site-specific uncertainty;
- distinguishes generation, hybrid-system, and delivered-electricity costs.

### Remaining problems

The abstract has substantial grammar and style problems. Examples include:

- “causing a significant boost in electricity usage across the world in data centres”;
- “A systematic literature review ... is carried out and analyzed in this review”;
- “seven component approach” without a hyphen;
- a sentence fragment caused by “USD 108/kWh in 2025. and that”;
- “The degree of benefit ... will vary by site,” which is vague;
- inconsistent “data centres” and “data-center.”

### Required action

Replace the entire abstract with a polished 200–230 word version. The abstract should contain five elements in order:

1. problem and significance;
2. review methodology and evidence base;
3. framework contribution;
4. principal critical findings;
5. limits and practical implication.

Do not claim “results show” unless those results arose from a reproducible analysis. Prefer “the reviewed evidence indicates.”

### Recommended abstract

Artificial-intelligence workloads are accelerating electricity demand and increasing the power-density, reliability, cooling, and grid-integration requirements of data centers. This study presents a systematic critical review of the energy infrastructure required to integrate renewable generation and energy storage with AI data centers. Following the PRISMA 2020 reporting framework, the review synthesizes 185 journal articles, conference papers, standards, agency reports, and industry sources published between 2015 and 2026. The evidence is organized into a seven-component decision framework covering site assessment, technology selection, electrical architecture, hierarchical control, workload flexibility, economic evaluation, and sustainability compliance. The review finds that declining renewable-generation and battery costs improve the prospects for low-carbon data-center infrastructure, but published cost metrics are frequently not comparable. In particular, battery-pack prices must be distinguished from installed battery energy storage system costs, unfirmed renewable-generation LCOE must not be compared directly with firm delivered electricity, and reliability claims require chronological, site-specific adequacy assessment. Wind–solar complementarity and flexible computing loads can reduce balancing requirements, but the achievable benefit depends on resource correlation, network constraints, service-level agreements, and workload portability. The proposed framework therefore supports structured project screening rather than prescribing a universal technology mix. Remaining research needs include reproducible techno-economic models, independently verified corporate performance data, multi-year resource assessment, and integrated evaluation of energy, water, reliability, and grid impacts.

## 2.2 Introduction and research gap

### Improvements already made

The revised version appropriately removes the unsupported “2.9 Wh per GPT-3 query” attribution and qualifies the 165% growth statement by adding the 2024–2030 period. It also replaces unsupported claims of guaranteed interconnection-time and storage-cost reductions with a more cautious description of the framework.

### Remaining problems

- “Data canters” remains in Section 1.1.
- “1, 287 MWh” should be “1,287 MWh.”
- “552 tones” should be checked and corrected to “552 metric tons CO₂e” if supported.
- The text speculates about “The next GPT,” which is unnecessary and scientifically weak.
- The comparison with Japan is rhetorical and should be cited precisely or removed.
- The fragment beginning “In congested regions...” in Section 1.3 remains unfixed.
- Section 1.5 item 7 still reads “Resilience and sustainability compliance are also important.”
- Objective 2 still promises “transparent economic modelling” and NPV analysis even though the new manuscript no longer contains an applied project model.
- Objective 3 says “validate,” which overstates what case studies can do.

### Required action

- Remove speculative discussion of future GPT models.
- Complete the grid-interconnection sentence with a main verb.
- Rewrite Objectives 2 and 3 so they match the actual review.
- Rewrite item 7 in parallel with items 1–6.

### Recommended objective wording

1. To synthesize current evidence on data-center electrical systems, renewable generation, energy storage, grid integration, cooling, and workload flexibility.
2. To establish a consistent basis for comparing technology costs, reliability metrics, and delivered-electricity options while identifying the assumptions required for project-specific analysis.
3. To translate the reviewed evidence into a seven-component decision framework and illustrate its applicability using publicly reported industry practices.

## 2.3 Review methodology and PRISMA section

### Improvements already made

The new Section 1.6 directly addresses the reviewer's largest methodological concern. It names databases, eligibility criteria, screening stages, source counts, and a PRISMA flow figure.

### Critical remaining risk

The exact screening numbers and source breakdown must be based on an actual documented search record. They cannot be retrofitted merely to match the 185 references. The manuscript currently states precise values such as 1,604 identified records, 317 duplicates, and 211 full-text exclusions, but no search date, full search strings, database-specific search fields, export files, screening log, or supplementary record is provided.

The claimed source breakdown also needs a real audit. The bibliography contains books, preprints, company webpages, working papers, standards, technical reports, corporate reports, blogs, and incomplete entries. Calling a group “14 standards and patents” is particularly questionable because no patent category is clearly demonstrated.

### Required action

Create a supplementary review-method file containing:

- exact search date for every database;
- complete database-specific search strings;
- fields searched;
- language restrictions;
- document-type restrictions;
- export formats;
- duplicate-removal method;
- screening method and number of screeners;
- conflict-resolution method;
- exclusion reason for each full-text record;
- evidence-quality or source-quality classification method;
- a final included-study register linked to reference numbers.

If these records do not exist, revise the language from “systematic review” to a transparent structured/scoping review and do not invent PRISMA counts.

### Specific textual corrections

- “International Standards Organisation” should be “International Organization for Standardization.”
- “IEO” appears to be an error, likely “IEC” or “IEA.” Verify before correction.
- “Greenhouse Gases Protocol” should be “Greenhouse Gas Protocol.”
- “research instutions” should be “research institutions.”
- Add a space after the period in “sources.Studies.”
- Replace “were discounted” with “were excluded.”
- Identify whether screening was performed by one or two authors.
- Add the date on which the final search was executed.
- Do not italicize entire methodology paragraphs.

## 2.4 Source count and literature-review opening

### Improvements already made

The original inconsistency between “over 185 peer-reviewed articles” and “over 160 sources” has been removed.

### Remaining problems

- The opening sentence of Section 2 appears twice.
- “14 standards and patents” does not match the abstract's broader categories and may not match the actual references.
- The total category count is internally consistent at 185, but it still requires verification against the final, renumbered list.
- Several references published before 2015 remain in the bibliography. These can be valid foundational sources, but the methodology says 2015–2026 without explaining exceptions.

### Required action

Add an explicit foundational-source exception:

> The primary search window was 2015–2026. Earlier sources were retained only when they defined foundational methods, standards, or metrics that remain in current use.

Then report the number of pre-2015 foundational sources separately.

## 2.5 Equations and storage-sizing section

### Improvements already made

The revised Section 5.3 is conceptually much better. It:

- defines LOLE as duration rather than probability;
- removes division by 8,760;
- defines critical non-deferrable load;
- formulates deterministic sizing over deficit events;
- stops claiming a universal 720 MWh baseline and more than 90% reduction;
- labels the optimization equations as conceptual and not used for new numerical results.

### Remaining technical and presentation problems

- Equation (1) refers to the positive-part operator in the definition, but the rendered equation does not visibly include the positive-part notation.
- The sentence defining the deficit event is grammatically incomplete.
- Equation numbers are duplicated. The solar/wind constraints and grid constraint reuse (9), while later grid-cost equations also use (12) and (13), potentially conflicting with the AHP equation.
- Several variables are malformed because Word equation objects were extracted poorly.
- Battery SOC Equation (6) must divide discharge by efficiency, not multiply by discharge efficiency, depending on the chosen convention. Use one clearly defined convention.
- Complementarity, grid availability, backup availability, charging/discharging exclusivity, SOC boundary conditions, and cyclic end-state constraints are missing from the conceptual MILP.
- A statement calls deterministic sizing “Dynamic sizing,” which is an error.
- “Probabilistic and Optimizations based” is grammatically incorrect.

### Required action

Rebuild all equations with Word's equation editor and renumber sequentially after all insertions. At minimum, the conceptual optimization should include:

- energy balance;
- SOC transition;
- SOC bounds;
- battery power bounds;
- charge/discharge exclusivity or a statement explaining why simultaneous operation is excluded by cost;
- renewable availability limits;
- grid import/export bounds;
- backup bounds;
- reliability constraint;
- terminal SOC condition;
- optional emissions constraint;
- objective function with annualization or discounted lifecycle-cost treatment.

Add a symbol table immediately after the equations or in the Nomenclature section.

## 2.6 Framework components

### Improvements already made

Components 1–4 are now much more operational. The revised manuscript adds inputs, screening logic, outputs, AHP weighting, sensitivity analysis, and a modeling-selection table.

### Remaining problems

- The AHP values are described as illustrative, which is correct, but they should not be presented as if derived from an actual pairwise-comparison matrix.
- No worked example or matrix is given.
- Criteria partly double-count water under infrastructure and environmental exposure.
- Component 2 has grammatical errors and inconsistent capitalization.
- The bullet list separates “usable energy capacity” and “storage duration” awkwardly.
- Component 4 contains “cybersécurité,” a French-language intrusion.
- The figure formerly described as a Pareto frontier is now conceptual, which is appropriate, but the caption and text must make that status unmistakable.

### Required action

- Call the weights “illustrative default weights” and do not report a consistency ratio unless the actual matrix is shown.
- Add either a short worked AHP example in supplementary material or state that project stakeholders must generate the pairwise matrix.
- Consolidate each component into a repeated structure:
  - Purpose
  - Required inputs
  - Decision process
  - Outputs
  - Limitations
- Replace “Figure 8 Technology-mix Selection Framework” with a caption that states “conceptual decision framework; no site-specific optimization results are shown.”

## 2.7 Economic analysis

### Improvements already made

This is one of the strongest revisions. The new manuscript:

- removes unsupported project CAPEX totals;
- removes unsupported NPV, IRR, and payback outputs;
- distinguishes pack and installed BESS costs;
- separates unfirmed generation from partially firmed hybrids and firm grid service;
- stops treating capacity-market prices as LCOE;
- introduces the grid-cost stack;
- explains conversion from $/MW-day to $/MWh;
- removes the universal $500,000/h downtime claim;
- includes a critical appraisal.

### Remaining problems

- The section contains many grammar problems and awkward machine-generated wording.
- The cost benchmark table combines point estimates and wide ranges from different geographic and methodological bases.
- The BESS LCOE of 80–130/MWh needs a clearly defined charging-energy treatment and duty cycle or should be called LCOS rather than LCOE.
- The phrase “weighted-average LCOE for these 17 projects” needs the technology and source context stated precisely.
- A “partially firmed” hybrid category needs a definition.
- The central 7.5% real WACC is retained even though the paper no longer calculates project outputs. It can remain as a recommended screening assumption, but it should not appear as a finding.
- Equation (13) should be checked carefully for dimensional presentation. The equivalent capacity adder is `(capacity price × 365)/(8,760 × load factor)`, with units shown.
- “LAMP” should likely be “LMP.” Verify the source.
- The statement that PJM's value “represents a 92% annual load factor” is inaccurate wording. The 92% is an assumed data-center load factor used in the conversion, not a property of the auction value.
- Policy statements about U.S. tax-credit changes require exact, current legal verification and should be framed cautiously.

### Required action

- Rename the battery metric to “illustrative LCOS or storage-service cost” unless generation is embedded.
- Add a column for “Geography/year/source” in all benchmark tables.
- Add a column for “Included cost components.”
- Define “unfirmed,” “partially firmed,” and “firm” before Table 9.
- State explicitly that the benchmark values are not adjusted to a common currency year unless they actually are.
- If values are normalized, describe inflation index and base year.
- Use “screening assumption” for 7.5% real WACC.
- Have a tax specialist or authoritative current source verify all tax-credit language before submission.

## 2.8 Case studies

### Improvements already made

The manuscript is more cautious in the general economic discussion, but the case-study section itself remains mostly inherited from the original.

### Remaining problems

The case studies still contain many potentially unsupported or overstated statements:

- number of facilities and PPA capacities;
- site-specific wind and solar configurations;
- PUE values;
- fuel-cell replacement costs;
- specific corporate nuclear arrangements;
- company LCOE estimates in the comparative table;
- claims that the companies “validate” the framework;
- claims of 100% renewable operation that may refer to annual matching rather than hourly physical supply;
- “Rare” as Apple's backup type is not a defensible technical category.

The table mixes CFE percentages, annual renewable matching, procurement coverage, physical generation, storage, and estimated LCOE as if they were directly comparable.

### Required action

Redesign the case-study table with the following columns:

- Company
- Reporting year
- Metric reported
- Accounting basis: annual matching, hourly CFE, procurement coverage, or physical supply
- Publicly reported energy strategy
- Evidence source
- Independent verification available? Yes/No/unclear
- Relevance to framework component
- Transferability limitation

Remove estimated company-specific LCOEs unless each value has a direct, credible source and identical accounting boundaries.

Replace all “validates” language with “illustrates,” “is consistent with,” or “provides an industry example relevant to.”

## 2.9 Workload flexibility and demand response

### Improvements already made

The revised manuscript now acknowledges that training flexibility is commercially constrained and removes generalized ancillary-service revenue claims.

### Remaining problems

- The workload-flexibility table still assigns qualitative flexibility without a stated evidence method.
- “Background tasks” are labeled highly flexible, but this depends on operational context.
- The prose contains errors such as “interrupt ability,” “data-immutability,” and “Check the project specific flexible share shall be validated.”
- Section 11.2 still says training can be deferred without affecting project timelines, which conflicts with the new commercial-limits paragraph.
- The example of 10,000–50,000 MWh training energy is not sourced clearly and may be unnecessary.
- “DSG” is undefined and appears erroneous.

### Required action

- Define the table as a qualitative screening classification.
- Replace categorical labels with “potential flexibility, subject to...”
- Align Sections 7.6, 9.5, 11.2, and 11.3 around the same constraints.
- Remove unsupported universal savings percentages unless each is well sourced.
- Define or delete “DSG.”

## 2.10 Cooling, water, and sustainability

### Improvements already made

The WUE discussion now recognizes the energy–water tradeoff and avoids universal numeric water-use claims in the framework section.

### Remaining problems

- WUE is normally expressed relative to total site source water and IT energy, and the definition should follow the cited standard/source.
- The manuscript needs a clearer distinction among direct on-site water use, off-site water consumed in electricity generation, and lifecycle water impacts.
- Section 12.4 retains dramatic global AI water and e-waste claims that need particularly strong primary sources.
- The cooling section still uses some unsupported performance ranges and awkward wording.
- The sustainability section should distinguish annual contractual matching from hourly CFE and from physical islanded renewable operation.

### Required action

Add a concise sustainability-metrics table containing:

- PUE;
- WUE;
- CUE or operational carbon intensity;
- hourly CFE score;
- annual renewable matching;
- embodied carbon;
- e-waste/circularity metric;
- system boundary and reporting period.

For every corporate metric, state whether it is self-reported and whether independent assurance is identified.

## 2.11 Limitations and conclusions

### Improvements already made

A dedicated limitations section has been added and the conclusions are now more cautious. Unsupported project-level financial results have been removed.

### Remaining problems

The limitations section is poorly written, overlong, and numerically inconsistent in its enumeration. It begins with “Several limitations have been considered,” progresses through “The seventh,” then “Finally,” then “Ninth,” then “Last but not least.” It also omits a concise explicit statement of U.S. bias near the beginning.

The Conclusions still open with “provides a scalable, deployable path,” which is stronger than supported by a literature framework. The phrase “cost trajectories ... are firmly established” is too absolute. The implementation recommendations may imply that LOLE methods are categorically preferable, when the correct method depends on planning purpose, data availability, and risk tolerance.

### Required action

Rewrite the limitations into five compact paragraphs:

1. evidence-base and geographic bias;
2. self-reported corporate data and source quality;
3. methodological and screening limitations;
4. lack of original site-specific model validation;
5. technology, policy, and market uncertainty.

End the conclusions with a balanced contribution statement rather than a universal deployment claim.

---

# 3. Reviewer comments: completion status

## Fully or substantially addressed

- Addition of a review-methodology section.
- Reconciliation of LOLE versus LOLP and removal of division by 8,760.
- Identification of critical non-deferrable load.
- Removal of unsupported 720 MWh and >90% reduction claims.
- Correction of battery cost units and pack/system distinction.
- Removal of grid “LCOE” misuse.
- Separation of unfirmed and firmed/delivered costs.
- Use of a single 7.5% real WACC as a screening assumption with sensitivity range.
- Removal of unsupported NPV/IRR/payback figures.
- Addition of framework inputs, decision rules, and outputs.
- Expansion of MCDA/AHP description.
- Addition of modeling-method selection table.
- Addition of WUE and commercial workload constraints.
- Addition of a limitations section.
- Correction of earlier find-and-replace corruption in at least some locations.

## Partially addressed and still requiring work

- PRISMA reproducibility and verification of screening counts.
- Exact source-type breakdown.
- Figure source lines and reproducibility details.
- Critical appraisal across all major sections.
- Citation support for case study and sustainability claims.
- Consistent figure/table/equation numbering.
- Consistent cost-year and geographic basis.
- Reference style, completeness, and quality.
- Full English-language proofread.
- Nomenclature list.
- Clear method for source-quality appraisal.

## Not visibly completed in the revised manuscript

- Highlights file or Highlights block.
- CRediT author contribution statement.
- Declaration of competing interest.
- Funding statement.
- Data availability statement.
- Declaration of generative-AI use.
- Complete point-by-point Response to Reviewer and Editor.
- A verified clean manuscript with all tracked changes accepted.
- A marked-up manuscript with genuine Word Track Changes.
- Complete Elsevier-style reference normalization.

---

# 4. Mandatory structural changes before resubmission

## 4.1 Add front matter after Keywords

Add a Nomenclature section or a separate nomenclature table. Include all abbreviations and all equation symbols actually used. At minimum:

AI, ADR, AHP, APF, ATS, BESS, BMS, CAES, CAPEX, CFE, CF, CHP, COP, CUE, DER, DRL, EMS, EMT, ESG, GFC, GFI, GHG, GIS, HJT, IBR, IEC, IEEE, IRR, ITC, LCOE, LCOS, LDES, LFP, LiDAR, LOLE, LOLP, MAPE, MCDA, MILP, MPC, NMC, NPV, O&M, OPF, OT, PCC, PDU, PFC, PFR, PLL, PPA, PSH, PTC, PUE, PV, REC, RL, RoCoF, RPS, SCR, SLA, SMPS, SOC, SOH, SSR, STATCOM, STS, TES, THD, TMY, TOPCon, UPS, VFD, VRFB, VRE, VSC, WACC, and WUE.

## 4.2 Add end matter before References

Include:

### CRediT authorship contribution statement

Use only roles that accurately reflect the authors' work.

### Declaration of competing interest

Use Elsevier's standard declaration if accurate.

### Funding

State the actual funder and grant number, or “This research received no external funding.”

### Data availability

Because this is a review, provide the screening spreadsheet, search strings, extraction sheet, and source-classification table in a repository if possible. Do not promise code or datasets that do not exist.

### Declaration of generative AI and AI-assisted technologies

Disclose the actual tool and use accurately. State that the authors reviewed and edited all output and take responsibility for the manuscript.

### Acknowledgments

Include only if applicable.

## 4.3 Prepare Highlights as a separate file

Recommended draft, each to be checked against the journal's character limit:

- Systematic review links AI data-center loads with energy infrastructure.
- Seven-component framework connects engineering, economics, and operations.
- Pack, installed BESS, generation, and delivered costs are distinguished.
- Reliability requires chronological, site-specific adequacy assessment.
- Workload and renewable flexibility are bounded by commercial constraints.

---

# 5. Figures and tables

## 5.1 Figure corrections

Every figure caption must include one of:

- Source: Authors' compilation based on [references].
- Source: Authors' calculation using [dataset, site, years].
- Adapted from [reference], with permission.
- Reproduced from [reference], with permission.

Do not use “Source: authors” for a figure derived from external data without naming the data.

### Figure-specific actions

- Global electricity-demand figure: identify exact dataset, publication year, and whether intermediate years are interpolated.
- PRISMA figure: use the official PRISMA 2020 structure and ensure counts match the screening log.
- Daily load profile: label it “illustrative” unless it is based on measured data. State assumptions.
- Solar-cost figure: list the underlying annual data; do not draw a continuous historical series from only two endpoints.
- Wind–solar complementarity figure: specify location or state clearly that it is conceptual. If data-based, give dataset, coordinates/region, years, temporal resolution, and normalization method.
- Storage landscape: state sources for every bubble/value and explain whether cost refers to pack, installed system, or LCOS.
- Seven-component framework: “Source: authors.”
- Technology-mix framework: state explicitly that it is conceptual and not an optimization result.
- Hierarchical-control figure: state whether adapted from the literature.
- Electricity-cost figure: identify cost year, geography, and category boundaries.

## 5.2 Table corrections

- Renumber all tables after insertions. Current numbering is inconsistent.
- Ensure every table is cited in the text before it appears.
- Add source notes below every table.
- Define all abbreviations in table footnotes.
- Avoid mixing global averages, U.S. estimates, and company-specific values without a geography/year column.
- Avoid using “TBD,” “Rare,” or “Minimal” in a scholarly comparison table.
- Remove unsupported company LCOEs.
- Add uncertainty/limitations columns where appropriate.

---

# 6. Reference audit

The reference list requires a full manual and automated audit. This is now one of the highest publication risks.

## 6.1 Required checks for every reference

- Does the reference exist?
- Does the title match the linked document?
- Do authors, year, journal, volume, issue, pages/article number, and DOI match?
- Does the cited source support the exact sentence?
- Is the source primary where a primary source is available?
- Is the source peer-reviewed, preprint, company report, standard, webpage, or commentary?
- Is the source inside the declared search window, or documented as foundational?
- Is the URL stable and accompanied by an access date where required?
- Is the reference duplicated elsewhere under a different number?

## 6.2 Specific red flags visible in the revised list

- Reference [118] contains “Technoogy” and an `nlr.gov`-style URL that must be checked.
- Reference [40] also uses an `nlr.gov` URL and should be verified.
- Some source titles consist only of a URL or organization name.
- Some journal articles have no volume, pages, or DOI.
- Some ResearchGate links are used where an original publisher or official source should be cited.
- Company blogs and Substack-style sources should not support central technical claims.
- Foundational power-flow sources from 1990, 1991, 1998, 1999, 2007, 2011, and 2013 fall outside the declared window and need explicit justification.
- Multiple terms and organizations are inconsistently styled, including data center/data centre and NREL citations.

## 6.3 Citation-renumbering risk

Because the revised manuscript inserted and deleted many references, perform a citation-integrity audit after all editing. Search every in-text number and verify it points to the intended final reference. Do not rely on manually typed numbering. Use reference-management software such as EndNote, Zotero, or Mendeley with the journal's numbered style.

---

# 7. Language and technical copy-editing list

Correct at minimum the following residual problems:

- Data canters → data centers.
- 1, 287 → 1,287.
- tones → metric tons, if supported.
- “AI workload Growth” → “AI Workload Growth.”
- “seven component” → “seven-component.”
- “wind-solar” → “wind–solar” when expressing a paired relationship.
- “has being proposed” → “has been proposed.”
- “renewables powered” → “renewable-powered.”
- “optimization based” → “optimization-based.”
- “Dynamic sizing” → “Deterministic sizing.”
- “Optimizations based” → “optimization-based.”
- “principle criterion” → “principal criterion.”
- “The required inputs include for this component are” → “The required inputs for this component are.”
- “Ac or dc” → “AC or DC.”
- “cybersécurité” → “cybersecurity.”
- “work loads” → “workloads.”
- “interrupt ability” → “interruptibility.”
- “project specific” → “project-specific.”
- “air-cooled systems uses” → “air-cooled systems use.”
- “0.876hours/year” → “0.876 h/year.”
- “52.6 minutes of each hour of the year” → “52.6 min/year.”
- “unstructured control” → verify intended term, likely “infrastructure control” or “facility control.”
- “equipment redundant” → “equipment redundancy.”
- “common mode fail” → “common-mode failures.”
- “O&M – Set up expenses” → define the actual cost category.
- “cutback” → likely “curtailment.”
- “there is some evidence for universal cost parity” → likely “there is insufficient evidence for universal cost parity.”
- “facility global footprint” → “global facility portfolio.”
- “high 90's percent” → remove or replace with a sourced value.
- “data center 's” → “data center's.”
- “loads balancing” → “load balancing.”
- Apple:100 → Apple: 100%.
- “measures are common and are used” → simplify.
- “Last but not least” → remove from scholarly prose.

Perform a separate technical edit for capitalization of section headings and defined terms.

---

# 8. Recommended revised section structure

1. Introduction
   1.1 AI Data-Center Electricity Demand
   1.2 Renewable-Energy and Grid Context
   1.3 Core Integration Challenges
   1.4 Scope and Research Questions
   1.5 Contributions and Paper Structure
2. Review Methodology
   2.1 Databases and Search Strategy
   2.2 Eligibility and Source-Quality Criteria
   2.3 Screening and Data Extraction
   2.4 Limitations of the Review Method
3. Evidence Synthesis
   3.1 AI Load and Cooling Characteristics
   3.2 Renewable Generation
   3.3 Energy Storage and Backup
   3.4 Grid Integration and Power Quality
   3.5 Workload Flexibility
4. Engineering Assessment Methods
   4.1 Resource and Site Assessment
   4.2 Storage-Adequacy Formulations
   4.3 Power-Flow, Harmonic, and EMT Methods
   4.4 Economic and Reliability Metrics
5. Seven-Component Decision Framework
6. Critical Industry Case Studies
7. Key Technical and Commercial Challenges
8. Economic Evidence and Cost Comparability
9. Sustainability, Water, and Regulation
10. Limitations
11. Conclusions and Research Priorities

This structure would reduce repetition among the existing Sections 2, 3, 5, 6, 7, 9, and 11. If restructuring is too disruptive for the current revision deadline, retain the existing numbering but remove duplicated explanations.

---

# 9. Point-by-point response strategy

For every reviewer comment, use four short blocks:

**Reviewer comment:** Quote the comment exactly.

**Response:** Thank the reviewer and state whether the comment is accepted.

**Action taken:** Describe exactly what changed. If an unsupported result was removed, say so directly.

**Location:** Give section, page, and line numbers in the marked-up manuscript.

Example:

> **Reviewer comment:** “Equation 2 is wrong...”
>
> **Response:** We agree. The previous equation divided the annual shortfall-duration sum by 8,760, producing a dimensionless probability rather than LOLE in hours per year.
>
> **Action taken:** Equation (2) has been reformulated as the sum of shortfall indicators multiplied by the time-step duration. The text now states that no division by 8,760 is applied. The reliability criterion is consistently expressed as 99.99% annual availability, corresponding to 0.876 h/year under the simplified annual-duration relation.
>
> **Location:** Section 5.3, page X, lines Y–Z.

Do not say a concern is “addressed” unless the manuscript and supporting files actually contain the required evidence.

---

# 10. Final resubmission checklist

## Scientific integrity

- [ ] All PRISMA counts are supported by a screening log.
- [ ] The 185-source classification is manually verified.
- [ ] Earlier foundational sources are explained.
- [ ] No original model outputs remain without a reproducible model.
- [ ] Conceptual equations are labeled as synthesized formulations.
- [ ] Every quantitative claim has a supporting source with matching scope.
- [ ] Company-reported metrics are labeled self-reported.
- [ ] Annual matching, hourly CFE, physical supply, and reliability are not conflated.

## Technical consistency

- [ ] LOLE is consistently in h/year.
- [ ] 99.99% corresponds to 0.876 h/year under the stated simplified relationship.
- [ ] Critical load is defined consistently.
- [ ] Pack, cell, installed BESS, and LCOS/LCOE are separated.
- [ ] Grid delivered cost is not called LCOE.
- [ ] Capacity prices are converted dimensionally correctly.
- [ ] All equations are sequentially numbered and all symbols defined.
- [ ] Tables use consistent currency year, geography, and cost boundaries.

## Presentation

- [ ] Full professional English edit completed.
- [ ] US spelling applied consistently.
- [ ] Figure, table, and equation numbering rebuilt.
- [ ] Every figure and table has a source note.
- [ ] Nomenclature added.
- [ ] Abstract shortened and polished.
- [ ] Limitations rewritten concisely.
- [ ] Conclusions avoid universal claims.

## References

- [ ] All references imported into a reference manager.
- [ ] All citation numbers regenerated automatically.
- [ ] Every DOI and URL verified.
- [ ] Incomplete references completed.
- [ ] Duplicate references removed.
- [ ] ResearchGate/vendor/blog sources replaced with primary sources where possible.
- [ ] Elsevier numbered style applied consistently.

## Journal deliverables

- [ ] Marked-up manuscript with genuine Track Changes.
- [ ] Clean revised manuscript.
- [ ] Point-by-point Response to Reviewer and Editor.
- [ ] Highlights file.
- [ ] CRediT statement.
- [ ] Competing-interest declaration.
- [ ] Funding statement.
- [ ] Data-availability statement.
- [ ] Generative-AI declaration.
- [ ] Supplementary PRISMA search and screening file.

---

# Final recommendation

The revised manuscript has made the correct strategic change by converting unsupported original numerical results into a critical, literature-based framework. That direction should be preserved. The next revision should focus less on adding new content and more on **verification, consolidation, precise source matching, professional language editing, and journal compliance**.

The paper will be much more defensible if it makes three claims clearly and consistently:

1. it systematically organizes a fragmented evidence base;
2. it provides an actionable seven-component decision framework;
3. it identifies why commonly reported cost, reliability, sustainability, and flexibility metrics cannot be compared without consistent boundaries and site-specific analysis.

If those claims are supported by a genuine PRISMA record, a fully audited reference list, carefully bounded quantitative statements, and a clean professional presentation, the manuscript will be substantially better positioned for re-review.
