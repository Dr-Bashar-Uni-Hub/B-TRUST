# Preregistration amendment — Phase 69 (model-class robustness)
Written 2026-11-07 before any embedding-model result is computed. Phases 65–68 results are known.

Purpose: all gate scores and transfer results so far come from one model class (TF-IDF + LR). Test whether conclusions hold
for a dense-embedding model class.

Model M_emb: spaCy en_core_web_lg 3.8.0 (GitHub release wheel), document vector = mean of token vectors
(nlp.pipe with parser/ner/lemmatizer disabled), StandardScaler, LogisticRegression(C=1.0, max_iter=2000). No tuning.
Corpora, label maps, splits (StratifiedKFold 5, seed 65), leakage rule and targets: identical to Phases 65 and 68.

H8a (primary): Spearman rho(G0 lift under M_emb, mean transfer T under M_emb) > 0, exact one-sided permutation test, alpha 0.05, k = 5.
H8b (primary): the G0 decision (PASS/CAUTION/FAIL, same thresholds) is identical under M_emb and TF-IDF for all five corpora.
Secondary (no confirmatory weight): whether any corpus trained with M_emb beats the 37.1% majority on YouLeQD 70; DASQ-trained
G6 vote loss on YouLeQD under M_emb vs TF-IDF (0.724), paired video-cluster bootstrap 10,000, seed 69.
