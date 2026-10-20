# Tracking: the paper bot against the market, 2026-01-02 to 2026-10-16

Updated 2026-10-20 01:07 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +11.55% | +11.72% |
| Worst drawdown | -3.37% | -9.13% |

Over 199 trading days: daily correlation with SPY 0.469 (95% CI 0.349 to 0.581), beta 0.309 (95% CI 0.221 to 0.389), tracking error +11.75% a year, average daily return against SPY's -0.67% a year (95% CI -26.50% to +24.38%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 75.9% on average (186 days); below it: 75.0% (13 days). By regime: bull: 76.2% (165 d) | ordinary: 74.3% (34 d).

## Execution

92 signals: monitor: price deviation 38 (41.3%), filled 34 (37.0%), blocked: exposure 13 (14.1%), monitor: stoploss guard 6 (6.5%), monitor: cooldown 1 (1.1%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.024%; 19 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
