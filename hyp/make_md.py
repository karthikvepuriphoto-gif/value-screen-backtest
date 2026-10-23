import pandas as pd,sys
T=pd.read_csv('results/hyp_all_tests.csv'); V=pd.read_csv('results/variants.csv'); RS=pd.read_csv('results/regime_switch_monthly.csv')
f=lambda v: '' if pd.isna(v) else f'{v:.4f}'
def tab(d):
    d=d.sort_values('p')
    c=['hypothesis','full_mean','full_t','p','p_bonf','q_BH','IS_mean','p_IS','OOS_mean','p_OOS','verdict','note']
    x=d[c].copy()
    for k in c[1:10]: x[k]=x[k].map(f)
    return x.fillna('').to_markdown(index=False)
HDR=f"""All {len(T)} tests in the global pool (results/hyp_all_tests.csv) are corrected together.
- `p` is the larger of the t-test p and the bootstrap/permutation p (circular-shift permutation of the regime flag, so persistence is preserved).
- `p_bonf` is the Bonferroni-adjusted p, and `q_BH` is the Benjamini-Hochberg q.
- In-sample (IS) is 2012–2018; out-of-sample (OOS) is 2019–2026.
- ROBUST means q_BH<0.10, IS p<0.05, and OOS has the same sign with p<0.10.
- Means are quarterly excess returns (segments) or monthly excess-return differences, in-regime minus out-of-regime (regimes).
"""
FAM={'hyp-segments':(['segment','baseline'],'Sector, ex-financials and financials-only, market-cap bucket, score level, value metric, and extra pick-level patterns (momentum, falling knife, volatility, debt, quality, rank, repeat holdings)'),
 'hyp-election':(['election'],'Presidential cycle, party in power, and months around elections. **Small-sample warning:** about 3.5 cycles and 4 presidential elections.'),
 'hyp-seasonality':(['seasonality'],'Month of year, Halloween / Sell in May, quarter, January, turn of the year'),
 'hyp-weather':(['weather'],'NOAA contiguous-US temperature anomaly (last month), ENSO from CPC ONI (lagged 2 months), and hurricane season, tested on equal-weight point-in-time S&P 500 sector sleeves (Insurance, Energy, Utilities, Agriculture by SIC) and on the strategy'),
 'hyp-macro':(['macro'],'Fed hiking or cutting (6-month change in the 3-month T-bill), 10y−3m inversion, VIX, oil versus its 200-day average, CPI YoY>3% (lagged 2 months), NBER recession, S&P versus its 200-day average. FRED was unreachable from the box, so the macro series are proxies from yfinance (^IRX, ^TNX, ^VIX, CL=F, ^GSPC) and BLS CPI.')}
for b,(fams,desc) in FAM.items():
    open(f'/tmp/{b}.md','w').write(f"# {b}\n\n{desc}\n\n{HDR}\n{tab(T[T.family.isin(fams)])}\n\nCode: `hyp/build_panels.py`, `hyp/regimes.py`, `hyp/run_tests.py`, `hyp/stats_util.py`\n")
vc=['variant','full_CAGR','full_Sharpe','full_MaxDD','IS_CAGR','OOS_CAGR','full_vsSPY_t','full_vsBase_t','full_vsBase_p','q_BH_vsBase','OOS_vsBase_t','CAGR_2012-15','CAGR_2016-19','CAGR_2020-22','CAGR_2023-26','turnover']
def vt(d):
    x=d[vc].copy()
    for k in vc[1:]: x[k]=x[k].map(lambda v:f'{v:.3f}')
    return x.to_markdown(index=False)
spy="SPY CAGR: full period 14.8%, IS 12.3%, OOS 17.1%. By subperiod: 2012–15 14.8%, 2016–19 14.7%, 2020–22 7.3%, 2023–26 21.6%."
rob=V[~V.variant.str.startswith(('gate','ex-','fin','momentum','quality','max'))]
open('/tmp/hyp-robustness.md','w').write(f"# hyp-robustness: parameter sensitivity and subperiods (point-in-time S&P 500, quarterly rebalance unless noted)\n\n{spy}\n\nThe vsBase and vsSPY columns are t-stats of the monthly return difference. The p-value is the larger of the t-test p and a 3-month block-bootstrap p. q_BH is computed within the variant table.\n\n{vt(rob)}\n\n![variants](results/variants_equity.png)\n")
cmb=V[V.variant.str.startswith(('gate','ex-','fin','momentum','quality','max'))|(V.variant=='base Top20')]
x=RS.copy()
for k in x.columns[1:]: x[k]=x[k].map(lambda v:f'{v:.3f}')
open('/tmp/hyp-combos-regime-switch.md','w').write(f"# hyp-combos-regime-switch\n\n## Filters, combinations, and quarterly regime gates (screen when the regime is favourable, otherwise SPY), run through the full engine\n{spy}\n\n{vt(cmb)}\n\n## Monthly regime switch (synthetic, 20 bps per round trip). Rules were *selected on 2012–2018 only*\n{x.to_markdown(index=False)}\n\nThe best in-sample-selected rule, 'pres_election_pm3m' (hold the screen from August to February around presidential elections), covers only 4 elections. Its out-of-sample excess return is not significant (p=0.38), so it is not robust.\n")
