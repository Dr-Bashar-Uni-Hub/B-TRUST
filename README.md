# B-TRUST — research code and reproducibility materials

**Author:** Bashar ALHAJAHMAD, Siirt University, Türkiye. ORCID: 0009-0009-3455-7206.

**Study:** *When Bloom Labels Measure Difficulty: A Validity-First Evaluation of Automated Cognitive-Level Classification under Annotator Disagreement and Dataset Shift*.

This repository contains a **curated, publication-candidate subset** of the B-TRUST research archive v3.1 (20 November 2026), including experiment source code, runnable notebooks, preregistrations, method validation reports, summary tables, hashed-ID per-item predictions for Phases 73 and 76, and figure sources. It intentionally omits some third-party question text, human-annotation source files and nested ZIP archives. It is **not a complete standalone reconstruction of the private environment**.

> **Important:** The original v1.0 baseline archive (Phases 38–57), trained model checkpoints, third-party datasets and some private item-level LLM data are *not* part of the provided v3.1 upload package. Therefore a full end-to-end reconstruction of all manuscript claims from this repository alone is not yet possible. The researcher should provide lawful acquisition/reconstruction instructions and, where allowed, additional artifacts before claiming full open reproducibility.

## Navigation

- `v1.1_phases58-64/`: baseline continuation, original preregistrations, scripts, aggregate results.
- `v2.0_phases65-68/` and `v2.2_phase71_and_checkpoint/`: gate and cross-corpus analyses.
- `phase70_user_run/`: transformer and LLM experiment scripts, validations and permitted aggregate outputs.
- `phase73_v2_user_run/`: preregistered eight-corpus transformer experiment and hashed prediction outputs.
- `phase75_robustness_exploratory/`, `phase75_method_review/`, `freedman_lane_verification/`: exploratory analyses and corrected statistical checks.
- `phase76_ready_A1/`: pre-run amended steps-matched robustness notebook, results and validations.
- `v3.1_manuscript_v0.5/`: supporting manuscript generation, revision and QC materials where applicable (working manuscript PDFs and DOCX omitted).
- `framework_figure_v0.5/`: editable framework figure and source generator.
- `confirmatory_study/`: deferred protocol materials; the internal-only learner-question sampling frame is excluded.
- `RELEASE_FILES_SHA256.csv`: hashes for files actually included in this candidate package.
- `PUBLIC_RELEASE_REVIEW.md`: privacy, rights, verification and completeness checklist.

## Replication and rights

Review the README and scripts in each experiment folder. Public datasets should be fetched from their original sources with the appropriate permissions and versions. Do **not** redistribute third-party question/comment text without confirming permissions. Raw human-annotation files and the internal stage-one learner-question sampling frame are excluded from this release candidate. Paths and environment dependencies in old scripts may require configuration.

Results reported in the manuscript distinguish preregistered analysis (including Phase 73 and the subsequent Phase 76 robustness intervention) from exploratory findings. Phase 76 added training steps; original Phase 73 findings were retained. See `phase76_ready_A1/results_received_2026-11-20/validation/PHASE76_VALIDATION_AND_INTEGRATION_REPORT.md`.

## Status and citation

Release candidate for **private review**, not yet audited as a public reproducibility release. No open-source license has been assigned to the author's code in this package. A publication-ready manuscript and an archival DOI should be added after final review if the author chooses.
