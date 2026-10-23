# Tracking: the paper bot against the market, 2026-01-02 to 2026-10-21

Updated 2026-10-23 00:45 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +11.90% | +13.16% |
| Worst drawdown | -3.37% | -9.13% |

Over 202 trading days: daily correlation with SPY 0.468 (95% CI 0.341 to 0.576), beta 0.308 (95% CI 0.220 to 0.390), tracking error +11.68% a year, average daily return against SPY's -1.88% a year (95% CI -27.50% to +23.61%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.0% on average (189 days); below it: 75.0% (13 days). By regime: bull: 76.3% (167 d) | ordinary: 74.4% (35 d).

## Execution

97 signals: monitor: price deviation 41 (42.3%), filled 35 (36.1%), blocked: exposure 14 (14.4%), monitor: stoploss guard 6 (6.2%), monitor: cooldown 1 (1.0%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.034%; 19 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
