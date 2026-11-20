"""Creates scaria_all.pkl and eduqg_all.pkl exactly as used in Phases 65-68."""
import glob, json, pandas as pd
tot=[]
for f in sorted(glob.glob("AEQG_Blooms_Evaluation_LLMs/generated_questions/PS*_ExpertEvaluation.xlsx")):
    d=pd.read_excel(f); d.columns=[c.strip() for c in d.columns]
    d["grp"]=d.Prompt.notna().cumsum(); d["pos"]=d.groupby("grp").cumcount(); d["ps"]=f.split("/")[-1][:3]; tot.append(d)
d=pd.concat(tot,ignore_index=True); d["Model"]=d.Model.str.strip().str.replace("LLama","Llama")
assert d.groupby(["ps","grp",d.pos//6]).Model.nunique().max()==1   # intended level = pos % 6 + 1
d.to_pickle("scaria_all.pkl")
rows=[]
for split in ["train","valid"]:
    for ch in json.load(open(f"question-generation/raw_data/qg_{split}_v0.json")):
        for q in ch["questions"]:
            rows.append(dict(split=split,book=ch.get("bname"),chapter=ch.get("chapter"),
                             text=q["question"].get("normal_format") or q["question"].get("question_text"),bloom=q.get("bloom"),qid=q["question"].get("question_id")))
pd.DataFrame(rows).to_pickle("eduqg_all.pkl"); print("ok")
