# Bot health

Run `20261013T025524Z-daily-388683` at 2026-10-13T02:55:24Z, data through the 2026-10-12 session. **Status: degraded.**

## Coverage

- Universe: 503 symbols; 503 with prices; 503 current.
- Missing tickers (no prices at all): none
- Stale: none
- Missing trading days inside histories: 1 days over 1 symbols
- Missing fields in the last year of bars: none
- Delisted symbols kept: 0; membership history recorded from 2026-10-09T01:51:19Z (earlier backtests use the membership seen then).

## Checks

- missing_days: 1
- moves: 12
- staleness: 2

## Sources this run

- leavers_missing_prices: n=3, symbols=['ABC', 'ANTM', 'BLL']

## IPO pipeline

- 0 first-time IPO deals of 0 registrants; by status: none
- 0 with an offer price read, 0 with a first trade.
- EDGAR daily index read through not yet; backfill reached not started.

## Live tracking

- stock, 2026-W42: base_rate Brier 0.2441 (n=502); model Brier 0.2484 (n=502); random_walk Brier 0.2500 (n=502)
- ipo: no resolved predictions yet
- stock model stock-2026-10-09-bc9b4b29c3, shrinkage 1
- **stock: calibration drift: expected calibration error 0.130 over the last 2 periods (limit 0.10)**
