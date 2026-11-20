"""Phase 70 LLM validation, part 5: attempt to reconstruct the checkpoint key (question_hash) from plausible constructions.
Result 2026-11-19: no match among 1,378 constructions (sha256/sha1/md5/blake2b/sha3 over question text, prompt+text, model/settings
prefixes, dataset prefixes, JSON request dicts). Identical texts share one key and one prediction (8 groups)."""
import hashlib, json, pandas as pd
D=pd.read_csv("p70_llm_detailed.csv"); g=D.groupby("question_hash")
print("keys:",D.question_hash.nunique(),"| keys shared by >1 row:",int((g.size()>1).sum()),
      "| all shared keys have identical text and prediction:",bool(all(x.question.nunique()==1 and x.prediction.nunique()==1 for _,x in g if len(x)>1)))
