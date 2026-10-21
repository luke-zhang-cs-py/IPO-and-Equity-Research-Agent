# Tracking: the paper bot against the market, 2026-01-02 to 2026-10-19

Updated 2026-10-21 00:42 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +11.38% | +12.19% |
| Worst drawdown | -3.37% | -9.13% |

Over 200 trading days: daily correlation with SPY 0.467 (95% CI 0.348 to 0.575), beta 0.308 (95% CI 0.219 to 0.390), tracking error +11.74% a year, average daily return against SPY's -1.40% a year (95% CI -26.49% to +24.60%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.0% on average (187 days); below it: 75.0% (13 days). By regime: bull: 76.2% (165 d) | ordinary: 74.4% (35 d).

## Execution

93 signals: monitor: price deviation 39 (41.9%), filled 34 (36.6%), blocked: exposure 13 (14.0%), monitor: stoploss guard 6 (6.5%), monitor: cooldown 1 (1.1%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.024%; 19 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
