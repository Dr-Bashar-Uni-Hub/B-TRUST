"""Phase 75 (EXPLORATORY, not preregistered; uses existing outputs + cheap TF-IDF recomputation, no transformer training, no API).
(a) Partial Spearman of G0 lift vs transfer T controlling for log corpus size and majority-class share (k = 8; permutation p).
(b) Size-matched TF-IDF G0: each corpus subsampled to n = 126 (smallest corpus), 20 stratified-as-possible draws, vs T of each model class.
(c) Training-free diagnostic: first-word lookup lift (cross-validated lookup accuracy minus majority rate) vs T of each model class.
Also skill-over-majority transfer T' for the k = 8 transformers (checklist B3)."""
import numpy as np, pandas as pd, itertools, warnings, sys
from scipy.stats import spearmanr, rankdata
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import cohen_kappa_score
sys.path.insert(0,"/home/claude/p71"); import corpora as C
warnings.filterwarnings("ignore")
REV={"remember":1,"understand":2,"apply":3,"analyze":4,"evaluate":5,"create":6}
def faraji(f):
    d=pd.read_csv(f"/home/claude/p71/{f}"); d=pd.DataFrame({"text":d.QUESTION,"y":d["BT LEVEL"].str.strip().str.lower().map(REV)})
    d=d[d.text.map(lambda s:isinstance(s,str) and s.strip()!="")].copy(); d["n"]=d.text.map(C.norm); return d.drop_duplicates("n").reset_index(drop=True)
corp={"EDUB":C.edub(),"YAHYA":faraji("yahya-2012_revised.csv"),"SANGO":faraji("Sangodiah_2017_415_revised.csv"),"MOHOM":faraji("Mohammed-and-Omar_2020_126_revised.csv"),
      "GANI":faraji("Gani_2023_collected-dataset-1200_revised.csv"),"SCAR-I":C.scar_i(),"SCAR-E":C.scar_e(),"EDUQG":C.eduqg()}
K=list(corp)
# transfer T per model class
p71=pd.read_csv("/home/claude/p71/p71_gates_transfer.csv"); v73=pd.read_csv("/home/claude/p73res/v73_recomputed.csv")
T={"tfidf":p71[p71.model=="tfidf"].set_index("train")["T"],"emb":p71[p71.model=="emb"].set_index("train")["T"],
   "distilbert":v73[v73.model=="distilbert"].set_index("train")["T"],"roberta":v73[v73.model=="roberta"].set_index("train")["T"]}
G0={"tfidf":p71[p71.model=="tfidf"].set_index("train").G0_lift,"emb":p71[p71.model=="emb"].set_index("train").G0_lift,
    "distilbert":v73[v73.model=="distilbert"].set_index("train").G0_lift,"roberta":v73[v73.model=="roberta"].set_index("train").G0_lift}
size=pd.Series({k:len(v) for k,v in corp.items()}); majs=pd.Series({k:v.y.value_counts(normalize=True).iloc[0] for k,v in corp.items()})
def perm_p(x,y):  # exact one-sided Spearman
    obs=spearmanr(x,y).statistic; return obs,np.mean([spearmanr(x,np.array(q)).statistic>=obs-1e-12 for q in itertools.permutations(y)])
def partial(x,y,Z):  # partial Spearman via rank residuals; permutation of y-residual (one-sided)
    rx,ry=rankdata(x),rankdata(y); Zr=np.column_stack([np.ones(len(x))]+[rankdata(z) for z in Z])
    res=lambda v: v-Zr@np.linalg.lstsq(Zr,v,rcond=None)[0]; ex,ey=res(rx),res(ry); obs=np.corrcoef(ex,ey)[0,1]
    null=[np.corrcoef(ex,np.array(q))[0,1] for q in itertools.permutations(ey)]; return obs,np.mean(np.array(null)>=obs-1e-12)
rows=[]
for m in T:
    x=G0[m].loc[K].values; y=T[m].loc[K].values
    r,p=perm_p(x,y); rows.append(dict(model=m,analysis="G0 (own model) vs T, raw",rho=r,p=p))
    r,p=partial(x,y,[np.log(size.loc[K].values)]); rows.append(dict(model=m,analysis="partial | log size",rho=r,p=p))
    r,p=partial(x,y,[majs.loc[K].values]); rows.append(dict(model=m,analysis="partial | majority share",rho=r,p=p))
    r,p=partial(x,y,[np.log(size.loc[K].values),majs.loc[K].values]); rows.append(dict(model=m,analysis="partial | log size + majority share",rho=r,p=p))
    r,_=perm_p(np.log(size.loc[K].values),y); rows.append(dict(model=m,analysis="log size vs T (descriptive)",rho=r,p=np.nan))
    r,_=perm_p(-majs.loc[K].values,y); rows.append(dict(model=m,analysis="balance (−majority share) vs T (descriptive)",rho=r,p=np.nan))
# (b) size-matched TF-IDF G0 at n = 126
def cv_acc(X,y,seed):
    p=np.zeros(len(y),int); kf=StratifiedKFold(5,shuffle=True,random_state=seed)
    try: splits=list(kf.split(X,y))
    except ValueError: splits=list(StratifiedKFold(3,shuffle=True,random_state=seed).split(X,y))
    for a,b in splits:
        mdl=C.model(); mdl.fit(X[a],y[a]); p[b]=mdl.predict(X[b])
    return (p==y).mean(), cohen_kappa_score(y,p)
def lookup_cv(key,y):
    p=np.zeros(len(y),int); maj=pd.Series(y).mode()[0]
    for a,b in StratifiedKFold(5,shuffle=True,random_state=65).split(key,y):
        t=pd.DataFrame({"k":key[a],"y":y[a]}).groupby("k").y.agg(lambda s:s.mode()[0]); p[b]=pd.Series(key[b]).map(t).fillna(maj).astype(int).to_numpy()
    return p
sm={}
for k,d in corp.items():
    lifts=[]
    for s in range(20):
        rg=np.random.default_rng(750+s); idx=rg.choice(len(d),126,replace=False) if len(d)>126 else np.arange(len(d))
        X=d.n.to_numpy()[idx]; y=d.y.to_numpy()[idx]
        vc=pd.Series(y).value_counts(); keep=np.isin(y,vc[vc>=3].index); X,y=X[keep],y[keep]   # tiny classes cannot be stratified
        acc,_=cv_acc(X,y,s); maj=pd.Series(y).value_counts(normalize=True).iloc[0]
        meta=np.nan
        if "meta" in d:
            mm=d.meta.to_numpy()[idx][keep]; meta=(lookup_cv(mm,y)==y).mean()
        lifts.append(acc-np.nanmax([maj,meta]))
        if len(d)<=126: break
    sm[k]=np.mean(lifts)
sm=pd.Series(sm)
# (c) first-word lookup lift (no model training)
fw={}
for k,d in corp.items():
    y=d.y.to_numpy(); key=d.n.str.split().str[0].fillna("").to_numpy(); fw[k]=(lookup_cv(key,y)==y).mean()-max(pd.Series(y).value_counts(normalize=True).iloc[0], (lookup_cv(d.meta.to_numpy(),y)==y).mean() if "meta" in d else 0)
fw=pd.Series(fw)
for m in T:
    y=T[m].loc[K].values
    r,p=perm_p(sm.loc[K].values,y); rows.append(dict(model=m,analysis="size-matched TF-IDF G0 (n=126) vs T",rho=r,p=p))
    r,p=perm_p(fw.loc[K].values,y); rows.append(dict(model=m,analysis="first-word lookup lift (no training) vs T",rho=r,p=p))
R=pd.DataFrame(rows); R.to_csv("/home/claude/p75/p75_robustness.csv",index=False)
D=pd.DataFrame({"n":size,"majority_share":majs,"G0_tfidf":G0["tfidf"],"G0_tfidf_n126":sm,"firstword_lift":fw,
                "G0_distilbert":G0["distilbert"],"G0_roberta":G0["roberta"]}).loc[K]; D.to_csv("/home/claude/p75/p75_diagnostics.csv")
pd.set_option("display.width",200); print(D.round(3).to_string()); print(R.pivot(index="analysis",columns="model",values="rho").round(3).to_string())
print(R.pivot(index="analysis",columns="model",values="p").round(4).to_string())
# B3: skill-over-majority transfer for k=8 transformers
majT={"YAHYA":corp["YAHYA"].y.value_counts(normalize=True).iloc[0],"SANGO":corp["SANGO"].y.value_counts(normalize=True).iloc[0],"MOHOM":corp["MOHOM"].y.value_counts(normalize=True).iloc[0],
      "GANI":corp["GANI"].y.value_counts(normalize=True).iloc[0],"SCAR-E":corp["SCAR-E"].y.value_counts(normalize=True).iloc[0],"EDUQG":corp["EDUQG"].y.value_counts(normalize=True).iloc[0]}
yq,_=C.youleqd(); majT["YLQ70"]=yq.y.value_counts(normalize=True).iloc[0]; majT["LAK40"]=8/40
import json
out=[]
for m in ["distilbert","roberta"]:
    sk={}
    for c in K:
        g=json.load(open(f"/home/claude/p73res/out/gate_{m}_{c}.json")); s=[g[t]-majT[t] for t in majT if t in g]; sk[c]=np.mean(s)
    x=G0[m].loc[K].values; y=np.array([sk[c] for c in K]); r,p=perm_p(x,y); out.append(dict(model=m,rho_skill=r,p_skill=p))
print(pd.DataFrame(out).round(4).to_string(index=False)); pd.DataFrame(out).to_csv("/home/claude/p75/p75_skill_transformers.csv",index=False)
