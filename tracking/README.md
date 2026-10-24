# Tracking: the paper bot against the market, 2026-01-02 to 2026-10-22

Updated 2026-10-24 00:51 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +11.24% | +11.83% |
| Worst drawdown | -3.37% | -9.13% |

Over 203 trading days: daily correlation with SPY 0.473 (95% CI 0.348 to 0.580), beta 0.310 (95% CI 0.224 to 0.389), tracking error +11.67% a year, average daily return against SPY's -1.13% a year (95% CI -26.94% to +23.43%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.0% on average (190 days); below it: 75.0% (13 days). By regime: bull: 76.3% (168 d) | ordinary: 74.4% (35 d).

## Execution

98 signals: monitor: price deviation 41 (41.8%), filled 35 (35.7%), blocked: exposure 15 (15.3%), monitor: stoploss guard 6 (6.1%), monitor: cooldown 1 (1.0%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.034%; 19 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
