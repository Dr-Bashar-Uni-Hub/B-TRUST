from pathlib import Path
import pandas as pd, numpy as np, json
from sklearn.metrics import roc_auc_score,average_precision_score,brier_score_loss
p=Path(__file__).resolve().parent
d=pd.read_csv(p/'scar_hashed_oof_predictions.csv');y=d['disagree'].to_numpy(dtype=int);n=len(y);k=int(np.ceil(.2*n))
print('n',n,'disagreements',sum(y),'budget',k)
for name,col in [('text','p_text_oof'),('length','p_length_oof')]:
 s=d[col].to_numpy();ix=np.argsort(-s,kind='stable')[:k];found=int(y[ix].sum())
 print(name,{'AUROC':roc_auc_score(y,s),'AP':average_precision_score(y,s),'Brier':brier_score_loss(y,s),'found':found,'precision':found/k,'recall':found/sum(y)})
print('random expected',k*sum(y)/n)
