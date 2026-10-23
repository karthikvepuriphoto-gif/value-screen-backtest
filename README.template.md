# value-screen-backtest

A rules-based, point-in-time backtest of a value checklist taken from the *Investing Club* YouTube channel (2019–2022): Buffett, Phil Town (Rule #1), Peter Lynch's PEG and Greenblatt-style metrics.

**Research only, not investment advice.**

## Strategy (parameters fixed in advance from the creator's stated rules; nothing was tuned)
- **Rebalance:** quarterly, on the first trading day of Jan, Apr, Jul and Oct (2012-01 to 2026-10).
- **Must pass (all companies):** market cap > $500M, net income > 0 and above the prior year (rising earnings).
- **Must pass (non-financials only):** FCF (CFO − capex) > 0, long-term debt / equity < 1, and current ratio > 1 when it is reported.
- **Score:**
  - P/FCF < 10 (2 points) or < 15 (1 point)
  - P/E ≤ 15
  - PEG < 1, using 3-year net income CAGR
  - P/B < 1.5
  - ROE > 15%
  - revenue growth > 5%
  - net income growth > 15%
- **Ranking:** by score, with ties broken by earnings yield. Buy the top N at equal weight, capped at 5% (Top 10 is uncapped at 10% each, because a 5% cap would leave it half in cash).
- **Optional stop:** sell a position if it falls 40% from its peak since entry. The cash is held until the next rebalance.
- **Costs:** 10 bps on traded notional.

## Data, point in time
- **Fundamentals:** SEC EDGAR XBRL `companyfacts`. Each value is used only after its **first filing date**, so restatements cause no lookahead. Flow items (net income, revenue, CFO, capex) are annual 10-K figures. Balance-sheet items and shares are the latest 10-K or 10-Q values.
- **Market cap:** yfinance close with splits backed out, multiplied by the shares outstanding reported on the cover page.
- **Prices:** yfinance adjusted close. Benchmarks are SPY (cap-weighted) and RSP (equal-weight S&P 500).

## Results (2012-01-03 to 2026-10-22)
The 2019–2026 period is effectively out of sample, since the rules came from videos made in 2019–2022 and were not fitted to data. Turnover is one-way per year over the full period.

{STATS}

![equity](results/equity_curve.png)

### Calendar-year returns (2026 is year to date)
{YEARLY}

## Current portfolio (Top 20 as of 2026-10-22)
See [`current_portfolio.csv`](current_portfolio.csv): {PICKS}.

## Caveats
- **Survivorship bias:** the universe is *today's* S&P 500 + S&P 400, so companies that went bankrupt or were acquired between 2012 and 2026 are missing. This almost certainly inflates returns. A survivorship-free version needs historical index membership plus prices for delisted names.
- **Missing data:** about 100–270 names per date lack usable XBRL data or price history (early years especially), and OZK has no SEC XBRL data at all (it files with the FDIC).
- **Sector labels:** financials are identified with *current* yfinance sectors, and a few names have no label.
- **Stale and coarse fundamentals:** annual flow data can be up to about 15 months old. The XBRL tag choice is simple (LongTermDebt only, so leases and short-term debt are ignored).
- **Concentration:** the screen heavily favors insurers, banks and other financials, so results are a concentrated factor bet (value plus financials) with higher volatility and drawdown than SPY.
- **Cost model:** no taxes, no slippage beyond 10 bps, and the risk-free rate is 0 in the Sharpe ratio.

## Run
```
pip install -r requirements.txt
python fetch_sec.py      # SEC companyfacts (sets a User-Agent)
python fetch_prices.py   # yfinance prices (re-run for tickers Yahoo rate-limits)
python backtest.py
python make_readme.py
```
