import requests,json,time,pandas as pd,os,gzip
from concurrent.futures import ThreadPoolExecutor
H={'User-Agent':'Karthik Vepuri research karthikvepuri.research@gmail.com'}
m=requests.get('https://www.sec.gov/files/company_tickers.json',headers=H).json()
cik={v['ticker'].replace('.','-'):int(v['cik_str']) for v in m.values()}
U=pd.read_csv('data/universe.csv').ticker
TAGS=['NetIncomeLoss','Revenues','RevenueFromContractWithCustomerExcludingAssessedTax','SalesRevenueNet','NetCashProvidedByUsedInOperatingActivities',
'PaymentsToAcquirePropertyPlantAndEquipment','StockholdersEquity','LongTermDebt','LongTermDebtNoncurrent','AssetsCurrent','LiabilitiesCurrent','EarningsPerShareDiluted']
def get(t):
    p=f'data/facts/{t}.json'
    if os.path.exists(p) or t not in cik: return
    for i in range(4):
        time.sleep(0.15)
        r=requests.get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik[t]:010d}.json',headers=H)
        if r.status_code==200: break
        time.sleep(2)
    else: print('fail',t,r.status_code); return
    j=r.json(); out={}
    g=j['facts'].get('us-gaap',{})
    for k in TAGS:
        if k in g: out[k]=[u for unit in g[k]['units'].values() for u in unit]
    d=j['facts'].get('dei',{}).get('EntityCommonStockSharesOutstanding')
    if d: out['Shares']=[u for unit in d['units'].values() for u in unit]
    json.dump(out,open(p,'w'))
with ThreadPoolExecutor(5) as ex: list(ex.map(get,U))
print('missing cik',[t for t in U if t not in cik]); print(len(os.listdir('data/facts')))
