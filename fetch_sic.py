"""SIC industry codes from SEC submissions API (used for financial flag + sector tests)."""
import requests,pandas as pd,time,json,os
from concurrent.futures import ThreadPoolExecutor
H={'User-Agent':'Karthik Vepuri research karthikvepuri.research@gmail.com'}
m=requests.get('https://www.sec.gov/files/company_tickers.json',headers=H).json()
cik={v['ticker'].replace('.','-'):int(v['cik_str']) for v in m.values()}
U=pd.read_csv('data/universe.csv').ticker
R=pd.read_csv('data/membership/removed_names.csv')
pairs=[(t,cik[t]) for t in U if t in cik]+[(r.ticker,int(r.cik)) for _,r in R.dropna(subset=['cik']).iterrows() if os.path.exists(f'data/facts/{r.ticker}.json')]
def g(p):
    t,c=p
    for i in range(3):
        time.sleep(0.25); r=requests.get(f'https://data.sec.gov/submissions/CIK{c:010d}.json',headers=H)
        if r.status_code==200: j=r.json(); return dict(ticker=t,cik=c,sic=j.get('sic'),sic_desc=j.get('sicDescription'),name=j.get('name'))
        time.sleep(2)
    return dict(ticker=t,cik=c)
with ThreadPoolExecutor(4) as ex: out=list(ex.map(g,pairs))
pd.DataFrame(out).to_csv('data/sic.csv',index=False); print(len(out),pd.DataFrame(out).sic.notna().sum())
