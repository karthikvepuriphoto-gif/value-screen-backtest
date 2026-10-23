import pandas as pd
st=pd.read_csv('results/stats.csv'); y=pd.read_csv('results/yearly.csv',index_col=0)
d=st.copy()
for c in ['CAGR','Vol','MaxDD']: d[c]=(d[c]*100).map('{:.1f}%'.format)
d['Sharpe']=d.Sharpe.map('{:.2f}'.format); d['turnover']=d.turnover.map(lambda v:'' if pd.isna(v) else f'{v*100:.0f}%')
yy=(y*100).round(1).astype(str)+'%'
cp=pd.read_csv('current_portfolio.csv')
tmpl=open('README.template.md').read()
open('README.md','w').write(tmpl.replace('{STATS}',d.to_markdown(index=False)).replace('{YEARLY}',yy.to_markdown()).replace('{PICKS}',', '.join(cp.ticker)))
