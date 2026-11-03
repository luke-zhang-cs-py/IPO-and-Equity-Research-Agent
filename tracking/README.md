# Tracking: the paper bot against the market, 2026-01-02 to 2026-11-02

Updated 2026-11-03 03:32 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +8.35% | +10.09% |
| Worst drawdown | -3.68% | -9.13% |

Over 210 trading days: daily correlation with SPY 0.489 (95% CI 0.376 to 0.601), beta 0.329 (95% CI 0.240 to 0.417), tracking error +11.56% a year, average daily return against SPY's -2.39% a year (95% CI -28.66% to +23.45%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.2% on average (197 days); below it: 75.0% (13 days). By regime: bull: 76.3% (168 d) | ordinary: 75.3% (42 d).

## Execution

102 signals: monitor: price deviation 42 (41.2%), filled 36 (35.3%), blocked: exposure 17 (16.7%), monitor: stoploss guard 6 (5.9%), monitor: cooldown 1 (1.0%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.023%; 19 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
