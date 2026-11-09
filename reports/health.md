# Bot health

Run `20261109T233902Z-edgar-29ab43` at 2026-11-09T23:39:02Z, data through the 2026-11-09 session. **Status: failing.**

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

- staleness ABBV: newest bar 2026-11-05, 2 trading days behind 2026-11-09
- staleness ABNB: newest bar 2026-11-05, 2 trading days behind 2026-11-09
- staleness ALLE: newest bar 2026-11-05, 2 trading days behind 2026-11-09
- staleness AMCR: newest bar 2026-11-05, 2 trading days behind 2026-11-09
- staleness ANET: newest bar 2026-11-05, 2 trading days behind 2026-11-09
- staleness APP: newest bar 2026-11-05, 2 trading days behind 2026-11-09
- staleness ARES: newest bar 2026-11-05, 2 trading days behind 2026-11-09
- staleness BE: newest bar 2026-11-05, 2 trading days behind 2026-11-09
- staleness CARR: newest bar 2026-11-05, 2 trading days behind 2026-11-09
- staleness CDW: newest bar 2026-11-05, 2 trading days behind 2026-11-09
- staleness CEG: newest bar 2026-11-05, 2 trading days behind 2026-11-09
- staleness CFG: newest bar 2026-11-05, 2 trading days behind 2026-11-09
- staleness COIN: newest bar 2026-11-05, 2 trading days behind 2026-11-09
- staleness CRWD: newest bar 2026-11-05, 2 trading days behind 2026-11-09
- staleness CVNA: newest bar 2026-11-05, 2 trading days behind 2026-11-09
- staleness DASH: newest bar 2026-11-05, 2 trading days behind 2026-11-09
- staleness DDOG: newest bar 2026-11-05, 2 trading days behind 2026-11-09
- staleness DELL: newest bar 2026-11-05, 2 trading days behind 2026-11-09
- staleness DOW: newest bar 2026-11-05, 2 trading days behind 2026-11-09
- staleness EXE: newest bar 2026-11-05, 2 trading days behind 2026-11-09

## Sources this run

- edgar_skipped: reason=SEC_USER_AGENT is not set; EDGAR asks every caller for "Name email"

## IPO pipeline

- 0 first-time IPO deals of 0 registrants; by status: none
- 0 with an offer price read, 0 with a first trade.
- EDGAR daily index read through not yet; backfill reached not started.

## Live tracking

- stock, 2026-W45: base_rate Brier 0.2525 (n=2441); model Brier 0.2512 (n=2441); random_walk Brier 0.2500 (n=2441)
- ipo: no resolved predictions yet
- stock model stock-2026-10-09-bc9b4b29c3, shrinkage 1
