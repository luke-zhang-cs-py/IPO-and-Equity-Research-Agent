# Bot health

Run `20261106T011745Z-edgar-e1d6ea` at 2026-11-06T01:17:45Z, data through the 2026-11-05 session. **Status: failing.**

## Coverage

- Universe: 503 symbols; 503 with prices; 0 current.
- Missing tickers (no prices at all): none
- Stale: A, AAPL, ABBV, ABNB, ABT, ACGL, ACN, ADBE, ADI, ADM, ADP, ADSK, AEE, AEP, AES, AFL, AIG, AIZ, AJG, AKAM, ALB, ALGN, ALL, ALLE, AMAT
- Missing trading days inside histories: 1 days over 1 symbols
- Missing fields in the last year of bars: none
- Delisted symbols kept: 1; membership history recorded from 2026-10-09T01:51:19Z (earlier backtests use the membership seen then).

## Checks

- missing_days: 1
- moves: 12
- staleness: 505

Errors (first 20):

- staleness A: newest bar 2026-11-03, 2 trading days behind 2026-11-05
- staleness AAPL: newest bar 2026-11-03, 2 trading days behind 2026-11-05
- staleness ABBV: newest bar 2026-11-03, 2 trading days behind 2026-11-05
- staleness ABNB: newest bar 2026-11-03, 2 trading days behind 2026-11-05
- staleness ABT: newest bar 2026-11-03, 2 trading days behind 2026-11-05
- staleness ACGL: newest bar 2026-11-03, 2 trading days behind 2026-11-05
- staleness ACN: newest bar 2026-11-03, 2 trading days behind 2026-11-05
- staleness ADBE: newest bar 2026-11-03, 2 trading days behind 2026-11-05
- staleness ADI: newest bar 2026-11-03, 2 trading days behind 2026-11-05
- staleness ADM: newest bar 2026-11-03, 2 trading days behind 2026-11-05
- staleness ADP: newest bar 2026-11-03, 2 trading days behind 2026-11-05
- staleness ADSK: newest bar 2026-11-03, 2 trading days behind 2026-11-05
- staleness AEE: newest bar 2026-11-03, 2 trading days behind 2026-11-05
- staleness AEP: newest bar 2026-11-03, 2 trading days behind 2026-11-05
- staleness AES: newest bar 2026-11-03, 2 trading days behind 2026-11-05
- staleness AFL: newest bar 2026-11-03, 2 trading days behind 2026-11-05
- staleness AIG: newest bar 2026-11-03, 2 trading days behind 2026-11-05
- staleness AIZ: newest bar 2026-11-03, 2 trading days behind 2026-11-05
- staleness AJG: newest bar 2026-11-03, 2 trading days behind 2026-11-05
- staleness AKAM: newest bar 2026-11-03, 2 trading days behind 2026-11-05

## Sources this run

- edgar_skipped: reason=SEC_USER_AGENT is not set; EDGAR asks every caller for "Name email"

## IPO pipeline

- 0 first-time IPO deals of 0 registrants; by status: none
- 0 with an offer price read, 0 with a first trade.
- EDGAR daily index read through not yet; backfill reached not started.

## Live tracking

- stock, 2026-W45: base_rate Brier 0.2497 (n=1004); model Brier 0.2472 (n=1004); random_walk Brier 0.2500 (n=1004)
- ipo: no resolved predictions yet
- stock model stock-2026-10-09-bc9b4b29c3, shrinkage 1
