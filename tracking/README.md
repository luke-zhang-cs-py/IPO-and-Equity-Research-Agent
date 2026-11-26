# Tracking: the paper bot against the market, 2026-01-02 to 2026-11-25

Updated 2026-11-26 04:14 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +4.84% | +4.91% |
| Worst drawdown | -7.93% | -11.46% |

Over 227 trading days: daily correlation with SPY 0.564 (95% CI 0.444 to 0.667), beta 0.337 (95% CI 0.262 to 0.419), tracking error +12.78% a year, average daily return against SPY's -0.84% a year (95% CI -26.38% to +26.21%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.2% on average (209 days); below it: 72.0% (18 days). By regime: bull: 76.3% (168 d) | drawdown: 62.7% (1 d) | ordinary: 74.9% (58 d).

## Execution

108 signals: monitor: price deviation 47 (43.5%), filled 37 (34.3%), blocked: exposure 17 (15.7%), monitor: stoploss guard 6 (5.6%), monitor: cooldown 1 (0.9%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.023%; 23 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
