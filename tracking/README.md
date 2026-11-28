# Tracking: the paper bot against the market, 2026-01-02 to 2026-11-27

Updated 2026-11-28 04:02 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +5.66% | +6.61% |
| Worst drawdown | -7.93% | -11.46% |

Over 228 trading days: daily correlation with SPY 0.568 (95% CI 0.453 to 0.670), beta 0.339 (95% CI 0.267 to 0.419), tracking error +12.79% a year, average daily return against SPY's -1.77% a year (95% CI -28.54% to +25.67%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.2% on average (209 days); below it: 71.5% (19 days). By regime: bull: 76.3% (168 d) | drawdown: 62.7% (1 d) | ordinary: 74.7% (59 d).

## Execution

109 signals: monitor: price deviation 48 (44.0%), filled 37 (33.9%), blocked: exposure 17 (15.6%), monitor: stoploss guard 6 (5.5%), monitor: cooldown 1 (0.9%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.023%; 23 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
