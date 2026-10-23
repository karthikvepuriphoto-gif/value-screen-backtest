import pandas as pd,re,requests,json
se=pd.read_csv('data/membership/sp500_ticker_start_end.csv',parse_dates=['start_date','end_date'])
se['ticker']=se.ticker.str.replace('.','-')
se=se[(se.end_date.isna())|(se.end_date>='2012-01-01')]
se.to_csv('data/membership/sp500_intervals.csv',index=False)
cur=set(pd.read_csv('data/universe.csv').ticker)
H={'User-Agent':'Karthik Vepuri research karthikvepuri.research@gmail.com'}
m=requests.get('https://www.sec.gov/files/company_tickers.json',headers=H).json()
cikcur={v['ticker'].replace('.','-'):int(v['cik_str']) for v in m.values()}
ch=pd.read_csv('data/membership/wiki_changes.csv')
names={}
for _,r in ch.iterrows():
    if isinstance(r.rem_t,str): names[r.rem_t.replace('.','-')]=(r.rem_n,r.reason,r.date)
def norm(s): s=s.upper(); s=re.sub(r'[^A-Z0-9 ]',' ',s); s=re.sub(r'\b(INC|CORP|CORPORATION|CO|COMPANY|LTD|PLC|HOLDINGS|GROUP|THE|LP|LLC|NV|SA|AG)\b',' ',s); return ' '.join(s.split())
lk={}
for line in open('data/membership/cik-lookup-data.txt',encoding='latin-1'):
    p=line.rstrip('\n').rsplit(':',2)
    if len(p)>=2:
        try: lk.setdefault(norm(p[0]),int(p[1]))
        except: pass
rows=[]
need=sorted(set(se.ticker)-cur)
for t in need:
    nm,reason,dt=names.get(t,(None,None,None))
    c=cikcur.get(t) or (lk.get(norm(nm)) if nm else None)
    rows.append(dict(ticker=t,name=nm,removal_reason=reason,removal_date=dt,cik=c,cik_src='current_ticker' if cikcur.get(t) else ('name_match' if c else None)))
D=pd.DataFrame(rows); D.to_csv('data/membership/removed_names.csv',index=False)
print(len(D),'have name',D.name.notna().sum(),'have cik',D.cik.notna().sum()); print(D.cik_src.value_counts())
