"""QC: recompute every key manuscript number from archived outputs and compare with the value stated in the text."""
import numpy as np, pandas as pd, re, corpora as C
from sklearn.metrics import cohen_kappa_score
EX=C.EX; R=[]
def chk(claim,stated,actual,tol):
    R.append(dict(claim=claim,stated=stated,recomputed=round(float(actual),4),raw=float(actual),ok=abs(float(actual)-stated)<=tol))
q=pd.read_csv(f"{EX}/Phase42_Results/phase42/questions.csv"); q["t"]=[a.replace(b,"<T>") for a,b in zip(q.question,q.topic)]
chk("EduBloom templates with >1 label (%)",92.8,100*(q.groupby("t").bloom_level.nunique()>1).mean(),0.05)
chk("EduBloom n",73712,len(q),0)
i=pd.read_csv(f"{EX}/Phase42_Results/phase42/internal_predictions.csv").merge(q[["question","difficulty"]],on="question")
best=i.groupby("difficulty").bloom_level.agg(lambda s:s.value_counts().idxmax()); chk("Metadata-only internal acc (%)",50.0,100*(i.difficulty.map(best)==i.bloom_level).mean(),0.05)
chk("Frozen DistilBERT internal acc (%)",50.9,100*(i.distilbert_prediction==i.bloom_level).mean(),0.05)
chk("Frozen LR internal acc (%)",48.2,100*(i.lr_prediction==i.bloom_level).mean(),0.05)
chk("DistilBERT L4 predictions",0,(i.distilbert_prediction=="L4").sum(),0); chk("DistilBERT L2 predictions",3,(i.distilbert_prediction=="L2").sum(),0)
js=pd.read_csv("/home/claude/p71/p72_edubloom_stem_JS_distance.csv",index_col=0); chk("JS distance L5-L6",0.217,js.loc["L5","L6"],0.0005)
r=pd.read_csv(f"{EX}/Phase42_Results/phase42/record_level_predictions.csv"); r["label"]=r.label.str.strip().str.lower(); rel=r[r.label!="irrelevant"]
mp={f"L{k+1}":v for k,v in enumerate(["knowledge","comprehension","application","analysis","evaluation","synthesis"])}
chk("YouLeQD relevant n",70,len(rel),0); chk("DistilBERT correct /70",26,(rel.distilbert_prediction.map(mp)==rel.label).sum(),0)
chk("LR correct /70",23,(rel.lr_prediction.map(mp)==rel.label).sum(),0); chk("Majority correct /70",26,(rel.label=="comprehension").sum(),0)
chk("kappa DistilBERT",0.107,cohen_kappa_score(rel.label,rel.distilbert_prediction.map(mp)),0.0005); chk("kappa LR",0.096,cohen_kappa_score(rel.label,rel.lr_prediction.map(mp)),0.0005)
chk("DistilBERT L1 predictions /300",240,(r.distilbert_prediction=="L1").sum(),0)
f3=pd.read_csv("fig/fig3_values.csv").set_index(["granularity","predictor"]).vote_loss
chk("Human LOO G6",0.686,f3[("6 levels","Human (leave-one-out)")],0.0005); chk("Best constant G6",0.738,f3[("6 levels","Best constant")],0.0005)
chk("Best constant G3",0.552,f3[("3 bands","Best constant")],0.0005); chk("Best constant G2",0.481,f3[("2 bands","Best constant")],0.0005)
chk("LLM vote loss G6",0.590,f3[("6 levels","Zero-shot LLM")],0.0005)
b=pd.read_csv("/home/claude/p58/p60_e1_cluster_bootstrap.csv").iloc[0]; chk("H1 diff (pp)",-2.9,100*b["diff"],0.05); chk("H1 CI lo",-12.2,100*b.ci_lo,0.05); chk("H1 CI hi",6.8,100*b.ci_hi,0.05)
e=pd.read_csv("/home/claude/p58/p61_e2_results.csv").set_index("analysis")
chk("H2 oracle diff (pp)",-8.1,100*e.loc["E2a_relevant70_oracle","diff_unnorm"],0.05); chk("H2 oracle CI hi",-1.5,100*e.loc["E2a_relevant70_oracle","ci_unnorm_hi"],0.05)
chk("H2 gate diff (pp)",-1.0,100*e.loc["E2b_all300_relevance_gate","diff_unnorm"],0.05); chk("H2 gate CI hi",0.4,100*e.loc["E2b_all300_relevance_gate","ci_unnorm_hi"],0.05)
s=pd.read_csv("/home/claude/p58/p62_e3_simulation.csv"); nul=s[s.true_risk==0.5]
chk("Video-level FCR max (%)",1.5,100*nul.video_hoeffding.max(),0.05); chk("Row CP FCR max (%)",13.0,100*nul.row_cp.max(),0.05)
pw=s[(s.true_risk.round(2)==0.4)&(s.icc==0.0)].set_index("videos").video_hoeffding; chk("Power J=236 (true .4, ICC 0) %",84.7,100*pw[236],0.05); chk("Power J=120 %",53.2,100*pw[120],0.05)
chk("Phase 63 min p over grid",0.986,pd.read_csv("/home/claude/p58/p63_diag_min_p.csv").min_p_over_grid.min(),0.0006)
g1=pd.read_csv("/home/claude/p65/p65_G1_G3_scaria.csv").iloc[0]; chk("Expert-expert kappa",0.864,g1.expert_expert_kappa,0.0005)
chk("Generator-e1 kappa",0.638,g1.generator_vs_e1_kappa,0.0005); chk("Generator-e2 kappa",0.725,g1.generator_vs_e2_kappa,0.0005); chk("Scaria both-rated n",2071,g1.n,0)
chk("Expert-expert exact (%)",88.8,100*g1.expert_expert_exact,0.05)
t=pd.read_csv("/home/claude/p65/p66_67_tests.csv"); tt=t.set_index("test")
chk("H5 diff (pp)",0.04,100*tt.iloc[0]["est"],0.01); chk("H6 diff (pp)",0.2,100*tt.loc["H6 PROV-RAND on DASQ","est"],0.05); chk("CL-ALL (pp)",-4.6,100*tt.loc["CL-ALL on DASQ","est"],0.05)
p71=pd.read_csv("/home/claude/p71/p71_tests.csv").set_index("model")
chk("H11a rho",0.93,p71.loc["tfidf","rho_T"],0.005); chk("H11a p",0.0011,p71.loc["tfidf","p_T"],0.00005); chk("H11b rho",0.69,p71.loc["emb","rho_T"],0.005); chk("H11b p",0.035,p71.loc["emb","p_T"],0.0005)
chk("TF-IDF skill rho",0.95,p71.loc["tfidf","rho_Tskill"],0.005); chk("emb skill p",0.16,p71.loc["emb","p_Tskill"],0.005)
G=pd.read_csv("/home/claude/p71/p71_gates_transfer.csv"); gt=G[G.model=="tfidf"].set_index("train")
for k,(lift,T) in {"SCAR-I":(70.9,46.1),"YAHYA":(58.8,50.4),"SCAR-E":(57.8,42.1),"MOHOM":(40.5,33.6),"SANGO":(23.7,36.1),"GANI":(13.0,27.1),"EDUB":(0.04,29.3),"EDUQG":(0.0,17.2)}.items():
    chk(f"{k} G0 lift (pp)",lift if k!="SCAR-E" else 57.7,100*gt.loc[k,"G0_lift"],0.05); chk(f"{k} transfer (%)",T,100*gt.loc[k,"T"],0.05)
p70=pd.read_csv("/home/claude/p70res/p70_tests.csv").set_index("model"); chk("H9a rho",0.70,p70.loc["distilbert","rho"],0.005); chk("H9c p",0.175,p70.loc["roberta","exact_p"],0.0005)
h=pd.read_csv("/home/claude/p70llm/val_h10_robustness.csv"); chk("H10 diff",-0.148,h.iloc[0]["diff"],0.0005); chk("H10 CI lo",-0.232,h.iloc[0].ci_lo,0.0005); chk("H10 CI hi",-0.065,h.iloc[0].ci_hi,0.0005)
sk=pd.read_csv("/home/claude/p70llm/val_skill_over_majority.csv").set_index("dataset"); chk("LLM EduQG skill (pp)",-4.1,100*sk.loc["EDUQG","skill"],0.05)
pc=pd.read_csv("/home/claude/p70llm/val_paired_comparisons.csv"); chk("Smallest Holm p",0.21,pc.mcnemar_p_holm.min(),0.005)

# ---- Phase 73 (v0.3) ----
v=pd.read_csv("/home/claude/p73res/v73_recomputed.csv"); t73=pd.read_csv("/home/claude/p73res/out/p73_tests.csv").set_index("model")
chk("H12a rho",0.83,t73.loc["distilbert","rho"],0.005); chk("H12a p",0.0077,t73.loc["distilbert","exact_p"],0.00005)
chk("H12b rho",0.93,t73.loc["roberta","rho"],0.005); chk("H12b p",0.0008,t73.loc["roberta","exact_p"],0.00005)
ex=pd.read_csv("/home/claude/p73res/v73_exploratory.csv"); k6=ex[ex.test.str.startswith("exclude")]; ref=ex[ex.test.str.startswith("TF-IDF G0")]
chk("k=6 rho (both)",0.94,k6.rho.min(),0.005); chk("k=6 p",0.0083,k6.exact_p.max(),0.00005); chk("reference-model rho",0.62,ref.rho.min(),0.005); chk("reference-model p",0.057,ref.exact_p.max(),0.0005)
for m,c,lo in [("distilbert","SANGO",0.98),("distilbert","MOHOM",0.98),("roberta","SANGO",0.98),("roberta","MOHOM",0.98)]:
    chk(f"{m} {c} top-class share >= {lo}",1,int(v[(v.model==m)&(v.train==c)].oof_share_top_class.iloc[0]>=lo),0)
yp=pd.read_csv("/home/claude/p73res/v73_youleqd_paired.csv").set_index(["model","train"])
chk("DistilBERT SCAR-E diff vs const",-0.090,yp.loc[("distilbert","SCAR-E"),"diff_vs_const"],0.0005); chk("its CI hi",-0.013,yp.loc[("distilbert","SCAR-E"),"ci_hi"],0.0005)
chk("RoBERTa SCAR-I CI hi",-0.014,yp.loc[("roberta","SCAR-I"),"ci_hi"],0.0005); chk("RoBERTa SCAR-E CI hi",-0.005,yp.loc[("roberta","SCAR-E"),"ci_hi"],0.0005)
chk("min Holm p of three best",0.27,min(yp.loc[[("distilbert","SCAR-E"),("roberta","SCAR-I"),("roberta","SCAR-E")],"holm_boot_p"]),0.005)
chk("max Holm p of three best",0.45,max(yp.loc[[("distilbert","SCAR-E"),("roberta","SCAR-I"),("roberta","SCAR-E")],"holm_boot_p"]),0.005)
chk("MOHOM correct /70",0,yp.loc[("roberta","MOHOM"),"correct"],0); chk("LLM better than # models",12,int((yp.llm_ci_hi<0).sum()),0)
chk("LLM - DistilBERT SCAR-E",-0.057,yp.loc[("distilbert","SCAR-E"),"llm_minus_model"],0.0005); chk("its CI hi",0.034,yp.loc[("distilbert","SCAR-E"),"llm_ci_hi"],0.0005)
rp=pd.read_csv("/home/claude/p73res/v73_reproducibility_p70_vs_p73.csv"); chk("max |G0 diff| p70 vs p73",0.01,max(0.01,(rp.G0_lift_p70-rp.G0_lift_p73).abs().max()),0.0)
chk("max YLQ diff p70 vs p73",3,(rp.YLQ70_p70-rp.YLQ70_p73).abs().max(),0)

# ---- Phase 75 (v0.4) ----
r75=pd.read_csv("/home/claude/p75/p75_robustness.csv").set_index(["analysis","model"]).rho
p75=pd.read_csv("/home/claude/p75/p75_robustness.csv").set_index(["analysis","model"]).p
chk("balance vs TF-IDF T",0.90,r75[("balance (−majority share) vs T (descriptive)","tfidf")],0.005)
chk("partial both DistilBERT",0.67,r75[("partial | log size + majority share","distilbert")],0.005)
chk("partial both RoBERTa",0.81,r75[("partial | log size + majority share","roberta")],0.005)
chk("partial both TF-IDF p > .05",1,int(p75[("partial | log size + majority share","tfidf")]>0.05),0)
chk("partial both emb p > .05",1,int(p75[("partial | log size + majority share","emb")]>0.05),0)
for m in ["tfidf","emb","distilbert","roberta"]: chk(f"partial | size significant {m}",1,int(p75[("partial | log size",m)]<0.05),0)
chk("size-matched vs DistilBERT T",0.33,r75[("size-matched TF-IDF G0 (n=126) vs T","distilbert")],0.005)
chk("first-word vs DistilBERT T",0.57,r75[("first-word lookup lift (no training) vs T","distilbert")],0.005)
chk("first-word vs transformer p > .05",1,int(p75[("first-word lookup lift (no training) vs T","roberta")]>0.05),0)
sk=pd.read_csv("/home/claude/p75/p75_skill_transformers.csv").set_index("model")
chk("skill rho DistilBERT",0.83,sk.loc["distilbert","rho_skill"],0.005); chk("skill rho RoBERTa",0.93,sk.loc["roberta","rho_skill"],0.005)

# ---- Phase 76 and v0.5 Freedman–Lane / simulation ----
t76=pd.read_csv("/home/claude/p76res/out/p76_tests.csv").set_index("model")
chk("R3 DistilBERT rho",0.86,t76.loc["distilbert","rho"],0.005); chk("R3 DistilBERT p",0.005,t76.loc["distilbert","exact_p"],0.0005)
chk("R3 RoBERTa rho",0.83,t76.loc["roberta","rho"],0.005); chk("R3 RoBERTa p",0.008,t76.loc["roberta","exact_p"],0.0005)
v76=pd.read_csv("/home/claude/p76res/v76_recomputed.csv").set_index(["model","train"])
sh=[v76.loc[(m,c),"oof_share_top_class"] for m in ["distilbert","roberta"] for c in ["SANGO"]]; chk("SANGO top share min",0.34,min(sh),0.005); chk("SANGO top share max",0.36,max(sh),0.005)
sh=[v76.loc[(m,"MOHOM"),"oof_share_top_class"] for m in ["distilbert","roberta"]]; chk("MOHOM top share min",0.24,min(sh),0.005); chk("MOHOM top share max",0.29,max(sh),0.005)
cmp=pd.read_csv("/home/claude/p76res/v76_vs_p73.csv"); sm=cmp[cmp.corpus.isin(["SANGO","MOHOM"])]
chk("min dOOF small",0.42,sm.d_oof.min(),0.005); chk("max dOOF small",0.51,sm.d_oof.max(),0.005); chk("min dT small",0.18,sm.dT.min(),0.005); chk("max dT small",0.32,sm.dT.max(),0.005)
chk("all small CI lo > 0",1,int((sm.ci_lo>0).all()),0)
ref=cmp[cmp.corpus.isin(["EDUB","SCAR-I"])]; chk("unchanged corpora identical",0,ref.d_oof.abs().max()+ref.dT.abs().max(),0)
tf=pd.read_csv("/home/claude/p71/p71_gates_transfer.csv"); tf=tf[tf.model=="tfidf"].set_index("train").G0
for m in ["distilbert","roberta"]:
    g=cmp[cmp.model==m].set_index("corpus"); chk(f"{m} gate agreement P76",7,int((g.G0_76==tf.loc[g.index]).sum()),0); chk(f"{m} gate agreement P73",5,int((g.G0_73==tf.loc[g.index]).sum()),0)
gap=cmp[cmp.corpus.isin(["YAHYA","SANGO","MOHOM","EDUQG"])]; chk("gap min small",0.16,gap.gap_train_oof.min(),0.005); chk("gap max small",0.29,gap.gap_train_oof.max(),0.005)
ov=pd.read_csv("/home/claude/p76res/out/p76_overfitting.csv").set_index(["model","corpus"]); chk("train acc SANGO/MOHOM = 1",1,int(all(ov.loc[(m,c),"train_acc_cv_mean"]>0.995 for m in ["distilbert","roberta"] for c in ["SANGO","MOHOM"])),0)
eq=v76.xs("EDUQG",level="train").oof_share_top_class; chk("EDUQG P76 share min",0.81,eq.min(),0.005); chk("EDUQG P76 share max",0.82,eq.max(),0.005)
T11=pd.read_csv("/home/claude/p78/v05_table11.csv").set_index(["row","col"])
chk("TF-IDF ref P76 DistilBERT rho",0.86,T11.loc[("tfidf_reference","DistilBERT P76"),"rho"],0.005); chk("TF-IDF ref P76 RoBERTa rho",0.83,T11.loc[("tfidf_reference","RoBERTa P76"),"rho"],0.005)
chk("firstword P76 DistilBERT rho",0.83,T11.loc[("firstword","DistilBERT P76"),"rho"],0.005); chk("firstword P76 RoBERTa rho",0.81,T11.loc[("firstword","RoBERTa P76"),"rho"],0.005)
chk("firstword P76 max p",0.011,max(T11.loc[("firstword","DistilBERT P76"),"p"],T11.loc[("firstword","RoBERTa P76"),"p"]),0.0005)
chk("sizematched P76 p min",0.057,min(T11.loc[("sizematched","DistilBERT P76"),"p"],T11.loc[("sizematched","RoBERTa P76"),"p"]),0.0005)
chk("sizematched P76 p max",0.066,max(T11.loc[("sizematched","DistilBERT P76"),"p"],T11.loc[("sizematched","RoBERTa P76"),"p"]),0.0005)
both=[T11.loc[("fl_both",c),"p"] for c in ["TF-IDF","Embeddings","DistilBERT P76","RoBERTa P76"]]; chk("both-covariate p min (v0.5 family)",0.058,min(both),0.0005); chk("both-covariate p max",0.25,max(both),0.005)
chk("RoBERTa P73 both p",0.028,T11.loc[("fl_both","RoBERTa P73"),"p"],0.0005)
size=[T11.loc[("fl_size",c),"p"] for c in ["TF-IDF","Embeddings","DistilBERT P76","RoBERTa P76"]]; chk("size-controlled max p",0.042,max(size),0.0005)
fam=pd.read_csv("/home/claude/p78/fl_v05_family.csv"); chk("Holm TF-IDF size",0.022,fam[(fam.model=="tfidf")&(fam.control=="log size")].holm12.iloc[0],0.0005)
chk("only TF-IDF survives Holm",1,int((fam.holm12<0.05).sum()==1),0)
import re
sim=open("/home/claude/p78/fl_size_sim_results.txt").read(); vals=[(float(a),float(b),float(f)) for a,b,f in re.findall(r"rho\(x,Z1\)=([\d.]+) cov=\d beta_Z=([\d.]+): FL ([\d.]+)",sim)]
ok=[f for r,b,f in vals if r==0 or b==0]; lib=[f for r,b,f in vals if r>0 and b>0]
chk("sim FL valid min",0.045,min(ok),0.0005); chk("sim FL valid max",0.053,max(ok),0.0005); chk("sim FL liberal min",0.074,min(lib),0.0005); chk("sim FL liberal max",0.101,max(lib),0.0005)
sk=pd.read_csv("/home/claude/p78/v76_skill_exact.csv").set_index("model"); chk("skill P76 RoBERTa p",0.057,sk.loc["roberta","p"],0.0005); chk("skill P76 DistilBERT p",0.008,sk.loc["distilbert","p"],0.0005)
# strict rounding: every 3-dp stated value must equal round(actual, 3)
for r_ in R:
    if isinstance(r_["stated"],float) and 0<abs(r_["stated"])<1 and len(str(r_["stated"]).split(".")[-1])==3:
        r_["ok"]=r_["ok"] and (f"{r_['raw']:.3f}"==f"{r_['stated']:.3f}")
Q=pd.DataFrame(R); Q.to_csv("qc_numbers.csv",index=False); print(Q[~Q.ok].to_string() if (~Q.ok).any() else "ALL CHECKS PASSED"); print(len(Q),"checks")
