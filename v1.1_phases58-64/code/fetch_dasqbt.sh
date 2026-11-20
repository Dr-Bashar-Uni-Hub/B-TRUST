#!/bin/sh
# DASQBT is NOT redistributed (YesNLP/QYTL has no licence file). Fetch the exact version used in Phases 60-64:
git clone https://github.com/YesNLP/QYTL.git QYTL && (cd QYTL && git checkout 42a67bc82c01d6e656b83393ee2a4041c12976ee) && cp -r QYTL/data/DASQBT ./DASQBT
