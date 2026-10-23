"""SEC companyfacts for S&P 500 names removed since 2012 (CIK via current ticker map or name match)."""
import requests,json,time,os,pandas as pd
from concurrent.futures import ThreadPoolExecutor
H={'User-Agent':'Karthik Vepuri research karthikvepuri.research@gmail.com'}
TAGS=['NetIncomeLoss','Revenues','RevenueFromContractWithCustomerExcludingAssessedTax','SalesRevenueNet','NetCashProvidedByUsedInOperatingActivities',
'PaymentsToAcquirePropertyPlantAndEquipment','StockholdersEquity','LongTermDebt','LongTermDebtNoncurrent','AssetsCurrent','LiabilitiesCurrent','EarningsPerShareDiluted']
R=pd.read_csv('data/membership/removed_names.csv').dropna(subset=['cik'])
ent={}
def get(row):
    t,c=row.ticker,int(row.cik); p=f'data/facts/{t}.json'
    if os.path.exists(p): return
    for i in range(4):
        time.sleep(0.2); r=requests.get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{c:010d}.json',headers=H)
        if r.status_code in (200,404): break
        time.sleep(2)
    if r.status_code!=200: return
    j=r.json(); out={'_entity':j.get('entityName')}; g=j['facts'].get('us-gaap',{})
    for k in TAGS:
        if k in g: out[k]=[u for unit in g[k]['units'].values() for u in unit]
    d=j['facts'].get('dei',{}).get('EntityCommonStockSharesOutstanding')
    if d: out['Shares']=[u for unit in d['units'].values() for u in unit]
    json.dump(out,open(p,'w'))
with ThreadPoolExecutor(4) as ex: list(ex.map(get,[r for _,r in R.iterrows()]))
print(sum(os.path.exists(f'data/facts/{t}.json') for t in R.ticker),'of',len(R))
