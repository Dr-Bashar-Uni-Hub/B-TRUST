"""Phase 70 LLM validation, part 2: H10 reproduction, best-constant check, missing/irrelevant-vote treatment, robustness."""
import numpy as np, pandas as pd, corpora as C
from scipy.stats import binomtest
D=pd.read_csv("p70_llm_detailed.csv"); S=pd.read_csv("p70_llm.csv").iloc[0]
yq,V=C.youleqd(); g=D[D.dataset=="YLQ70"].reset_index(drop=True); assert (g.question.str.strip()==yq.text.str.strip()).all()
pq=g.prediction.to_numpy(); vid=yq.vid.to_numpy()
print("vote matrix: NaN (irrelevant/missing) votes per item:",np.bincount(np.isnan(V).sum(1)).tolist(),"| total NaN votes",int(np.isnan(V).sum()))
def vl_pre(p): return np.nanmean(np.where(np.isnan(V),1.0,(V!=np.asarray(p)[:,None]).astype(float)),1)   # preregistered: NaN vote = loss
def vl_bloom(p): M=~np.isnan(V); return ((V!=np.asarray(p)[:,None])&M).sum(1)/M.sum(1)                   # alt: Bloom votes only
def boot(d,seed=70,B=10000,cluster=True):
    if cluster:
        gg=pd.Series(d).groupby(vid); s=gg.sum().to_numpy(); c=gg.size().to_numpy(); rb=np.random.default_rng(seed)
        bs=[s[i].sum()/c[i].sum() for i in (rb.integers(0,len(s),len(s)) for _ in range(B))]
    else:
        rb=np.random.default_rng(seed); bs=[d[rb.integers(0,len(d),len(d))].mean() for _ in range(B)]
    return d.mean(),np.percentile(bs,2.5),np.percentile(bs,97.5)
# 1. exact reproduction of the reported H10
d=vl_pre(pq)-vl_pre(np.full(70,2)); est,lo,hi=boot(d)
print(f"H10 reproduced: LLM {vl_pre(pq).mean():.6f} (reported {S.ylq_voteloss:.6f}); const {vl_pre(np.full(70,2)).mean():.6f} (reported {S.ylq_constantloss:.6f}); "
      f"diff {est:+.6f} CI [{lo:+.6f},{hi:+.6f}] (reported [{S.h10_ci_lo:+.6f},{S.h10_ci_hi:+.6f}])")
# 2. best constant under each loss
for nm,f in [("prereg (irrelevant vote = loss)",vl_pre),("Bloom votes only",vl_bloom)]:
    cl={k:f(np.full(70,k)).mean() for k in range(1,7)}; print(f"constants under {nm}:",{k:round(v,4) for k,v in cl.items()},"-> best",min(cl,key=cl.get))
# 3. robustness grid
rows=[]
for nm,f in [("prereg: irrelevant vote = loss",vl_pre),("Bloom votes only",vl_bloom)]:
    best=min(range(1,7),key=lambda k:f(np.full(70,k)).mean())
    for cl in [True,False]:
        d=f(pq)-f(np.full(70,best)); est,lo,hi=boot(d,cluster=cl)
        rows.append(dict(loss=nm,baseline=f"best constant ({best})",bootstrap="video-cluster" if cl else "item",diff=est,ci_lo=lo,ci_hi=hi,supported=hi<0))
y=yq.y.to_numpy(); corr=(pq==y).astype(float); cc=(y==2).astype(float)
b=int(((corr==1)&(cc==0)).sum()); c=int(((corr==0)&(cc==1)).sum()); est,lo,hi=boot(cc-corr)
rows.append(dict(loss="consolidated-label error",baseline="constant comprehension",bootstrap="video-cluster",diff=est,ci_lo=lo,ci_hi=hi,supported=hi<0,
                 note=f"acc {corr.sum():.0f}/70 vs {cc.sum():.0f}/70; McNemar b={b} c={c} exact p={binomtest(b,b+c).pvalue:.4f}"))
for seed in [1,2,3]:
    est,lo,hi=boot(vl_pre(pq)-vl_pre(np.full(70,2)),seed=seed); rows.append(dict(loss="prereg",baseline="const 2",bootstrap=f"video-cluster seed {seed}",diff=est,ci_lo=lo,ci_hi=hi,supported=hi<0))
R=pd.DataFrame(rows); pd.set_option("display.width",250); print(R.round(4).to_string(index=False)); R.to_csv("val_h10_robustness.csv",index=False)
# 4. human reference and coarse granularities (exploratory)
H=np.nanmean(np.array([np.where(np.isnan(V[:,j])|np.isnan(V[:,k]),np.where(np.isnan(V[:,j])&np.isnan(V[:,k]),0.0,1.0),(V[:,j]!=V[:,k]).astype(float)) for j in range(3) for k in range(3) if j!=k]),0)
est,lo,hi=boot(vl_pre(pq)-H); print(f"EXPLORATORY LLM minus human leave-one-out (G6): {vl_pre(pq).mean():.4f} vs {H.mean():.4f}; diff {est:+.4f} CI [{lo:+.4f},{hi:+.4f}]")
for gname,m in [("G3",lambda v:np.ceil(v/2)),("G2",lambda v:np.where(v>=4,2.0,1.0))]:
    Vc=np.where(np.isnan(V),np.nan,m(np.nan_to_num(V,nan=1))); pc=m(pq)
    f=lambda p: np.nanmean(np.where(np.isnan(Vc),1.0,(Vc!=np.asarray(p)[:,None]).astype(float)),1)
    best=min(np.unique(m(np.arange(1,7))),key=lambda k:f(np.full(70,k)).mean()); est,lo,hi=boot(f(pc)-f(np.full(70,best)))
    print(f"EXPLORATORY {gname}: LLM {f(pc).mean():.4f} vs best constant {f(np.full(70,best)).mean():.4f}; diff {est:+.4f} CI [{lo:+.4f},{hi:+.4f}]")
