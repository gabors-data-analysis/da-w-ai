# Employee Commits Dataset v2.1 - Summary

**Version**: 2.1  
**Date**: 2025-11-12  
**Iterations**: 3 (v1.0 -> v2.0 -> v2.1)
**Model**: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)

---

## What Changed in v2.1

**Increased extreme values from 10 to 50:**
- 30 very high commits (range: 200-450/month) — up from 3
- 10 zero commits with long tenure — up from 3
- 5 high commits for juniors — up from 2
- 5 high commits for infrastructure — up from 2

**Data errors remain at 8** (unchanged from v2.0)

**Total problematic cases: 58** (8 errors + 50 extreme values)
**Clean observations: 542**
**Total: 600 employees**

---

## Files Provided

### 1. employee_commits_claude.csv
**Full dataset with all metadata (600 rows × 8 columns)**

Columns:
- `i` - Employee ID
- `x` - Days with company
- `y` - Monthly commits
- `department` - IT or Analytics
- `seniority` - Junior, Mid, Senior
- `role` - Specific job role
- `data_issue` - Description of any quality issues
- `issue_category` - Clean, Data Error, or Extreme Value

Use this for teaching data quality and cleaning decisions.

### 2. employee_commits_raw.csv
**Minimal dataset (600 rows × 5 columns)**

Columns:
- `i` - Employee ID
- `x` - Days with company
- `y` - Monthly commits
- `department` - IT or Analytics
- `role` - Specific job role

**Dropped columns**: seniority, data_issue, issue_category

Use this as the "raw data" students receive before they know about issues.

### 3. employee_commits_clean.csv
**Only clean observations (542 rows)**

All 8 data errors and 50 extreme values removed.
Use for comparison or to skip the cleaning exercise.

### 4. data_quality_report.csv
**List of all 58 problematic cases**

Shows each issue with employee ID, x, y, and explanation.
Use as an answer key or for discussion.

### 5. employee_commits_v2_plots.png
**Diagnostic visualizations**

Four panels showing data quality issues highlighted:
- Full view with errors (X) and extreme values (★)
- Zoomed view focusing on reasonable range
- Distribution of monthly commits
- Boxplots by role

---

## Data Quality Issues Breakdown

### Data Errors (8 cases) - Must Fix

| Issue Type | Count | Range | Story |
|------------|-------|-------|-------|
| Negative commits | 2 | -15, -8 | Data pipeline bug |
| Impossibly high commits | 3 | 6,800 - 12,000 | Decimal/aggregation error |
| Negative tenure | 1 | -120 days | Date calculation error |
| Impossibly long tenure | 2 | 19,500 - 22,000 days | Date entry error (1925 vs 2025) |

### Extreme Values (50 cases) - Require Judgment

| Issue Type | Count | Range | Story | Keep or Drop? |
|------------|-------|-------|-------|---------------|
| Very high commits | 30 | 200 - 450/month | Bot-assisted or granular style | Analyst choice |
| Zero commits, long tenure | 10 | x > 2,900 days | Moved to management | Analyst choice |
| High commits for junior | 5 | 154 - 248/month | Internal transfers | Analyst choice |
| High for infrastructure | 5 | 75 - 108/month | IaC enthusiasts | Analyst choice |

---

## Key Statistics

### Full Dataset (including issues)
- **x**: Mean = 1,496 days, Min = -120, Max = 22,000
- **y**: Mean = 87, Min = -15, Max = 12,000

### Clean Data Only (542 obs)
- **x**: Mean = 1,434 days (3.9 years), Range = 3 to 5,446
- **y**: Median = 18, Mean = 42, Range = 0 to 445

### With Extreme Values Removed (542 obs)
- **y**: Median = 15, Mean = 27, Range = 0 to 150 (approximately)

---

## Teaching Questions

### Level 1: Data Quality
1. Identify which observations are clearly errors vs possibly valid
2. What's your decision rule for each type of extreme value?
3. Document the impact of including vs excluding extreme values

### Level 2: Exploration
1. Visualize the relationship between x and y
2. How does it differ by department? By role?
3. Is the relationship linear? Log-linear? Something else?

### Level 3: Modeling
1. Compare multiple approaches:
   - Linear regression (OLS)
   - Log transformations
   - Poisson regression
   - Negative binomial regression
   - Robust regression (M-estimators)
   - Quantile regression (median)
   
2. Which model assumptions are violated and why?
3. How sensitive are results to data cleaning decisions?

### Level 4: Communication
1. What's your conclusion about the x-y relationship?
2. How certain are you? What are the caveats?
3. What additional data would help?
4. How would you report this to a non-technical stakeholder?

---

## Suggested Workflow for Students

**Stage 1: Initial Exploration**
- Load `employee_commits_raw.csv`
- Create basic visualizations
- Calculate summary statistics
- Notice anything unusual?

**Stage 2: Data Quality Assessment**
- Identify outliers and unusual values
- Categorize as errors vs extreme values
- Make cleaning decisions with justification

**Stage 3: Multiple Analyses**
- Try 3-4 different cleaning approaches
- For each: visualize, model, interpret
- Compare results across approaches

**Stage 4: Synthesis**
- Which approach do you recommend and why?
- What is the relationship between x and y?
- How confident are you in this conclusion?

---

## Instructor Notes

### Why This Dataset Works

1. **Realistic complexity**: Not obviously clean or dirty
2. **Ambiguity**: No single "correct" answer for extreme values
3. **Multiple valid approaches**: Forces critical thinking
4. **Count data features**: Overdispersion, zeros, skewness
5. **Rich metadata**: Can explore heterogeneity

### Discussion Points

- **Error vs extreme**: What makes something an error vs just unusual?
- **Decision rules**: How do you decide what to keep/drop?
- **Transparency**: How do you document cleaning decisions?
- **Sensitivity**: When do conclusions change materially?
- **Model choice**: Why prefer one model over another for count data?

### Extensions

1. Add time dimension (multiple months per employee)
2. Include team/project identifiers for clustering
3. Add more covariates (education, experience, etc.)
4. Create a prediction task (predict commits for new employees)

---

## Technical Details

**Seed**: 20251112  
**Software**: Python 3.x with numpy, pandas, matplotlib  
**Also available**: R version (simulate_employee_commits_v2.R)

**Key assumptions**:
- Base monthly rates by role (7-38 commits/month)
- Seniority multipliers (0.6x, 1.2x, 0.8x)
- Individual heterogeneity (log-normal, σ=0.45)
- Negative binomial distribution (size=5)
- 5% baseline zeros (moved teams, admin roles, etc.)

---

For questions or modifications, see `generate_data_v2.1.py`
