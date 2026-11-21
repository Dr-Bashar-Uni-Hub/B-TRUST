"""Independent reproduction of the post-hoc SCAR disagreement-screening analysis (manuscript Section 4.6; Supplementary S9).
Matched texts: SCAR-I intended vs SCAR-E expert consensus, after removing 2 SCAR-I texts with conflicting duplicate labels."""
import sys, re, numpy as np, pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
sys.path.insert(0,"."); import corpora as C
si=C.scar_i(); se=C.scar_e(); conf=si.groupby("n").y.nunique(); bad=set(conf[conf>1].index)
I=si[~si.n.isin(bad)].drop_duplicates("n").set_index("n"); E=se.drop_duplicates("n").set_index("n").y
sh=sorted(set(I.index)&set(E.index)); n=np.array(sh); y=(I.y.loc[sh].values!=E.loc[sh].values).astype(int); text=I.text.loc[sh].values
feat=np.column_stack([[len(t) for t in text],[len(t.split()) for t in text],[t.count("?") for t in text],[t.count(",") for t in text],[int(bool(re.search(r"\d",t))) for t in text]])
k=int(round(0.2*len(y))); rows=[]
for cw in [None,"balanced"]:
    for seed in [0,1,2,42,65]:
        pt=np.zeros(len(y)); pl=np.zeros(len(y))
        for a,b in StratifiedKFold(5,shuffle=True,random_state=seed).split(n,y):
            pt[b]=make_pipeline(TfidfVectorizer(ngram_range=(1,2),min_df=2),LogisticRegression(max_iter=2000,class_weight=cw)).fit(n[a],y[a]).predict_proba(n[b])[:,1]
            pl[b]=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000,class_weight=cw)).fit(feat[a],y[a]).predict_proba(feat[b])[:,1]
        rows.append(dict(class_weight=str(cw),seed=seed,auroc_text=roc_auc_score(y,pt),ap_text=average_precision_score(y,pt),brier_text=brier_score_loss(y,pt),
                         mean_p_text=pt.mean(),found_text=int(y[np.argsort(-pt)[:k]].sum()),auroc_len=roc_auc_score(y,pl),found_len=int(y[np.argsort(-pl)[:k]].sum())))
R=pd.DataFrame(rows); R.to_csv("screening_reproduction.csv",index=False)
print(f"matched {len(y)}, disagreements {y.sum()} ({y.mean():.4f}); budget {k}; constant Brier {y.mean()*(1-y.mean()):.4f}")
print(R.groupby("class_weight")[["auroc_text","ap_text","brier_text","mean_p_text","found_text","auroc_len","found_len"]].agg(["min","max"]).round(3).T.to_string())
