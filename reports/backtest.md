# Backtest

Walk-forward, out of sample, run `20261017T101320Z-weekly-9e550f` at 2026-10-17T10:13:20Z. Stocks: next-session direction (close up) of S&P 500 members; IPOs: a first close 20% or more above the offer. Base rate, random walk and average recent IPO are the baselines; DM is Diebold-Mariano (HLN-corrected), the bootstrap is a moving-block one.

## Stocks: next-day direction

1,139,758 out-of-sample predictions, 2017-01-03 to 2026-10-14.

| forecaster | Brier | log loss | hit rate | ECE | MAE | RMSE |
|---|---|---|---|---|---|---|
| model | 0.2498 | 0.6927 | 51.5% | 0.008 | 0.0141 | 0.0219 |
| base | 0.2499 | 0.6929 | 51.7% | 0.011 | 0.0140 | 0.0218 |
| rw | 0.2500 | 0.6931 | 50.0% | 0.018 | 0.0140 | 0.0218 |

| comparison | mean loss difference | DM p | DM p (Holm) | bootstrap 95% CI | bootstrap p |
|---|---|---|---|---|---|
| model vs base: brier | -0.00008 | 0.607 | 1 | [-0.00039, +0.00022] | 0.605 |
| model vs base: log_loss | -0.00017 | 0.589 | 1 | [-0.00079, +0.00043] | 0.581 |
| model vs base: abs_error | +0.00012 | 1.72e-06 | 1.03e-05 | [+0.00007, +0.00018] | 0.0005 |
| model vs rw: brier | -0.00023 | 0.381 | 1 | [-0.00072, +0.00027] | 0.368 |
| model vs rw: log_loss | -0.00046 | 0.382 | 1 | [-0.00145, +0.00055] | 0.37 |
| model vs rw: abs_error | +0.00012 | 1.72e-06 | 1.03e-05 | [+0.00007, +0.00018] | 0.0005 |

The model does not beat the best baseline (base) on Brier at the 5% level after Holm.
A negative difference means the model's loss is lower.

## IPOs: first-day pop

No resolved out-of-sample predictions yet.

## Leakage test (scrambled future)

- stocks: passed at cutoffs 2021-05-24, 2024-02-05, 2026-04-06 (largest change 0)
- IPOs: passed at cutoffs  (largest change 0)
