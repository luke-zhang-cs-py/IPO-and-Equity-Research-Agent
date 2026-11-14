# Tracking: the paper bot against the market, 2026-01-02 to 2026-11-13

Updated 2026-11-14 02:31 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +8.35% | +10.42% |
| Worst drawdown | -5.74% | -9.13% |

Over 219 trading days: daily correlation with SPY 0.554 (95% CI 0.422 to 0.664), beta 0.359 (95% CI 0.267 to 0.435), tracking error +11.74% a year, average daily return against SPY's -2.76% a year (95% CI -27.34% to +22.26%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.2% on average (206 days); below it: 75.0% (13 days). By regime: bull: 76.3% (168 d) | ordinary: 75.7% (51 d).

## Execution

106 signals: monitor: price deviation 45 (42.5%), filled 37 (34.9%), blocked: exposure 17 (16.0%), monitor: stoploss guard 6 (5.7%), monitor: cooldown 1 (0.9%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.023%; 20 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
