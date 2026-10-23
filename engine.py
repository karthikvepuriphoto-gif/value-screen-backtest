"""Backtest engine v2: point-in-time S&P 500 membership, delisted names, SIC sectors, configurable rules."""
import pandas as pd,numpy as np,pickle,os
from pit import build,snapshot
DATA='data'
def sic_sector(s):
    if pd.isna(s): return 'Unknown'
    s=int(s)
    if s in (6798,) or 6500<=s<=6553: return 'RealEstate'
    if 6300<=s<=6411: return 'Insurance'
    if 6000<=s<=6299 or 6700<=s<=6799: return 'Banks/DivFin'
    if 4900<=s<=4949 or 4950<=s<=4991: return 'Utilities' if s not in (4922,4923,4924,4925,4950,4953,4955,4959,4961) else ('Energy' if s<4950 else 'Industrials')
    if s in (1311,1381,1382,1389,2911,2990,5171,5172) or 1200<=s<=1241 or 4610<=s<=4619: return 'Energy'
    if 2830<=s<=2836 or 3840<=s<=3851 or 8000<=s<=8099 or s in (3826,5122,6324): return 'Health'
    if 3630<=s<=3639: return 'ConsDisc'
    if 3570<=s<=3579 or 3600<=s<=3699 or 7370<=s<=7379 or 3820<=s<=3829: return 'Tech'
    if 4800<=s<=4899 or 2710<=s<=2741 or 7810<=s<=7841: return 'Comm'
    if 2000<=s<=2199 or 5400<=s<=5499 or 2840<=s<=2844 or s in (5141,5912): return 'Staples'
    if 100<=s<=999 or 1000<=s<=1499 or 2600<=s<=2699 or 2800<=s<=2899 or 3200<=s<=3399 or 2400<=s<=2499: return 'Materials'
    if 5000<=s<=5999 or 2200<=s<=2399 or 3710<=s<=3716 or 7000<=s<=7999 or 2500<=s<=2599 or 3940<=s<=3949 or 1520<=s<=1531 or 3630<=s<=3639 or 3140<=s<=3149: return 'ConsDisc'
    return 'Industrials'
AG_SIC=set(range(100,1000))|set(range(2870,2880))|{3523,2041,2070,2075,5150,5153,5191}
class Data:
    def __init__(s):
        A=pd.read_parquet(f'{DATA}/adj.parquet');C=pd.read_parquet(f'{DATA}/close.parquet');Sp=pd.read_parquet(f'{DATA}/splits.parquet')
        ra=pd.read_parquet(f'{DATA}/rem_adj.parquet');rc=pd.read_parquet(f'{DATA}/rem_close.parquet');rs=pd.read_parquet(f'{DATA}/rem_splits.parquet')
        ok=pd.read_csv(f'{DATA}/membership/removed_priced_ok.csv').ticker.tolist()
        ok=[t for t in ok if t not in A.columns]
        A=A.join(ra[ok],how='left');C=C.join(rc[ok],how='left');Sp=Sp.join(rs[ok],how='left')
        A=A.sort_index();C=C.sort_index();Sp=Sp.sort_index()
        Sp=Sp.replace(0,1).fillna(1); fac=Sp[::-1].cumprod()[::-1].shift(-1).fillna(1)
        s.A=A; s.RAW=C*fac
        R=pd.read_csv(f'{DATA}/membership/removed_names.csv'); s.alias={r.ticker:r.rename_to for _,r in R.iterrows() if isinstance(r.rename_to,str)}
        s.removed=R
        sic=pd.read_csv(f'{DATA}/sic.csv').drop_duplicates('ticker').set_index('ticker')
        s.sic=sic.sic; s.sector=sic.sic.map(sic_sector)
        s.cur=pd.read_csv(f'{DATA}/universe.csv').ticker.tolist()
        iv=pd.read_csv(f'{DATA}/membership/sp500_intervals.csv',parse_dates=['start_date','end_date'])
        iv['end_date']=iv.end_date.fillna(pd.Timestamp('2100-01-01')); iv['t']=iv.ticker.map(lambda x:s.alias.get(x,x)); s.iv=iv
        p='data/pit_all.pkl'
        if os.path.exists(p): s.F=pickle.load(open(p,'rb'))
        else:
            names=set(s.cur)|set(ok)
            s.F={t:build(t) for t in names}; pickle.dump(s.F,open(p,'wb'))
        # renamed old tickers use the new ticker's facts (same CIK)
        s.days=A.index[A.index>='2012-01-01']
    def members(s,d,universe):
        if universe=='SP500_PIT':
            m=s.iv[(s.iv.start_date<=d)&(s.iv.end_date>=d)].t.unique().tolist()
        elif universe=='SP500_current':
            m=s.iv[s.iv.end_date>pd.Timestamp('2026-10-01')].t.unique().tolist()
        elif universe=='SP900_current': m=s.cur
        return [t for t in m if t in s.F and s.F[t] is not None and t in s.A.columns]
_SC={}
def screen(D,d,universe,mcap_min=5e8):
    k=(d,universe)
    if k in _SC: return _SC[k].copy()
    mem=D.members(d,universe)
    F={t:D.F[t] for t in mem}
    s=snapshot(F,d)
    px=D.RAW.loc[:d].iloc[-1].reindex(s.index)
    alive=D.A.loc[:d].iloc[-5:].notna().any().reindex(s.index).fillna(False)
    s=s[alive]; px=px.reindex(s.index)
    s['mcap']=px*s.sh; s['sector']=D.sector.reindex(s.index).fillna('Unknown'); s['sic']=D.sic.reindex(s.index)
    s['fin']=s.sector.isin(['Insurance','Banks/DivFin'])
    s['fcf']=s.cfo-s.capex.fillna(0)
    s['pe']=s.mcap/s.ni; s['pfcf']=(s.mcap/s.fcf).where(s.fcf>0); s['pb']=(s.mcap/s.equity).where(s.equity>0)
    s['roe']=(s.ni/s.equity).where(s.equity>0); s['g_ni']=s.ni/s.ni1-1; s['g_rev']=s.rev/s.rev1-1
    g3=((s.ni/s.ni3)**(1/3)-1).where((s.ni3>0)&(s.ni>0)); s['g']=g3.fillna(s.g_ni)
    s['peg']=(s.pe/(100*s.g)).where(s.g>0)
    s['de']=(s.ltd.fillna(0)/s.equity).where(s.equity>0); s['cr']=s.ca/s.cl
    h=D.A.loc[:d]; s['mom12']=(h.iloc[-1]/h.iloc[-253]-1).reindex(s.index) if len(h)>253 else np.nan
    _SC[k]=s; return s.copy()
DEFAULT=dict(universe='SP500_PIT',N=20,stop=None,cap=0.05,cost=0.001,mcap_min=5e8,pfcf1=10,pfcf2=15,pe=15,pb=1.5,roe=.15,grev=.05,gni=.15,
             require_rising=True,de_max=1.0,filt=None,freq=3,score_min=None)
def select(s,P):
    ok=(s.mcap>P['mcap_min'])&(s.ni>0)&s.mcap.notna()
    if P['require_rising']: ok&=(s.ni>s.ni1)
    ok&= s.fin | ((s.fcf>0)&(s.de<P['de_max'])&((s.cr>1)|s.cr.isna()))
    sc=np.where(s.pfcf<P['pfcf1'],2,np.where(s.pfcf<P['pfcf2'],1,0))+(s.pe<=P['pe'])+(s.peg<1)+(s.pb<P['pb'])+(s.roe>P['roe'])+(s.g_rev>P['grev'])+(s.g_ni>P['gni'])
    s=s.assign(score=sc,ey=1/s.pe,passed=ok)
    s=s[s.passed]
    if P['filt'] is not None: s=s[P['filt'](s)]
    if P['score_min'] is not None: s=s[s.score>=P['score_min']]
    return s.sort_values(['score','ey'],ascending=False)
def rebal_dates(D,freq=3):
    days=D.days; ms=[m for m in range(1,13) if (m-1)%freq==0]
    return [days[days>=pd.Timestamp(y,m,1)][0] for y in range(2012,2027) for m in ms if pd.Timestamp(y,m,1)<=days[-1]]
def run(D,**kw):
    P={**DEFAULT,**kw}; days=D.days; reb=set(rebal_dates(D,P['freq'])); A=D.A
    cash=1.0;pos={};peak={};out=[];turn=0;log=[];prev=None;entry={}
    gate=P.get('gate')  # function(date)->True to hold screen, else SPY
    for d in days:
        if prev is not None:
            r=(A.loc[d]/A.loc[prev])
            for t in list(pos):
                x=r.get(t,np.nan)
                if np.isnan(x):
                    if np.isnan(A.at[d,t]) and t!='SPY':   # delisted / series ended: exit at last price
                        cash+=pos.pop(t)*(1-P['cost']); continue
                    x=1.0
                pos[t]*=x
                if P['stop'] and t!='SPY':
                    peak[t]=max(peak[t],A.at[d,t]);
                    if A.at[d,t]<=(1-P['stop'])*peak[t]: cash+=pos.pop(t)*(1-P['cost'])
        nav=cash+sum(pos.values())
        if d in reb:
            if gate is not None and not gate(d): pick=['SPY']; w=1.0
            else:
                s=select(screen(D,d,P['universe']),P); s=s[A.loc[d].reindex(s.index).notna()]
                pick=s.head(P['N']).index.tolist()
                w=min(1/max(len(pick),1),P['cap']) if P['cap'] else 1/max(len(pick),1)
                for i,t in enumerate(pick): log.append(dict(date=d,ticker=t,rank=i+1,**{k:s.at[t,k] for k in ['score','sector','sic','mcap','pe','pfcf','pb','peg','roe','g_ni','g_rev','fin']}))
            tgt={t:nav*w for t in pick}
            traded=sum(abs(tgt.get(t,0)-pos.get(t,0)) for t in set(tgt)|set(pos)); nav-=traded*P['cost']; turn+=traded/nav/2
            tgt={t:nav*w for t in pick}; pos=tgt; cash=nav-sum(tgt.values()); peak={t:A.at[d,t] for t in pos}
        out.append(cash+sum(pos.values())); prev=d
    e=pd.Series(out,index=days)
    return e,turn/((days[-1]-days[0]).days/365.25),pd.DataFrame(log)
def stats(e,a=None,b=None):
    e=e.loc[a:b]; r=e.pct_change().dropna(); y=(e.index[-1]-e.index[0]).days/365.25
    return dict(CAGR=(e.iloc[-1]/e.iloc[0])**(1/y)-1,Vol=r.std()*252**.5,Sharpe=r.mean()/r.std()*252**.5,MaxDD=(e/e.cummax()-1).min())
def pick_returns(D,log):
    """forward return of each pick from its rebalance date to the next rebalance (delisting: last price), and SPY same window"""
    A=D.A; dates=sorted(log.date.unique()); nxt={d:(dates[i+1] if i+1<len(dates) else A.index[-1]) for i,d in enumerate(dates)}
    out=[]
    for _,r in log.iterrows():
        s=A[r.ticker].loc[r.date:nxt[r.date]].dropna()
        if len(s)<2: continue
        sp=A['SPY'].loc[r.date:nxt[r.date]]
        out.append({**r,'ret':s.iloc[-1]/s.iloc[0]-1,'spy':sp.iloc[-1]/sp.iloc[0]-1})
    o=pd.DataFrame(out); o['excess']=o.ret-o.spy; return o
