# Scientific revision report — manuscript v0.4 → v0.5 (2026-11-20)

**Author:** Bashar ALHAJAHMAD (sole author).

**Basis:** the author's decisions of 2026-11-20. No new training and no API calls; one new statistical simulation (Freedman–Lane check).

**Status:** complete working draft; see `JOURNAL_SUBMISSION_READINESS_CHECKLIST_v0.5.md`.

## 1. Changes by decision

| Decision | Implementation in v0.5 |
|---|---|
| 1. Phase 76 as a separate robustness subsection | New §4.6 (protocol) and §5.6 (results, Table 10). All Phase 73 findings retained unchanged in §5.5, including the collapse. Figure 6 shows both protocols. Reports: 7/8 gate agreement; collapse eliminated (top class 24–36%); OOF accuracy +42 to +51 pp and transfer +18 to +32 pp on SANGO/MOHOM; R3 ρ 0.86 / 0.83 |
| 2. Interpretation | Phase 73 FAILs attributed to insufficient optimisation under the original fixed protocol, "for these two architectures and these two protocols". Stated as training-protocol sensitivity, not label validity (no expert labels exist for SANGO/MOHOM). Training–validation gaps (up to 0.29) reported, with explicit wording that overfitting is not shown to be absent or harmless |
| 3. Phase 75 revisions | Training-free-diagnostics conclusion revised: TF-IDF G0 and the first-word lookup predict transformer transfer once collapse is removed. Class-balance collinearity (ρ −0.90 to −0.93) reported for every class; no claim that G0 predicts transfer independently of balance. Freedman–Lane applied **after** verification (§2 below); labelled exploratory; balance-related p-values marked † as descriptive |
| 4. Minimum-training recommendation | §6.2 recommends checking for optimisation failure and single-class collapse (top-class share vs majority rate; training loss) before interpreting G0; explicitly not a validated 300-step minimum. Framework Figure 1 updated to name the check |
| 5. Confirmatory study deferred | Appendix A, §6.4, §7, §8: designed but deferred. Learner-question and LLM results labelled secondary throughout, including the Abstract; explicit statement of no superiority over human annotators or the strongest fine-tuned models |
| 6. Positioning | Abstract rewritten (412 → 291 words) around construct validity, the framework, recoverability–transfer, and trainability and class balance; preregistered vs exploratory labels kept |

## 2. Freedman–Lane verification

- **Implementation:** checked algebraically. The statistic corr(e_x, M·e_y[π]) equals the re-residualised form, because the residual-maker M annihilates the fitted values.
- **Simulation** (k = 8, ranks, 3,000 data sets per scenario; reproduced exactly on rerun): Freedman–Lane holds 4.5–5.3% at nominal 5% unless the covariate is both collinear with G0 and related to transfer; then 7.4–10.1%. The original Phase 75 method gave 6.6–16.2%.
- **Applied as:**
  - size-controlled tests, interpretable (size is nearly unrelated to G0 and transfer);
  - balance-controlled tests, descriptive only;
  - Holm across 12 partial tests leaves only TF-IDF controlling for size (adjusted p = 0.022).
- **Reference verified:** Freedman & Lane (1983), *JBES* 1(4), 292–298, doi:10.1080/07350015.1983.10509354.

## 3. Corrections found during this revision

| # | Issue | Correction | Effect |
|---|---|---|---|
| E1 | Three p-values in the Phase 76 report and the first v0.5 text were double-rounded (0.0575→0.058; 0.0585→0.059) | Corrected to 0.057, 0.057, 0.058 from exact permutation counts; QC now checks rounding against unrounded values | None on conclusions |
| E2 | Size-controlled range stated as "p ≤ 0.043" | "p = 0.002–0.042" | Precision only |
| E3 | Figure 1 and Tables 1, 2, 3, 7, 9 were not cited in the text | In-text citations added | Editorial compliance |
| E4 | Abstract 412 words | Rewritten to 291 words, all numbers re-verified | Journal limits |
| E5 | Table headers broke mid-word | Column widths rebalanced | Presentation |
| E6 | Phase 75 conclusion "no training-free diagnostic predicted transformer transfer" | Revised (it held only under collapse) | Conclusion changed, as approved |
| E7 | Phase 75 partial p-values from an invalid permutation scheme | Replaced with Freedman–Lane values plus the simulation caveat | DistilBERT and RoBERTa "both controls" claims withdrawn |

## 4. Quality control

- **Numbers:** `qc_numbers.py` runs **149 checks** (v0.4: 107; plus Phase 76, Freedman–Lane, simulation ranges, Holm, exact rounding). All pass; three-decimal values are compared, correctly rounded, against unrounded sources.
- **Tables 10 and 11:** generated from `v05_table10.csv` and `v05_table11.csv`, computed from archived outputs; no hand-transcribed values.
- **Citations:** 30 references; every in-text citation is listed and every reference cited (scripted check). All figures (1–6) and tables (1–12, A1) are cited in the text.
- **Hypothesis labels:**
  - preregistered: H1–H12, R1–R3;
  - exploratory: Phase 75 checks, Phase 76 follow-ups, simulations;
  - descriptive: transformer and LLM comparisons, as before.
- **Clustering:** video-cluster bootstrap unchanged for learner-question analyses.
- **Multiplicity:**
  - Holm within the partial-test family and the 16-model YouLeQD comparisons;
  - no global correction across preregistered hypotheses (each registered as its own primary test; listed as an optional supplementary table).

## 5. What the manuscript now claims, and does not

**Claims (with evidence status):**

- **EduBloom's labels encode difficulty** (descriptive; documented generation).
- **G0 predicts cross-corpus transfer** in four supervised model classes (preregistered), including transformers after collapse is removed (preregistered R3).
- **The association is not explained by corpus size** (exploratory, valid regime).
- **Recoverability is not validity**: SCAR-I.
- **Label correction and filtering did not improve transfer** (preregistered negative).
- **Certification is infeasible** at the available sample size (power analysis).
- **Gate decisions depend on the training protocol** (preregistered Phase 76).

**Does not claim:**

- that G0 predicts transfer independently of class balance;
- causal effects of recoverability;
- that 300 steps, or any budget, suffices in general;
- label validity for SANGO or MOHOM;
- that overfitting is absent or harmless;
- that the LLM or any model outperforms human annotators or the strongest fine-tuned models;
- algorithmic novelty.
