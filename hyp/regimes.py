"""Monthly regime/condition flags, each known at the START of month m (indexed by month-end of m)."""
import pandas as pd,numpy as np,json
def load():
    y=pd.read_csv('data/macro/yf_macro.csv',index_col=0,parse_dates=True)
    y.index=pd.to_datetime(y.index).tz_localize(None) if getattr(y.index,'tz',None) else y.index
    me=pd.date_range('2011-01-31','2026-10-31',freq='ME')
    prev=lambda s: s.dropna().resample('ME').last().reindex(me).ffill().shift(1)   # value at end of previous month
    R=pd.DataFrame(index=me)
    irx=prev(y['^IRX']); tnx=prev(y['^TNX']); vix=prev(y['^VIX']); oil=y['CL=F'].where(y['CL=F']>0)
    gspc=y['^GSPC']
    R['fed_hiking']=(irx-irx.shift(6))>0.25          # 3m T-bill (tracks fed funds) up >25bp over trailing 6m
    R['fed_cutting']=(irx-irx.shift(6))<-0.25
    R['curve_inverted']=(tnx-irx)<0                   # 10y - 3m
    R['vix_gt20']=vix>20; R['vix_gt25']=vix>25
    R['vix_high_vs_1y']=vix>vix.rolling(12).median()
    o=oil.dropna(); R['oil_uptrend']=prev(o>o.rolling(200).mean()).astype(bool)
    R['spx_above_200d']=prev(gspc>gspc.rolling(200).mean()).astype(bool)
    c=[]
    for f in ['data/macro/cpi1.json','data/macro/cpi2.json']:
        for r in json.load(open(f))['Results']['series'][0]['data']:
            if r['period']!='M13' and r['value'] not in ('-',''): c.append((pd.Timestamp(int(r['year']),int(r['period'][1:]),1)+pd.offsets.MonthEnd(0),float(r['value'])))
    cpi=pd.Series(dict(c)).sort_index(); yoy=(cpi/cpi.shift(12)-1).reindex(me).ffill().shift(2)  # released mid next month -> lag 2
    R['infl_gt3']=yoy>0.03
    R['nber_recession']=[(m>=pd.Timestamp('2020-03-01'))&(m<=pd.Timestamp('2020-04-30')) for m in me]  # NBER: peak Feb-2020, trough Apr-2020
    # election
    yr=me.year; R['cycle_yr1']=(yr%4==1); R['cycle_yr2_midterm']=(yr%4==2); R['cycle_yr3_preelection']=(yr%4==3); R['cycle_yr4_election']=(yr%4==0)
    rep=[(pd.Timestamp('2017-01-20')<=m<=pd.Timestamp('2021-01-31')) or m>=pd.Timestamp('2025-01-31') for m in me]
    R['party_R_president']=rep
    def near(m,years,k): return any(abs((m.year-yy)*12+m.month-11)<=k for yy in years)
    R['pres_election_pm3m']=[near(m,[2012,2016,2020,2024],3) for m in me]
    R['midterm_election_pm3m']=[near(m,[2014,2018,2022,2026],3) for m in me]
    R['post_pres_election_6m']=[any(0<=(m.year-yy)*12+m.month-11<=6 for yy in [2012,2016,2020,2024]) for m in me]
    # seasonality
    for k in range(1,13): R[f'month_{k:02d}']=me.month==k
    R['halloween_NovApr']=me.month.isin([11,12,1,2,3,4])
    for q in range(1,5): R[f'quarter_Q{q}']=((me.month-1)//3+1)==q
    R['january']=me.month==1
    R['turn_of_year_DecJan']=me.month.isin([12,1])
    # weather/climate
    t=pd.read_csv('data/macro/ustemp.csv',comment='#'); t['d']=pd.to_datetime(t.Date.astype(str),format='%Y%m')+pd.offsets.MonthEnd(0)
    t=t.set_index('d').Value; norm=t.groupby(t.index.month).transform(lambda v: v.expanding().mean().shift(1))  # expanding same-month normal (no lookahead)
    anom=(t-norm).reindex(me)
    R['temp_anom_prev_hot']=anom.shift(1)>anom.shift(1).rolling(36,min_periods=12).std()*0.5   # last month hot (>0.5 sd); known by month start
    R['temp_anom_prev_cold']=anom.shift(1)<-anom.shift(1).rolling(36,min_periods=12).std()*0.5
    on=[]
    for l in open('data/macro/oni.txt').read().split('\n')[1:]:
        p=l.split()
        if len(p)==4: on.append((p[0],int(p[1]),float(p[3])))
    seas=['DJF','JFM','FMA','MAM','AMJ','MJJ','JJA','JAS','ASO','SON','OND','NDJ']
    oni=pd.Series({pd.Timestamp(y_,seas.index(s)+1,1)+pd.offsets.MonthEnd(0):v for s,y_,v in on}).sort_index()  # indexed by centre month
    oni=oni.reindex(me).ffill().shift(2)   # season ends 1 month after centre, published early the month after -> known 2 months later
    R['enso_el_nino']=oni>=0.5; R['enso_la_nina']=oni<=-0.5
    R['hurricane_season_JunNov']=me.month.isin([6,7,8,9,10,11]); R['hurricane_peak_AugOct']=me.month.isin([8,9,10])
    R['summer_JJA']=me.month.isin([6,7,8]); R['winter_DJF']=me.month.isin([12,1,2])
    return R.fillna(False).astype(bool)
if __name__=='__main__':
    R=load(); print(R.loc['2012':].mean().round(2).to_string())
