Run from the corpora directory (loaders use relative paths), with the Phase 73 outputs available for comparison:
  python3 v76_validate.py      -> v76_recomputed.csv (verification, R1–R3)
  python3 v76_compare.py       -> v76_vs_p73.csv (paired comparison with Phase 73, gate agreement, fixed-reference G0)
  python3 v76_exploratory.py   -> v76_youleqd_paired.csv (Phase 75 diagnostics vs P76 transfer, skill over majority, YouLeQD paired tests)
v76_freedman_lane.csv was produced inline with the Freedman–Lane procedure from phase75_method_review/p75_review.py, using Phase 76 G0 and T.
Model weights (16 fp16 full-fit checkpoints) are on the author's Google Drive (BTRUST_p76_out/models/full); not part of this archive.
