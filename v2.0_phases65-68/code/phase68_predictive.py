"""Phase 68 — H7: do gate scores predict transfer across training corpora? (preregistered, k=5)"""
import numpy as np, pandas as pd, itertools, warnings
from scipy.stats import spearmanr
import corpora as C
warnings.filterwarnings("ignore")
corp={"EDUB":C.edub(),"DASQ":C.dasq(),"SCAR-I":C.scar_i(),"SCAR-E":C.scar_e(),"EDUQG":C.eduqg()}
yq,_=C.youleqd(); lk=C.lak()
targets={"DASQ":corp["DASQ"],"SCAR-E":corp["SCAR-E"],"EDUQG":corp["EDUQG"]}
rows=[]
for tr,d in corp.items():
    m=C.model().fit(d.n,d.y); ts=set(d.n); acc={}
    for tn,t in targets.items():
        if tn==tr or {tr,tn}=={"SCAR-I","SCAR-E"}: continue
        keep=~t.n.isin(ts); acc[tn]=(m.predict(t.n[keep])==t.y[keep].to_numpy()).mean()
    acc["YLQ70"]=(m.predict(yq.n)==yq.y.to_numpy()).mean()
    acc["LAK40"]=np.mean([a in s for a,s in zip(m.predict(lk.n),lk.refs)])
    rows.append(dict(train=tr,**acc,T_mean=np.mean(list(acc.values()))))
M=pd.DataFrame(rows); g=pd.read_csv("p65_gates_G0.csv").rename(columns={"corpus":"train"})
M=M.merge(g[["train","G0_lift","kappa_cv","G0"]],on="train"); M.to_csv("p68_transfer_matrix.csv",index=False)
print(M.round(4).to_string(index=False))
def exact_perm(x,y):
    obs=spearmanr(x,y).statistic; perms=[spearmanr(x,np.array(p)).statistic for p in itertools.permutations(y)]
    return obs,np.mean(np.array(perms)>=obs-1e-12)
for gate in ["G0_lift","kappa_cv"]:
    rho,p=exact_perm(M[gate].to_numpy(),M.T_mean.to_numpy()); print(f"H7 Spearman({gate}, T_mean) = {rho:.3f}, exact one-sided p = {p:.4f}")
# Exploratory: is transfer better explained by target being held-out human exam text? per-target ranking
print("\nPer-target accuracy minus target majority rate (skill over prior):")
maj={"DASQ":corp["DASQ"].y.value_counts(normalize=True).iloc[0],"SCAR-E":corp["SCAR-E"].y.value_counts(normalize=True).iloc[0],
     "EDUQG":corp["EDUQG"].y.value_counts(normalize=True).iloc[0],"YLQ70":yq.y.value_counts(normalize=True).iloc[0],"LAK40":8/40}
S=M.set_index("train")[[c for c in maj]].copy()
for c in maj: S[c]=S[c]-maj[c]
print(S.round(3).to_string()); S.to_csv("p68_skill_over_prior.csv")
