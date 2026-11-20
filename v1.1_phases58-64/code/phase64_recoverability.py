"""Phase 64 (EXPLORATORY, not preregistered) — label-recoverability audit applied to EduBloom and DASQBT.
Question: does the audit discriminate, i.e. does a human-authored dataset show text-recoverable labels where EduBloom does not?"""
import re, numpy as np, pandas as pd, warnings
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import cohen_kappa_score
warnings.filterwarnings("ignore")
norm=lambda s:re.sub(r"\s+"," ",str(s).lower()).strip()
def cv_text(X,y,seed=64,k=5):
    pred=np.empty(len(y),dtype=object)
    for a,b in StratifiedKFold(k,shuffle=True,random_state=seed).split(X,y):
        m=make_pipeline(TfidfVectorizer(ngram_range=(1,2),min_df=2,max_features=50000),LogisticRegression(max_iter=2000)).fit(X[a],y[a])
        pred[b]=m.predict(X[b])
    return pred
def first_verb_lookup(fw,y,seed=64,k=5):   # out-of-fold majority label for first word
    pred=np.empty(len(y),dtype=object); maj=pd.Series(y).mode()[0]
    for a,b in StratifiedKFold(k,shuffle=True,random_state=seed).split(fw,y):
        tab=pd.DataFrame({"f":fw[a],"y":y[a]}).groupby("f").y.agg(lambda s:s.mode()[0])
        pred[b]=pd.Series(fw[b]).map(tab).fillna(maj).to_numpy()
    return pred
def boot_ci(correct,B=5000,seed=64):
    rg=np.random.default_rng(seed); n=len(correct); return np.percentile([correct[rg.integers(0,n,n)].mean() for _ in range(B)],[2.5,97.5])
rows=[]
def report(name,y,preds):
    maj=pd.Series(y).value_counts(normalize=True).iloc[0]
    for k,p in preds.items():
        c=(p==y).astype(float); lo,hi=boot_ci(c)
        rows.append(dict(dataset=name,n=len(y),predictor=k,acc=c.mean(),ci_lo=lo,ci_hi=hi,majority=maj,
                         lift_over_majority=c.mean()-maj,kappa=cohen_kappa_score(y,p)))
# DASQBT (deduplicated, human-authored)
d=pd.read_csv("DASQBT/combined.csv"); d["n"]=d.QUESTION.map(norm); d["y"]=d["BT LEVEL"].str.strip().str.lower(); d=d.drop_duplicates("n").reset_index(drop=True)
X=d.n.to_numpy(); y=d.y.to_numpy(); fw=d.n.str.split().str[0].fillna("").to_numpy()
report("DASQBT",y,{"text_LR_5fold":cv_text(X,y),"first_word_lookup":first_verb_lookup(fw,y)})
# EduBloom: random stratified subsample of the same size as DASQBT to equalise data quantity, plus full-size reference already in Phase 58
q=pd.read_csv("/home/claude/bt/ex/Phase42_Results/phase42/questions.csv")
qs=q.sample(len(d),random_state=64).reset_index(drop=True)
Xq=qs.question.map(norm).to_numpy(); yq=qs.bloom_level.to_numpy(); fwq=pd.Series(Xq).str.split().str[0].to_numpy()
meta=(qs.difficulty+"|"+qs.question_type).to_numpy()
report("EduBloom_sizematched",yq,{"text_LR_5fold":cv_text(Xq,yq),"first_word_lookup":first_verb_lookup(fwq,yq),
                                  "metadata_only_lookup(difficulty+type)":first_verb_lookup(meta,yq)})
out=pd.DataFrame(rows); out.to_csv("p64_recoverability.csv",index=False); print(out.round(4).to_string(index=False))
# Label consistency of exact-duplicate texts (DASQBT pre-dedup) vs stem consistency (EduBloom)
raw=pd.read_csv("DASQBT/combined.csv"); raw["n"]=raw.QUESTION.map(norm); raw["y"]=raw["BT LEVEL"].str.strip().str.lower()
dup=raw[raw.n.duplicated(keep=False)].groupby("n").y.nunique()
print(f"\nDASQBT duplicated texts: {len(dup)}; with conflicting labels: {(dup>1).sum()}")
q["t"]=[a.replace(b,"<T>") for a,b in zip(q.question,q.topic)]
gt=q.groupby("t").bloom_level.nunique(); print(f"EduBloom templates (topic removed): {len(gt)}; with >1 label: {(gt>1).mean():.3f} of templates")
