# Script to combine all Excel files and aggregate ratings by text_id

# Load required libraries
library(readxl)      # For reading Excel files
library(dplyr)       # For data manipulation
library(purrr)       # For functional programming tools
library(tidyr)       # For data reshaping
library(stringr)     # For string manipulation

# Set the directory path
directory_path <- "C:\\Users\\Kenneth Colombe\\OneDrive - UT Cloud\\Desktop\\Data Analysis w AI\\text analysis\\final_merge\\student_ratings"


# Function to read Excel files
read_excel_files <- function(file_path) {
  tryCatch({
    # Read Excel file
    data <- read_excel(file_path)
    
    # Add file name as a column to track the source
    data$source_file <- basename(file_path)
    
    return(data)
  }, error = function(e) {
    # Print warning if there's an error reading the file
    warning(paste("Could not read file:", file_path, "Error:", e$message))
    return(NULL)
  })
}

# Create directory if it doesn't exist
if (!dir.exists(directory_path)) {
  dir.create(directory_path, recursive = TRUE)
  cat("Directory created:", directory_path, "\n")
}

# Get list of all Excel files in the directory
excel_files <- list.files(
  path = directory_path,
  pattern = "\\.xlsx$|\\.xls$",  # Match both .xlsx and .xls files
  full.names = TRUE
)

# Check if any Excel files were found
if (length(excel_files) == 0) {
  stop("No Excel files found in the specified directory.")
}

# Print the number of files found
cat("Found", length(excel_files), "Excel files in the directory.\n")

# Read all Excel files
all_data <- excel_files %>%
  map(read_excel_files) %>%
  bind_rows()

# Check if any data was read
if (nrow(all_data) == 0) {
  stop("No data was read from the Excel files.")
}

# Save the combined raw data
raw_output_file <- "combined_raw_data.csv"
write.csv(all_data, raw_output_file, row.names = FALSE)
cat("Raw combined data saved to:", raw_output_file, "\n")

# Print column names to help identify relevant columns
cat("Available columns in the dataset:\n")
print(names(all_data))

# Using the actual column names from the dataset
text_id_col <- "text_id"       # Column containing text ID
human_rating_col <- "human_rating"  # Column containing human ratings
ai_rating_col <- "ai_rating"        # Column containing AI ratings
uid_col <- "uid"               # Column containing rater ID

# Check if the required columns exist
required_cols <- c(text_id_col, human_rating_col, ai_rating_col, uid_col)
missing_cols <- required_cols[!required_cols %in% names(all_data)]

if (length(missing_cols) > 0) {
  warning("The following required columns are missing: ", paste(missing_cols, collapse = ", "),
          "\nPlease adjust the column names in the script.")
}

# Aggregate data by text_id
  aggregated_data <- all_data %>%
    group_by(!!sym(text_id_col)) %>%
    summarize(
      num_human_raters = n_distinct(!!sym(uid_col)),
      avg_human_rating = mean(!!sym(human_rating_col), na.rm = TRUE),
      mad_human_rating = mean(abs(!!sym(human_rating_col) - mean(!!sym(human_rating_col), na.rm = TRUE)), na.rm = TRUE),
      avg_ai_rating = mean(!!sym(ai_rating_col), na.rm = TRUE),
      human_rate_first = first(!!sym(human_rating_col)),
      ai_rate_first = first(!!sym(ai_rating_col)),
      human_ai_diff = avg_human_rating - avg_ai_rating,
      .groups = "drop"
    )
  
  # Handle NaN values in mean absolute deviation when there's only one rating
  aggregated_data$mad_human_rating[is.na(aggregated_data$mad_human_rating)] <- 0
  
  # Create output file path
  agg_output_file <- "aggregated_ratings_by_text.csv"
  
  # Save the aggregated data as a CSV file
  write.csv(aggregated_data, agg_output_file, row.names = FALSE)
  
  # Print success message
  cat("Aggregated data saved to:", agg_output_file, "\n")
  cat("Total texts:", nrow(aggregated_data), "\n")
