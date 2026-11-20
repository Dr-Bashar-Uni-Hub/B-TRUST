# Missing artifacts register (v1.1)

| # | Artifact | Why it matters | Status |
|---|---|---|---|
| 1 | Fine-tuned DistilBERT checkpoint (Drive: Bloom_Research/Phase42_DistilBERT_Checkpoint) | Full probability vectors; re-scoring; hierarchical rule for DistilBERT | Not supplied |
| 2 | The script that actually produced the frozen Phase 42 predictions | run_phase42.py and both notebooks use proportional sampling and different LR settings; frozen artifacts use a 250-per-class test and max_features=50000, no sublinear TF, max_iter=2000 | Missing |
| 3 | Phase 37 source archive (Phase37_Human_Annotation_Audit) | Input to Phase 38 | Missing |
| 4 | Standalone Phase 46 / Phase 56 archives | Phase 56 documented in Phase 55 folder only | Not asserted to exist |
| 5 | EduBloom primary documentation (Kaggle page, generation process, licence) | Needed before describing its origin in print | Not obtained |
| 6 | DASQBT upstream source and annotation procedure; QYTL licence | Provenance and redistribution rights | Unknown; no licence file |
| 7 | LAK 2026 raw source and licence | Second external test | Only matched CSV available |
| 8 | Seeds / fold assignments for Phase 41 relevance OOF | Phase 41 vs Phase 43 relevance F1 discrepancy | Not saved |
| 9 | Independent large multi-annotator Bloom test set with source IDs | Required for any confirmatory or certification claim | Not available |
| 10 | Candidate external benchmarks (Ravikiran et al. 2026, Zenodo 10.5281/zenodo.20465724; Ferrato et al. 2026, Zenodo 10.5281/zenodo.19332485) | External validation | Not downloaded |
