Exploratory and paired-comparison analyses in this folder were produced interactively; their logic is recorded here for re-execution:
- v73_exploratory.csv: k = 6 Spearman excluding SANGO and MOHOM; TF-IDF G0 (Phase 71) vs transformer T; gate agreement with TF-IDF.
- v73_reproducibility_p70_vs_p73.csv: G0 lift and YouLeQD counts for EDUB, SCAR-I, SCAR-E, EDUQG in Phases 70 and 73.
- v73_youleqd_paired.csv: 16 models vs constant and vs the Phase 70 LLM; six-level vote loss; video-cluster bootstrap (10,000, seed 73);
  bootstrap p = 2*min(P(diff>=0), P(diff<=0)); Holm across 16; exact McNemar vs constant.
All are also checked by v2.7_manuscript/qc/qc_numbers.py.
