# Pre-submission checklist — B-TRUST manuscript v0.4 (2026-11-20)

Author: Bashar ALHAJAHMAD (sole author). **Status: not submission-ready.**

Owner key: **R** = researcher; **C** = Claude (analysis/drafting); **R+C** = both. Status: open unless marked.

## A. Experimental (evidence still to obtain)

| # | Item | Owner | Blocks submission? |
|---|---|---|---|
| A1 | ~~Run Phase 73 v2 notebook~~ **Done** (T4; torch 2.14.1, transformers 4.46.3). Run date still to record. | R | — |
| A2 | ~~Validate Phase 73; paired YouLeQD comparisons~~ **Done**; integrated in v0.3 | C | — |
| A2b | **Phase 76 steps-matched retraining** — notebook prepared and preregistered (`68ae8b96`), dry-run verified. Needs your approval, then a T4 run (~3–4 h; no API calls) | R approves and runs; C validates | Strongly recommended (central to the trainability question) |
| A3 | Confirmatory learner-question study — **protocol v1 proposed** (650 relevant items, 4 blinded annotators, C1–C3 with Holm). Needs approval, ethics clearance, recruitment, and separate approval for paid API calls | R | Recommended; otherwise present as future work |
| A4 | Preregister the A3 analysis before coding ends (G2 by granularity, LLM vs constant, certification with power plan) | C, approved by R | If A3 is done |
| A5 | Optional, needs explicit approval for paid API calls: LLM run-to-run variability and a temperature-0 rerun on a subset; second LLM or prompt | R decides | No |
| A6 | Gate-threshold sensitivity analysis (lift 3–10 pp, κ 0.15–0.45), offline | C | No (strengthens §3.4; thresholds are uncalibrated) |
| A6b | ~~Robustness of the G0–transfer association to size and balance; training-free diagnostics~~ **Done** (Phase 75, exploratory; §5.6, Table 10) | C | — |
| A7 | Family-wise view across preregistered hypotheses (for example, Holm across H1–H12 primary tests) as a supplementary table | C | No |

## B. Scientific and statistical

| # | Item | Owner |
|---|---|---|
| B1 | ~~Integrate Phase 73; extend QC~~ **Done** (93 checks pass) | C |
| B2 | Decide whether to keep the H2 information weights as primary or present an unweighted sensitivity | R+C |
| B3 | Report skill-over-majority transfer for the k = 8 transformers (data available from Phase 73) | C |
| B4 | Re-check every claim against its evidence label after integration (confirmatory / exploratory / descriptive) | R+C |
| B5 | Decide how to present the inferred LAK40 → Li et al. (2022) link; optionally contact Xu et al. to confirm the parent dataset and the single-label vs multi-label discrepancy | R |

## C. References

| # | Item | Owner |
|---|---|---|
| C1 | ~~Check the 10 † entries~~ **Done**: all verified, DOIs added | — |
| C2 | Confirm Sangodiah et al. (2017) on the publisher's site (currently verified through citing sources, ‡) | C |
| C3 | Add pages for Ming et al. (2025, ICSC) and Xu et al. (2026, LAK '26); proceedings details for Faraji et al. (AIED 2026) when published; page range for Goren et al. (NeurIPS 2024) | C |
| C3b | ~~Citation integrity (every reference cited, every citation listed)~~ **Done** (scripted; Hoeffding citation added) | — |
| C4 | EduBloom dataset version year (Kaggle "Updated" date or DOI record) | R |
| C5 | Convert to the target journal's reference style | C |

## D. Data, ethics and permissions

| # | Item | Owner |
|---|---|---|
| D1 | Written permission or ID-only release for YouLeQD/QYTL, EduQG and the LAK '26 release (no licence files) | R |
| D2 | Ethics statement for the confirmatory annotation study and for use of public YouTube comments | R |
| D3 | CC BY-SA 4.0 obligations for any redistributed EduBloom derivative | R |
| D4 | Create the public code repository and persistent identifier (for example, Zenodo DOI); update Code availability | R+C |

## E. Editorial and declarations

| # | Item | Owner |
|---|---|---|
| E1 | ~~Author name, affiliation, ORCID, contact details~~ **Done** (title page and Word metadata) | — |
| E2 | CRediT drafted — **confirm the role list; decide whether to keep Supervision** | R |
| E3 | Funding drafted (no external funding) — **confirm** | R |
| E4 | Competing interests drafted (none) — **confirm**, including the Anthropic transparency note | R |
| E5 | Generative AI declaration drafted (Claude substantive roles; ChatGPT for audit instructions; Claude as evaluated system) — **confirm and complete ChatGPT's uses** | R |
| E6 | Select target venue only after A1–A3 are evaluated; check scope, indexing (SCI/SCIE), current quartile, word and figure limits | R+C |
| E7 | Cover letter arguing the contribution precisely (no algorithmic novelty; validity operationalisation; preregistered predictive and negative results) | R+C |
| E8 | Supplementary materials: preregistrations, deviation log, QC report, checkpoint verification, provenance report, full robustness tables | C |
| E9 | Language edit and final consistency pass (Abstract ↔ Results ↔ Conclusion) after integration | R+C |
| E10 | Single-author voice: the draft uses "we"; check the target journal's preference ("I" or impersonal) | R+C |

## F. Already completed in v0.2

- [x] LAK40 provenance traced to `Bloom-All_40.csv` (Xu et al., 2026); 40/40 items verified identical
- [x] Sangodiah et al. (2017) full reference identified
- [x] Angelopoulos et al., Dunn et al., Stutz et al. and Li et al. details verified
- [x] Five publication-quality figures generated from archived outputs; nine tables; equations
- [x] Numbers QC: 69 checks; 3 rounding corrections documented
- [x] Phase 73 v2 prepared without LLM; per-question predictions; checkpoint/resume; dry run reproduces Phase 71 exactly
- [x] Phase 73 run, validated (all values recomputed exactly) and integrated in v0.3; collapse qualification and paired tests reported
- [x] Declarations: no funding, no competing interests, sole author
- [x] v0.4: author information; framework Figure 1 (SVG, vector PDF, source); §3.4 validity/recoverability/trainability; §5.6 robustness (Table 10); §6.5 framework value; Table 11; softened implications; references verified; citation integrity; 107-check QC passes
