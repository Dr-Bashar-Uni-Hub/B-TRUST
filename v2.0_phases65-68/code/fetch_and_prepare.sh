#!/bin/sh
# Rebuilds the inputs for Phases 65-68 from pinned public commits. No third-party text is redistributed in this archive.
set -e
git clone -q https://github.com/YesNLP/QYTL.git && (cd QYTL && git checkout -q 42a67bc82c01d6e656b83393ee2a4041c12976ee) && cp -r QYTL/data/DASQBT ./DASQBT
git clone -q https://github.com/nicyscaria/AEQG_Blooms_Evaluation_LLMs.git && (cd AEQG_Blooms_Evaluation_LLMs && git checkout -q 0cd206967209b62ac200df9dcd73eb4e8763347e)
git clone -q https://github.com/hadifar/question-generation.git && (cd question-generation && git checkout -q d253fe84a7fe6401768504ef6ab9eea36359107b)
python3 prepare_pickles.py
