# Backtest

Walk-forward, out of sample, run `20261114T130143Z-weekly-4eb3aa` at 2026-11-14T13:01:43Z. Stocks: next-session direction (close up) of S&P 500 members; IPOs: a first close 20% or more above the offer. Base rate, random walk and average recent IPO are the baselines; DM is Diebold-Mariano (HLN-corrected), the bootstrap is a moving-block one.

## Stocks: next-day direction

1,150,529 out-of-sample predictions, 2017-01-03 to 2026-11-12.

| forecaster | Brier | log loss | hit rate | ECE | MAE | RMSE |
|---|---|---|---|---|---|---|
| model | 0.2498 | 0.6927 | 51.5% | 0.008 | 0.0141 | 0.0220 |
| base | 0.2499 | 0.6929 | 51.7% | 0.011 | 0.0140 | 0.0219 |
| rw | 0.2500 | 0.6931 | 50.0% | 0.018 | 0.0140 | 0.0219 |

| comparison | mean loss difference | DM p | DM p (Holm) | bootstrap 95% CI | bootstrap p |
|---|---|---|---|---|---|
| model vs base: brier | -0.00008 | 0.594 | 1 | [-0.00040, +0.00024] | 0.596 |
| model vs base: log_loss | -0.00018 | 0.577 | 1 | [-0.00080, +0.00048] | 0.581 |
| model vs base: abs_error | +0.00012 | 1.83e-06 | 1.1e-05 | [+0.00007, +0.00017] | 0.0005 |
| model vs rw: brier | -0.00024 | 0.36 | 1 | [-0.00073, +0.00029] | 0.336 |
| model vs rw: log_loss | -0.00048 | 0.361 | 1 | [-0.00147, +0.00059] | 0.339 |
| model vs rw: abs_error | +0.00012 | 1.83e-06 | 1.1e-05 | [+0.00007, +0.00017] | 0.0005 |

The model does not beat the best baseline (base) on Brier at the 5% level after Holm.
A negative difference means the model's loss is lower.

## IPOs: first-day pop

No resolved out-of-sample predictions yet.

## Leakage test (scrambled future)

- stocks: passed at cutoffs 2021-06-08, 2024-02-27, 2026-05-01 (largest change 0)
- IPOs: passed at cutoffs  (largest change 0)
