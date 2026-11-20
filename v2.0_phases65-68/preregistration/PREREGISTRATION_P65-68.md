# B-TRUST v2 framework study — Preregistration, Phases 65–68
Written 2026-11-07 before any model is trained on Scaria or EduQG, and before any cross-corpus transfer is computed.
SHA-256 recorded in PREREG_SHA256.txt before execution.

## Disclosure of what was already seen
v1.0 + v1.1 results (Phases 38–64). For new corpora ONLY: row counts, label distributions, the Scaria intended-vs-expert-1
crosstab (used to verify that intended level = position mod 6), and the Faraji et al. (2026) published transfer matrix.

## Corpora (all labels mapped to revised levels 1–6: Remember … Create)
- EDUB: EduBloom, random 2,550-item subsample (seed 65) to equalise size; L1–L6 → 1–6 (provisional).
- DASQ: DASQBT combined.csv, exact-duplicate-removed (2,329); original names → revised (knowledge 1, comprehension 2, application 3,
  analysis 4, evaluation 5, synthesis 6). Very likely the Gani et al. (2023) 2,522-item combined set.
- SCAR-I: Scaria et al. (2024), 2,550 LLM-generated questions (nicyscaria/AEQG_Blooms_Evaluation_LLMs @0cd20696), intended level = row position mod 6 + 1.
- SCAR-E: same texts, expert consensus = both SkillLevel_1 and SkillLevel_2 present, in 1–6, and equal. (Set E.)
- EDUQG: EduQG (hadifar/question-generation @d253fe84), 903 questions with OpenStax bloom 1–4.
Held-out human-judged targets: YouLeQD 70 consolidated-relevant (3 votes), LAK 40 (set membership).
Excluded: kgb1802 CSV (30 items, no provenance); Mendeley CS (numeric keyword score, no levels).

## Fixed model
TF-IDF word 1–2-gram (min_df=2, max_features=50,000) + LogisticRegression(C=1, max_iter=2000). No tuning anywhere.
Leakage rule: every test set drops items whose normalised text appears in the training corpus.

## Framework gates (computed for every corpus)
- G0 Text recoverability: 5-fold stratified CV accuracy (seed 65); lift = acc − max(majority rate, metadata-only CV acc if metadata exist); κ_CV.
  Decision: FAIL if lift < 5 pp or κ_CV < 0.20; PASS if lift ≥ 15 pp and κ_CV ≥ 0.40; otherwise CAUTION.
- G0b Level coverage: number of revised levels with ≥ 30 items (6 required for six-level use).
- G1 Provenance validity (where independent expert labels exist): Cohen's κ between the corpus label source and each expert,
  relative to expert–expert κ.
- G3 Human ceiling (where ≥ 2 experts): exact and adjacent (|Δ| ≤ 1) agreement and κ at G6, G3, G2.

## Phase 66 — H5 PRIMARY (label-source controlled experiment)
On set E (identical texts), train M_I on intended labels and M_E on expert-consensus labels.
Primary endpoint: accuracy on DASQ (largest independent human-labelled corpus).
Test: paired bootstrap over DASQ items, 10,000 resamples, seed 66, of acc(M_E) − acc(M_I). SUPPORTED iff 95% CI lower bound > 0.
Secondary (no confirmatory weight): exact McNemar on DASQ; EDUQG accuracy; YouLeQD 70 G6 vote loss; LAK 40.

## Phase 67 — H6 PRIMARY (provenance filtering vs quantity-matched and data-driven baselines)
All trained on SCAR-I intended labels:
- ALL: all 2,550.
- PROV: items in E whose intended label equals the expert consensus.
- RAND: random subsets of ALL with |PROV| items, 20 draws (seed 67); item-level correctness averaged over draws.
- CL: confident-learning pruning of ALL (5-fold OOF probabilities, seed 67; drop item if p(intended) < mean p(class) over items labelled that class).
- CLm: CL then random subsample to |PROV| (20 draws, averaged).
Primary H6: acc(PROV) − acc(RAND) on DASQ, paired bootstrap over items (10,000, seed 67); SUPPORTED iff CI lower bound > 0.
Exploratory: PROV vs CLm, PROV vs ALL, CL vs ALL; same metrics on EDUQG and YouLeQD.

## Phase 68 — H7 EXPLORATORY-CONFIRMATORY (do gates predict transfer?)
Training corpora: EDUB, DASQ, SCAR-I, SCAR-E, EDUQG (k = 5).
Transfer score T(C) = mean accuracy over external human-judged targets {DASQ, SCAR-E, EDUQG, YouLeQD 70 (consolidated), LAK 40},
excluding C itself and, for SCAR-I/SCAR-E, each other.
H7: Spearman ρ(G0 lift, T) > 0, exact one-sided permutation test over 120 orderings, α = 0.05.
With k = 5 only a perfect ordering reaches p < 0.05; a failure is weak evidence. Also reported: ρ(κ_CV, T).

## Decision rules
Each hypothesis is reported as supported/failed exactly as defined. Novelty claims require the prior-art comparison in the
report; a supported H5/H6 shows label provenance matters for transfer, not that a new learning algorithm exists.
Deviations go to DEVIATIONS.md before re-analysis.
