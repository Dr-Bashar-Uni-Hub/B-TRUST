"""Independent review of Phase 75 conditional permutation tests.
Original method: residualise ranks of x and y on ranks of covariates Z, then permute y-residuals directly (permuted residuals are not
orthogonal to Z -> null not the correct reference). Freedman–Lane (1983): permute reduced-model residuals of y, add back fitted values,
re-residualise on Z, recompute the partial correlation. Exact over all 8! permutations. Also Holm across the 12 partial tests."""
import numpy as np, pandas as pd, itertools
from scipy.stats import rankdata
D=pd.read_csv("/home/claude/p75/p75_diagnostics.csv",index_col=0); K=list(D.index)
p71=pd.read_csv("/home/claude/p71/p71_gates_transfer.csv"); v73=pd.read_csv("/home/claude/p73res/v73_recomputed.csv")
T={"tfidf":p71[p71.model=="tfidf"].set_index("train")["T"],"emb":p71[p71.model=="emb"].set_index("train")["T"],
   "distilbert":v73[v73.model=="distilbert"].set_index("train")["T"],"roberta":v73[v73.model=="roberta"].set_index("train")["T"]}
G0={"tfidf":p71[p71.model=="tfidf"].set_index("train").G0_lift,"emb":p71[p71.model=="emb"].set_index("train").G0_lift,
    "distilbert":v73[v73.model=="distilbert"].set_index("train").G0_lift,"roberta":v73[v73.model=="roberta"].set_index("train").G0_lift}
covs={"log size":[np.log(D.n.loc[K].values)],"majority share":[D.majority_share.loc[K].values],"both":[np.log(D.n.loc[K].values),D.majority_share.loc[K].values]}
perms=np.array(list(itertools.permutations(range(8))))
def design(Z): return np.column_stack([np.ones(8)]+[rankdata(z) for z in Z])
def resid(v,X): return v-X@np.linalg.lstsq(X,v,rcond=None)[0]
def stat(x,y,X):
    ex,ey=resid(x,X),resid(y,X); return np.corrcoef(ex,ey)[0,1]
rows=[]
for m in T:
    x=rankdata(G0[m].loc[K].values); y=rankdata(T[m].loc[K].values)
    for cname,Z in covs.items():
        X=design(Z); obs=stat(x,y,X); ex,ey=resid(x,X),resid(y,X)
        p_orig=np.mean([np.corrcoef(ex,ey[p])[0,1]>=obs-1e-12 for p in perms])           # original (flawed) method
        fitted=y-ey
        fl=np.array([stat(x,fitted+ey[p],X) for p in perms]); p_fl=np.mean(fl>=obs-1e-12)  # Freedman–Lane
        rows.append(dict(model=m,control=cname,partial_rho=obs,p_original=p_orig,p_freedman_lane=p_fl,resid_df=8-X.shape[1]-1))
R=pd.DataFrame(rows)
o=np.argsort(R.p_freedman_lane.values); adj=np.empty(len(R)); run=0
for r,i in enumerate(o): run=max(run,(len(R)-r)*R.p_freedman_lane.values[i]); adj[i]=min(1,run)
R["p_FL_holm12"]=adj; R.to_csv("p75_review_freedman_lane.csv",index=False)
pd.set_option("display.width",200); print(R.round(4).to_string(index=False))
# Collinearity diagnostics
print("\nSpearman between covariates and G0 (k=8):")
for m in T:
    g=rankdata(G0[m].loc[K].values)
    print(f"  {m:10s} rho(G0, log n)={np.corrcoef(g,rankdata(np.log(D.n.loc[K].values)))[0,1]:+.2f}  rho(G0, majority share)={np.corrcoef(g,rankdata(D.majority_share.loc[K].values))[0,1]:+.2f}")
