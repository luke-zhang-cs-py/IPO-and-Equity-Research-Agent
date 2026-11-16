# Bot health

Run `20261116T233602Z-edgar-e8dd10` at 2026-11-16T23:36:02Z, data through the 2026-11-16 session. **Status: failing.**

## Coverage

- Universe: 503 symbols; 503 with prices; 433 current.
- Missing tickers (no prices at all): none
- Stale: ABBV, ABNB, ALLE, AMCR, ANET, APP, ARES, BE, CARR, CDW, CEG, CFG, COIN, CRWD, CVNA, DASH, DDOG, DELL, DOW, EXE, FANG, FDXF, FOX, FOXA, FTV
- Missing trading days inside histories: 1 days over 1 symbols
- Missing fields in the last year of bars: none
- Delisted symbols kept: 1; membership history recorded from 2026-10-09T01:51:19Z (earlier backtests use the membership seen then).

## Checks

- missing_days: 1
- moves: 12
- staleness: 71

Errors (first 20):

- staleness ABBV: newest bar 2026-11-12, 2 trading days behind 2026-11-16
- staleness ABNB: newest bar 2026-11-12, 2 trading days behind 2026-11-16
- staleness ALLE: newest bar 2026-11-12, 2 trading days behind 2026-11-16
- staleness AMCR: newest bar 2026-11-12, 2 trading days behind 2026-11-16
- staleness ANET: newest bar 2026-11-12, 2 trading days behind 2026-11-16
- staleness APP: newest bar 2026-11-12, 2 trading days behind 2026-11-16
- staleness ARES: newest bar 2026-11-12, 2 trading days behind 2026-11-16
- staleness BE: newest bar 2026-11-12, 2 trading days behind 2026-11-16
- staleness CARR: newest bar 2026-11-12, 2 trading days behind 2026-11-16
- staleness CDW: newest bar 2026-11-12, 2 trading days behind 2026-11-16
- staleness CEG: newest bar 2026-11-12, 2 trading days behind 2026-11-16
- staleness CFG: newest bar 2026-11-12, 2 trading days behind 2026-11-16
- staleness COIN: newest bar 2026-11-12, 2 trading days behind 2026-11-16
- staleness CRWD: newest bar 2026-11-12, 2 trading days behind 2026-11-16
- staleness CVNA: newest bar 2026-11-12, 2 trading days behind 2026-11-16
- staleness DASH: newest bar 2026-11-12, 2 trading days behind 2026-11-16
- staleness DDOG: newest bar 2026-11-12, 2 trading days behind 2026-11-16
- staleness DELL: newest bar 2026-11-12, 2 trading days behind 2026-11-16
- staleness DOW: newest bar 2026-11-12, 2 trading days behind 2026-11-16
- staleness EXE: newest bar 2026-11-12, 2 trading days behind 2026-11-16

## Sources this run

- edgar_skipped: reason=SEC_USER_AGENT is not set; EDGAR asks every caller for "Name email"

## IPO pipeline

- 0 first-time IPO deals of 0 registrants; by status: none
- 0 with an offer price read, 0 with a first trade.
- EDGAR daily index read through not yet; backfill reached not started.

## Live tracking

- stock, 2026-W46: base_rate Brier 0.2468 (n=2445); model Brier 0.2439 (n=2445); random_walk Brier 0.2500 (n=2445)
- ipo: no resolved predictions yet
- stock model stock-2026-10-09-bc9b4b29c3, shrinkage 1
