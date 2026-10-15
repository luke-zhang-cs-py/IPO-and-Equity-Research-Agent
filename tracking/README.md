# Tracking: the paper bot against the market, 2026-01-02 to 2026-10-14

Updated 2026-10-15 00:38 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +12.21% | +12.65% |
| Worst drawdown | -3.37% | -9.13% |

Over 197 trading days: daily correlation with SPY 0.477 (95% CI 0.351 to 0.587), beta 0.314 (95% CI 0.227 to 0.396), tracking error +11.67% a year, average daily return against SPY's -0.98% a year (95% CI -26.76% to +24.16%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 75.9% on average (184 days); below it: 75.0% (13 days). By regime: bull: 76.2% (163 d) | ordinary: 74.3% (34 d).

## Execution

88 signals: filled 34 (38.6%), monitor: price deviation 34 (38.6%), blocked: exposure 13 (14.8%), monitor: stoploss guard 6 (6.8%), monitor: cooldown 1 (1.1%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.024%; 19 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
