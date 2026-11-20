"""B-TRUST framework diagram — editable SVG source, rendered to vector PDF and PNG with cairosvg.
Grayscale-safe: meaning is carried by line style and labels, not colour."""
import cairosvg, html
W, H = 1600, 1180
FONT = "Arial, 'Liberation Sans', 'DejaVu Sans', sans-serif"
out = []
def esc(s): return html.escape(s, quote=False)
def box(x, y, w, h, lines, fill="#FFFFFF", stroke="#000000", sw=1.6, dash=None, bold_first=True, fs=17, rx=6, tag=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    n = len(lines); lh = fs * 1.25; y0 = y + h / 2 - (n - 1) * lh / 2 + fs * 0.35
    for i, t in enumerate(lines):
        wgt = "bold" if (i == 0 and bold_first) else "normal"
        size = fs if i == 0 else fs - 2
        out.append(f'<text x="{x + w / 2}" y="{y0 + i * lh}" text-anchor="middle" font-family="{FONT}" font-size="{size}" font-weight="{wgt}" fill="#000">{esc(t)}</text>')
    if tag:
        out.append(f'<text x="{x + w - 8}" y="{y + 16}" text-anchor="end" font-family="{FONT}" font-size="12" font-style="italic" fill="#333">{esc(tag)}</text>')
def band(y, h, title):
    out.append(f'<rect x="20" y="{y}" width="{W - 40}" height="{h}" rx="10" fill="#F2F2F2" stroke="#7F7F7F" stroke-width="1.2"/>')
    out.append(f'<text x="40" y="{y + 28}" font-family="{FONT}" font-size="20" font-weight="bold" fill="#000">{esc(title)}</text>')
def arrow(x1, y1, x2, y2, dash=None, sw=1.6, marker="arr"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#000" stroke-width="{sw}"{d} marker-end="url(#{marker})"/>')
def path(dpath, dash=None, sw=1.6):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    out.append(f'<path d="{dpath}" fill="none" stroke="#000" stroke-width="{sw}"{d} marker-end="url(#arr)"/>')
def label(x, y, t, fs=13, anchor="middle", italic=True):
    st = ' font-style="italic"' if italic else ""
    out.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" font-size="{fs}"{st} fill="#000">{esc(t)}</text>')

out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
out.append('<defs><marker id="arr" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#000"/></marker></defs>')
out.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>')

# ---- Layer 1: input ----
band(20, 170, "1  Input: corpora and data preparation")
bw, bh, by = 340, 100, 70
xs = [45, 430, 815, 1200]
box(xs[0], by, bw, bh, ["Labelled corpora", "Questions and learning objectives", "(training corpora and targets)"])
box(xs[1], by, bw, bh, ["Provenance and label source", "Generator, publisher, single expert,", "expert consensus; licence"])
box(xs[2], by, bw, bh, ["Taxonomy harmonisation", "Original ↔ revised Bloom by name", "(provisional alignment)"])
box(xs[3], by, bw - 10, bh, ["Duplicate and overlap checks", "Within-corpus duplicates; cross-corpus", "overlap; test-set leakage rule"])

# ---- Layer 2: validity assessment ----
band(210, 470, "2  Validity assessment: gates grouped by the evidence each one requires")
cw, ch, cy = 290, 205, 300
cx = [45, 350, 655, 960, 1265]
heads = [("Corpus labels only", "no model"), ("Corpus + cross-validated model", "model-relative"), ("Independent expert labels", "on a sample"),
         ("Target-population human labels", "≥ 2 annotators + model"), ("Calibration data + model", "power analysis first")]
for x, (h1, h2) in zip(cx, heads):
    label(x + cw / 2, cy - 30, h1, fs=15, italic=False); label(x + cw / 2, cy - 12, h2, fs=13)
box(cx[0], cy, cw, ch, ["G0b  Level coverage", "≥ 30 items at each of", "the six levels"], tag="corpus-level")
box(cx[1], cy, cw, ch, ["G0  Label recoverability", "CV accuracy minus max(majority,", "metadata-only); κ_CV", "+ collapse check (top-class share)"], tag="corpus-level")
box(cx[2], cy, cw, ch, ["G1  Provenance agreement", "κ(label source, expert) ÷", "κ(expert, expert)"], tag="corpus-level")
box(cx[3], cy, cw, 95, ["G3  Human disagreement", "Leave-one-annotator-out", "vote loss at 6 / 3 / 2 levels"], tag="target-level", fs=16)
box(cx[3], cy + 110, cw, 95, ["G2  Target-population skill", "Vote loss and accuracy vs", "best constant (fixed a priori)"], tag="target-level", fs=16)
box(cx[4], cy, cw, ch, ["G4  Decision readiness", "Certification feasibility:", "power plan, then video-level", "Learn-then-Test"], tag="target-level")
arrow(cx[3] + cw / 2, cy + 95, cx[3] + cw / 2, cy + 110)            # G3 -> G2 (ceiling reference)
label(cx[3] + cw / 2 + 62, cy + 106, "ceiling", fs=12)
arrow(cx[3] + cw, cy + 157, cx[4], cy + 157)                          # G2 -> G4
# investigation box (under the corpus-level columns)
iy = 545
box(45, iy, 900, 125, ["Gate FAIL or CAUTION → investigate; not by itself proof of invalid labels",
    "Check: training collapse and corpus size · class imbalance · metadata or template leakage",
    "· provenance and generation process · taxonomy alignment · threshold sensitivity",
    "If unresolved: restrict use, revise the corpus, or collect new labels"], dash="7,5", fs=16)
for x in cx[:3]:
    path(f"M{x + cw / 2},{cy + ch} L{x + cw / 2},{iy}", dash="2,4", sw=1.3)
path(f"M{cx[3] + 70},{cy + ch} L{cx[3] + 70},{iy + 45} L946,{iy + 45}", dash="2,4", sw=1.3)
path(f"M{cx[4] + 60},{cy + ch} L{cx[4] + 60},{iy + 85} L946,{iy + 85}", dash="2,4", sw=1.3)

# input -> corpus-level gates
for x in cx[:3]:
    arrow(x + cw / 2, 190, x + cw / 2, cy - 42)

# ---- Layer 3: evaluation ----
band(700, 200, "3  Evaluation: model classes and targets")
ey, eh = 765, 115
box(45, ey, 250, eh, ["TF-IDF logistic", "regression", "(word 1–2-grams)"], fs=16)
box(310, ey, 250, eh, ["Word-embedding", "logistic regression", "(spaCy mean vectors)"], fs=16)
box(575, ey, 250, eh, ["Fine-tuned", "DistilBERT, RoBERTa", "(fixed settings)"], fs=16)
box(840, ey, 230, eh, ["Zero-shot LLM", "no training corpus;", "target-level only"], fs=16, dash="5,4")
box(1085, ey, 225, eh, ["Cross-dataset", "transfer", "(leakage rule)"], fs=16)
box(1325, ey, 230, eh, ["Held-out human-", "judged targets", "YouLeQD 70; LAK40"], fs=16)
# bracket over trained models (computes G0) and over all models (predictions for G2)
out.append(f'<line x1="170" y1="752" x2="700" y2="752" stroke="#000" stroke-width="1.4" stroke-dasharray="8,5"/>')
for x in (170, 435, 700): out.append(f'<line x1="{x}" y1="752" x2="{x}" y2="{ey}" stroke="#000" stroke-width="1.4" stroke-dasharray="8,5"/>')
path(f"M435,752 C435,700 495,690 495,{cy + ch}", dash="8,5", sw=1.4)
label(500, 742, "trained classes compute G0", fs=13, anchor="start")
out.append(f'<line x1="955" y1="745" x2="955" y2="{ey}" stroke="#000" stroke-width="1.4"/>')
path(f"M955,745 L1020,745 L1020,{cy + ch}", sw=1.4)
label(1026, 735, "predictions (all model classes)", fs=13, anchor="start")
path(f"M1440,{ey} L1440,725 L1180,725 L1180,{cy + ch}", sw=1.4)
path(f"M1500,{ey} L1500,{cy + ch}", sw=1.4)
label(1310, 718, "target labels", fs=13)
# ---- Layer 4: outputs ----
band(920, 240, "4  Outputs")
oy, oh, ow = 975, 115, 290
ox = [45, 350, 655, 960, 1265]
outs = [["Validity evidence", "and detected", "failure modes"], ["Cross-dataset", "generalisation", "(transfer T)"],
        ["Uncertainty and", "annotator", "disagreement"], ["Decision-readiness", "assessment", "(certifiable or not)"],
        ["Recommendation", "further validation, restricted", "use, or new annotation"]]
for x, t in zip(ox, outs): box(x, oy, ow, oh, t, fs=16)
for i in range(4): arrow(ox[i] + ow, oy + oh / 2, ox[i + 1], oy + oh / 2, sw=1.3)
path(f"M1197,{ey + eh} L1197,905 L495,905 L495,{oy}", sw=1.4)
arrow(800, 912, 800, oy - 2)

# legend
ly = 1118
out.append(f'<line x1="45" y1="{ly}" x2="95" y2="{ly}" stroke="#000" stroke-width="1.6"/>'); label(105, ly + 5, "data or evidence flow", fs=13, anchor="start", italic=False)
out.append(f'<line x1="300" y1="{ly}" x2="350" y2="{ly}" stroke="#000" stroke-width="1.4" stroke-dasharray="8,5"/>'); label(360, ly + 5, "model class used to compute a gate", fs=13, anchor="start", italic=False)
out.append(f'<line x1="620" y1="{ly}" x2="670" y2="{ly}" stroke="#000" stroke-width="1.3" stroke-dasharray="2,4"/>'); label(680, ly + 5, "FAIL / CAUTION routed to investigation", fs=13, anchor="start", italic=False)
label(1555, ly + 5, "corpus-level gates: G0b, G0, G1 · target-level gates: G2, G3, G4", fs=13, anchor="end")
out.append("</svg>")
svg = "\n".join(out)
open("btrust_framework.svg", "w").write(svg)
cairosvg.svg2pdf(bytestring=svg.encode(), write_to="btrust_framework.pdf")
cairosvg.svg2png(bytestring=svg.encode(), write_to="btrust_framework.png", output_width=3200)
print("written")
