# Bot health

Run `20261120T025342Z-daily-35af0d` at 2026-11-20T02:53:42Z, data through the 2026-11-19 session. **Status: degraded.**

## Coverage

- Universe: 503 symbols; 503 with prices; 503 current.
- Missing tickers (no prices at all): none
- Stale: none
- Missing trading days inside histories: 1 days over 1 symbols
- Missing fields in the last year of bars: none
- Delisted symbols kept: 1; membership history recorded from 2026-10-09T01:51:19Z (earlier backtests use the membership seen then).

## Checks

- missing_days: 1
- moves: 13
- staleness: 1

## Sources this run

- leavers_missing_prices: n=3, symbols=['ABC', 'ANTM', 'BLL']
- reconcile_unavailable: symbol=SPX, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=WSM, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=WST, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=WTW, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=WY, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=WYNN, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=XEL, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=XOM, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=XYL, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=XYZ, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=YUM, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ZBH, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ZBRA, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ZTS, error=blocked: 403 from cdn.cboe.com

## IPO pipeline

- 0 first-time IPO deals of 0 registrants; by status: none
- 0 with an offer price read, 0 with a first trade.
- EDGAR daily index read through not yet; backfill reached not started.

## Live tracking

- stock, 2026-W47: base_rate Brier 0.2596 (n=1944); model Brier 0.2764 (n=1944); random_walk Brier 0.2500 (n=1944)
- ipo: no resolved predictions yet
- stock model stock-2026-10-09-bc9b4b29c3, shrinkage 1
