# B-TRUST v1.1 continuation (Phases 58–64) — 2026-11-07

This archive EXTENDS the immutable v1.0 freeze (`BTRUST_Frozen_Supporting_Files_2026-11-07.zip`, Phases 38–57). Nothing in v1.0 was modified.
Full narrative: the Claude Doc "B-TRUST v1.1 — Continuation Record (Phases 58–64) and Manuscript Plan".

## Status in one paragraph
B-TRUST is not a validated new algorithm. Phase 58 shows why earlier phases failed: EduBloom labels encode a 3-level difficulty band
(metadata-only rule = 50.0% on the frozen internal test, matching DistilBERT 50.9% / LR 48.2%), and the frozen models equal a
majority baseline on YouLeQD. Phase 57 also certified an infeasible event. Every controller component is prior art (Section 3 of the doc).
Preregistered results: H1 FAILED, H2 SUPPORTED only under oracle relevance (fails with the deployable gate), H3 SUPPORTED (modest).
Certification: 0/12 (exploratory). Phase 64 (exploratory): the label-recoverability audit separates DASQBT from EduBloom.

## Contents
- `preregistration/` — PREREGISTRATION_P60-63.md (sha256 1ea59177…), hash record, DEVIATIONS.md (D1, D2)
- `code/` — phase58_audit.py … phase64_recoverability.py; fetch_dasqbt.sh; run_all.sh
- `outputs/` — all result CSVs (record-level outputs carry comment IDs only, no comment text)
- `logs/` — console logs of the runs that produced `outputs/`
- `MISSING_ARTIFACTS.md`, `PHASE_LEDGER_v1.1.md`, `ENVIRONMENT.txt`, `SHA256_MANIFEST_v1.1.csv`

## Reproduce
1. Extract the v1.0 phase archives so that `/home/claude/bt/ex/<PhaseXX_…>/` exists (or edit the EX paths in the scripts).
2. `cd code && sh fetch_dasqbt.sh && sh run_all.sh`
Determinism: Phases 60–64 were re-run from a clean directory; all output CSVs were byte-identical (Phase 62 sha256 prefix b31d7b748079f2b1).

## Data rights
DASQBT and YouLeQD come from github.com/YesNLP/QYTL, which has NO licence file. They are not redistributed here.
Do not publish raw comment text or DASQBT questions without permission from the dataset authors.
