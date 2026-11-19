# Tracking: the paper bot against the market, 2026-01-02 to 2026-11-18

Updated 2026-11-19 03:42 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +5.22% | +6.88% |
| Worst drawdown | -6.45% | -9.13% |

Over 222 trading days: daily correlation with SPY 0.565 (95% CI 0.435 to 0.676), beta 0.369 (95% CI 0.286 to 0.440), tracking error +11.72% a year, average daily return against SPY's -2.36% a year (95% CI -26.74% to +22.89%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.2% on average (209 days); below it: 75.0% (13 days). By regime: bull: 76.3% (168 d) | ordinary: 75.6% (54 d).

## Execution

108 signals: monitor: price deviation 47 (43.5%), filled 37 (34.3%), blocked: exposure 17 (15.7%), monitor: stoploss guard 6 (5.6%), monitor: cooldown 1 (0.9%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.023%; 21 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
