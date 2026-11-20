"""Phase 70 LLM validation, part 1: recompute metrics, cross-file consistency, sampling, label mapping, leakage checks."""
import numpy as np, pandas as pd, hashlib, corpora as C
S=pd.read_csv("p70_llm.csv").iloc[0]; D=pd.read_csv("p70_llm_detailed.csv"); A=pd.read_csv("p70_llm_abstentions.csv")
print("rows per dataset:",D.dataset.value_counts().to_dict())
# 1. recompute accuracy / coverage / abstentions
out=[]
for ds,g in D.groupby("dataset",sort=False):
    if ds=="LAK40":
        refs=g.reference_set.map(eval); corr=np.array([(p in s) if v else False for p,s,v in zip(g.prediction,refs,g.valid_prediction)])
    else: corr=((g.prediction==g.reference_label)&g.valid_prediction).to_numpy()
    n=len(g); nv=int(g.valid_prediction.sum())
    out.append(dict(dataset=ds,n=n,valid=nv,abst=n-nv,coverage=nv/n,acc_overall=corr.sum()/n,acc_conditional=corr.sum()/nv,
                    reported_acc=S[ds],reported_cov=S[f"{ds}_coverage"],reported_abst=S[f"{ds}_abstentions"],
                    stored_correct_matches=bool((g.correct.to_numpy()==corr).all())))
R=pd.DataFrame(out); print(R.round(4).to_string(index=False))
print("reported acc equals overall (abstention counted wrong):",bool(np.allclose(R.acc_overall,R.reported_acc)))
# 2. cross-file consistency
ab=D[D.status=="abstention"]; print("abstentions in detailed:",len(ab)," in abstentions file:",len(A)," match on hash:",set(ab.question_hash)==set(A.question_hash))
print("hash = sha256(question)? ", (D.question.map(lambda s:hashlib.sha256(str(s).encode()).hexdigest())==D.question_hash).mean())
print("unique question hashes:",D.question_hash.nunique(),"of",len(D),"| reported cached predictions + abstentions:",S.total_cached_predictions+S.total_cached_abstentions)
dup=D[D.question_hash.duplicated(keep=False)].sort_values("question_hash"); print("duplicated questions across rows:",len(dup)); print(dup[["dataset","item_index","prediction","reference_label"]].head(12).to_string(index=False))
# 3. sampling: reproduce rg = default_rng(70); DASQ choice(500), then SCAR-E choice(500); EDUQG all; YLQ70; LAK40
corp={"DASQ":C.dasq(),"SCAR-E":C.scar_e(),"EDUQG":C.eduqg()}; yq,V=C.youleqd(); lk=C.lak()
rg=np.random.default_rng(70); idx={"DASQ":rg.choice(len(corp["DASQ"]),500,replace=False),"SCAR-E":rg.choice(len(corp["SCAR-E"]),500,replace=False)}
for ds in ["DASQ","SCAR-E","EDUQG","YLQ70","LAK40"]:
    g=D[D.dataset==ds].reset_index(drop=True)
    if ds in idx: ref=corp[ds].iloc[idx[ds]].reset_index(drop=True)
    elif ds=="EDUQG": ref=corp[ds]
    elif ds=="YLQ70": ref=yq
    else: ref=lk
    same_text=(g.question.astype(str).str.strip()==ref.text.astype(str).str.strip()).mean()
    same_lab=(g.reference_label.to_numpy()==ref.y.to_numpy()).mean() if ds!="LAK40" else (g.reference_set.map(eval).tolist()==ref.refs.tolist())
    print(f"{ds}: item text matches notebook sampling {same_text:.4f}; labels match {same_lab}; item_index == position {bool((g.item_index==(idx[ds] if ds in idx else np.arange(len(g)))).all())}")
R.to_csv("val_recomputed_metrics.csv",index=False)
