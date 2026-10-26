# Bot health

Run `20261026T022400Z-edgar-02c659` at 2026-10-26T02:24:00Z, data through the 2026-10-23 session. **Status: degraded.**

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
- staleness: 1

## Sources this run

- edgar_skipped: reason=SEC_USER_AGENT is not set; EDGAR asks every caller for "Name email"

## IPO pipeline

- 0 first-time IPO deals of 0 registrants; by status: none
- 0 with an offer price read, 0 with a first trade.
- EDGAR daily index read through not yet; backfill reached not started.

## Live tracking

- stock, 2026-W43: base_rate Brier 0.2468 (n=2012); model Brier 0.2528 (n=2012); random_walk Brier 0.2500 (n=2012)
- ipo: no resolved predictions yet
- stock model stock-2026-10-09-bc9b4b29c3, shrinkage 1
