# Phase 3 summary: survivorship fix and hypothesis tests

**Bottom line:**
- With survivorship bias removed (point-in-time S&P 500), the screen returns **13.2% CAGR** with Sharpe 0.68. SPY returned **14.8%** with Sharpe 0.92 over 2012–2026.
- The biased universe had shown 16.0%.
- **None** of the 147 hypotheses survives Benjamini-Hochberg (min q_BH = 0.69) or Bonferroni correction, and none is both in-sample and out-of-sample significant.
- 7 effects were significant in-sample only.
- No variant from the 42 parameter, filter, and regime-gate runs beats SPY significantly.
- **Paper-trading candidates: none.**

Branches: [survivorship-fix](https://github.com/karthikvepuriphoto-gif/value-screen-backtest/tree/survivorship-fix) · [hyp-segments](https://github.com/karthikvepuriphoto-gif/value-screen-backtest/tree/hyp-segments) · [hyp-election](https://github.com/karthikvepuriphoto-gif/value-screen-backtest/tree/hyp-election) · [hyp-seasonality](https://github.com/karthikvepuriphoto-gif/value-screen-backtest/tree/hyp-seasonality) · [hyp-weather](https://github.com/karthikvepuriphoto-gif/value-screen-backtest/tree/hyp-weather) · [hyp-macro](https://github.com/karthikvepuriphoto-gif/value-screen-backtest/tree/hyp-macro) · [hyp-combos-regime-switch](https://github.com/karthikvepuriphoto-gif/value-screen-backtest/tree/hyp-combos-regime-switch) · [hyp-robustness](https://github.com/karthikvepuriphoto-gif/value-screen-backtest/tree/hyp-robustness). Details are in [SURVIVORSHIP.md](SURVIVORSHIP.md).

## Lowest-p hypotheses (global pool of 147 tests)
| family      | hypothesis                                                             |   full_mean |     p |   p_bonf |   q_BH |   IS_mean |   p_IS |   OOS_mean |   p_OOS | verdict         |
|:------------|:-----------------------------------------------------------------------|------------:|------:|---------:|-------:|----------:|-------:|-----------:|--------:|:----------------|
| weather     | Energy sector (EW S&P500 PIT) excess | enso_la_nina vs not             |       0.045 | 0.011 |        1 |  0.685 |     0.008 |  0.669 |      0.058 |   0.011 | not significant |
| election    | strategy excess | pres_election_pm3m vs not                            |       0.018 | 0.023 |        1 |  0.685 |     0.024 |  0.024 |      0.012 |   0.33  | IN-SAMPLE ONLY  |
| weather     | Agriculture sector (EW S&P500 PIT) excess | enso_la_nina vs not        |       0.03  | 0.034 |        1 |  0.685 |     0.004 |  0.819 |      0.042 |   0.053 | not significant |
| election    | strategy excess | post_pres_election_6m vs not                         |       0.017 | 0.04  |        1 |  0.685 |     0.016 |  0.145 |      0.018 |   0.149 | not significant |
| seasonality | strategy excess | month_05 vs not                                      |      -0.021 | 0.041 |        1 |  0.685 |    -0.01  |  0.357 |     -0.031 |   0.08  | not significant |
| weather     | Agriculture sector (EW S&P500 PIT) excess | temp_anom_prev_cold vs not |       0.019 | 0.045 |        1 |  0.685 |     0.02  |  0.024 |      0.019 |   0.309 | IN-SAMPLE ONLY  |
| seasonality | strategy excess | quarter_Q4 vs not                                    |       0.013 | 0.045 |        1 |  0.685 |     0.006 |  0.427 |      0.02  |   0.044 | not significant |
| segment     | sector=Tech: minus other passers (quarterly)                           |       0.017 | 0.045 |        1 |  0.685 |     0.009 |  0.421 |      0.025 |   0.061 | not significant |
| seasonality | strategy excess | month_11 vs not                                      |       0.022 | 0.047 |        1 |  0.685 |     0.017 |  0.329 |      0.026 |   0.096 | not significant |
| segment     | sector=Materials: sleeve EW excess vs SPY (quarterly)                  |      -0.02  | 0.048 |        1 |  0.685 |    -0.036 |  0.048 |     -0.006 |   0.561 | IN-SAMPLE ONLY  |
| segment     | sector=RealEstate: sleeve EW excess vs SPY (quarterly)                 |      -0.017 | 0.059 |        1 |  0.685 |    -0.007 |  0.535 |     -0.025 |   0.058 | not significant |
| segment     | sector=Materials: minus other passers (quarterly)                      |      -0.019 | 0.061 |        1 |  0.685 |    -0.037 |  0.041 |     -0.003 |   0.799 | IN-SAMPLE ONLY  |
| segment     | sector=Staples: sleeve EW excess vs SPY (quarterly)                    |      -0.022 | 0.063 |        1 |  0.685 |    -0.041 |  0.003 |     -0.012 |   0.49  | IN-SAMPLE ONLY  |
| segment     | sector=Tech: sleeve EW excess vs SPY (quarterly)                       |       0.013 | 0.066 |        1 |  0.685 |     0.009 |  0.43  |      0.017 |   0.068 | not significant |
| segment     | sector=RealEstate: minus other passers (quarterly)                     |      -0.016 | 0.082 |        1 |  0.776 |    -0.008 |  0.551 |     -0.023 |   0.069 | not significant |

## Best variants by CAGR (SPY 14.8%)
| variant                           |   full_CAGR |   full_Sharpe |   IS_CAGR |   OOS_CAGR |   full_vsSPY_t |   q_BH_vsBase |
|:----------------------------------|------------:|--------------:|----------:|-----------:|---------------:|--------------:|
| D/E<0.5                           |       0.146 |         0.736 |     0.121 |      0.168 |          0.17  |         0.878 |
| gate: curve not inverted else SPY |       0.146 |         0.755 |     0.113 |      0.176 |          0.13  |         0.878 |
| gate: S&P>200d else SPY           |       0.14  |         0.754 |     0.121 |      0.157 |          0.022 |         0.88  |
| semiannual rebal                  |       0.14  |         0.725 |     0.115 |      0.162 |         -0.006 |         0.878 |
| ex Materials+Staples              |       0.14  |         0.715 |     0.119 |      0.158 |          0.005 |         0.878 |
| gate: oil uptrend else SPY        |       0.14  |         0.78  |     0.113 |      0.163 |         -0.253 |         0.959 |
| financials only (N10)             |       0.139 |         0.669 |     0.114 |      0.161 |          0.111 |         0.878 |
| no rising-NI rule                 |       0.139 |         0.696 |     0.111 |      0.164 |          0.02  |         0.878 |

## Caveats
- Only 24% of delisted names have prices (4% of acquisitions), and usable member coverage is 72% in 2012 rising to 98% in 2026.
- There is no point-in-time S&P 400 data.
- Macro data uses yfinance and BLS proxies because FRED was unreachable from the box.
- The election tests cover only about 3.5 cycles.

---
