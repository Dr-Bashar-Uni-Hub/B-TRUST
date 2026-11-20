# Phase 73 validation report (2026-11-19)

**Recommendation: ACCEPT, with interpretive qualifications.** Every reported value recomputes exactly from the per-question files, and both preregistered ranking tests are supported. However, training collapse on the two smallest corpora contributes to the transformer association and changes those corpora's gate decisions.

Input: `p73_outputs.zip` (sha256 `77a9c604…`), 51 files, run by the researcher on a Tesla T4 (torch 2.14.1+cu130, transformers 4.46.3) using notebook v2 (`9f3e3a49…`), which has no LLM section.

## 1. Verification (`v73_validate.py`)

- **Integrity:** all 16 gate files, 16 out-of-fold files and 16 per-question files are present. Item keys and label order match each corpus exactly.
- **Targets and leakage:** excluded targets (self; SCAR-I/SCAR-E) are absent, test sets match the leakage rule, and no test item appears in its training corpus.
- **Recomputation:** CV accuracy, G0 lift, κ, gate decision and mean transfer T recompute to within 1e-9 of the reported values for all 16 model–corpus pairs.
- **Tests:** Spearman ρ and exact p recompute exactly.

## 2. Preregistered tests

| Hypothesis | Result | Status |
|---|---|---|
| H12a DistilBERT, k = 8 | ρ = 0.833, exact p = 0.0077 | Supported |
| H12b RoBERTa, k = 8 | ρ = 0.934, exact p = 0.0008 | Supported |
| H12c PASS above FAIL in transfer | Holds for both models | Supported |

## 3. Qualification: training collapse (exploratory)

With fixed settings (3 epochs, batch 16), fine-tuning collapsed on SANGO (413 items, about 21 steps per epoch) and MOHOM (126 items, about 7). 98–100% of out-of-fold predictions fell in one class, and both MOHOM models scored 0/70 on YouLeQD. EDUQG also collapsed, but it fails G0 under every model class.

| Exploratory check | Result |
|---|---|
| Excluding SANGO and MOHOM (k = 6) | ρ = 0.943, exact p = 0.0083, both models |
| TF-IDF G0 as a fixed reference model, vs transformer transfer | ρ = 0.619, exact p = 0.0575 (not significant) |
| Gate decisions equal to TF-IDF | 5/8 for both models (SANGO and MOHOM PASS → FAIL; GANI CAUTION → PASS) |

**Interpretation:** G0 is model-relative. Under collapse, a FAIL reflects the model's trainability on a small corpus, not label validity.

## 4. Run-to-run reproducibility (Phase 70 vs Phase 73; same settings, four shared corpora)

G0 lift differed by less than 0.01. YouLeQD correct counts differed by up to 3 of 70 items; RoBERTa trained on SCAR-E scored 33 in Phase 70 and 30 in Phase 73.

## 5. Paired YouLeQD comparisons (descriptive; video-cluster bootstrap, 10,000 resamples, seed 73; Holm across 16)

- **Against the constant:**
  - three models have unadjusted intervals below zero: DistilBERT on SCAR-E (−0.090, CI −0.174 to −0.013); RoBERTa on SCAR-I (−0.086, CI −0.167 to −0.014); RoBERTa on SCAR-E (−0.086, CI −0.171 to −0.005);
  - none survives Holm (adjusted p 0.27–0.45);
  - both MOHOM-trained models are significantly worse (0/70).
- **Against the LLM:** the LLM has lower vote loss than 12 of 16 models, but is not distinguishable from the four Scaria-trained models (all intervals include zero).

## 6. Effect on the manuscript (v0.3)

| Location | Change |
|---|---|
| Table 8 | H12a/b supported (replaces pending row) |
| Figure 5 | Transformer panels now k = 8, collapsed corpora marked |
| Gate-agreement claim | Restricted to k = 5 and TF-IDF/embeddings; transformers agree 5/8 at k = 8 |
| §5.2 | Paired transformer results; no superiority claim either way |
| §6.2 | "Recoverability is model-relative", with a collapse-check recommendation (untested) |
| §7 | New "Fixed fine-tuning settings" limitation |
| Abstract and Conclusion | Updated to match |

## 7. Correction during validation

The reference-model p was first reported in chat as 0.058. The exact value is 0.05749, which rounds to **0.057**. The manuscript uses 0.057, and the QC check runs at strict tolerance.
