"""All values for manuscript v0.5 Tables 10 and 11, recomputed from archived outputs into CSV (no hand transcription)."""
import numpy as np, pandas as pd, json, itertools, sys
from scipy.stats import spearmanr, rankdata
sys.path.insert(0,"/home/claude/p71")
K=["EDUB","YAHYA","SANGO","MOHOM","GANI","SCAR-I","SCAR-E","EDUQG"]
def ex(x,y):
    o=spearmanr(x,y).statistic; return o,np.mean([spearmanr(x,np.array(q)).statistic>=o-1e-12 for q in itertools.permutations(y)])
D=pd.read_csv("/home/claude/p75/p75_diagnostics.csv",index_col=0)
p71=pd.read_csv("/home/claude/p71/p71_gates_transfer.csv"); v73=pd.read_csv("/home/claude/p73res/v73_recomputed.csv"); v76=pd.read_csv("/home/claude/p76res/v76_recomputed.csv")
cols={"TF-IDF":p71[p71.model=="tfidf"].set_index("train"),"Embeddings":p71[p71.model=="emb"].set_index("train"),
      "DistilBERT P73":v73[v73.model=="distilbert"].set_index("train"),"DistilBERT P76":v76[v76.model=="distilbert"].set_index("train"),
      "RoBERTa P73":v73[v73.model=="roberta"].set_index("train"),"RoBERTa P76":v76[v76.model=="roberta"].set_index("train")}
perms=np.array(list(itertools.permutations(range(8))))
def fl(x,y,Z):
    X=np.column_stack([np.ones(8)]+[rankdata(z) for z in Z]); M=np.eye(8)-X@np.linalg.pinv(X); x,y=rankdata(x),rankdata(y)
    ex_,ey=M@x,M@y; c=lambda a,b: np.corrcoef(a,b)[0,1]; obs=c(ex_,ey); null=np.array([c(ex_,M@ey[p]) for p in perms]); return obs,np.mean(null>=obs-1e-12)
covs={"size":[np.log(D.n.loc[K].values)],"balance":[D.majority_share.loc[K].values],"both":[np.log(D.n.loc[K].values),D.majority_share.loc[K].values]}
tfl=cols["TF-IDF"].G0_lift.loc[K].values
rows=[]
for cn,g in cols.items():
    G0=g.G0_lift.loc[K].values; T=g["T"].loc[K].values
    r,p=ex(G0,T); rows.append(dict(row="own",col=cn,rho=r,p=p))
    for k,Z in covs.items(): r,p=fl(G0,T,Z); rows.append(dict(row=f"fl_{k}",col=cn,rho=r,p=p))
    r,p=ex(D.G0_tfidf_n126.loc[K].values,T); rows.append(dict(row="sizematched",col=cn,rho=r,p=p))
    r,p=ex(D.firstword_lift.loc[K].values,T); rows.append(dict(row="firstword",col=cn,rho=r,p=p))
    if "P7" in cn: r,p=ex(tfl,T); rows.append(dict(row="tfidf_reference",col=cn,rho=r,p=p))
T11=pd.DataFrame(rows); T11.to_csv("/home/claude/p78/v05_table11.csv",index=False)
print(T11.pivot(index="row",columns="col",values="rho").round(3).to_string()); print(T11.pivot(index="row",columns="col",values="p").round(4).to_string())
# Table 10: Phase 73 vs Phase 76 by corpus
cmp=pd.read_csv("/home/claude/p76res/v76_vs_p73.csv")
r10=[]
for c in K:
    d=cmp[(cmp.model=="distilbert")&(cmp.corpus==c)].iloc[0]; r=cmp[(cmp.model=="roberta")&(cmp.corpus==c)].iloc[0]
    s73d=v73[(v73.model=="distilbert")&(v73.train==c)].oof_share_top_class.iloc[0]; s73r=v73[(v73.model=="roberta")&(v73.train==c)].oof_share_top_class.iloc[0]
    s76d=v76[(v76.model=="distilbert")&(v76.train==c)].oof_share_top_class.iloc[0]; s76r=v76[(v76.model=="roberta")&(v76.train==c)].oof_share_top_class.iloc[0]
    r10.append(dict(corpus=c,epochs=int(d.epochs_cv_76),share73=f"{s73d:.0%} / {s73r:.0%}",share76=f"{s76d:.0%} / {s76r:.0%}",
        oof73=f"{d.oof_acc_73:.2f} / {r.oof_acc_73:.2f}",oof76=f"{d.oof_acc_76:.2f} / {r.oof_acc_76:.2f}",
        gate=f"{d.G0_73} → {d.G0_76}" if (d.G0_73==r.G0_73 and d.G0_76==r.G0_76) else f"{d.G0_73}→{d.G0_76} / {r.G0_73}→{r.G0_76}",
        T73=f"{d.T_73:.2f} / {r.T_73:.2f}",T76=f"{d.T_76:.2f} / {r.T_76:.2f}",gap=f"{d.gap_train_oof:.2f} / {r.gap_train_oof:.2f}"))
T10=pd.DataFrame(r10); T10.to_csv("/home/claude/p78/v05_table10.csv",index=False); print(T10.to_string(index=False))
