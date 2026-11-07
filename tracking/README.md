# Tracking: the paper bot against the market, 2026-01-02 to 2026-11-06

Updated 2026-11-07 02:04 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +6.04% | +7.63% |
| Worst drawdown | -5.74% | -9.13% |

Over 214 trading days: daily correlation with SPY 0.542 (95% CI 0.397 to 0.661), beta 0.354 (95% CI 0.259 to 0.432), tracking error +11.75% a year, average daily return against SPY's -2.31% a year (95% CI -29.72% to +23.10%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.2% on average (201 days); below it: 75.0% (13 days). By regime: bull: 76.3% (168 d) | ordinary: 75.6% (46 d).

## Execution

104 signals: monitor: price deviation 43 (41.3%), filled 37 (35.6%), blocked: exposure 17 (16.3%), monitor: stoploss guard 6 (5.8%), monitor: cooldown 1 (1.0%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.023%; 20 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
