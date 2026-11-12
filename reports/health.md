# Bot health

Run `20261112T024544Z-daily-7b320a` at 2026-11-12T02:45:44Z, data through the 2026-11-11 session. **Status: degraded.**

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
- staleness: 2

## Sources this run

- leavers_missing_prices: n=3, symbols=['ABC', 'ANTM', 'BLL']

## IPO pipeline

- 0 first-time IPO deals of 0 registrants; by status: none
- 0 with an offer price read, 0 with a first trade.
- EDGAR daily index read through not yet; backfill reached not started.

## Live tracking

- stock, 2026-W46: base_rate Brier 0.2440 (n=1509); model Brier 0.2381 (n=1509); random_walk Brier 0.2500 (n=1509)
- ipo: no resolved predictions yet
- stock model stock-2026-10-09-bc9b4b29c3, shrinkage 1
