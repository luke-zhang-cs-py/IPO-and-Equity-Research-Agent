# Bot health

Run `20261126T031753Z-edgar-2676f8` at 2026-11-26T03:17:53Z, data through the 2026-11-25 session. **Status: failing.**

## Coverage

- Universe: 503 symbols; 503 with prices; 418 current.
- Missing tickers (no prices at all): none
- Stale: DAL, DASH, DD, DDOG, DE, DECK, DELL, DG, DGX, DHI, DHR, DIS, DLR, DLTR, DOC, DOV, DOW, DPZ, DRI, DTE, DUK, DVA, DVN, DXCM, MTD
- Missing trading days inside histories: 1 days over 1 symbols
- Missing fields in the last year of bars: none
- Delisted symbols kept: 1; membership history recorded from 2026-10-09T01:51:19Z (earlier backtests use the membership seen then).

## Checks

- missing_days: 1
- moves: 12
- staleness: 87

Errors (first 20):

- staleness DAL: newest bar 2026-11-23, 2 trading days behind 2026-11-25
- staleness DASH: newest bar 2026-11-23, 2 trading days behind 2026-11-25
- staleness DD: newest bar 2026-11-23, 2 trading days behind 2026-11-25
- staleness DDOG: newest bar 2026-11-23, 2 trading days behind 2026-11-25
- staleness DE: newest bar 2026-11-23, 2 trading days behind 2026-11-25
- staleness DECK: newest bar 2026-11-23, 2 trading days behind 2026-11-25
- staleness DELL: newest bar 2026-11-23, 2 trading days behind 2026-11-25
- staleness DG: newest bar 2026-11-23, 2 trading days behind 2026-11-25
- staleness DGX: newest bar 2026-11-23, 2 trading days behind 2026-11-25
- staleness DHI: newest bar 2026-11-23, 2 trading days behind 2026-11-25
- staleness DHR: newest bar 2026-11-23, 2 trading days behind 2026-11-25
- staleness DIS: newest bar 2026-11-23, 2 trading days behind 2026-11-25
- staleness DLR: newest bar 2026-11-23, 2 trading days behind 2026-11-25
- staleness DLTR: newest bar 2026-11-23, 2 trading days behind 2026-11-25
- staleness DOC: newest bar 2026-11-23, 2 trading days behind 2026-11-25
- staleness DOV: newest bar 2026-11-23, 2 trading days behind 2026-11-25
- staleness DOW: newest bar 2026-11-23, 2 trading days behind 2026-11-25
- staleness DPZ: newest bar 2026-11-23, 2 trading days behind 2026-11-25
- staleness DRI: newest bar 2026-11-23, 2 trading days behind 2026-11-25
- staleness DTE: newest bar 2026-11-23, 2 trading days behind 2026-11-25

## Sources this run

- edgar_skipped: reason=SEC_USER_AGENT is not set; EDGAR asks every caller for "Name email"

## IPO pipeline

- 0 first-time IPO deals of 0 registrants; by status: none
- 0 with an offer price read, 0 with a first trade.
- EDGAR daily index read through not yet; backfill reached not started.

## Live tracking

- stock, 2026-W48: base_rate Brier 0.2413 (n=920); model Brier 0.2290 (n=920); random_walk Brier 0.2500 (n=920)
- ipo: no resolved predictions yet
- stock model stock-2026-10-09-bc9b4b29c3, shrinkage 1
