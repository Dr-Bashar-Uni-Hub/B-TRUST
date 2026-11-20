"""Shared corpus loaders for Phases 65-68 (preregistered sha256 6c60ecc9...). All labels -> revised 1..6."""
import re, numpy as np, pandas as pd
import os
EX=os.environ.get("BTRUST_EX","/home/claude/bt/ex")
norm=lambda s: re.sub(r"\s+"," ",str(s).lower()).strip()
ORIG={"knowledge":1,"comprehension":2,"application":3,"analysis":4,"evaluation":5,"synthesis":6}
REVN={"remember":1,"understand":2,"apply":3,"analyze":4,"evaluate":5,"create":6}
def _fin(d): d=d[d.text.map(lambda s: isinstance(s,str) and len(s.strip())>0)].copy(); d["n"]=d.text.map(norm); return d.reset_index(drop=True)
def edub():
    q=pd.read_csv(f"{EX}/Phase42_Results/phase42/questions.csv").sample(2550,random_state=65)
    d=pd.DataFrame({"text":q.question.values,"y":q.bloom_level.str[1].astype(int).values,"meta":(q.difficulty+"|"+q.question_type).values}); return _fin(d)
def dasq():
    d=pd.read_csv("DASQBT/combined.csv"); d=pd.DataFrame({"text":d.QUESTION,"y":d["BT LEVEL"].str.strip().str.lower().map(ORIG)})
    d=_fin(d); return d.drop_duplicates("n").reset_index(drop=True)
def scaria_raw():
    d=pd.read_pickle("scaria_all.pkl"); d=d.rename(columns={"Questions":"text"})
    d["intended"]=d.pos%6+1
    for k in (1,2): d[f"e{k}"]=d[f"SkillLevel_{k}"].where(d[f"SkillLevel_{k}"].between(1,6))
    d["consensus"]=np.where(d.e1.notna()&d.e2.notna()&(d.e1==d.e2),d.e1,np.nan)
    return _fin(d)
def scar_i():
    d=scaria_raw(); d["y"]=d.intended; return d
def scar_e():
    d=scaria_raw(); d=d[d.consensus.notna()].copy(); d["y"]=d.consensus.astype(int); return d.reset_index(drop=True)
def eduqg():
    d=pd.read_pickle("eduqg_all.pkl"); d=d[d.bloom.isin(["1","2","3","4"])]
    d=pd.DataFrame({"text":d.text.values,"y":d.bloom.astype(int).values}); return _fin(d)
def youleqd():
    r=pd.read_csv(f"{EX}/Phase42_Results/phase42/record_level_predictions.csv")
    for c in ["label","lebel1","lebel2","lebel3"]: r[c]=r[c].astype(str).str.strip().str.lower()
    r=r[r.label!="irrelevant"].copy()
    d=pd.DataFrame({"text":r.text.fillna("").values,"y":r.label.map(ORIG).values,"vid":r.vid.values})
    V=r[["lebel1","lebel2","lebel3"]].apply(lambda s:s.map(ORIG)).to_numpy(float)  # irrelevant -> nan, never matches
    d=_fin(d); return d, V
def lak():
    l=pd.read_csv(f"{EX}/Phase48_Final_LR/lak_matched_models.csv")
    refs=l.reference_labels.map(eval).map(lambda s:{REVN[x.lower()] for x in s})
    d=pd.DataFrame({"text":l.Learning_outcome.values,"refs":refs.values}); return _fin(d)
def model():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    return make_pipeline(TfidfVectorizer(ngram_range=(1,2),min_df=2,max_features=50000),LogisticRegression(C=1.0,max_iter=2000))
