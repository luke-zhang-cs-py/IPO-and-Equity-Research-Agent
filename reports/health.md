# Bot health

Run `20261121T030216Z-daily-629646` at 2026-11-21T03:02:16Z, data through the 2026-11-20 session. **Status: degraded.**

## Coverage

- Universe: 503 symbols; 503 with prices; 503 current.
- Missing tickers (no prices at all): none
- Stale: none
- Missing trading days inside histories: 1 days over 1 symbols
- Missing fields in the last year of bars: none
- Delisted symbols kept: 1; membership history recorded from 2026-10-09T01:51:19Z (earlier backtests use the membership seen then).

## Checks

- missing_days: 1
- moves: 12
- staleness: 1

## Sources this run

- leavers_missing_prices: n=3, symbols=['ABC', 'ANTM', 'BLL']
- reconcile_unavailable: symbol=A, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=AAPL, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ABBV, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ABNB, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ABT, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ACGL, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ACN, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ADBE, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ADI, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ADM, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ADP, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ADSK, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=AEE, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=AEP, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=AES, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=AFL, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=AIG, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=AIZ, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=AJG, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=AKAM, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ALB, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ALGN, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ALL, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=ALLE, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=AMAT, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=AMCR, error=blocked: 403 from cdn.cboe.com
- reconcile_unavailable: symbol=SPX, error=blocked: 403 from cdn.cboe.com

## IPO pipeline

- 0 first-time IPO deals of 0 registrants; by status: none
- 0 with an offer price read, 0 with a first trade.
- EDGAR daily index read through not yet; backfill reached not started.

## Live tracking

- stock, 2026-W47: base_rate Brier 0.2590 (n=2514); model Brier 0.2762 (n=2514); random_walk Brier 0.2500 (n=2514)
- ipo: no resolved predictions yet
- stock model stock-2026-10-09-bc9b4b29c3, shrinkage 1
- **stock: calibration drift: expected calibration error 0.104 over the last 3 periods (limit 0.10)**
