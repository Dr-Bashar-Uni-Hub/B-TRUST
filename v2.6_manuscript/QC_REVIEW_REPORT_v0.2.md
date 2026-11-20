# Internal scientific review — manuscript working draft v0.2 (2026-11-19)

**Verdict:** the draft is internally consistent with the archived outputs after the corrections below. It is a complete working draft, not a submission-ready article. Frozen baselines and experimental outputs were not changed; every correction below concerns reporting.

## 1. Consistency between reported numbers and outputs

`qc_numbers.py` recomputes 69 key numbers from the archived output files and compares each with the value in the text (`qc_numbers.csv`). **66 matched; 3 failed by a rounding slip in earlier reporting.**

| # | Claim | Previously reported | Correct | Recomputed value | Where the old value appears |
|---|---|---|---|---|---|
| R1 | H1 95% CI, upper bound | +6.9 pp | **+6.8 pp** | 6.8497 | Continuation doc §5; draft v0.1 |
| R2 | SCAR-E G0 lift | +57.8 pp | **+57.7 pp** | 57.7488 | Continuation doc §§10, 13; draft v0.1 |
| R3 | H10 95% CI, lower bound | −0.233 | **−0.232** | −0.232456 | Continuation doc §16; draft v0.1; Phase 70 validation report |

None changes any conclusion. v0.2 uses the corrected values. The continuation doc is corrected with a note; the archived Phase 70 validation report is left unchanged as an archived record, and this erratum applies to it.

**Decision-rule discrepancy (not an error, now disclosed).** Coarse-level vote losses for the pooled human-authored LR differ by decision rule: 0.600 and 0.500 under the preregistered coarse-probability rule (Phase 61), versus 0.576 and 0.495 when its six-level prediction is coarsened (Figure 3, the only rule available for models without probabilities). The constant beats the model under both. The Figure 3 caption and Section 5.3 now state both.

## 2. Corrections made while drafting (v0.1 → v0.2)

| # | Issue | Correction |
|---|---|---|
| E1 | "FAIL corpora transferred worst for all supervised model classes" — false at k = 8 (GANI, CAUTION, below EDUB under TF-IDF) | Restated as "each PASS corpus above each FAIL corpus", narrow under embeddings, labelled exploratory |
| E2 | "No supervised model exceeded a constant on learner questions" — RoBERTa scored 33/70 vs 26/70 | "No statistically supported advantage" |
| E3 | Relevance-gate description conflated Phase 61 (cross-fitted, 66 admitted / 39 relevant) with Phase 63 (12 splits) | Separated in §4.4 |
| E4 | Power stated as "84%/85%" for one ICC | Reported as 84–85% (236 sources) and 52–53% (120 sources) across ICC 0–0.5 |
| E5 | Figure 5 appeared before Figure 4 | Renumbered in order of appearance, cross-references updated |
| E6 | EduBloom described as "LLM-generated" in earlier claims tables | "Generated per its authors; method not stated" |

## 3. Statistical claims

- **Confirmatory claims match their preregistrations:** H1 failed, H2 supported only with oracle relevance, H3 supported, H5 and H6 failed, H8a/b supported, H9a/c failed and H9b/d supported, H10 supported on six-level vote loss only, H11a/b supported.
- **No result is upgraded from exploratory.** The H10 consolidated-label (p = 0.17) and coarse-level results are reported beside H10.
- **Multiplicity:** corrections are applied within analyses where stated (Bonferroni across thresholds, Holm across comparators). There is **no global correction across the ~11 preregistered hypotheses**; each was registered as its own primary test. Reviewers may ask for a family-wise view, so the checklist includes it.
- **Spearman tests with k = 5 or 8** have coarse null distributions. The text states that only a perfect ordering can reach significance at k = 5.
- **"Below the human reference"** (LLM 0.590 vs 0.686) is explained as majority agreement, not better-than-human judgement.

## 4. Methodological adequacy

- **Adequately described:** estimands, gates, thresholds, inference, preregistration, deviations, and the Phase 70 protocol including temperature, cache and abstention.
- **Gaps a reviewer may raise:**
  - G0 thresholds (5/15 pp, κ 0.20/0.40) are a priori and uncalibrated; a sensitivity analysis is listed (X6).
  - Transfer T averages heterogeneous targets, including a four-level EDUQG; a skill-over-majority version is reported for TF-IDF and embeddings only.
  - The information weights in H2 are a modelling choice.

## 5. Comparisons and baselines

- **Constants** are chosen with the labels (optimistic for the baseline), which is stated.
- **Transformer–LLM comparisons** are descriptive only: no item-level predictions, different samples and conditions. Phase 73 v2 saves per-question predictions.
- **The DASQ vs separate-corpora distinction** is stated wherever both appear (Figure 5 caption; Table 1 note).

## 6. Citations

- **29 references.** 18 checked against a primary or bibliographic source; Sangodiah et al. (2017) verified only through citing sources (‡); 10 standard references marked † still to check against publisher records. Missing details: pages for Ming et al. (2025) and Xu et al. (2026); EduBloom version year; volume and pages for Williamson et al. (2012).
- **LAK40 provenance resolved:** file-level match to Xu et al. (2026) — 40/40 items, identifiers and reference sets identical. The parent dataset is inferred to be Li et al. (2022) from an identical description; the source appendix states single-label sampling, inconsistent with two multi-label items. Both points are disclosed in §3.2 and §7.

## 7. Novelty relative to prior literature

- The draft makes **no algorithmic novelty claim** and states that the selective/risk-control machinery is existing work.
- The framework is presented as an operationalisation of Williamson et al. (2012) and Kane (2013).
- The LLM cross-dataset stability finding is attributed to Faraji et al. (2026).
- **Remaining risk:** reviewers may regard the gates as standard data-quality checks. The defensible contribution rests on:
  - the EduBloom case;
  - the demonstration that gates catch distinct failures;
  - the preregistered predictive tests, including the negative ones.

  This should be argued explicitly in the cover letter.

## 8. Limitations, biases and threats to validity

All of the following are disclosed in §7 of the manuscript:

- small, repeatedly used learner-question target;
- few corpora;
- Phase 70 protocol deviations and unverifiable cache;
- pretraining contamination;
- taxonomy alignment;
- provenance gaps;
- uncalibrated thresholds;
- researcher degrees of freedom (RQ5 formulated after initial failures).

**Additional disclosure, not about the data:** the same model family that assisted the analysis and drafting (Claude) was also an evaluated system. This is declared in Competing interests and the Generative AI statement.

## 9. Consistency across Abstract, Results, Discussion and Conclusion

Every number in the Abstract was checked against Results and `qc_numbers.csv` (50.0 vs 50.9%; 787 of ~793; 9 unanimous; ρ 0.93, p 0.001; ρ 0.69, p 0.035; −0.148, CI −0.232 to −0.065; 34/70 vs 26/70, p 0.17; ~236 sources). The Discussion and Conclusion make no claim absent from Results. Pending items are confined to Table 8, Appendix A and forward references.
