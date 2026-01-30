# Using AI to design illustration
# Claude 4.0 sonnet 2025-08-13
# version 1
# prompt

library(tidyverse)
library(ggplot2)
library(viridis)

# Set seed for reproducibility
set.seed(42)

# Generate data with realistic common support violations
n <- 2500

# Create parental income distribution
log_parent_income <- rnorm(n, mean = 10.8, sd = 0.7)

# College attendance probability (stronger function for bigger gap)
# More extreme logistic function
college_prob <- plogis(-12 + 1.2 * log_parent_income)

# Add some randomness but maintain strong correlation
has_degree <- rbinom(n, 1, college_prob)

# Generate log income outcome with realistic structure
# College premium + parental income effect + noise
college_premium <- 0.4  # ~40% income boost
parental_effect <- 0.6  # Strong intergenerational correlation
intercept <- 4.5        # Base log income

log_income <- intercept + 
  parental_effect * log_parent_income + 
  college_premium * has_degree +
  rnorm(n, 0, 0.3)  # Random noise

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
  # Add vertical lines to highlight problematic regions
  geom_vline(xintercept = c(9.5, 12.0), 
             linetype = "dashed", 
             color = "red", 
             alpha = 0.6) +
  annotate("text", x = 9.2, y = 0.35, 
           label = "No college\ngraduates", 
           size = 3, color = "red") +
  annotate("text", x = 12.3, y = 0.35, 
           label = "Almost no\nnon-graduates", 
           size = 3, color = "red")

# Display the plot
print(p1)

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
  `t-statistic` = round(c(coef_full[3], coef_overlap[3]), 2),
  `True Effect` = c(0.400, 0.400)  # Known from data generation
)

print(comparison)

cat("\nInterpretation:\n")
cat("- True college premium: 40% (0.400 log points)\n")
cat("- Full sample estimate:", round(coef_full[1], 3), "\n")
cat("- Common support estimate:", round(coef_overlap[1], 3), "\n")
cat("- Bias in full sample:", round(coef_full[1] - 0.400, 3), "\n")
cat("- Bias in overlap sample:", round(coef_overlap[1] - 0.400, 3), "\n")