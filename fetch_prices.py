import yfinance as yf,pandas as pd
U=pd.read_csv('data/universe.csv').ticker.tolist()+['SPY','RSP']
D=yf.download(U,start='2011-01-01',auto_adjust=False,actions=True,progress=False)
D['Adj Close'].to_parquet('data/adj.parquet'); D['Close'].to_parquet('data/close.parquet'); D['Stock Splits'].to_parquet('data/splits.parquet')
# note: re-run for any tickers that came back empty (Yahoo rate limits)
