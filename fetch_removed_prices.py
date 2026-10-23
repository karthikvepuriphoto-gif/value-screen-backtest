import yfinance as yf,pandas as pd,time,requests,io
R=pd.read_csv('data/membership/removed_names.csv'); T=R.ticker.tolist()
out={}
for i in range(0,len(T),50):
    D=yf.download(T[i:i+50],start='2011-01-01',auto_adjust=False,actions=True,progress=False,threads=False)
    for t in T[i:i+50]:
        try:
            if D['Adj Close'][t].notna().sum()>20: out[t]=D.xs(t,axis=1,level=1)
        except KeyError: pass
    time.sleep(3)
print('yfinance',len(out))
# stooq.com now serves a JavaScript bot challenge, so it is not used (we do not bypass it)
print('total',len(out))
A=pd.DataFrame({t:v['Adj Close'] for t,v in out.items()});C=pd.DataFrame({t:v['Close'] for t,v in out.items()});S=pd.DataFrame({t:v['Stock Splits'] for t,v in out.items()})
A.to_parquet('data/rem_adj.parquet');C.to_parquet('data/rem_close.parquet');S.to_parquet('data/rem_splits.parquet')
pd.Series({t:out[t].attrs.get('src','yfinance') for t in out}).to_csv('data/membership/removed_price_source.csv')
