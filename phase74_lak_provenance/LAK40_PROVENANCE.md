# LAK40 provenance (resolved 2026-11-19)
- Our LAK40 = rows with Annotator == "groundtruth" of `human_annotation/Bloom-All_40.csv` in github.com/AEQUITAS-Lab/Data-Annotation-LAK-2026
  (commit 91de3c386ecb48bf6047b6ecf80646e429d86aae; file sha256 e50005a101c3a6dbe7b36c50381bc0d5855fd0e50137148782b4b0c0868a9f8b).
  Verified: 40/40 learning outcomes match; identifiers and reference sets identical; 2 multi-label items ({Analyze, Create}; {Apply, Evaluate, Create}).
- Release: Xu, Khatri, Dai, Liu, Li, Zhang & Yu (2026). Enhancing LLM-based data annotation with error decomposition. LAK '26. arXiv:2601.11920.
- Parent dataset (inferred from an identical description in the release appendix A.1, which gives no citation): Li, Raković, Poh, Gašević & Chen (2022),
  EDM 2022, pp. 530–537, doi:10.5281/zenodo.6853191 — 21,380 learning objectives, 5,558 courses, Australian university; one trained annotator,
  second annotator on 30% (kappa 0.63 before, 0.80 after discussion).
- Discrepancy: appendix A.1.2 states that single-labelled objectives were sampled; Bloom-All_40 contains 2 multi-label ground-truth items. Preserved and disclosed.
- Taxonomy: revised (Remember … Create); scored by set membership; alignment with original-taxonomy predictions by name is provisional.
- Licence: the repository has no licence file; the file is not redistributed here.
- Human ceiling (descriptive, p74_log.txt): A1/A2 overlap with ground truth 80.0% / 87.5%; A1–A2 exact-set agreement 60.0%, kappa 0.58 (first labels).
