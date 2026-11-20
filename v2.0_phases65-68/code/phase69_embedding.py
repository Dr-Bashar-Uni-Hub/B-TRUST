"""Phase 69 — model-class robustness with spaCy en_core_web_lg mean vectors (preregistered amendment sha256 61c720d7...)."""
import numpy as np, pandas as pd, itertools, warnings, spacy
from scipy.stats import spearmanr
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import cohen_kappa_score
import corpora as C
warnings.filterwarnings("ignore")
nlp=spacy.load("en_core_web_lg",disable=["parser","ner","lemmatizer","tagger","attribute_ruler","senter"])
cache={}
def emb(texts):
    out=[]; todo=[t for t in dict.fromkeys(texts) if t not in cache]
    for t,d in zip(todo,nlp.pipe(todo,batch_size=256)): cache[t]=d.vector
    return np.vstack([cache[t] for t in texts])
mk=lambda: make_pipeline(StandardScaler(),LogisticRegression(C=1.0,max_iter=2000))
corp={"EDUB":C.edub(),"DASQ":C.dasq(),"SCAR-I":C.scar_i(),"SCAR-E":C.scar_e(),"EDUQG":C.eduqg()}
yq,V=C.youleqd(); lk=C.lak()
def lookup_cv(key,y,seed=65):
    p=np.zeros(len(y),int); maj=pd.Series(y).mode()[0]
    for a,b in StratifiedKFold(5,shuffle=True,random_state=seed).split(key,y):
        t=pd.DataFrame({"k":key[a],"y":y[a]}).groupby("k").y.agg(lambda s:s.mode()[0]); p[b]=pd.Series(key[b]).map(t).fillna(maj).astype(int).to_numpy()
    return p
g0=[]
for nm,d in corp.items():
    X=emb(list(d.n)); y=d.y.to_numpy(); p=np.zeros(len(y),int)
    for a,b in StratifiedKFold(5,shuffle=True,random_state=65).split(X,y): p[b]=mk().fit(X[a],y[a]).predict(X[b])
    acc=(p==y).mean(); maj=pd.Series(y).value_counts(normalize=True).iloc[0]
    meta=(lookup_cv(d.meta.to_numpy(),y)==y).mean() if "meta" in d else np.nan
    lift=acc-np.nanmax([maj,meta]); k=cohen_kappa_score(y,p)
    gate="FAIL" if (lift<0.05 or k<0.20) else ("PASS" if (lift>=0.15 and k>=0.40) else "CAUTION")
    g0.append(dict(corpus=nm,cv_acc_emb=acc,G0_lift_emb=lift,kappa_cv_emb=k,G0_emb=gate))
G=pd.DataFrame(g0); tf=pd.read_csv("p65_gates_G0.csv")[["corpus","G0_lift","G0"]]; G=G.merge(tf,on="corpus")
G["same_decision"]=G.G0==G.G0_emb; G.to_csv("p69_G0_embedding.csv",index=False); print(G.round(4).to_string(index=False))
targets={"DASQ":corp["DASQ"],"SCAR-E":corp["SCAR-E"],"EDUQG":corp["EDUQG"]}; rows=[]; preds={}
for tr,d in corp.items():
    m=mk().fit(emb(list(d.n)),d.y.to_numpy()); ts=set(d.n); acc={}
    for tn,t in targets.items():
        if tn==tr or {tr,tn}=={"SCAR-I","SCAR-E"}: continue
        keep=~t.n.isin(ts); acc[tn]=(m.predict(emb(list(t.n[keep])))==t.y[keep].to_numpy()).mean()
    pq=m.predict(emb(list(yq.n))); preds[tr]=pq; acc["YLQ70"]=(pq==yq.y.to_numpy()).mean()
    acc["LAK40"]=np.mean([a in s for a,s in zip(m.predict(emb(list(lk.n))),lk.refs)])
    rows.append(dict(train=tr,**acc,T_mean=np.mean(list(acc.values()))))
M=pd.DataFrame(rows).merge(G[["corpus","G0_lift_emb"]].rename(columns={"corpus":"train"}),on="train"); M.to_csv("p69_transfer_embedding.csv",index=False)
print(M.round(4).to_string(index=False))
obs=spearmanr(M.G0_lift_emb,M.T_mean).statistic; perm=[spearmanr(M.G0_lift_emb,np.array(p)).statistic for p in itertools.permutations(M.T_mean)]
pv=np.mean(np.array(perm)>=obs-1e-12)
print(f"H8a rho = {obs:.3f}, exact one-sided p = {pv:.4f}, supported = {pv<0.05}")
print("H8b identical G0 decisions for all 5 corpora:", bool(G.same_decision.all()))
# secondary: DASQ-trained vote loss on YouLeQD, embedding vs TF-IDF
vl=lambda p: np.nanmean(np.where(np.isnan(V),1.0,(V!=p[:,None]).astype(float)),1)
tfm=C.model().fit(corp["DASQ"].n,corp["DASQ"].y); d=vl(preds["DASQ"])-vl(tfm.predict(yq.n))
g=pd.Series(d).groupby(yq.vid.values); s=g.sum().to_numpy(); c=g.size().to_numpy(); rg=np.random.default_rng(69)
bs=[s[i].sum()/c[i].sum() for i in (rg.integers(0,len(s),len(s)) for _ in range(10000))]
print(f"Secondary: DASQ-trained YouLeQD G6 vote loss emb={vl(preds['DASQ']).mean():.4f} tfidf={vl(tfm.predict(yq.n)).mean():.4f} diff={d.mean():+.4f} CI [{np.percentile(bs,2.5):+.4f},{np.percentile(bs,97.5):+.4f}]")
print("Secondary: any corpus beats YouLeQD majority 0.3714 under M_emb:", {k:round(v,4) for k,v in zip(M.train,M.YLQ70)})
