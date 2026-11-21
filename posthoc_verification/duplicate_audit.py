"""Duplicate and overlap audit (Supplementary S7 and Table S8 counts). Run from the directory with corpora.py and its inputs."""
import sys, pandas as pd
sys.path.insert(0, "."); import corpora as C
rows = []
for k, d in [("EDUB", C.edub()), ("SCAR-I", C.scar_i()), ("SCAR-E", C.scar_e()), ("EDUQG", C.eduqg())]:
    g = d.groupby("n").y.nunique(); conflicting = int((g > 1).sum())
    rows.append(dict(config=k, rows_analysed=len(d), unique_texts=d.n.nunique(), surplus_copies=len(d) - d.n.nunique(),
                     texts_with_conflicting_labels=conflicting, rows_after_dedup_rule=d.n.nunique() - conflicting))
for k, f in [("YAHYA", "yahya-2012_revised.csv"), ("SANGO", "Sangodiah_2017_415_revised.csv"), ("MOHOM", "Mohammed-and-Omar_2020_126_revised.csv"), ("GANI", "Gani_2023_collected-dataset-1200_revised.csv")]:
    n = pd.read_csv(f).QUESTION.map(C.norm)
    rows.append(dict(config=k, rows_analysed=n.nunique(), unique_texts=n.nunique(), surplus_copies=0, texts_with_conflicting_labels=0, rows_after_dedup_rule=n.nunique(), raw_file_rows=len(n)))
R = pd.DataFrame(rows); R.to_csv("duplicate_audit.csv", index=False); print(R.to_string(index=False))
si, se = set(C.scar_i().n), set(C.scar_e().n); print(f"SCAR-E unique {len(se)}; contained in SCAR-I unique {len(si)}: shared {len(si & se)} ({len(si & se)/len(si):.1%} of SCAR-I)")
