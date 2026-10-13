# Tracking: the paper bot against the market, 2026-01-02 to 2026-10-12

Updated 2026-10-13 03:05 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +12.11% | +13.90% |
| Worst drawdown | -3.37% | -9.13% |

Over 195 trading days: daily correlation with SPY 0.482 (95% CI 0.358 to 0.595), beta 0.319 (95% CI 0.233 to 0.408), tracking error +11.62% a year, average daily return against SPY's -2.53% a year (95% CI -30.40% to +25.19%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 75.9% on average (182 days); below it: 75.0% (13 days). By regime: bull: 76.1% (161 d) | ordinary: 74.3% (34 d).

## Execution

86 signals: filled 33 (38.4%), monitor: price deviation 33 (38.4%), blocked: exposure 13 (15.1%), monitor: stoploss guard 6 (7.0%), monitor: cooldown 1 (1.2%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.023%; 18 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
