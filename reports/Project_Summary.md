# S&P 500 Stock Regression Project
**Course:** Regression Methods  
**Student:** Paul Lopes  
**Date:** December 2, 2025  
**Repository:** https://github.com/paullopes2004/RegressionCourseProject

**Contributions:** Data wrangling, feature engineering, regression modeling, visualization, and report writing were completed by Paul Lopes. (Update this line if teammates contribute.)

---

## Abstract
This project evaluates whether basic market microstructure variables explain cross-sectional differences in annual returns for S&P 500 constituents. Daily stock prices from 2013–2018 (Kaggle, Cam Nugent) were aggregated to compute a one-year log return between the first trading day of 2017 and the first trading day of 2018. Predictor variables include 2017 volatility, average trading volume, 90-day momentum, and a 30-day moving-average trend. Multiple linear regression in R explains roughly 53% of the variation in 1-year returns across 503 firms, highlighting momentum and volatility as the dominant drivers. Diagnostic plots indicate adequate linear fit with mild deviations from normality but no major heteroskedasticity issues.

## Introduction
Understanding which stock characteristics explain cross-sectional returns is central to asset pricing. Professional investors often rely on factor models built from fundamental or technical data. This study asks: *Which observable trading characteristics most strongly relate to 1-year returns among large-cap U.S. equities?* By focusing on accessible indicators derived from publicly available price data, the analysis mirrors what students can reproduce without proprietary datasets while reinforcing linear regression concepts taught in class.

## Materials and Methods
1. **Data Source:** `all_stocks_5yr.csv` from Cam Nugent's Kaggle dataset (https://www.kaggle.com/datasets/camnugent/sandp500). Raw data contain daily OHLCV quotes for S&P 500 companies between 2013 and 2018.
2. **Software:** R 4.4 with `tidyverse`, `lubridate`, `broom`, and `scales`. Script: `scripts/sp500_regression.R`.
3. **Feature Engineering:**
   - Convert prices to daily log returns per ticker.
   - Define response `y_log_return = log(price_2018-01-02 / price_2017-01-03)` (first trading days each year).
   - Predictors (computed using 2017 data only):
     - `volatility`: annualized standard deviation of daily log returns.
     - `avg_volume_mln`: mean daily traded shares (millions).
     - `momentum_90`: log return between day 1 and day 90 of 2017.
     - `trend_ma30`: relative difference between the first closing price and the 30-day moving average.
   - Filter tickers with ≥20 valid daily returns and complete predictor set, yielding 503 companies.
4. **Model:** Ordinary Least Squares `lm(y ~ volatility + avg_volume_mln + momentum_90 + trend_ma30)`.
5. **Diagnostics:** Residual-vs-fitted and Q-Q plots saved to `figures/` along with exported coefficient, fit, and residual tables in `outputs/`.

## Results
### Descriptive Statistics
- Sample size: 503 tickers (median start price $69.77).
- Average 1-year log return: 0.187 (≈20.6% simple return).
- Volatility ranges from 9% to 60% annualized; 90-day momentum spans −55% to +43%.

### Model Fit
- `R² = 0.529`, `Adjusted R² = 0.525`, residual standard error `σ = 0.158`.
- ANOVA F-statistic = 139.7 (p < 1e-78), indicating the model explains significantly more variance than an intercept-only model.

### Coefficient Estimates
| Term | Estimate | Std. Error | t | p-value | Interpretation |
| --- | --- | --- | --- | --- | --- |
| Intercept | 0.186 | 0.021 | 8.98 | <1e-17 | Baseline log return when predictors equal zero. |
| Volatility | -0.468 | 0.089 | -5.28 | 2e-7 | Higher volatility associates with lower annual returns, consistent with risk-adjusted drag. |
| Avg Volume (M) | 0.00070 | 0.00111 | 0.63 | 0.531 | Trading activity is not a significant cross-sectional predictor. |
| Momentum 90 | 1.047 | 0.073 | 14.3 | <1e-38 | Positive early-year momentum strongly predicts full-year gains. |
| Trend MA30 | 0.233 | 0.195 | 1.20 | 0.231 | Short-term moving-average slope is not statistically significant after controlling for momentum. |

### Diagnostics
- `figures/residuals_vs_fitted.png`: Residuals scatter evenly without strong funnel shape, supporting homoskedastic errors.
- `figures/qq_plot.png`: Tail deviations suggest mild leptokurtosis, but the central portion aligns closely with normality.

## Discussion
Momentum dominates explanatory power, reaffirming behavioral finance literature that recent winners often continue to outperform. The negative volatility coefficient implies that calmer stocks delivered higher returns during the 2017 window, possibly reflecting investor preference for stability. Volume and short moving-average trends contribute little after controlling for momentum. Limitations include ignoring sector fixed effects, excluding fundamental metrics (PE ratio, earnings surprises), and using only one year of returns. Extending the approach to multiple years or incorporating regularization (LASSO) could test robustness and mitigate multicollinearity.

## Acknowledgments
- Cam Nugent for curating the S&P 500 dataset on Kaggle.
- Regression Methods instructor for project guidance.
- ChatGPT (OpenAI GPT-5.1 Codex) assisted with scripting and documentation; cited per course policy.

## Literature Cited
1. Cam Nugent. *S&P 500 Stock Data*. Kaggle, https://www.kaggle.com/datasets/camnugent/sandp500 (accessed Nov 29, 2025).
2. Jegadeesh, N., & Titman, S. (1993). Returns to buying winners and selling losers: Implications for stock market efficiency. *Journal of Finance*, 48(1), 65–91. (Provides theoretical backing for momentum interpretation.)

## Appendices
- **Appendix A:** `scripts/sp500_regression.R` (analysis pipeline).
- **Appendix B:** `outputs/model_coefficients.csv`, `model_glance.csv`, `model_augmented_residuals.csv` provide machine-readable summaries.
- **Appendix C:** Raw Kaggle CSV stored in `data/raw/` (excluded from written report submission but required for reproducibility).
- **Appendix D:** `figures/residuals_vs_fitted.png`, `figures/qq_plot.png` ready for slides.

*URL to dataset:* https://www.kaggle.com/datasets/camnugent/sandp500
