"""Monthly regime-switch: hold screen (Top20 PIT) in month m if flag known at start of m is favourable, else SPY. 10bps per side on switch.
Rule SELECTION uses 2012-2018 only; 2019-2026 is the honest test."""
import pandas as pd,numpy as np,sys; sys.path.insert(0,'hyp')
from stats_util import *; from regimes import load
M=pd.read_parquet('data/hyp_monthly.parquet').dropna(subset=['S','SPY']); R=load().reindex(M.index)
def sw(flag):
    f=flag.astype(bool); r=np.where(f,M.S,M.SPY); sw_=f.astype(int).diff().abs().fillna(0); return pd.Series(r-sw_*0.002,index=M.index)
def st_(r,per):
    r=sub(r,per); y=len(r)/12; c=(1+r).prod()**(1/y)-1; return c,r.mean()/r.std()*12**.5,((1+r).cumprod()/(1+r).cumprod().cummax()-1).min()
cands=[c for c in R.columns if R[c].loc[IS[0]:IS[1]].nunique()>1]
sel=[]
for c in cands:
    for neg in [False,True]:
        f=~R[c] if neg else R[c]; d=diff_test(sub(M.X,IS),sub(f,IS))
        if d['p_t']<.10 and d['mean']>0 and f.loc[IS[0]:IS[1]].mean()>=.15: sel.append((('NOT ' if neg else '')+c,d['p_t'],f))
rows=[]
def rep(name,r):
    row=dict(rule=name)
    for lab,per in [('full',('2012','2026')),('IS',IS),('OOS',OOS)]:
        c,s,m=st_(r,per); row[f'{lab}_CAGR']=c; row[f'{lab}_Sharpe']=s; row[f'{lab}_MaxDD']=m
        t=mean_test(sub(r-M.SPY,per),block=3); row[f'{lab}_excess_t']=t['t']; row[f'{lab}_excess_p']=max(t['p_t'],t['p_boot'])
    rows.append(row)
rep('SPY',M.SPY); rep('screen always',M.S)
for c in ['spx_above_200d','halloween_NovApr']: rep(f'monthly gate: {c}',sw(R[c]))
for c in ['vix_gt20','curve_inverted','fed_hiking','infl_gt3']: rep(f'monthly gate: NOT {c}',sw(~R[c]))
print('IS-selected flags:',[(n,round(p,3)) for n,p,_ in sel])
for n,p,f in sel: rep(f'IS-selected gate: {n}',sw(f))
if len(sel)>1:
    comb=pd.concat([f for _,_,f in sel],axis=1).any(axis=1); rep('IS-selected OR-combination',sw(comb))
T=pd.DataFrame(rows); T.to_csv('results/regime_switch_monthly.csv',index=False)
pd.set_option('display.width',250); print(T.to_string(float_format=lambda v:f'{v:.3f}'))
