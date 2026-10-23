import numpy as np,pandas as pd
from scipy import stats as st
RNG=np.random.default_rng(7)
IS=('2012-01-01','2018-12-31'); OOS=('2019-01-01','2026-12-31')
def mean_test(x,block=1,B=4000):
    """H0 mean=0. t-test + (block) bootstrap of the mean (centered). returns mean,t,p_t,p_boot,n"""
    x=pd.Series(x).dropna().values; n=len(x)
    if n<4: return dict(mean=np.nan,t=np.nan,p_t=np.nan,p_boot=np.nan,n=n)
    m=x.mean(); se=x.std(ddof=1)/np.sqrt(n); t=m/se if se>0 else np.nan; pt=2*st.t.sf(abs(t),n-1)
    xc=x-m; nb=int(np.ceil(n/block)); idx=RNG.integers(0,n,(B,nb))
    bm=np.stack([xc[(idx+k)%n] for k in range(block)],axis=2).reshape(B,-1)[:,:n].mean(1)
    pb=(np.abs(bm)>=abs(m)).mean()
    return dict(mean=m,t=t,p_t=pt,p_boot=max(pb,1/B),n=n)
def diff_test(y,flag,B=None):
    """H0: mean(y|flag)=mean(y|~flag). Welch t + circular-shift permutation of flag (keeps regime persistence)."""
    d=pd.DataFrame({'y':y,'f':flag}).dropna(); y_=d.y.values; f=d.f.values.astype(bool); n=len(y_)
    if f.sum()<3 or (~f).sum()<3: return dict(mean=np.nan,t=np.nan,p_t=np.nan,p_boot=np.nan,n=int(f.sum()),m_in=np.nan,m_out=np.nan)
    obs=y_[f].mean()-y_[~f].mean(); t,pt=st.ttest_ind(y_[f],y_[~f],equal_var=False)
    sh=[np.roll(f,k) for k in range(1,n)]; ds=np.array([y_[s].mean()-y_[~s].mean() for s in sh if 0<s.sum()<n])
    pb=((np.abs(ds)>=abs(obs)).sum()+1)/(len(ds)+1)
    return dict(mean=obs,t=t,p_t=pt,p_boot=pb,n=int(f.sum()),m_in=y_[f].mean(),m_out=y_[~f].mean())
def sub(s,per):
    return s.loc[per[0]:per[1]]
def bh(p):
    p=np.asarray(p,float); m=np.isfinite(p).sum(); o=np.argsort(np.where(np.isfinite(p),p,9)); q=np.full(len(p),np.nan); prev=1
    for r,i in list(enumerate(o,1))[::-1]:
        if not np.isfinite(p[i]): continue
        prev=min(prev,p[i]*m/r); q[i]=prev
    return q
