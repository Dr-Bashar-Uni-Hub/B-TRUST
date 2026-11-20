# Preregistration — Phase 71: replication of H7/H8 with k = 8 training corpora
Written 2026-11-19 before any model is trained on the Faraji et al. corpora. Known beforehand: all v1.0–v2.1 results; that DASQBT equals
the union of the four Faraji human corpora (+7 items) with identical labels; that Faraji's LLM file equals SCAR-E (99.9% label match);
row counts and label distributions of the new files. No model outputs on them.

Data: Faraji et al. repository (bloom-classification-aied2026-main, MIT licence), uploaded by the researcher; revised labels.
Training corpora (k = 8): EDUB, YAHYA (600), SANGO (415), MOHOM (126), GANI (1,200), SCAR-I, SCAR-E, EDUQG.
DASQ is dropped (it is the union of YAHYA, SANGO, MOHOM, GANI). Exact duplicates within a corpus are removed (first kept).
Targets: YAHYA, SANGO, MOHOM, GANI, SCAR-E, EDUQG, YouLeQD 70, LAK 40. A corpus is never tested on itself; SCAR-I and SCAR-E are never
tested on each other; leakage rule: drop test items whose normalised text occurs in the training corpus.
Models: TF-IDF LR (Phase 65 configuration) and spaCy en_core_web_lg mean-vector LR (Phase 69 configuration). No tuning.
Gates: G0 lift, κ_CV and decisions exactly as Phase 65 (5-fold, seed 65); G0b level coverage.

H11a (primary, TF-IDF): Spearman ρ(G0 lift, mean transfer accuracy T) > 0; exact one-sided permutation test over all 8! orderings, α = 0.05.
H11b (primary, embeddings): same test under the embedding model.
Secondary (no confirmatory weight): (i) ρ with T' = mean skill over target majority rate; (ii) sensitivity k = 7 dropping SCAR-I
(same-text dependence with SCAR-E); (iii) agreement of G0 decisions between model classes; (iv) any corpus beating the YouLeQD majority.
Interpretation: a replication success means G0 predicts relative transfer across more corpora; it does not establish absolute fitness for use.
