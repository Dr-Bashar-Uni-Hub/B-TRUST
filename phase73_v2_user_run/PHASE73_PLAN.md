# Phase 73 (v2) — implementation plan and run instructions

## Purpose
Test whether label recoverability (G0) predicts cross-corpus transfer for fine-tuned transformers on the same eight corpora as the
TF-IDF and embedding replications (Phase 71), and save per-question predictions so that paired, video-clustered comparisons become possible.
**No LLM component and no API calls** (Claude was evaluated in Phase 70).

## Preregistration
In the notebook's first cell (H12a, H12b, H12c, descriptive YouLeQD predictions). Notebook SHA-256: `9f3e3a49fef073a6ac4b4d634192fd86686d76e1d14f26e34f41babfee88d28f`.
This v2 supersedes the never-run v1 notebook (741c3605…), which contained an LLM section.

## What was verified before handing over
- Corpus loading reproduces the Phase 71 counts (asserted in the notebook).
- **End-to-end dry run** with a TF-IDF stand-in for `fit_predict` reproduced Phase 71's TF-IDF results exactly (rho 0.929, exact p 0.001116; all
  transfer values identical) and wrote all 51 output files. Only the transformer training function is untested here (no GPU in the sandbox).

## How to run (Google Colab)
1. Runtime → Change runtime type → **T4 GPU** (or better). Optionally uncomment the Google Drive lines in cell 1 so outputs persist.
2. Run cell 1; upload `BTRUST_Frozen_Supporting_Files_2026-11-07.zip` and `BTRUST_v2.6_ManuscriptPhase73_2026-11-19.zip`. Note the printed versions and GPU.
3. Run cells 2–4. Cell 4 trains 2 models × 8 corpora × (5 CV folds + 1 full fit) = 96 fine-tunes, roughly 2–3 h on a T4.
   **If Colab disconnects**, re-run cells 1–4: completed (model, corpus) pairs are skipped (needs Drive persistence, otherwise outputs are lost with the VM).
4. Run cell 5. It writes the tests and downloads `p73_outputs.zip`.
5. Send back `p73_outputs.zip` together with: run date, GPU type, printed torch/transformers versions, and any warnings or errors.

## Outputs (in p73_outputs.zip)
| File | Content |
|---|---|
| gate_<model>_<corpus>.json (16) | G0 lift, kappa, decision, per-target accuracy, mean transfer T, runtime |
| oof_<model>_<corpus>.csv (16) | Out-of-fold predictions behind each G0 value (item_key, y, oof_pred) |
| items_<model>_<corpus>.csv (16) | **Per-question predictions** for every target: YAHYA, SANGO, MOHOM, GANI, SCAR-E, EDUQG, YLQ70 (with row and video id), LAK40 (with reference set) |
| p73_k8_<model>.csv (2) | Gate and transfer table per model |
| p73_tests.csv | H12a/H12b rho and exact p; H12c separation |
Items are keyed by a hash of the normalised text; no question text is written.

## After the run (my side)
Validate as for Phase 70: recompute every number from the per-question files, check the samples, then run paired video-cluster comparisons on
YouLeQD (transformers vs constant, vs frozen models, vs the Phase 70 LLM) and update Table 8, Figure 5, Sections 5.2, 5.5 and 6.2 (Appendix A).
