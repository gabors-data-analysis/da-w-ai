# Using AI to design illustration
# Claude 4.0 sonnet 2025-08-13
# version 1
# prompt

library(tidyverse)
library(ggplot2)

# Set seed for reproducibility
set.seed(42)

# Generate data with realistic common support violations
n <- 2500

# Create parental income distribution
log_parent_income <- rnorm(n, mean = 10.8, sd = 0.6)

# College attendance probability (strong function of parental income)
# Logistic function ensuring violations at extremes
college_prob <- plogis(-8 + 0.8 * log_parent_income)

# Add some randomness but maintain strong correlation
has_degree <- rbinom(n, 1, college_prob)

# Create the dataset
data <- tibble(
  log_parent_income = log_parent_income,
  has_degree = factor(has_degree, 
                      levels = c(0, 1), 
                      labels = c("No College", "College"))
)

# Create the common support visualization
p1 <- data %>%
  ggplot(aes(x = log_parent_income, fill = has_degree)) +
  geom_histogram(aes(y = after_stat(density)), 
                 alpha = 0.7, 
                 position = "identity", 
                 bins = 40) +
  scale_fill_manual(values = c("No College" = "#E74C3C", 
                               "College" = "#3498DB")) +
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
  geom_vline(xintercept = c(9.8, 11.8), 
             linetype = "dashed", 
             color = "red", 
             alpha = 0.6) +
  annotate("text", x = 9.5, y = 0.4, 
           label = "No college\ngraduates", 
           size = 3, color = "red") +
  annotate("text", x = 12.1, y = 0.4, 
           label = "Almost no\nnon-graduates", 
           size = 3, color = "red")

# Alternative: Side-by-side density plots
p2 <- data %>%
  ggplot(aes(x = log_parent_income, fill = has_degree)) +
  geom_density(alpha = 0.6) +
  scale_fill_manual(values = c("No College" = "#E74C3C", 
                               "College" = "#3498DB")) +
  labs(
    title = "Common Support: Overlapping Distributions",
    subtitle = "Areas without overlap indicate common support violations",
    x = "Log Parental Income",
    y = "Density",
    fill = "Education Status"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(size = 14, face = "bold"),
    plot.subtitle = element_text(size = 11, color = "gray40"),
    legend.position = "bottom"
  )

# Display both plots
print(p1)
print(p2)

# Summary statistics for teaching
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

# Calculate overlap region
overall_min <- min(data$log_parent_income)
overall_max <- max(data$log_parent_income)
college_min <- min(data$log_parent_income[data$has_degree == "College"])
college_max <- max(data$log_parent_income[data$has_degree == "College"])
no_college_min <- min(data$log_parent_income[data$has_degree == "No College"])
no_college_max <- max(data$log_parent_income[data$has_degree == "No College"])

overlap_min <- max(college_min, no_college_min)
overlap_max <- min(college_max, no_college_max)

cat("\nCommon support region: [", round(overlap_min, 2), ", ", round(overlap_max, 2), "]\n")
cat("This represents", round(overlap_max - overlap_min, 2), "log points of parental income\n")

