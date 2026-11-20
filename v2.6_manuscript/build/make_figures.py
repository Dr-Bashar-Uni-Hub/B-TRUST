"""Manuscript figures, computed from archived outputs only (v1.0–v2.5 + Phase 70 researcher outputs)."""
import numpy as np, pandas as pd, matplotlib, joblib, json
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import corpora as C
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,"axes.spines.top":False,"axes.spines.right":False,"savefig.dpi":300})
EX=C.EX; out={}
# Fig 1: EduBloom difficulty x level
q=pd.read_csv(f"{EX}/Phase42_Results/phase42/questions.csv"); ct=pd.crosstab(q.difficulty,q.bloom_level).loc[["Easy","Medium","Hard"]]
fig,ax=plt.subplots(figsize=(5.2,2.2)); im=ax.imshow(ct.values,cmap="Blues")
for i in range(3):
    for j in range(6): v=ct.values[i,j]; ax.text(j,i,f"{v:,}",ha="center",va="center",fontsize=7.5,color="white" if v>ct.values.max()*0.55 else "black")
ax.set_xticks(range(6),[f"L{k}" for k in range(1,7)]); ax.set_yticks(range(3),ct.index); ax.set_xlabel("Bloom label"); ax.set_ylabel("Difficulty field")
ax.spines[:].set_visible(False); fig.tight_layout(); fig.savefig("fig/fig1_edubloom_difficulty_level.png"); out["fig1"]=ct.to_dict()
# Fig 2: frozen DistilBERT internal confusion
i=pd.read_csv(f"{EX}/Phase42_Results/phase42/internal_predictions.csv"); cm=pd.crosstab(i.bloom_level,i.distilbert_prediction).reindex(index=[f"L{k}" for k in range(1,7)],columns=[f"L{k}" for k in range(1,7)],fill_value=0)
fig,ax=plt.subplots(figsize=(3.6,3.2)); ax.imshow(cm.values,cmap="Greys")
for a in range(6):
    for b in range(6): v=cm.values[a,b]; ax.text(b,a,str(v),ha="center",va="center",fontsize=7.5,color="white" if v>120 else "black")
ax.set_xticks(range(6),cm.columns); ax.set_yticks(range(6),cm.index); ax.set_xlabel("Predicted"); ax.set_ylabel("EduBloom label"); ax.spines[:].set_visible(False)
fig.tight_layout(); fig.savefig("fig/fig2_distilbert_confusion.png"); out["fig2_col_totals"]=cm.sum().to_dict()
# Fig 3: vote loss by granularity on YouLeQD 70
yq,V=C.youleqd(); r=pd.read_csv(f"{EX}/Phase42_Results/phase42/record_level_predictions.csv")
for c in ["label"]: r[c]=r[c].astype(str).str.strip().str.lower()
rel=r[r.label!="irrelevant"].reset_index(drop=True); assert (rel.text.fillna("").str.strip()==yq.text.str.strip()).all()
llm=pd.read_csv("/mnt/user-data/uploads/p70_llm_detailed.csv"); llm=llm[llm.dataset=="YLQ70"].prediction.to_numpy()
das=pd.Series(joblib.load("/home/claude/p58/p60_das_lr_model.joblib").predict(yq.n)).map(C.ORIG).to_numpy()
P={"Frozen EduBloom LR":rel.lr_prediction.map(lambda s:int(str(s)[1])).to_numpy(),"Frozen EduBloom DistilBERT":rel.distilbert_prediction.map(lambda s:int(str(s)[1])).to_numpy(),
   "Pooled human-authored LR":das,"Zero-shot LLM":llm}
G={"6 levels":lambda v:v,"3 bands":lambda v:np.ceil(v/2),"2 bands":lambda v:np.where(v>=4,2.0,1.0)}
rows=[]
for gname,m in G.items():
    Vc=np.where(np.isnan(V),np.nan,m(np.nan_to_num(V,nan=1)))
    f=lambda p: np.nanmean(np.where(np.isnan(Vc),1.0,(Vc!=np.asarray(p,float)[:,None]).astype(float)),1).mean()
    for k,p in P.items(): rows.append(dict(granularity=gname,predictor=k,vote_loss=f(m(p))))
    cl={c:f(np.full(70,c)) for c in np.unique(m(np.arange(1,7)))}; rows.append(dict(granularity=gname,predictor="Best constant",vote_loss=min(cl.values())))
    H=np.nanmean(np.array([np.where(np.isnan(Vc[:,j])|np.isnan(Vc[:,k]),np.where(np.isnan(Vc[:,j])&np.isnan(Vc[:,k]),0.0,1.0),(Vc[:,j]!=Vc[:,k]).astype(float)) for j in range(3) for k in range(3) if j!=k]),0).mean()
    rows.append(dict(granularity=gname,predictor="Human (leave-one-out)",vote_loss=H))
F3=pd.DataFrame(rows); F3.to_csv("fig/fig3_values.csv",index=False)
order=["Frozen EduBloom LR","Frozen EduBloom DistilBERT","Pooled human-authored LR","Zero-shot LLM","Best constant","Human (leave-one-out)"]
cols=["#9e9e9e","#616161","#4a7fb5","#c0504d","#000000","#6aa84f"]; fig,ax=plt.subplots(figsize=(6.2,2.8)); w=0.13
for k,(pname,c) in enumerate(zip(order,cols)):
    vals=[F3[(F3.granularity==g)&(F3.predictor==pname)].vote_loss.iloc[0] for g in G]
    ax.bar(np.arange(3)+(k-2.5)*w,vals,w,label=pname,color=c,hatch="//" if pname=="Best constant" else None,edgecolor="white" if pname!="Best constant" else "black",fill=pname!="Best constant")
ax.set_xticks(range(3),list(G)); ax.set_ylabel("Mean vote loss (lower is better)"); ax.set_ylim(0,0.9); ax.legend(fontsize=6.5,ncol=3,frameon=False,loc="upper center",bbox_to_anchor=(0.5,1.22))
fig.tight_layout(); fig.savefig("fig/fig3_vote_loss_granularity.png")
# Fig 4: G0 lift vs transfer
p71=pd.read_csv("/home/claude/p71/p71_gates_transfer.csv"); d70={m:pd.read_csv(f"/home/claude/p70res/p70_transfer_{m}.csv") for m in ["distilbert","roberta"]}
panels=[("TF-IDF (k = 8)",p71[p71.model=="tfidf"][["train","G0_lift","T","G0"]]),("Word embeddings (k = 8)",p71[p71.model=="emb"][["train","G0_lift","T","G0"]])]
for m,lab in [("distilbert","DistilBERT (k = 5)"),("roberta","RoBERTa (k = 5)")]:
    g=pd.read_csv(f"/home/claude/p70res/p70_G0_{m}.csv"); t=d70[m].merge(g[["corpus","G0"]].rename(columns={"corpus":"train"}),on="train")
    panels.append((lab,t.rename(columns={"T_mean":"T"})[["train","G0_lift","T","G0"]]))
mk={"PASS":"o","CAUTION":"s","FAIL":"x"}; fig,axs=plt.subplots(1,4,figsize=(7.2,2.3),sharey=False)
for ax,(lab,t) in zip(axs,panels):
    for _,row in t.iterrows():
        ax.scatter(row.G0_lift*100,row["T"]*100,marker=mk[row.G0],color="black",s=18)
        off={"SCAR-E":(-4,-9),"GANI":(-18,-9)}.get(row.train,(2,2)); ax.annotate(row.train,(row.G0_lift*100,row["T"]*100),fontsize=5.5,xytext=off,textcoords="offset points")
    ax.set_title(lab,fontsize=8); ax.set_xlabel("G0 lift (pp)",fontsize=7.5); ax.tick_params(labelsize=7)
axs[0].set_ylabel("Mean transfer accuracy (%)",fontsize=7.5); fig.tight_layout(); fig.savefig("fig/fig4_g0_vs_transfer.png")
# Fig 5: power curves
s=pd.read_csv("/home/claude/p58/p62_e3_simulation.csv"); fig,ax=plt.subplots(figsize=(4.2,2.6))
for tr,ls in [(0.3,"-"),(0.4,"--")]:
    for icc,c in [(0.0,"#000000"),(0.5,"#9e9e9e")]:
        g=s[(s.true_risk.round(2)==tr)&(s.icc==icc)].sort_values("videos"); ax.plot(g.videos,g.video_hoeffding,ls,color=c,marker="o",ms=3,label=f"true risk {tr}, ICC {icc}")
ax.axhline(0.8,color="grey",lw=0.6,ls=":"); ax.set_xscale("log"); ax.set_xlabel("Independent sources of accepted decisions (videos)"); ax.set_ylabel("Power to certify risk ≤ 0.5"); ax.legend(fontsize=6.5,frameon=False)
fig.tight_layout(); fig.savefig("fig/fig5_power.png")
json.dump(out,open("fig/fig_meta.json","w"),default=str,indent=1); print(F3.pivot(index="predictor",columns="granularity",values="vote_loss").round(4))
