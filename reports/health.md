# Bot health

Run `20261117T054733Z-edgar-0e036e` at 2026-11-17T05:47:33Z, data through the 2026-11-16 session. **Status: degraded.**

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

- edgar_skipped: reason=SEC_USER_AGENT is not set; EDGAR asks every caller for "Name email"

## IPO pipeline

- 0 first-time IPO deals of 0 registrants; by status: none
- 0 with an offer price read, 0 with a first trade.
- EDGAR daily index read through not yet; backfill reached not started.

## Live tracking

- stock, 2026-W47: base_rate Brier 0.2564 (n=503); model Brier 0.2659 (n=503); random_walk Brier 0.2500 (n=503)
- ipo: no resolved predictions yet
- stock model stock-2026-10-09-bc9b4b29c3, shrinkage 1
