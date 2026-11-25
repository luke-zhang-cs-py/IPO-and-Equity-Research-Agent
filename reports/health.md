# Bot health

Run `20261125T044946Z-daily-627d15` at 2026-11-25T04:49:46Z, data through the 2026-11-24 session. **Status: failing.**

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
- staleness: 2

Errors (first 20):

- staleness SNDK: newest bar 2026-11-19, 3 trading days behind 2026-11-24

## Sources this run

- prices_failed: symbol=DAL, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DASH, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DD, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DDOG, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DE, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DECK, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DELL, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DG, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DGX, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DHI, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DHR, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DIS, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DLR, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DLTR, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DOC, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DOV, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DOW, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DPZ, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DRI, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DTE, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DUK, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DVA, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DVN, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=DXCM, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=MTD, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=MU, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=NCLH, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=NDAQ, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=NDSN, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=NEE, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]

## IPO pipeline

- 0 first-time IPO deals of 0 registrants; by status: none
- 0 with an offer price read, 0 with a first trade.
- EDGAR daily index read through not yet; backfill reached not started.

## Live tracking

- stock, 2026-W48: base_rate Brier 0.2413 (n=920); model Brier 0.2290 (n=920); random_walk Brier 0.2500 (n=920)
- ipo: no resolved predictions yet
- stock model stock-2026-10-09-bc9b4b29c3, shrinkage 1
