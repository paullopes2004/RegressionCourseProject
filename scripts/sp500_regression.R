#!/usr/bin/env Rscript
suppressPackageStartupMessages({
  library(tidyverse)
  library(lubridate)
  library(glue)
  library(broom)
  library(scales)
})

message('--- S&P 500 Regression Project ---')

raw_path <- file.path('data', 'raw', 'all_stocks_5yr.csv')
if (!file.exists(raw_path)) {
  stop(glue('File not found: {raw_path}. Please place the Kaggle CSV there.'))
}

raw_df <- read_csv(raw_path, show_col_types = FALSE) %>%
  rename_with(~tolower(.x))

message('Rows: ', nrow(raw_df), ' | Columns: ', ncol(raw_df))

target_year <- 2017

message('Preparing daily data...')
daily_df <- raw_df %>%
  mutate(date = ymd(date)) %>%
  arrange(name, date) %>%
  group_by(name) %>%
  mutate(daily_log_return = log(close) - log(lag(close))) %>%
  ungroup()

if (!dir.exists('data/processed')) dir.create('data/processed', recursive = TRUE)
if (!dir.exists('figures')) dir.create('figures', recursive = TRUE)
if (!dir.exists('outputs')) dir.create('outputs', recursive = TRUE)

message('Engineering features for year ', target_year, '...')

feature_fn <- function(tbl) {
  yr_filter <- tbl %>% filter(year(date) %in% c(target_year, target_year + 1))
  idx_year <- which(year(yr_filter$date) == target_year)
  idx_future <- which(year(yr_filter$date) == target_year + 1)
  if (length(idx_year) == 0 || length(idx_future) == 0) {
    return(tibble())
  }
  start_price <- yr_filter$close[idx_year[1]]
  end_price <- yr_filter$close[idx_future[1]]
  if (is.na(start_price) || is.na(end_price) || start_price <= 0 || end_price <= 0) {
    return(tibble())
  }
  year_returns <- yr_filter$daily_log_return[idx_year]
  if (sum(is.finite(year_returns)) < 20) {
    return(tibble())
  }
  avg_volume <- mean(yr_filter$volume[idx_year], na.rm = TRUE)
  momentum_90 <- if (length(idx_year) >= 90) {
    log(yr_filter$close[idx_year[90]] / yr_filter$close[idx_year[1]])
  } else {
    NA_real_
  }
  trend_ma30 <- if (length(idx_year) >= 30) {
    ma30 <- mean(yr_filter$close[idx_year[1:30]])
    start <- yr_filter$close[idx_year[1]]
    (ma30 - start) / start
  } else {
    NA_real_
  }
  tibble(
    name = yr_filter$name[1],
    observations_2017 = length(idx_year),
    start_price = start_price,
    end_price = end_price,
    y_log_return = log(end_price / start_price),
    volatility = sd(year_returns, na.rm = TRUE) * sqrt(252),
    avg_volume_mln = avg_volume / 1e6,
    momentum_90 = momentum_90,
    trend_ma30 = trend_ma30
  )
}

features_df <- daily_df %>%
  group_by(name) %>%
  group_modify(~feature_fn(.x)) %>%
  ungroup() %>%
  drop_na(y_log_return, volatility, avg_volume_mln, momentum_90, trend_ma30)

write_csv(features_df, 'data/processed/sp500_features.csv')
message('Generated features for ', nrow(features_df), ' tickers.')

message('Building regression model...')
model_df <- features_df

ols_fit <- lm(y_log_return ~ volatility + avg_volume_mln + momentum_90 + trend_ma30, data = model_df)
model_coef <- tidy(ols_fit, conf.int = TRUE)
model_glance <- glance(ols_fit)
model_aug <- augment(ols_fit)

write_csv(model_coef, 'outputs/model_coefficients.csv')
write_csv(model_glance, 'outputs/model_glance.csv')
write_csv(model_aug, 'outputs/model_augmented_residuals.csv')

message('R-squared: ', round(model_glance$r.squared, 3))

message('Creating diagnostic plots...')

ggplot(model_aug, aes(.fitted, .resid)) +
  geom_point(alpha = 0.5, color = '#6A5ACD') +
  geom_hline(yintercept = 0, linetype = 'dashed', color = 'gray60') +
  labs(title = 'Residuals vs Fitted', x = 'Fitted values', y = 'Residuals') +
  theme_minimal(base_size = 12)

ggsave('figures/residuals_vs_fitted.png', width = 6, height = 4, dpi = 300)

qq <- ggplot(model_aug, aes(sample = .resid)) +
  stat_qq(color = '#008b8b') +
  stat_qq_line(color = 'gray40') +
  labs(title = 'Normal Q-Q Plot', x = 'Theoretical Quantiles', y = 'Sample Quantiles') +
  theme_minimal(base_size = 12)

qq

ggsave('figures/qq_plot.png', width = 6, height = 4, dpi = 300)

corr_df <- model_df %>% select(y_log_return, volatility, avg_volume_mln, momentum_90, trend_ma30)

corr_matrix <- cor(corr_df)

corr_tbl <- corr_df %>%
  pivot_longer(cols = everything()) %>%
  group_by(name) %>%
  summarise(mean = mean(value), sd = sd(value))

message('Pipeline complete. Artifacts saved to data/processed, outputs, and figures directories.')
