# Backtest

Walk-forward, out of sample, run `20261024T102211Z-weekly-fc5670` at 2026-10-24T10:22:11Z. Stocks: next-session direction (close up) of S&P 500 members; IPOs: a first close 20% or more above the offer. Base rate, random walk and average recent IPO are the baselines; DM is Diebold-Mariano (HLN-corrected), the bootstrap is a moving-block one.

## Stocks: next-day direction

1,142,273 out-of-sample predictions, 2017-01-03 to 2026-10-21.

| forecaster | Brier | log loss | hit rate | ECE | MAE | RMSE |
|---|---|---|---|---|---|---|
| model | 0.2498 | 0.6927 | 51.5% | 0.008 | 0.0141 | 0.0219 |
| base | 0.2499 | 0.6929 | 51.7% | 0.011 | 0.0140 | 0.0218 |
| rw | 0.2500 | 0.6931 | 50.0% | 0.018 | 0.0140 | 0.0218 |

| comparison | mean loss difference | DM p | DM p (Holm) | bootstrap 95% CI | bootstrap p |
|---|---|---|---|---|---|
| model vs base: brier | -0.00008 | 0.628 | 1 | [-0.00039, +0.00024] | 0.637 |
| model vs base: log_loss | -0.00016 | 0.61 | 1 | [-0.00079, +0.00047] | 0.618 |
| model vs base: abs_error | +0.00012 | 1.63e-06 | 9.76e-06 | [+0.00007, +0.00017] | 0.0005 |
| model vs rw: brier | -0.00023 | 0.38 | 1 | [-0.00075, +0.00030] | 0.388 |
| model vs rw: log_loss | -0.00046 | 0.38 | 1 | [-0.00150, +0.00060] | 0.389 |
| model vs rw: abs_error | +0.00012 | 1.63e-06 | 9.76e-06 | [+0.00007, +0.00017] | 0.0005 |

The model does not beat the best baseline (base) on Brier at the 5% level after Holm.
A negative difference means the model's loss is lower.

## IPOs: first-day pop

No resolved out-of-sample predictions yet.

## Leakage test (scrambled future)

- stocks: passed at cutoffs 2021-05-27, 2024-02-09, 2026-04-13 (largest change 0)
- IPOs: passed at cutoffs  (largest change 0)
