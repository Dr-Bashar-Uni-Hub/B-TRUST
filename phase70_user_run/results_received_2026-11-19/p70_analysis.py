"""Analysis of researcher-run Phase 70 outputs (preregistered H9a-H9d in the Phase 70 notebook, sha256 6fd8d2e6...)."""
import pandas as pd, numpy as np, itertools
from scipy.stats import spearmanr
rows=[]
for m in ["distilbert","roberta"]:
    G=pd.read_csv(f"p70_G0_{m}.csv"); T=pd.read_csv(f"p70_transfer_{m}.csv")
    x=T.G0_lift.to_numpy(); y=T.T_mean.to_numpy(); obs=spearmanr(x,y).statistic
    p=np.mean([spearmanr(x,np.array(q)).statistic>=obs-1e-12 for q in itertools.permutations(y)])
    fail=T[T.train.isin(G[G.G0=="FAIL"].corpus)].T_mean; ok=T[T.train.isin(G[G.G0=="PASS"].corpus)].T_mean
    rows.append(dict(model=m,rho=obs,exact_p=p,H_rho_supported=p<0.05,identical_G0=bool(G.same_as_tfidf.all()),
                     min_PASS_T=ok.min(),max_FAIL_T=fail.max(),PASS_above_all_FAIL=bool(ok.min()>fail.max()),
                     best_YLQ70=T.YLQ70.max(),best_YLQ70_train=T.loc[T.YLQ70.idxmax(),"train"]))
R=pd.DataFrame(rows); R.to_csv("p70_tests.csv",index=False); print(R.round(4).to_string(index=False))
