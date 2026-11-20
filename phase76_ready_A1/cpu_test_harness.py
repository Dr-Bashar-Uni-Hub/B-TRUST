import json, os, platform, numpy as np, pandas as pd, time, sys
sys.path.insert(0,"/home/claude/p71")
nb=json.load(open('/home/claude/p76f/Phase76_StepsMatched_Robustness_A1.ipynb')); src=[c['source'] for c in nb['cells'] if c['cell_type']=='code']
FARAJI='/home/claude/BTRUST_v2.3_Provenance_2026-11-19/v2.2_phase71_and_checkpoint/data_faraji_MIT'
OUT='/tmp/p76_real'; os.makedirs(OUT,exist_ok=True); SAVE_FULL_FIT_WEIGHTS=True; SAVE_CV_FOLD_WEIGHTS=False
import torch, transformers
class _F:
    @staticmethod
    def download(p): print("[download]",p, os.path.getsize(p),"bytes", flush=True)
files=_F(); display=lambda d: print(d.to_string()[:1800], flush=True)
exec(src[1])
for k in list(corp):
    d=corp[k]; idx=np.concatenate([g.index.values[:7] for _,g in d.groupby("y")]); corp[k]=d.loc[np.sort(idx)].reset_index(drop=True)
print({k:len(v) for k,v in corp.items()}, flush=True)
exec(src[2]); MIN_STEPS=3; LOCAL='/home/claude/up/ckpt/Phase42_DistilBERT_Checkpoint'; t0=time.time()
exec(src[3].replace('for name, short in [("distilbert-base-uncased", "distilbert"), ("roberta-base", "roberta")]: run(name, short)','run(LOCAL,"distilbert")'))
print("run time %.0fs"%(time.time()-t0), flush=True); exec(src[4].replace('for short in ["distilbert", "roberta"]:', 'for short in ["distilbert"]:'))
fs=sorted(os.listdir(OUT)); print("top-level files:",len(fs)); print([f for f in fs if not f.startswith(('gate_','oof_','items_','diag_'))])
md=os.path.join(OUT,'models','full'); ex=sorted(os.listdir(md))[0]; print("saved full-fit models:",len(os.listdir(md)),"| files in",ex,":",sorted(os.listdir(os.path.join(md,ex))))
print(open(os.path.join(md,ex,'b_trust_training_config.json')).read()[:420]); print(open(f"{OUT}/diag_distilbert_SANGO.jsonl").readline()[:300])
print("TEST COMPLETE", flush=True)
