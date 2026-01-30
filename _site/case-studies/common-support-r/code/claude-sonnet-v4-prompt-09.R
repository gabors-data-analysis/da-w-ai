library(tidyverse)
library(ggplot2)
library(viridis)

# Set seed for reproducibility
set.seed(42)

# Generate data with EXTREME common support violations
n <- 3000

# Create parental income distribution (MUCH tighter distribution)
log_parent_income <- rnorm(n, mean = 10.4, sd = 0.4)

over_low <- 10.45
over_high <-11.25

# VERY tight selection thresholds for minimal overlap
college_prob <- ifelse(log_parent_income < over_low, 0.02,   # Almost no college below 10.75
                       ifelse(log_parent_income > over_high, 0.98,   # Almost all college above 11.05
                              0.5))                               # 50/50 in tiny middle range

# Add some randomness but maintain very strong correlation
has_degree <- rbinom(n, 1, college_prob)

# Generate log income outcome with QUADRATIC functions
# Control group (no college): STRONG downward curvature at low incomes
intercept_control <- 8.5
linear_control <- 0.3
quadratic_control <- -1.4  # Strong negative curvature

# Treated group (college): MINIMAL curvature, mostly linear  
intercept_treated <- 9.5
linear_treated <- 0.3
quadratic_treated <- -0.05  # Very small curvature

# Center quadratic around 11.0 (above support region)
center <- 11.0

# Generate outcomes using quadratic functions
log_income <- ifelse(has_degree == 0,
                     # No college: strong quadratic - outcomes plummet at low incomes
                     intercept_control + linear_control * log_parent_income + 
                       quadratic_control * (log_parent_income - center)^2 + rnorm(n, 0, 0.12),
                     # College: minimal quadratic - mostly linear
                     intercept_treated + linear_treated * log_parent_income + 
                       quadratic_treated * (log_parent_income - center)^2 + rnorm(n, 0, 0.12))

# Create the dataset
data <- tibble(
  log_parent_income = log_parent_income,
  has_degree_num = has_degree,
  has_degree = factor(has_degree, 
                      levels = c(0, 1), 
                      labels = c("No College", "College")),
  log_income = log_income
)


# Create scatterplot to show individual observations and gaps
p2 <- data %>%
  ggplot(aes(x = log_parent_income, y = log_income, color = has_degree)) +
  geom_point(alpha = 0.6, size = 1.2) +
  scale_color_viridis_d(option = "plasma", end = 0.8) +
  # Add regression lines
  geom_smooth(method = "lm", se = FALSE, size = 1.2) +
  # Highlight common support region
  geom_vline(xintercept = c(over_low, over_high), 
             linetype = "dashed", color = "red", alpha = 0.8) +
  annotate("rect", xmin = over_low, xmax = over_high, ymin = -Inf, ymax = Inf,
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
  geom_vline(xintercept = c(over_low, over_high), 
             linetype = "dashed", 
             color = "red", 
             alpha = 0.8, 
             size = 1) +
  annotate("text", x = (overlap_min-0.3), y = 0.35, 
           label = "Almost no\ncollege (2%)", 
           size = 3, color = "red", fontface = "bold") +
  annotate("text", x = overlap_max, y = 0.35, 
           label = "Almost all\ncollege (98%)", 
           size = 3, color = "red", fontface = "bold") +
  annotate("rect", xmin = overlap_min, xmax = overlap_max, ymin = -Inf, ymax = Inf,
           alpha = 0.15, fill = "green") +
  annotate("text", x = 10.9, y = 0.2, 
           label = "Tiny common\nsupport region", 
           size = 3, color = "darkgreen", fontface = "bold")

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

data <- data %>%
  mutate(
    log_parent_income2 = log_parent_income^2,  # Add quadratic term
    has_degree_num = as.numeric(has_degree) - 1  # Convert factor to numeric (0/1)
  )

data_overlap <- data_overlap %>%
  mutate(
    log_parent_income2 = log_parent_income^2,  # Add quadratic term
    has_degree_num = as.numeric(has_degree) - 1  # Convert factor to numeric (0/1)
  )

# Full sample regression
model_full <- lm(log_income ~ has_degree_num  + log_parent_income  , data = data)
model_full
# Overlap sample regression  
model_overlap <- lm(log_income ~ has_degree_num + log_parent_income, data = data_overlap)
model_overlap

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

# Calculate treatment effects for interpretation  
# Control: 10.0 + 0.2*x - 0.8*(x-11)^2
# Treated: 9.5 + 0.4*x - 0.05*(x-11)^2  
# Treatment Effect = -0.5 + 0.2*x + 0.75*(x-11)^2

# Function to calculate treatment effect
calc_te <- function(x) -0.5 + 0.2*x + 0.75*(x-11)^2

# Calculate average treatment effects
ate_full <- mean(calc_te(data$log_parent_income))
ate_overlap <- mean(calc_te(data_overlap$log_parent_income))

cat("\nInterpretation:\n")
cat("- QUADRATIC OUTCOME FUNCTIONS by education group:\n")
cat("- No College:  y = 10.0 + 0.2*x - 0.8*(x-11)² (STRONG curvature)\n")
cat("- College:     y = 9.5 + 0.4*x - 0.05*(x-11)² (MINIMAL curvature)\n")
cat("- Treatment Effect = -0.5 + 0.2*x + 0.75*(x-11)²\n\n")

# Show treatment effects at different income levels
cat("Treatment effects by family income:\n")
for(income in c(9.0, 9.5, 10.0, 10.8, 11.0, 12.0)) {
  te <- calc_te(income)
  cat(sprintf("- At log_parent_income = %.1f: %+.0f%% return to college\n", income, te * 100))
}
cat("\n")

cat("- True ATE in full sample:", round(ate_full, 3), "\n")
cat("- True ATE in overlap sample:", round(ate_overlap, 3), "\n")
cat("- Full sample estimate:", round(coef_full[1], 3), "\n")
cat("- Common support estimate:", round(coef_overlap[1], 3), "\n")
cat("- Bias in full sample:", round(coef_full[1] - ate_full, 3), "\n")
cat("- Bias in overlap sample:", round(coef_overlap[1] - ate_overlap, 3), "\n\n")

cat("MECHANISM OF BIAS:\n")
cat("- Control group outcomes PLUMMET at low family incomes (quadratic penalty)\n")
cat("- Treated group outcomes remain stable (minimal curvature)\n")  
cat("- Huge treatment effects at low incomes (outside common support)\n")
cat("- Full sample: Misses these large effects due to no low-income college grads\n")
cat("- Common support: Only captures moderate effects in middle-income range\n")