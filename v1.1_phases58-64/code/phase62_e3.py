"""Phase 62 / E3 — validity and power of row-level vs video-level one-sided risk certification under clustering.
Semi-synthetic: cluster sizes resampled from the real YouLeQD video-size distribution. Preregistered."""
import numpy as np, pandas as pd
from scipy.stats import beta
from scipy.special import expit, logit
r=pd.read_csv("/home/claude/bt/ex/Phase42_Results/phase42/record_level_predictions.csv")
sizes=r.vid.value_counts().to_numpy(); print("videos",len(sizes),"size dist",np.bincount(sizes)[1:].tolist())
rng=np.random.default_rng(62); ALPHA=0.5; DELTA=0.1; NS=4000
def sigma_for_icc(icc): return np.sqrt(icc/(1-icc)*np.pi**2/3) if icc>0 else 0.0
def mu_for_risk(target,s):  # latent intercept giving marginal mean = target
    z=np.random.default_rng(0).normal(size=200000)*s; lo,hi=-10,10
    for _ in range(60):
        m=(lo+hi)/2; (lo,hi)=(m,hi) if expit(m+z).mean()<target else (lo,m)
    return (lo+hi)/2
rows=[]
for icc in [0.0,0.2,0.5]:
    s=sigma_for_icc(icc)
    for true in [ALPHA, ALPHA-0.1, ALPHA-0.2]:
        mu=mu_for_risk(true,s)
        for J in [30,60,120,236,500,1000]:
            cert=np.zeros((NS,3),bool)
            for k in range(NS):
                n=rng.choice(sizes,J); u=rng.normal(0,s,J)
                p=np.repeat(expit(mu+u),n); l=rng.random(p.size)<p
                N=l.size; K=l.sum()
                cert[k,0]=K/N+np.sqrt(np.log(1/DELTA)/(2*N))<ALPHA                      # row Hoeffding
                cert[k,1]=(beta.ppf(1-DELTA,K+1,N-K) if K<N else 1.0)<ALPHA             # row Clopper-Pearson
                vm=np.add.reduceat(l.astype(float),np.r_[0,np.cumsum(n)[:-1]])/n        # per-video mean loss
                cert[k,2]=(vm-ALPHA).mean()+np.sqrt(np.log(1/DELTA)/(2*J))<0             # video-level Hoeffding
            rate=cert.mean(0)
            rows.append(dict(icc=icc,true_risk=true,videos=J,mean_items=float(J*sizes.mean()),
                             row_hoeffding=rate[0],row_cp=rate[1],video_hoeffding=rate[2]))
            print(rows[-1])
d=pd.DataFrame(rows); d.to_csv("p62_e3_simulation.csv",index=False)
null=d[d.true_risk==ALPHA]; mc=2*np.sqrt(DELTA*(1-DELTA)/NS)
print("\nNULL (true risk = cap): false-certification rates; limit δ=0.1 (+2SE=%.3f)"%(DELTA+mc))
print(null.pivot_table(index=["icc","videos"],values=["row_hoeffding","row_cp","video_hoeffding"]).round(4))
v_ok=(null.video_hoeffding<=DELTA+mc).all()
row_bad=((null.icc>=0.2)&((null.row_hoeffding>DELTA+mc)|(null.row_cp>DELTA+mc))).any()
print("H3 video-level valid in all cells:",bool(v_ok)," | some row-level test invalid at ICC>=0.2:",bool(row_bad)," => H3 supported:",bool(v_ok and row_bad))
