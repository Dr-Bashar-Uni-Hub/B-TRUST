"""Sensitivity of TF-IDF G0 to repeated texts (Supplementary Table S8; manuscript Section 4.5). Rule: drop texts with
conflicting labels, then keep one copy of each remaining repeated text. Same model and folds as the preregistered G0."""
import sys, numpy as np, pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import cohen_kappa_score
sys.path.insert(0, "."); import corpora as C
def g0(d):
    X = d.n.to_numpy(); y = d.y.to_numpy(); p = np.zeros(len(y), int)
    for a, b in StratifiedKFold(5, shuffle=True, random_state=65).split(X, y): p[b] = C.model().fit(X[a], y[a]).predict(X[b])
    maj = pd.Series(y).value_counts(normalize=True).iloc[0]; lift = (p == y).mean() - maj; k = cohen_kappa_score(y, p)
    return lift, k, ("FAIL" if (lift < .05 or k < .20) else ("PASS" if (lift >= .15 and k >= .40) else "CAUTION"))
rows = []
for name, f in [("SCAR-I", C.scar_i), ("SCAR-E", C.scar_e), ("EDUQG", C.eduqg)]:
    d = f(); o = g0(d); bad = d.groupby("n").y.nunique().loc[lambda s: s > 1].index
    dd = d[~d.n.isin(bad)].drop_duplicates("n").reset_index(drop=True); n_ = g0(dd)
    rows.append(dict(corpus=name, n_orig=len(d), n_dedup=len(dd), lift_orig=o[0], lift_dedup=n_[0], kappa_orig=o[1], kappa_dedup=n_[1], gate_orig=o[2], gate_dedup=n_[2]))
pd.DataFrame(rows).to_csv("dedup_sensitivity.csv", index=False); print(pd.DataFrame(rows).round(4).to_string(index=False))
