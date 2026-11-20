"""Phase 73 validation: recompute gates, transfer and tests from per-question files; check item keys, leakage, collapse."""
import numpy as np, pandas as pd, json, hashlib, itertools, warnings, sys
from scipy.stats import spearmanr
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import cohen_kappa_score
sys.path.insert(0,"/home/claude/p71"); import corpora as C
warnings.filterwarnings("ignore"); O="/home/claude/p76res/out"
REV={"remember":1,"understand":2,"apply":3,"analyze":4,"evaluate":5,"create":6}
def faraji(f):
    d=pd.read_csv(f"/home/claude/p71/{f}"); d=pd.DataFrame({"text":d.QUESTION,"y":d["BT LEVEL"].str.strip().str.lower().map(REV)})
    d=d[d.text.map(lambda s:isinstance(s,str) and s.strip()!="")].copy(); d["n"]=d.text.map(C.norm); return d.drop_duplicates("n").reset_index(drop=True)
corp={"EDUB":C.edub(),"YAHYA":faraji("yahya-2012_revised.csv"),"SANGO":faraji("Sangodiah_2017_415_revised.csv"),"MOHOM":faraji("Mohammed-and-Omar_2020_126_revised.csv"),
      "GANI":faraji("Gani_2023_collected-dataset-1200_revised.csv"),"SCAR-I":C.scar_i(),"SCAR-E":C.scar_e(),"EDUQG":C.eduqg()}
yq,_=C.youleqd(); lk=C.lak(); TG=["YAHYA","SANGO","MOHOM","GANI","SCAR-E","EDUQG"]; h=lambda s:hashlib.sha256(s.encode()).hexdigest()[:16]
def lookup_cv(key,y):
    p=np.zeros(len(y),int); maj=pd.Series(y).mode()[0]
    for a,b in StratifiedKFold(5,shuffle=True,random_state=65).split(key,y):
        t=pd.DataFrame({"k":key[a],"y":y[a]}).groupby("k").y.agg(lambda s:s.mode()[0]); p[b]=pd.Series(key[b]).map(t).fillna(maj).astype(int).to_numpy()
    return p
issues=[]; rows=[]
for m in ["distilbert","roberta"]:
    for c,d in corp.items():
        g=json.load(open(f"{O}/gate_{m}_{c}.json")); oof=pd.read_csv(f"{O}/oof_{m}_{c}.csv")
        if not ((oof.item_key.values==d.n.map(h).values).all() and (oof.y.values==d.y.values).all()): issues.append(f"{m}/{c}: OOF keys or labels do not match corpus order")
        p=oof.oof_pred.to_numpy(); y=d.y.to_numpy(); acc=(p==y).mean(); maj=pd.Series(y).value_counts(normalize=True).iloc[0]
        meta=(lookup_cv(d.meta.to_numpy(),y)==y).mean() if "meta" in d else np.nan; lift=acc-np.nanmax([maj,meta]); k=cohen_kappa_score(y,p)
        gate="FAIL" if (lift<.05 or k<.20) else ("PASS" if (lift>=.15 and k>=.40) else "CAUTION")
        it=pd.read_csv(f"{O}/items_{m}_{c}.csv"); accs={}
        ts=set(d.n.map(h))
        for tn in TG:
            if tn==c or {c,tn}=={"SCAR-I","SCAR-E"}:
                if (it.target==tn).any(): issues.append(f"{m}/{c}: excluded target {tn} present"); 
                continue
            t=corp[tn]; keep=~t.n.isin(set(d.n)); exp=t[keep]; x=it[it.target==tn]
            if len(x)!=len(exp) or not (x.item_key.values==exp.n.map(h).values).all(): issues.append(f"{m}/{c}->{tn}: item set mismatch")
            if x.item_key.isin(ts).any(): issues.append(f"{m}/{c}->{tn}: leakage")
            accs[tn]=(x.pred.values==x.y.values).mean()
        x=it[it.target=="YLQ70"]; accs["YLQ70"]=(x.pred.values==yq.y.values).mean()
        x=it[it.target=="LAK40"]; accs["LAK40"]=np.mean([a in s for a,s in zip(x.pred.values,lk.refs)])
        T=np.mean(list(accs.values()))
        for nm,a,b in [("cv_acc",acc,g["cv_acc"]),("G0_lift",lift,g["G0_lift"]),("kappa",k,g["kappa_cv"]),("T",T,g["T"])]:
            if abs(a-b)>1e-9: issues.append(f"{m}/{c}: {nm} recomputed {a:.6f} vs reported {b:.6f}")
        if gate!=g["G0"]: issues.append(f"{m}/{c}: gate {gate} vs {g['G0']}")
        rows.append(dict(model=m,train=c,n=len(y),G0_lift=lift,kappa=k,G0=gate,T=T,oof_classes_predicted=int(pd.Series(p).nunique()),
                         oof_share_top_class=pd.Series(p).value_counts(normalize=True).iloc[0],YLQ70=accs["YLQ70"],steps_per_epoch_cv=int(np.ceil(len(y)*0.8/16))))
R=pd.DataFrame(rows); R.to_csv("/home/claude/p76res/v76_recomputed.csv",index=False)
print("ISSUES:",issues if issues else "none")
print(R.round(3).to_string(index=False))
for m,g in R.groupby("model"):
    x,y=g.G0_lift.to_numpy(),g["T"].to_numpy(); obs=spearmanr(x,y).statistic
    pv=np.mean([spearmanr(x,np.array(q)).statistic>=obs-1e-12 for q in itertools.permutations(y)])
    print(f"{m}: recomputed rho {obs:.4f} exact p {pv:.6f}; PASS>FAIL {g[g.G0=='PASS']['T'].min()>g[g.G0=='FAIL']['T'].max()}")
# ---- Phase 76 additions: R1/R2/R3 recomputed; top-class share vs gate file ----
print("\nR1/R2 per model:")
for m,g in R.groupby("model"):
    g=g.set_index("train"); small=g.loc[["SANGO","MOHOM"]]
    gj={c:json.load(open(f"{O}/gate_{m}_{c}.json")) for c in ["SANGO","MOHOM"]}
    share_ok=all(abs(gj[c]["oof_top_class_share"]-small.loc[c,"oof_share_top_class"])<1e-9 for c in gj)
    print(f"  {m}: top-class share SANGO {small.loc['SANGO','oof_share_top_class']:.3f}, MOHOM {small.loc['MOHOM','oof_share_top_class']:.3f} -> R1 {bool((small.oof_share_top_class<0.80).all())}; "
          f"G0 SANGO {small.loc['SANGO','G0']}, MOHOM {small.loc['MOHOM','G0']} -> R2 {bool((small.G0!='FAIL').all())}; share matches gate file: {share_ok}")
t=pd.read_csv(f"{O}/p76_tests.csv").set_index("model"); print(t[["rho","exact_p"]])
