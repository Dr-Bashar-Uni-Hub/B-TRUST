"""Phase 61 / E2 — granularity-adaptive (hierarchical) vs flat selection. Preregistered + deviation D1."""
import numpy as np, pandas as pd, warnings
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
warnings.filterwarnings("ignore")
BT=["knowledge","comprehension","application","analysis","evaluation","synthesis"]
G={6:{c:c for c in BT},
   3:{"knowledge":"low","comprehension":"low","application":"mid","analysis":"mid","evaluation":"high","synthesis":"high"},
   2:{"knowledge":"LOTS","comprehension":"LOTS","application":"LOTS","analysis":"HOTS","evaluation":"HOTS","synthesis":"HOTS"}}
W={6:1.0,3:np.log(3)/np.log(6),2:np.log(2)/np.log(6)}
EX="/home/claude/bt/ex"
r=pd.read_csv(f"{EX}/Phase42_Results/phase42/record_level_predictions.csv")
for c in ["label","lebel1","lebel2","lebel3"]: r[c]=r[c].astype(str).str.strip().str.lower()
r["text"]=r.text.fillna("").astype(str)
pr=pd.read_csv("p60_das_lr_proba_youleqd.csv"); assert (pr.cid==r.cid).all()
P=pr[[f"p_{c}" for c in BT]].to_numpy()
V=r[["lebel1","lebel2","lebel3"]].to_numpy(); vid=r.vid.astype(str).to_numpy()
rel=(r.label!="irrelevant").to_numpy(); yrel=rel.astype(int)

def coarse(g):  # probs per coarse class, coarse label names, and loss matrix per coarse class
    names=sorted(set(G[g].values())); M=np.array([[G[g][c]==n for n in names] for c in BT],float)
    Pc=P@M
    Vc=np.vectorize(lambda v:G[g].get(v,"__irr__"))(V)
    L=np.stack([(Vc!=n).mean(1) for n in names],1)   # vote loss for each coarse class
    return Pc,L
CO={g:coarse(g) for g in (6,3,2)}
# per-item: for each granularity, max prob and loss of argmax
MP={g:CO[g][0].max(1) for g in CO}; LS={g:CO[g][1][np.arange(len(r)),CO[g][0].argmax(1)] for g in CO}
# human LOO reference by granularity on relevant items
for g in (6,3,2):
    Vc=np.vectorize(lambda v:G[g].get(v,"__irr__"))(V)
    h=np.mean([(Vc[:,j]!=Vc[:,k]) for j in range(3) for k in range(3) if j!=k],0)
    print(f"G{g}: model argmax vote loss (relevant)={LS[g][rel].mean():.4f}  human LOO={h[rel].mean():.4f}")

# cross-fitted relevance gate (5-fold group-disjoint; fitted on train folds only)
relp=np.full(len(r),np.nan)
for a,b in StratifiedGroupKFold(5,shuffle=True,random_state=61).split(r,yrel,vid):
    m=make_pipeline(TfidfVectorizer(analyzer="char",ngram_range=(2,4),min_df=2,max_features=10000),
                    LogisticRegression(max_iter=500,class_weight="balanced")).fit(r.text.iloc[a],yrel[a])
    relp[b]=m.predict_proba(r.text.iloc[b])[:,1]
gate=relp>=0.5
print(f"gate: accepted {gate.sum()}, of which relevant {(gate&rel).sum()}/{rel.sum()}")
TG=np.round(np.linspace(0,1,101),2)

def decisions(method,t,mask):
    acc=np.zeros(len(r),bool); loss=np.zeros(len(r)); w=np.zeros(len(r))
    if method=="FLAT":
        a=mask&(MP[6]>=t); acc|=a; loss[a]=LS[6][a]; w[a]=1
    else:
        left=mask.copy()
        for g in (6,3,2):
            a=left&(MP[g]>=t); acc|=a; loss[a]=LS[g][a]; w[a]=W[g]; left&=~a
    return acc,loss,w

def curve(method,idx,mask):
    pts=[]
    for t in TG:
        a,l,w=decisions(method,t,mask)
        a,l,w=a[idx],l[idx],w[idx]
        if a.sum()==0: continue
        pts.append((w.sum()/len(idx), l[a].mean()))
    return np.array(sorted(set(pts)))

def aurc(pts,lo=None):
    if lo is not None:
        pts=pts[pts[:,0]>=lo-1e-12]
    if len(pts)<2: return np.nan
    area=np.trapezoid(pts[:,1],pts[:,0])
    return area if lo is None else area/(pts[-1,0]-pts[0,0])

def stats(idx,mask):
    cf=curve("FLAT",idx,mask); ch=curve("HIER",idx,mask)
    lo=max(cf[0,0],ch[0,0])
    return aurc(ch)-aurc(cf), aurc(ch,lo)-aurc(cf,lo), aurc(ch),aurc(cf),aurc(ch,lo),aurc(cf,lo),cf,ch

def boot(base_idx,mask,B=10000,seed=61):
    groups=pd.Series(base_idx).groupby(vid[base_idx]).apply(list).tolist()
    rg=np.random.default_rng(seed); out=[]
    for b in range(B):
        pick=rg.integers(0,len(groups),len(groups)); idx=np.concatenate([groups[i] for i in pick])
        s=stats(idx,mask); out.append(s[:2])
    return np.array(out)

out=[]
for name,base,mask in [("E2a_relevant70_oracle",np.where(rel)[0],np.ones(len(r),bool)),
                       ("E2b_all300_relevance_gate",np.arange(len(r)),gate)]:
    s=stats(base,mask)
    bs=boot(base,mask, B=2000 if False else 10000)
    ci1=np.nanpercentile(bs[:,0],[2.5,97.5]); ci2=np.nanpercentile(bs[:,1],[2.5,97.5])
    out.append(dict(analysis=name,AURC_HIER=s[2],AURC_FLAT=s[3],diff_unnorm=s[0],ci_unnorm_lo=ci1[0],ci_unnorm_hi=ci1[1],
                    meanrisk_common_HIER=s[4],meanrisk_common_FLAT=s[5],diff_common=s[1],ci_common_lo=ci2[0],ci_common_hi=ci2[1],
                    H2_supported=bool(ci1[1]<0 and ci2[1]<0)))
    pd.DataFrame(s[6],columns=["U","risk"]).to_csv(f"p61_{name}_FLAT_curve.csv",index=False)
    pd.DataFrame(s[7],columns=["U","risk"]).to_csv(f"p61_{name}_HIER_curve.csv",index=False)
o=pd.DataFrame(out); o.to_csv("p61_e2_results.csv",index=False); print(o.round(4).T.to_string())

# Descriptive operating points at matched information-weighted coverage for HIER on relevant70
for name in ["E2a_relevant70_oracle","E2b_all300_relevance_gate"]:
    f=pd.read_csv(f"p61_{name}_FLAT_curve.csv"); h=pd.read_csv(f"p61_{name}_HIER_curve.csv")
    print("\n",name)
    for U in [0.1,0.2,0.3,0.5]:
        fi=f.iloc[(f.U-U).abs().argmin()]; hi=h.iloc[(h.U-U).abs().argmin()]
        print(f"  U≈{U}: FLAT U={fi.U:.3f} risk={fi.risk:.3f} | HIER U={hi.U:.3f} risk={hi.risk:.3f}")
