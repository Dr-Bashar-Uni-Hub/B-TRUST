import numpy as np,pandas as pd
exec(open("phase63_e4.py").read().split("rows=[]")[0])
out=[]
for seed in range(12):
    traincal,test=next(GroupShuffleSplit(1,test_size=.25,random_state=seed).split(r,y,vid))
    a,b=next(GroupShuffleSplit(1,test_size=.33,random_state=100+seed).split(r.iloc[traincal],y[traincal],vid[traincal]))
    tr,cal=traincal[a],traincal[b]; m=fitrel(tr); relp=np.zeros(len(r)); relp[cal]=m.predict_proba(r.text.iloc[cal])[:,1]
    best=(1.0,None)
    for tau in [0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.0]:
        for t in np.round(np.arange(0.95,-0.01,-0.05),2):
            acc,loss,w=decide(t,relp>=tau)
            if acc[cal].sum()==0: continue
            p=max(pval(np.where(acc,loss-A1,0.0),cal),pval(np.where(acc,(1-y)-A2,0.0),cal))
            if p<best[0]: best=(p,(tau,t,int(acc[cal].sum()),loss[cal][acc[cal]].mean(),(1-y[cal])[acc[cal]].mean()))
    out.append(dict(seed=seed,min_p_over_grid=best[0],argmin=best[1]))
d=pd.DataFrame(out); print(d.to_string(index=False)); print("any lambda with p<=0.1 (optimistic, no multiplicity):",bool((d.min_p_over_grid<=0.1).any()))
d.to_csv("p63_diag_min_p.csv",index=False)
