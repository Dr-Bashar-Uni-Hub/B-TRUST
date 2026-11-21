# Post-hoc verification scripts (Computers & Education submission, Supplementary Sections S7 and S9)

These scripts reproduce the duplicate audit, the repeated-text sensitivity analysis (Supplementary Table S8; manuscript Section 4.5)
and the independent re-runs of the disagreement-screening analysis (Supplementary Table S9; manuscript Section 4.6).
All three are exploratory, post-hoc analyses; none was preregistered.

## Requirements
- Python 3.12 with numpy, pandas, scipy and scikit-learn (versions used: see the repository's environment notes).
- `corpora.py` and `prepare_pickles.py` from the repository (`v2.0_phases65-68/code/`) in the working directory.
- Inputs, rebuilt rather than redistributed:
  - Faraji et al. (2026) CSVs (MIT): copy the four `*_revised.csv` files into the working directory.
  - Scaria et al. (2024) and EduQG: clone at the pinned commits (`nicyscaria/AEQG_Blooms_Evaluation_LLMs` @ 0cd20696…,
    `hadifar/question-generation` @ d253fe84…), then run `python3 prepare_pickles.py`.
  - EduBloom and YouLeQD (used by `corpora.py`): extract the frozen archive's phase archives and set `BTRUST_EX` to that folder.

## Run
    export BTRUST_EX=/path/to/extracted/phase_archives
    python3 duplicate_audit.py        # -> duplicate_audit.csv
    python3 dedup_sensitivity.py      # -> dedup_sensitivity.csv
    python3 screening_reproduction.py # -> screening_reproduction.csv

## Expected outputs
The files in `outputs/` were produced this way on 2026-11-21. `dedup_sensitivity.csv` and `screening_reproduction.csv` were regenerated
from a freshly rebuilt environment and are byte-identical to the versions used for the submitted Supplementary Material
(checksums in `outputs/SHA256SUMS.txt`).

## Key definitions
- **Repeated texts:** SCAR-I has 2,550 rows and 2,532 unique normalised texts (18 surplus copies); SCAR-E 1,839 and 1,825 (14);
  EDUQG 903 and 891 (12). Two repeated SCAR-I texts carry conflicting labels.
- **Deduplication rule (Table S8):** drop both copies of texts with conflicting labels, then keep one copy of each other repeated
  text. SCAR-I therefore has 2,530 rows after the rule (20 fewer: 18 surplus copies plus the 2 conflicting texts).
- **Screening re-runs (Table S9):** five stratified five-fold out-of-fold runs with fold-assignment seeds 0, 1, 2, 42 and 65,
  with and without class-balanced weighting. Text model: TF-IDF unigrams and bigrams (min_df = 2) with logistic regression.
  Length/format model: standardised character count, word count, question marks, commas and digit presence, with logistic regression.
- **Interpretation:** the 408 disagreements are differences between the generator's intended levels and the experts' consensus,
  not 408 objectively incorrect Bloom labels.

## What these files do NOT verify
- The author-run screening analysis (AUROC 0.751; 173 vs 82 disagreements; the conditional bootstrap intervals 18.9–30.7 points
  and 1.94–2.32) was produced by a separate notebook. Its code, saved out-of-fold scores and exact length/format features should be
  added to this folder by the author. The re-runs here reproduce its results closely but not identically.
- The author run's use of class-balanced weighting is inferred (it is the only setting that reproduces its Brier score of 0.186);
  the author's notebook should confirm it.
