# Tracking: the paper bot against the market, 2026-01-02 to 2026-10-15

Updated 2026-10-17 00:37 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +11.39% | +12.97% |
| Worst drawdown | -3.37% | -9.13% |

Over 198 trading days: daily correlation with SPY 0.472 (95% CI 0.352 to 0.582), beta 0.313 (95% CI 0.230 to 0.395), tracking error +11.69% a year, average daily return against SPY's -2.28% a year (95% CI -27.07% to +24.31%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 75.9% on average (185 days); below it: 75.0% (13 days). By regime: bull: 76.2% (164 d) | ordinary: 74.3% (34 d).

## Execution

90 signals: monitor: price deviation 36 (40.0%), filled 34 (37.8%), blocked: exposure 13 (14.4%), monitor: stoploss guard 6 (6.7%), monitor: cooldown 1 (1.1%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.024%; 19 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
