// Part 2 — Methodology, Experimental Setup, Results
const { C, P, H1, H2, H3, B, N, img, eq, caption, table, tcap, gap } = require("./build_part1.js");

// ---------------- 3 Methodology ----------------
C.push(H1("3. Methodology"));
C.push(H2("3.1 Design"));
C.push(P("The study evaluates Bloom classifiers in two directions. *Inward*, it asks whether a training corpus's labels carry construct-relevant information in the text and agree with independent experts. *Outward*, it asks whether models trained on a corpus agree with human judgement on other populations, especially learner-posed questions, and whether any selective policy can be certified. The validity gates (Section 3.4) formalise the inward checks; the transfer and certification analyses formalise the outward ones. Figure 1 summarises the framework."));
C.push(img("fig0_framework", 600));
C.push(caption("Figure 1.", "The B-TRUST validity-first evaluation framework. Inputs (layer 1) are prepared and checked for duplicates and leakage. The six checks (layer 2) are grouped by the evidence each requires, not by a fixed order: G0b needs only the corpus labels; G0 needs a model trained on the corpus by cross-validation and is therefore relative to that model class and configuration (dashed arrow from layer 3); G1 needs independent expert labels on a sample; G2 and G3 need human-labelled target-population data (G3 provides the human ceiling against which G2 is read); G4 needs calibration data, a model and a prior power analysis. A FAIL or CAUTION routes to investigation (dotted arrows), not to an automatic verdict that the labels are invalid. Layer 3 lists the model classes and targets used in this study; the zero-shot LLM has no training corpus and enters only target-level checks. Layer 4 summarises the outputs. The framework organises existing validity reasoning and statistical tools; it is not a new learning algorithm."));
C.push(H2("3.2 Data"));
C.push(P("All labels were mapped to the revised taxonomy order (1 Remember … 6 Create). Original-taxonomy names were mapped by name (knowledge 1, comprehension 2, application 3, analysis 4, evaluation 5, synthesis 6), following the correspondence in Anderson and Krathwohl (2001). Because the original taxonomy places Synthesis below Evaluation and the revised places Create above Evaluate, this alignment is provisional. Exact duplicate texts within a corpus were removed, and no exact text overlaps between corpora. Table 1 lists the training corpora."));
C.push(tcap("Table 1.", "Training corpora. n is after removing exact duplicates."));
C.push(table(["Corpus", "Label source", "n", "Source and licence"], [
  ["EDUB", "Generated corpus; level assigned together with difficulty and type fields", "2,550", "Random subsample (seed 65) of 73,712 items; EduBloom (Sharma et al., n.d.), CC BY-SA 4.0"],
  ["YAHYA", "Human-authored, labelled", "599", "Yahya et al. (2012), via Faraji et al. (2026), MIT"],
  ["SANGO", "Human-authored, labelled", "413", "Sangodiah et al. (2017), via Faraji et al. (2026), MIT"],
  ["MOHOM", "Human-authored, labelled", "126", "Mohammed & Omar (2020), via Faraji et al. (2026), MIT"],
  ["GANI", "Human-authored, labelled", "1,185", "Gani et al. (2023), via Faraji et al. (2026), MIT"],
  ["SCAR-I", "LLM generator's intended level", "2,550", "Scaria et al. (2024), MIT; intended level reconstructed from row order"],
  ["SCAR-E", "Two-expert consensus on the same texts", "1,839", "Items both experts rated and agreed on; experts were blind to the intended level"],
  ["EDUQG", "Levels distributed with expert-written MCQs", "903", "Hadifar et al. (2023); levels 1–4 only; no licence file"]],
  [1.0, 2.6, 0.6, 3.6]));
C.push(gap());
C.push(P("Earlier phases pooled the four human-authored corpora as \"DASQ\" (2,329 items), which is their union plus seven items. Results reported for DASQ are labelled as such."));
C.push(P("**Held-out human-judged targets.**"));
C.push(B("**YouLeQD 70.** Of 300 learner questions from YouTube lecture comments coded by three annotators (Ming et al., 2025), 70 have a consolidated Bloom label; the rest were consolidated as irrelevant. Annotators used the original taxonomy and could code a question as irrelevant. The questions come from lecture videos, which define the clusters for inference. The file used is byte-identical to the authors' public release."));
C.push(B("**LAK40.** Forty learning outcomes extracted from the file `Bloom-All_40.csv` by keeping the rows whose `Annotator` value is `groundtruth`. The file was released with Xu et al. (2026) in their LAK '26 repository; our 40 items match its ground-truth rows exactly, including identifiers and reference sets. Their appendix describes the parent dataset as 21,380 learning objectives from 5,558 courses at an Australian university, annotated by a trained annotator with a second annotator on a 30% subset (κ = 0.63 before and 0.80 after discussion). This matches the dataset of Li et al. (2022), but the appendix does not cite it, so the link is inferred from the description. Two items have more than one acceptable level; we score set membership, treating a prediction as correct if it is in the reference set. The appendix states that single-label objectives were sampled for its evaluation set, which does not match these two multi-label items; we report the discrepancy and preserve the items. The file also contains two further annotators (A1, A2), used here only to describe the human ceiling. The repository has no licence file."));
C.push(B("**Cross-corpus targets.** Each training corpus was also tested on the other human-judged corpora (YAHYA, SANGO, MOHOM, GANI, SCAR-E, EDUQG). A corpus was never tested on itself, SCAR-I and SCAR-E were never tested on each other, and test items whose normalised text appeared in the training corpus were dropped."));
C.push(H2("3.3 Losses and reference quantities"));
C.push(P("For a question with m annotator votes V1, …, Vm and a granularity map φg (identity at six levels; three bands {1,2}, {3,4}, {5,6}; or two bands {1,2,3}, {4,5,6}), the vote loss of predicting class c is given in Equation 1, where an \"irrelevant\" vote never matches. It is the probability of disagreeing with a randomly drawn annotator."));
C.push(...eq("eq1", 300, "1"));
C.push(P("The human reference (Equation 2) is the same quantity for one annotator against another. The best constant is the single class with the lowest mean loss; it is chosen using the labels and is therefore an optimistic baseline."));
C.push(...eq("eq2", 330, "2"));
C.push(H2("3.4 Validity gates"));
C.push(P("**Three properties to keep apart.** *Label validity* is whether a label correctly describes the cognitive demand of an item; it can be checked only against independent judgement (G1, and on target populations G2 and G3). *Label recoverability* is whether the label can be predicted from the item text by some model; high recoverability does not imply validity, because consistent but wrong labels are also learnable. *Model trainability* is whether a particular model class and training configuration can learn from a corpus of a given size; it limits measured recoverability. G0 measures recoverability through a chosen model, so a low G0 can reflect low trainability rather than low recoverability (Sections 5.5 and 5.6)."));
C.push(P("The checks are not a strict sequence. G0b can be computed from the labels alone and G0 from the corpus alone, before any deployment; G1 needs expert labels; G2–G4 need target-population evidence. Any FAIL or CAUTION is a prompt to investigate (training collapse, corpus size, class imbalance, metadata leakage, provenance, taxonomy alignment), not by itself evidence that a corpus is invalid or unusable."));
C.push(P("**G0 — recoverability.** Five-fold stratified cross-validated accuracy of a text model, minus the larger of the majority rate and the cross-validated accuracy of a lookup on metadata (where metadata exist):"));
C.push(...eq("eq3", 420, "3"));
C.push(P("FAIL if lift < 5 percentage points or cross-validated κ < 0.20; PASS if lift ≥ 15 points and κ ≥ 0.40; otherwise CAUTION. These thresholds were set a priori and have not been calibrated against an external criterion."));
C.push(B("**G0b — coverage.** At least 30 items at each of the six levels."));
C.push(B("**G1 — provenance.** Where independent expert labels exist: κ between the corpus label source and each expert, divided by expert–expert κ."));
C.push(B("**G2 — target skill.** Vote loss or accuracy on the target population, relative to the best constant."));
C.push(B("**G3 — human ceiling.** Leave-one-annotator-out vote loss and κ at each granularity."));
C.push(B("**G4 — decision readiness.** A power calculation for certification before any calibration is attempted."));
C.push(P("Cross-corpus transfer T is a training corpus's mean accuracy over its admissible targets (Section 3.2)."));

// ---------------- 4 Experimental Setup ----------------
C.push(H1("4. Experimental Setup"));
C.push(H2("4.1 Models"));
C.push(P("Table 2 lists the model classes and their configurations."));
C.push(tcap("Table 2.", "Model classes. No hyperparameters were tuned on any evaluation data."));
C.push(table(["Model class", "Configuration", "Phases"], [
  ["TF-IDF logistic regression", "Word 1–2-grams, min_df 2, 50,000 features, C = 1, max_iter 2,000", "60–71"],
  ["Word-embedding logistic regression", "spaCy en_core_web_lg 3.8.0 mean token vectors, standardised; C = 1", "69, 71"],
  ["Fine-tuned transformers", "distilbert-base-uncased and roberta-base; max length 64, batch 16, learning rate 2e-5, 3 epochs, weight decay 0.01, seed 70", "70, 73, 76 (run by the author in Colab)"],
  ["Zero-shot LLM", "claude-sonnet-5-5; one-word original-Bloom prompt; settings in Section 4.5", "70 (run by the researcher)"],
  ["Frozen EduBloom models", "TF-IDF LR and fine-tuned DistilBERT from an earlier phase; both reproduced from saved weights (300/300 and 1,498/1,500 predictions identical; the two differences are numerical near-ties)", "58–63"]],
  [2.0, 5.2, 1.6]));
C.push(gap());
C.push(H2("4.2 Statistical inference"));
C.push(B("**Paired model comparisons:** video-cluster bootstrap with 10,000 resamples, exact McNemar tests, and Holm or Bonferroni correction where stated."));
C.push(B("**Gate–transfer association:** Spearman ρ with an exact one-sided permutation test over all orderings (120 for k = 5; 720 for k = 6; 40,320 for k = 8). With k = 5 only a perfect ordering can reach p < 0.05."));
C.push(B("**Partial associations (exploratory):** Spearman partial correlations controlling for log corpus size and/or majority-class share, tested with the Freedman–Lane permutation procedure (Freedman & Lane, 1983) by exact enumeration; its behaviour in this setting was checked by simulation (Section 5.7)."));
C.push(B("**Fine-tuned models on YouLeQD (Phase 73, descriptive):** each of the 16 model–corpus combinations was compared with the constant and with the LLM by paired video-cluster bootstrap (10,000 resamples, seed 73), with Holm correction across the 16 comparisons."));
C.push(B("**Certification:** video-level Hoeffding (1963) tests within Learn-then-Test (Angelopoulos et al., 2025) fixed-sequence search over thresholds, with Bonferroni across relevance thresholds. Validity under clustering was checked by simulation using the real distribution of comments per video, with intraclass correlation 0, 0.2 and 0.5 and 4,000 simulations per cell."));
C.push(H2("4.3 Preregistration and deviations"));
C.push(P("Table 3 lists the preregistrations and their status."));
C.push(tcap("Table 3.", "Preregistrations. Each file was hashed (SHA-256) before the corresponding outcomes were computed."));
C.push(table(["Preregistration", "Hypotheses", "SHA-256 prefix", "Status"], [
  ["Phases 60–63", "H1 (base model), H2 (granularity back-off), H3 (clustered inference), certification", "1ea59177", "Reported"],
  ["Phases 65–68", "H5 (label source), H6 (provenance filtering), H7 (gate predicts transfer, k = 5)", "6c60ecc9", "Reported; H7 superseded by H11a"],
  ["Phase 69 amendment", "H8a, H8b (embedding robustness, k = 5)", "61c720d7", "Reported"],
  ["Phase 70 notebook", "H9a–H9d (transformers, k = 5); H10 (LLM vs constant)", "6fd8d2e6", "Reported"],
  ["Phase 71", "H11a, H11b (k = 8 replication, TF-IDF and embeddings)", "e66af025", "Reported"],
  ["Phase 73 notebook (v2)", "H12a–H12c (transformers, k = 8); no LLM component", "9f3e3a49", "Reported"],
  ["Phase 76 notebook", "R1–R3 (steps-matched retraining); pre-run amendment A1 added saving and diagnostics only", "68ae8b96; A1 e8880619", "Reported"]],
  [1.6, 3.8, 1.5, 1.6]));
C.push(gap());
C.push(P("All deviations were logged before re-analysis. D1: the coverage range for one area-under-curve comparison was unspecified, so both versions were required to agree. D2: an implementation flaw in a certification search was found after the run; a whole-grid diagnostic showed it did not affect the conclusion. D3–D5: added robustness checks and interpretation notes. The Phase 70 deviations are described in Section 4.5."));
C.push(H2("4.4 Learner-question target and relevance"));
C.push(P("Deployable analyses on all 300 comments need a relevance step. In the granularity analysis (H2), a character n-gram relevance model was cross-fitted over five video-grouped folds; at threshold 0.5 it admitted 66 of the 300 comments, of which 39 were relevant. In the certification analyses, the relevance model was refitted within each of 12 video-disjoint train/calibration/test splits. Contamination by irrelevant comments is reported with every deployable result."));
C.push(H2("4.5 Zero-shot LLM protocol and deviations (Phase 70)"));
C.push(P("The LLM was run by the researcher on all targets: 500-item random samples of DASQ and SCAR-E (drawn with the preregistered seed and verified to match it exactly), all 903 EDUQG items, YouLeQD 70 and LAK40. The run deviated from the preregistered configuration in four ways:"));
C.push(B("output limit of 128 tokens instead of 5;"));
C.push(B("a model reasoning setting was enabled;"));
C.push(B("sampling temperature was left at the API default instead of 0, so predictions are stochastic and a rerun would not reproduce them item-for-item;"));
C.push(B("predictions were assembled from cached runs. The researcher's execution history documents a consistent configuration, but the cache stores no request metadata and its key could not be reconstructed (1,378 candidate constructions tested), so consistency is not independently verified."));
C.push(P("One DASQ item, a question truncated in its source, produced a parser failure: the model answered \"Knowledge\" and then explained the truncation. It was scored as incorrect; a lenient first-word parser would also have scored it incorrect, so no accuracy changes. All reported LLM numbers were recomputed from the item-level file."));
C.push(H2("4.6 Training-protocol robustness (Phase 76)"));
C.push(P("Phase 76 repeated the Phase 73 transformer analysis with one change: epochs = max(3, ⌈300 / steps per epoch⌉), so that every fit had at least 300 optimisation steps. Its preregistration (hypotheses R1–R3 and interpretation rules) was written after Phase 73 and the exploratory Phase 75 analyses were seen, and before it was run. A pre-run amendment (A1) added only artifact saving and diagnostics (per-epoch training loss, post-training train accuracy, model checkpoints) and corrected an output path. Training was unchanged, as verified by a code diff and by item-for-item reproduction of Phase 73 on the corpora whose configuration did not change."));
C.push(H2("4.7 Reproducibility"));
C.push(P("Every analysis run in the project environment was re-executed from a clean directory and produced byte-identical outputs. Author-run Colab outputs (Phases 70, 73 and 76) were re-analysed from their item-level files; every Phase 73 and Phase 76 value, including item sets and leakage exclusions, recomputed exactly. The frozen EduBloom models are reproducible from their saved weights but not from code, because the archived training script does not match them."));

// ---------------- 5 Results ----------------
C.push(H1("5. Results"));
C.push(H2("5.1 RQ1 — EduBloom labels encode difficulty, not cognitive level (descriptive)"));
C.push(P("EduBloom's documentation states that its questions were generated and then categorised by Bloom level, question type and difficulty, without describing expert validation (Sharma et al., n.d.). Its labels follow the difficulty field (Figure 2), and a model trained on it learns the same three bands (Figure 3). Table 4 summarises the evidence."));
C.push(img("fig1_edubloom_difficulty_level", 470));
C.push(caption("Figure 2.", "EduBloom label counts by difficulty field (all 73,712 items). Easy items are labelled only L1 or L2, Medium L2–L4, and Hard L4–L6."));
C.push(tcap("Table 4.", "Evidence that EduBloom labels encode difficulty rather than text-recoverable cognitive level."));
C.push(table(["Evidence", "Value"], [
  ["Question templates (topic removed) carrying more than one label", "92.8% of 10,753"],
  ["Metadata-only rule (difficulty, no text), balanced internal test of 1,500", "50.0%"],
  ["Frozen fine-tuned DistilBERT / TF-IDF LR on the same test", "50.9% / 48.2%"],
  ["DistilBERT predictions of L4 / L2 on that test", "0 / 3 of 1,500"],
  ["TF-IDF LR, all 73,712 items, natural class priors, 5-fold", "38.8% (38.7% with question stems held out)"],
  ["Question stems shared by L5 (Evaluate) and L6 (Create)", "787 of about 793"],
  ["Jensen–Shannon distance of stem distributions, L5 vs L6", "0.217 (every other level pair 0.50–1.00)"],
  ["Questions containing a creation verb, L6 / L5", "4.9% / 4.6%"],
  ["G0 lift over the metadata-only rule (2,550-item subsample)", "+0.04 percentage points (FAIL)"]],
  [5.6, 2.8]));
C.push(gap());
C.push(img("fig2_distilbert_confusion", 300));
C.push(caption("Figure 3.", "Confusion matrix of the frozen fine-tuned DistilBERT on the balanced EduBloom internal test (250 items per level). The model almost never predicts L2 or L4, consistent with having learned three difficulty bands."));
C.push(P("Stems never cross difficulty bands (L1 vs L3–L6 Jensen–Shannon distance 1.000). The generator evidently drew stems from separate Easy, Medium and Hard pools and assigned levels within each pool, so the text cannot distinguish \"Create\" from \"Evaluate\"."));

C.push(H2("5.2 RQ2 — Agreement with learner-question annotators"));
C.push(P("**Frozen EduBloom models (descriptive).** On YouLeQD 70, the fine-tuned DistilBERT's accuracy (26/70, 37.1%) equalled the always-Comprehension baseline and the LR was lower (23/70, 32.9%). Neither model's agreement exceeded independence (κ = 0.107 and 0.096; permutation p = 0.085 and 0.083). DistilBERT predicted L1 for 240 of the 300 comments."));
C.push(P("**Taxonomy-matched training (confirmatory, H1 failed).** An LR trained on the pooled human-authored corpora (DASQ) reduced six-level vote loss by only 2.9 points relative to the frozen EduBloom LR (0.724 vs 0.752; 95% CI −12.2 to +6.8). Its agreement nonetheless exceeded independence (κ = 0.146, permutation p = 0.003; exploratory)."));
C.push(P("**Zero-shot LLM (H10 confirmatory; other rows exploratory).** Table 5 reports H10 and its robustness checks. H10 is supported only on its preregistered metric, six-level vote loss. Comprehension was the best constant under both vote treatments. All 43 non-Bloom votes were explicit \"irrelevant\" codes, which penalise every predictor equally and therefore cancel in paired differences."));
C.push(tcap("Table 5.", "Zero-shot LLM versus the best constant classifier (Comprehension) on YouLeQD 70. Negative differences favour the LLM."));
C.push(table(["Comparison", "Estimate", "95% CI", "Result"], [
  ["**H10:** six-level vote loss, video-cluster bootstrap (preregistered)", "−0.148 (0.590 vs 0.738)", "−0.232 to −0.065", "Supported"],
  ["Six-level vote loss, irrelevant votes excluded", "−0.164", "−0.267 to −0.057", "Holds"],
  ["Six-level vote loss, item-level bootstrap", "−0.148", "−0.233 to −0.067", "Holds"],
  ["Consolidated-label error, 34/70 vs 26/70 correct", "−0.114", "−0.250 to +0.029", "Not significant (McNemar p = 0.17)"],
  ["Three-band vote loss (exploratory)", "−0.067", "−0.154 to +0.015", "Not significant"],
  ["Two-band vote loss (exploratory)", "−0.076", "−0.162 to 0.000", "Not significant"]],
  [3.6, 1.7, 1.5, 1.8]));
C.push(gap());
C.push(P("In exploratory paired comparisons with every model that has item-level YouLeQD predictions (Table 6), the LLM had lower vote loss, with Bonferroni-corrected intervals excluding zero. No accuracy difference survived Holm correction."));
C.push(tcap("Table 6.", "Exploratory paired comparisons on YouLeQD 70 (identical items). Vote-loss differences are LLM minus comparator; McNemar counts are items only the LLM got right vs only the comparator got right."));
C.push(table(["Comparator", "Comparator vote loss", "Difference (95% CI)", "Bonferroni 98.75% CI", "McNemar", "Holm p"], [
  ["Frozen EduBloom LR", "0.752", "−0.162 (−0.243, −0.078)", "−0.266, −0.055", "19 vs 8", "0.21"],
  ["Frozen EduBloom DistilBERT", "0.748", "−0.157 (−0.253, −0.064)", "−0.277, −0.035", "22 vs 14", "0.51"],
  ["Constant (Comprehension)", "0.738", "−0.148 (−0.232, −0.065)", "−0.255, −0.039", "17 vs 9", "0.51"],
  ["DASQ TF-IDF LR (Phase 60)", "0.724", "−0.133 (−0.221, −0.044)", "−0.244, −0.019", "17 vs 9", "0.51"]],
  [2.2, 1.2, 2.0, 1.6, 1.0, 0.8]));
C.push(gap());
C.push(P("**Fine-tuned transformers (Phase 73; descriptive, with paired tests).** Phase 73 saved per-question predictions for 16 fine-tuned models (two architectures × eight training corpora). Against the constant, three models trained on Scaria data had lower six-level vote loss with unadjusted intervals excluding zero: DistilBERT trained on SCAR-E (−0.090, 95% CI −0.174 to −0.013), and RoBERTa trained on SCAR-I (−0.086, CI −0.167 to −0.014) and on SCAR-E (−0.086, CI −0.171 to −0.005). None survived Holm correction across the 16 comparisons (adjusted p = 0.27–0.45). Both models trained on MOHOM scored 0/70 and were significantly worse than the constant, a consequence of training collapse (Section 5.5)."));
C.push(P("The LLM had lower vote loss than 12 of the 16 fine-tuned models, but its differences from the four Scaria-trained models had intervals that included zero (for example, −0.057, CI −0.147 to +0.034, against DistilBERT trained on SCAR-E). We therefore make no claim that the LLM outperforms the best fine-tuned models."));
C.push(P("**Run-to-run variation.** Phase 70 and Phase 73 fine-tuned the same two architectures on four shared corpora with identical settings. G0 lift differed by less than 0.01, but YouLeQD scores differed by up to three of 70 items; RoBERTa trained on SCAR-E scored 33/70 in Phase 70 and 30/70 in Phase 73. The earlier observation was within run-to-run variation."));

C.push(H2("5.3 RQ3 — The human ceiling (descriptive)"));
C.push(P("YouLeQD annotators agreed on the exact level in 44–56% of pairwise comparisons where both coded a question as relevant (κ = 0.22–0.40), and all three agreed on only 9 of the 70 questions. Their leave-one-annotator-out six-level vote loss was 0.686, so supervised models at 0.72–0.75 had only about 4–7 points of headroom (Figure 4)."));
C.push(img("fig3_vote_loss_granularity", 520));
C.push(caption("Figure 4.", "Mean vote loss on YouLeQD 70 at six levels and two coarser groupings (lower is better). Coarse values for all models are computed by coarsening each model's six-level prediction; under the preregistered coarse-probability rule, the pooled human-authored LR scores 0.600 (three bands) and 0.500 (two bands). The best constant is chosen using the labels. \"Human (leave-one-out)\" is one annotator scored against the others."));
C.push(P("The LLM's vote loss (0.590) fell below the human reference (difference −0.095, 95% CI −0.165 to −0.015; exploratory). This reflects agreement with the annotator majority, which a single annotator cannot achieve by construction; it is not evidence of better-than-human judgement. At coarser granularity the best constant (always \"lower-order\") was hard to beat: its three- and two-band losses (0.552 and 0.481) were below the pooled human-authored LR's under either decision rule."));
C.push(P("Agreement depended strongly on the item population. The two Scaria experts agreed on 88.8% of generated questions at the exact level (κ = 0.864; n = 2,071). On LAK40, the two additional annotators agreed with the ground truth on 80.0% and 87.5% of outcomes (any overlap of label sets) and with each other on 60.0% of exact label sets (κ = 0.58 on first labels); for comparison, the LLM's set-membership accuracy on LAK40 was 72.5%. These are descriptive reference points from different item populations, not a ranking."));

C.push(H2("5.4 RQ4 — Abstention and certification"));
C.push(P("**Granularity back-off (confirmatory, H2).** Backing off from six levels to three bands to two bands lowered the area under the vote-risk curve, weighted by the information retained, by 8.1 points when an oracle relevance filter was used (95% CI −14.8 to −1.5; the common-coverage version agreed, −8.2, CI −15.2 to −1.7). With the learned relevance gate on all 300 comments, the reduction was not significant (−1.0, CI −2.3 to +0.4). Part of the oracle gain reflects the item mix, because constants were strong at coarse levels (Section 5.3)."));
C.push(P("**Clustered inference (confirmatory, H3 supported).** In simulation at the null boundary, video-level tests kept false certification at 0.9–1.5% in every cell (limit 10%). Row-level Clopper–Pearson exceeded the limit under strong clustering, reaching 13.0% at intraclass correlation 0.5. Because YouLeQD videos average 1.27 comments, clustering is a secondary issue for these data."));
C.push(img("fig5_power", 360));
C.push(caption("Figure 5.", "Simulated power of the video-level Hoeffding test to certify conditional risk ≤ 0.5 at δ = 0.1, by number of independent sources of accepted decisions (log scale), for true risks 0.3 and 0.4 and intraclass correlation 0 and 0.5. The dotted line marks 80% power."));
C.push(P("**Power (descriptive).** Certifying a conditional risk of at most 0.5 for a model whose true risk is 0.4 required about 236 independent sources of accepted decisions for 84–85% power across intraclass correlations of 0–0.5; 120 sources gave 52–53% (Figure 5)."));
C.push(P("**Certification on YouLeQD (exploratory).** No nonempty policy was certified in any of 12 video-disjoint splits. Even the most favourable single threshold, ignoring multiplicity, gave p ≥ 0.986: at thresholds where calibration risk looked acceptable, only 1–4 decisions were accepted out of 59 calibration videos. An earlier certification attempt had also failed, for a design reason: it tested \"disagrees with at least one annotator\", an event occurring for 93–96% of relevant questions, against caps of 0.8–0.9."));

C.push(H2("5.5 RQ5 — Validity gates"));
C.push(P("Table 7 reports the gate audit with TF-IDF, and Table 8 the preregistered tests of whether G0 lift predicts mean transfer."));
C.push(tcap("Table 7.", "Gate audit with TF-IDF (k = 8). Mean transfer T is accuracy averaged over admissible targets."));
C.push(table(["Training corpus", "n", "G0 lift", "κ_CV", "G0", "Levels with ≥ 30 items", "Mean transfer T"], [
  ["SCAR-I", "2,550", "+70.9 pp", "0.85", "PASS", "6", "46.1%"],
  ["YAHYA", "599", "+58.8 pp", "0.71", "PASS", "6", "50.4%"],
  ["SCAR-E", "1,839", "+57.7 pp", "0.76", "PASS", "6", "42.1%"],
  ["MOHOM", "126", "+40.5 pp", "0.55", "PASS", "0", "33.6%"],
  ["SANGO", "413", "+23.7 pp", "0.40", "PASS", "6", "36.1%"],
  ["GANI", "1,185", "+13.0 pp", "0.39", "CAUTION", "6", "27.1%"],
  ["EDUB", "2,550", "+0.04 pp", "0.23", "FAIL", "6", "29.3%"],
  ["EDUQG", "903", "0.0 pp", "0.02", "FAIL", "3", "17.2%"]],
  [1.6, 0.8, 1.0, 0.8, 1.0, 1.4, 1.4]));
C.push(gap());
C.push(tcap("Table 8.", "Does G0 lift predict transfer? Exact one-sided permutation tests of Spearman ρ."));
C.push(table(["Hypothesis", "Model class", "k", "ρ", "Exact p", "Status"], [
  ["H11a", "TF-IDF", "8", "0.93", "0.0011", "Supported"],
  ["H11b", "Word embeddings", "8", "0.69", "0.035", "Supported"],
  ["H9a", "DistilBERT", "5", "0.70", "0.117", "Failed"],
  ["H9c", "RoBERTa", "5", "0.60", "0.175", "Failed"],
  ["H12a", "DistilBERT", "8", "0.83", "0.0077", "Supported"],
  ["H12b", "RoBERTa", "8", "0.93", "0.0008", "Supported"]],
  [1.4, 1.8, 0.5, 0.7, 1.0, 1.8]));
C.push(gap());
C.push(img("fig4_g0_vs_transfer", 600));
C.push(caption("Figure 6.", "G0 lift versus mean transfer accuracy, eight corpora per panel. Top row: TF-IDF, and the transformers under the preregistered Phase 73 protocol (3 epochs). Bottom row: word embeddings, and the transformers under the preregistered Phase 76 protocol (at least 300 optimisation steps per fit). Circles: PASS; squares: CAUTION; crosses: FAIL. Asterisks mark corpora on which more than 95% of out-of-fold predictions fell in one class (training collapse). Panels have different y-axis ranges."));
C.push(P("Figure 6 plots these associations. The TF-IDF result held on skill over each target's majority rate (ρ = 0.95, p = 0.0006) and with SCAR-I removed (ρ = 0.93, p = 0.0034). The embedding result did not hold on either check (p = 0.16 and 0.083; exploratory). The earlier five-corpus test (H7: ρ = 1.0, p = 0.0083) is superseded by H11a. At k = 5, the pooled human-authored corpus transferred best under the transformers (mean 58–59%) despite only the third-highest G0 lift, which defeated the ranking test (H9a, H9c). At k = 8, with the four human-authored corpora separated, both transformer tests were supported (H12a, H12b)."));
C.push(P("**Training collapse on small corpora.** Under both transformers, SANGO (413 items) and MOHOM (126 items) failed G0 because fine-tuning collapsed: 98–100% of out-of-fold predictions fell in a single class, with about 21 and 7 optimisation steps per epoch under the fixed settings. Both corpora pass G0 under TF-IDF. Collapse lowers G0 and transfer together, so it contributes to the k = 8 association; excluding the two collapsed corpora left the association intact (ρ = 0.94, exact p = 0.0083 for both models; exploratory). G0 computed with TF-IDF as a fixed reference model did not significantly predict transformer transfer (ρ = 0.62, p = 0.057; exploratory). Section 5.6 reports a preregistered rerun with more optimisation steps."));
C.push(P("**Gate decisions agree only partly across model classes.** Decisions were identical under TF-IDF, embeddings, DistilBERT and RoBERTa for all five Phase 65 corpora (H8b, H9b and H9d supported; confirmatory). At k = 8, TF-IDF and embeddings agreed on 7 of 8 corpora (SANGO sat at the PASS/CAUTION boundary), but the transformers agreed with TF-IDF on only 5 of 8: SANGO and MOHOM moved from PASS to FAIL through collapse, and GANI from CAUTION to PASS (descriptive). Each PASS corpus transferred better than each FAIL corpus in every supervised model class, narrowly under embeddings (26.7% vs 26.0%); for the transformers this was preregistered as H12c and held for both models. With more optimisation steps (Section 5.6), the transformers agreed with TF-IDF on 7 of 8 corpora."));
C.push(P("**Each gate caught a distinct failure.**"));
C.push(B("**G0** failed EDUB and EDUQG."));
C.push(B("**G0b** caught MOHOM, which passed G0 but has fewer than 30 items at every level."));
C.push(B("**G1** caught SCAR-I, the most recoverable corpus of all: its generator labels agreed with the two experts at κ = 0.638 and 0.725, against expert–expert κ = 0.864 (provenance ratio 0.79). Recoverability therefore cannot detect consistent-but-invalid labels."));
C.push(B("**G2** caught every supervised model on learner questions: no TF-IDF or fine-tuned model showed a multiplicity-corrected advantage over the constant."));
C.push(B("**G4** caught every certification attempt."));
C.push(P("**Correcting labels did not improve transfer (confirmatory; H5 and H6 failed).** Training on expert rather than generator labels for the same 1,839 texts changed accuracy on DASQ by +0.04 points (95% CI −1.7 to +1.8), although the two label sources disagreed on 22% of items. Keeping only items where generator and experts agreed did no better than an equally sized random subset (+0.2 points, CI −0.9 to +1.3). Confident-learning pruning reduced accuracy (−4.6 points, CI −6.0 to −3.3; exploratory)."));
C.push(tcap("Table 9.", "Zero-shot LLM accuracy and skill over each target's majority rate (exploratory). DASQ and SCAR-E are 500-item random samples."));
C.push(table(["Target", "n", "Accuracy", "Majority rate", "Skill (95% CI)"], [
  ["SCAR-E", "500", "80.6%", "22.2%", "+58.4 pp (+52.8 to +63.6)"],
  ["DASQ", "500", "69.8%", "39.2%", "+30.6 pp (+24.2 to +36.8)"],
  ["YouLeQD 70", "70", "48.6%", "37.1%", "+11.4 pp (−2.9 to +25.0), video-cluster"],
  ["EDUQG", "903", "69.0%", "73.1%", "**−4.1 pp (−6.3 to −1.9)**"],
  ["LAK40 (set membership)", "40", "72.5%", "—", "—"]],
  [1.8, 0.7, 1.1, 1.2, 2.8]));
C.push(gap());
C.push(P("Table 9 shows that EDUQG, which fails G0 under every supervised model class, also remained below its majority rate for the zero-shot LLM."));
C.push(H2("5.6 Training-protocol robustness (Phase 76; preregistered)"));
C.push(P("Phase 73 used one fixed fine-tuning protocol (3 epochs, batch 16), under which training collapsed on the two smallest corpora (Section 5.5). Phase 76 retrained both transformers on all eight corpora, changing only the number of epochs so that every fit had at least 300 optimisation steps (Section 4.6). The preregistered hypotheses were: R1, collapse resolved on SANGO and MOHOM (most frequent out-of-fold class below 80% of predictions); R2, neither corpus FAIL; R3, ρ(G0, T) > 0 at k = 8. Table 10 compares the two protocols; Phase 73 results are retained unchanged."));
C.push(tcap("Table 10.", "Phase 73 (3 epochs) versus Phase 76 (at least 300 optimisation steps), by training corpus. Each cell gives DistilBERT / RoBERTa. Epochs: Phase 76 cross-validation fits (Phase 73 used 3 for every corpus). Top class: share of out-of-fold predictions in the most frequent class. Gap: Phase 76 training accuracy minus out-of-fold accuracy."));
C.push(table(["Corpus", "Epochs", "Top class P73", "Top class P76", "OOF acc. P73", "OOF acc. P76", "G0 decision", "T P73", "T P76", "Gap P76"], [["EDUB", "3", "20% / 25%", "20% / 25%", "0.41 / 0.40", "0.41 / 0.40", "FAIL → FAIL", "0.32 / 0.31", "0.32 / 0.31", "0.07 / 0.06"], ["YAHYA", "10", "22% / 23%", "17% / 19%", "0.62 / 0.71", "0.83 / 0.81", "PASS → PASS", "0.48 / 0.56", "0.61 / 0.57", "0.16 / 0.19"], ["SANGO", "15", "99% / 100%", "36% / 34%", "0.33 / 0.32", "0.75 / 0.74", "FAIL → PASS", "0.31 / 0.30", "0.48 / 0.55", "0.25 / 0.26"], ["MOHOM", "43", "98% / 100%", "29% / 24%", "0.25 / 0.23", "0.71 / 0.74", "FAIL → PASS", "0.09 / 0.09", "0.35 / 0.41", "0.29 / 0.26"], ["GANI", "5", "67% / 63%", "62% / 59%", "0.80 / 0.83", "0.86 / 0.86", "PASS → PASS", "0.41 / 0.47", "0.45 / 0.53", "0.09 / 0.09"], ["SCAR-I", "3", "18% / 18%", "18% / 18%", "0.89 / 0.89", "0.89 / 0.89", "PASS → PASS", "0.53 / 0.57", "0.53 / 0.57", "0.04 / 0.04"], ["SCAR-E", "4", "24% / 23%", "24% / 24%", "0.84 / 0.84", "0.84 / 0.83", "PASS → PASS", "0.55 / 0.59", "0.55 / 0.59", "0.07 / 0.10"], ["EDUQG", "7", "100% / 100%", "82% / 81%", "0.73 / 0.73", "0.73 / 0.73", "FAIL → FAIL", "0.16 / 0.16", "0.22 / 0.22", "0.16 / 0.19"]], [1.05, 0.85, 1.0, 1.0, 1.0, 1.0, 1.2, 0.95, 0.95, 0.95]));
C.push(gap());
C.push(B("**All three hypotheses were supported for both models.** The most frequent class fell to 34–36% of predictions on SANGO and 24–29% on MOHOM (R1); both corpora moved from FAIL to PASS (R2); and G0 predicted transfer (DistilBERT ρ = 0.86, exact p = 0.005; RoBERTa ρ = 0.83, p = 0.008; R3)."));
C.push(B("**The change is attributable to training length.** On EDUB and SCAR-I, whose configuration did not change, Phase 76 reproduced Phase 73 item for item, so the pipeline was deterministic in this environment. On SANGO and MOHOM, out-of-fold accuracy rose by 42 to 51 percentage points (paired bootstrap 95% CIs excluding zero) and mean transfer by 18 to 32 points."));
C.push(B("**Gate decisions agreed with TF-IDF on 7 of 8 corpora** for both transformers, against 5 of 8 in Phase 73; only GANI differed (TF-IDF CAUTION, transformers PASS)."));
C.push(B("**Training–validation gaps were substantial.** Training accuracy reached 1.00 on SANGO and MOHOM (and on YAHYA for RoBERTa), with gaps of 0.16–0.29 on the smaller corpora. Out-of-fold accuracy and transfer nevertheless improved relative to Phase 73. The models memorised their training data; whether a shorter schedule would generalise as well or better was not tested, and these results do not show that overfitting was absent or harmless."));
C.push(B("**EDUQG**, which was not part of R1, also collapsed under Phase 73 (100% of predictions in one class) and remained near-collapsed under Phase 76 (81–82%, close to its 73% majority rate); it fails G0 under every model class."));
C.push(P("On learner questions, SANGO-trained models scored lower under Phase 76 (17 of 70) than under Phase 73 (23 and 26 of 70), because the collapsed Phase 73 models had predicted the YouLeQD majority class for 58–67 of the 70 questions. No Phase 76 model had a multiplicity-corrected advantage over the constant, and the LLM remained indistinguishable from the four Scaria-trained models (descriptive)."));
C.push(P("Phase 76 therefore shows that the Phase 73 FAIL decisions for SANGO and MOHOM were attributable to insufficient optimisation under the original fixed protocol. It is evidence of training-protocol sensitivity for these two architectures and these two protocols. It does not show that any particular budget is sufficient in general, and it provides no independent evidence about the validity of SANGO's or MOHOM's labels, for which no expert labels exist."));
C.push(H2("5.7 Size, class balance and training-free diagnostics (exploratory)"));
C.push(P("Because G0 is computed with a trained model, its association with transfer could reflect corpus size, class imbalance or trainability rather than label recoverability. Table 11 reports exploratory checks (Phase 75, extended with Phase 76 values). Partial correlations use the Freedman–Lane permutation procedure (Freedman & Lane, 1983), enumerated exactly over all 8! permutations. An earlier implementation that permuted residuals directly was anti-conservative and has been replaced. In simulations calibrated to this setting (k = 8, ranked variables; 3,000 data sets per scenario), Freedman–Lane kept close to its nominal 5% level when the covariate was unrelated to G0 or to transfer (4.5–5.3%), but was liberal (7.4–10.1%) when the covariate was both strongly collinear with G0 and related to transfer. That is the situation for class balance, so partial p-values involving class balance (†) are descriptive."));
C.push(tcap("Table 11.", "Exploratory robustness of the G0–transfer association (Spearman ρ, exact one-sided permutation p; k = 8). Columns give the model class whose mean transfer T is predicted; P73 and P76 denote the two transformer training protocols. † Freedman–Lane is liberal in this configuration (see text); these p-values are descriptive."));
C.push(table(["Diagnostic or control", "TF-IDF", "Embeddings", "DistilBERT P73", "DistilBERT P76", "RoBERTa P73", "RoBERTa P76"], [["G0 with the model's own class (preregistered: H11a, H11b, H12a, H12b, R3)", "0.93 (p .001)", "0.69 (p .035)", "0.83 (p .008)", "0.86 (p .005)", "0.93 (p < .001)", "0.83 (p .008)"], ["Partial, controlling for log corpus size", "0.93 (p .002)", "0.70 (p .042)", "0.81 (p .016)", "0.86 (p .008)", "0.89 (p .003)", "0.83 (p .012)"], ["Partial, controlling for majority-class share †", "0.56 (p .043)", "0.39 (p .205)", "0.73 (p .014)", "0.69 (p .033)", "0.89 (p .004)", "0.65 (p .044)"], ["Partial, controlling for both †", "0.43 (p .201)", "0.35 (p .246)", "0.67 (p .074)", "0.67 (p .080)", "0.81 (p .028)", "0.69 (p .058)"], ["TF-IDF G0 at a common size (n = 126)", "0.69 (p .035)", "0.52 (p .098)", "0.33 (p .214)", "0.60 (p .066)", "0.33 (p .214)", "0.62 (p .057)"], ["First-word lookup lift (no model training)", "0.88 (p .004)", "0.76 (p .018)", "0.57 (p .076)", "0.83 (p .008)", "0.57 (p .076)", "0.81 (p .011)"], ["TF-IDF G0 as a fixed reference model", "—", "—", "0.62 (p .057)", "0.86 (p .005)", "0.62 (p .057)", "0.83 (p .008)"]], [1.95, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2]));
C.push(gap());
C.push(B("**Corpus size does not explain the association.** Size was nearly unrelated to G0 and to transfer (|ρ| ≤ 0.12), the setting in which the procedure is valid, and controlling for it left the association in place in every model class (unadjusted p = 0.002–0.042). After Holm adjustment across the 12 partial tests for TF-IDF, embeddings and the Phase 76 transformers, only TF-IDF remained below 0.05 (adjusted p = 0.022)."));
C.push(B("**G0 cannot be separated from class balance.** G0 and the majority-class share were strongly collinear for TF-IDF, embeddings and the Phase 76 transformers (ρ = −0.90 to −0.93). With both covariates controlled, no association under these protocols was significant (p = 0.058–0.25). Under the Phase 73 protocol, RoBERTa's partial association remained (p = 0.028), but that configuration included collapsed corpora, and the test is liberal there. We therefore do not claim that G0 predicts transfer independently of class balance."));
C.push(B("**Training-free diagnostics predict transformer transfer once collapse is removed.** With the Phase 73 transformers, neither TF-IDF G0 (ρ = 0.62, p = 0.057), a size-matched TF-IDF G0 (ρ = 0.33) nor a first-word lookup that involves no model training (ρ = 0.57) predicted transformer transfer significantly. With the Phase 76 transformers, TF-IDF G0 (ρ = 0.86 and 0.83, p ≤ 0.008) and the first-word lookup (ρ = 0.83 and 0.81, p ≤ 0.011) did, and the size-matched G0 was borderline (p = 0.057 and 0.066). The earlier negative finding was therefore affected by training collapse."));
C.push(P("Against skill over each target's majority rate, the Phase 76 association held for DistilBERT (ρ = 0.83, p = 0.008) but not for RoBERTa (ρ = 0.62, p = 0.057)."));

module.exports = { C };
