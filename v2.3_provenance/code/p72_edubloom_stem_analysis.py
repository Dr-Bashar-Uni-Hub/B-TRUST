"""Phase 72 (descriptive, not preregistered): EduBloom stem-distribution distances between levels."""
import sys, re, pandas as pd
from scipy.spatial.distance import jensenshannon
q = pd.read_csv(sys.argv[1] if len(sys.argv) > 1 else "/home/claude/bt/ex/Phase42_Results/phase42/questions.csv")
q["stem"] = [re.sub(r"\s+", " ", a.replace(b, "<T>")).split(",")[0] for a, b in zip(q.question, q.topic)]
ct = pd.crosstab(q.stem, q.bloom_level); P = (ct / ct.sum()).T; L = list(P.index)
M = pd.DataFrame([[jensenshannon(P.loc[a], P.loc[b], base=2) for b in L] for a in L], index=L, columns=L); print(M.round(3))
cre = r"\b(?:design|create|propose|develop|construct|formulate|invent|compose|devise|build)\b"
print({l: round(q[q.bloom_level == l].question.str.lower().str.contains(cre).mean(), 4) for l in L})
print("shared stems L5&L6:", len(set(ct.index[ct.L5 > 0]) & set(ct.index[ct.L6 > 0])), "of", (ct.L5 > 0).sum(), "/", (ct.L6 > 0).sum())
M.to_csv("p72_edubloom_stem_JS_distance.csv")
