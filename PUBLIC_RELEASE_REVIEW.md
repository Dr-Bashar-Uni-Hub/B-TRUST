# Public release review — required before switching GitHub to public

This is a **curated upload candidate**, not a certification that every file is safe or independently reproducible.

## Already excluded

- `confirmatory_study/stage1_sampling_frame.csv`: 5,146 learner questions from a source without a documented reuse licence; internal annotation only.
- `v2.3_provenance/phase37_archive/q_bt_human_label*.csv`: raw text and annotator records.
- `v2.2_phase71_and_checkpoint/data_faraji_MIT/*.csv`: question text, withheld pending item-by-item rights review, even though the archive labels this subset MIT.
- `v2.2_phase71_and_checkpoint/outputs/p71_distilbert_internal_proba.csv`: contains a `question` column.
- `phase70_user_run/llm_results_and_validation_2026-11-19/received/p70_llm_detailed.csv` and `p70_llm_abstentions.csv`: contain original question text.
- Nested `p73_outputs.zip`, `p76_outputs.zip`, internal working manuscripts and temporary file artifacts.

## Verify manually before making public

1. Inspect all remaining `.py`, `.ipynb`, `.md`, `.jsonl`, `.csv`, `.sh`, `.txt`, `.js` for passwords, API credentials, user identifiers, original third-party text, computer-specific paths and sensitive metadata. No comprehensive security scan is implied.
2. Check model/output rights, dependencies and dataset licences; verify the SHA256 list for included release files.
3. If source data cannot be shared, document precisely how the permitted inputs can be obtained, reconstructed and independently validated; do not claim full reproducibility when the v1.0 archive or private records are required.
4. Add a `LICENSE` only after deciding on code and third-party permissions; absence of a licence means others have no broad reuse permission by default.
5. Confirm claims of preregistration using original full manuscripts/hashes/archived files, and correct outdated statuses in any legacy README under a phase folder.
6. Add a final accepted manuscript, versioned release and persistent DOI later, if appropriate. Verify each uploaded file and link before inserting the Code availability paragraph in a submitted manuscript.

## Entire filtered-out file inventory

The full omitted file list and reasons are in `EXCLUDED_FILES.csv`.
