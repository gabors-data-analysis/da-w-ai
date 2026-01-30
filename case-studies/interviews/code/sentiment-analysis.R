library(httr)
library(jsonlite)
library(readxl)
library(dplyr)
library(purrr)
library(progress)

# API key -- first time use
# you must add your key to "api-key.R" and save it as "my-openai-api-key.R" add it to gitignore


# Set API key
source("my-openai-api-key.R")

# Load data in xlsx format from here or set your path
data_path="/data/interviews/"
post_df <- read_excel(paste0(data_path, "interview-texts-only.xlsx"))

# Validate columns
required_cols <- c("text_id", "processed_tex")
if (!all(required_cols %in% names(post_df))) {
  stop("Missing required columns")
}



#  Change model= to either gpt-3.5-turbo or latest version of gpt-4.1-yyyy-mm-dd. note that 3.5 is cheaper. see https://platform.openai.com/docs/pricing
classify_text <- function(text, model = "gpt-4.1-2025-04-14", retries = 3) {
  guidelines <- "
## Task:
Please read each text carefully and rate the overall sentiment of the manager's statement as positive or negative.
Your rating should reflect the manager’s expressed tone, not your judgment of the match.

## Rating Scale:

| **Score** | **Meaning** |
|----------|-------------|
| **2**    | Strongly positive sentiment |
| **1**    | Mildly positive sentiment |
| **0**    | Neutral or unclear sentiment |
| **-1**   | Mildly negative sentiment |
| **-2**   | Strongly negative sentiment |

Use **0** if unsure or mixed.
"
  prompt <- paste0(guidelines, '\nNow rate this manager statement:\n"""', text, '"""\nReply with only the integer score (e.g., 2 or -1).')
  key <- trimws(Sys.getenv("OPENAI_API_KEY"))
  
  for (i in 1:retries) {
    resp <- tryCatch({
      httr::POST(
        url = "https://api.openai.com/v1/chat/completions",
        httr::add_headers("Authorization" = paste("Bearer", key)),
        httr::content_type_json(),
        body = jsonlite::toJSON(list(
          model = model,
          messages = list(list(role = "user", content = prompt)),
          temperature = 0
        ), auto_unbox = TRUE)
      )
    }, error = function(e) NULL)
    
    if (!is.null(resp) && httr::status_code(resp) == 200) {
      raw_txt <- httr::content(resp, as = "text", encoding = "UTF-8")
      parsed <- tryCatch(jsonlite::fromJSON(raw_txt, simplifyVector = FALSE), error = function(e) NULL)
      
      if (!is.null(parsed) && !is.null(parsed$choices)) {
        val <- parsed$choices[[1]]$message$content
        score <- suppressWarnings(as.integer(trimws(val)))
        if (!is.na(score)) return(score)
      }
    }
    Sys.sleep(2 ^ (i - 1))  # exponential backoff
  }
  
  return(NA)
}

# test
classify_text(post_df$processed_tex[1])


# Add a progress bar
pb <- progress_bar$new(
  format = "  Classifying [:bar] :current/:total (:percent) in :elapsed",
  total = nrow(post_df), clear = FALSE, width = 60
)

results <- post_df %>%
  mutate(score = map_int(processed_tex, ~{
    pb$tick()
    classify_text(.x)
  }))


# Check for missing values
missing_scores <- results %>% filter(is.na(score))
if (nrow(missing_scores) > 0) {
  cat("Missing scores for the following texts:\n")
  print(missing_scores)
} else {
  cat("All texts classified successfully.\n")
}


write.csv(results, "manager_sentiment_results.csv", row.names = FALSE)

###x EXTRA
# run the code twice, save as ..results2 and compare


# read manager_sentiment_results.csv
results <- read.csv("manager_sentiment_results.csv")
results2 <-read.csv("manager_sentiment_results2.csv")

# Compare the two dataframes
comparison <- results %>%
  select(text_id, score) %>%
  inner_join(results2 %>% select(text_id, score), by = "text_id", suffix = c(".old", ".new")) %>%
  mutate(match = score.old == score.new)
# Check for mismatches
mismatches <- comparison %>% filter(!match)
if (nrow(mismatches) > 0) {
  cat("Mismatches found:\n")
  print(mismatches)
} else {
  cat("No mismatches found.\n")
}
# Save the comparison to a CSV file
write.csv(comparison, "sentiment_comparison.csv", row.names = FALSE)
