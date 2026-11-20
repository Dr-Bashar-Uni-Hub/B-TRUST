# Phase 42 DistilBERT checkpoint — verification (2026-11-19)
Supplied by the researcher from Google Drive (Bloom_Research/Phase42_DistilBERT_Checkpoint). Not redistributed here.
model.safetensors sha256: fbf2804e8f22fb8b7b5bafe91271f2729b88a20eacdba6e3b0783587eef62cc4 (267,844,872 bytes).
Run with a pure-NumPy forward pass (code/np_distilbert.py; PyTorch could not be installed in the sandbox).

| Check | Result |
|---|---|
| YouLeQD 300 predictions vs frozen Phase 42 | 300/300 identical; confidence diff median 1.0e-4, max 5.3e-4 |
| Internal 1,500 predictions vs frozen | 1,498/1,500 identical; both mismatches are L5/L6 near-ties (top-2 margins 3.2e-5 and 2.6e-4; median margin 0.178) |
| Internal accuracy | 50.73% here vs 50.87% frozen (the 2 near-tie flips) |
Interpretation: this is the checkpoint that produced the frozen predictions; the tiny differences fit GPU mixed-precision inference.
Full probability vectors: outputs/p71_distilbert_youleqd_proba.csv, outputs/p71_distilbert_internal_proba.csv.

Hyperparameters recovered from training_args.bin (pickle opcodes parsed without PyTorch; only cleanly parsed values listed):
num_train_epochs 2; learning_rate 2e-5; per_device_train_batch_size 16; per_device_eval_batch_size 32; seed 42; weight_decay 0.01;
lr_scheduler_type linear; warmup_ratio 0.0; warmup_steps 0; gradient_accumulation_steps 1; eval_strategy no; max_steps -1;
output_dir /content/phase42/distilbert. fp16/bf16 and other boolean/None fields could not be read reliably.
label_mapping.json: classes L1–L6, seed 42, source EduBloom, base model distilbert/distilbert-base-uncased.
Still missing: the script that drew the balanced 250-per-level internal test and trained the frozen LR.
