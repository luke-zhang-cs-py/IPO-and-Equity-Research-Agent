# Tracking: the paper bot against the market, 2026-01-02 to 2026-10-28

Updated 2026-10-29 01:53 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +12.06% | +13.05% |
| Worst drawdown | -3.37% | -9.13% |

Over 207 trading days: daily correlation with SPY 0.472 (95% CI 0.359 to 0.582), beta 0.309 (95% CI 0.224 to 0.389), tracking error +11.60% a year, average daily return against SPY's -1.55% a year (95% CI -27.03% to +24.10%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.1% on average (194 days); below it: 75.0% (13 days). By regime: bull: 76.3% (168 d) | ordinary: 75.0% (39 d).

## Execution

100 signals: monitor: price deviation 42 (42.0%), filled 35 (35.0%), blocked: exposure 16 (16.0%), monitor: stoploss guard 6 (6.0%), monitor: cooldown 1 (1.0%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.034%; 19 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
