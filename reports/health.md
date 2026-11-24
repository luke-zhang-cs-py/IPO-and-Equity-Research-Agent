# Bot health

Run `20261124T054742Z-daily-5f8f61` at 2026-11-24T05:47:42Z, data through the 2026-11-23 session. **Status: failing.**

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

- staleness SNDK: newest bar 2026-11-19, 2 trading days behind 2026-11-23

## Sources this run

- prices_failed: symbol=A, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=AAPL, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=ABBV, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=ABNB, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=ABT, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=ACGL, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=ACN, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=ADBE, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=ADI, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=ADM, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=ADP, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=ADSK, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=AEE, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=AEP, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=AES, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=AFL, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=AIG, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=AIZ, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=AJG, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=AKAM, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=ALB, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=ALGN, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=ALL, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=ALLE, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=AMAT, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=AMCR, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=AMD, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=AME, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=AMGN, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]
- prices_failed: symbol=AMP, errors=[('yahoo', 'rate_limited: 429 from query1.finance.yahoo.com'), ('cboe', 'blocked: 403 from cdn.cboe.com')]

## IPO pipeline

- 0 first-time IPO deals of 0 registrants; by status: none
- 0 with an offer price read, 0 with a first trade.
- EDGAR daily index read through not yet; backfill reached not started.

## Live tracking

- stock, 2026-W48: base_rate Brier 0.2397 (n=467); model Brier 0.2013 (n=467); random_walk Brier 0.2500 (n=467)
- ipo: no resolved predictions yet
- stock model stock-2026-10-09-bc9b4b29c3, shrinkage 1
