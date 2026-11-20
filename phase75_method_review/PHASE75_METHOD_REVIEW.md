# Independent review of the Phase 75 conditional permutation analysis (2026-11-20)

**Verdict:** the partial-correlation tests in Phase 75 used an invalid permutation scheme, and their p-values were anti-conservative in all 12 cases. Corrected with the Freedman–Lane procedure, one claim in manuscript v0.4 no longer holds, and after multiplicity adjustment only 3 of 12 partial tests survive. The simple Spearman tests in Phase 75 (size-matched G0, first-word lookup) are unaffected.

**Per your instruction, the manuscript is not modified now.** The corrections below are queued for the post-Phase 76 revision.

## 1. The problem

The original code ranked G0 (x) and transfer (y), regressed both on the ranked covariates Z, and then permuted the y-residuals directly against the fixed x-residuals.

Permuted residuals are **not orthogonal to Z**. With k = 8 and 2–3 columns in Z, they leave the residual subspace, so the reference distribution is not the null distribution of the partial correlation. This is a known pitfall; Freedman and Lane (1983) proposed the standard remedy.

## 2. The correction

**Freedman–Lane** proceeds in four steps:

1. Fit the reduced model y ~ Z.
2. Permute its residuals and add back the fitted values to form y*.
3. Re-residualise y* on Z.
4. Recompute the partial correlation with the x-residuals.

This was evaluated exactly over all 8! = 40,320 permutations, with Holm adjustment across the 12 partial tests (4 model classes × 3 covariate sets). Script: `p75_review.py`; output: `p75_review_freedman_lane.csv`.

| Model class | Control | Partial ρ | p (original) | p (Freedman–Lane) | Holm (12) | Residual df |
|---|---|---|---|---|---|---|
| TF-IDF | log size | 0.93 | .001 | .002 | **.022** | 5 |
| TF-IDF | class balance | 0.56 | .028 | .043 | .25 | 5 |
| TF-IDF | both | 0.43 | .147 | .201 | .60 | 4 |
| Embeddings | log size | 0.70 | .029 | .042 | .25 | 5 |
| Embeddings | class balance | 0.39 | .173 | .205 | .60 | 5 |
| Embeddings | both | 0.35 | .196 | .246 | .60 | 4 |
| DistilBERT | log size | 0.81 | .009 | .016 | .13 | 5 |
| DistilBERT | class balance | 0.73 | .011 | .014 | .12 | 5 |
| DistilBERT | **both** | **0.67** | **.030** | **.074** | .30 | 4 |
| RoBERTa | log size | 0.89 | .002 | .003 | **.036** | 5 |
| RoBERTa | class balance | 0.89 | <.001 | .004 | **.039** | 5 |
| RoBERTa | both | 0.81 | .010 | .028 | .20 | 4 |

**Collinearity:** Spearman ρ between G0 and the majority-class share is −0.93 (TF-IDF), −0.90 (embeddings), −0.83 (DistilBERT) and −0.65 (RoBERTa). With residual df of 4–5, partial correlations among such collinear variables are unstable, and the tests have little power.

## 3. What can and cannot be concluded with eight corpora

**Supported (cautiously):**
- Corpus size does not appear to account for the association. All four unadjusted Freedman–Lane tests are below .05, and size is only weakly related to G0 for TF-IDF and embeddings (ρ 0.05, 0.12).

**Not supported:**
- Any claim that the association survives control for class balance, or for both covariates, in any specific model class.
- Any claim that DistilBERT's association survives both controls.
- Any multiplicity-robust claim beyond TF-IDF and RoBERTa controlling for size, and RoBERTa controlling for balance.

**Not identifiable at k = 8:**
- Whether G0 and class balance have separate associations with transfer. They are nearly the same ranking across these corpora.

**Recommended framing:** the conditional analyses are descriptive sensitivity checks. They show the result is not obviously an artefact of corpus size, and that it cannot be distinguished from class balance with eight corpora. More corpora would be needed to separate them.

## 4. Queued manuscript corrections (apply after Phase 76 is validated)

| Location (v0.4) | Current text | Correction |
|---|---|---|
| Table 10, partial-correlation rows | Original permutation p-values | Replace with Freedman–Lane p-values; add a Holm (12) column or note; add residual df |
| §5.6, bullet "Class balance is collinear…" | "…for the transformers they remained (ρ = 0.67 and 0.81)" | "…only RoBERTa's remained before multiplicity adjustment (ρ = 0.81, Freedman–Lane p = .028; Holm-adjusted p = .20); DistilBERT's did not (p = .074)" |
| §5.6, bullet "Corpus size does not explain…" | "left it intact in every model class" | Keep, adding: "unadjusted; after Holm adjustment across the 12 partial tests, TF-IDF and RoBERTa remain" |
| §5.6 intro and §7 limitation | "indicative only" | Add the collinearity (ρ up to −0.93) and the Freedman–Lane method; state that G0 and balance cannot be separated at k = 8 |
| Abstract | "it was not explained by corpus size, but for TF-IDF it could not be separated from class balance" | Still accurate; optionally add "in exploratory analyses with eight corpora" |
| References | — | Add Freedman, D., & Lane, D. (1983), *Journal of Business & Economic Statistics*, 1(4), 292–298. **Bibliographic details to be verified before insertion.** |

**Effect on conclusions:** the narrowed interpretation in v0.4 still holds: G0 is informative but model-relative, and partly reflects trainability. The one strengthening claim, that the transformer association survives both controls, is withdrawn for DistilBERT and weakened for RoBERTa.
