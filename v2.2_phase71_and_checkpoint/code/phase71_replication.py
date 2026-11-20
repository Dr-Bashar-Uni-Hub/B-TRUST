"""Phase 71 — H11a/H11b: k = 8 replication (preregistered sha256 e66af025...)."""
import numpy as np, pandas as pd, itertools, warnings, re, spacy
from scipy.stats import spearmanr
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import cohen_kappa_score
import corpora as C
warnings.filterwarnings("ignore")
REV={"remember":1,"understand":2,"apply":3,"analyze":4,"evaluate":5,"create":6}
def faraji(f):
    d=pd.read_csv(f); d=pd.DataFrame({"text":d.QUESTION,"y":d["BT LEVEL"].str.strip().str.lower().map(REV)})
    d=d[d.text.map(lambda s:isinstance(s,str) and s.strip()!="")].copy(); d["n"]=d.text.map(C.norm); return d.drop_duplicates("n").reset_index(drop=True)
corp={"EDUB":C.edub(),"YAHYA":faraji("yahya-2012_revised.csv"),"SANGO":faraji("Sangodiah_2017_415_revised.csv"),
      "MOHOM":faraji("Mohammed-and-Omar_2020_126_revised.csv"),"GANI":faraji("Gani_2023_collected-dataset-1200_revised.csv"),
      "SCAR-I":C.scar_i(),"SCAR-E":C.scar_e(),"EDUQG":C.eduqg()}
yq,_=C.youleqd(); lk=C.lak(); print({k:len(v) for k,v in corp.items()})
TG=["YAHYA","SANGO","MOHOM","GANI","SCAR-E","EDUQG"]
nlp=spacy.load("en_core_web_lg",disable=["parser","ner","lemmatizer","tagger","attribute_ruler","senter"]); cache={}
def emb(t):
    todo=[x for x in dict.fromkeys(t) if x not in cache]
    for x,d in zip(todo,nlp.pipe(todo,batch_size=256)): cache[x]=d.vector
    return np.vstack([cache[x] for x in t])
MODELS={"tfidf":(lambda:C.model(),lambda t:np.asarray(t)),
        "emb":(lambda:make_pipeline(StandardScaler(),LogisticRegression(C=1.0,max_iter=2000)),lambda t:emb(list(t)))}
def lookup_cv(key,y):
    p=np.zeros(len(y),int); maj=pd.Series(y).mode()[0]
    for a,b in StratifiedKFold(5,shuffle=True,random_state=65).split(key,y):
        t=pd.DataFrame({"k":key[a],"y":y[a]}).groupby("k").y.agg(lambda s:s.mode()[0]); p[b]=pd.Series(key[b]).map(t).fillna(maj).astype(int).to_numpy()
    return p
majrate={k:corp[k].y.value_counts(normalize=True).iloc[0] for k in TG}; majrate["YLQ70"]=yq.y.value_counts(normalize=True).iloc[0]; majrate["LAK40"]=8/40
def exact(x,y):
    obs=spearmanr(x,y).statistic; c=0; n=0
    for p in itertools.permutations(y):
        n+=1; c+=spearmanr(x,np.array(p)).statistic>=obs-1e-12
    return obs,c/n
allrows=[]; summary=[]
for mname,(mk,fx) in MODELS.items():
    rows=[]
    for c,d in corp.items():
        X=fx(d.n); y=d.y.to_numpy(); p=np.zeros(len(y),int)
        for a,b in StratifiedKFold(5,shuffle=True,random_state=65).split(X,y): p[b]=mk().fit(X[a],y[a]).predict(X[b])
        acc=(p==y).mean(); maj=pd.Series(y).value_counts(normalize=True).iloc[0]
        meta=(lookup_cv(d.meta.to_numpy(),y)==y).mean() if "meta" in d else np.nan
        lift=acc-np.nanmax([maj,meta]); k=cohen_kappa_score(y,p)
        gate="FAIL" if (lift<.05 or k<.20) else ("PASS" if (lift>=.15 and k>=.40) else "CAUTION")
        m=mk().fit(X,y); ts=set(d.n); accs={}; skill={}
        for tn in TG:
            if tn==c or {c,tn}=={"SCAR-I","SCAR-E"}: continue
            t=corp[tn]; keep=~t.n.isin(ts); a_=(m.predict(fx(t.n[keep]))==t.y[keep].to_numpy()).mean(); accs[tn]=a_; skill[tn]=a_-majrate[tn]
        accs["YLQ70"]=(m.predict(fx(yq.n))==yq.y.to_numpy()).mean(); skill["YLQ70"]=accs["YLQ70"]-majrate["YLQ70"]
        accs["LAK40"]=np.mean([a in s for a,s in zip(m.predict(fx(lk.n)),lk.refs)]); skill["LAK40"]=accs["LAK40"]-majrate["LAK40"]
        rows.append(dict(model=mname,train=c,n=len(y),cv_acc=acc,G0_lift=lift,kappa_cv=k,G0=gate,
                         levels_ge30=int((pd.Series(y).value_counts()>=30).sum()),T=np.mean(list(accs.values())),T_skill=np.mean(list(skill.values())),
                         **{f"acc_{k_}":v for k_,v in accs.items()}))
    R=pd.DataFrame(rows); allrows.append(R); print(R.drop(columns=[c for c in R if c.startswith("acc_")]).round(4).to_string(index=False))
    rho,p=exact(R.G0_lift.to_numpy(),R["T"].to_numpy()); rs,ps=exact(R.G0_lift.to_numpy(),R.T_skill.to_numpy())
    R7=R[R.train!="SCAR-I"]; r7,p7=exact(R7.G0_lift.to_numpy(),R7["T"].to_numpy())
    summary.append(dict(model=mname,rho_T=rho,p_T=p,supported=p<0.05,rho_Tskill=rs,p_Tskill=ps,rho_k7=r7,p_k7=p7,
                        any_beats_YLQ_majority=bool((R.acc_YLQ70>majrate["YLQ70"]).any())))
    print(summary[-1])
A=pd.concat(allrows); A.to_csv("p71_gates_transfer.csv",index=False)
dec=A.pivot(index="train",columns="model",values="G0"); dec["same"]=dec.tfidf==dec.emb; print(dec)
S=pd.DataFrame(summary); S.to_csv("p71_tests.csv",index=False); print(S.round(4).to_string(index=False))
