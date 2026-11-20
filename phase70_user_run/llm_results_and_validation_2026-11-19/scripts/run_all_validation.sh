#!/bin/sh
# Phase 70 LLM validation. Needs: p70_llm*.csv, corpora.py + its inputs (see v2.x archive), the v1.0 archives (BTRUST_EX),
# p60_das_lr_model.joblib (v1.1 Phase 60; regenerate with phase60_e1.py) and the Phase 70 transformer CSVs.
python3 v1_consistency.py && python3 v2_h10.py && python3 v3_paired.py && python3 v4_skill.py
