"""Phase 76 exploratory follow-ups (not preregistered): Phase 75 diagnostics vs P76 transfer; skill-over-majority rho;
collapsed P73 predictions on YouLeQD; paired YouLeQD comparisons (Holm across 16), as for Phase 73."""
import numpy as np, pandas as pd, json, itertools, sys
from scipy.stats import spearmanr, binomtest
sys.path.insert(0,"/home/claude/p71"); import corpora as C
O73="/home/claude/p73res/out"; O76="/home/claude/p76res/out"; K=["EDUB","YAHYA","SANGO","MOHOM","GANI","SCAR-I","SCAR-E","EDUQG"]
def ex(x,y):
    o=spearmanr(x,y).statistic; return o,np.mean([spearmanr(x,np.array(q)).statistic>=o-1e-12 for q in itertools.permutations(y)])
D=pd.read_csv("/home/claude/p75/p75_diagnostics.csv",index_col=0)
V=pd.read_csv("/home/claude/p76res/v76_recomputed.csv")
print("Phase 75 diagnostics vs Phase 76 transformer transfer (exploratory):")
for m in ["distilbert","roberta"]:
    T=V[V.model==m].set_index("train")["T"].loc[K].values
    for col,lab in [("G0_tfidf_n126","size-matched TF-IDF G0 (n=126)"),("firstword_lift","first-word lookup (no training)")]:
        r,p=ex(D[col].loc[K].values,T); print(f"  {m:10s} {lab:34s} rho {r:.3f} p {p:.4f}")
# skill over majority for P76
yq,Vv=C.youleqd(); majT={}
import corpora
REV={"remember":1,"understand":2,"apply":3,"analyze":4,"evaluate":5,"create":6}
def faraji(f):
    d=pd.read_csv(f"/home/claude/p71/{f}"); d=pd.DataFrame({"text":d.QUESTION,"y":d["BT LEVEL"].str.strip().str.lower().map(REV)})
    d=d[d.text.map(lambda s:isinstance(s,str) and s.strip()!="")].copy(); d["n"]=d.text.map(C.norm); return d.drop_duplicates("n")
for k,f in [("YAHYA","yahya-2012_revised.csv"),("SANGO","Sangodiah_2017_415_revised.csv"),("MOHOM","Mohammed-and-Omar_2020_126_revised.csv"),("GANI","Gani_2023_collected-dataset-1200_revised.csv")]:
    majT[k]=faraji(f).y.value_counts(normalize=True).iloc[0]
majT["SCAR-E"]=C.scar_e().y.value_counts(normalize=True).iloc[0]; majT["EDUQG"]=C.eduqg().y.value_counts(normalize=True).iloc[0]; majT["YLQ70"]=yq.y.value_counts(normalize=True).iloc[0]; majT["LAK40"]=8/40
for m in ["distilbert","roberta"]:
    sk=[np.mean([json.load(open(f"{O76}/gate_{m}_{c}.json"))[t]-majT[t] for t in majT if t in json.load(open(f"{O76}/gate_{m}_{c}.json"))]) for c in K]
    g0=V[V.model==m].set_index("train").G0_lift.loc[K].values; r,p=ex(g0,np.array(sk)); print(f"  {m}: skill-over-majority rho {r:.3f} p {p:.4f}")
# collapsed P73 predictions on YouLeQD
print("\nPhase 73 vs Phase 76 YouLeQD prediction distribution (SANGO, MOHOM):")
for m in ["distilbert","roberta"]:
    for c in ["SANGO","MOHOM"]:
        a=pd.read_csv(f"{O73}/items_{m}_{c}.csv"); b=pd.read_csv(f"{O76}/items_{m}_{c}.csv")
        a=a[a.target=="YLQ70"].pred.value_counts().to_dict(); b=b[b.target=="YLQ70"].pred.value_counts().to_dict()
        print(f"  {m} {c}: P73 {a}  ->  P76 {b}")
print("  (YouLeQD consolidated labels: 2 = comprehension is the majority, 26/70)")
# paired YouLeQD comparisons (as Phase 73)
vid=yq.vid.to_numpy(); y=yq.y.to_numpy()
vl=lambda p: np.nanmean(np.where(np.isnan(Vv),1.0,(Vv!=np.asarray(p,float)[:,None]).astype(float)),1)
llm=pd.read_csv("/mnt/user-data/uploads/p70_llm_detailed.csv") if __import__("os").path.exists("/mnt/user-data/uploads/p70_llm_detailed.csv") else pd.read_csv("/home/claude/p70llm/p70_llm_detailed.csv")
llm=llm[llm.dataset=="YLQ70"].prediction.to_numpy()
g=pd.Series(np.arange(70)).groupby(vid).apply(list).tolist(); rb=np.random.default_rng(76); idx=[np.concatenate([g[i] for i in rb.integers(0,len(g),len(g))]) for _ in range(10000)]
def ci(d): bs=np.array([d[i].mean() for i in idx]); return np.percentile(bs,[2.5,97.5]), 2*min((bs>=0).mean(),(bs<=0).mean())
rows=[]
for m in ["distilbert","roberta"]:
    for c in K:
        it=pd.read_csv(f"{O76}/items_{m}_{c}.csv"); x=it[it.target=="YLQ70"].sort_values("row"); p=x.pred.to_numpy(); assert (x.y.values==y).all()
        d=vl(p)-vl(np.full(70,2)); (lo,hi),pb=ci(d); d2=vl(llm)-vl(p); (lo2,hi2),_=ci(d2)
        rows.append(dict(model=m,train=c,correct=int((p==y).sum()),voteloss=vl(p).mean(),diff_vs_const=d.mean(),ci_lo=lo,ci_hi=hi,boot_p=pb,llm_minus=d2.mean(),llm_lo=lo2,llm_hi=hi2))
R=pd.DataFrame(rows); o=np.argsort(R.boot_p.values); adj=np.empty(len(R)); run=0
for r_,i in enumerate(o): run=max(run,(len(R)-r_)*R.boot_p.values[i]); adj[i]=min(1,run)
R["holm"]=adj; R.to_csv("/home/claude/p76res/v76_youleqd_paired.csv",index=False)
print("\nYouLeQD 70, Phase 76 models (descriptive; video-cluster bootstrap; Holm across 16):")
print(R[["model","train","correct","voteloss","diff_vs_const","ci_lo","ci_hi","holm","llm_minus","llm_lo","llm_hi"]].round(3).to_string(index=False))
print("models with unadjusted CI below constant:",R[R.ci_hi<0][["model","train"]].values.tolist(),"| surviving Holm:",R[R.holm<0.05][["model","train"]].values.tolist())
print("LLM lower than model (CI hi<0):",int((R.llm_hi<0).sum()),"of 16")
