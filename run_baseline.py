import pandas as pd,numpy as np,sys
from engine import Data,run,stats
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
D=Data(); res={};T={};rows=[]
V=[('Top20',dict(N=20)),('Top20+stop40',dict(N=20,stop=.4)),('Top10',dict(N=10,cap=None)),('Top10+stop40',dict(N=10,cap=None,stop=.4)),('Top30',dict(N=30)),('Top30+stop40',dict(N=30,stop=.4))]
for uni in ['SP500_PIT','SP500_current']:
    for n,kw in V:
        e,tu,log=run(D,universe=uni,**kw); res[(uni,n)]=e; T[(uni,n)]=tu
        if uni=='SP500_PIT' and n=='Top20': log.to_csv('results/pit_top20_log.csv',index=False)
        print(uni,n,round(e.iloc[-1],2),flush=True)
for b in ['SPY','RSP']: res[('bench',b)]=D.A[b].reindex(D.days).ffill()/D.A[b].reindex(D.days).ffill().iloc[0]
for k,e in res.items():
    for lab,a,b in [('Full','2012-01-01',None),('2012-2018',None,'2018-12-31'),('2019-2026','2019-01-01',None)]:
        rows.append(dict(universe=k[0],strategy=k[1],period=lab,**stats(e,a,b),turnover=T.get(k,np.nan)))
St=pd.DataFrame(rows); St.to_csv('results/survivorship_stats.csv',index=False)
E=pd.DataFrame({f'{a}|{b}':v for (a,b),v in res.items()}); E.to_csv('results/survivorship_equity.csv')
Y=E.resample('YE').last(); Y=pd.concat([Y.iloc[:1]-1,Y.pct_change().iloc[1:]]); Y.index=Y.index.year; Y.to_csv('results/survivorship_yearly.csv')
fig,ax=plt.subplots(figsize=(11,6))
for c in ['SP500_PIT|Top20','SP500_PIT|Top20+stop40','SP500_current|Top20','bench|SPY','bench|RSP']: ax.plot(E[c],label=c,ls='--' if 'bench' in c else '-')
old=pd.read_csv('results/equity.csv',index_col=0,parse_dates=True); ax.plot(old['Top20'],label='old biased S&P900 Top20',ls=':')
ax.set_yscale('log');ax.legend();ax.grid(alpha=.3);ax.set_title('Survivorship fix: point-in-time S&P 500 vs biased universes');plt.savefig('results/survivorship_equity.png',dpi=120)
pd.set_option('display.width',200); print(St.to_string(float_format=lambda v:f'{v:.3f}'))
