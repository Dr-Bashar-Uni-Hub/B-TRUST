# Phase 73 — run by the researcher in Colab (GPU). Preregistered in the notebook's first cell.
Notebook sha256: 741c3605ee9ba9f8f15e9bb785b97a0298da9288aea20945717733285b52041a — record it with the run date.
Upload when prompted: BTRUST_Frozen_Supporting_Files_2026-11-07.zip and this BTRUST_v2.4 ZIP.
Tests: H12a/H12b transformers at k = 8 (same corpora as Phase 71); H12c PASS>FAIL separation; H10 LLM (needs your API key).
Saves YouLeQD item-level predictions (descriptive only). Corpus-loading cell tested locally (counts match Phase 71); GPU cells untested here.
Expected runtime on a T4: ~2–3 h for transformers (96 fine-tunes). Return all p73_*.csv files.

**SUPERSEDED (2026-11-19):** use phase73_v2_user_run/ instead. The v1 notebook includes an LLM section that must not be run
(it would repeat Phase 70 with paid API calls); v2 removes it and saves per-question predictions for all targets.
