# Tracking: the paper bot against the market, 2026-01-02 to 2026-10-30

Updated 2026-10-31 01:42 UTC by `python evaluation/tracker.py`; every run is a line in `track.json`. The bot is the paper replay (a breakout signal on 30 large caps, every guardrail on, fills from daily bars); this measures how its account moves with the market, not whether it has an edge.

| | Account | SPY |
|---|---|---|
| Return | +9.84% | +10.62% |
| Worst drawdown | -3.37% | -9.13% |

Over 209 trading days: daily correlation with SPY 0.490 (95% CI 0.373 to 0.599), beta 0.324 (95% CI 0.239 to 0.409), tracking error +11.55% a year, average daily return against SPY's -1.34% a year (95% CI -26.78% to +24.05%). Intervals resample the days 1,000 times; an interval that spans zero is no evidence either way.

## Trend accordance

Invested on days SPY was above its 200-day average: 76.1% on average (196 days); below it: 75.0% (13 days). By regime: bull: 76.3% (168 d) | ordinary: 75.2% (41 d).

## Execution

102 signals: monitor: price deviation 42 (41.2%), filled 36 (35.3%), blocked: exposure 17 (16.7%), monitor: stoploss guard 6 (5.9%), monitor: cooldown 1 (1.0%). Fill rate of planned shares 100.0%; mean slippage from the signal's price -0.023%; 19 stops hit.

Look-ahead check on the signal: 0 found in 30 sampled days.
