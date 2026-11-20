# Confirmatory study — annotation protocol and codebook (draft for preregistration)
Sampling frame: `stage1_sampling_frame.csv` (sha256 643e3b6d…), 5,146 learner questions from 1,309 YouTube lecture videos in
YesNLP/QYTL (commit 42a67bc8). Excludes all 236 videos and 300 comments of the existing YouLeQD human set. At most 5 questions
per video; rows are in a fixed random order (seed 70).

## Stage 1 — relevance screening
- Annotate rows strictly in `order`. Stop after the row at which the running count of RELEVANT items (Stage 1 consensus) reaches 1,100,
  or at the end of the frame. Any prefix of the frame is a random sample, so the stop rule does not bias the sample.
- Two independent annotators per item, blind to each other and to any model output. Disagreements → a third annotator.
- RELEVANT = the question asks about the subject matter of the lecture (a concept, procedure, problem, claim or application).
  IRRELEVANT = about the video, presenter, audio, course logistics, personal circumstances, spam, or not answerable as subject matter.
- Record time per item and an "unsure" flag.

## Stage 2 — Bloom coding (relevant items only)
- Three independent annotators per item (four if budget allows), trained on this codebook and a 60-item calibration set drawn
  from OUTSIDE the frame. Annotators never see each other's codes, model outputs, the video, or the subject label.
- Code the cognitive process the question asks the ANSWERER to perform, not the verbs the asker happens to use.
- Taxonomy: original Bloom (to match DASQBT and the existing YouLeQD labels), with revised names recorded alongside.

| Code | Original / revised | The question asks the answerer to … | Typical learner-question examples (paraphrased) |
|---|---|---|---|
| 1 | Knowledge / Remember | recall a fact, term, definition, formula | "what is the unit of …", "what does X stand for" |
| 2 | Comprehension / Understand | explain, interpret, give meaning or cause | "why does X happen", "what does this step mean" |
| 3 | Application / Apply | carry out a procedure in a given case | "how would I solve this with …", "does this work for …" |
| 4 | Analysis / Analyze | break down, compare, relate parts | "what is the difference between X and Y" |
| 5 | Evaluation / Evaluate | judge against criteria, justify a choice | "is X a better approach than Y", "is this claim valid" |
| 6 | Synthesis / Create | design, propose or generate something new | "how could we build/design a …" |

Decision rules:
1. If a question contains several sub-questions, code the highest level that the answer genuinely requires.
2. "Why" questions default to Comprehension unless they require weighing alternatives (Evaluation).
3. Yes/no questions are coded by what a correct justification would require.
4. Record a second-choice code (optional) and a confidence (1–3); these support adjacent-level analysis.

## Quality control
- Report pairwise and Fleiss' κ for Stage 1 and Stage 2, exact and adjacent agreement, by subject.
- Re-code a random 10% after two weeks to estimate intra-rater reliability.
- Annotators are paid by time, not by item.

## Analysis (to be preregistered before Stage 2 coding finishes)
- Split by VIDEO into calibration and test halves (seed fixed in the preregistration). Models are trained only on external corpora;
  the relevance model is trained on the existing 300-comment YouLeQD set.
- Gates G2 (skill over constant, by granularity), G3 (leave-one-annotator-out vote loss), G4 (video-level LTT certification as in
  Phase 63, with the power plan of Phase 62) — code in the v1.1 and v2.0 archives.
- One primary hypothesis, chosen before unblinding; recommended: "the best G0-passing model has lower G2 vote loss than the
  best constant at G3 granularity on the test half (video-cluster bootstrap, 95% CI)".

## Data rights
The QYTL repository has no licence file. Obtain permission from its authors before annotation results containing comment text are
published; release only IDs and labels otherwise.
