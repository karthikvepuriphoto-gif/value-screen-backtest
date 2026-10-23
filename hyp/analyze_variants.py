import pandas as pd,numpy as np,sys,pickle; sys.path.insert(0,'.'); sys.path.insert(0,'hyp')
from engine import stats; from stats_util import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
V=pickle.load(open('data/variants.pkl','rb'))
E=pd.read_csv('results/survivorship_equity.csv',index_col=0,parse_dates=True); spy=E['bench|SPY']
mo=lambda e:e.resample('ME').last().pct_change().dropna()
base=mo(V['base Top20'][0]); sm=mo(spy)
rows=[]
SUBS=[('2012-15','2012','2015'),('2016-19','2016','2019'),('2020-22','2020','2022'),('2023-26','2023','2026')]
for k,(e,tu) in V.items():
    r=dict(variant=k,turnover=tu); m=mo(e)
    for lab,a,b in [('full','2012',None),('IS','2012','2018-12-31'),('OOS','2019',None)]:
        s=stats(e,a,b); r[f'{lab}_CAGR']=s['CAGR']; r[f'{lab}_Sharpe']=s['Sharpe']; r[f'{lab}_MaxDD']=s['MaxDD']
        t=mean_test(sub(m-sm,(a,b or '2026')),block=3); r[f'{lab}_vsSPY_t']=t['t']; r[f'{lab}_vsSPY_p']=max(t['p_t'],t['p_boot'])
        t=mean_test(sub(m-base,(a,b or '2026')),block=3); r[f'{lab}_vsBase_t']=t['t']; r[f'{lab}_vsBase_p']=max(t['p_t'],t['p_boot'])
    for lab,a,b in SUBS: r[f'CAGR_{lab}']=stats(e,a,b)['CAGR']; r[f'SPY_{lab}']=stats(spy,a,b)['CAGR']
    rows.append(r)
T=pd.DataFrame(rows)
T['q_BH_vsSPY']=bh(T.full_vsSPY_p.values); T['q_BH_vsBase']=bh(T.full_vsBase_p.replace(0,np.nan).values)
T.to_csv('results/variants.csv',index=False)
fig,ax=plt.subplots(figsize=(11,6))
for k in ['base Top20','stop30','ex-financials','momentum12>0 filter','gate: S&P>200d else SPY','gate: curve not inverted else SPY']:
    if k in V: ax.plot(V[k][0],label=k)
ax.plot(spy,label='SPY',ls='--',c='k'); ax.set_yscale('log'); ax.legend(); ax.grid(alpha=.3); ax.set_title('Selected variants (PIT S&P 500)')
plt.savefig('results/variants_equity.png',dpi=110)
pd.set_option('display.width',250)
print(T[['variant','full_CAGR','full_Sharpe','IS_CAGR','OOS_CAGR','full_vsSPY_t','full_vsBase_t','OOS_vsBase_t','q_BH_vsBase']+[f'CAGR_{l}' for l,_,_ in SUBS]].to_string(float_format=lambda v:f'{v:.3f}'))
print('SPY subperiods',[round(stats(spy,a,b)['CAGR'],3) for _,a,b in SUBS])
