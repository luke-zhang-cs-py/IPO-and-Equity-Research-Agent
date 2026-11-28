# Backtest

Walk-forward, out of sample, run `20261128T150717Z-weekly-e3d228` at 2026-11-28T15:07:17Z. Stocks: next-session direction (close up) of S&P 500 members; IPOs: a first close 20% or more above the offer. Base rate, random walk and average recent IPO are the baselines; DM is Diebold-Mariano (HLN-corrected), the bootstrap is a moving-block one.

## Stocks: next-day direction

1,155,121 out-of-sample predictions, 2017-01-03 to 2026-11-25.

| forecaster | Brier | log loss | hit rate | ECE | MAE | RMSE |
|---|---|---|---|---|---|---|
| model | 0.2498 | 0.6927 | 51.5% | 0.008 | 0.0142 | 0.0220 |
| base | 0.2499 | 0.6929 | 51.7% | 0.011 | 0.0140 | 0.0219 |
| rw | 0.2500 | 0.6931 | 50.0% | 0.018 | 0.0140 | 0.0219 |

| comparison | mean loss difference | DM p | DM p (Holm) | bootstrap 95% CI | bootstrap p |
|---|---|---|---|---|---|
| model vs base: brier | -0.00010 | 0.538 | 1 | [-0.00040, +0.00024] | 0.538 |
| model vs base: log_loss | -0.00020 | 0.521 | 1 | [-0.00081, +0.00048] | 0.517 |
| model vs base: abs_error | +0.00012 | 1.91e-06 | 1.14e-05 | [+0.00007, +0.00018] | 0.0005 |
| model vs rw: brier | -0.00025 | 0.346 | 1 | [-0.00072, +0.00028] | 0.345 |
| model vs rw: log_loss | -0.00049 | 0.347 | 1 | [-0.00145, +0.00057] | 0.344 |
| model vs rw: abs_error | +0.00012 | 1.91e-06 | 1.14e-05 | [+0.00007, +0.00018] | 0.0005 |

The model does not beat the best baseline (base) on Brier at the 5% level after Holm.
A negative difference means the model's loss is lower.

## IPOs: first-day pop

No resolved out-of-sample predictions yet.

## Leakage test (scrambled future)

- stocks: passed at cutoffs 2021-06-15, 2024-03-07, 2026-05-13 (largest change 0)
- IPOs: passed at cutoffs  (largest change 0)
