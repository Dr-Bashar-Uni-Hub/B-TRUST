"""Phase 58 audit (consolidated from the interactive audit). Usage: python3 phase58_audit.py <EX>
EX = folder containing the extracted v1.0 phase archives (default /home/claude/bt/ex)."""
import sys, joblib, numpy as np, pandas as pd, warnings
from sklearn.metrics import cohen_kappa_score
warnings.filterwarnings("ignore"); EX=sys.argv[1] if len(sys.argv)>1 else "/home/claude/bt/ex"
m=joblib.load(f"{EX}/Phase48_Final_LR/original_lr_model.joblib")
r=pd.read_csv(f"{EX}/Phase42_Results/phase42/record_level_predictions.csv"); r["text"]=r.text.fillna("").astype(str)
i=pd.read_csv(f"{EX}/Phase42_Results/phase42/internal_predictions.csv"); q=pd.read_csv(f"{EX}/Phase42_Results/phase42/questions.csv")
print("[2.1] LR reproduces YouLeQD preds:",(m.predict(r.text)==r.lr_prediction).mean()," internal preds:",(m.predict(i.question)==i.lr_prediction).mean())
print("[2.1] internal acc LR/DB:",(i.lr_prediction==i.bloom_level).mean(),(i.distilbert_prediction==i.bloom_level).mean())
print("[2.2] internal test class counts:",i.bloom_level.value_counts().sort_index().to_dict())
print("[2.2] difficulty x level:\n",pd.crosstab(q.difficulty,q.bloom_level))
q["t"]=[a.replace(b,"<T>") for a,b in zip(q.question,q.topic)]
print("[2.2] templates:",q.t.nunique()," with >1 label:",round((q.groupby("t").bloom_level.nunique()>1).mean(),4))
im=i.merge(q[["question","difficulty"]],on="question"); best=im.groupby("difficulty").bloom_level.agg(lambda s:s.value_counts().idxmax())
print("[2.2] metadata-only (difficulty) accuracy on internal test:",(im.difficulty.map(best)==im.bloom_level).mean())
print("[2.2] DistilBERT internal prediction counts:",i.distilbert_prediction.value_counts().sort_index().to_dict())
mp={f"L{k+1}":v for k,v in enumerate(["knowledge","comprehension","application","analysis","evaluation","synthesis"])}
rel=r[r.consolidated_relevant]; y=rel.label.str.lower()
for c in ["lr_prediction","distilbert_prediction"]:
    p=rel[c].map(mp); print(f"[2.3] {c} relevant70 acc={(p==y).mean():.4f} kappa={cohen_kappa_score(y,p):.4f}")
print("[2.3] majority 'comprehension':",round((y=="comprehension").mean(),4))
V=r[["lebel1","lebel2","lebel3"]].apply(lambda s:s.astype(str).str.strip().str.lower()).to_numpy(); relm=(r.label.str.lower()!="irrelevant").to_numpy()
for c in ["lr_prediction","distilbert_prediction"]:
    p=r[c].map(mp).to_numpy(); d=(V!=p[:,None])
    print(f"[2.4] {c}: P(disagree>=1 annotator|relevant)={d.any(1)[relm].mean():.4f}  items all-3-agree={int((d.mean(1)==0).sum())}")
H=np.mean([(V[:,j]!=V[:,k]) for j in range(3) for k in range(3) if j!=k],0); print("[2.5] human LOO G6 vote loss, relevant:",round(H[relm].mean(),4))
