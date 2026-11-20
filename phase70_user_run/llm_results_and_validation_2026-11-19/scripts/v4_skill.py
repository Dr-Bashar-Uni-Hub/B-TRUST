"""Phase 70 LLM validation, part 4: Bonferroni CIs for paired vote-loss comparisons; skill over majority per dataset; prediction distributions."""
import numpy as np, pandas as pd, joblib, corpora as C
D=pd.read_csv("p70_llm_detailed.csv"); yq,V=C.youleqd(); vid=yq.vid.to_numpy()
r=pd.read_csv(f"{C.EX}/Phase42_Results/phase42/record_level_predictions.csv")
for c in ["label"]: r[c]=r[c].astype(str).str.strip().str.lower()
rel=r[r.label!="irrelevant"].reset_index(drop=True)
vl=lambda p: np.nanmean(np.where(np.isnan(V),1.0,(V!=np.asarray(p)[:,None]).astype(float)),1)
cl=vl(D[D.dataset=="YLQ70"].prediction.to_numpy())
comps={"Frozen EduBloom LR":rel.lr_prediction.map(lambda s:int(str(s)[1])).to_numpy(),"Frozen EduBloom DistilBERT":rel.distilbert_prediction.map(lambda s:int(str(s)[1])).to_numpy(),
       "Constant comprehension":np.full(70,2),"DASQBT TF-IDF LR":pd.Series(joblib.load("/home/claude/p58/p60_das_lr_model.joblib").predict(yq.n)).map(C.ORIG).to_numpy()}
rb=np.random.default_rng(70); g=pd.Series(np.arange(70)).groupby(vid).apply(list).tolist()
idx=[np.concatenate([g[i] for i in rb.integers(0,len(g),len(g))]) for _ in range(10000)]
for k,p in comps.items():
    d=cl-vl(p); bs=np.array([d[i].mean() for i in idx]); lo,hi=np.percentile(bs,[100*0.05/8,100*(1-0.05/8)])
    print(f"Bonferroni (4 comparisons) 98.75% CI, Claude minus {k}: [{lo:+.4f},{hi:+.4f}] excludes 0: {hi<0}")
rows=[]
for ds,gq in D.groupby("dataset",sort=False):
    if ds=="LAK40": continue
    yv=gq.reference_label.to_numpy(); corr=gq.correct.to_numpy().astype(float); maj=pd.Series(yv).value_counts(normalize=True)
    mc=(yv==maj.index[0]).astype(float); d=corr-mc
    if ds=="YLQ70": bs=[d[i].mean() for i in idx]
    else: rr=np.random.default_rng(70); bs=[d[rr.integers(0,len(d),len(d))].mean() for _ in range(10000)]
    lo,hi=np.percentile(bs,[2.5,97.5])
    rows.append(dict(dataset=ds,n=len(gq),accuracy=corr.mean(),majority_class=int(maj.index[0]),majority_rate=maj.iloc[0],skill=d.mean(),ci_lo=lo,ci_hi=hi,
                     pred_dist=gq.prediction.value_counts().sort_index().astype(int).to_dict(),ref_dist=pd.Series(yv).value_counts().sort_index().astype(int).to_dict()))
lak=D[D.dataset=="LAK40"]; print("LAK40: accuracy 0.725; reference sets are multi-label, majority baseline per Phase 68 convention 8/40 = 0.20")
R=pd.DataFrame(rows); pd.set_option("display.width",300); print(R.round(4).to_string(index=False)); R.to_csv("val_skill_over_majority.csv",index=False)
e=D[D.dataset=="EDUQG"]; print("EDUQG confusion (rows reference, cols prediction):"); print(pd.crosstab(e.reference_label,e.prediction))
