# QC addendum — manuscript v0.3 (2026-11-19)

## Numbers check

`qc_numbers.py` now runs **93 checks**: the 69 from v0.2, plus 24 for Phase 73. **All 93 pass** at strict tolerance.

- The three v0.2 rounding corrections (H1 +6.8; SCAR-E 57.7; H10 −0.232) are now encoded in the script.
- One new rounding issue was caught before entering the manuscript: the reference-model p is 0.057, not 0.058.

## Claims changed by Phase 73

| Claim | v0.2 | v0.3 |
|---|---|---|
| Transformer ranking | Not significant (k = 5); H12 pending | Supported at k = 8 (H12a ρ 0.83, p 0.008; H12b ρ 0.93, p < 0.001), partly driven by collapse; holds at k = 6 without collapsed corpora |
| Gate decisions across model classes | "Agreed across model classes" | Agreed at k = 5 (confirmatory) and 7/8 for TF-IDF vs embeddings; transformers agree only 5/8 at k = 8 |
| Learner questions, fine-tuned models | "No item-level predictions; descriptive" | 16 paired tests; none survives Holm against the constant |
| LLM vs fine-tuned models | Descriptive only | LLM lower than 12/16, but not distinguishable from the four best; no superiority claim |
| Phase 70 RoBERTa 33/70 | Unconfirmed observation | 30/70 on rerun; within run-to-run variation |

## Declarations (author-supplied, 2026-11-19)

- **Funding:** none.
- **Competing interests:** none; the Anthropic disclosure is kept as transparency.
- **Authorship:** sole author, with all CRediT roles except Supervision and Funding acquisition.
- **Generative AI:** the declaration uses singular "author".
- **Still needed:** the author's name, affiliation and ORCID, and confirmation of the AI declaration wording.

## Consistency

- **Abstract ↔ Results ↔ Conclusion:** rechecked against v0.3; the Abstract numbers are covered by the QC script.
- **"Pending":** the only remaining uses refer to the confirmatory annotation study.
