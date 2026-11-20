#!/bin/sh
# Run from code/ after fetch_and_prepare.sh. Requires v1.0 archives extracted to /home/claude/bt/ex (see corpora.py EX).
export OPENBLAS_NUM_THREADS=4
python3 phase65_gates.py && python3 phase66_67.py && python3 phase68_predictive.py
# Phase 69 (needs: pip install spacy and en_core_web_lg 3.8.0 from github.com/explosion/spacy-models releases)
python3 phase69_embedding.py
