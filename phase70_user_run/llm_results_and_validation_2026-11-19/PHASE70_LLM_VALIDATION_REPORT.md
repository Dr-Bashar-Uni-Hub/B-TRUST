# Phase 70 LLM evaluation — scientific validation report

**Recommendation: ACCEPT WITH CORRECTIONS.** (Updated 2026-11-19 with the researcher's answers on cache consistency; see Section 9.) Every reported number reproduces exactly from the item-level file and the original vote data, and H10 survives all defensible alternatives tried. Corrections are needed in how the result is documented and described: protocol deviations, the scope of the H10 claim, the EduQG result, and transformer comparability. No paid API rerun is needed, unless the cached predictions turn out to come from runs with different settings (correction C1).

Validated 2026-11-19 from `p70_llm.csv` (sha256 `23caaba5…`), `p70_llm_detailed.csv` (`66e56155…`) and `p70_llm_abstentions.csv` (`488e9ed8…`). Scripts: `v1_consistency.py` to `v4_skill.py`; full log in `validation_log.txt`.

## 1. Verification of reported results — verified

| Dataset | n | Valid | Abstentions | Accuracy (abstention = wrong) | Accuracy among valid | Reported |
| --- | --- | --- | --- | --- | --- | --- |
| DASQ (500 sample) | 500 | 499 | 1 | 69.80% | 69.94% | 69.80% |
| SCAR-E (500 sample) | 500 | 500 | 0 | 80.60% | 80.60% | 80.60% |
| EduQG | 903 | 903 | 0 | 68.99% | 68.99% | 68.99% |
| YouLeQD 70 | 70 | 70 | 0 | 48.57% | 48.57% | 48.57% |
| LAK 40 (set membership) | 40 | 40 | 0 | 72.50% | 72.50% | 72.50% |

- **Metrics:** all accuracies, coverage and abstention counts recompute exactly; the stored `correct` column agrees with recomputation on every row. Reported accuracy counts the abstention as wrong, the conservative choice.
- **Cross-file consistency:** the single abstention is the same item in the detailed and abstention files.
- **Sampling:** the 500 DASQ and 500 SCAR-E items are exactly those drawn by the preregistered code (`default_rng(70)`, DASQ draw first). Texts and labels match 100%; EduQG, YouLeQD and LAK are complete and in order.
- **Label mapping:** consistent. Original names map to 1–6 in revised order (evaluation 5, synthesis 6), matching the revised labels of SCAR-E, EduQG and LAK (Evaluate 5, Create 6).
- **Duplicates:** 21 rows are 8 repeated questions (7 in EduQG, 1 in SCAR-E) with identical text and identical labels; reusing the cached answer is correct. The 2,000 unique questions equal the reported cache size.
- **Leakage:** none in the train–test sense, because the model is zero-shot. Pretraining contamination cannot be excluded (Section 6).

## 2. Validation of H10 — verified, with a scope limit

**Exact reproduction.** From the item predictions and the original YouLeQD vote matrix, H10 reproduces to six decimals: Claude vote loss 0.590476, constant 0.738095, difference −0.147619, 95% video-cluster CI −0.232456 to −0.064815, matching the reported values.

**Best constant.** Comprehension is the best constant under both vote treatments: 0.738 with irrelevant votes as loss (runner-up Analysis, 0.786) and 0.679 with Bloom votes only (runner-up Knowledge, 0.719).

**Missing votes.** No votes are missing. All 43 non-Bloom votes on the 70 items are explicit "irrelevant" codes (31 items have none, 35 have one, 4 have two). Because an irrelevant vote penalises every predictor equally, it cancels in any paired difference, so its treatment cannot drive H10.

| Variant | Difference | 95% CI | H10 holds |
| --- | --- | --- | --- |
| Preregistered: irrelevant vote = loss, video-cluster bootstrap | −0.148 | −0.233 to −0.065 | Yes |
| Same, item-level bootstrap | −0.148 | −0.233 to −0.067 | Yes |
| Bloom votes only, video-cluster | −0.164 | −0.267 to −0.057 | Yes |
| Bloom votes only, item-level | −0.164 | −0.269 to −0.062 | Yes |
| Bootstrap seeds 1, 2, 3 | −0.148 | upper bounds −0.062 to −0.064 | Yes |
| **Consolidated-label accuracy, 34/70 vs 26/70** | −0.114 | −0.250 to +0.029 | **No** (McNemar 17 vs 9, p = 0.17) |
| Exploratory: G3 granularity vs best constant | −0.067 | −0.154 to +0.015 | No |
| Exploratory: G2 granularity vs best constant | −0.076 | −0.162 to 0.000 | No |

**Scope of the claim.** H10 is supported as preregistered, on six-level vote loss. The advantage over the constant relies on agreement with all three annotators. On the single consolidated label, and at coarser granularities, it is not statistically established on 70 items.

**Exploratory.** Claude's vote loss (0.590) is below the human leave-one-annotator-out reference (0.686): difference −0.095, CI −0.165 to −0.015. This does not show better-than-human judgement. A predictor can match the modal annotator, which no single annotator can do by construction, so it should be reported only as agreement with the annotator majority.

## 3. Comparison with other models

**Paired comparisons on YouLeQD 70** (identical items, item-level predictions available):

| Comparator | Comparator vote loss | Claude minus comparator | 95% CI | Bonferroni 98.75% CI | Accuracy McNemar (Claude-only vs comparator-only) | Holm p |
| --- | --- | --- | --- | --- | --- | --- |
| Frozen EduBloom LR | 0.752 | −0.162 | −0.243 to −0.078 | −0.266 to −0.055 | 19 vs 8 | 0.21 |
| Frozen EduBloom DistilBERT | 0.748 | −0.157 | −0.253 to −0.064 | −0.277 to −0.035 | 22 vs 14 | 0.51 |
| Constant comprehension | 0.738 | −0.148 | −0.233 to −0.065 | −0.255 to −0.039 | 17 vs 9 | 0.51 |
| DASQBT TF-IDF LR (Phase 60) | 0.724 | −0.133 | −0.221 to −0.044 | −0.244 to −0.019 | 17 vs 9 | 0.51 |

Claude has significantly lower vote loss than every comparator, including after Bonferroni correction. No accuracy difference survives Holm correction.

**Phase 70 transformers: descriptive only.** No paired test is possible, for four reasons:

1. The transformer runs saved no item-level predictions.
2. On DASQ and SCAR-E, Claude was scored on 500-item samples, while transformers were scored on full corpora with leakage exclusions.
3. Conditions differ: zero-shot versus supervised fine-tuning, with each transformer trained on a different corpus.
4. Only YouLeQD 70 and LAK 40 used identical items.

| | Claude | Best DistilBERT | Best RoBERTa |
| --- | --- | --- | --- |
| YouLeQD 70 (correct) | 34 | 31 (SCAR-I) | 33 (SCAR-E) |
| LAK 40 (correct) | 29 | 28 (DASQ) | 29 (DASQ) |
| SCAR-E | 80.6% (500 sample) | 72.5% (DASQ-trained, full) | 74.5% (DASQ-trained, full) |
| DASQ | 69.8% (500 sample) | 57.9% (SCAR-E-trained) | 62.1% (SCAR-E-trained) |
| EduQG | 69.0% | 69.4% (SCAR-E-trained) | 66.4% (SCAR-E-trained) |

No statistical claim of Claude over transformers can be made from these. Phase 73 saves item-level transformer predictions, which will allow paired YouLeQD comparisons.

## 4. Abstentions and data quality

- **The one abstention is a format failure, not uncertainty.** The item is DASQ "State in one word ...", whose text is truncated in the source dataset; reference Comprehension. The model answered "Knowledge" and then explained that the question appeared cut off, which the one-word parser rejected.
- **It changes no accuracy.** A lenient first-word parser would also score it wrong (Knowledge ≠ Comprehension), so DASQ accuracy is 69.8% under either rule. No labels were changed.
- **Prediction distributions are plausible** on DASQ, SCAR-E and YouLeQD. Claude never predicted Synthesis on YouLeQD, where no consolidated label is Synthesis.

## 5. Skill over each dataset's majority rate

| Dataset | Accuracy | Majority rate | Skill | 95% CI |
| --- | --- | --- | --- | --- |
| SCAR-E | 80.6% | 22.2% | +58.4 pp | +52.8 to +63.6 |
| DASQ | 69.8% | 39.2% | +30.6 pp | +24.2 to +36.8 |
| YouLeQD 70 | 48.6% | 37.1% | +11.4 pp | −2.9 to +25.0 (video-cluster) |
| **EduQG** | 69.0% | 73.1% | **−4.1 pp** | **−6.3 to −1.9** |

**EduQG is a negative result that the summary file hides.** Claude is significantly worse than always predicting Remember. Of 660 Remember items it labels 72 as Comprehension or higher; it labels only 20 of 110 Apply items correctly, calling 57 of them Remember. This matches EduQG failing the framework's G0 gate: its publisher labels are not recoverable from text by any model class tested, now including a zero-shot LLM.

## 6. Methodological problems and required corrections

| # | Problem | Severity | Required correction |
| --- | --- | --- | --- |
| C1 | **Protocol deviations from the preregistered H10 setup.** The run used `max_tokens=128` and a `thinking_mode` setting, versus `max_tokens=5`. Predictions were cached across several runs (1,712 new in the final run; 2,000 total). Temperature and prompt text are not recorded in the outputs. | Moderate | Document every change to the notebook. Confirm the prompt text, temperature and thinking setting, and that all cached predictions came from runs with identical settings. If any cached subset used different settings, rerunning those items is a demonstrated methodological necessity (≤ 288 calls). |
| C2 | **H10 scope.** Support rests on six-level vote loss. Consolidated-label accuracy (p = 0.17) and coarse granularities are not significant. | Moderate | State H10 as "lower vote loss than the best constant on 70 items", and report the non-significant accuracy test beside it. |
| C3 | **EduQG below majority** is not visible in the summary file. | Moderate | Report skill over majority for every dataset. |
| C4 | **Transformer comparison** is unpaired, on non-identical samples, under different conditions. | Moderate | Present it as descriptive only; use Phase 73 item-level predictions for paired tests. |
| C5 | **Pretraining contamination.** YouLeQD labels have been public on GitHub, and DASQ sources since 2012–2023, SCAR-E since 2024, EduQG since 2022. A pretrained LLM may have seen them. | Moderate, untestable here | State as a limitation. The clean test is the unpublished confirmatory learner-question set. |
| C6 | **Single model, single prompt.** No prompt-sensitivity or second-LLM check. | Minor | State as a limitation. |
| C7 | **The "below human" observation** could be misread as better-than-human judgement. | Minor | Report only as agreement with the annotator majority. |

**Additional point not in the original audit brief:** pretraining contamination (C5). It is the main threat to interpreting any zero-shot LLM result on public benchmarks, and it is why the confirmatory set matters more for the LLM than for the trained models.

## 7. What Phase 70 adds to B-TRUST

**Supported:**

- On authentic learner questions, a zero-shot LLM agrees with the three annotators significantly better than the best constant and than every trained model with item-level predictions (vote loss). This is the first model in the project with a statistically supported advantage over the constant on YouLeQD, on the preregistered metric.
- It achieves high accuracy on human-authored exam questions (DASQ 69.8%) and on expert-validated generated questions (SCAR-E 80.6%), well above each majority rate.
- It fails on EduQG, the corpus that fails the label-recoverability gate under every model class.

**How it strengthens the manuscript.** The EduQG result extends the framework's main pattern to a fifth model class: corpora that fail G0 stay hard even for a strong zero-shot model. The YouLeQD result shows that the learner-question gap (G2) is not universal across model classes. But with n = 70, one prompt, and possible contamination, the paper should present it as a promising preregistered result requiring confirmation, not as a solved problem.

**Not supported:**

- Claude outperforms fine-tuned transformers: no paired test possible.
- Claude exceeds human annotators.
- Claude is accurate on learner questions in absolute terms: 48.6%, accuracy CI against majority includes zero.
- Any claim at three or two levels.

**Publication risks:** contamination (C5); undocumented protocol changes (C1); over-reading 70 items; the framework's predictive claim for strong models still rests on Phase 73.

## 8. Draft manuscript text (not inserted into the manuscript, pending approval)

**Results.** A zero-shot LLM (claude-sonnet-5-5) was evaluated on all targets without training. On the 70 learner questions, its six-level vote loss was 0.590, against 0.738 for the best constant classifier (Comprehension): a difference of −0.148 (95% video-cluster bootstrap CI −0.233 to −0.065), supporting the preregistered hypothesis. The result held when irrelevant votes were excluded and under item-level resampling. Its vote loss was also lower than that of every trained model with item-level predictions (Bonferroni-corrected CIs excluding zero). On the consolidated single label, its accuracy (34/70 vs 26/70) did not differ significantly from the constant (exact McNemar p = 0.17), nor at three- or two-level granularity. Accuracy exceeded the majority rate on human-authored exam questions (69.8% vs 39.2%) and on expert-validated generated questions (80.6% vs 22.2%), but fell below it on EduQG (69.0% vs 73.1%; difference −4.1 pp, 95% CI −6.3 to −1.9).

**Discussion.** The LLM result extends the framework's central pattern to a fifth model class. EduQG, which fails the label-recoverability gate under every model class, remained below its majority rate even for a strong zero-shot model. Conversely, the LLM was the only model whose agreement with learner-question annotators exceeded a constant baseline on the preregistered metric. This suggests that the learner-question gap reflects the training data available to supervised models rather than an absolute limit. Because the advantage rests on agreement with all three annotators, and was not significant on the consolidated label, it should be confirmed on a larger, unpublished learner-question set.

**Limitations.** The LLM was evaluated with one model and one prompt, on 70 learner questions. Because all benchmark datasets have been publicly available, pretraining contamination cannot be ruled out. The evaluation settings differed from the preregistered configuration (longer output limit, model reasoning setting, cached predictions across runs). Comparisons with fine-tuned transformers are descriptive, because they used non-identical samples and lacked item-level predictions.

## 9. Follow-up on correction C1 (2026-11-19)

**Researcher's account.** According to the Colab execution history, all saved predictions used `claude-sonnet-5-5`, the original Bloom prompt,
`max_tokens=128` and `thinking={"type":"between_tools"}`. Temperature was not specified. Earlier debugging runs used other settings but were not
intentionally included in the final checkpoint. The 287 cached predictions were recovered and the evaluation continued with the same configuration.
The checkpoint does not store request metadata.

**Checkpoint-key check (`v5_checkpoint_key.py`).** The `question_hash` key could not be reconstructed: none of 1,378 plausible constructions match
(five hash functions over question text, prompt plus text, model and settings prefixes, dataset prefixes, JSON request dictionaries). The data do show
that identical texts always share one key and one prediction (8 groups), and that the one stored raw response is multi-sentence, which fits
`max_tokens=128` (a 5-token limit would have truncated it). Whether the key encodes the configuration needs the notebook cell that builds it.

**Conclusion.** No concrete evidence of a configuration mismatch was found, so the ≤ 288 cached items were not rerun, as instructed. Configuration
consistency rests on the execution history and is stated as such; it is not independently proven.

**Additional deviation identified: temperature.** The preregistered setting was temperature 0; the run used the API default. Predictions are
therefore stochastic and a rerun would not reproduce them item-for-item. H10 remains a valid test of this single run of this configuration, but
run-to-run variability is unknown. Estimating it would require new paid calls and is not proposed without approval.

**Effect on conclusions.** None of the verified numbers change. C1 now covers four documented deviations (output limit, reasoning setting,
cached multi-run assembly, default temperature) plus unverifiable cache configuration. The Limitations text in Section 8 is amended accordingly:
"... (longer output limit, model reasoning setting, default sampling temperature instead of 0, and predictions assembled from cached runs whose
configuration is documented by execution history but not stored with the predictions)."
