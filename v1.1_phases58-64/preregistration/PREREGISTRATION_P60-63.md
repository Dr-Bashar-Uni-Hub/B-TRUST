# B-TRUST continuation — Preregistration for Phases 60–63
Written: 2026-11-07, BEFORE any new model output is compared to YouLeQD or LAK labels.
Hash of this file is recorded in `PREREG_SHA256.txt` before execution.

## Disclosure of what was already seen
- Frozen v1.0 results (Phases 38–57), annotator agreement statistics (Phases 38–39), and the Phase 58 audit findings (EduBloom labels ≈ difficulty band; frozen models ≈ majority baseline on YouLeQD).
- DASQBT training-side audit only (duplicates, overlap, label-by-first-word table). NO DASQBT-trained model has been applied to YouLeQD or LAK.

## Data
- Training (Bloom classifier): DASQBT `combined.csv` from YesNLP/QYTL (commit 42a67bc8), exact-duplicate-removed after whitespace/lowercase normalisation. Original Bloom taxonomy labels by name. `train_aug.csv` (LLM-generated) EXCLUDED from primary; used only in ablation A2.
- Evaluation A: YouLeQD 300 (sha256 67e3f66b…), three annotator votes, consolidated label, video id. 70 consolidated-relevant.
- Evaluation B: LAK 2026 learning outcomes, n=40. Fixed name mapping knowledge→Remember, comprehension→Understand, application→Apply, analysis→Analyze, evaluation→Evaluate, synthesis→Create (Anderson & Krathwohl 2001 correspondence). Set-membership scoring as in Phase 48.

## Fixed model (no tuning on any evaluation data)
M_DAS: TfidfVectorizer(ngram_range=(1,2), min_df=2, max_features=50000) + LogisticRegression(max_iter=2000, C=1.0), i.e. identical configuration to the frozen Phase 48 LR. Seed irrelevant (deterministic lbfgs).

## Granularities (fixed from literature convention, not data)
- G6: six original levels.
- G3: {knowledge, comprehension} | {application, analysis} | {evaluation, synthesis}.
- G2: LOTS {knowledge, comprehension, application} | HOTS {analysis, evaluation, synthesis}.
- Information weight w_g = log|Y_g| / log 6 (w6=1, w3≈0.613, w2≈0.387).

## Losses / estimands
- Vote loss at granularity g: ℓ_g(c; V) = 1 − (1/3) Σ_j 1[φ_g(V_j) = c]; an "irrelevant" vote never matches.
- Human reference h_g(V) = mean over ordered annotator pairs (j≠k) of 1[φ_g(V_j) ≠ φ_g(V_k)].
- Contamination = fraction of accepted Bloom decisions whose consolidated label is irrelevant.
- Information-weighted coverage U = mean over items of a(x)·w_{g(x)}.

## Phase 60 — E1 Base-model validity (PRIMARY)
H1: On the 70 consolidated-relevant YouLeQD items, M_DAS has lower mean G6 vote loss than the frozen EduBloom LR.
Test: paired video-cluster bootstrap (10,000 resamples of videos, seed 60); success iff 95% CI upper bound of (M_DAS − frozen LR) < 0.
Also reported (secondary, no success claim): vs frozen DistilBERT, vs constant-majority (comprehension), consolidated accuracy, Cohen's κ, balanced accuracy, permutation test vs independence, LAK set-membership accuracy with exact McNemar vs frozen models.
Ablations: A1 char 2–5-gram TF-IDF; A2 + train_aug; A3 class_weight='balanced'.

## Phase 61 — E2 Granularity-adaptive selection (PRIMARY for decision rule)
Rule HIER(t): accept at the finest g ∈ (G6, G3, G2) with max coarse probability ≥ t; else abstain. FLAT(t): accept G6 prediction iff max prob ≥ t.
Population: 70 relevant (oracle-relevance diagnostic) for E2a; full 300 with within-fold relevance gate for E2b.
H2: Area under the vote-loss vs information-weighted-coverage curve (AURC_w) for HIER < FLAT, using M_DAS.
Test: paired video-cluster bootstrap, 10,000 resamples, seed 61; success iff 95% CI upper bound of (HIER − FLAT) < 0.
AURC_w computed by sweeping t over the 101 grid values 0.00…1.00 and integrating loss over coverage by trapezoid on the realised (U, risk) points with U>0.

## Phase 62 — E3 Statistical validity of cluster-level testing (PRIMARY for inference component)
Semi-synthetic simulation using the actual YouLeQD video-size distribution (236 videos). Per-item loss Bernoulli with video random effect on logit scale; ICC ∈ {0, 0.2, 0.5}; true conditional risk set exactly at the cap (null boundary) α=0.5 and also above it (0.6).
Compare one-sided tests at δ=0.1: (i) row-level Hoeffding, (ii) row-level Clopper–Pearson, (iii) video-level Hoeffding on per-video mean of a(ℓ−α) (range [−α, 1−α]).
H3: video-level test keeps false-certification rate ≤ δ (+MC error 2·SE) for all ICC; at least one row-level test exceeds δ at ICC ≥ 0.2. 4,000 sims per cell, seed 62.
Also: power curves — number of videos needed to certify conditional risk ≤ α given true risk α−0.1 and α−0.2.

## Phase 63 — E4 Certification attempt on YouLeQD (EXPLORATORY; failure expected per E3 power)
Same 12 seeds / split scheme as Phase 57. Relevance model refitted within train. Thresholds λ=(τ_rel, t) on a fixed grid; fixed-sequence LTT ordered from most conservative; constraints α1=0.5 on vote loss at chosen granularity, α2=0.3 contamination, δ=0.1, video-level Hoeffding. Report nonempty count, test-set realised risk.

## Decision rules
- If H1 fails: the bottleneck is not only EduBloom label validity; report.
- If H2 fails: granularity backoff provides no measurable benefit here; report.
- Any success is "experimentally supported on this data", not "novel" — novelty requires the prior-art analysis in the report.
- No evaluation-set-dependent change to any setting in this file. Deviations, if any, will be logged in DEVIATIONS.md with reason.
