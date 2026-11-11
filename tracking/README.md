# Tracking: the paper bot against the market, 2026-01-02 to 2026-11-10

Updated 2026-11-11 02:00 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +7.10% | +9.77% |
| Worst drawdown | -5.74% | -9.13% |

Over 216 trading days: daily correlation with SPY 0.553 (95% CI 0.421 to 0.664), beta 0.358 (95% CI 0.269 to 0.434), tracking error +11.77% a year, average daily return against SPY's -3.46% a year (95% CI -29.12% to +21.78%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.2% on average (203 days); below it: 75.0% (13 days). By regime: bull: 76.3% (168 d) | ordinary: 75.6% (48 d).

## Execution

105 signals: monitor: price deviation 44 (41.9%), filled 37 (35.2%), blocked: exposure 17 (16.2%), monitor: stoploss guard 6 (5.7%), monitor: cooldown 1 (1.0%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.023%; 20 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
