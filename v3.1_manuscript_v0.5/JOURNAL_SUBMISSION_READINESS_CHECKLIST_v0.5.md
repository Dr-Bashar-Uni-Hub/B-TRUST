# Journal-submission readiness checklist — B-TRUST manuscript v0.5 (2026-11-20)

Author: Bashar ALHAJAHMAD (sole author).

**Overall status: scientifically complete for the defined scope; NOT yet submission-ready.**

The remaining blockers are author confirmations, data permissions, a public code repository, a few bibliographic details, and journal-specific formatting. No further experiment is required for the current claims. The confirmatory study is deferred by decision, and its absence is stated as a limitation.

## A. Scientific content

| # | Item | Status |
|---|---|---|
| A1 | All preregistered results reported, including negative ones (H1, H5, H6, H9a/c) | ✅ Done |
| A2 | Phase 73 retained; Phase 76 as a separate robustness subsection | ✅ Done |
| A3 | Exploratory analyses labelled; Freedman–Lane verified by simulation; balance-related p-values descriptive | ✅ Done |
| A4 | Trainability vs label validity distinguished; no causal claims | ✅ Done |
| A5 | Learner-question and LLM results secondary, with limitations; no superiority claims | ✅ Done |
| A6 | Numbers QC: 149 checks pass with exact rounding | ✅ Done |
| A7 | Optional: family-wise (Holm) supplementary table across all preregistered hypotheses | ⬜ Optional |
| A8 | Optional: gate-threshold sensitivity analysis (lift 3–10 pp, κ 0.15–0.45), offline | ⬜ Optional; reviewers may ask, since thresholds are uncalibrated |
| A9 | Optional: confirmatory learner-question study (design B′) | ⏸ Deferred by author decision |

## B. Author confirmations — **blocking**

| # | Item | Status |
|---|---|---|
| B1 | CRediT role list; decide whether to keep "Supervision" (unusual for a single author) | ⬜ Author |
| B2 | Funding statement ("no specific grant…") | ⬜ Author to confirm |
| B3 | Competing interests ("none", with the Anthropic transparency note) | ⬜ Author to confirm |
| B4 | Generative AI declaration: confirm wording; complete ChatGPT's uses (currently: drafting audit instructions) | ⬜ Author |

## C. Data, code and ethics — **blocking**

| # | Item | Status |
|---|---|---|
| C1 | Written permission, or ID-only release, for the three sources without licence files (YouLeQD/QYTL, EduQG, LAK '26 release) | ⬜ Author |
| C2 | Public code and data repository with a persistent identifier (e.g. Zenodo DOI from GitHub). Archives v1.0–v3.1 are ready to deposit, minus unlicensed text | ⬜ Author (Claude can prepare the deposit package) |
| C3 | Ethics statement. This study used only existing public datasets and collected no new human data; confirm whether Siirt University requires a formal exemption for secondary analysis of public YouTube comments | ⬜ Author |
| C4 | CC BY-SA 4.0 attribution for EduBloom-derived material (already credited) | ✅ Done |

## D. References — partly blocking

| # | Item | Status |
|---|---|---|
| D1 | 29 of 30 entries verified against publisher, indexing or catalogue records; Sangodiah et al. (2017) via citing sources (‡) | ✅ Done |
| D2 | Missing details: pages for Ming et al. (ICSC 2025) and Xu et al. (LAK '26); Faraji et al. proceedings (AIED 2026); page range for Goren et al. (NeurIPS 2024); EduBloom version year | ⬜ Fill when available; otherwise cite as arXiv/accepted |
| D3 | Every citation listed and every reference cited (scripted) | ✅ Done |
| D4 | Convert to the target journal's reference style | ⬜ After venue choice |

## E. Editorial — partly blocking

| # | Item | Status |
|---|---|---|
| E1 | Title page with author, affiliation, ORCID, corresponding author; Word metadata | ✅ Done |
| E2 | Abstract 291 words | ✅ Done; check the venue limit (often 150–250) |
| E3 | All figures (1–6) and tables (1–12, A1) cited and numbered in order | ✅ Done |
| E4 | Figures in grayscale-safe vector or high-resolution formats; framework SVG/PDF | ✅ Done |
| E5 | **Length:** ~11,700 words including tables and references | ⬜ Check the venue limit; candidates to move to supplementary: Tables 3, 6, 9, 10 and Appendix A |
| E6 | Single-author voice: the text uses "we"; check the venue's preference | ⬜ Author and Claude |
| E7 | Language edit and final read-through | ⬜ Author and Claude |
| E8 | Cover letter stating the contribution precisely: validity operationalisation, preregistered predictive and negative results, no algorithmic novelty | ⬜ Claude can draft after venue choice |
| E9 | Supplementary materials: preregistrations, deviation logs, QC report, Freedman–Lane simulation, Phase 76 validation report, provenance report, robustness tables | ⬜ Claude can assemble |

## F. Venue selection — **blocking**

- [ ] Choose a target after reviewing scope, SCIE indexing, current quartile, word and abstract limits, and data and AI policies.
- Candidate fields from earlier assessment, scopes not re-verified: educational data mining, AI in education, learning analytics, educational measurement, behavioural research methods.
- The manuscript's emphasis (construct validity of training labels, validity-first evaluation, recoverability–transfer, trainability and imbalance) fits measurement- and methods-oriented educational technology journals better than general educational psychology.

## Minimum path to submission

1. B1–B4 confirmations.
2. C1 permissions or an ID-only release decision.
3. C2 repository and DOI.
4. Venue choice (F).
5. E5 length, E2 abstract, D4 reference style.
6. E8 cover letter and E9 supplementary package.
7. Final language edit (E7).
