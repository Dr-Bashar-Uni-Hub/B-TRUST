"""Phase 70 LLM validation, part 3: raw vote audit; paired comparisons vs models with item-level YouLeQD predictions; transformer comparability."""
import numpy as np, pandas as pd, joblib, re, corpora as C
from scipy.stats import binomtest
EX=C.EX; D=pd.read_csv("p70_llm_detailed.csv"); yq,V=C.youleqd(); vid=yq.vid.to_numpy(); y=yq.y.to_numpy()
r=pd.read_csv(f"{EX}/Phase42_Results/phase42/record_level_predictions.csv")
for c in ["label","lebel1","lebel2","lebel3"]: r[c]=r[c].astype(str).str.strip().str.lower()
rel=r[r.label!="irrelevant"].reset_index(drop=True); assert (rel.text.fillna("").str.strip()==yq.text.str.strip()).all()
raw=rel[["lebel1","lebel2","lebel3"]].stack(); print("non-Bloom raw votes on the 70 items:",raw[~raw.isin(C.ORIG)].value_counts().to_dict())
L2={f"l{i}":i for i in range(1,7)}; L2.update({f"L{i}":i for i in range(1,7)})
P={"Claude (zero-shot)":D[D.dataset=="YLQ70"].prediction.to_numpy(),
   "Frozen EduBloom LR":rel.lr_prediction.map(lambda s:int(str(s)[1])).to_numpy(),
   "Frozen EduBloom DistilBERT":rel.distilbert_prediction.map(lambda s:int(str(s)[1])).to_numpy(),
   "Constant comprehension":np.full(70,2)}
m=joblib.load("/home/claude/p58/p60_das_lr_model.joblib"); P["DASQBT TF-IDF LR (Phase 60)"]=pd.Series(m.predict(yq.n)).map(C.ORIG).to_numpy()
vl=lambda p: np.nanmean(np.where(np.isnan(V),1.0,(V!=np.asarray(p)[:,None]).astype(float)),1)
def boot(d,seed=70,B=10000):
    g=pd.Series(d).groupby(vid); s=g.sum().to_numpy(); c=g.size().to_numpy(); rb=np.random.default_rng(seed)
    bs=[s[i].sum()/c[i].sum() for i in (rb.integers(0,len(s),len(s)) for _ in range(B))]; return np.percentile(bs,[2.5,97.5])
rows=[]; cl=vl(P["Claude (zero-shot)"]); ca=(P["Claude (zero-shot)"]==y)
for k,p in P.items():
    if k.startswith("Claude"): continue
    d=cl-vl(p); lo,hi=boot(d); a=(p==y); b=int((ca&~a).sum()); c=int((~ca&a).sum())
    rows.append(dict(comparator=k,comp_voteloss=vl(p).mean(),comp_acc=a.mean(),claude_minus_comp=d.mean(),ci_lo=lo,ci_hi=hi,mcnemar_b=b,mcnemar_c=c,mcnemar_p=binomtest(b,b+c).pvalue if b+c else 1.0))
R=pd.DataFrame(rows).sort_values("ci_hi")
# Holm across the four vote-loss comparisons, using bootstrap p (two-sided, from percentile inversion is not available) -> report Holm on McNemar p
pv=R.mcnemar_p.to_numpy(); o=np.argsort(pv); adj=np.empty(len(pv)); run=0
for rank,i in enumerate(o): run=max(run,(len(pv)-rank)*pv[i]); adj[i]=min(1,run)
R["mcnemar_p_holm"]=adj; print(f"Claude: vote loss {cl.mean():.4f}, accuracy {ca.mean():.4f}"); print(R.round(4).to_string(index=False)); R.to_csv("val_paired_comparisons.csv",index=False)
# Transformer comparability (Phase 70 files; no item-level predictions)
rows=[]
for mdl in ["distilbert","roberta"]:
    T=pd.read_csv(f"/home/claude/p70res/p70_transfer_{mdl}.csv")
    for _,t in T.iterrows(): rows.append(dict(model=mdl,train=t.train,YLQ70_correct=round(t.YLQ70*70),LAK40_correct=round(t.LAK40*40),DASQ=t.DASQ,SCAR_E=t["SCAR-E"],EDUQG=t.EDUQG))
T=pd.DataFrame(rows); print(T.round(3).to_string(index=False)); print("Claude: YLQ70 34/70, LAK40 29/40, DASQ 0.698 (500-sample), SCAR-E 0.806 (500-sample), EDUQG 0.690 (all 903)")
T.to_csv("val_transformer_side_by_side.csv",index=False)
