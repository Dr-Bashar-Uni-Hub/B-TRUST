"""Phase 63 / E4 — exploratory certification on YouLeQD with corrected procedure. Preregistered as exploratory."""
import numpy as np, pandas as pd, warnings
from sklearn.model_selection import GroupShuffleSplit
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
warnings.filterwarnings("ignore")
BT=["knowledge","comprehension","application","analysis","evaluation","synthesis"]
G={6:{c:c for c in BT},3:{"knowledge":"low","comprehension":"low","application":"mid","analysis":"mid","evaluation":"high","synthesis":"high"},
   2:{"knowledge":"LOTS","comprehension":"LOTS","application":"LOTS","analysis":"HOTS","evaluation":"HOTS","synthesis":"HOTS"}}
W={6:1.0,3:np.log(3)/np.log(6),2:np.log(2)/np.log(6)}
A1,A2,DELTA=0.5,0.3,0.1; TAUS=[0.9,0.8,0.7,0.6,0.5]; TS=np.round(np.arange(0.95,0.0,-0.05),2)
r=pd.read_csv("/home/claude/bt/ex/Phase42_Results/phase42/record_level_predictions.csv")
for c in ["label","lebel1","lebel2","lebel3"]: r[c]=r[c].astype(str).str.strip().str.lower()
r["text"]=r.text.fillna("").astype(str); y=(r.label!="irrelevant").astype(int).to_numpy(); vid=r.vid.astype(str).to_numpy()
P=pd.read_csv("p60_das_lr_proba_youleqd.csv")[[f"p_{c}" for c in BT]].to_numpy(); V=r[["lebel1","lebel2","lebel3"]].to_numpy()
MP={};LS={}
for g in (6,3,2):
    names=sorted(set(G[g].values())); M=np.array([[G[g][c]==n for n in names] for c in BT],float); Pc=P@M
    Vc=np.vectorize(lambda v:G[g].get(v,"__irr__"))(V); L=np.stack([(Vc!=n).mean(1) for n in names],1)
    MP[g]=Pc.max(1); LS[g]=L[np.arange(len(r)),Pc.argmax(1)]
def decide(t,gate):
    acc=np.zeros(len(r),bool); loss=np.zeros(len(r)); w=np.zeros(len(r)); left=gate.copy()
    for g in (6,3,2):
        a=left&(MP[g]>=t); acc|=a; loss[a]=LS[g][a]; w[a]=W[g]; left&=~a
    return acc,loss,w
def pval(vals,ids):  # video-level Hoeffding p-value for H0: E[video mean of vals] >= 0, vals in [-a,1-a]
    vm=pd.Series(vals[ids]).groupby(vid[ids]).mean().to_numpy(); m=vm.mean(); J=len(vm)
    return np.exp(-2*J*max(0.0,-m)**2)
fitrel=lambda tr:make_pipeline(TfidfVectorizer(analyzer="char",ngram_range=(2,4),min_df=2,max_features=10000),
                               LogisticRegression(max_iter=500,class_weight="balanced")).fit(r.text.iloc[tr],y[tr])
rows=[]
for seed in range(12):   # identical split scheme to Phase 57
    traincal,test=next(GroupShuffleSplit(1,test_size=.25,random_state=seed).split(r,y,vid))
    a,b=next(GroupShuffleSplit(1,test_size=.33,random_state=100+seed).split(r.iloc[traincal],y[traincal],vid[traincal]))
    tr,cal=traincal[a],traincal[b]
    m=fitrel(tr); relp=np.zeros(len(r)); relp[cal]=m.predict_proba(r.text.iloc[cal])[:,1]; relp[test]=m.predict_proba(r.text.iloc[test])[:,1]
    best=None; ncert=0
    for tau in TAUS:                      # Bonferroni over 5 paths, fixed-sequence within path
        for t in TS:
            acc,loss,w=decide(t,relp>=tau)
            p1=pval(np.where(acc,loss-A1,0.0),cal); p2=pval(np.where(acc,(1-y)-A2,0.0),cal)
            if max(p1,p2)>DELTA/len(TAUS): break
            ncert+=1; U=w[cal].mean()
            if acc[cal].sum()>0 and (best is None or U>best[0]): best=(U,tau,t)
        # (continue to next tau path)
    if best:
        acc,loss,w=decide(best[2],relp>=best[1]); at=acc[test]
        rows.append(dict(seed=seed,certified=True,tau=best[1],t=best[2],cal_U=best[0],test_accepted=int(at.sum()),
                         test_vote_risk=loss[test][at].mean() if at.any() else np.nan,
                         test_contamination=(1-y[test])[at].mean() if at.any() else np.nan,test_U=w[test].mean()))
    else:
        acc,loss,w=decide(0.0,relp>=0.5)
        rows.append(dict(seed=seed,certified=False,n_certified_lambdas=ncert,
                         cal_accepted_at_loosest=int(acc[cal].sum()),cal_videos=len(set(vid[cal])),
                         cal_vote_risk_loosest=loss[cal][acc[cal]].mean(),cal_contam_loosest=(1-y[cal])[acc[cal]].mean()))
d=pd.DataFrame(rows); d.to_csv("p63_e4_certification.csv",index=False); print(d.round(3).to_string(index=False))
print("\nnonempty certified policies:",int(d.certified.sum()),"/ 12")
