# hyp-macro

Fed hiking or cutting (6-month change in the 3-month T-bill), 10y−3m inversion, VIX, oil versus its 200-day average, CPI YoY>3% (lagged 2 months), NBER recession, S&P versus its 200-day average. FRED was unreachable from the box, so the macro series are proxies from yfinance (^IRX, ^TNX, ^VIX, CL=F, ^GSPC) and BLS CPI.

All 147 tests in the global pool (results/hyp_all_tests.csv) are corrected together.
- `p` is the larger of the t-test p and the bootstrap/permutation p (circular-shift permutation of the regime flag, so persistence is preserved).
- `p_bonf` is the Bonferroni-adjusted p, and `q_BH` is the Benjamini-Hochberg q.
- In-sample (IS) is 2012–2018; out-of-sample (OOS) is 2019–2026.
- ROBUST means q_BH<0.10, IS p<0.05, and OOS has the same sign with p<0.10.
- Means are quarterly excess returns (segments) or monthly excess-return differences, in-regime minus out-of-regime (regimes).

| hypothesis                              |   full_mean |   full_t |      p |   p_bonf |   q_BH |   IS_mean |   p_IS |   OOS_mean |   p_OOS | verdict         | note          |
|:----------------------------------------|------------:|---------:|-------:|---------:|-------:|----------:|-------:|-----------:|--------:|:----------------|:--------------|
| strategy excess | fed_cutting vs not    |     -0.0096 |  -1.2482 | 0.22   |        1 | 0.9912 |           |        |    -0.0119 |  0.1833 | not significant |               |
| strategy excess | curve_inverted vs not |     -0.0098 |  -1.2276 | 0.227  |        1 | 0.9912 |           |        |    -0.0124 |  0.1733 | not significant |               |
| strategy excess | infl_gt3 vs not       |      0.0042 |   0.6015 | 0.5497 |        1 | 0.9912 |           |        |     0.0059 |  0.4828 | not significant |               |
| strategy excess | vix_gt20 vs not       |      0.0037 |   0.5436 | 0.5889 |        1 | 0.9912 |    0.0065 | 0.5422 |     0.0033 |  0.7189 | not significant |               |
| strategy excess | vix_gt25 vs not       |      0.0039 |   0.3896 | 0.7004 |        1 | 0.9912 |           |        |     0.005  |  0.657  | not significant |               |
| strategy excess | spx_above_200d vs not |     -0.0016 |  -0.2172 | 0.8289 |        1 | 0.9912 |    0.015  | 0.3133 |    -0.0064 |  0.4817 | not significant |               |
| strategy excess | vix_high_vs_1y vs not |     -0.0007 |  -0.1433 | 0.904  |        1 | 0.9912 |   -0.0022 | 0.7101 |     0.0005 |  0.9528 | not significant |               |
| strategy excess | oil_uptrend vs not    |     -0.0006 |  -0.1168 | 0.9072 |        1 | 0.9912 |   -0.0032 | 0.6145 |     0.0018 |  0.8617 | not significant |               |
| strategy excess | fed_hiking vs not     |      0.0008 |   0.1247 | 0.9209 |        1 | 0.9912 |   -0.0066 | 0.4217 |     0.0076 |  0.4685 | not significant |               |
| strategy excess | nber_recession vs not |             |          |        |          |        |           |        |            |         | not significant | only 2 months |

Code: `hyp/build_panels.py`, `hyp/regimes.py`, `hyp/run_tests.py`, `hyp/stats_util.py`
