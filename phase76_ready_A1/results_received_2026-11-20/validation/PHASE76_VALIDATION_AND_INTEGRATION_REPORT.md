# Phase 76 validation and integration report (run by the author on 2026-11-20; validated and integrated into manuscript v0.5 on 2026-11-20)

**Recommendation: ACCEPT.** Every value recomputes exactly, and all three preregistered hypotheses are supported for both models. The Phase 73 FAIL decisions for SANGO and MOHOM are attributed to training configuration, as the preregistered interpretation rule specifies. Phase 73 results are preserved unchanged and are reported alongside.

**Input:** `p76_outputs.zip` (sha256 `b3734f36…`), 70 files. Notebook A1 (`e8880619…`); Tesla T4; torch 2.14.1+cu130; transformers 4.46.3; Python 3.13.16. Full-fit fp16 checkpoints are on the author's Google Drive (not received; not needed for validation).

## 1. Verification (`v76_validate.py`)

- **No issues.** Item keys and label order match every corpus. Excluded targets are absent and leakage exclusions hold.
- **Recomputation:** CV accuracy, G0 lift, κ, gate decision, transfer T and top-class share all recompute within 1e-9 for all 16 model–corpus pairs.
- **Tests:** ρ and exact p reproduce.

## 2. Preregistered hypotheses

| | DistilBERT | RoBERTa | Status |
|---|---|---|---|
| R1: collapse resolved (top-class share < 80%) | SANGO 36.1%, MOHOM 28.6% | SANGO 33.9%, MOHOM 23.8% | Supported |
| R2: SANGO and MOHOM not FAIL | PASS, PASS | PASS, PASS | Supported |
| R3: ρ(G0 lift, T) > 0, k = 8 | ρ = 0.857, exact p = 0.0054 | ρ = 0.833, exact p = 0.0077 | Supported |

**Preregistered interpretation applied:** R1 and R2 hold, so the Phase 73 FAILs for SANGO and MOHOM are attributed to training configuration (trainability), not to their labels.

## 3. Comparison with Phase 73 (`v76_vs_p73.csv`)

**Run-to-run reference.** On EDUB and SCAR-I, epochs were unchanged (3 in both phases), and Phase 76 reproduces Phase 73 **item for item**: zero difference in out-of-fold predictions, transfer and YouLeQD. The pipeline is therefore deterministic in this environment, so the differences below are attributable to the change in epochs alone. (Phase 70 vs Phase 73 had differed by up to 3 of 70 YouLeQD items under identical settings in a different session.)

| Corpus | Epochs (CV) | ΔOOF accuracy, DistilBERT / RoBERTa (95% CI) | Gate 73 → 76 | ΔT, DistilBERT / RoBERTa |
|---|---|---|---|---|
| SANGO | 3 → 15 | +0.42 (0.36, 0.48) / +0.42 (0.35, 0.48) | FAIL → PASS | +0.18 / +0.25 |
| MOHOM | 3 → 43 | +0.46 (0.37, 0.56) / +0.51 (0.41, 0.60) | FAIL → PASS | +0.26 / +0.32 |
| YAHYA | 3 → 10 | +0.20 (0.17, 0.24) / +0.10 (0.07, 0.14) | PASS → PASS | +0.13 / +0.01 |
| GANI | 3 → 5 | +0.06 (0.05, 0.08) / +0.03 (0.01, 0.04) | PASS → PASS | +0.04 / +0.06 |
| SCAR-E | 3 → 4 (full fit unchanged) | +0.002 / −0.001 (n.s.) | PASS → PASS | 0 / 0 |
| EDUQG | 3 → 7 | +0.003 / −0.004 (n.s.) | FAIL → FAIL | +0.06 / +0.06 |
| EDUB, SCAR-I | unchanged | 0 | unchanged | 0 |

**Gate agreement with TF-IDF:** 5/8 → **7/8** for both models; only GANI differs (TF-IDF CAUTION, transformers PASS).

## 4. Overfitting (`p76_overfitting.csv`)

- **Memorisation:** training accuracy reaches 1.00 on SANGO and MOHOM (and on YAHYA for RoBERTa). Train–out-of-fold gaps are 0.16–0.29 on the small corpora and 0.04–0.10 on the large ones.
- **Not harmful relative to Phase 73:** out-of-fold accuracy and transfer improved substantially on the small corpora.
- **Not shown:** that the chosen epochs are optimal. Fewer steps might generalise equally well.

**YouLeQD decline for SANGO-trained models (23–26 → 17 of 70) is not overfitting.** The collapsed Phase 73 models predicted Comprehension, the YouLeQD majority class, for 58–67 of 70 questions, so they scored like a constant. The Phase 76 models predict all levels. Likewise MOHOM's Phase 73 score of 0/70 came from predicting "Create" for 69–70 questions.

## 5. Exploratory follow-ups (not preregistered)

| Analysis | DistilBERT | RoBERTa | Phase 73 value |
|---|---|---|---|
| TF-IDF G0 (fixed reference) vs transformer T | ρ 0.857, p 0.005 | ρ 0.833, p 0.008 | ρ 0.619, p 0.058 |
| First-word lookup (no training) vs T | ρ 0.833, p 0.008 | ρ 0.810, p 0.011 | ρ 0.571, p 0.076 |
| Size-matched TF-IDF G0 (n = 126) vs T | ρ 0.595, p 0.066 | ρ 0.619, p 0.057 | ρ 0.333, p 0.21 |
| G0 vs skill over majority | ρ 0.833, p 0.008 | ρ 0.619, p 0.057 | ρ 0.83 / 0.93 |
| Freedman–Lane partial, control log size | 0.857, p 0.009 | 0.834, p 0.012 | — |
| Freedman–Lane partial, control class balance | 0.686, p 0.033 | 0.655, p 0.044 | — |
| Freedman–Lane partial, both | 0.673, p 0.080 | 0.691, p 0.058 | — |
| ρ(G0, majority share) | −0.93 | −0.93 | −0.83 / −0.65 |

**Learner questions** (YouLeQD 70; paired video-cluster bootstrap; Holm across 16):
- the same three Scaria-trained models have unadjusted intervals below the constant, and none survives Holm;
- the LLM has lower vote loss than 12 of 16 models and is not distinguishable from the four Scaria-trained models.

These results are unchanged from Phase 73.

## 6. Trainability vs label validity

**What Phase 76 shows (trainability):**
- the Phase 73 FAILs on SANGO and MOHOM were caused by too few optimisation steps;
- with at least 300 steps, both corpora are learnable by both transformers, matching TF-IDF;
- with collapse removed, training-independent diagnostics (TF-IDF G0, first-word lookup) also predict transformer transfer.

So the transformer G0–transfer association is not explained by trainability alone.

**What it does not show (label validity):**
- that SANGO's or MOHOM's labels are valid; no independent expert labels exist for them (G1 untested);
- recoverability is not validity (SCAR-I shows that consistent but partly wrong labels are highly learnable);
- whether G0 and class balance have separate associations with transfer. They are collinear (ρ −0.93) in every model class at k = 8.

## 7. Effect on the manuscript (to decide with the author; manuscript not modified)

| v0.4 statement | Status after Phase 76 |
|---|---|
| Transformer gate decisions agree with TF-IDF on only 5/8 | Holds for Phase 73 settings; with adequate training, 7/8 |
| SANGO/MOHOM FAIL "through collapse" | Confirmed: attributable to training configuration (preregistered rule) |
| "No training-free diagnostic predicted transformer transfer" (Phase 75) | **Reversed under adequate training:** TF-IDF G0 and first-word lookup now do (exploratory); size-matched G0 is borderline |
| Transformer association survives both controls | Already withdrawn by the Freedman–Lane review; with Phase 76 values, not significant for either model (p 0.080, 0.058) |
| G0 is model- and configuration-relative | Holds, and now demonstrated experimentally rather than inferred |
| Recommendation: compute G0 with the deployment model plus a collapse check | Strengthened: add a minimum-steps rule, supported by one controlled experiment |


## 8. Errata to this report (found by the v0.5 numbers check)

Three p-values in Sections 5 and 7 were rounded from four-decimal intermediates (double rounding). They are corrected above:

| Value | Exact (count / 40,320) | Previously | Correct |
|---|---|---|---|
| Size-matched G0 vs RoBERTa transfer | 2,318 / 40,320 = 0.05749 | 0.058 | **0.057** |
| G0 vs skill over majority, RoBERTa | 2,318 / 40,320 = 0.05749 | 0.058 | **0.057** |
| Freedman–Lane, both covariates, RoBERTa | 2,357 / 40,320 = 0.05846 | 0.059 | **0.058** |

No conclusion changes. The QC script now compares every three-decimal value, correctly rounded, against its unrounded source.

## 9. Freedman–Lane appropriateness (verified before use in v0.5)

- **Implementation:** exact enumeration over all 8! permutations of reduced-model residuals. The statistic is corr(e_x, M·e_y[π]) with residual-maker M = I − X(X′X)⁻¹X′, which is algebraically identical to re-residualising "fitted + permuted residuals", because M annihilates the fitted values.
- **Type I error by simulation** (`fl_size_sim.py`; k = 8, ranks, 3,000 data sets per scenario, 2,000 permutations each; results reproduced exactly on rerun):
  - **4.5–5.3%** at nominal 5% when the covariate is unrelated to x or to y;
  - **7.4–10.1%** when the covariate is both collinear with x (ρ 0.65–0.93) and related to y;
  - the original Phase 75 method: **6.6–16.2%** throughout.
- **Our data:**
  - **Corpus size** is nearly unrelated to G0 and to transfer (|ρ| ≤ 0.12), so the size-controlled tests are in the valid regime.
  - **Class balance** is collinear with G0 (ρ −0.90 to −0.93) and related to transfer (ρ −0.62 to −0.90), the liberal regime; those p-values are therefore reported as descriptive (marked † in Table 11).
- **Reference verified:** Freedman, D., & Lane, D. (1983). *Journal of Business & Economic Statistics*, 1(4), 292–298. https://doi.org/10.1080/07350015.1983.10509354

## 10. Integration into manuscript v0.5

| Location | Content |
|---|---|
| §4.6 (new) | Phase 76 protocol, preregistration and amendment A1 |
| Table 3 | Phase 76 preregistration row |
| §5.5 | Phase 73 collapse results retained unchanged, with pointers to §5.6 |
| §5.6 (new) | Phase 76 results (R1–R3); Table 10 (Phase 73 vs Phase 76 by corpus); training–validation gaps; trainability, not validity |
| §5.7 (revised) | Freedman–Lane partials with simulation caveat; Table 11 (Phase 73 and Phase 76 columns); training-free diagnostics updated |
| Figure 6 | 2 × 3 panels; Phase 73 and Phase 76 transformer panels; collapsed corpora marked |
| §6.2 | Optimisation-check recommendation (no fixed budget); class-balance confound; no causal claim |
| §7, §8, Appendix A, Abstract | Updated accordingly; confirmatory study deferred; learner-question and LLM results secondary |
