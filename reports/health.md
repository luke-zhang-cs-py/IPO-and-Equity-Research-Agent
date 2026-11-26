# Bot health

Run `20261126T040200Z-daily-fd4938` at 2026-11-26T04:02:00Z, data through the 2026-11-25 session. **Status: failing.**

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

- staleness SNDK: newest bar 2026-11-19, 4 trading days behind 2026-11-25

## Sources this run

- leavers_missing_prices: n=3, symbols=['ABC', 'ANTM', 'BLL']
- reconcile_unavailable: symbol=DECK, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=DELL, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=DG, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=DGX, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=DHI, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=DHR, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=DIS, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=DLR, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=DLTR, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=DOC, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=DOV, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=DOW, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=DPZ, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=DRI, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=DTE, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=DUK, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=DVA, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=DVN, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=DXCM, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=EBAY, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ECHO, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ECL, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ED, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=EFX, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=EG, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=EIX, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=SPX, error=blocked: 403 from cdn.cboe.com

## IPO pipeline

- 0 first-time IPO deals of 0 registrants; by status: none
- 0 with an offer price read, 0 with a first trade.
- EDGAR daily index read through not yet; backfill reached not started.

## Live tracking

- stock, 2026-W48: base_rate Brier 0.2423 (n=1506); model Brier 0.2334 (n=1506); random_walk Brier 0.2500 (n=1506)
- ipo: no resolved predictions yet
- stock model stock-2026-10-09-bc9b4b29c3, shrinkage 1
