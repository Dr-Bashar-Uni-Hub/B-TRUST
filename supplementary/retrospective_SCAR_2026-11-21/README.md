# B-TRUST supplementary retrospective SCAR audit (2026-11-21)

This is an exploratory **post-hoc** analysis, not prospective educator validation or an evaluation of the complete B-TRUST G0–G4 framework.

## Contents
- `retrospective_SCAR_validation.ipynb`: original Colab analysis; requires `tables` reconstructed by the separate eight-corpus audit.
- `scar_hashed_oof_predictions.csv`: hashed text IDs, paired annotation labels, disagreement flags and out-of-fold scores. No raw question texts.
- `screening_metrics.csv`, `bootstrap_intervals.csv`, `review_budget_comparison.csv`: original notebook outputs.
- `summary.json`, `bloom_level_breakdown.csv`, `bootstrap_draws.csv`: final fixed-score lightweight analysis outputs.
- `reproduce_fixed_score_summary.py`: lightweight rerun from the hashed prediction CSV without original corpora or GPU.

The screening model predicts *disagreement* between two existing SCAR labeling schemes, not ground-truth Bloom correctness. Bootstrap intervals condition on saved out-of-fold scores; they do not reflect model retraining. The SCAR expert-consensus subset may be selected. Avoid treating SCAR-I and SCAR-E as independent question corpora.

Run: `python reproduce_fixed_score_summary.py` (requires pandas, numpy, scikit-learn).
