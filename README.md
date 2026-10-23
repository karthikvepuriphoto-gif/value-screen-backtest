# hyp-weather

NOAA contiguous-US temperature anomaly (last month), ENSO from CPC ONI (lagged 2 months), and hurricane season, tested on equal-weight point-in-time S&P 500 sector sleeves (Insurance, Energy, Utilities, Agriculture by SIC) and on the strategy

All 147 tests in the global pool (results/hyp_all_tests.csv) are corrected together.
- `p` is the larger of the t-test p and the bootstrap/permutation p (circular-shift permutation of the regime flag, so persistence is preserved).
- `p_bonf` is the Bonferroni-adjusted p, and `q_BH` is the Benjamini-Hochberg q.
- In-sample (IS) is 2012–2018; out-of-sample (OOS) is 2019–2026.
- ROBUST means q_BH<0.10, IS p<0.05, and OOS has the same sign with p<0.10.
- Means are quarterly excess returns (segments) or monthly excess-return differences, in-regime minus out-of-regime (regimes).

| hypothesis                                                               |   full_mean |   full_t |      p |   p_bonf |   q_BH |   IS_mean |   p_IS |   OOS_mean |   p_OOS | verdict         | note                        |
|:-------------------------------------------------------------------------|------------:|---------:|-------:|---------:|-------:|----------:|-------:|-----------:|--------:|:----------------|:----------------------------|
| Energy sector (EW S&P500 PIT) excess | enso_la_nina vs not               |      0.0447 |   3.0148 | 0.0114 |        1 | 0.6851 |    0.0083 | 0.6685 |     0.0578 |  0.0108 | not significant |                             |
| Agriculture sector (EW S&P500 PIT) excess | enso_la_nina vs not          |      0.0303 |   2.6875 | 0.0339 |        1 | 0.6851 |    0.004  | 0.8193 |     0.042  |  0.0532 | not significant | ag sleeve has only ~4 names |
| Agriculture sector (EW S&P500 PIT) excess | temp_anom_prev_cold vs not   |      0.0194 |   2.1525 | 0.0452 |        1 | 0.6851 |    0.0204 | 0.0241 |     0.0193 |  0.3085 | IN-SAMPLE ONLY  | ag sleeve has only ~4 names |
| Insurance sector (EW S&P500 PIT) excess | temp_anom_prev_hot vs not      |     -0.0102 |  -1.9075 | 0.0852 |        1 | 0.7763 |   -0.007  | 0.1928 |    -0.0118 |  0.184  | not significant |                             |
| Agriculture sector (EW S&P500 PIT) excess | enso_el_nino vs not          |     -0.0249 |  -2.9262 | 0.0904 |        1 | 0.7763 |   -0.0148 | 0.2556 |    -0.0335 |  0.1383 | not significant | ag sleeve has only ~4 names |
| Utilities sector (EW S&P500 PIT) excess | temp_anom_prev_hot vs not      |     -0.0115 |  -1.6876 | 0.108  |        1 | 0.7763 |   -0.0032 | 0.7518 |    -0.0171 |  0.0753 | not significant |                             |
| strategy excess | enso_el_nino vs not                                    |     -0.0093 |  -1.5446 | 0.1264 |        1 | 0.8387 |   -0.0066 | 0.494  |    -0.0117 |  0.2379 | not significant |                             |
| strategy excess | enso_la_nina vs not                                    |      0.0083 |   1.3313 | 0.2486 |        1 | 0.9912 |   -0.0042 | 0.6024 |     0.0139 |  0.117  | not significant |                             |
| Insurance sector (EW S&P500 PIT) excess | hurricane_peak_AugOct vs not   |      0.0065 |   1.1337 | 0.2604 |        1 | 0.9912 |    0.0052 | 0.325  |     0.0076 |  0.4624 | not significant |                             |
| Insurance sector (EW S&P500 PIT) excess | enso_el_nino vs not            |     -0.0063 |  -1.2009 | 0.2898 |        1 | 0.9912 |   -0.0023 | 0.6747 |    -0.0091 |  0.3871 | not significant |                             |
| Utilities sector (EW S&P500 PIT) excess | summer_JJA vs not              |     -0.008  |  -1.0843 | 0.2898 |        1 | 0.9912 |   -0.0052 | 0.5952 |    -0.0103 |  0.3492 | not significant |                             |
| strategy excess | hurricane_season_JunNov vs not                         |      0.0079 |   1.5524 | 0.322  |        1 | 0.9912 |    0.0036 | 0.5246 |     0.0118 |  0.383  | not significant |                             |
| Utilities sector (EW S&P500 PIT) excess | temp_anom_prev_cold vs not     |      0.0081 |   1.0323 | 0.3239 |        1 | 0.9912 |   -0.0026 | 0.8434 |     0.0191 |  0.1258 | not significant |                             |
| Energy sector (EW S&P500 PIT) excess | enso_el_nino vs not               |     -0.0136 |  -0.9952 | 0.3295 |        1 | 0.9912 |   -0.0075 | 0.6113 |    -0.0197 |  0.4516 | not significant |                             |
| strategy excess | temp_anom_prev_cold vs not                             |      0.0058 |   1.1434 | 0.3672 |        1 | 0.9912 |    0.001  | 0.8658 |     0.0114 |  0.3723 | not significant |                             |
| Energy sector (EW S&P500 PIT) excess | temp_anom_prev_cold vs not        |      0.0139 |   1.351  | 0.392  |        1 | 0.9912 |    0.0136 | 0.2651 |     0.0173 |  0.4086 | not significant |                             |
| Energy sector (EW S&P500 PIT) excess | summer_JJA vs not                 |     -0.0107 |  -1.0511 | 0.392  |        1 | 0.9912 |   -0.001  | 0.9266 |    -0.0195 |  0.3333 | not significant |                             |
| strategy excess | temp_anom_prev_hot vs not                              |     -0.0044 |  -0.7614 | 0.4481 |        1 | 0.9912 |   -0.0003 | 0.988  |    -0.0078 |  0.3764 | not significant |                             |
| Insurance sector (EW S&P500 PIT) excess | enso_la_nina vs not            |      0.005  |   0.7012 | 0.4865 |        1 | 0.9912 |   -0.0112 | 0.1771 |     0.0145 |  0.1452 | not significant |                             |
| Energy sector (EW S&P500 PIT) excess | winter_DJF vs not                 |      0.0084 |   0.6859 | 0.5568 |        1 | 0.9912 |   -0.0106 | 0.3976 |     0.0249 |  0.2581 | not significant |                             |
| Insurance sector (EW S&P500 PIT) excess | hurricane_season_JunNov vs not |      0.003  |   0.5831 | 0.5606 |        1 | 0.9912 |    0.005  | 0.2828 |     0.0011 |  0.9002 | not significant |                             |
| Utilities sector (EW S&P500 PIT) excess | enso_la_nina vs not            |      0.0047 |   0.5388 | 0.5923 |        1 | 0.9912 |   -0.0025 | 0.8763 |     0.0105 |  0.347  | not significant |                             |
| Energy sector (EW S&P500 PIT) excess | temp_anom_prev_hot vs not         |     -0.0061 |  -0.4624 | 0.645  |        1 | 0.9912 |   -0.0022 | 0.8916 |    -0.0119 |  0.5619 | not significant |                             |
| Energy sector (EW S&P500 PIT) excess | hurricane_peak_AugOct vs not      |     -0.0053 |  -0.4794 | 0.6818 |        1 | 0.9912 |   -0.0033 | 0.8313 |    -0.007  |  0.7849 | not significant |                             |
| Utilities sector (EW S&P500 PIT) excess | winter_DJF vs not              |      0.0031 |   0.3772 | 0.7072 |        1 | 0.9912 |    0.0047 | 0.7043 |     0.0018 |  0.914  | not significant |                             |
| Agriculture sector (EW S&P500 PIT) excess | temp_anom_prev_hot vs not    |     -0.0026 |  -0.3001 | 0.7646 |        1 | 0.9912 |   -0.0059 | 0.5887 |    -0.0008 |  0.9523 | not significant | ag sleeve has only ~4 names |
| Agriculture sector (EW S&P500 PIT) excess | summer_JJA vs not            |     -0.0019 |  -0.24   | 0.8305 |        1 | 0.9912 |   -0.0043 | 0.759  |     0.0001 |  1      | not significant | ag sleeve has only ~4 names |
| Utilities sector (EW S&P500 PIT) excess | enso_el_nino vs not            |     -0.0006 |  -0.0735 | 0.9416 |        1 | 0.9912 |    0.0104 | 0.3749 |    -0.0091 |  0.3763 | not significant |                             |

Code: `hyp/build_panels.py`, `hyp/regimes.py`, `hyp/run_tests.py`, `hyp/stats_util.py`
