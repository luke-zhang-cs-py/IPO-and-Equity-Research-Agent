# Tracking: the paper bot against the market, 2026-01-02 to 2026-11-24

Updated 2026-11-25 04:57 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +4.84% | +5.21% |
| Worst drawdown | -7.93% | -11.46% |

Over 226 trading days: daily correlation with SPY 0.564 (95% CI 0.446 to 0.668), beta 0.338 (95% CI 0.262 to 0.417), tracking error +12.81% a year, average daily return against SPY's -1.17% a year (95% CI -26.96% to +26.99%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.2% on average (209 days); below it: 72.5% (17 days). By regime: bull: 76.3% (168 d) | drawdown: 62.7% (1 d) | ordinary: 75.1% (57 d).

## Execution

108 signals: monitor: price deviation 47 (43.5%), filled 37 (34.3%), blocked: exposure 17 (15.7%), monitor: stoploss guard 6 (5.6%), monitor: cooldown 1 (0.9%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.023%; 23 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
