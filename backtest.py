import pandas as pd,numpy as np,pickle,os,sys
from pit import build,snapshot
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
A=pd.read_parquet('data/adj.parquet').sort_index(); C=pd.read_parquet('data/close.parquet').sort_index(); S=pd.read_parquet('data/splits.parquet').sort_index()
S=S.replace(0,1).fillna(1); fac=S[::-1].cumprod()[::-1].shift(-1).fillna(1)  # product of splits strictly after t
RAW=C*fac   # unsplit-adjusted close, matches as-reported share counts
U=pd.read_csv('data/universe.csv').ticker.tolist()
sect=pd.read_csv('data/fundamentals.csv').set_index('ticker').sector
FIN=set(sect[sect=='Financial Services'].index)
if os.path.exists('data/pit.pkl'): F=pickle.load(open('data/pit.pkl','rb'))
else: F={t:build(t) for t in U}; pickle.dump(F,open('data/pit.pkl','wb'))
days=A.index[A.index>='2012-01-01']
reb=[days[days>=pd.Timestamp(y,m,1)][0] for y in range(2012,2027) for m in (1,4,7,10) if pd.Timestamp(y,m,1)<=days[-1]]
_C={}
def screen(date):
    if date in _C: return _C[date].copy()
    _C[date]=_screen(date); return _C[date].copy()
def _screen(date):
    s=snapshot(F,date)
    px=RAW.loc[:date].iloc[-1].reindex(s.index)
    s['mcap']=px*s.sh
    s['fin']=s.index.isin(FIN)
    s['fcf']=s.cfo-s.capex.fillna(0)
    s['pe']=s.mcap/s.ni; s['pfcf']=(s.mcap/s.fcf).where(s.fcf>0); s['pb']=(s.mcap/s.equity).where(s.equity>0)
    s['roe']=(s.ni/s.equity).where(s.equity>0); s['g_ni']=s.ni/s.ni1-1; s['g_rev']=s.rev/s.rev1-1
    g3=((s.ni/s.ni3)**(1/3)-1).where((s.ni3>0)&(s.ni>0)); s['g']=g3.fillna(s.g_ni)
    s['peg']=(s.pe/(100*s.g)).where(s.g>0)
    s['de']=(s.ltd.fillna(0)/s.equity).where(s.equity>0); s['cr']=s.ca/s.cl
    ok=(s.mcap>5e8)&(s.ni>0)&(s.ni>s.ni1)&s.mcap.notna()
    nf=~s.fin
    ok&= s.fin | ((s.fcf>0)&(s.de<1)&((s.cr>1)|s.cr.isna()))
    sc=np.where(s.pfcf<10,2,np.where(s.pfcf<15,1,0))+(s.pe<=15)+((s.peg<1))+(s.pb<1.5)+(s.roe>.15)+(s.g_rev>.05)+(s.g_ni>.15)
    s['score']=sc; s['ey']=1/s.pe; s['pass']=ok
    return s
def run(N=20,stop=False,cap=0.05,cost=0.001,capN=True):
    nav=1.0; pos={}; cash=1.0; out=[]; peak={}; turn=0; hist=[]
    ri=set(reb)
    prev=None
    for d in days:
        if prev is not None:
            r=A.loc[d]/A.loc[prev]
            for t in list(pos):
                x=r.get(t,np.nan); pos[t]*= (1 if np.isnan(x) else x)
                peak[t]=max(peak[t],A.at[d,t] if not np.isnan(A.at[d,t]) else peak[t])
                if stop and A.at[d,t]<=0.6*peak[t]:
                    cash+=pos[t]*(1-cost); turn+=pos[t]/max(cash+sum(pos.values()),1e-9); del pos[t]
        nav=cash+sum(pos.values())
        if d in ri:
            s=screen(d); s=s[s['pass']&A.loc[d].reindex(s.index).notna()]
            pick=s.sort_values(['score','ey'],ascending=False).head(N).index.tolist()
            w=min(1/N,cap) if capN else 1/N
            tgt={t:nav*w for t in pick}
            traded=sum(abs(tgt.get(t,0)-pos.get(t,0)) for t in set(tgt)|set(pos))
            nav-=traded*cost; tgt={t:nav*w for t in pick}; turn+=traded/nav/2
            pos=tgt; cash=nav-sum(tgt.values()); peak={t:A.at[d,t] for t in pos}
            hist.append((d,pick))
        out.append(nav); prev=d
    return pd.Series(out,index=days),turn,hist
def stats(e):
    r=e.pct_change().dropna(); y=(e.index[-1]-e.index[0]).days/365.25
    return dict(CAGR=(e.iloc[-1]/e.iloc[0])**(1/y)-1,Vol=r.std()*252**.5,Sharpe=r.mean()/r.std()*252**.5,MaxDD=(e/e.cummax()-1).min())
if __name__=='__main__':
    res={};T={}
    V=[('Top20',20,False),('Top20+stop40',20,True),('Top10',10,False),('Top10+stop40',10,True),('Top30',30,False),('Top30+stop40',30,True)]
    H={}
    for n,N,st in V:
        e,tu,h=run(N,st,capN=False if N==10 else True); res[n]=e; T[n]=tu/((days[-1]-days[0]).days/365.25); H[n]=h; print(n,'done',e.iloc[-1])
    for b in ['SPY','RSP']: res[b]=A[b].reindex(days).ffill()/A[b].reindex(days).ffill().iloc[0]
    R=pd.DataFrame(res)
    R.to_csv('results/equity.csv')
    rows=[]
    for c in R:
        for lab,a,b in [('Full 2012-2026',None,None),('2012-2018',None,'2018-12-31'),('2019-2026',  '2019-01-01',None)]:
            e=R[c].loc[a:b]; st=stats(e); st.update(strategy=c,period=lab,turnover=T.get(c,np.nan)); rows.append(st)
    St=pd.DataFrame(rows)[['strategy','period','CAGR','Vol','Sharpe','MaxDD','turnover']]; St.to_csv('results/stats.csv',index=False)
    Y=R.resample('YE').last().pct_change(); Y.iloc[0]=R.resample('YE').last().iloc[0]/1-1; Y.index=Y.index.year; Y.to_csv('results/yearly.csv')
    pd.DataFrame([(d.date(),i+1,t) for d,p in H['Top20'] for i,t in enumerate(p)],columns=['rebalance','rank','ticker']).to_csv('results/top20_holdings_history.csv',index=False)
    fig,ax=plt.subplots(figsize=(11,6))
    for c in ['Top20','Top20+stop40','Top10','Top30','SPY','RSP']: ax.plot(R[c],label=c,ls='--' if c in('SPY','RSP') else '-')
    ax.set_yscale('log');ax.axvline(pd.Timestamp('2019-01-01'),color='gray',ls=':');ax.legend();ax.grid(alpha=.3);ax.set_title('Value screen backtest (point-in-time SEC fundamentals), growth of $1')
    plt.savefig('results/equity_curve.png',dpi=120)
    s=screen(A.index[-1]); s=s[s['pass']&A.iloc[-1].reindex(s.index).notna()].sort_values(['score','ey'],ascending=False).head(20)
    s['weight']=0.05; s['sector']=sect.reindex(s.index)
    s[['sector','score','weight','mcap','pe','pfcf','pb','peg','roe','g_ni','g_rev','de','cr']].round(3).to_csv('current_portfolio.csv')
    pd.set_option('display.width',200); print(St.to_string(float_format=lambda v:f'{v:.3f}')); print(Y.round(3).to_string()); print(s[['sector','score','pe','pfcf','pb','roe','g_ni']].round(2).to_string())
