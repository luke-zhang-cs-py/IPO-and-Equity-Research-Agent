# Tracking: the paper bot against the market, 2026-01-02 to 2026-11-23

Updated 2026-11-24 06:11 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +4.45% | +5.73% |
| Worst drawdown | -7.93% | -11.46% |

Over 225 trading days: daily correlation with SPY 0.566 (95% CI 0.456 to 0.665), beta 0.339 (95% CI 0.265 to 0.418), tracking error +12.80% a year, average daily return against SPY's -2.15% a year (95% CI -28.48% to +24.76%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.2% on average (209 days); below it: 73.1% (16 days). By regime: bull: 76.3% (168 d) | drawdown: 62.7% (1 d) | ordinary: 75.3% (56 d).

## Execution

108 signals: monitor: price deviation 47 (43.5%), filled 37 (34.3%), blocked: exposure 17 (15.7%), monitor: stoploss guard 6 (5.6%), monitor: cooldown 1 (0.9%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.023%; 23 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
