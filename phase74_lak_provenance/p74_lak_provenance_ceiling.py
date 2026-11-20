"""Phase 74 (descriptive): LAK40 provenance verification and human ceiling from the source file's two annotators.
Source: AEQUITAS-Lab/Data-Annotation-LAK-2026 @91de3c38, human_annotation/Bloom-All_40.csv (sha256 e50005a1...)."""
import pandas as pd, numpy as np, re
from sklearn.metrics import cohen_kappa_score
d=pd.read_csv("Bloom-All_40.csv"); L=["Remember","Understand","Apply","Analyze","Evaluate","Create"]
sets={a:g.set_index("ID")[L].apply(lambda r:frozenset(l for l in L if r[l]==1),axis=1) for a,g in d.groupby("Annotator")}
gt,a1,a2=sets["groundtruth"],sets["A1"],sets["A2"]
print("label counts per annotator:",{k:int(v.map(len).sum()) for k,v in sets.items()},"| multi-label:",{k:int((v.map(len)>1).sum()) for k,v in sets.items()})
single=lambda s:s.map(lambda x:min(x,key=L.index) if len(x) else "none")
for name,a in [("A1",a1),("A2",a2)]:
    hit=np.mean([len(a[i]&gt[i])>0 for i in gt.index]); print(f"{name} vs groundtruth: set-overlap agreement {hit:.3f}")
print(f"A1 vs A2 exact-set agreement {np.mean([a1[i]==a2[i] for i in gt.index]):.3f}; kappa (first label) {cohen_kappa_score(single(a1),single(a2)):.3f}")
for name,a in [("A1",a1),("A2",a2)]: print(f"kappa {name} vs groundtruth (first label): {cohen_kappa_score(single(a),single(gt)):.3f}")
ours=pd.read_csv("/home/claude/bt/ex/Phase48_Final_LR/lak_matched_models.csv")
print("our LAK40 IDs == groundtruth IDs:",sorted(ours.ID)==sorted(gt.index))
