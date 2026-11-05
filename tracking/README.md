# Tracking: the paper bot against the market, 2026-01-02 to 2026-11-04

Updated 2026-11-05 02:37 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +8.61% | +12.24% |
| Worst drawdown | -4.00% | -9.13% |

Over 212 trading days: daily correlation with SPY 0.491 (95% CI 0.383 to 0.605), beta 0.328 (95% CI 0.242 to 0.413), tracking error +11.58% a year, average daily return against SPY's -4.40% a year (95% CI -30.76% to +20.68%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.2% on average (199 days); below it: 75.0% (13 days). By regime: bull: 76.3% (168 d) | ordinary: 75.5% (44 d).

## Execution

103 signals: monitor: price deviation 42 (40.8%), filled 37 (35.9%), blocked: exposure 17 (16.5%), monitor: stoploss guard 6 (5.8%), monitor: cooldown 1 (1.0%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.023%; 19 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
