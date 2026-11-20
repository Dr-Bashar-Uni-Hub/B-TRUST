# Confirmatory annotation study — feasibility review (2026-11-20)

**Scope:** protocol development only. No data collection, no annotation and no API calls are authorised.

**Recommendation:** replace protocol v1's 650 questions and 4 annotators with **design B′**:

- **about 500 relevant questions and 3 annotators**;
- **two primary hypotheses** (C1 vote loss, C2 consolidated-label accuracy), Holm-adjusted;
- **C3** (fine-tuned model) demoted to secondary.

It cuts the cost by about a quarter (about 41 versus 57 person-hours) and keeps 82% power for the hardest test under a pessimistic effect.

## 1. Why the sample size matters here

The key open question is C2: H10 was supported on vote loss but not on consolidated-label accuracy (34/70 vs 26/70, p = 0.17). A confirmatory study that cannot test C2 adequately would not resolve the main weakness.

**Inputs** (from Phase 70 item-level data): paired vote-loss SD 0.366, effect −0.148; McNemar discordant pairs 17 vs 9 of 70 (d = 0.114, discordant proportion ψ = 0.371).

**Shrinkage scenarios:**
- C1 at half the observed effect;
- C2 with d reduced by 25% and ψ unchanged (conservative).

| Design | Relevant n | Primary tests | C1, observed | C1, half | C2, observed | C2, −25% |
|---|---|---|---|---|---|---|
| A: protocol v1 | 650 | C1–C3 (α/3) | 1.00 | 1.00 | 0.99 | 0.89 |
| **B′: recommended** | **~500** | **C1, C2 (α/2)** | 1.00 | 0.99 | 0.98 | **0.82** |
| B | 450 | C1, C2 (α/2) | 1.00 | 0.98 | 0.96 | 0.77 |
| C | 400 | C1, C2 (α/2) | 1.00 | 0.96 | 0.94 | 0.72 |
| D | 380 | C2 only | 1.00 | 0.98 | 0.96 | 0.79 |
| E | 250 | C1 only | 1.00 | 0.89 | 0.85 | 0.61 |

Values are normal-approximation power (Connor's method for McNemar), computed directly for every row; n = 490 gives 0.81 and n = 500 gives 0.82 for C2 at −25%. Protocol v1 stated "about 85%" for this case; the conservative calculation gives 0.89, so v1 understated its own power.

**Smallest defensible design: B′ (about 500 relevant questions).**
- **Below about 400**, C2 power under a modest shrinkage falls under 0.75.
- **Design E (250)** cannot address the open C2 question and is **not recommended**.
- **Design D** is the smallest option if C2 alone is primary, but it drops the vote-loss replication of H10.

**Why three annotators suffice.** The vote-loss SD above was estimated from three-annotator data, so the power for C1 already assumes three. A fourth annotator mainly improves κ precision (about ±0.05 vs ±0.036 at n = 500). That is a descriptive aim (CQ3), not a confirmatory one.

## 2. Workload (person-hours)

Assumptions: about 10 s per item for Stage 1 screening, about 30 s per item for Stage 2 coding, 3 h of training and calibration per person, and 10% re-coding.

| Design | Screened | Stage 1 (2 screeners) | Stage 2 | Training | Re-code | Total |
|---|---|---|---|---|---|---|
| A (650, 4 coders) | ~2,790 | 15 h | 22 h | 18 h | 2 h | ~57 h |
| **B′ (500, 3 coders)** | **~2,140** | **12 h** | **13 h** | **15 h** | **1 h** | **~41 h** |
| B′ with a single screener + 20% double screening | ~2,140 | ~7 h | 13 h | 12 h | 1 h | ~33 h |

**Option: single screener plus 20% double screening.** It cuts Stage 1 time but risks missing relevant items. Use it only if the double-screened subset shows κ ≥ 0.80 for relevance; report that κ and the estimated miss rate.

**Calendar time.** With part-time annotators (about 5 h/week each), about 3–4 weeks of coding after ethics approval and training.

## 3. How questions are collected and screened

**Collection:** no new collection is needed. The frame already exists:

- `stage1_sampling_frame.csv`: 5,146 learner questions from 1,309 YouTube lecture videos in the public YouLeQD repository (YesNLP/QYTL);
- it excludes every video and comment of the 300-item set already used;
- at most 5 questions per video, in a fixed random order (seed 70).

No scraping and no contact with commenters is involved.

**Stage 1 (relevance):**
- screeners work through the frame in its fixed order and stop when the target count of relevant items is reached (about 2,140 rows for B′);
- any prefix of a random order is a random sample, so stopping early introduces no selection bias.

**Stage 2 (Bloom coding):**
- three independent, blinded annotators per relevant item;
- original Bloom codes with revised names recorded, plus an optional second choice and confidence;
- no adjudication for primary analyses.

**Clustering:** about 1.3 relevant questions per video is expected. All inference uses video-cluster bootstrap.

**Model-assisted pre-screening is not recommended.** Using the relevance classifier to enrich Stage 1 would make the sample depend on a model and require inverse-probability weighting. It is mentioned only as a fallback if screening capacity becomes the bottleneck.

## 4. Ethics and data protection (to confirm with the university)

- **Ethics approval:** apply to Siirt University's research ethics committee responsible for non-interventional research (confirm the correct board and application form). Approval or a formal exemption must be documented before annotation starts, and its reference number cited in the article.
- **Personal data:** YouTube comments can contain personal data, so processing must comply with Türkiye's personal data protection law (KVKK, Law No. 6698).
  - Store no usernames, channel identifiers or profile data. The frame holds comment and video IDs and text only.
  - Mask any personal names appearing in comment text before annotation.
  - Release only item IDs and labels.
- **Data rights:** the source repository has no licence file. Request written permission from the YouLeQD authors before publishing any comment text or derived labels.
- **Annotators:** informed consent (their codes and agreement statistics will be analysed and reported in aggregate), fair compensation, and the right to withdraw.

## 5. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Relevance rate lower than 23.3% | Frame holds ~1,200 expected relevant; B′ needs ~500, leaving a 2.4× margin |
| Low inter-annotator agreement | Calibration threshold (κ ≥ 0.60) before coding; codebook decision rules; κ is reported regardless |
| LLM pretraining exposure to the public frame text | The labels are new and unpublished; disclose that the texts are public |
| C3 depends on retraining (no Phase 73 weights) | Phase 76 now saves full-fit weights; if approved, the C3 model can be frozen from a saved checkpoint |

## 6. Decision needed (after Phase 76)

Whether the confirmatory study is essential depends on the target journal and on how strongly the paper claims the LLM result:

- **If the LLM learner-question result stays a secondary, explicitly provisional finding**, the article can be submitted with the study described as future work.
- **If it is to be a headline claim**, design B′ should be run first.
