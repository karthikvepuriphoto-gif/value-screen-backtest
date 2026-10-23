# hyp-election

Presidential cycle, party in power, and months around elections. **Small-sample warning:** about 3.5 cycles and 4 presidential elections.

All 147 tests in the global pool (results/hyp_all_tests.csv) are corrected together.
- `p` is the larger of the t-test p and the bootstrap/permutation p (circular-shift permutation of the regime flag, so persistence is preserved).
- `p_bonf` is the Bonferroni-adjusted p, and `q_BH` is the Benjamini-Hochberg q.
- In-sample (IS) is 2012–2018; out-of-sample (OOS) is 2019–2026.
- ROBUST means q_BH<0.10, IS p<0.05, and OOS has the same sign with p<0.10.
- Means are quarterly excess returns (segments) or monthly excess-return differences, in-regime minus out-of-regime (regimes).

| hypothesis                                     |   full_mean |   full_t |      p |   p_bonf |   q_BH |   IS_mean |   p_IS |   OOS_mean |   p_OOS | verdict         | note                      |
|:-----------------------------------------------|------------:|---------:|-------:|---------:|-------:|----------:|-------:|-----------:|--------:|:----------------|:--------------------------|
| strategy excess | pres_election_pm3m vs not    |      0.0182 |   2.6224 | 0.0226 |        1 | 0.6851 |    0.0244 | 0.0241 |     0.0122 |  0.3298 | IN-SAMPLE ONLY  | SMALL SAMPLE: ~3.5 cycles |
| strategy excess | post_pres_election_6m vs not |      0.0172 |   2.5533 | 0.0395 |        1 | 0.6851 |    0.0161 | 0.1446 |     0.0184 |  0.1489 | not significant | SMALL SAMPLE: ~3.5 cycles |
| strategy excess | cycle_yr1 vs not             |      0.0069 |   1.4292 | 0.1808 |        1 | 0.9912 |    0.0074 | 0.5422 |     0.0064 |  0.4681 | not significant | SMALL SAMPLE: ~3.5 cycles |
| strategy excess | party_R_president vs not     |     -0.0032 |  -0.5881 | 0.5576 |        1 | 0.9912 |   -0.0089 | 0.1807 |     0.0005 |  0.9561 | not significant | SMALL SAMPLE: ~3.5 cycles |
| strategy excess | cycle_yr2_midterm vs not     |     -0.0026 |  -0.4067 | 0.6855 |        1 | 0.9912 |   -0.0142 | 0.1325 |     0.0093 |  0.4211 | not significant | SMALL SAMPLE: ~3.5 cycles |
| strategy excess | cycle_yr4_election vs not    |     -0.0025 |  -0.4007 | 0.6898 |        1 | 0.9912 |    0.01   | 0.3976 |    -0.0141 |  0.142  | not significant | SMALL SAMPLE: ~3.5 cycles |
| strategy excess | cycle_yr3_preelection vs not |     -0.0024 |  -0.3658 | 0.7232 |        1 | 0.9912 |   -0.0049 | 0.7108 |    -0.0011 |  0.9255 | not significant | SMALL SAMPLE: ~3.5 cycles |
| strategy excess | midterm_election_pm3m vs not |      0.001  |   0.1192 | 0.906  |        1 | 0.9912 |   -0.0154 | 0.1566 |     0.0171 |  0.234  | not significant | SMALL SAMPLE: ~3.5 cycles |

Code: `hyp/build_panels.py`, `hyp/regimes.py`, `hyp/run_tests.py`, `hyp/stats_util.py`
