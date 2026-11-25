# Bot health

Run `20261125T014601Z-edgar-f146c4` at 2026-11-25T01:46:01Z, data through the 2026-11-24 session. **Status: failing.**

## Coverage

- Universe: 503 symbols; 503 with prices; 467 current.
- Missing tickers (no prices at all): none
- Stale: A, AAPL, ABBV, ABNB, ABT, ACGL, ACN, ADBE, ADI, ADM, ADP, ADSK, AEE, AEP, AES, AFL, AIG, AIZ, AJG, AKAM, ALB, ALGN, ALL, ALLE, AMAT
- Missing trading days inside histories: 1 days over 1 symbols
- Missing fields in the last year of bars: none
- Delisted symbols kept: 1; membership history recorded from 2026-10-09T01:51:19Z (earlier backtests use the membership seen then).

## Checks

- missing_days: 1
- moves: 12
- staleness: 38

Errors (first 20):

- staleness A: newest bar 2026-11-20, 2 trading days behind 2026-11-24
- staleness AAPL: newest bar 2026-11-20, 2 trading days behind 2026-11-24
- staleness ABBV: newest bar 2026-11-20, 2 trading days behind 2026-11-24
- staleness ABNB: newest bar 2026-11-20, 2 trading days behind 2026-11-24
- staleness ABT: newest bar 2026-11-20, 2 trading days behind 2026-11-24
- staleness ACGL: newest bar 2026-11-20, 2 trading days behind 2026-11-24
- staleness ACN: newest bar 2026-11-20, 2 trading days behind 2026-11-24
- staleness ADBE: newest bar 2026-11-20, 2 trading days behind 2026-11-24
- staleness ADI: newest bar 2026-11-20, 2 trading days behind 2026-11-24
- staleness ADM: newest bar 2026-11-20, 2 trading days behind 2026-11-24
- staleness ADP: newest bar 2026-11-20, 2 trading days behind 2026-11-24
- staleness ADSK: newest bar 2026-11-20, 2 trading days behind 2026-11-24
- staleness AEE: newest bar 2026-11-20, 2 trading days behind 2026-11-24
- staleness AEP: newest bar 2026-11-20, 2 trading days behind 2026-11-24
- staleness AES: newest bar 2026-11-20, 2 trading days behind 2026-11-24
- staleness AFL: newest bar 2026-11-20, 2 trading days behind 2026-11-24
- staleness AIG: newest bar 2026-11-20, 2 trading days behind 2026-11-24
- staleness AIZ: newest bar 2026-11-20, 2 trading days behind 2026-11-24
- staleness AJG: newest bar 2026-11-20, 2 trading days behind 2026-11-24
- staleness AKAM: newest bar 2026-11-20, 2 trading days behind 2026-11-24

## Sources this run

- edgar_skipped: reason=SEC_USER_AGENT is not set; EDGAR asks every caller for "Name email"

## IPO pipeline

- 0 first-time IPO deals of 0 registrants; by status: none
- 0 with an offer price read, 0 with a first trade.
- EDGAR daily index read through not yet; backfill reached not started.

## Live tracking

- stock, 2026-W48: base_rate Brier 0.2397 (n=467); model Brier 0.2013 (n=467); random_walk Brier 0.2500 (n=467)
- ipo: no resolved predictions yet
- stock model stock-2026-10-09-bc9b4b29c3, shrinkage 1
