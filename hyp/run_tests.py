import pandas as pd,numpy as np,sys; sys.path.insert(0,'.'); sys.path.insert(0,'hyp')
from stats_util import *; from regimes import load
from engine import AG_SIC
pk=pd.read_parquet('data/hyp_picks.parquet'); U=pd.read_parquet('data/hyp_univ.parquet'); M=pd.read_parquet('data/hyp_monthly.parquet')
R=load().reindex(M.index)
pk=pk.dropna(subset=['excess']); pk['date']=pd.to_datetime(pk.date)
# per-quarter buckets
pk['mcap_terc']=pk.groupby('date').mcap.transform(lambda v: pd.qcut(v.rank(method='first'),3,labels=['small','mid','large']))
pk['vol_terc']=pk.groupby('date').vol.transform(lambda v: pd.qcut(v.rank(method='first'),3,labels=['lowvol','midvol','highvol']) if v.notna().sum()>=3 else np.nan)
prev=set(); rep=[]
for d,g in pk[pk.top20].groupby('date'):
    rep+= [(d,t,t in prev) for t in g.ticker]; prev=set(g.ticker)
rp=pd.DataFrame(rep,columns=['date','ticker','repeat']); pk=pk.merge(rp,on=['date','ticker'],how='left')
U['date']=pd.to_datetime(U.date); U['ag']=U.sic.isin(AG_SIC)
SEG={}
for s in sorted(pk.sector.unique()): SEG[f'sector={s}']=pk.sector==s
SEG['financials (Ins+Banks/DivFin)']=pk.fin.astype(bool); SEG['ex-financials']=~pk.fin.astype(bool)
for b in ['small','mid','large']: SEG[f'mcap tercile={b} (within passers)']=pk.mcap_terc==b
SEG['mcap<10B']=pk.mcap<1e10; SEG['mcap>50B']=pk.mcap>5e10
SEG['score>=7']=pk.score>=7; SEG['score 5-6']=pk.score.between(5,6); SEG['score<=4']=pk.score<=4
SEG['metric P/FCF<10']=pk.pfcf<10; SEG['metric P/E<10']=pk.pe<10; SEG['metric P/B<1']=pk.pb<1; SEG['metric PEG<0.5']=pk.peg<0.5
SEG['metric ROE>20%']=pk.roe>.2; SEG['metric rev growth>10%']=pk.g_rev>.1; SEG['metric NI growth>50% (rebound)']=pk.g_ni>.5
SEG['extra: 12m momentum>0']=pk.mom12>0; SEG['extra: 6m drop >20% (falling knife)']=pk.mom6<-.2
SEG['extra: low-vol tercile']=pk.vol_terc=='lowvol'; SEG['extra: high-vol tercile']=pk.vol_terc=='highvol'
SEG['extra: low debt D/E<0.3 (non-fin)']=(pk.de<.3)&~pk.fin.astype(bool)
SEG['extra: quality ROE>15% & D/E<0.5']=(pk.roe>.15)&((pk.de<.5)|pk.fin.astype(bool))
SEG['Top20: rank 1-10']=(pk['rank']<=10); SEG['Top20: rank 11-20']=pk['rank'].between(11,20)
SEG['Top20: repeat holding']=pk.repeat==True; SEG['Top20: new entry']=pk.repeat==False
rows=[]
def add(fam,hyp,series_fn,kind,note=''):
    r=dict(family=fam,hypothesis=hyp,test=kind,note=note)
    for lab,per in [('full',('2012','2026')),('IS',IS),('OOS',OOS)]:
        o=series_fn(per)
        for k,v in o.items(): r[f'{lab}_{k}']=v
    rows.append(r)
ALL=pk  # all screen-passers
for name,mask in SEG.items():
    base=ALL[ALL['rank']<=20] if name.startswith('Top20') else ALL
    m=mask.reindex(base.index).fillna(False).astype(bool)
    qs=base[m].groupby('date').excess.mean()
    rest=base[~m].groupby('date').excess.mean() if not name.startswith('Top20') else base[~m].groupby('date').excess.mean()
    add('segment',f'{name}: sleeve EW excess vs SPY (quarterly)',lambda per,qs=qs: mean_test(sub(qs,per)),'mean>0')
    dd=(qs-rest).dropna()
    add('segment',f'{name}: minus other passers (quarterly)',lambda per,dd=dd: mean_test(sub(dd,per)),'diff')
q20=ALL[ALL['rank']<=20].groupby('date').excess.mean(); qall=ALL.groupby('date').excess.mean()
add('baseline','Top20 picks EW excess vs SPY (quarterly)',lambda per: mean_test(sub(q20,per)),'mean>0')
add('baseline','All passers EW excess vs SPY (quarterly)',lambda per: mean_test(sub(qall,per)),'mean>0')
add('baseline','Strategy Top20 monthly excess vs SPY',lambda per: mean_test(sub(M.X,per),block=3),'mean>0')
# regime-conditional strategy excess
FAM={'election':[c for c in R if c.startswith(('cycle_','party_','pres_','midterm_','post_pres'))],
     'seasonality':[c for c in R if c.startswith(('month_','halloween','quarter_','january','turn_of_year'))],
     'macro':['fed_hiking','fed_cutting','curve_inverted','vix_gt20','vix_gt25','vix_high_vs_1y','oil_uptrend','infl_gt3','nber_recession','spx_above_200d']}
for fam,cols in FAM.items():
    for c in cols:
        add(fam,f'strategy excess | {c} vs not',lambda per,c=c: diff_test(sub(M.X,per),sub(R[c],per)),'diff',
            'SMALL SAMPLE: ~3.5 cycles' if fam=='election' else ('only 2 months' if c=='nber_recession' else ''))
    if fam=='seasonality':
        add(fam,'Halloween on SPY itself (Nov-Apr vs May-Oct)',lambda per: diff_test(sub(M.SPY,per),sub(R['halloween_NovApr'],per)),'diff')
# weather / climate on sectors
# agriculture sleeve
import engine; Dd=engine.Data(); Rm=Dd.A.resample('ME').last().pct_change()
reb=sorted(U.date.unique()); ag={}
for i,d in enumerate(reb):
    nd=reb[i+1] if i+1<len(reb) else Rm.index[-1]; tk=U[(U.date==d)&U.ag].ticker
    for m in Rm.index[(Rm.index>d)&(Rm.index<=nd+pd.offsets.MonthEnd(0))]: ag[m]=Rm.loc[m,tk].mean() if len(tk) else np.nan
M['sl_Agriculture']=pd.Series(ag); 
W={'sl_Insurance':['hurricane_season_JunNov','hurricane_peak_AugOct','enso_el_nino','enso_la_nina','temp_anom_prev_hot'],
   'sl_Energy':['temp_anom_prev_hot','temp_anom_prev_cold','winter_DJF','summer_JJA','hurricane_peak_AugOct','enso_el_nino','enso_la_nina'],
   'sl_Utilities':['temp_anom_prev_hot','temp_anom_prev_cold','summer_JJA','winter_DJF','enso_el_nino','enso_la_nina'],
   'sl_Agriculture':['temp_anom_prev_hot','temp_anom_prev_cold','enso_el_nino','enso_la_nina','summer_JJA']}
for sl,cols in W.items():
    y=M[sl]-M.SPY
    for c in cols: add('weather',f'{sl[3:]} sector (EW S&P500 PIT) excess | {c} vs not',lambda per,y=y,c=c: diff_test(sub(y,per),sub(R[c],per)),'diff','ag sleeve has only ~%d names'%U[U.ag].groupby('date').size().median() if sl=='sl_Agriculture' else '')
    for c in ['enso_el_nino','enso_la_nina','temp_anom_prev_hot','hurricane_season_JunNov']:
        pass
for c in ['hurricane_season_JunNov','enso_el_nino','enso_la_nina','temp_anom_prev_hot','temp_anom_prev_cold']:
    add('weather',f'strategy excess | {c} vs not',lambda per,c=c: diff_test(sub(M.X,per),sub(R[c],per)),'diff')
T=pd.DataFrame(rows)
T['p']=T[['full_p_t','full_p_boot']].max(axis=1)
T['m_tests']=T.p.notna().sum(); T['p_bonf']=(T.p*T.m_tests).clip(upper=1); T['q_BH']=bh(T.p.values)
T['p_IS']=T[['IS_p_t','IS_p_boot']].max(axis=1); T['p_OOS']=T[['OOS_p_t','OOS_p_boot']].max(axis=1)
same=np.sign(T.IS_mean)==np.sign(T.OOS_mean)
T['IS_sig']=T.p_IS<.05; T['OOS_confirms']=same&(T.p_OOS<.10)
T['verdict']=np.select([(T.q_BH<.10)&T.IS_sig&T.OOS_confirms,T.IS_sig&~T.OOS_confirms,(T.q_BH<.10)],
                       ['ROBUST','IN-SAMPLE ONLY','sig full-sample, not IS/OOS-stable'],'not significant')
T.to_csv('results/hyp_all_tests.csv',index=False)
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',70); pd.set_option('display.max_rows',500)
print(len(T),'tests'); print(T.sort_values('p')[['family','hypothesis','full_mean','full_t','p','q_BH','IS_mean','p_IS','OOS_mean','p_OOS','verdict']].head(40).to_string(float_format=lambda v:f'{v:.4f}'))
print(T.verdict.value_counts())
