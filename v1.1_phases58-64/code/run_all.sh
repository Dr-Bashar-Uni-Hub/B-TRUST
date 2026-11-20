#!/bin/sh
# Run from code/. Needs ./DASQBT (see fetch_dasqbt.sh) and the v1.0 archives extracted so that
# /home/claude/bt/ex/<PhaseXX>/... exists (scripts use that path; edit EX/paths if you extract elsewhere).
export OPENBLAS_NUM_THREADS=4
python3 phase58_audit.py /home/claude/bt/ex
python3 phase60_e1.py && python3 phase61_e2.py && python3 phase62_e3.py && python3 phase63_e4.py && python3 phase63_diag.py && python3 phase64_recoverability.py
