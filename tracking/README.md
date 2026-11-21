# Tracking: the paper bot against the market, 2026-01-02 to 2026-11-20

Updated 2026-11-21 03:18 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +3.56% | +0.97% |
| Worst drawdown | -7.93% | -11.46% |

Over 224 trading days: daily correlation with SPY 0.568 (95% CI 0.452 to 0.674), beta 0.357 (95% CI 0.276 to 0.432), tracking error +12.16% a year, average daily return against SPY's +2.20% a year (95% CI -22.08% to +27.94%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.2% on average (209 days); below it: 73.8% (15 days). By regime: bull: 76.3% (168 d) | ordinary: 75.3% (56 d).

## Execution

108 signals: monitor: price deviation 47 (43.5%), filled 37 (34.3%), blocked: exposure 17 (15.7%), monitor: stoploss guard 6 (5.6%), monitor: cooldown 1 (0.9%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.023%; 23 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
