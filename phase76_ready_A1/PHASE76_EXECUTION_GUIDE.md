# Phase 76 — Colab execution guide (approved 2026-11-20)

**Notebook:** `Phase76_StepsMatched_Robustness_A1.ipynb`, sha256 `e8880619a239cb2440334d02e9f7c95561602fb703b839a3da3f66ede976e7dc`.

**Status: ready for execution.** No API calls; the notebook contains no LLM code.

## What was verified before handing over

1. **Real end-to-end test with PyTorch** (torch 2.14.1, transformers 4.46.3, the same versions as your Phase 73 run), on CPU, with your fine-tuned DistilBERT checkpoint standing in for the pretrained model. To fit the sandbox, the test used about 40 items per corpus and a 3-step minimum instead of 300. All of the following ran successfully:
   - the training loop with per-epoch loss logging;
   - post-training train accuracy;
   - fp16 checkpoint saving, with tokeniser and training config;
   - per-question predictions and gate files;
   - R1–R3 tests and the overfitting table;
   - the results-only archive;
   - resuming after an interruption.
2. **A saved checkpoint, reloaded, reproduced all 70 recorded YouLeQD predictions.**
3. **The code diff against the preregistered notebook** shows that training, data, splits and settings are unchanged; only saving, logging and the output folder changed (`A1_code_diff.txt`).
4. **Bug fixed:** the preregistered version (`68ae8b96`) still pointed its output folder at the Phase 73 location. Had it run with Drive enabled, it would have skipped every corpus and reported Phase 73 results. A1 writes only to `BTRUST_p76_out` and refuses any path containing "p73".

**Not testable here:** the GPU path and Colab's Drive mount. Cell 1 checks both and stops with a clear message if either fails.

## Before you start

- **Google Drive:** about **3.5 GB free** (16 fp16 models plus results). Fold weights are **off by default**; turning them on (`SAVE_CV_FOLD_WEIGHTS = True`) needs about 15 GB more.
- **Colab runtime:** Runtime → Change runtime type → **T4 GPU**.
- **Files to upload in cell 1:** `BTRUST_Frozen_Supporting_Files_2026-11-07.zip` and `BTRUST_v2.9_Phase76Ready_2026-11-20.zip`, selected together.
- **Your Phase 73 Drive folder is untouched.** Phase 76 writes only to `MyDrive/BTRUST_p76_out`.

## Running

| Step | Action | Expected |
|---|---|---|
| 1 | Run cell 1. Approve Drive access; upload both ZIPs | Prints versions, GPU (`Tesla T4`) and `Outputs -> /content/drive/MyDrive/BTRUST_p76_out` |
| 2 | Run cell 2 (corpora) | No assertion error (eight corpora with Phase 71 counts) |
| 3 | Run cell 3 (fine-tuning helper) | Defines functions; no output |
| 4 | Run cell 4 (training) | One line per model × corpus, e.g. `distilbert SANGO PASS 0.31 T 0.42 210s`. Longest steps: MOHOM (43 CV epochs) and RoBERTa on the large corpora. **About 3–4 h in total.** |
| 5 | Run cell 5 (tests) | Tables for R1–R3 and overfitting; downloads `p76_outputs.zip` (results only, no weights; a copy is also saved on Drive) |

**If Colab disconnects:** reconnect and run cells 1–4 again. Completed (model, corpus) pairs are skipped, because their files are already on Drive. A pair interrupted midway is redone from the start.

**Do not change** any setting other than the two save flags. The protocol fixes everything else.

## What to send back

1. `p76_outputs.zip`.
2. The run date, and the first line printed by cell 1 (versions and GPU).
3. Any warnings or errors, with the cell number.

The weights stay on your Drive; send them only if requested.

## Output files (in `BTRUST_p76_out`)

| File | Content |
|---|---|
| `environment.json` | torch, transformers, Python, GPU, save flags |
| `gate_<model>_<corpus>.json` (16) | G0 lift, κ, decision, per-target accuracy, mean transfer T, out-of-fold top-class share, full-fit epochs |
| `oof_<model>_<corpus>.csv` (16) | Out-of-fold predictions behind G0 (hashed item keys) |
| `items_<model>_<corpus>.csv` (16) | Per-question predictions for every target |
| `diag_<model>_<corpus>.jsonl` (16) | Per fit: epochs, steps, per-epoch loss, train accuracy |
| `p76_k8_<model>.csv`, `p76_tests.csv`, `p76_overfitting.csv` | Gate and transfer tables; R1–R3; train vs out-of-fold gap |
| `models/full/<model>_<corpus>/` (16) | fp16 weights, tokeniser, `b_trust_training_config.json` |

## What I will do with the results (validation plan)

1. **Recompute** every value from the per-question files, as for Phase 73.
2. **R1:** is collapse resolved on SANGO and MOHOM? (Out-of-fold top-class share below 80%.)
3. **R2:** are SANGO and MOHOM no longer FAIL?
4. **R3:** ρ(G0, T) at k = 8, plus the k = 6 sensitivity and skill over majority.
5. **Compare with Phase 73, per corpus:**
   - paired item-level difference in out-of-fold accuracy and in transfer, with bootstrap CIs;
   - changes in gate decisions;
   - run-to-run variation (±3 of 70 on YouLeQD under identical settings) used as the reference for "no real change".
6. **Overfitting:** train vs out-of-fold accuracy gap and final loss for each corpus, compared with Phase 73. Longer training that raises train accuracy without improving out-of-fold accuracy or transfer will be reported as overfitting.
7. **Trainability vs validity.** Phase 76 can show whether the Phase 73 FAILs were caused by training length (trainability). It cannot show that SANGO's or MOHOM's labels are valid; that needs independent expert agreement (G1) or target-population evidence (G2/G3).
