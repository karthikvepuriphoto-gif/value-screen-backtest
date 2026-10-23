import pandas as pd,numpy as np,sys,pickle; sys.path.insert(0,'.'); sys.path.insert(0,'hyp')
from engine import Data,run,stats; from regimes import load
D=Data(); R=load()
def flag(c,neg=False):
    def g(d):
        v=bool(R[c].asof(d+pd.offsets.MonthEnd(0))); return (not v) if neg else v
    return g
V={'base Top20':{},
 # robustness / parameter sensitivity
 'N=10':dict(N=10,cap=None),'N=15':dict(N=15,cap=None),'N=25':dict(N=25),'N=30':dict(N=30),'N=40':dict(N=40),'N=50':dict(N=50),
 'stop25':dict(stop=.25),'stop30':dict(stop=.3),'stop40':dict(stop=.4),'stop50':dict(stop=.5),
 'monthly rebal':dict(freq=1),'semiannual rebal':dict(freq=6),'annual rebal':dict(freq=12),
 'mcap>2B':dict(mcap_min=2e9),'mcap>10B':dict(mcap_min=1e10),
 'P/FCF 8/12':dict(pfcf1=8,pfcf2=12),'P/FCF 12/20':dict(pfcf1=12,pfcf2=20),'P/E<=12':dict(pe=12),'P/E<=18':dict(pe=18),
 'P/B<1':dict(pb=1.0),'P/B<2':dict(pb=2.0),'ROE>10%':dict(roe=.10),'ROE>20%':dict(roe=.20),
 'no rising-NI rule':dict(require_rising=False),'D/E<0.5':dict(de_max=.5),'D/E<2':dict(de_max=2.0),'score>=6 only':dict(score_min=6),
 'cost 30bps':dict(cost=.003),
 # segment filters / combos
 'ex-financials':dict(filt=lambda s:~s.fin),'financials only (N10)':dict(filt=lambda s:s.fin,N=10,cap=None),
 'ex Materials+Staples':dict(filt=lambda s:~s.sector.isin(['Materials','Staples'])),
 'momentum12>0 filter':dict(filt=lambda s:s.mom12>0),'ex-fin + mom>0':dict(filt=lambda s:(~s.fin)&(s.mom12>0)),
 'quality ROE>15% & D/E<0.5':dict(filt=lambda s:(s.roe>.15)&((s.de<.5)|s.fin)),
 'max 4 per sector':dict(filt='sectorcap'),
 # regime switch (screen in favorable regime, else SPY), decided at each quarterly rebalance
 'gate: S&P>200d else SPY':dict(gate=flag('spx_above_200d')),'gate: VIX<=20 else SPY':dict(gate=flag('vix_gt20',True)),
 'gate: curve not inverted else SPY':dict(gate=flag('curve_inverted',True)),'gate: Fed not hiking else SPY':dict(gate=flag('fed_hiking',True)),
 'gate: inflation<=3% else SPY':dict(gate=flag('infl_gt3',True)),'gate: oil uptrend else SPY':dict(gate=flag('oil_uptrend')),
}
import engine
_sel=engine.select
def sel(s,P):
    if P.get('filt')=='sectorcap':
        P={**P,'filt':None}; o=_sel(s,P); return o[o.groupby('sector').cumcount()<4]
    return _sel(s,P)
engine.select=sel
out={}
for k,kw in V.items():
    e,tu,log=engine.run(D,**kw); out[k]=(e,tu); print(k,round(e.iloc[-1],2),flush=True)
pickle.dump(out,open('data/variants.pkl','wb'))
