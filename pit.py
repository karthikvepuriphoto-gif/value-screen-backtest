"""Build point-in-time fundamental panel from SEC companyfacts (first-filed values only, keyed by filing date)."""
import json,os,pandas as pd,numpy as np
FLOW={'ni':['NetIncomeLoss'],'rev':['Revenues','RevenueFromContractWithCustomerExcludingAssessedTax','SalesRevenueNet'],
      'cfo':['NetCashProvidedByUsedInOperatingActivities'],'capex':['PaymentsToAcquirePropertyPlantAndEquipment']}
INST={'eq':['StockholdersEquity'],'ltd':['LongTermDebt','LongTermDebtNoncurrent'],'ca':['AssetsCurrent'],'cl':['LiabilitiesCurrent'],'sh':['Shares']}
def annual(recs):
    rows=[]
    for r in recs:
        if 'start' not in r or not r.get('form','').startswith('10-K'): continue
        dur=(pd.Timestamp(r['end'])-pd.Timestamp(r['start'])).days
        if 350<=dur<=380: rows.append((pd.Timestamp(r['end']),pd.Timestamp(r['filed']),r['val']))
    return rows
def inst(recs):
    return [(pd.Timestamp(r['end']),pd.Timestamp(r['filed']),r['val']) for r in recs if 'start' not in r and r.get('form','')[:4] in ('10-K','10-Q')]
def build(t):
    f=f'data/facts/{t}.json'
    if not os.path.exists(f): return None
    j=json.load(open(f)); out={}
    for k,tags in FLOW.items():
        rows=[x for tg in tags for x in annual(j.get(tg,[]))]
        if rows:
            d=pd.DataFrame(rows,columns=['end','filed','val']).sort_values('filed').drop_duplicates('end',keep='first')  # first filed = no restatement lookahead
            out[k]=d
    for k,tags in INST.items():
        rows=[x for tg in tags for x in inst(j.get(tg,[]))]
        if rows: out[k]=pd.DataFrame(rows,columns=['end','filed','val']).sort_values('filed').drop_duplicates('end',keep='first')
    return out
def asof(d,date,n_back=0):
    """value of the n_back-th most recent period whose first filing is <= date"""
    if d is None: return np.nan
    k=d[d.filed<=date].sort_values('end')
    if len(k)<=n_back: return np.nan
    # stale guard: latest period must end within 550 days
    if (date-k.end.iloc[-1]).days>550: return np.nan
    return k.val.iloc[-1-n_back]
def snapshot(F,date):
    rows=[]
    for t,o in F.items():
        if o is None: continue
        g=lambda k,n=0: asof(o.get(k),date,n)
        rows.append(dict(ticker=t,ni=g('ni'),ni1=g('ni',1),ni3=g('ni',3),rev=g('rev'),rev1=g('rev',1),cfo=g('cfo'),capex=g('capex'),
                         equity=g('eq'),ltd=g('ltd'),ca=g('ca'),cl=g('cl'),sh=g('sh')))
    return pd.DataFrame(rows).set_index('ticker')
