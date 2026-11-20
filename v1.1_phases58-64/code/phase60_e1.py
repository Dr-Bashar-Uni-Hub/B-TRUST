"""Phase 60 / E1 — base-model validity (preregistered, sha256 1ea59177...).
Train fixed-config TF-IDF LR on DASQBT (human-authored, original Bloom names), evaluate on YouLeQD 70 relevant and LAK 40.
"""
import re, json, warnings
import numpy as np, pandas as pd, joblib
from scipy.stats import binomtest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import cohen_kappa_score, balanced_accuracy_score
warnings.filterwarnings("ignore")
BT = ["knowledge", "comprehension", "application", "analysis", "evaluation", "synthesis"]
L2N = {f"L{i+1}": v for i, v in enumerate(BT)}           # frozen-model provisional mapping
REV = dict(zip(BT, ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]))
norm = lambda s: re.sub(r"\s+", " ", str(s).lower()).strip()
EX = "/home/claude/bt/ex"

def load_das(aug=False):
    d = pd.read_csv("DASQBT/combined.csv"); d["n"] = d.QUESTION.map(norm)
    d["y"] = d["BT LEVEL"].str.strip().str.lower()
    d = d.drop_duplicates("n")
    if aug:
        a = pd.read_csv("DASQBT/train_aug.csv"); a["n"] = a.QUESTION.map(norm)
        a["y"] = a["BT LEVEL"].str.strip().str.lower(); d = pd.concat([d, a]).drop_duplicates("n")
    assert set(d.y) == set(BT)
    return d

def fit(d, variant="primary"):
    if variant == "char":
        vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=2, max_features=50000)
    else:
        vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=50000)
    lr = LogisticRegression(max_iter=2000, C=1.0, class_weight="balanced" if variant == "balanced" else None)
    return make_pipeline(vec, lr).fit(d.n, d.y)

r = pd.read_csv(f"{EX}/Phase42_Results/phase42/record_level_predictions.csv")
for c in ["label", "lebel1", "lebel2", "lebel3"]: r[c] = r[c].astype(str).str.strip().str.lower()
r["text"] = r.text.fillna("").astype(str); r["n"] = r.text.map(norm)
V = r[["lebel1", "lebel2", "lebel3"]].to_numpy()
rel = (r.label != "irrelevant").to_numpy()
vid = r.vid.astype(str).to_numpy()

def vote_loss(pred):  # G6, irrelevant votes never match
    return (V != np.asarray(pred)[:, None]).mean(1)

das = load_das()
models = {"DAS_LR": fit(das)}
models["A1_char"] = fit(das, "char"); models["A2_aug"] = fit(load_das(True)); models["A3_balanced"] = fit(das, "balanced")
P = {k: m.predict(r.n) for k, m in models.items()}
P["Frozen_EduBloom_LR"] = r.lr_prediction.map(L2N).to_numpy()
P["Frozen_DistilBERT"] = r.distilbert_prediction.map(L2N).to_numpy()
P["Majority_comprehension"] = np.array(["comprehension"] * len(r))
# Save DAS_LR full probabilities for Phases 61/63
proba = models["DAS_LR"].predict_proba(r.n); cls = list(models["DAS_LR"].classes_)
pd.DataFrame(proba, columns=[f"p_{c}" for c in cls]).assign(cid=r.cid).to_csv("p60_das_lr_proba_youleqd.csv", index=False)
joblib.dump(models["DAS_LR"], "p60_das_lr_model.joblib")

# human leave-one-annotator-out reference (G6)
H = np.mean([(V[:, j] != V[:, k]) for j in range(3) for k in range(3) if j != k], axis=0)

rows = []; rng = np.random.default_rng(60)
y = r.label.to_numpy()
for k, p in P.items():
    vl = vote_loss(p); m = rel
    acc = (p[m] == y[m]).mean()
    obs = acc; null = np.array([(rng.permutation(p[m]) == y[m]).mean() for _ in range(5000)])
    rows.append(dict(model=k, n=int(m.sum()), vote_loss=vl[m].mean(), consolidated_acc=acc,
                     kappa=cohen_kappa_score(y[m], p[m]), balanced_acc=balanced_accuracy_score(y[m], p[m]),
                     perm_p_vs_independence=(null >= obs).mean(),
                     pred_distribution=json.dumps(pd.Series(p[m]).value_counts().to_dict())))
rows.append(dict(model="Human_leave_one_out", n=int(rel.sum()), vote_loss=H[rel].mean()))
res = pd.DataFrame(rows); res.to_csv("p60_e1_youleqd_relevant.csv", index=False)
print(res.drop(columns="pred_distribution").round(4).to_string(index=False))

# PRIMARY: paired video-cluster bootstrap, 10,000 reps, seed 60
def cluster_boot(diff, groups, B=10000, seed=60):
    g = pd.Series(diff).groupby(groups); s = g.sum().to_numpy(); c = g.size().to_numpy()
    rg = np.random.default_rng(seed); G = len(s); out = np.empty(B)
    for b in range(B):
        i = rg.integers(0, G, G); out[b] = s[i].sum() / c[i].sum()
    return diff.mean(), np.percentile(out, [2.5, 97.5])
boot = []
for comp in ["Frozen_EduBloom_LR", "Frozen_DistilBERT", "Majority_comprehension", "A1_char", "A2_aug", "A3_balanced"]:
    d = vote_loss(P["DAS_LR"])[rel] - vote_loss(P[comp])[rel]
    est, ci = cluster_boot(d, vid[rel]); boot.append(dict(contrast=f"DAS_LR - {comp}", diff=est, ci_lo=ci[0], ci_hi=ci[1]))
d = vote_loss(P["DAS_LR"])[rel] - H[rel]; est, ci = cluster_boot(d, vid[rel])
boot.append(dict(contrast="DAS_LR - Human_LOO", diff=est, ci_lo=ci[0], ci_hi=ci[1]))
boot = pd.DataFrame(boot); boot.to_csv("p60_e1_cluster_bootstrap.csv", index=False)
print("\n", boot.round(4).to_string(index=False))
print("\nPRIMARY H1 (DAS_LR - Frozen_EduBloom_LR CI upper < 0):", bool(boot.iloc[0].ci_hi < 0))
print("videos among relevant:", len(set(vid[rel])))

# Confusion matrix for DAS_LR on relevant
print("\n", pd.crosstab(pd.Series(y[rel], name="consolidated"), pd.Series(P["DAS_LR"][rel], name="DAS_LR")))

# LAK secondary
lak = pd.read_csv(f"{EX}/Phase48_Final_LR/lak_matched_models.csv"); lak["n"] = lak.Learning_outcome.map(norm)
refs = lak.reference_labels.map(eval)
lp = {"DAS_LR": pd.Series(models["DAS_LR"].predict(lak.n)).map(REV),
      "Frozen_EduBloom_LR": lak.lr_prediction.map(L2N).map(REV), "Frozen_DistilBERT": lak.prediction.map(L2N).map(REV)}
hit = {k: np.array([p in s for p, s in zip(v, refs)]) for k, v in lp.items()}
lres = []
for k in hit:
    lres.append(dict(model=k, correct=int(hit[k].sum()), n=40, acc=hit[k].mean()))
for comp in ["Frozen_EduBloom_LR", "Frozen_DistilBERT"]:
    b = int((hit["DAS_LR"] & ~hit[comp]).sum()); c = int((~hit["DAS_LR"] & hit[comp]).sum())
    p = binomtest(b, b + c, 0.5).pvalue if b + c else 1.0
    lres.append(dict(model=f"McNemar DAS_LR vs {comp}", correct=b, n=b + c, acc=p))
lres = pd.DataFrame(lres); lres.to_csv("p60_e1_lak.csv", index=False)
print("\nLAK (acc column = exact McNemar p for McNemar rows; correct=DAS-only, n=discordant):\n", lres.round(4).to_string(index=False))
print("LAK reference distribution:", pd.Series([x for s in refs for x in s]).value_counts().to_dict())
print("LAK DAS_LR predictions:", lp["DAS_LR"].value_counts().to_dict())
