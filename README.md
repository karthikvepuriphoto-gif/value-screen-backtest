# hyp-seasonality

Month of year, Halloween / Sell in May, quarter, January, turn of the year

All 147 tests in the global pool (results/hyp_all_tests.csv) are corrected together.
- `p` is the larger of the t-test p and the bootstrap/permutation p (circular-shift permutation of the regime flag, so persistence is preserved).
- `p_bonf` is the Bonferroni-adjusted p, and `q_BH` is the Benjamini-Hochberg q.
- In-sample (IS) is 2012–2018; out-of-sample (OOS) is 2019–2026.
- ROBUST means q_BH<0.10, IS p<0.05, and OOS has the same sign with p<0.10.
- Means are quarterly excess returns (segments) or monthly excess-return differences, in-regime minus out-of-regime (regimes).

| hypothesis                                   |   full_mean |   full_t |      p |   p_bonf |   q_BH |   IS_mean |   p_IS |   OOS_mean |   p_OOS | verdict         | note   |
|:---------------------------------------------|------------:|---------:|-------:|---------:|-------:|----------:|-------:|-----------:|--------:|:----------------|:-------|
| strategy excess | month_05 vs not            |     -0.0211 |  -2.2129 | 0.0414 |        1 | 0.6851 |   -0.0101 | 0.3571 |    -0.0308 |  0.0804 | not significant |        |
| strategy excess | quarter_Q4 vs not          |      0.0134 |   2.1597 | 0.0452 |        1 | 0.6851 |    0.0061 | 0.4269 |     0.0202 |  0.0437 | not significant |        |
| strategy excess | month_11 vs not            |      0.0215 |   2.1681 | 0.0466 |        1 | 0.6851 |    0.0167 | 0.3287 |     0.0264 |  0.0957 | not significant |        |
| strategy excess | quarter_Q2 vs not          |     -0.0109 |  -1.9081 | 0.1638 |        1 | 0.9568 |   -0.0063 | 0.2944 |    -0.0149 |  0.2128 | not significant |        |
| strategy excess | month_07 vs not            |      0.0097 |   1.1703 | 0.322  |        1 | 0.9912 |    0.0036 | 0.7349 |     0.0151 |  0.3723 | not significant |        |
| strategy excess | month_02 vs not            |      0.0087 |   1.3316 | 0.3672 |        1 | 0.9912 |    0.0053 | 0.5904 |     0.0118 |  0.5745 | not significant |        |
| strategy excess | month_03 vs not            |     -0.0108 |  -0.8577 | 0.4043 |        1 | 0.9912 |    0.004  | 0.6867 |    -0.0239 |  0.3295 | not significant |        |
| strategy excess | month_12 vs not            |      0.008  |   0.9212 | 0.4237 |        1 | 0.9912 |    0.0051 | 0.7182 |     0.0108 |  0.617  | not significant |        |
| strategy excess | january vs not             |     -0.0068 |  -0.7779 | 0.5028 |        1 | 0.9912 |   -0.0173 | 0.2865 |     0.0011 |  0.9894 | not significant |        |
| strategy excess | month_01 vs not            |     -0.0068 |  -0.7779 | 0.5028 |        1 | 0.9912 |   -0.0173 | 0.2865 |     0.0011 |  0.9894 | not significant |        |
| strategy excess | month_09 vs not            |     -0.0041 |  -0.5293 | 0.6158 |        1 | 0.9912 |   -0.0013 | 0.9157 |    -0.0065 |  0.8191 | not significant |        |
| strategy excess | quarter_Q1 vs not          |     -0.0035 |  -0.5756 | 0.6554 |        1 | 0.9912 |   -0.0024 | 0.6982 |    -0.0045 |  0.8191 | not significant |        |
| strategy excess | month_04 vs not            |     -0.0034 |  -0.4947 | 0.6667 |        1 | 0.9912 |   -0.0009 | 0.9398 |    -0.0055 |  0.8404 | not significant |        |
| strategy excess | halloween_NovApr vs not    |      0.0049 |   0.9591 | 0.6836 |        1 | 0.9912 |    0.0047 | 0.4068 |     0.0051 |  0.766  | not significant |        |
| strategy excess | month_10 vs not            |      0.004  |   0.3683 | 0.7176 |        1 | 0.9912 |   -0.0068 | 0.4337 |     0.0136 |  0.5143 | not significant |        |
| strategy excess | month_08 vs not            |     -0.0022 |  -0.2537 | 0.8028 |        1 | 0.9912 |    0.004  | 0.771  |    -0.0076 |  0.7766 | not significant |        |
| strategy excess | month_06 vs not            |     -0.0022 |  -0.2212 | 0.8305 |        1 | 0.9912 |   -0.0045 | 0.6747 |    -0.0001 |  1      | not significant |        |
| strategy excess | quarter_Q3 vs not          |      0.0014 |   0.2572 | 0.8701 |        1 | 0.9912 |    0.0025 | 0.6818 |     0.0004 |  0.9894 | not significant |        |
| Halloween on SPY itself (Nov-Apr vs May-Oct) |      0.0007 |   0.1168 | 0.9072 |        1 | 0.9912 |    0.0013 | 0.8524 |     0.0003 |  0.9793 | not significant |        |
| strategy excess | turn_of_year_DecJan vs not |      0.0006 |   0.0972 | 0.9718 |        1 | 0.9912 |   -0.0058 | 0.5799 |     0.0062 |  0.7447 | not significant |        |

Code: `hyp/build_panels.py`, `hyp/regimes.py`, `hyp/run_tests.py`, `hyp/stats_util.py`
