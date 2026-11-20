# Phase 76 — steps-matched fine-tuning robustness experiment (PROPOSED; NOT RUN)
Requires the author's approval before execution. Preregistration (R1–R3 and interpretation rules) in the notebook's first cell.
Single manipulated factor vs Phase 73: epochs = max(3, ceil(300 / ceil(n_train / 16))) (at least 300 optimisation steps per fit).
Dry run with a TF-IDF stand-in: all 51 outputs written; R1–R3 bookkeeping works; stand-in reproduces Phase 71 exactly.
Run: Colab T4 GPU; upload BTRUST_Frozen_Supporting_Files_2026-11-07.zip and BTRUST_v2.8_*.zip; optional Google Drive persistence; ~3–4 h; no API calls.
Return p76_outputs.zip with run date, GPU and library versions.

**SUPERSEDED (2026-11-20):** do not run this version. Its output folder still pointed to the Phase 73 location (bug). Use phase76_ready_A1/
(notebook sha256 e8880619…), which adds the author-approved saving and diagnostics and fixes the output folder.
