# Tracking: the paper bot against the market, 2026-01-02 to 2026-11-17

Updated 2026-11-18 03:45 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +6.39% | +7.21% |
| Worst drawdown | -5.74% | -9.13% |

Over 221 trading days: daily correlation with SPY 0.566 (95% CI 0.436 to 0.680), beta 0.367 (95% CI 0.284 to 0.441), tracking error +11.72% a year, average daily return against SPY's -1.46% a year (95% CI -25.00% to +23.08%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.2% on average (208 days); below it: 75.0% (13 days). By regime: bull: 76.3% (168 d) | ordinary: 75.7% (53 d).

## Execution

108 signals: monitor: price deviation 47 (43.5%), filled 37 (34.3%), blocked: exposure 17 (15.7%), monitor: stoploss guard 6 (5.6%), monitor: cooldown 1 (0.9%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.023%; 20 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
