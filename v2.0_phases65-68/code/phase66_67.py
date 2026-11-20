"""Phase 66 (H5) and Phase 67 (H6) — preregistered."""
import numpy as np, pandas as pd, warnings
from scipy.stats import binomtest
from sklearn.model_selection import StratifiedKFold
import corpora as C
warnings.filterwarnings("ignore")
dq=C.dasq(); eq=C.eduqg(); yq,V=C.youleqd(); lk=C.lak()
def evaluate(m,trainset):
    out={}
    for nm,d in [("DASQ",dq),("EDUQG",eq)]:
        keep=~d.n.isin(trainset); out[nm]=(m.predict(d.n[keep])==d.y[keep].to_numpy()).astype(float); out[nm+"_keep"]=keep.to_numpy()
    p=m.predict(yq.n); out["YLQ_voteloss"]=np.nanmean(np.where(np.isnan(V),1.0,(V!=p[:,None]).astype(float)),1)
    out["YLQ_acc"]=(p==yq.y.to_numpy()).astype(float)
    pl=m.predict(lk.n); out["LAK"]=np.array([a in s for a,s in zip(pl,lk.refs)],float)
    return out
def boot(diff,B=10000,seed=0):
    rg=np.random.default_rng(seed); n=len(diff); s=np.array([diff[rg.integers(0,n,n)].mean() for _ in range(B)])
    return diff.mean(),np.percentile(s,2.5),np.percentile(s,97.5)
def summ(tag,o): return dict(condition=tag,DASQ=o["DASQ"].mean(),EDUQG=o["EDUQG"].mean(),YLQ_voteloss=o["YLQ_voteloss"].mean(),YLQ_acc=o["YLQ_acc"].mean(),LAK=o["LAK"].mean())
res=[]
# ---------- Phase 66: same texts (set E), two label sources ----------
s=C.scaria_raw(); E=s[s.consensus.notna()].reset_index(drop=True); tr=set(E.n)
mI=C.model().fit(E.n,E.intended); mE=C.model().fit(E.n,E.consensus.astype(int))
oI=evaluate(mI,tr); oE=evaluate(mE,tr)
print("Set E size",len(E)," label disagreement intended vs consensus:",round((E.intended!=E.consensus).mean(),4))
res+= [summ("P66_M_I_intended_on_E",oI),summ("P66_M_E_expert_on_E",oE)]
d=oE["DASQ"]-oI["DASQ"]; est,lo,hi=boot(d,seed=66)
b=int(((oE["DASQ"]==1)&(oI["DASQ"]==0)).sum()); c=int(((oE["DASQ"]==0)&(oI["DASQ"]==1)).sum())
h5=dict(test="H5 acc(M_E)-acc(M_I) on DASQ",est=est,ci_lo=lo,ci_hi=hi,mcnemar_b=b,mcnemar_c=c,mcnemar_p=binomtest(b,b+c).pvalue if b+c else 1,supported=lo>0)
print("H5:",{k:(round(v,4) if isinstance(v,float) else v) for k,v in h5.items()})
# ---------- Phase 67: filtering experiment on intended labels ----------
S=s.reset_index(drop=True); X=S.n.to_numpy(); y=S.intended.to_numpy(); trS=set(S.n)
prov=(S.consensus.notna()&(S.consensus==S.intended)).to_numpy(); nP=int(prov.sum())
oALL=evaluate(C.model().fit(X,y),trS); oPROV=evaluate(C.model().fit(X[prov],y[prov]),trS)
rg=np.random.default_rng(67); R=[]
for k in range(20):
    idx=rg.choice(len(X),nP,replace=False); R.append(evaluate(C.model().fit(X[idx],y[idx]),trS))
oRAND={k:np.mean([r[k] for r in R],0) for k in R[0] if not k.endswith("_keep")}
# confident learning (per-class threshold on OOF self-confidence)
P=np.zeros((len(X),6))
for a,bb in StratifiedKFold(5,shuffle=True,random_state=67).split(X,y):
    m=C.model().fit(X[a],y[a]); P[bb]=m.predict_proba(X[bb])
self_conf=P[np.arange(len(y)),y-1]; thr=pd.Series(self_conf).groupby(y).transform("mean").to_numpy()
cl=self_conf>=thr; oCL=evaluate(C.model().fit(X[cl],y[cl]),trS)
cli=np.where(cl)[0]; CLm=[]
for k in range(20):
    idx=rg.choice(cli,min(nP,len(cli)),replace=False); CLm.append(evaluate(C.model().fit(X[idx],y[idx]),trS))
oCLm={k:np.mean([r[k] for r in CLm],0) for k in CLm[0] if not k.endswith("_keep")}
print(f"PROV n={nP}  CL kept {cl.sum()}  overlap PROV&CL {int((prov&cl).sum())}")
for tag,o in [("P67_ALL",oALL),("P67_PROV",oPROV),("P67_RAND(mean20)",oRAND),("P67_CL",oCL),("P67_CLm(mean20)",oCLm)]: res.append(summ(tag,o))
tests=[h5]
for tag,a,bb,seed,prim in [("H6 PROV-RAND",oPROV,oRAND,67,True),("PROV-CLm",oPROV,oCLm,671,False),("PROV-ALL",oPROV,oALL,672,False),("CL-ALL",oCL,oALL,673,False)]:
    est,lo,hi=boot(a["DASQ"]-bb["DASQ"],seed=seed); tests.append(dict(test=tag+" on DASQ",est=est,ci_lo=lo,ci_hi=hi,supported=(lo>0) if prim else None))
r=pd.DataFrame(res); r.to_csv("p66_67_conditions.csv",index=False); t=pd.DataFrame(tests); t.to_csv("p66_67_tests.csv",index=False)
print(r.round(4).to_string(index=False)); print(t.round(4).to_string(index=False))
