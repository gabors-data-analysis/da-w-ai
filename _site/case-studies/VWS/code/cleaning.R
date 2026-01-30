#########################################################################################
# Prepared for Data Analysis with AI - MA course
#
# gabors-data-analysis.com 
#
# License: Free to share, modify and use for educational purposes. 
#   Not to be used for commercial purposes.
# version 1.1 2025-01-24
#########################################################################################
#
# WVS cleaning
# input:
# WVS_Cross-National_Wave_7_csv_v6_0.csv
#
# output:
# WVS_subset.csv
# WVS_random_subset.csv
# WVS_GDP_merged_data.csv
#
#########################################################################################

# Clear memory 
rm(list = ls())

# Libraries
library(osfr)   # To handle Open Science Framework (OSF) file operations
library(dplyr)  # For data manipulation
library(readr)  # For reading and writing CSV files 
library(WDI)    # For loading World Bank data


# Set working directory, and input-output folders
setwd("~/Dropbox/bekes-kezdi-2nd-edition-shared/input-vadle/da-w-ai/teaching")
data_in <- "data/raw/"
data_out <- "data/clean/"

#### IMPORT AND PREPARE DATA ####

##### Importing #####
# Download the file from OSF and store it in the input folder
osf <- osf_retrieve_file("36dgb") %>% 
  osf_download(path = data_in, conflicts = "overwrite")

# Load the raw data from the downloaded file into a tibble
raw_data <- read.csv(osf$local_path)

##### Preparing #####
# Select a subset of variables from the raw data
subset_data <- raw_data %>%
  select(
    B_COUNTRY, B_COUNTRY_ALPHA, C_COW_NUM, C_COW_ALPHA, D_INTERVIEW, A_YEAR, 
    S025, A_STUDY, A_WAVE, W_WEIGHT, S018, Q1:Q89, Q260:Q290
  )

# Save into a csv 
write.csv(subset_data, paste0(data_out, "WVS_subset.csv"), row.names = FALSE)

#### Create random subsample ####
# Set Seed
set.seed(20250124)

# Create a random subsample grouped by country
rand_subset_data <- subset_data %>%
  group_by(B_COUNTRY) %>%  # Group data by country
  sample_frac(size = 2000 / nrow(subset_data)) %>%  # Sample a fraction of rows for each group, we want to get n=2000
  mutate(n_respondent= n()) %>%
  ungroup()  # Remove grouping after sampling

# Save into a csv
write.csv(rand_subset_data, paste0(data_out, "WVS_random_subset2000.csv"), row.names = FALSE)

#### Create aggregate subset merged with GDP data ####
## Subset and aggregate
# Clean the data for the latest wave and code negative values as missing
subset_data_clean <- subset_data %>%
  filter(A_WAVE == 7) %>%  # Filter rows for wave 7
  select(
    B_COUNTRY, B_COUNTRY_ALPHA, C_COW_NUM, C_COW_ALPHA, D_INTERVIEW, A_YEAR, 
    S025, A_STUDY, A_WAVE, W_WEIGHT, S018,
    names(subset_data)[grep("^Q\\d+$", names(subset_data))] # We select variables starting with Q - these are the vars of interest
  ) %>%
  mutate(across(starts_with("Q"), ~ na_if(., -5))) %>%  # E.g.: Replace -5 with NA for variables starting with "Q"
  mutate(across(starts_with("Q"), ~ na_if(., -4))) %>%  
  mutate(across(starts_with("Q"), ~ na_if(., -3))) %>%  
  mutate(across(starts_with("Q"), ~ na_if(., -2))) %>%  
  mutate(across(starts_with("Q"), ~ na_if(., -1))) %>%  
  group_by(B_COUNTRY) %>%  # Group data by country
  mutate(n_respondent= n()) %>%
  ungroup()  


# Aggregate data by country and year
# select vars for aggregation
data_for_aggr <- subset_data_clean %>%
  select( B_COUNTRY_ALPHA, D_INTERVIEW, A_YEAR, Q1:Q89, n_respondent
  )

# def numeric and categorical columns 
num_cols <- paste0("Q", 1:89)
cat_cols <- setdiff(names(data_for_aggr), c(num_cols, "B_COUNTRY_ALPHA", "D_INTERVIEW", "A_YEAR", "n_respondent")) 

# aaggregation on the reduced dataset
aggregated_data <- data_for_aggr %>%
  group_by(B_COUNTRY_ALPHA, A_YEAR) %>%
  summarise(
    across(all_of(num_cols), ~ mean(.x, na.rm = TRUE)),
    across(all_of(cat_cols), ~ names(which.max(table(.x, useNA = "no")))),
    .groups = "drop"
  )

colSums(is.na(aggregated_data))

## Merge with GDP
# Import GDP data from World Bank
gdp_data <- WDI(country = "all", 
                indicators <- c(
                  GDP_USD = "NY.GDP.MKTP.CD",
                  GDP_USD_PPP = "NY.GDP.MKTP.PP.CD",
                  GDP_USD_PPP_per_capita = "NY.GDP.PCAP.PP.CD",
                  Population = "SP.POP.TOTL"
                ),
                start = 2017, end = 2023,  # Year range to match survey years
                extra = TRUE)

# Keep only relevant columns in GDP data 
gdp_data <- gdp_data %>%
  select(iso3c, year, GDP_USD, GDP_USD_PPP, GDP_USD_PPP_per_capita, Population)  # 

# Merge aggregated data with GDP data by country and year (as year of survey varies even though it is the same wave!)
merged_data <- aggregated_data %>%
  left_join(gdp_data, by = c("B_COUNTRY_ALPHA" = "iso3c", "A_YEAR" = "year"), keep =T)

# Save 
write.csv(merged_data, paste0(data_out, "WVS_GDP_merged_data.csv"), row.names = FALSE)


