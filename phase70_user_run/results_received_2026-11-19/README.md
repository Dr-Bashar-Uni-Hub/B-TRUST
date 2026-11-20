# Phase 70 results (run by the researcher in Colab; received 2026-11-19)
Four files received: p70_G0_{distilbert,roberta}.csv, p70_transfer_{distilbert,roberta}.csv (sha256 in p70_received_sha256.txt).
p70_llm.csv was NOT received, so H10 (LLM) is untested. Run date and notebook hash were not supplied; results are taken as produced by the
preregistered notebook (sha256 6fd8d2e6…) without independent verification.
Tests computed here from the files (p70_analysis.py -> p70_tests.csv):
- H9a DistilBERT rho(G0 lift, T) = 0.70, exact p = 0.117 -> FAILED.  H9b identical G0 decisions 5/5 -> SUPPORTED.
- H9c RoBERTa rho = 0.60, exact p = 0.175 -> FAILED.               H9d identical G0 decisions 5/5 -> SUPPORTED.
- Failure source: DASQ (human exam corpus) has the highest transfer (0.58–0.59) but only the third-highest G0 lift.
- Exploratory: every PASS corpus has higher transfer than every FAIL corpus under both transformers.
- Exploratory: RoBERTa/SCAR-E 33/70 on YouLeQD vs majority 26/70; no valid paired test possible (no item-level predictions); one of 10 comparisons.
