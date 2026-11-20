# Scientific revision report — manuscript v0.3 → v0.4 (2026-11-20)

**Author:** Bashar ALHAJAHMAD (Siirt University), sole author.

**Status:** complete working draft, **not submission-ready**. Two pieces of evidence remain pending: the Phase 76 robustness experiment (awaiting approval) and the confirmatory annotation study (protocol proposed). All frozen baselines, preregistered results and archived outputs are unchanged.

## 1. What changed and why

| Area | Change | Effect on findings |
|---|---|---|
| Author information | Title page, corresponding author, ORCID, affiliation, Word metadata (creator, last modified by, description) | None |
| Framework figure | New **Figure 1** (§3.1): evidence-grouped checks, a model-relative G0, failures routed to investigation, and outputs. Supplied as editable SVG, vector PDF and the generating script. Existing Figures 1–5 renumbered 2–6, with all cross-references updated. | None (presentation) |
| Conceptual clarity | §3.4 now defines and separates label validity, label recoverability and model trainability, and states that the checks are not a strict sequence and that a FAIL triggers investigation | Interpretation narrowed |
| Number of checks | The Abstract and contributions said "five ordered gates"; there are **six** checks (G0, G0b, G1–G4), and they are not strictly ordered | Corrected (confirmed error) |
| New exploratory evidence | §5.6 and Table 10 (Phase 75; existing outputs only): partial correlations controlling for size and class balance, a size-matched G0, and a training-free first-word diagnostic | Qualifies the RQ5 claim (see §2) |
| Interpretation | §6.2: robustness interpretation added, no causal claim. §6.5: why a framework without a new algorithm is useful. §6.6: "should not be used for training" softened to "warrants investigation". New Table 11 separates findings, interpretations and recommendations. | Claims narrowed |
| Limitations | Added "Robustness analyses are exploratory and low-powered" | — |
| Conclusion and Appendix A | Updated for Phase 76 and the confirmatory study; Appendix A now has status and location for both | — |
| References | All 10 † entries verified against publisher, indexing or catalogue records, with DOIs added. Remaining notes: Sangodiah ‡ (citing sources); pages for Ming et al. and Xu et al.; Faraji et al. proceedings; EduBloom version year | None |
| Citation integrity | Scripted check: Hoeffding (1963) was listed but uncited, so a citation was added. Figure 6 was not cited in the text, so a citation was added. No in-text citation is missing from the list. | Corrected (confirmed) |
| Declarations | Single-author CRediT, funding and competing interests, all marked for confirmation. The generative AI declaration covers Claude's substantive roles, ChatGPT's known role, and Claude as an evaluated system. | — |

## 2. New robustness evidence (Phase 75, exploratory) and its effect

Computed from existing outputs plus cheap TF-IDF recomputation; no transformer training and no API calls. k = 8 corpora; exact permutation p-values.

1. **Corpus size does not explain the G0–transfer association.** It remained after controlling for log size in all four model classes (ρ 0.70–0.93, p ≤ 0.03).
2. **For TF-IDF, G0 is collinear with class balance.** Balance alone predicts TF-IDF transfer (ρ = 0.90). With size and balance both controlled, the TF-IDF and embedding associations lose significance (p = 0.15, 0.20); the transformer associations remain (ρ = 0.67, p = 0.030; ρ = 0.81, p = 0.010).
3. **No training-independent diagnostic predicts transformer transfer.** Size-matched TF-IDF G0 (n = 126) and a training-free first-word lookup predict TF-IDF transfer (ρ 0.69, 0.88) but not transformer transfer (ρ 0.33, 0.57; p > 0.05).
4. **Skill over the majority rate** gives the same transformer associations as raw transfer.

**Effect on conclusions.** The preregistered results (H11a/b, H12a/b) stand. Their interpretation is narrowed: recoverability as measured by G0 is informative but model-relative, partly reflects trainability for the transformers, and cannot be separated from class balance for TF-IDF at k = 8. No causal claim is made.

## 3. Is a new experiment justified?

**Yes, for one targeted question.** The collapse confound can be separated only by retraining small corpora long enough to avoid collapse.

The Phase 76 notebook (sha256 `68ae8b96…`) changes a single factor: epochs = max(3, ⌈300 / steps per epoch⌉). That gives SANGO 15/12 epochs and MOHOM 43/38 epochs (CV fit / full fit); every other setting is unchanged.

| Hypothesis | Criterion |
|---|---|
| R1 | Collapse resolved: top-class share < 80% on SANGO and MOHOM |
| R2 | SANGO and MOHOM are not FAIL |
| R3 | ρ > 0 at k = 8 |

The interpretation rules are fixed in advance. The notebook was dry-run with a stand-in model: the plumbing and the R1–R3 bookkeeping work, and the stand-in reproduces Phase 71 exactly. **Not run; requires the author's approval and a GPU session (about 3–4 h on a T4). No API calls.**

## 4. Scientific quality control

**Confirmed issues** (corrected in v0.4):

| # | Issue | Correction | Effect |
|---|---|---|---|
| Q1 | Six checks described as "five ordered gates" | Text corrected; Figure 1 shows the evidence grouping | Presentation only |
| Q2 | Hoeffding (1963) listed but uncited | Cited at first use (§4.2) | None |
| Q3 | Figure 6 not cited in the text | Cited in §5.5 | None |
| Q4 | Implication stated categorically ("should not be used for training") | Softened, with the reasons given | Claim narrowed |
| Q5 | 10 references flagged † | Verified; DOIs added | None |

**Numbers check:** `qc_numbers.py` now runs **107 checks** against archived outputs (v0.2: 69; Phase 73: 24; Phase 75: 14). All pass at strict tolerance.

**Potential concerns** (not errors; disclosed or listed for decision):

| # | Concern | Current handling |
|---|---|---|
| P1 | No family-wise correction across the ~13 preregistered hypotheses (H1–H12, H10) | Each was registered as its own primary test; a supplementary Holm table is recommended (checklist A7) |
| P2 | Transfer T averages heterogeneous targets | The skill-over-majority version gives the same conclusions for TF-IDF and the transformers; it is weaker for embeddings |
| P3 | YouLeQD 70 reused across many phases | Disclosed; the confirmatory protocol addresses it |
| P4 | G1 evaluated on one corpus only (Scaria) | Disclosed; more expert-labelled corpora needed |
| P5 | Pretraining contamination (LLM, pretrained encoders) | Disclosed; the unpublished confirmatory set is the clean test |
| P6 | Gate thresholds not externally calibrated | Disclosed (§3.4, §6.6, Figure 1); sensitivity analysis listed (A6) |
| P7 | Clustered observations | Video-cluster bootstrap throughout; mean 1.27 comments per video; simulation-validated video-level tests |
| P8 | Data licensing | Three sources lack licence files; no text redistributed; permissions pending |
| P9 | Cross-dataset comparability | Leakage rule and exclusions are verified item by item; samples differ only for the LLM's 500-item draws (disclosed) |
| P10 | Novelty | No algorithmic claim; the contribution is stated as operationalisation plus preregistered evidence (§6.5) |
| P11 | AI involvement | Claude was both a substantive assistant and an evaluated system; disclosed in Competing interests and the AI declaration |

## 5. Confirmatory annotation protocol (proposed; `CONFIRMATORY_ANNOTATION_PROTOCOL_v1.md`)

- **Existing data assessed:** none can provide unpublished, independently coded learner questions; LAK40, Li et al. (2022) and Scaria are different populations.
- **Design:** 650 relevant learner questions (about 2,800 screened) from the 5,146-question, 1,309-video frame.
- **Annotation:** four calibrated, blinded Stage 2 annotators per question.
- **Hypotheses:** C1 (LLM vote loss), C2 (LLM consolidated accuracy, McNemar) and C3 (prespecified fine-tuned model), Holm-adjusted.
- **Baseline:** a constant fixed a priori.
- **Power:**
  - C2: 85% for a 25%-shrunk effect;
  - C1: over 90% at half the observed effect;
  - κ precision: about ±0.04.
- **Not started.** It needs approval, ethics clearance, and separate approval for paid API calls.

## 6. Not yet resolved (blocks submission)

1. Phase 76 (approval, run, validation, integration).
2. The confirmatory study, or a decision to present it as future work.
3. Author confirmation of the CRediT roles (including Supervision), funding, competing interests and ChatGPT use.
4. Data permissions for YouLeQD/QYTL, EduQG and LAK '26.
5. A public code repository with a persistent identifier.
6. The remaining bibliographic details (pages for Ming et al. and Xu et al.; Faraji et al. proceedings; EduBloom year).
7. Target-journal selection after evaluation, with reformatting.
