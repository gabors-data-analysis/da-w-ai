# WVS Cleaning & GDP Merge

**Version:** 1.1 (2025-05-25)  
**Course:** Data Analysis with AI (MA, BA)  
**Author:** Gábor’s Data Analysis (gabors-data-analysis.com)  

---

## Overview

This script cleans and subsets World Values Survey (WVS) Wave 7 data, generates a random subsample, aggregates by country & year, and merges with World Bank GDP indicators.

---

## Prerequisites
- Packages:  
  - **osfr** (download from OSF)  
  - **dplyr** (data manipulation)  
  - **readr** (CSV I/O)  
  - **WDI** (World Bank API)

---

## Directory Structure

```
project-root/
├─ data/
│  ├─ raw/        ← input CSVs
│  └─ clean/      ← outputs
└─ scripts/
   └─ cleaning.R ← this script
```

---

## Input

- `data/raw/WVS_Cross-National_Wave_7_csv_v6_0.csv`  
  Downloaded automatically from OSF (ID: 36dgb).

---

## Output

1. **WVS_subset.csv**  
   Selected variables and respondents, wave 1–7.
2. **WVS_random_subset2000.csv**  
   Random sample of 2 000 respondents (≈ per country).
3. **WVS_GDP_merged_data.csv**  
   Aggregated (mean & mode) by country & year for wave 7, merged with GDP & population (2017–2023).

---

## Processing Steps

1. **Setup**  
   - Clear environment (`rm(list=ls())`)  
   - Load libraries  
   - Define `data_in` and `data_out` folders

2. **Import & Subset**  
   - Download raw CSV via OSF  
   - Select key demographics (country codes, interview date, weights) and survey items (Q1–Q89, Q260–Q290)  
   - Save to `WVS_subset.csv`
   - Note: This file contains answers from all respondents from the data.

3. **Random Subsample**  
   - In this step, we create a random subsample to reduce sample size. 
   - Seed: `20250124`  
   - Sample ~2 000 respondents stratified by country  
   - Count the resulting number of respondents in each country
   - Save to `WVS_random_subset2000.csv`

4. **Aggregate & Clean**  
   - In this step, we aggregate the full data (step 2 data) to country-level, then join with GDP data.
   - Recode negative codes (`–1…–5`) to `NA`  
   - Count the number of respondents in each country
   - Compute country–year means for numeric items, modes for categorical  
   - Download GDP & population (2017–2023) via `WDI`  
   - Merge on ISO3 country code & year  
   - Save to `WVS_GDP_merged_data.csv`

---

## Usage

```sh
Rscript scripts/cleaning.R
```

Ensure your working directory is set to project root.  
Raw data and outputs will live under `data/raw` and `data/clean`.

---

---

## Contact

gabors-data-analysis.com | MA (BA) Data Analysis with AI course
