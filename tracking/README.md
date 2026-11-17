# Tracking: the paper bot against the market, 2026-01-02 to 2026-11-16

Updated 2026-11-17 04:39 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +6.98% | +8.31% |
| Worst drawdown | -5.74% | -9.13% |

Over 220 trading days: daily correlation with SPY 0.564 (95% CI 0.430 to 0.681), beta 0.365 (95% CI 0.280 to 0.438), tracking error +11.73% a year, average daily return against SPY's -2.00% a year (95% CI -26.05% to +22.05%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.2% on average (207 days); below it: 75.0% (13 days). By regime: bull: 76.3% (168 d) | ordinary: 75.7% (52 d).

## Execution

107 signals: monitor: price deviation 46 (43.0%), filled 37 (34.6%), blocked: exposure 17 (15.9%), monitor: stoploss guard 6 (5.6%), monitor: cooldown 1 (0.9%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.023%; 20 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
