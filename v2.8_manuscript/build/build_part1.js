// B-TRUST manuscript builder — part 1 (helpers + Abstract → Experimental Setup)
const fs = require("fs");
const D = require("docx");
const { Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, AlignmentType, HeadingLevel,
        ShadingType, BorderStyle, LevelFormat, PageBreak, Footer, PageNumber } = D;

const TW = 9026; // text width in DXA (A4, 1-inch margins)
const FONT = "Times New Roman";

// --- inline markup: **bold**, *italic* ---
function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*)/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const t = m[0];
    if (t.startsWith("**")) out.push(new TextRun({ text: t.slice(2, -2), bold: true, ...base }));
    else out.push(new TextRun({ text: t.slice(1, -1), italics: true, ...base }));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out;
}
const P = (text, opts = {}) => new Paragraph({ children: runs(text, opts.run || {}), spacing: { after: 120, line: 276 },
  alignment: opts.align || AlignmentType.JUSTIFIED, ...(opts.para || {}) });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)] });
const H3 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun(t)] });
const B = (text, level = 0) => new Paragraph({ numbering: { reference: "bullets", level }, children: runs(text),
  spacing: { after: 60, line: 276 } });
const N = (text, ref = "nums") => new Paragraph({ numbering: { reference: ref, level: 0 }, children: runs(text),
  spacing: { after: 60, line: 276 } });

function img(file, widthPx) {
  const sz = { "fig1_edubloom_difficulty_level": [1560, 660], "fig2_distilbert_confusion": [1080, 960],
    "fig3_vote_loss_granularity": [1860, 840], "fig4_g0_vs_transfer": [2160, 690], "fig5_power": [1260, 780],
    "fig0_framework": [3200, 2360], "eq1": [948, 196], "eq2": [1088, 160], "eq3": [1535, 99] }[file];
  const h = Math.round(widthPx * sz[1] / sz[0]);
  return new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 80 },
    children: [new ImageRun({ type: "png", data: fs.readFileSync(`fig/${file}.png`), transformation: { width: widthPx, height: h },
      altText: { title: file, description: file, name: file } })] });
}
const eq = (file, w, label) => [img(file, w), new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 120 },
  children: [new TextRun({ text: `(${label})`, font: FONT })] })];
const caption = (label, text) => new Paragraph({ spacing: { before: 60, after: 200 }, alignment: AlignmentType.JUSTIFIED,
  children: [new TextRun({ text: label + " ", bold: true, size: 20 }), ...runs(text, { size: 20 })] });

const border = { style: BorderStyle.SINGLE, size: 4, color: "999999" };
const borders = { top: border, bottom: border, left: border, right: border };
function table(headers, rows, widths) {
  const sum = widths.reduce((a, b) => a + b, 0);
  const w = widths.map(x => Math.round(x * TW / sum)); w[w.length - 1] += TW - w.reduce((a, b) => a + b, 0);
  const cell = (t, i, head) => new TableCell({ borders, width: { size: w[i], type: WidthType.DXA },
    shading: head ? { fill: "E7E6E6", type: ShadingType.CLEAR, color: "auto" } : undefined,
    margins: { top: 50, bottom: 50, left: 90, right: 90 },
    children: [new Paragraph({ children: runs(String(t), { size: 18, bold: head || undefined }), spacing: { after: 0 } })] });
  return new Table({ width: { size: TW, type: WidthType.DXA }, columnWidths: w,
    rows: [new TableRow({ tableHeader: true, children: headers.map((h, i) => cell(h, i, true)) }),
           ...rows.map(r => new TableRow({ children: r.map((c, i) => cell(c, i, false)) }))] });
}
const tcap = (label, text) => new Paragraph({ spacing: { before: 200, after: 80 }, keepNext: true,
  children: [new TextRun({ text: label + " ", bold: true, size: 20 }), ...runs(text, { size: 20 })] });
const gap = () => new Paragraph({ spacing: { after: 160 }, children: [] });

const C = []; // content

// ---------------- Title page ----------------
C.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 600, after: 240 }, children: [new TextRun({
  text: "When Bloom Labels Measure Difficulty: A Validity-First Evaluation of Automated Cognitive-Level Classification under Annotator Disagreement and Dataset Shift",
  bold: true, size: 32, font: "Arial" })] }));
C.push(P("**Working draft v0.4 — 20 November 2026 — not for submission**", { align: AlignmentType.CENTER }));
C.push(P("**Bashar ALHAJAHMAD**", { align: AlignmentType.CENTER }));
C.push(P("Assistant Professor (Dr. Öğr. Üyesi), Department of Computer Engineering, Faculty of Engineering, Siirt University, Siirt, Türkiye", { align: AlignmentType.CENTER }));
C.push(P("ORCID: 0009-0009-3455-7206 (https://orcid.org/0009-0009-3455-7206)", { align: AlignmentType.CENTER }));
C.push(P("**Corresponding author:** Bashar ALHAJAHMAD, bashar.ahmad@siirt.edu.tr", { align: AlignmentType.CENTER }));
C.push(P("**Status of evidence.** All results are verified through analysis Phase 75. Phases 73 (eight-corpus transformer replication) and 75 (exploratory robustness analyses from existing outputs) are integrated. Two components are pending and no conclusion in this draft depends on them: a proposed steps-matched fine-tuning experiment (Phase 76, awaiting approval) and the confirmatory learner-question annotation study. Appendix A lists where their results will be integrated. Analyses are labelled **confirmatory** (preregistered, hashed before outcomes were seen), **exploratory** (not preregistered, or secondary) or **descriptive** (no inferential test).", { para: { border: { top: border, bottom: border, left: border, right: border } } }));

// ---------------- Abstract ----------------
C.push(H1("Abstract"));
C.push(P("Automated classification of questions by Bloom's taxonomy is widely proposed for item banks and learning analytics, yet reported accuracies are usually within-dataset and rarely examine what the training labels measure. We present a validity-first evaluation of automated Bloom classification using eight labelled corpora, two held-out human-judged targets, and five model classes."));
C.push(P("A public 73,712-question corpus, documented by its authors as generated, has labels that track a three-level difficulty field rather than question text. A rule using only the difficulty field matched a fine-tuned DistilBERT on a balanced test (50.0% vs 50.9%), and the corpus's \"Evaluate\" and \"Create\" levels share 787 of about 793 question stems. Models trained on it did not exceed a majority baseline on 70 learner questions from lecture-video comments, on which three annotators agreed unanimously for only nine."));
C.push(P("We propose six validity checks, organised by the evidence each requires rather than as a strict sequence: label recoverability from text, level coverage, provenance agreement with independent experts, skill over a constant on the target population, the human-disagreement ceiling, and decision readiness. In preregistered tests across eight corpora, recoverability predicted cross-corpus transfer for TF-IDF models (Spearman ρ = 0.93, exact p = 0.001), more weakly for word embeddings (ρ = 0.69, p = 0.035), and for fine-tuned DistilBERT and RoBERTa (ρ = 0.83, p = 0.008; ρ = 0.93, p < 0.001). For the transformers, part of this association reflects training collapse on the two smallest corpora, which also changed their gate decisions; the association held without them (ρ = 0.94, p = 0.008). In exploratory analyses it was not explained by corpus size, but for TF-IDF it could not be separated from class balance, and no training-free diagnostic predicted transformer transfer, so recoverability as measured here partly reflects model trainability. Recoverability alone did not flag LLM-generated labels that agreed with experts less than experts agreed with each other, and correcting those labels did not change transfer."));
C.push(P("A zero-shot large language model had lower six-level vote loss than the best constant classifier on learner questions (preregistered; difference −0.148, 95% CI −0.232 to −0.065), but its accuracy on the consolidated label did not differ significantly (34/70 vs 26/70, p = 0.17). No fine-tuned model showed a multiplicity-corrected advantage over the constant. Certifying selective decisions on such data would require roughly 236 independent sources of accepted decisions."));
C.push(P("**Keywords:** Bloom's taxonomy; automated question classification; validity; annotator disagreement; dataset shift; selective prediction; learning analytics"));

// ---------------- 1 Introduction ----------------
C.push(H1("1. Introduction"));
C.push(P("Bloom's taxonomy (Bloom, 1956; Anderson & Krathwohl, 2001) is the most common framework for describing the cognitive demand of educational questions and learning objectives. Classifying items by hand is slow and teacher-dependent, so a long line of work has proposed automated classifiers, from support vector machines (Yahya et al., 2012) to word-embedding and convolutional models (Mohammed & Omar, 2020; Gani et al., 2023), transformer classifiers for learning objectives (Li et al., 2022) and, recently, large language models (LLMs) (Kumar et al., 2025; Faraji et al., 2026). These systems are proposed for tagging item banks, auditing assessments and analysing learner questions (Ming et al., 2025)."));
C.push(P("Reported accuracies are typically within-dataset. Faraji et al. (2026) showed that supervised models degrade substantially on unseen Bloom datasets while prompted LLMs are more stable. Two questions remain underexamined. First, what do the training labels measure? A classifier can be accurate on its own test split while learning something other than cognitive demand. Second, what does accuracy mean when human judgement of Bloom levels is itself unreliable? The least reliable labels belong to one of the most consequential applications, learner-posed questions."));
C.push(P("This paper treats automated Bloom classification as a measurement problem. Following argument-based validity (Kane, 2013) and its application to automated scoring (Williamson et al., 2012), we ask what evidence must hold before a classifier's output can be interpreted as a cognitive level. The study began as an attempt to build a risk-controlled selective classifier for Bloom levels on learner questions. That attempt failed, and diagnosing why produced the findings reported here."));
C.push(P("**Research questions.**"));
C.push(N("**RQ1 — Label validity.** Are a large public Bloom corpus's labels recoverable from question text beyond its difficulty metadata?"));
C.push(N("**RQ2 — Transfer.** Do models trained on that corpus agree with human Bloom judgements of real learner questions beyond a majority baseline, and do taxonomy-matched human-authored corpora or a zero-shot LLM do better?"));
C.push(N("**RQ3 — Ceiling.** How much headroom does annotator disagreement leave at six, three and two levels?"));
C.push(N("**RQ4 — Abstention and certification.** Can granularity back-off and risk-controlled abstention rescue usable decisions, and what sample size would certification need?"));
C.push(N("**RQ5 — Validity gates.** Do simple pre-training checks of label validity predict how well a corpus's models transfer, and do their decisions agree across model classes?"));
C.push(P("RQ1–RQ4 follow the original study plan; RQ5 was added when the gate framework was developed and is tested only in preregistered phases."));
C.push(P("**Contributions.** We make five contributions, none of which is a new learning or risk-control algorithm:"));
C.push(B("**A documented validity failure.** A public 73,712-question corpus, generated according to its own documentation, encodes difficulty rather than cognitive level. Models trained on it match a majority baseline on learner questions."));
C.push(B("**A validity-first gate framework** with quantified decision rules, operationalising established validity reasoning (Kane, 2013; Williamson et al., 2012) for the *training labels* of Bloom classifiers. Each check caught a real failure that the others passed. The study separates three properties that are easily conflated: label validity, label recoverability, and model trainability; it shows that the recoverability check is relative to the model and training configuration used to compute it."));
C.push(B("**Preregistered evidence** that label recoverability predicts cross-corpus transfer across eight corpora and four supervised model classes, reported with explicit negative and qualifying results: label correction and filtering did not improve transfer, the transformer ranking failed on five corpora and was partly driven by training collapse on eight."));
C.push(B("**A power analysis for certification**, showing why distribution-free risk control is infeasible on current learner-question data and how many independent sources it would require."));
C.push(B("**Open materials**: preregistrations, deviation logs, code, outputs and checksummed archives for every analysis phase."));

// ---------------- 2 Related Work ----------------
C.push(H1("2. Related Work"));
C.push(H2("2.1 Automated Bloom classification"));
C.push(P("Supervised Bloom classifiers have progressed from SVMs on term-frequency features (Yahya et al., 2012) and taxonomy-based features (Sangodiah et al., 2017), through modified TF-IDF combined with word2vec (Mohammed & Omar, 2020), to CNNs over pretrained contextual embeddings (Gani et al., 2023). For learning objectives, Li et al. (2022) annotated 21,380 objectives from 5,558 university courses and reported strong BERT-based classification. Several small human-authored question corpora recur across this literature, and later corpora often pool earlier ones. We found that a 2,522-question set distributed with the YouLeQD repository contains, with identical labels, every item of the Yahya, Sangodiah, Mohammed & Omar and Gani corpora as redistributed by Faraji et al. (2026), plus seven items."));
C.push(P("Most of these labels follow verb-based guidance. Verb lists are a known weak proxy for cognitive demand (Stanny, 2016), and in our data a lookup on the first word of a question recovers much of the label signal in such corpora."));
C.push(P("Generated corpora are a growing alternative. Scaria et al. (2024) prompted LLMs to generate questions at each Bloom level and had two experts judge each question's level, producing both an intended (generator) label and an expert label for the same text. Ming et al. (2025) released YouLeQD, learner questions extracted from YouTube lecture comments, with a 300-question subset coded by three annotators. Hadifar et al. (2023) released EduQG, in which 903 expert-written multiple-choice questions carry Bloom levels."));
C.push(H2("2.2 Cross-dataset transfer and LLMs"));
C.push(P("Faraji et al. (2026) evaluated supervised models and prompted LLMs across five Bloom corpora and found that supervised models degraded on unseen datasets, whereas LLMs were more stable. Kumar et al. (2025) likewise reported competitive zero-shot LLM accuracy on a 600-item corpus. Our LLM results are consistent with this prior work and should not be read as a new finding about LLMs. What we add is evidence about *why* supervised transfer varies: in our data, transfer tracked a measurable property of the training labels."));
C.push(H2("2.3 Validity of automated scoring and dataset artifacts"));
C.push(P("Argument-based validity (Kane, 2013) asks what evidence supports a proposed interpretation of scores. Williamson et al. (2012) set out categories of validity evidence for automated scoring, including construct relevance, agreement with human scores and generalisability. These categories address system outputs; we apply the same reasoning to the training labels of automated classifiers. Machine learning research has documented how models exploit features correlated with labels but not with the intended construct, as in shortcut learning (Geirhos et al., 2020) and annotation artifacts (Gururangan et al., 2018). Our recoverability gate is a simple pre-training diagnostic in this tradition."));
C.push(H2("2.4 Disagreement, label noise and annotation by LLMs"));
C.push(P("Learning from disagreement treats annotator variation as signal rather than noise (Uma et al., 2021). Confident learning (Northcutt et al., 2021) prunes likely label errors using out-of-fold model confidence; we test it as a baseline. In learning analytics, Xu et al. (2026) decomposed LLM annotation errors into task-inherent ambiguity and model-specific error, using, among other tasks, a sample of the Li et al. (2022) learning objectives; one of our held-out targets comes from their released files."));
C.push(H2("2.5 Selective prediction and distribution-free risk control"));
C.push(P("Selective classification (Chow, 1970; Geifman & El-Yaniv, 2017) and its hierarchical extension (Goren et al., 2024) trade coverage for risk. Learn-then-Test (Angelopoulos et al., 2025) provides distribution-free control of multiple risks through multiple testing, with extensions for ambiguous ground truth (Stutz et al., 2023; Caprio et al., 2024) and clustered data (Dunn et al., 2023). Every component of the selective controller we originally proposed already exists in this literature, so we make no algorithmic novelty claim. We use these tools to quantify what certification would require on learner-question data."));

module.exports = { D, C, P, H1, H2, H3, B, N, img, eq, caption, table, tcap, gap, runs, TW, FONT, border };
