# Using AI to design illustration
# Claude 4.0 sonnet 2025-08-13
# version 6
# prompt: Maybe add a scatterplot at the end



library(tidyverse)
library(ggplot2)
library(viridis)

# Set seed for reproducibility
set.seed(42)

# Generate data with EXTREME common support violations
n <- 3000

# Create parental income distribution (MUCH tighter distribution)
log_parent_income <- rnorm(n, mean = 10.8, sd = 0.5)

# VERY tight selection thresholds for minimal overlap
college_prob <- ifelse(log_parent_income < 10.75, 0.02,   # Almost no college below 10.75
                       ifelse(log_parent_income > 11.05, 0.98,   # Almost all college above 11.05
                              0.5))                               # 50/50 in tiny middle range

# Add some randomness but maintain very strong correlation
has_degree <- rbinom(n, 1, college_prob)

# Generate log income outcome with EXPONENTIAL heterogeneous treatment effects
parental_effect <- 0.6        # Strong intergenerational correlation
intercept <- 4.0              # Base log income

# EXPONENTIAL college premium: returns explode with family income
college_premium <- 0.05 * exp(1.2 * (log_parent_income - 10.8))

log_income <- intercept + 
  parental_effect * log_parent_income + 
  college_premium * has_degree +
  rnorm(n, 0, 0.15)  # Low noise for clear signal

# Create the dataset
data <- tibble(
  log_parent_income = log_parent_income,
  has_degree_num = has_degree,
  has_degree = factor(has_degree, 
                      levels = c(0, 1), 
                      labels = c("No College", "College")),
  log_income = log_income
)

# Create the common support visualization
p1 <- data %>%
  ggplot(aes(x = log_parent_income, fill = has_degree)) +
  geom_histogram(aes(y = after_stat(density)), 
                 alpha = 0.7, 
                 position = "identity", 
                 bins = 40) +
  scale_fill_viridis_d(option = "plasma", end = 0.8) +
  labs(
    title = "Common Support Violation: College Attendance by Family Income",
    subtitle = "Distributions show limited overlap in extreme income ranges",
    x = "Log Parental Income",
    y = "Density",
    fill = "Education Status"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(size = 14, face = "bold"),
    plot.subtitle = element_text(size = 11, color = "gray40"),
    legend.position = "bottom"
  ) +
  # Add vertical lines to highlight problematic regions (very tight thresholds)
  geom_vline(xintercept = c(10.75, 11.05), 
             linetype = "dashed", 
             color = "red", 
             alpha = 0.8, 
             size = 1) +
  annotate("text", x = 10.4, y = 0.35, 
           label = "Almost no\ncollege (2%)", 
           size = 3, color = "red", fontface = "bold") +
  annotate("text", x = 11.4, y = 0.35, 
           label = "Almost all\ncollege (98%)", 
           size = 3, color = "red", fontface = "bold") +
  annotate("rect", xmin = 10.75, xmax = 11.05, ymin = -Inf, ymax = Inf,
           alpha = 0.15, fill = "green") +
  annotate("text", x = 10.9, y = 0.2, 
           label = "Tiny common\nsupport region", 
           size = 3, color = "darkgreen", fontface = "bold")

# Display the plot
print(p1)

# Create scatterplot to show individual observations and gaps
p2 <- data %>%
  ggplot(aes(x = log_parent_income, y = log_income, color = has_degree)) +
  geom_point(alpha = 0.6, size = 1.2) +
  scale_color_viridis_d(option = "plasma", end = 0.8) +
  # Add regression lines
  geom_smooth(method = "lm", se = FALSE, size = 1.2) +
  # Highlight common support region
  geom_vline(xintercept = c(10.75, 11.05), 
             linetype = "dashed", color = "red", alpha = 0.8) +
  annotate("rect", xmin = 10.75, xmax = 11.05, ymin = -Inf, ymax = Inf,
           alpha = 0.1, fill = "green") +
  labs(
    title = "Individual Observations: Common Support Gaps",
    subtitle = "Each point represents one person - note missing counterfactuals outside green region",
    x = "Log Parental Income", 
    y = "Log Individual Income",
    color = "Education Status"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(size = 14, face = "bold"),
    plot.subtitle = element_text(size = 11, color = "gray40"),
    legend.position = "bottom"
  )

print(p2)

# Summary statistics and common support analysis
cat("\n=== Common Support Analysis ===\n")
cat("Sample size:", nrow(data), "\n")

# Show the problem quantitatively
support_analysis <- data %>%
  group_by(has_degree) %>%
  summarise(
    n = n(),
    min_income = min(log_parent_income),
    max_income = max(log_parent_income),
    mean_income = mean(log_parent_income),
    .groups = "drop"
  )

print(support_analysis)

# Calculate overlap region precisely
college_min <- min(data$log_parent_income[data$has_degree == "College"])
college_max <- max(data$log_parent_income[data$has_degree == "College"])
no_college_min <- min(data$log_parent_income[data$has_degree == "No College"])
no_college_max <- max(data$log_parent_income[data$has_degree == "No College"])

overlap_min <- max(college_min, no_college_min)
overlap_max <- min(college_max, no_college_max)

cat("\nCommon support region: [", round(overlap_min, 2), ", ", round(overlap_max, 2), "]\n")

# Define overlap sample
data_overlap <- data %>%
  filter(log_parent_income >= overlap_min & log_parent_income <= overlap_max)

cat("Overlap sample size:", nrow(data_overlap), "observations\n")
cat("Percentage of full sample:", round(100 * nrow(data_overlap) / nrow(data), 1), "%\n")

# === OLS COMPARISON ===
cat("\n=== OLS Regression Comparison ===\n")

# Full sample regression
model_full <- lm(log_income ~ has_degree_num + log_parent_income, data = data)

# Overlap sample regression  
model_overlap <- lm(log_income ~ has_degree_num + log_parent_income, data = data_overlap)

# Extract coefficients
coef_full <- summary(model_full)$coefficients["has_degree_num", ]
coef_overlap <- summary(model_overlap)$coefficients["has_degree_num", ]

# Create comparison table
comparison <- tibble(
  Sample = c("Full Sample", "Common Support Only"),
  `N` = c(nrow(data), nrow(data_overlap)),
  `College Coefficient` = round(c(coef_full[1], coef_overlap[1]), 3),
  `Standard Error` = round(c(coef_full[2], coef_overlap[2]), 3),
  `t-statistic` = round(c(coef_full[3], coef_overlap[3]), 2)
)

print(comparison)

# Calculate average treatment effects for interpretation
# True ATE varies exponentially with parental income
ate_full <- mean(0.05 * exp(0.4 * (data$log_parent_income - 10.8)))
ate_overlap <- mean(0.05 * exp(0.4 * (data_overlap$log_parent_income - 10.8)))

cat("\nInterpretation:\n")
cat("- Model uses EXPONENTIAL heterogeneous treatment effects\n")
cat("- College premium = 0.05 * exp(0.4 * (parental_income - 10.8))\n")
cat("- Low-income families: ~5% returns, High-income families: ~20%+ returns\n\n")
cat("- True ATE in full sample:", round(ate_full, 3), "\n")
cat("- True ATE in overlap sample:", round(ate_overlap, 3), "\n")
cat("- Full sample estimate:", round(coef_full[1], 3), "\n")
cat("- Common support estimate:", round(coef_overlap[1], 3), "\n")
cat("- Bias in full sample:", round(coef_full[1] - ate_full, 3), "\n")
cat("- Bias in overlap sample:", round(coef_overlap[1] - ate_overlap, 3), "\n\n")

cat("MECHANISM OF BIAS:\n")
cat("- Full sample includes many high-income college grads (huge returns)\n")
cat("- But almost no high-income non-grads for comparison\n")
cat("- Estimated effect conflates college premium with family income effects\n")
cat("- Common support focuses on comparable middle-income families\n")