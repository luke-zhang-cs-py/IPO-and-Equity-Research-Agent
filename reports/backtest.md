# Backtest

Walk-forward, out of sample, run `20261107T123132Z-weekly-2a0886` at 2026-11-07T12:31:32Z. Stocks: next-session direction (close up) of S&P 500 members; IPOs: a first close 20% or more above the offer. Base rate, random walk and average recent IPO are the baselines; DM is Diebold-Mariano (HLN-corrected), the bootstrap is a moving-block one.

## Stocks: next-day direction

1,148,014 out-of-sample predictions, 2017-01-03 to 2026-11-05.

| forecaster | Brier | log loss | hit rate | ECE | MAE | RMSE |
|---|---|---|---|---|---|---|
| model | 0.2498 | 0.6927 | 51.5% | 0.008 | 0.0141 | 0.0220 |
| base | 0.2499 | 0.6929 | 51.7% | 0.011 | 0.0140 | 0.0219 |
| rw | 0.2500 | 0.6931 | 50.0% | 0.018 | 0.0140 | 0.0219 |

| comparison | mean loss difference | DM p | DM p (Holm) | bootstrap 95% CI | bootstrap p |
|---|---|---|---|---|---|
| model vs base: brier | -0.00009 | 0.588 | 1 | [-0.00038, +0.00025] | 0.591 |
| model vs base: log_loss | -0.00018 | 0.571 | 1 | [-0.00077, +0.00049] | 0.576 |
| model vs base: abs_error | +0.00012 | 1.75e-06 | 1.05e-05 | [+0.00007, +0.00018] | 0.0005 |
| model vs rw: brier | -0.00023 | 0.372 | 1 | [-0.00074, +0.00030] | 0.375 |
| model vs rw: log_loss | -0.00047 | 0.373 | 1 | [-0.00149, +0.00061] | 0.378 |
| model vs rw: abs_error | +0.00012 | 1.75e-06 | 1.05e-05 | [+0.00007, +0.00018] | 0.0005 |

The model does not beat the best baseline (base) on Brier at the 5% level after Holm.
A negative difference means the model's loss is lower.

## IPOs: first-day pop

No resolved out-of-sample predictions yet.

## Leakage test (scrambled future)

- stocks: passed at cutoffs 2021-06-04, 2024-02-21, 2026-04-24 (largest change 0)
- IPOs: passed at cutoffs  (largest change 0)
