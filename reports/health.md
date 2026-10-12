# Bot health

Run `20261012T221935Z-edgar-b190a2` at 2026-10-12T22:19:35Z, data through the 2026-10-12 session. **Status: failing.**

## Coverage

- Universe: 503 symbols; 503 with prices; 470 current.
- Missing tickers (no prices at all): none
- Stale: VRSK, VRSN, VRT, VRTX, VST, VTR, VTRS, VYLR, VZ, WAB, WAT, WDAY, WDC, WEC, WELL, WFC, WM, WMB, WMT, WRB, WSM, WST, WTW, WY, WYNN
- Missing trading days inside histories: 1 days over 1 symbols
- Missing fields in the last year of bars: volume 1
- Delisted symbols kept: 0; membership history recorded from 2026-10-09T01:51:19Z (earlier backtests use the membership seen then).

## Checks

- missing_days: 1
- moves: 12
- staleness: 34

Errors (first 20):

- staleness VRSK: newest bar 2026-10-08, 2 trading days behind 2026-10-12
- staleness VRSN: newest bar 2026-10-08, 2 trading days behind 2026-10-12
- staleness VRT: newest bar 2026-10-08, 2 trading days behind 2026-10-12
- staleness VRTX: newest bar 2026-10-08, 2 trading days behind 2026-10-12
- staleness VST: newest bar 2026-10-08, 2 trading days behind 2026-10-12
- staleness VTR: newest bar 2026-10-08, 2 trading days behind 2026-10-12
- staleness VTRS: newest bar 2026-10-08, 2 trading days behind 2026-10-12
- staleness VYLR: newest bar 2026-10-08, 2 trading days behind 2026-10-12
- staleness VZ: newest bar 2026-10-08, 2 trading days behind 2026-10-12
- staleness WAB: newest bar 2026-10-08, 2 trading days behind 2026-10-12
- staleness WAT: newest bar 2026-10-08, 2 trading days behind 2026-10-12
- staleness WDAY: newest bar 2026-10-08, 2 trading days behind 2026-10-12
- staleness WDC: newest bar 2026-10-08, 2 trading days behind 2026-10-12
- staleness WEC: newest bar 2026-10-08, 2 trading days behind 2026-10-12
- staleness WELL: newest bar 2026-10-08, 2 trading days behind 2026-10-12
- staleness WFC: newest bar 2026-10-08, 2 trading days behind 2026-10-12
- staleness WM: newest bar 2026-10-08, 2 trading days behind 2026-10-12
- staleness WMB: newest bar 2026-10-08, 2 trading days behind 2026-10-12
- staleness WMT: newest bar 2026-10-08, 2 trading days behind 2026-10-12
- staleness WRB: newest bar 2026-10-08, 2 trading days behind 2026-10-12

## Sources this run

- edgar_skipped: reason=SEC_USER_AGENT is not set; EDGAR asks every caller for "Name email"

## IPO pipeline

- 0 first-time IPO deals of 0 registrants; by status: none
- 0 with an offer price read, 0 with a first trade.
- EDGAR daily index read through not yet; backfill reached not started.

## Live tracking

- stock, 2026-W41: base_rate Brier 0.2438 (n=470); model Brier 0.2459 (n=470); random_walk Brier 0.2500 (n=470)
- ipo: no resolved predictions yet
- stock model stock-2026-10-09-bc9b4b29c3, shrinkage 1
- **stock: calibration drift: expected calibration error 0.119 over the last 1 periods (limit 0.10)**
