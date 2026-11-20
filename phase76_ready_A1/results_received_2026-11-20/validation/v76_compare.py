"""Phase 76 vs Phase 73: paired item-level OOF comparison, gate/transfer changes, overfitting; run-to-run reference = corpora with unchanged epochs."""
import numpy as np, pandas as pd, json, itertools
from scipy.stats import binomtest, spearmanr
O73="/home/claude/p73res/out"; O76="/home/claude/p76res/out"; K=["EDUB","YAHYA","SANGO","MOHOM","GANI","SCAR-I","SCAR-E","EDUQG"]
ep={"EDUB":(3,3),"YAHYA":(10,8),"SANGO":(15,12),"MOHOM":(43,38),"GANI":(5,4),"SCAR-I":(3,3),"SCAR-E":(4,3),"EDUQG":(7,6)}  # (CV, full) in P76; P73 = (3,3)
rows=[]
for m in ["distilbert","roberta"]:
    ov=pd.read_csv(f"{O76}/p76_overfitting.csv").set_index(["model","corpus"])
    for c in K:
        a=pd.read_csv(f"{O73}/oof_{m}_{c}.csv"); b=pd.read_csv(f"{O76}/oof_{m}_{c}.csv"); assert (a.item_key.values==b.item_key.values).all()
        ca=(a.oof_pred==a.y).values; cb=(b.oof_pred==b.y).values; n10=int((cb&~ca).sum()); n01=int((~cb&ca).sum())
        d=cb.astype(float)-ca.astype(float); rg=np.random.default_rng(76); bs=[d[rg.integers(0,len(d),len(d))].mean() for _ in range(5000)]
        g73=json.load(open(f"{O73}/gate_{m}_{c}.json")); g76=json.load(open(f"{O76}/gate_{m}_{c}.json"))
        rows.append(dict(model=m,corpus=c,epochs_cv_73=3,epochs_cv_76=ep[c][0],oof_acc_73=ca.mean(),oof_acc_76=cb.mean(),d_oof=d.mean(),
            ci_lo=np.percentile(bs,2.5),ci_hi=np.percentile(bs,97.5),mcnemar_p=binomtest(n10,n10+n01).pvalue if n10+n01 else 1.0,
            G0_73=g73["G0"],G0_76=g76["G0"],lift_73=g73["G0_lift"],lift_76=g76["G0_lift"],T_73=g73["T"],T_76=g76["T"],dT=g76["T"]-g73["T"],
            YLQ_73=round(g73["YLQ70"]*70),YLQ_76=round(g76["YLQ70"]*70),train_acc_cv=ov.loc[(m,c),"train_acc_cv_mean"],gap_train_oof=ov.loc[(m,c),"gap"]))
D=pd.DataFrame(rows); D.to_csv("/home/claude/p76res/v76_vs_p73.csv",index=False); pd.set_option("display.width",260)
print(D[["model","corpus","epochs_cv_76","oof_acc_73","oof_acc_76","d_oof","ci_lo","ci_hi","mcnemar_p","G0_73","G0_76","T_73","T_76","dT","YLQ_73","YLQ_76","train_acc_cv","gap_train_oof"]].round(3).to_string(index=False))
ref=D[D.corpus.isin(["EDUB","SCAR-I"])]; print("\nRun-to-run reference (unchanged epochs: EDUB, SCAR-I): |d_oof| max %.3f, |dT| max %.3f, |dYLQ| max %d"%(ref.d_oof.abs().max(),ref.dT.abs().max(),(ref.YLQ_76-ref.YLQ_73).abs().max()))
# gate agreement with TF-IDF
tf=pd.read_csv("/home/claude/p71/p71_gates_transfer.csv"); tf=tf[tf.model=="tfidf"].set_index("train").G0
for m in ["distilbert","roberta"]:
    g=D[D.model==m].set_index("corpus"); print(f"{m}: G0 decisions equal to TF-IDF: P73 {(g.G0_73==tf.loc[g.index]).sum()}/8 -> P76 {(g.G0_76==tf.loc[g.index]).sum()}/8; differences now:",{c:(tf[c],g.loc[c,'G0_76']) for c in g.index if g.loc[c,'G0_76']!=tf[c]})
# exploratory: TF-IDF G0 (fixed reference) vs P76 transformer T; skill-over-majority rho
def ex(x,y):
    o=spearmanr(x,y).statistic; return o,np.mean([spearmanr(x,np.array(q)).statistic>=o-1e-12 for q in itertools.permutations(y)])
tfl=pd.read_csv("/home/claude/p71/p71_gates_transfer.csv"); tfl=tfl[tfl.model=="tfidf"].set_index("train").G0_lift
for m in ["distilbert","roberta"]:
    g=D[D.model==m].set_index("corpus"); r,p=ex(tfl.loc[K].values,g.T_76.loc[K].values); r73,p73=ex(tfl.loc[K].values,g.T_73.loc[K].values)
    print(f"EXPLORATORY {m}: TF-IDF G0 (fixed reference) vs transformer T: P73 rho {r73:.3f} p {p73:.4f} -> P76 rho {r:.3f} p {p:.4f}")
