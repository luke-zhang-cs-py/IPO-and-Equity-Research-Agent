# Tracking: the paper bot against the market, 2026-01-02 to 2026-10-20

Updated 2026-10-22 00:46 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +11.69% | +12.57% |
| Worst drawdown | -3.37% | -9.13% |

Over 201 trading days: daily correlation with SPY 0.468 (95% CI 0.345 to 0.576), beta 0.308 (95% CI 0.219 to 0.391), tracking error +11.71% a year, average daily return against SPY's -1.47% a year (95% CI -27.93% to +23.72%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.0% on average (188 days); below it: 75.0% (13 days). By regime: bull: 76.2% (166 d) | ordinary: 74.4% (35 d).

## Execution

94 signals: monitor: price deviation 40 (42.6%), filled 34 (36.2%), blocked: exposure 13 (13.8%), monitor: stoploss guard 6 (6.4%), monitor: cooldown 1 (1.1%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.024%; 19 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
