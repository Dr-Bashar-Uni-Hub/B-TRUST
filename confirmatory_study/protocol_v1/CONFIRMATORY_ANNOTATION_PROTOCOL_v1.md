# B-TRUST confirmatory learner-question study — proposed protocol v1 (2026-11-19)

**Status: PROPOSED. Not started.** No data collection, API calls or analyses before the author's approval. The final analysis plan must be preregistered, with its SHA-256 recorded, before Stage 2 coding ends.

## 1. Why a new study is needed, and whether existing data suffice

The learner-question evidence rests on YouLeQD 70: 70 questions from one platform, coded by three annotators who agreed unanimously on 9. It has been used across many phases, and its source is public, so pretraining contamination cannot be excluded.

**Existing independently annotated data were assessed and cannot replace a new learner-question set:**

| Candidate | Independent annotation? | Learner questions? | Verdict |
|---|---|---|---|
| YouLeQD remaining 230 of 300 | Same three annotators | Yes, but consolidated as irrelevant | Already used; not usable for Bloom-level tests |
| LAK40 (Xu et al., 2026; A1, A2, ground truth) | Yes (2 annotators + ground truth) | No (learning objectives); n = 40 | Usable only as a small secondary reference |
| Li et al. (2022) learning objectives | One annotator + 30% second | No | Different population; public availability not verified |
| Scaria et al. (2024) expert labels | Yes (2 blinded experts) | No (LLM-generated questions) | Already used (SCAR-E) |
| Ravikiran et al. (2026) MCQs with educator Bloom labels (noted in an earlier phase; not downloaded) | Educator annotation | No (exam MCQs) | Could add a ninth training/target corpus for the gate analyses; cannot address learner questions |

**Conclusion:** existing data can extend the corpus-level gate analyses but cannot provide an unpublished, independently coded learner-question test set. The protocol below is required for the confirmatory claims.

## 2. Research questions

- **CQ1.** On unpublished learner questions, does a zero-shot LLM agree with independent annotators better than a fixed constant classifier, on six-level vote loss and on the consolidated label?
- **CQ2.** Does a prespecified fine-tuned model do so?
- **CQ3.** What is the human ceiling (inter-annotator agreement) at six, three and two levels on this population?
- **CQ4.** Is certification of a selective policy feasible at this sample size? (Exploratory.)

## 3. Confirmatory hypotheses (Holm-adjusted across C1–C3, family-wise α = 0.05)

| ID | Hypothesis | Metric | Test |
|---|---|---|---|
| C1 | LLM six-level vote loss < constant | Mean per-item vote loss difference | Video-cluster bootstrap (10,000), two-sided 95% CI and bootstrap p |
| C2 | LLM consolidated-label accuracy > constant | Accuracy on items with a consolidated label | Exact McNemar, two-sided |
| C3 | Prespecified fine-tuned model six-level vote loss < constant | As C1 | As C1 |

- **Constant:** Comprehension, fixed a priori (the best constant on YouLeQD 70). It is not re-chosen on the new data, so there is no optimism in the baseline.
- **LLM:** the model, prompt and parser are fixed in the preregistration.
  - Recommended: the same original-Bloom one-word prompt; first-valid-label-word parsing; temperature 0 with no reasoning setting, matching the Phase 70 preregistration rather than its deviations.
  - The Phase 70 configuration is run as a sensitivity analysis.
  - Requires paid API calls and therefore separate approval.
- **Fine-tuned model:** RoBERTa trained on SCAR-E with the Phase 73 configuration (lowest Phase 73 vote loss among RoBERTa models). It is retrained and its predictions frozen, with a hash, before any Stage 2 label is seen. No transformer weights were saved in Phase 73.

## 4. Sampling

- **Frame:** `stage1_sampling_frame.csv` (sha256 `643e3b6d…`): 5,146 learner questions from 1,309 YouTube lecture videos in the YouLeQD source repository. It excludes every video and comment of the existing 300-item set, has at most 5 questions per video, and is in a fixed random order (seed 70).
- **Stage 1** (relevance screening) proceeds in frame order until **650 relevant questions** are reached. Expected to need about 2,800 rows at the observed 23.3% relevance rate. Any prefix of the frame is a random sample.
- **Clusters:** videos. All inference uses video-cluster resampling.

## 5. Sample-size justification (computed from Phase 70 item-level data)

| Target | Assumption | Required relevant items |
|---|---|---|
| C2, McNemar accuracy | Observed effect 0.114 (17 vs 9 discordant of 70), α = 0.05/3, power 0.9 | 380 |
| C2, McNemar accuracy | Effect shrunk by 25% (0.086), power 0.8 | 527 |
| C1/C3, vote loss | Half the observed effect (−0.074), paired SD 0.366, α = 0.05/3, power 0.9 | 333 |
| C1/C3, vote loss | Effect −0.050, power 0.8 | 562 |
| CQ3, Fleiss κ precision | 4 raters | n = 500: ±0.036; n = 700: ±0.030 (approximate 95% half-width) |

**Chosen n = 650 relevant items.** That gives about 85% power for C2 under a 25% shrunken effect, and over 90% for C1 at half the observed effect. The design effect is small: about 1.3 relevant questions per video, so DEFF is about 1.06 at ICC 0.2.

## 6. Annotators and qualifications

- **Stage 1:** two annotators per question plus an adjudicator for disagreements. Codes: relevant, irrelevant, unsure.
- **Stage 2:** four annotators per relevant question, for vote loss and κ precision. Each must:
  - have a degree in education or the relevant subject, or teaching experience;
  - complete Bloom codebook training;
  - pass a 60-item calibration set drawn outside the frame, reaching Cohen's κ ≥ 0.60 against the training key.
- Annotators are paid by time, not by item.

## 7. Independence and blinding

- **Annotators do not see:** model outputs, other annotators' codes, the video, the subject label, comment metadata or votes.
- **Order:** each annotator receives an independently randomised order.
- **No discussion** between annotators during coding.
- **No adjudication for primary analyses:** the raw votes are the data. The consolidated label is the strict plurality of the four votes (at least 2, no tie). Tied items are labelled ambiguous; they are excluded from C2 but kept in C1/C3.

## 8. Taxonomy

- **Primary codes:** original Bloom (Knowledge … Evaluation, Synthesis), matching YouLeQD and H10. Revised names are recorded alongside.
- **Alignment:** the manuscript's name-based alignment (synthesis ↔ Create at position 6, evaluation ↔ Evaluate at 5). It is stated as provisional because the two taxonomies order these levels differently.
- **Per question:** annotators code the cognitive process the *answerer* must perform, not the asker's verbs (codebook decision rules from the v2.1 archive). They also record an optional second choice and a confidence of 1–3.

## 9. Irrelevant, ambiguous and multi-label questions

- **Irrelevant:** may still be coded in Stage 2. Treated as a non-matching vote in vote loss, exactly as in H10; Bloom-only-vote analyses are a sensitivity check.
- **Ambiguous:** an "unsure" flag plus a second choice. Primary analyses use first choices; a sensitivity analysis excludes items where at least 2 annotators were unsure.
- **Multi-label:** not allowed as a primary code (one best level). Second choices support adjacent-level and set-based secondary analyses.

## 10. Agreement and uncertainty

All with video-cluster bootstrap 95% CIs:

- Fleiss' κ;
- Krippendorff's α, nominal and ordinal;
- pairwise Cohen's κ;
- exact and adjacent agreement;
- leave-one-annotator-out vote loss (human reference) at six, three and two levels.

Intra-rater reliability: 10% of items are re-coded after at least two weeks.

## 11. Analysis plan

- **Primary:** C1–C3 as in Section 3, Holm-adjusted.
- **Secondary (Holm within family, labelled secondary):**
  - three- and two-level vote loss for the LLM and the fine-tuned model versus a constant fixed a priori (Lower-order / LOTS);
  - Bloom-only-vote sensitivity;
  - the Phase 70-configuration LLM.
- **Exploratory:** a certification attempt (G4) with a 50/50 video split; G2 for all Phase 73 models; LAK40 secondary reference.
- **Missing data:** an item missing any Stage 2 code is excluded from κ but kept in vote loss with the available votes; the missingness rate is reported.

## 12. Data quality

- 5% of items duplicated, to measure consistency.
- Time per item recorded; responses under 3 s are flagged.
- Straight-lining detection.
- Weekly drift checks against the calibration set.
- Every exclusion rule fixed before unblinding.

## 13. Ethics and data rights

- Ethics approval or a formal exemption from the Siirt University ethics committee before any annotation.
- Comments are public YouTube text: no usernames or identifiers are stored or released; releases contain item IDs and labels only.
- The source repository (YesNLP/QYTL) has no licence file, so written permission is required before publishing any comment text.
- Annotator informed consent and fair compensation.

## 14. Limitations (anticipated)

- One platform (YouTube lecture comments) and English only.
- The relevance definition shapes the population.
- Original taxonomy alignment is provisional.
- The LLM may still have seen the public source repository, although the new labels are unpublished.
- Four annotators cannot represent all expert populations.

## 15. Effort estimate (for planning only)

| Stage | Volume | Assumed time | Total |
|---|---|---|---|
| Stage 1 screening | ~2,800 rows × 2 annotators | ~10 s/item | ~16 h |
| Stage 2 coding | 650 items × 4 annotators | ~30 s/item | ~22 h |
| Training and calibration | — | — | ~3 h per annotator |
| Re-coding | — | — | ~2 h per annotator |

## 16. Approval gates

1. Author approves this protocol.
2. Ethics approval.
3. Annotator recruitment and calibration.
4. Stage 1.
5. Preregistration of the final analysis plan (hash) and freezing of model predictions (hash), before Stage 2 ends.
6. Approval of paid API calls for C1/C2.
7. Analysis.
