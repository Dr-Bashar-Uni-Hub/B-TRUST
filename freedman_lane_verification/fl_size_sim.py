"""Type I error of Freedman–Lane (FL) vs the original Phase 75 residual-permutation (RP) test at k = 8 (ranks), alpha = 0.05 one-sided.
Null: y depends on Z only. FL statistic per permutation = corr(e_x, M e_y[pi]) with M = I - X(X'X)^-1 X' (M annihilates fitted values).
3,000 datasets per scenario x 2,000 random permutations."""
import numpy as np
from scipy.stats import rankdata
rng=np.random.default_rng(78); k=8; B=2000; R=3000
def corr_rows(a,Bm):
    a=a-a.mean(); Bm=Bm-Bm.mean(1,keepdims=True); den=np.sqrt((a**2).sum()*(Bm**2).sum(1)); 
    with np.errstate(invalid="ignore",divide="ignore"): return np.where(den>0,(Bm@a)/den,-np.inf)
def run(rho,nc,bz):
    rf=rr=0
    for _ in range(R):
        Z=[rng.normal(size=k) for _ in range(nc)]; x=rho*Z[0]+np.sqrt(1-rho**2)*rng.normal(size=k); y=bz*Z[0]+rng.normal(size=k)
        x,y=rankdata(x),rankdata(y); X=np.column_stack([np.ones(k)]+[rankdata(z) for z in Z]); M=np.eye(k)-X@np.linalg.pinv(X)
        ex,ey=M@x,M@y; obs=corr_rows(ex,ey[None,:])[0]
        P=np.argsort(rng.random((B,k)),axis=1); EY=ey[P]
        rr+=np.mean(corr_rows(ex,EY)>=obs-1e-12)<=0.05; rf+=np.mean(corr_rows(ex,EY@M.T)>=obs-1e-12)<=0.05
    return rf/R, rr/R
print("alpha 0.05 one-sided; Monte Carlo SE ~0.004")
for rho in [0.0,0.65,0.93]:
    for nc in [1,2]:
        for bz in [0.0,1.5]:
            f,r=run(rho,nc,bz); print(f"rho(x,Z1)={rho:.2f} cov={nc} beta_Z={bz}: FL {f:.3f} | original {r:.3f}",flush=True)
