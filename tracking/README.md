# Tracking: the paper bot against the market, 2026-01-02 to 2026-10-29

Updated 2026-10-30 02:02 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +11.58% | +12.62% |
| Worst drawdown | -3.37% | -9.13% |

Over 208 trading days: daily correlation with SPY 0.474 (95% CI 0.350 to 0.581), beta 0.310 (95% CI 0.225 to 0.387), tracking error +11.58% a year, average daily return against SPY's -1.60% a year (95% CI -27.52% to +24.00%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.1% on average (195 days); below it: 75.0% (13 days). By regime: bull: 76.3% (168 d) | ordinary: 75.1% (40 d).

## Execution

100 signals: monitor: price deviation 42 (42.0%), filled 35 (35.0%), blocked: exposure 16 (16.0%), monitor: stoploss guard 6 (6.0%), monitor: cooldown 1 (1.0%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.034%; 19 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
