"""Phase 65 — framework gates G0, G0b, G1, G3 for all corpora (preregistered)."""
import numpy as np, pandas as pd, warnings
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import cohen_kappa_score
import corpora as C
warnings.filterwarnings("ignore")
def cv_pred(X,y,seed=65):
    p=np.zeros(len(y),int)
    for a,b in StratifiedKFold(5,shuffle=True,random_state=seed).split(X,y):
        p[b]=C.model().fit(X[a],y[a]).predict(X[b])
    return p
def lookup_cv(key,y,seed=65):
    p=np.zeros(len(y),int); maj=pd.Series(y).mode()[0]
    for a,b in StratifiedKFold(5,shuffle=True,random_state=seed).split(key,y):
        t=pd.DataFrame({"k":key[a],"y":y[a]}).groupby("k").y.agg(lambda s:s.mode()[0])
        p[b]=pd.Series(key[b]).map(t).fillna(maj).astype(int).to_numpy()
    return p
rows=[]
for name,f in [("EDUB",C.edub),("DASQ",C.dasq),("SCAR-I",C.scar_i),("SCAR-E",C.scar_e),("EDUQG",C.eduqg)]:
    d=f(); X=d.n.to_numpy(); y=d.y.to_numpy()
    p=cv_pred(X,y); acc=(p==y).mean(); maj=pd.Series(y).value_counts(normalize=True).iloc[0]
    meta=(lookup_cv(d.meta.to_numpy(),y)==y).mean() if "meta" in d else np.nan
    fw=(lookup_cv(d.n.str.split().str[0].fillna("").to_numpy(),y)==y).mean()
    ref=np.nanmax([maj,meta]); lift=acc-ref; k=cohen_kappa_score(y,p)
    gate="FAIL" if (lift<0.05 or k<0.20) else ("PASS" if (lift>=0.15 and k>=0.40) else "CAUTION")
    cov=int((pd.Series(y).value_counts()>=30).sum())
    rows.append(dict(corpus=name,n=len(y),cv_acc=acc,majority=maj,metadata_only=meta,first_word=fw,G0_lift=lift,kappa_cv=k,G0=gate,G0b_levels_ge30=cov))
g=pd.DataFrame(rows); g.to_csv("p65_gates_G0.csv",index=False); print(g.round(4).to_string(index=False))
# G1 and G3 on Scaria (2 experts, generator label)
s=C.scaria_raw(); both=s[s.e1.notna()&s.e2.notna()]
e1,e2,it=both.e1.astype(int).to_numpy(),both.e2.astype(int).to_numpy(),both.intended.to_numpy()
G3={6:lambda v:v,3:lambda v:(v+1)//2,2:lambda v:(v>=4).astype(int)+1}
out=[]
for g_,m in G3.items():
    a,b,i=m(e1),m(e2),m(it)
    out.append(dict(granularity=f"G{g_}",n=len(a),expert_expert_exact=(a==b).mean(),expert_expert_kappa=cohen_kappa_score(a,b),
                    expert_expert_adjacent=(np.abs(e1-e2)<=1).mean() if g_==6 else np.nan,
                    generator_vs_e1_kappa=cohen_kappa_score(i,a),generator_vs_e2_kappa=cohen_kappa_score(i,b),
                    generator_vs_e1_exact=(i==a).mean(),generator_vs_e2_exact=(i==b).mean()))
h=pd.DataFrame(out); h.to_csv("p65_G1_G3_scaria.csv",index=False); print("\nScaria items rated by both experts:",len(both)); print(h.round(4).to_string(index=False))
print("\nG1 provenance ratio (mean generator-expert kappa / expert-expert kappa, G6):",
      round((h.loc[0,'generator_vs_e1_kappa']+h.loc[0,'generator_vs_e2_kappa'])/2/h.loc[0,'expert_expert_kappa'],3))
