"""QC: recompute every key manuscript number from archived outputs and compare with the value stated in the text."""
import numpy as np, pandas as pd, re, corpora as C
from sklearn.metrics import cohen_kappa_score
EX=C.EX; R=[]
def chk(claim,stated,actual,tol):
    R.append(dict(claim=claim,stated=stated,recomputed=round(float(actual),4),ok=abs(float(actual)-stated)<=tol))
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
b=pd.read_csv("/home/claude/p58/p60_e1_cluster_bootstrap.csv").iloc[0]; chk("H1 diff (pp)",-2.9,100*b["diff"],0.05); chk("H1 CI lo",-12.2,100*b.ci_lo,0.05); chk("H1 CI hi",6.9,100*b.ci_hi,0.05)
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
    chk(f"{k} G0 lift (pp)",lift,100*gt.loc[k,"G0_lift"],0.05); chk(f"{k} transfer (%)",T,100*gt.loc[k,"T"],0.05)
p70=pd.read_csv("/home/claude/p70res/p70_tests.csv").set_index("model"); chk("H9a rho",0.70,p70.loc["distilbert","rho"],0.005); chk("H9c p",0.175,p70.loc["roberta","exact_p"],0.0005)
h=pd.read_csv("/home/claude/p70llm/val_h10_robustness.csv"); chk("H10 diff",-0.148,h.iloc[0]["diff"],0.0005); chk("H10 CI lo",-0.233,h.iloc[0].ci_lo,0.0005); chk("H10 CI hi",-0.065,h.iloc[0].ci_hi,0.0005)
sk=pd.read_csv("/home/claude/p70llm/val_skill_over_majority.csv").set_index("dataset"); chk("LLM EduQG skill (pp)",-4.1,100*sk.loc["EDUQG","skill"],0.05)
pc=pd.read_csv("/home/claude/p70llm/val_paired_comparisons.csv"); chk("Smallest Holm p",0.21,pc.mcnemar_p_holm.min(),0.005)
Q=pd.DataFrame(R); Q.to_csv("qc_numbers.csv",index=False); print(Q[~Q.ok].to_string() if (~Q.ok).any() else "ALL CHECKS PASSED"); print(len(Q),"checks")
