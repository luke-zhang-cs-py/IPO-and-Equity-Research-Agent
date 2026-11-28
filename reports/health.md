# Bot health

Run `20261128T030023Z-edgar-37a4d2` at 2026-11-28T03:00:23Z, data through the 2026-11-27 session. **Status: failing.**

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
- staleness: 3

Errors (first 20):

- staleness SNDK: newest bar 2026-11-19, 5 trading days behind 2026-11-27

## Sources this run

- edgar_skipped: reason=SEC_USER_AGENT is not set; EDGAR asks every caller for "Name email"

## IPO pipeline

- 0 first-time IPO deals of 0 registrants; by status: none
- 0 with an offer price read, 0 with a first trade.
- EDGAR daily index read through not yet; backfill reached not started.

## Live tracking

- stock, 2026-W48: base_rate Brier 0.2423 (n=1506); model Brier 0.2334 (n=1506); random_walk Brier 0.2500 (n=1506)
- ipo: no resolved predictions yet
- stock model stock-2026-10-09-bc9b4b29c3, shrinkage 1
