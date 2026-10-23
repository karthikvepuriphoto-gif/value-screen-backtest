"""Build panels used by every hypothesis test (no lookahead: all conditioning info is as-of rebalance/month start).
 - picks.parquet : all screen-PASSING names each quarter (+ rank, Top20 flag) with fwd quarter return & SPY
 - univ.parquet  : all usable PIT S&P500 members each quarter w/ fwd return (for sector sleeves)
 - monthly.parquet: monthly returns of strategy variants, SPY, RSP; and sector sleeves (EW universe)"""
import pandas as pd,numpy as np,sys; sys.path.insert(0,'.')
from engine import Data,screen,select,rebal_dates,DEFAULT,run
D=Data(); A=D.A; P=dict(DEFAULT)
reb=rebal_dates(D,3); nxt={d:(reb[i+1] if i+1<len(reb) else A.index[-1]) for i,d in enumerate(reb)}
mom12=A/A.shift(252)-1; mom6=A/A.shift(126)-1; vol=A.pct_change().rolling(252).std()*252**.5
rows=[];urows=[]
for d in reb:
    s0=screen(D,d,'SP500_PIT'); s0=s0[A.loc[d].reindex(s0.index).notna()]
    s=select(s0.copy(),P); s['rank']=np.arange(1,len(s)+1)
    seg=A.loc[d:nxt[d]]; fr=(seg.ffill().iloc[-1]/seg.iloc[0]-1); spy=fr['SPY']
    for t in s0.index:
        urows.append(dict(date=d,ticker=t,sector=s0.at[t,'sector'],sic=s0.at[t,'sic'],mcap=s0.at[t,'mcap'],ret=fr.get(t,np.nan),spy=spy,passed=t in s.index))
    for t in s.index:
        r=s.loc[t]; rows.append(dict(date=d,ticker=t,rank=int(r['rank']),score=r.score,sector=r.sector,sic=r.sic,mcap=r.mcap,pe=r.pe,pfcf=r.pfcf,pb=r.pb,peg=r.peg,roe=r.roe,g_ni=r.g_ni,g_rev=r.g_rev,de=r.de,fin=r.fin,
            mom12=mom12.at[d,t],mom6=mom6.at[d,t],vol=vol.at[d,t],ret=fr.get(t,np.nan),spy=spy))
    print(d.date(),len(s),flush=True)
pk=pd.DataFrame(rows); pk['excess']=pk.ret-pk.spy; pk['top20']=pk['rank']<=20
pk.to_parquet('data/hyp_picks.parquet'); U=pd.DataFrame(urows); U['excess']=U.ret-U.spy; U.to_parquet('data/hyp_univ.parquet')
# monthly
E=pd.read_csv('results/survivorship_equity.csv',index_col=0,parse_dates=True)
M=E.resample('ME').last().pct_change().dropna(how='all')
M=M.rename(columns={'SP500_PIT|Top20':'S','bench|SPY':'SPY','bench|RSP':'RSP'})
M['X']=M.S-M.SPY
# EW sector sleeves of PIT universe, monthly (membership as of each quarter start)
R=A.resample('ME').last().pct_change()
mem=U.groupby('date')
sl={}
for d,g in mem:
    months=R.loc[d:nxt[d]].index
    months=[m for m in months if m>d and m<=nxt[d]+pd.offsets.MonthEnd(0)]
    for sec,gg in g.groupby('sector'):
        for m in months:
            sl.setdefault(sec,{})[m]=R.loc[m,gg.ticker].mean()
SL=pd.DataFrame(sl); SL.columns=['sl_'+c for c in SL.columns]
ag=set(D.AG_SIC) if hasattr(D,'AG_SIC') else set()
M=M.join(SL); M.to_parquet('data/hyp_monthly.parquet'); print(M.tail(3).T)
