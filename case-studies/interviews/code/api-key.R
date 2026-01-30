# API key -- first time use
# you must add your key to "api-key.R" and save it as "my-openai-api-key.R" add it to gitignore


# replace your key here
Sys.setenv(OPENAI_API_KEY = "sk-....")

cat("Key length:", nchar(Sys.getenv("OPENAI_API_KEY")), "\n")

key <- trimws(Sys.getenv("OPENAI_API_KEY"))

resp <- httr::POST(
  url = "https://api.openai.com/v1/chat/completions",
  httr::add_headers("Authorization" = paste("Bearer", key)),
  httr::content_type_json(),
  body = jsonlite::toJSON(list(
    model = "gpt-4",
    messages = list(list(role = "user", content = "Reply with 1")),
    temperature = 0
  ), auto_unbox = TRUE)
)

cat(httr::content(resp, as = "text", encoding = "UTF-8"))
