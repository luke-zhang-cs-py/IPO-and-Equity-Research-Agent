# Backtest

Walk-forward, out of sample, run `20261031T114512Z-weekly-cd128b` at 2026-10-31T11:45:12Z. Stocks: next-session direction (close up) of S&P 500 members; IPOs: a first close 20% or more above the offer. Base rate, random walk and average recent IPO are the baselines; DM is Diebold-Mariano (HLN-corrected), the bootstrap is a moving-block one.

## Stocks: next-day direction

1,145,290 out-of-sample predictions, 2017-01-03 to 2026-10-29.

| forecaster | Brier | log loss | hit rate | ECE | MAE | RMSE |
|---|---|---|---|---|---|---|
| model | 0.2498 | 0.6927 | 51.5% | 0.008 | 0.0141 | 0.0219 |
| base | 0.2499 | 0.6929 | 51.7% | 0.011 | 0.0140 | 0.0218 |
| rw | 0.2500 | 0.6931 | 50.0% | 0.018 | 0.0140 | 0.0218 |

| comparison | mean loss difference | DM p | DM p (Holm) | bootstrap 95% CI | bootstrap p |
|---|---|---|---|---|---|
| model vs base: brier | -0.00008 | 0.609 | 1 | [-0.00039, +0.00025] | 0.608 |
| model vs base: log_loss | -0.00017 | 0.591 | 1 | [-0.00079, +0.00050] | 0.586 |
| model vs base: abs_error | +0.00012 | 1.72e-06 | 1.03e-05 | [+0.00007, +0.00018] | 0.0005 |
| model vs rw: brier | -0.00024 | 0.37 | 1 | [-0.00076, +0.00029] | 0.375 |
| model vs rw: log_loss | -0.00047 | 0.371 | 1 | [-0.00153, +0.00059] | 0.375 |
| model vs rw: abs_error | +0.00012 | 1.72e-06 | 1.03e-05 | [+0.00007, +0.00018] | 0.0005 |

The model does not beat the best baseline (base) on Brier at the 5% level after Holm.
A negative difference means the model's loss is lower.

## IPOs: first-day pop

No resolved out-of-sample predictions yet.

## Leakage test (scrambled future)

- stocks: passed at cutoffs 2021-06-01, 2024-02-14, 2026-04-17 (largest change 0)
- IPOs: passed at cutoffs  (largest change 0)
