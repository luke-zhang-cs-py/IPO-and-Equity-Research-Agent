# Bot health

Run `20261128T034716Z-daily-ff2227` at 2026-11-28T03:47:16Z, data through the 2026-11-27 session. **Status: failing.**

## Coverage

- Universe: 503 symbols; 503 with prices; 502 current.
- Missing tickers (no prices at all): none
- Stale: SNDK
- Missing trading days inside histories: 1 days over 1 symbols
- Missing fields in the last year of bars: none
- Delisted symbols kept: 1; membership history recorded from 2026-10-09T01:51:19Z (earlier backtests use the membership seen then).

## Checks

- missing_days: 1
- moves: 12
- staleness: 2

Errors (first 20):

- staleness SNDK: newest bar 2026-11-19, 5 trading days behind 2026-11-27

## Sources this run

- leavers_missing_prices: n=3, symbols=['ABC', 'ANTM', 'BLL']
- reconcile_unavailable: symbol=FE, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=FERG, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=FFIV, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=FICO, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=FIS, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=FISV, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=FITB, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=FIX, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=FLEX, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=FOX, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=FOXA, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=FRT, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=FSLR, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=FTNT, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=FTV, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=GD, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=GDDY, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=GE, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=GEHC, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=GEN, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=GEV, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=GILD, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=GIS, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=GL, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=GLW, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=GM, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=SPX, error=blocked: 403 from cdn.cboe.com

## IPO pipeline

- 0 first-time IPO deals of 0 registrants; by status: none
- 0 with an offer price read, 0 with a first trade.
- EDGAR daily index read through not yet; backfill reached not started.

## Live tracking

- stock, 2026-W48: base_rate Brier 0.2421 (n=2008); model Brier 0.2329 (n=2008); random_walk Brier 0.2500 (n=2008)
- ipo: no resolved predictions yet
- stock model stock-2026-10-09-bc9b4b29c3, shrinkage 1
