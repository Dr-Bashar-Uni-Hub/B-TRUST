# Provenance resolutions (2026-11-19)

## 1. EduBloom (Kaggle metadata supplied by the researcher)
- Authors: Pushkar Sharma (owner), Uzaib Saiyad, Rajesh Sable (AI and Data Analytics students). DOI 10.34740/kaggle/dsv/19232466. Licence CC BY-SA 4.0.
- Source: "EduBloom project dataset, developed and organized by the EduBloom team for educational AI and Bloom's Taxonomy-based question generation research."
- Collection methodology (paraphrased): questions were systematically generated and organised across subjects and topics, then categorised by
  Bloom level (Remember … Create), question type and difficulty, and stored as CSV with IDs. No human or expert validation is described;
  the data card recommends such validation for real-world use.
- Level names: the card lists the revised taxonomy in order (Remember … Create); the CSV uses L1–L6, consistent with L5 = Evaluate, L6 = Create.
- Phase 72 (descriptive): L5 and L6 share 787 of ~793 stems (Jensen–Shannon distance 0.217 vs 0.50–1.00 for all other pairs); creation verbs
  occur in 4.9% of L6 and 4.6% of L5; stem pools are disjoint across difficulty bands (L1 vs L3–L6 distance 1.000). L6 is not textually
  distinguishable from L5, so the L5/L6 naming question is moot for any text classifier.

## 2. Phase 37 archive — VERIFIED
q_bt_human_label.csv (sha256 94eb0ec0…) and q_bt_human_label_raw.csv (sha256 67e3f66b…) are byte-identical to YesNLP/QYTL. The chain from the
public YouLeQD annotations to Phase 38 is complete. Notebook included.

## 3. Phase 42 generating script — CONFIRMED MISSING (not recoverable from supplied files)
The re-supplied Phase42_Input_Package.zip and Phase42_SelfContained notebook are byte-identical to the v1.0 copies; the notebook's embedded
payload contains the same run_phase42.py (sha256 prefix 7b9945ff64244e85). That script cannot have produced the frozen artifacts:
proportional 6,000-item sampling (frozen internal test is 250 per level); LR max_features=80000, sublinear_tf=True, max_iter=1500 (frozen LR:
50000, no sublinear TF, 2000); DistilBERT output_dir 'phase42_checkpoints', eval_strategy 'epoch' (checkpoint's training_args:
'/content/phase42/distilbert', 'no'). The second checkpoint ZIP is byte-identical to the first.
Consequence: frozen models are reproducible from saved weights (LR joblib, verified checkpoint), not from code.
