# hyp-segments

Sector, ex-financials and financials-only, market-cap bucket, score level, value metric, and extra pick-level patterns (momentum, falling knife, volatility, debt, quality, rank, repeat holdings)

All 147 tests in the global pool (results/hyp_all_tests.csv) are corrected together.
- `p` is the larger of the t-test p and the bootstrap/permutation p (circular-shift permutation of the regime flag, so persistence is preserved).
- `p_bonf` is the Bonferroni-adjusted p, and `q_BH` is the Benjamini-Hochberg q.
- In-sample (IS) is 2012–2018; out-of-sample (OOS) is 2019–2026.
- ROBUST means q_BH<0.10, IS p<0.05, and OOS has the same sign with p<0.10.
- Means are quarterly excess returns (segments) or monthly excess-return differences, in-regime minus out-of-regime (regimes).

| hypothesis                                                               |   full_mean |   full_t |      p |   p_bonf |   q_BH |   IS_mean |   p_IS |   OOS_mean |   p_OOS | verdict         | note   |
|:-------------------------------------------------------------------------|------------:|---------:|-------:|---------:|-------:|----------:|-------:|-----------:|--------:|:----------------|:-------|
| sector=Tech: minus other passers (quarterly)                             |      0.0174 |   2.0443 | 0.0454 |        1 | 0.6851 |    0.009  | 0.4209 |     0.0248 |  0.0611 | not significant |        |
| sector=Materials: sleeve EW excess vs SPY (quarterly)                    |     -0.0198 |  -2.0233 | 0.0476 |        1 | 0.6851 |   -0.0356 | 0.0479 |    -0.006  |  0.5607 | IN-SAMPLE ONLY  |        |
| sector=RealEstate: sleeve EW excess vs SPY (quarterly)                   |     -0.0168 |  -1.9269 | 0.0588 |        1 | 0.6851 |   -0.0074 | 0.5349 |    -0.025  |  0.0578 | not significant |        |
| sector=Materials: minus other passers (quarterly)                        |     -0.0186 |  -1.9074 | 0.0613 |        1 | 0.6851 |   -0.037  | 0.041  |    -0.0025 |  0.7989 | IN-SAMPLE ONLY  |        |
| sector=Staples: sleeve EW excess vs SPY (quarterly)                      |     -0.0225 |  -1.921  | 0.0629 |        1 | 0.6851 |   -0.0412 | 0.0031 |    -0.0119 |  0.4901 | IN-SAMPLE ONLY  |        |
| sector=Tech: sleeve EW excess vs SPY (quarterly)                         |      0.0131 |   1.8754 | 0.0657 |        1 | 0.6851 |    0.0089 | 0.4304 |     0.0168 |  0.0683 | not significant |        |
| sector=RealEstate: minus other passers (quarterly)                       |     -0.0162 |  -1.772  | 0.0816 |        1 | 0.7763 |   -0.0085 | 0.551  |    -0.0229 |  0.0691 | not significant |        |
| mcap>50B: minus other passers (quarterly)                                |      0.0078 |   1.6645 | 0.1013 |        1 | 0.7763 |    0.0082 | 0.2064 |     0.0075 |  0.289  | not significant |        |
| sector=Staples: minus other passers (quarterly)                          |     -0.0183 |  -1.6429 | 0.1094 |        1 | 0.7763 |   -0.0362 | 0.0208 |    -0.0082 |  0.6006 | IN-SAMPLE ONLY  |        |
| extra: low-vol tercile: sleeve EW excess vs SPY (quarterly)              |     -0.0076 |  -1.6149 | 0.1117 |        1 | 0.7763 |   -0.0007 | 0.8635 |    -0.0137 |  0.1026 | not significant |        |
| extra: high-vol tercile: minus other passers (quarterly)                 |      0.0107 |   1.4297 | 0.1581 |        1 | 0.9568 |    0.0045 | 0.5838 |     0.016  |  0.1939 | not significant |        |
| extra: low-vol tercile: minus other passers (quarterly)                  |     -0.0089 |  -1.4157 | 0.1621 |        1 | 0.9568 |   -0.0018 | 0.8108 |    -0.0152 |  0.1333 | not significant |        |
| mcap tercile=small (within passers): minus other passers (quarterly)     |     -0.0056 |  -1.3281 | 0.1893 |        1 | 0.9912 |   -0.0026 | 0.6334 |    -0.0082 |  0.2088 | not significant |        |
| Top20: rank 1-10: minus other passers (quarterly)                        |     -0.0097 |  -1.2469 | 0.2174 |        1 | 0.9912 |   -0.0048 | 0.6075 |    -0.0139 |  0.2619 | not significant |        |
| Top20: rank 11-20: minus other passers (quarterly)                       |      0.0097 |   1.2469 | 0.2174 |        1 | 0.9912 |    0.0048 | 0.6075 |     0.0139 |  0.2619 | not significant |        |
| metric NI growth>50% (rebound): minus other passers (quarterly)          |     -0.0056 |  -1.1836 | 0.2413 |        1 | 0.9912 |   -0.0004 | 0.8962 |    -0.0101 |  0.2358 | not significant |        |
| metric NI growth>50% (rebound): sleeve EW excess vs SPY (quarterly)      |     -0.005  |  -1.1446 | 0.257  |        1 | 0.9912 |    0.0002 | 0.9735 |    -0.0096 |  0.1718 | not significant |        |
| mcap tercile=large (within passers): minus other passers (quarterly)     |      0.006  |   1.1564 | 0.2575 |        1 | 0.9912 |    0.0071 | 0.2703 |     0.005  |  0.5406 | not significant |        |
| extra: 12m momentum>0: minus other passers (quarterly)                   |      0.0083 |   1.1234 | 0.2658 |        1 | 0.9912 |    0.0137 | 0.2094 |     0.0036 |  0.7299 | not significant |        |
| sector=Health: sleeve EW excess vs SPY (quarterly)                       |     -0.008  |  -1.1083 | 0.273  |        1 | 0.9912 |    0.0038 | 0.7034 |    -0.0184 |  0.081  | not significant |        |
| mcap>50B: sleeve EW excess vs SPY (quarterly)                            |      0.0036 |   1.0485 | 0.2987 |        1 | 0.9912 |    0.0067 | 0.2233 |     0.0008 |  0.8521 | not significant |        |
| mcap tercile=small (within passers): sleeve EW excess vs SPY (quarterly) |     -0.0054 |  -1.0109 | 0.3162 |        1 | 0.9912 |   -0.0012 | 0.8608 |    -0.0091 |  0.2795 | not significant |        |
| extra: low debt D/E<0.3 (non-fin): minus other passers (quarterly)       |      0.0049 |   0.9994 | 0.3232 |        1 | 0.9912 |   -0.0034 | 0.5665 |     0.0122 |  0.1179 | not significant |        |
| score<=4: minus other passers (quarterly)                                |      0.0058 |   0.9785 | 0.3318 |        1 | 0.9912 |    0.0097 | 0.1044 |     0.0023 |  0.8203 | not significant |        |
| score 5-6: minus other passers (quarterly)                               |     -0.0053 |  -0.9075 | 0.3688 |        1 | 0.9912 |   -0.0114 | 0.0401 |    -0      |  0.9963 | IN-SAMPLE ONLY  |        |
| extra: 12m momentum>0: sleeve EW excess vs SPY (quarterly)               |     -0.0029 |  -0.878  | 0.3835 |        1 | 0.9912 |    0.0019 | 0.5852 |    -0.0071 |  0.1904 | not significant |        |
| sector=Health: minus other passers (quarterly)                           |     -0.007  |  -0.8672 | 0.3893 |        1 | 0.9912 |    0.0035 | 0.776  |    -0.0162 |  0.138  | not significant |        |
| score 5-6: sleeve EW excess vs SPY (quarterly)                           |     -0.006  |  -0.8438 | 0.4022 |        1 | 0.9912 |   -0.0095 | 0.1617 |    -0.0029 |  0.8105 | not significant |        |
| extra: high-vol tercile: sleeve EW excess vs SPY (quarterly)             |      0.0054 |   0.8261 | 0.4121 |        1 | 0.9912 |    0.0036 | 0.6851 |     0.0071 |  0.4774 | not significant |        |
| extra: 6m drop >20% (falling knife): sleeve EW excess vs SPY (quarterly) |     -0.0102 |  -0.7132 | 0.4788 |        1 | 0.9912 |    0.0067 | 0.781  |    -0.0264 |  0.109  | not significant |        |
| mcap tercile=large (within passers): sleeve EW excess vs SPY (quarterly) |      0.0023 |   0.7055 | 0.4863 |        1 | 0.9912 |    0.0053 | 0.2426 |    -0.0003 |  0.9483 | not significant |        |
| Top20: rank 1-10: sleeve EW excess vs SPY (quarterly)                    |     -0.0051 |  -0.6252 | 0.5342 |        1 | 0.9912 |   -0.0019 | 0.8426 |    -0.0079 |  0.5464 | not significant |        |
| Top20: repeat holding: sleeve EW excess vs SPY (quarterly)               |     -0.0056 |  -0.6141 | 0.5415 |        1 | 0.9912 |   -0.009  | 0.4392 |    -0.0027 |  0.8512 | not significant |        |
| sector=Industrials: sleeve EW excess vs SPY (quarterly)                  |     -0.0031 |  -0.6001 | 0.5508 |        1 | 0.9912 |   -0.004  | 0.4486 |    -0.0024 |  0.7841 | not significant |        |
| Top20: repeat holding: minus other passers (quarterly)                   |     -0.0054 |  -0.554  | 0.5817 |        1 | 0.9912 |   -0.0052 | 0.7371 |    -0.0055 |  0.6633 | not significant |        |
| Top20: new entry: minus other passers (quarterly)                        |      0.0054 |   0.554  | 0.583  |        1 | 0.9912 |    0.0052 | 0.7371 |     0.0055 |  0.6633 | not significant |        |
| extra: 6m drop >20% (falling knife): minus other passers (quarterly)     |     -0.008  |  -0.5685 | 0.5857 |        1 | 0.9912 |    0.0057 | 0.8092 |    -0.0212 |  0.1856 | not significant |        |
| Top20: rank 11-20: sleeve EW excess vs SPY (quarterly)                   |      0.0046 |   0.5447 | 0.588  |        1 | 0.9912 |    0.0028 | 0.7959 |     0.0061 |  0.6349 | not significant |        |
| ex-financials: sleeve EW excess vs SPY (quarterly)                       |     -0.0017 |  -0.5389 | 0.592  |        1 | 0.9912 |   -0.0007 | 0.8722 |    -0.0025 |  0.5852 | not significant |        |
| sector=Utilities: sleeve EW excess vs SPY (quarterly)                    |     -0.0098 |  -0.5427 | 0.593  |        1 | 0.9912 |   -0.0061 | 0.7515 |    -0.0262 |  0.6723 | not significant |        |
| metric P/B<1: minus other passers (quarterly)                            |      0.0058 |   0.5367 | 0.5936 |        1 | 0.9912 |    0.0135 | 0.306  |    -0.002  |  0.9074 | not significant |        |
| All passers EW excess vs SPY (quarterly)                                 |     -0.0017 |  -0.5115 | 0.6115 |        1 | 0.9912 |    0.0005 | 0.8989 |    -0.0037 |  0.478  | not significant |        |
| metric ROE>20%: minus other passers (quarterly)                          |      0.002  |   0.5078 | 0.6135 |        1 | 0.9912 |    0.0049 | 0.403  |    -0.0005 |  0.9303 | not significant |        |
| sector=ConsDisc: sleeve EW excess vs SPY (quarterly)                     |     -0.0028 |  -0.4812 | 0.6322 |        1 | 0.9912 |    0.0009 | 0.9076 |    -0.0061 |  0.5053 | not significant |        |
| sector=Banks/DivFin: minus other passers (quarterly)                     |      0.0037 |   0.4508 | 0.6542 |        1 | 0.9912 |    0.0025 | 0.8297 |     0.0048 |  0.6896 | not significant |        |
| mcap tercile=mid (within passers): sleeve EW excess vs SPY (quarterly)   |     -0.0019 |  -0.4506 | 0.655  |        1 | 0.9912 |   -0.0025 | 0.6296 |    -0.0014 |  0.839  | not significant |        |
| sector=Utilities: minus other passers (quarterly)                        |     -0.0077 |  -0.4263 | 0.6742 |        1 | 0.9912 |   -0.0086 | 0.679  |    -0.004  |  0.9369 | not significant |        |
| extra: low debt D/E<0.3 (non-fin): sleeve EW excess vs SPY (quarterly)   |      0.0014 |   0.4061 | 0.693  |        1 | 0.9912 |   -0.0012 | 0.8092 |     0.0037 |  0.4607 | not significant |        |
| extra: quality ROE>15% & D/E<0.5: sleeve EW excess vs SPY (quarterly)    |     -0.0014 |  -0.3651 | 0.7164 |        1 | 0.9912 |    0.0002 | 0.976  |    -0.0027 |  0.6123 | not significant |        |
| sector=Comm: minus other passers (quarterly)                             |      0.0269 |   0.3621 | 0.7211 |        1 | 0.9912 |    0.1613 | 0.29   |    -0.0739 |  0.2846 | not significant |        |
| metric P/E<10: minus other passers (quarterly)                           |      0.0029 |   0.3586 | 0.7258 |        1 | 0.9912 |    0.006  | 0.5924 |     0.0002 |  0.987  | not significant |        |
| sector=Industrials: minus other passers (quarterly)                      |     -0.0014 |  -0.3225 | 0.7482 |        1 | 0.9912 |   -0.0049 | 0.219  |     0.0017 |  0.8221 | not significant |        |
| metric P/FCF<10: sleeve EW excess vs SPY (quarterly)                     |     -0.0026 |  -0.3191 | 0.7512 |        1 | 0.9912 |   -0.0034 | 0.7578 |    -0.0018 |  0.8798 | not significant |        |
| sector=Comm: sleeve EW excess vs SPY (quarterly)                         |      0.0246 |   0.3203 | 0.7521 |        1 | 0.9912 |    0.164  | 0.2957 |    -0.0799 |  0.2707 | not significant |        |
| metric rev growth>10%: sleeve EW excess vs SPY (quarterly)               |     -0.0012 |  -0.3072 | 0.7598 |        1 | 0.9912 |   -0.0014 | 0.8073 |    -0.001  |  0.856  | not significant |        |
| ex-financials: minus other passers (quarterly)                           |     -0.002  |  -0.2909 | 0.7722 |        1 | 0.9912 |   -0.0049 | 0.5964 |     0.0005 |  0.9647 | not significant |        |
| financials (Ins+Banks/DivFin): minus other passers (quarterly)           |      0.002  |   0.2909 | 0.7722 |        1 | 0.9912 |    0.0049 | 0.5964 |    -0.0005 |  0.9685 | not significant |        |
| metric P/B<1: sleeve EW excess vs SPY (quarterly)                        |      0.0032 |   0.2783 | 0.7818 |        1 | 0.9912 |    0.0124 | 0.3747 |    -0.006  |  0.7461 | not significant |        |
| mcap<10B: minus other passers (quarterly)                                |      0.0022 |   0.2747 | 0.7845 |        1 | 0.9912 |    0.002  | 0.818  |     0.0024 |  0.8575 | not significant |        |
| sector=Insurance: minus other passers (quarterly)                        |      0.0019 |   0.264  | 0.7927 |        1 | 0.9912 |    0.0056 | 0.3351 |    -0.0013 |  0.9235 | not significant |        |
| metric PEG<0.5: minus other passers (quarterly)                          |      0.001  |   0.2417 | 0.8143 |        1 | 0.9912 |   -0.001  | 0.859  |     0.0028 |  0.6549 | not significant |        |
| metric rev growth>10%: minus other passers (quarterly)                   |      0.0013 |   0.2351 | 0.815  |        1 | 0.9912 |   -0.0033 | 0.626  |     0.0052 |  0.5293 | not significant |        |
| Strategy Top20 monthly excess vs SPY                                     |     -0.0006 |  -0.2332 | 0.8159 |        1 | 0.9912 |   -0.0008 | 0.7875 |    -0.0004 |  0.915  | not significant |        |
| sector=Banks/DivFin: sleeve EW excess vs SPY (quarterly)                 |      0.002  |   0.2276 | 0.8207 |        1 | 0.9912 |    0.0029 | 0.8127 |     0.0013 |  0.9237 | not significant |        |
| score<=4: sleeve EW excess vs SPY (quarterly)                            |     -0.0006 |  -0.191  | 0.8492 |        1 | 0.9912 |    0.0016 | 0.6815 |    -0.0025 |  0.5645 | not significant |        |
| metric PEG<0.5: sleeve EW excess vs SPY (quarterly)                      |     -0.001  |  -0.189  | 0.8508 |        1 | 0.9912 |   -0.0007 | 0.9227 |    -0.0012 |  0.8722 | not significant |        |
| sector=ConsDisc: minus other passers (quarterly)                         |     -0.001  |  -0.1566 | 0.8761 |        1 | 0.9912 |    0.0007 | 0.9341 |    -0.0024 |  0.8035 | not significant |        |
| metric P/FCF<10: minus other passers (quarterly)                         |     -0.001  |  -0.1385 | 0.8903 |        1 | 0.9912 |   -0.0041 | 0.679  |     0.0017 |  0.8764 | not significant |        |
| score>=7: sleeve EW excess vs SPY (quarterly)                            |     -0.0015 |  -0.1338 | 0.8941 |        1 | 0.9912 |    0.0092 | 0.628  |    -0.0104 |  0.4681 | not significant |        |
| mcap tercile=mid (within passers): minus other passers (quarterly)       |     -0.0004 |  -0.1084 | 0.9145 |        1 | 0.9912 |   -0.0046 | 0.261  |     0.0033 |  0.545  | not significant |        |
| sector=Energy: sleeve EW excess vs SPY (quarterly)                       |     -0.0016 |  -0.0896 | 0.9303 |        1 | 0.9912 |   -0.0058 | 0.7992 |     0.0016 |  0.9524 | not significant |        |
| extra: quality ROE>15% & D/E<0.5: minus other passers (quarterly)        |      0.0003 |   0.0841 | 0.9333 |        1 | 0.9912 |   -0.0008 | 0.8905 |     0.0013 |  0.8036 | not significant |        |
| Top20: new entry: sleeve EW excess vs SPY (quarterly)                    |      0.0008 |   0.0818 | 0.9377 |        1 | 0.9912 |   -0.0015 | 0.9195 |     0.0028 |  0.8442 | not significant |        |
| metric ROE>20%: sleeve EW excess vs SPY (quarterly)                      |     -0.0002 |  -0.0615 | 0.9511 |        1 | 0.9912 |    0.0041 | 0.4426 |    -0.004  |  0.4563 | not significant |        |
| financials (Ins+Banks/DivFin): sleeve EW excess vs SPY (quarterly)       |      0.0004 |   0.053  | 0.9607 |        1 | 0.9912 |    0.0042 | 0.6325 |    -0.003  |  0.7874 | not significant |        |
| Top20 picks EW excess vs SPY (quarterly)                                 |     -0.0003 |  -0.0369 | 0.9707 |        1 | 0.9912 |    0.0005 | 0.9603 |    -0.0009 |  0.9361 | not significant |        |
| metric P/E<10: sleeve EW excess vs SPY (quarterly)                       |      0.0003 |   0.0307 | 0.9756 |        1 | 0.9912 |    0.0048 | 0.6859 |    -0.0037 |  0.7834 | not significant |        |
| sector=Insurance: sleeve EW excess vs SPY (quarterly)                    |      0.0002 |   0.0301 | 0.9775 |        1 | 0.9912 |    0.0053 | 0.3994 |    -0.0042 |  0.7523 | not significant |        |
| score>=7: minus other passers (quarterly)                                |     -0.0003 |  -0.0265 | 0.9798 |        1 | 0.9912 |    0.0093 | 0.5713 |    -0.0082 |  0.5323 | not significant |        |
| mcap<10B: sleeve EW excess vs SPY (quarterly)                            |      0.0002 |   0.0196 | 0.9844 |        1 | 0.9912 |    0.001  | 0.9263 |    -0.0005 |  0.9758 | not significant |        |
| sector=Energy: minus other passers (quarterly)                           |     -0.0002 |  -0.0086 | 0.9932 |        1 | 0.9932 |   -0.0063 | 0.7905 |     0.0046 |  0.8581 | not significant |        |

Code: `hyp/build_panels.py`, `hyp/regimes.py`, `hyp/run_tests.py`, `hyp/stats_util.py`
