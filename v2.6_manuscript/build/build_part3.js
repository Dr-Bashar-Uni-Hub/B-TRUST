// Part 3 — Discussion, Limitations, Conclusion, declarations, references, appendix; assemble document
const fs = require("fs");
const { D, C, P, H1, H2, B, table, tcap, gap, runs, FONT } = require("./build_part1.js");
require("./build_part2.js");
const { Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat, HeadingLevel, Footer, PageNumber, PageBreak } = D;

// ---------------- 6 Discussion ----------------
C.push(H1("6. Discussion"));
C.push(H2("6.1 What \"accuracy\" means for a Bloom classifier"));
C.push(P("The EduBloom case shows that a classifier can reach respectable within-dataset accuracy while measuring something other than cognitive level. A metadata-only rule matched a fine-tuned transformer because both were recovering difficulty bands. Nothing in the within-dataset numbers revealed this; it became visible only when the labels were checked against the text and against the metadata. A Bloom corpus therefore needs validity evidence about its labels before its models are evaluated, much as a test needs evidence for its scores before they are interpreted (Kane, 2013; Williamson et al., 2012). This matters most for generated corpora, which are cheap to produce at scale and may carry the generator's assignment rules rather than the construct."));
C.push(H2("6.2 Recoverability is a screen, not a ranking, and not validity"));
C.push(P("For TF-IDF models, how learnable a corpus's labels were predicted how well its models transferred across eight corpora. For word embeddings the association was weaker and sensitive to the metric, and for fine-tuned transformers on five corpora it did not reach significance. A pretrained model appears able to extract transferable signal from corpora whose labels are only moderately learnable for simpler models, which flattens the ranking among passing corpora. What held across every supervised model class was the pass/fail separation, although it was observed rather than preregistered and was narrow for embeddings. We therefore present G0 primarily as a screen, pending the eight-corpus transformer test (Phase 73)."));
C.push(P("Recoverability is also not validity. The LLM-generated labels were the most recoverable of all, yet agreed with experts less than experts agreed with each other. A generator that writes characteristic text for each intended level produces labels that are easy to learn and partly wrong. The provenance gate (G1) is needed to detect this, and it requires independent expert judgement on at least a sample."));
C.push(H2("6.3 Cleaning labels did not help transfer"));
C.push(P("Correcting a fifth of the labels, or filtering to items where generator and experts agreed, did not change transfer to human-authored exam questions, and a standard data-driven cleaning method made it worse. Within the range of label quality observed here (generator–expert κ about 0.64–0.72), transfer appears limited by the shift between item populations rather than by residual label error. Label invalidity was decisive only at the EduBloom extreme, where the text carried essentially no label signal."));
C.push(H2("6.4 Learner questions remain hard"));
C.push(P("No supervised model showed a statistically supported advantage over a constant on learner questions. The best fine-tuned transformers scored above the majority rate (31/70 and 33/70 vs 26/70), but without item-level predictions this could not be tested. The zero-shot LLM was the only model whose agreement with learner-question annotators exceeded the best constant on the preregistered metric, which is consistent with the cross-dataset stability of LLMs reported by Faraji et al. (2026)."));
C.push(P("The LLM result needs three qualifications. First, it rests on agreement with all three annotators, and accuracy on the consolidated label was not significantly better than the constant's. Second, it comes from one model, one prompt and one stochastic run on 70 questions, under settings that deviated from the preregistration. Third, every dataset used here is public, so pretraining exposure cannot be excluded. We regard it as a promising preregistered result that requires confirmation on unpublished data."));
C.push(H2("6.5 Relation to prior work and scope of the contribution"));
C.push(P("The framework is an operationalisation, not a new validity theory: its gates map onto categories of evidence already set out for automated scoring (Williamson et al., 2012) and onto established diagnostics for shortcut learning and annotation artifacts (Geirhos et al., 2020; Gururangan et al., 2018). The statistical machinery for abstention and certification is likewise existing work (Angelopoulos et al., 2025; Dunn et al., 2023; Goren et al., 2024). The contribution lies in quantified decision rules applied to training labels, in the demonstration on real corpora that each gate catches a distinct failure, and in preregistered evidence on when the recoverability gate predicts transfer and when it does not. Whether these results generalise beyond English-language Bloom corpora, the corpora sampled here, and question- and objective-style items is untested."));
C.push(H2("6.6 Implications"));
C.push(B("**Research using automated Bloom labels as variables** (for example, relating question level to engagement) should report the labelling model's agreement with human judgement on the target population, compared against a constant."));
C.push(B("**Item-bank tagging:** a corpus that fails G0 or G0b should not be used for training, whatever its size, and validated performance on exam-style items should not be assumed to carry over to learner-posed questions."));
C.push(B("**Selective classification:** certification on learner-question data will require hundreds of independent sources of accepted decisions; fewer cannot support a distribution-free guarantee, regardless of the method used."));

// ---------------- 7 Limitations ----------------
C.push(H1("7. Limitations and Threats to Validity"));
C.push(B("**Small learner-question target.** All learner-question results rest on 70 questions from one platform, coded by three annotators who agreed unanimously on only 9. This set was used across many analysis phases; confirmatory hypotheses were registered before their outcomes were seen, but repeated use limits independence. A larger, unpublished learner-question set is in preparation."));
C.push(B("**Few corpora for the gate tests.** The predictive tests use eight training corpora, two of which share texts. The transformer tests use five, where only a perfect ordering can reach significance. Gate thresholds were set a priori and are not calibrated against external criteria."));
C.push(B("**Phase 70 LLM evaluation.** One model, one prompt and a single run. The output limit (128 tokens instead of 5), an enabled reasoning setting and the default sampling temperature (instead of 0) deviated from the preregistration, so predictions are stochastic and run-to-run variability is unknown. Predictions were assembled from cached runs whose consistent configuration is documented by the researcher's execution history but not stored with the predictions. One item produced a parser failure and was scored as incorrect. DASQ and SCAR-E were evaluated on 500-item samples."));
C.push(B("**Possible pretraining contamination.** Every dataset used here has been publicly available, some for over a decade. The LLM, and to a lesser degree the pretrained transformers and embeddings, may have seen the questions or their labels."));
C.push(B("**Limited comparisons between model classes.** The transformer runs saved no item-level predictions, were trained on different corpora, and were evaluated on different samples from the LLM. Comparisons between them are descriptive only."));
C.push(B("**Taxonomy alignment.** Original and revised taxonomies were aligned by name, which is provisional; LAK40 uses sets of acceptable levels and EDUQG covers only levels 1–4."));
C.push(B("**Provenance gaps.** EduBloom's generation method is not described beyond \"generated\", and its version year is unconfirmed. The script that produced the frozen EduBloom models is missing; they are reproducible from saved weights only. LAK40's link to Li et al. (2022) is inferred from a matching description, and its source states a single-label sampling procedure that does not match its two multi-label items. YouLeQD, EduQG and the LAK '26 release have no licence files, which restricts redistribution of text."));
C.push(B("**Analytic choices.** Coarse-level comparisons use constants chosen with the labels, which favours the constants, and coarse values depend on the decision rule (Figure 3 caption). Information weights for coarse decisions are a modelling choice."));
C.push(B("**Researcher degrees of freedom.** The study evolved over many phases, and RQ5 was formulated after the initial failures. Exploratory findings, including the PASS-over-FAIL separation, are labelled as such and should be treated as hypotheses."));

// ---------------- 8 Conclusion ----------------
C.push(H1("8. Conclusion"));
C.push(P("Automated Bloom classifiers should be evaluated as measurements, starting with their training labels. A large public corpus whose labels track a difficulty field produced models that matched a majority baseline on learner questions, while a metadata-only rule matched a fine-tuned transformer on the corpus's own test. A small set of pre-training checks would have flagged this before any model was trained."));
C.push(P("Across eight corpora, label recoverability predicted transfer for simpler models, and gate decisions agreed across four supervised model classes. Recoverability alone did not detect generator labels that disagreed with experts, and correcting those labels did not improve transfer. No supervised model showed a statistically supported advantage over a constant on learner questions. A zero-shot LLM did so on the preregistered vote-loss metric but not on the consolidated label, a result that needs confirmation on unpublished data."));
C.push(P("Two pending studies will determine whether the gates rank transfer for strong pretrained models (Phase 73) and whether the LLM result holds on new learner questions (the confirmatory annotation study)."));

// ---------------- Declarations ----------------
C.push(H1("Declarations"));
C.push(P("**Data availability.** Datasets were obtained from public sources: EduBloom (Kaggle, doi:10.34740/kaggle/dsv/19232466; CC BY-SA 4.0); the Faraji et al. (2026) repository of the Yahya, Sangodiah, Mohammed & Omar, Gani and Scaria datasets (MIT); the Scaria et al. (2024) repository (MIT); the YouLeQD/QYTL repository (no licence file); the EduQG repository (no licence file); and the LAK '26 repository of Xu et al. (2026) (no licence file). Question text is not redistributed where no licence permits it; scripts rebuild these inputs from pinned commits. Derived outputs (predictions keyed by item identifiers, statistics, figures) are included in the project archives."));
C.push(P("**Code availability.** All analysis code, preregistrations, deviation logs and SHA-256 manifests are in the project archives (v1.0 frozen archive; continuation archives v1.1–v2.6). [Public repository and persistent identifier to be created before submission.]"));
C.push(P("**CRediT authorship contribution statement.** [To be completed by the authors. Roles to assign: Conceptualization; Methodology; Software; Validation; Formal analysis; Investigation; Data curation; Writing – original draft; Writing – review & editing; Visualization; Supervision; Project administration; Funding acquisition.]"));
C.push(P("**Funding.** [To be completed by the authors.]"));
C.push(P("**Competing interests.** [To be completed by the authors.] Readers should note that one evaluated system is an Anthropic model (claude-sonnet-5-5) and that an Anthropic model also assisted the analysis and drafting (see below)."));
C.push(P("**Declaration of generative AI use.** Claude (Anthropic) was used to write and run analysis code, audit earlier analyses, search and verify literature, and draft and revise this manuscript. The authors directed the work, ran the Colab-based transformer and LLM evaluations, supplied data and provenance information, and approved the conclusions. The authors take full responsibility for the content. [Authors to confirm, and to declare any other AI tools used, for example in audit planning.] Separately from this assistance, claude-sonnet-5-5 was an object of evaluation (Phase 70)."));

// ---------------- References ----------------
C.push(H1("References"));
C.push(P("Entries marked † were recorded from standard bibliographic knowledge and must be checked against the publisher record before submission. Entries marked ‡ were verified through citing sources rather than the publisher record. All other entries were checked against a primary or bibliographic source during preparation of this draft.", { run: { size: 18 } }));
const refs = [
  "Anderson, L. W., & Krathwohl, D. R. (Eds.). (2001). *A taxonomy for learning, teaching, and assessing: A revision of Bloom's taxonomy of educational objectives*. Longman. †",
  "Angelopoulos, A. N., Bates, S., Candès, E. J., Jordan, M. I., & Lei, L. (2025). Learn then test: Calibrating predictive algorithms to achieve risk control. *The Annals of Applied Statistics, 19*(2), 1641–1662. https://doi.org/10.1214/24-AOAS1998",
  "Bloom, B. S. (Ed.). (1956). *Taxonomy of educational objectives: The classification of educational goals. Handbook I: Cognitive domain*. David McKay.",
  "Caprio, M., Stutz, D., Li, S., & Doucet, A. (2024). Conformalized credal regions for classification with ambiguous ground truth. *Transactions on Machine Learning Research*. arXiv:2411.04852",
  "Chow, C. K. (1970). On optimum recognition error and reject tradeoff. *IEEE Transactions on Information Theory, 16*(1), 41–46. †",
  "Dunn, R., Wasserman, L., & Ramdas, A. (2023). Distribution-free prediction sets for two-layer hierarchical models. *Journal of the American Statistical Association, 118*(544), 2491–2502. https://doi.org/10.1080/01621459.2022.2060112",
  "Faraji, A., Molavi, M., Rasoulkhani, Z., Tavakoli, M., & Kismihók, G. (2026). Cross-dataset Bloom question classification: Supervised models and prompted LLMs. Accepted at *Artificial Intelligence in Education (AIED 2026)*. arXiv:2606.13684",
  "Gani, M. O., Ayyasamy, R. K., Sangodiah, A., & Fui, Y. T. (2023). Bloom's taxonomy-based exam question classification: The outcome of CNN and optimal pre-trained word embedding technique. *Education and Information Technologies, 28*(12), 15893–15914. https://doi.org/10.1007/s10639-023-11842-1",
  "Geifman, Y., & El-Yaniv, R. (2017). Selective classification for deep neural networks. *Advances in Neural Information Processing Systems, 30*. †",
  "Geirhos, R., Jacobsen, J.-H., Michaelis, C., Zemel, R., Brendel, W., Bethge, M., & Wichmann, F. A. (2020). Shortcut learning in deep neural networks. *Nature Machine Intelligence, 2*, 665–673. †",
  "Goren, S., Galil, I., & El-Yaniv, R. (2024). Hierarchical selective classification. *Advances in Neural Information Processing Systems, 37*. arXiv:2405.11533",
  "Gururangan, S., Swayamdipta, S., Levy, O., Schwartz, R., Bowman, S., & Smith, N. A. (2018). Annotation artifacts in natural language inference data. In *Proceedings of NAACL-HLT 2018* (pp. 107–112). †",
  "Hadifar, A., Bitew, S. K., Deleu, J., Develder, C., & Demeester, T. (2023). EduQG: A multi-format multiple-choice dataset for the educational domain. *IEEE Access, 11*, 20885–20896. https://doi.org/10.1109/ACCESS.2023.3248790",
  "Hoeffding, W. (1963). Probability inequalities for sums of bounded random variables. *Journal of the American Statistical Association, 58*(301), 13–30. †",
  "Kane, M. T. (2013). Validating the interpretations and uses of test scores. *Journal of Educational Measurement, 50*(1), 1–73. †",
  "Kumar, R., Gulwani, D., & Singh, S. (2025). Automated analysis of learning outcomes and exam questions based on Bloom's taxonomy. arXiv:2511.10903",
  "Li, Y., Raković, M., Poh, B. X., Gašević, D., & Chen, G. (2022). Automatic classification of learning objectives based on Bloom's taxonomy. In *Proceedings of the 15th International Conference on Educational Data Mining* (pp. 530–537). https://doi.org/10.5281/zenodo.6853191",
  "Ming, N., Sharma, S., & Noh, J. (2025). YouLeQD: Decoding the cognitive complexity of questions and engagement in online educational videos from learners' perspectives. In *2025 IEEE 19th International Conference on Semantic Computing (ICSC)*. arXiv:2501.11712 [pages to add]",
  "Mohammed, M., & Omar, N. (2020). Question classification based on Bloom's taxonomy cognitive domain using modified TF-IDF and word2vec. *PLOS ONE, 15*(3), e0230442. https://doi.org/10.1371/journal.pone.0230442",
  "Northcutt, C. G., Jiang, L., & Chuang, I. L. (2021). Confident learning: Estimating uncertainty in dataset labels. *Journal of Artificial Intelligence Research, 70*, 1373–1411. †",
  "Sangodiah, A., Ahmad, R., & Wan Ahmad, W. F. (2017). Taxonomy based features in question classification using support vector machine. *Journal of Theoretical and Applied Information Technology, 95*(12), 2814–2823. ‡",
  "Scaria, N., Chenna, S. D., & Subramani, D. (2024). Automated educational question generation at different Bloom's skill levels using large language models: Strategies and evaluation. In *Artificial Intelligence in Education (AIED 2024)* (pp. 165–179). Springer. https://doi.org/10.1007/978-3-031-64299-9_12",
  "Sharma, P., Saiyad, U., & Sable, R. (n.d.). *EduBloom: Bloom taxonomy questions dataset* [Data set]. Kaggle. https://doi.org/10.34740/kaggle/dsv/19232466 [version year to add]",
  "Stanny, C. J. (2016). Reevaluating Bloom's taxonomy: What measurable verbs can and cannot say about student learning. *Education Sciences, 6*(4), 37.",
  "Stutz, D., Guha Roy, A., Matejovicova, T., Strachan, P., Cemgil, A. T., & Doucet, A. (2023). Conformal prediction under ambiguous ground truth. *Transactions on Machine Learning Research*. arXiv:2307.09302",
  "Uma, A. N., Fornaciari, T., Hovy, D., Paun, S., Plank, B., & Poesio, M. (2021). Learning from disagreement: A survey. *Journal of Artificial Intelligence Research, 72*, 1385–1470. †",
  "Williamson, D. M., Xi, X., & Breyer, F. J. (2012). A framework for evaluation and use of automated scoring. *Educational Measurement: Issues and Practice, 31*(1), 2–13. https://doi.org/10.1111/j.1745-3992.2011.00223.x [DOI verified; volume and pages †]",
  "Xu, Z., Khatri, V., Dai, Y., Liu, X., Li, S., Zhang, X., & Yu, R. (2026). Enhancing LLM-based data annotation with error decomposition. In *Proceedings of the 16th International Learning Analytics & Knowledge Conference (LAK '26)*. arXiv:2601.11920 [pages to add]",
  "Yahya, A. A., Toukal, Z., & Osman, A. (2012). Bloom's taxonomy–based classification for item bank questions using support vector machines. In W. Ding, H. Jiang, M. Ali, & M. Li (Eds.), *Modern advances in intelligent systems and tools* (Studies in Computational Intelligence, Vol. 431, pp. 135–140). Springer. https://doi.org/10.1007/978-3-642-30732-4_17"];
for (const r of refs) C.push(new Paragraph({ children: runs(r, { size: 20 }), indent: { left: 360, hanging: 360 }, spacing: { after: 80 } }));

// ---------------- Appendix A ----------------
C.push(new Paragraph({ children: [new PageBreak()] }));
C.push(H1("Appendix A. Integration map for pending results"));
C.push(P("No pending result is anticipated in the text. When each study is complete and validated, its results enter at the locations below, under its preregistration."));
C.push(tcap("Table A1.", "Where pending results will be integrated."));
C.push(table(["Pending study", "Manuscript location", "What changes"], [
  ["Phase 73: transformers at k = 8 (H12a, H12b)", "Table 8 (replace the pending row); Figure 5 (add k = 8 transformer panels); Section 5.5; Section 6.2", "Whether G0 ranks transfer for pretrained transformers"],
  ["Phase 73: PASS-over-FAIL separation (H12c)", "Section 5.5, paragraph on gate decisions; Section 6.2", "The separation moves from exploratory to confirmatory or is withdrawn"],
  ["Phase 73: item-level YouLeQD predictions", "Section 5.2 (transformer paragraph); Table 6 (add rows); Section 6.4", "Paired, video-clustered comparisons of transformers with the LLM and the constant become possible"],
  ["Confirmatory learner-question study", "New Section 5.6; Abstract; Sections 6.4, 7 and 8", "Replication of the H10-type comparison on unpublished data; G2 and certification on a larger sample"]],
  [2.4, 3.2, 3.0]));

// ---------------- Assemble ----------------
const doc = new Document({
  creator: "B-TRUST project", title: "When Bloom Labels Measure Difficulty (working draft v0.2)",
  styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial" }, paragraph: { spacing: { before: 360, after: 160 }, outlineLevel: 0, keepNext: true } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial" }, paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1, keepNext: true } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 22, bold: true, italics: true, font: "Arial" }, paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 2, keepNext: true } }] },
  numbering: { config: [
    { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
    { reference: "nums", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 540, hanging: 300 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: "Working draft v0.2 — not for submission — page ", size: 16 }), new TextRun({ children: [PageNumber.CURRENT], size: 16 })] })] }) },
    children: C }] });
Packer.toBuffer(doc).then(b => { fs.writeFileSync("BTRUST_Manuscript_v0.2.docx", b); console.log("written", b.length); });
