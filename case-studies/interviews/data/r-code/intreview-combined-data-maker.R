# Script to combine multiple data sources using text_id as key

# Load required libraries
library(readxl)      # For reading Excel files
library(dplyr)       # For data manipulation
library(readr)       # For reading CSV files
library(tidyr)       # For data reshaping

# Function to safely read Excel worksheet
safe_read_excel <- function(file_path, sheet_name) {
  tryCatch({
    # Read Excel file with specific sheet
    data <- read_excel(file_path, sheet = sheet_name)
    cat("Successfully read", file_path, "sheet:", sheet_name, "\n")
    cat("Number of rows:", nrow(data), "\n")
    cat("Number of columns:", ncol(data), "\n")
    cat("Column names:", paste(names(data), collapse = ", "), "\n\n")
    return(data)
  }, error = function(e) {
    # Print warning if there's an error reading the file
    warning(paste("Could not read file:", file_path, "sheet:", sheet_name, "Error:", e$message))
    return(NULL)
  })
}

# Function to safely read CSV
safe_read_csv <- function(file_path) {
  tryCatch({
    # Read CSV file
    data <- read_csv(file_path)
    cat("Successfully read", file_path, "\n")
    cat("Number of rows:", nrow(data), "\n")
    cat("Number of columns:", ncol(data), "\n")
    cat("Column names:", paste(names(data), collapse = ", "), "\n\n")
    return(data)
  }, error = function(e) {
    # Print warning if there's an error reading the file
    warning(paste("Could not read file:", file_path, "Error:", e$message))
    return(NULL)
  })
}

# Set base directories
interview_dir <- "C:/Users/Kenneth Colombe/OneDrive - UT Cloud/Desktop/Data Analysis w AI/text analysis/final_merge"

# Define file paths
domain_sentiment_file <- file.path(interview_dir, "domain_sentiment_results.xlsx")
interview_texts_file <- file.path(interview_dir, "interview-texts-only.xlsx")
aggregated_ratings_file <- file.path("aggregated_ratings_by_text.csv")
game_data_file <- file.path(interview_dir, "game_data.xlsx")

# Read each data source
cat("Reading data sources...\n\n")

# 1. Read domain sentiment results
domain_sentiment <- safe_read_excel(domain_sentiment_file, "domain_sentiment_results")
if (is.null(domain_sentiment)) {
  stop("Failed to read domain sentiment data. Please check the file path and sheet name.")
}

# 2. Read interview texts
interview_texts <- safe_read_excel(interview_texts_file, "Sheet1")
if (is.null(interview_texts)) {
  stop("Failed to read interview texts data. Please check the file path and sheet name.")
}

# 3. Read aggregated ratings
aggregated_ratings <- safe_read_csv(aggregated_ratings_file)
if (is.null(aggregated_ratings)) {
  stop("Failed to read aggregated ratings data. Please check the file path.")
}

# 4. Read game data
game_data <- safe_read_excel(game_data_file, "final_text_game_info_combined")
if (is.null(game_data)) {
  stop("Failed to read game data. Please check the file path and sheet name.")
}

# Check that all dataframes have text_id column
check_text_id <- function(df, name) {
  if (!"text_id" %in% names(df)) {
    stop(paste("text_id column not found in", name))
  }
}

check_text_id(domain_sentiment, "domain sentiment data")
check_text_id(interview_texts, "interview texts data")
check_text_id(aggregated_ratings, "aggregated ratings data")
check_text_id(game_data, "game data")

# Ensure text_id is character type in all dataframes
domain_sentiment$text_id <- as.character(domain_sentiment$text_id)
interview_texts$text_id <- as.character(interview_texts$text_id)
aggregated_ratings$text_id <- as.character(aggregated_ratings$text_id)
game_data$text_id <- as.character(game_data$text_id)

# Combine all data sources using left joins
cat("Combining data sources...\n")

# Start with interview texts as base
combined_data <- interview_texts

# Join domain sentiment data
combined_data <- combined_data %>%
  left_join(domain_sentiment, by = "text_id")

# Join aggregated ratings
combined_data <- combined_data %>%
  left_join(aggregated_ratings, by = "text_id")

# Join game data
combined_data <- combined_data %>%
  left_join(game_data, by = "text_id")

# Check for any text_ids that were dropped
cat("Checking for dropped text_ids...\n")
cat("Original text_ids in interview_texts:", length(unique(interview_texts$text_id)), "\n")
cat("Final text_ids in combined data:", length(unique(combined_data$text_id)), "\n")

# Check for missing values
cat("\nChecking for missing values after join...\n")
missing_counts <- colSums(is.na(combined_data))
for (col in names(missing_counts)) {
  if (missing_counts[col] > 0) {
    cat("Column", col, "has", missing_counts[col], "missing values\n")
  }
}

# Save combined data
output_file <- "combined_text_data.csv"
write.csv(combined_data, output_file, row.names = FALSE)
cat("\nCombined data saved to:", output_file, "\n")
cat("Total rows:", nrow(combined_data), "\n")
cat("Total columns:", ncol(combined_data), "\n")

# Create a summary of the join
summary_file <- "data_join_summary.csv"
summary_data <- data.frame(
  data_source = c("interview_texts", "domain_sentiment", "aggregated_ratings", "game_data", "combined_data"),
  row_count = c(nrow(interview_texts), nrow(domain_sentiment), nrow(aggregated_ratings), nrow(game_data), nrow(combined_data)),
  column_count = c(ncol(interview_texts), ncol(domain_sentiment), ncol(aggregated_ratings), ncol(game_data), ncol(combined_data)),
  unique_text_ids = c(length(unique(interview_texts$text_id)), 
                      length(unique(domain_sentiment$text_id)), 
                      length(unique(aggregated_ratings$text_id)), 
                      length(unique(game_data$text_id)), 
                      length(unique(combined_data$text_id)))
)
write.csv(summary_data, summary_file, row.names = FALSE)
cat("Join summary saved to:", summary_file, "\n")