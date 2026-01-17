# Employee Commits Dataset v3.0 - Complete Summary

**Version**: 3.0 (RECOMMENDED VERSION)  
**Date**: 2025-11-12  
**Iterations**: 4 (v1.0 → v2.0 → v2.1 → v3.0)  
**Model**: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)

---

## What's New in v3.0 - KEY IMPROVEMENTS

### 1. ✅ **Rising Productivity in First 2 Years** (Ramp-Up)
- Early career (0-2yr): Mean = 9.7 commits/month
- Productivity increases from ~30% to 100% over first 730 days
- **Pattern**: People are learning, ramping up skills

### 2. ✅ **Smooth Tenure Distribution** (No Cliff!)
- Exponential distribution: Most people have low tenure
- Natural decline: 148 employees <1yr, 112 at 1-2yr, 167 at 2-5yr, 115 at 5+yr
- **Pattern**: Realistic employee turnover and retention

### 3. ✅ **Marked Decline After 7-8 Years**
- Late career (7+yr): Mean = 8.7 commits/month (lower than early career!)
- Zero commits: 19.8% of employees with 7+ years (vs 5% baseline)
- **Pattern**: Move to management, mentoring, architecture roles

---

## The X-Y Relationship: Now MUCH Clearer!

### Overall Statistics (Clean Data, N=542)

**Correlations:**
- Pearson (linear): r = 0.019 (still weak in linear sense)
- Spearman (rank): r = 0.190 (p < 0.0001, **significant!**)

**Key Insight**: The relationship is **non-linear** and **non-monotonic**!

### The Career Progression Curve

| Career Stage | Tenure | Mean | Median | N | Pattern |
|--------------|--------|------|--------|---|---------|
| **Early** (Learning) | 0-1 year | 7.4 | 5.5 | 148 | Low (ramping up) |
| **Growing** (Maturing) | 1-2 years | 13.0 | 10.5 | 112 | Rising (learning curve) |
| **Peak** (Full productivity) | 2-5 years | **32.0** | **24.0** | 167 | **Maximum** (IC contributors) |
| **Late** (Leadership) | 5+ years | 10.3 | 7.0 | 115 | Declining (management) |

**Peak is 4.3x higher than early career!**  
**Late career drops back to early levels!**

### Statistical Significance

**ANOVA for Seniority Effect:**
- F-statistic: 93.66
- p-value: < 0.0001
- **Result**: Highly significant differences across career stages

**The evidence is overwhelming that career stage matters!**

---

## Visualizations Show Clear Patterns

### Panel 1: Tenure Distribution (Top Left)
- Smooth exponential decline (no cliff at 2000 days)
- Most employees concentrated in 0-2000 day range
- Natural thinning as tenure increases

### Panel 2: Career Progression Curve (Top Right)
**RED MEDIAN TREND LINE shows:**
1. **Rise** from 0 to ~1000 days (0-3 years)
2. **Peak** around 1000-2000 days (3-5 years)  
3. **Decline** after 2500 days (7+ years)
4. **Low plateau** after 3500+ days (10+ years)

This is the **inverted-U pattern** that students should discover!

### Panel 3: Productivity by Career Stage (Bottom Left)
Boxplots dramatically show:
- Early: Median ~5, tight distribution
- Peak: Median ~24, wide distribution (high variance)
- Late: Median ~7, back down to early levels

### Panel 4: Zero Commits Rate (Bottom Right)
**The "management transition" effect:**
- Stable ~5-15% for first 2500 days
- **Spike to 30-50%** after 2500 days (7 years)
- Shows clear transition from coding to leadership

---

## Why This is the BEST Teaching Dataset

### 1. **Realistic Career Arc**
This pattern matches real-world phenomena:
- Academic research output (inverted-U with age)
- Sports performance (peak then decline)
- Software engineering (senior devs code less)
- Management transitions (IC → people leadership)

### 2. **Multiple Valid Analysis Approaches**

Students can explore:

**Linear approaches:**
- Simple OLS: R² ≈ 0 (fails completely)
- With group dummies: R² ≈ 0.25 (much better!)

**Non-linear approaches:**
- Polynomial regression (quadratic or cubic)
- Splines (natural or smoothing splines)
- GAM (generalized additive models)
- Locally weighted regression (LOESS)

**Count data approaches:**
- Poisson regression
- Negative binomial (handles overdispersion)
- Zero-inflated models (for late-career zeros)

**Group-based approaches:**
- ANOVA / linear model with tenure groups
- Separate models by career stage
- Mixed effects with random slopes

### 3. **Forces Critical Thinking**

Questions students must grapple with:
- Why does simple linear regression fail?
- How do we model non-monotonic relationships?
- When to use continuous vs categorical predictors?
- How to interpret "no linear relationship" vs "no relationship"?

### 4. **Data Quality Challenges**

Still includes 58 problematic cases (8 errors + 50 extreme values):
- Students must clean data first
- Different cleaning decisions affect results
- Teaches importance of documentation

---

## Key Statistics Summary

### Tenure Distribution (Clean Data)
- Mean: 1,162 days (3.2 years)
- Median: 788 days (2.2 years)
- Range: 1 to 5,475 days (0 to 15 years)
- Most employees: 0-2000 days (70%)

### Commits Distribution (Clean Data)
- Mean: 16.8 commits/month
- Median: 10.0 commits/month (right-skewed!)
- Range: 0 to 119 commits/month
- Zero commits: 50 cases (9.2%)

### By Department (Clean Data)
- IT: Mean = 18.0, Median = 12.0 (n=307)
- Analytics: Mean = 15.1, Median = 9.0 (n=235)
- Difference: Not statistically significant (p=0.09)

### Data Quality Issues
- 8 errors (must fix): negative values, impossibly high/long
- 50 extreme values (analyst judgment): very high commits, zeros with long tenure
- 542 clean observations (90.3%)

---

## Files Provided (v3.0)

### Main Data Files

1. **employee_commits_claude_v3.csv** (600 rows)
   - Full dataset with metadata
   - Columns: i, x, y, department, seniority, role, data_issue, issue_category
   - **Use for**: Teaching with answer key

2. **employee_commits_raw_v3.csv** (600 rows)
   - Minimal dataset (i, x, y, department, role only)
   - **Use for**: Give to students first (discovery learning)

3. **employee_commits_clean_v3.csv** (542 rows)
   - Only clean observations
   - **Use for**: Analysis after cleaning or skip cleaning exercise

4. **data_quality_report_v3.csv** (58 rows)
   - List of all problematic cases
   - **Use for**: Answer key for data cleaning

### Visualization Files

5. **employee_commits_v3_plots.png**
   - Shows DGP features: ramp-up, peak, decline, zeros
   - 4 panels demonstrating career progression

6. **xy_relationship_analysis_v3.png**
   - Comprehensive 8-panel analysis
   - Shows relationship from multiple angles
   - Includes residual diagnostics

### Code Files

7. **generate_data_v3.py**
   - Complete data generation code
   - Fully commented and reproducible
   - Change seed or parameters as needed

8. **analyze_xy_relationship_v3.py**
   - Relationship analysis script
   - Creates 8-panel visualization
   - Statistical tests included

---

## Teaching Workflow (Recommended)

### Stage 1: Discovery (Raw Data)
1. Give students `employee_commits_raw_v3.csv`
2. Ask: "What is the relationship between x and y?"
3. Let them explore, visualize, analyze
4. They should discover the non-linear pattern!

### Stage 2: Data Quality
1. Ask: "Are there any data quality issues?"
2. Students identify errors and extreme values
3. Make and document cleaning decisions
4. Compare with `data_quality_report_v3.csv`

### Stage 3: Multiple Models
1. Try various modeling approaches
2. Compare: OLS, polynomials, splines, groups, etc.
3. Evaluate which model best captures the pattern
4. Discuss trade-offs (interpretability vs fit)

### Stage 4: Interpretation
1. What is the relationship between tenure and commits?
2. Why is it non-monotonic?
3. What does this tell us about career progression?
4. How would you communicate findings to stakeholders?

---

## Key Teaching Points

### 1. Linear Models Can Miss Important Patterns
- r ≈ 0 doesn't mean "no relationship"
- It means "no *linear* relationship"
- Always visualize first!

### 2. Non-Monotonic Relationships Are Common
- Not everything increases or decreases monotonically
- Career arcs, learning curves, life cycles all have peaks
- Need appropriate modeling approaches

### 3. Group-Based Analysis Often Better
- Categorical predictors (seniority) explain more than continuous (days)
- Domain knowledge helps create meaningful groups
- Sometimes simpler is better (interpretability)

### 4. Count Data Has Special Properties
- Discrete, non-negative, right-skewed
- Poisson/NB often better than OLS
- Zero-inflation is a real phenomenon

### 5. Context Matters
- The inverted-U makes perfect sense for careers
- Early: learning and ramping up
- Peak: full IC productivity  
- Late: transitioning to leadership
- **Domain knowledge guides modeling choices**

---

## Comparison: v2.1 vs v3.0

| Feature | v2.1 | v3.0 | Impact |
|---------|------|------|--------|
| Early career | Flat/low | **Rising** | More realistic learning curve |
| Tenure distribution | Hard cutoffs | **Smooth exponential** | No artificial cliff |
| Late career | Moderate decline | **Marked decline + zeros** | Clear management transition |
| X-Y correlation | -0.005 | 0.019 | Slightly positive (better) |
| Spearman correlation | 0.120 | **0.190** | Stronger non-linear signal |
| Seniority F-stat | 35.5 | **93.7** | Much stronger group effects |
| Pedagogical clarity | Good | **Excellent** | Pattern unmistakable |

**v3.0 is the recommended version for teaching!**

---

## Extensions and Variations

### Easy Modifications (change in generate_data_v3.py):

1. **Different ramp-up speed**: Change `x/730` factor
2. **Earlier/later peak**: Adjust 2500 day threshold
3. **Steeper decline**: Increase 0.12 decline factor
4. **More zeros**: Increase 0.07 probability increment
5. **Different roles**: Modify base_monthly_rates
6. **More departments**: Add to dept_split

### Advanced Extensions:

1. **Time series**: Multiple observations per employee
2. **Team effects**: Add team ID with random effects
3. **Project complexity**: Add covariate affecting commits
4. **Turnover**: Some employees leave (censoring)
5. **Promotions**: Explicit seniority changes over time

---

## Technical Details

### DGP Specifications (v3.0)

**Tenure Distribution:**
```
days_with_company ~ Exponential(mean=1200)
Truncated: [1, 5475] days
```

**Productivity Function:**
```
ramp_factor = {
  0.3 + 0.7*(x/730)           if x < 730
  1.0                          if 730 ≤ x < 2500
  max(0.25, 1.0 - 0.12*years)  if x ≥ 2500
}

lambda = base_rate × seniority_mult × ramp_factor × individual_effect
y ~ NegativeBinomial(mu=lambda, size=5)
```

**Zero Inflation:**
```
P(y=0) = {
  0.05                           if x < 2500
  min(0.35, 0.05 + 0.07*years)  if x ≥ 2500
}
```

### Random Seed
`np.random.seed(20251112)` - fully reproducible

### Software Requirements
- Python 3.x
- numpy, pandas, matplotlib, scipy, sklearn

---

## Bottom Line

**v3.0 creates a realistic dataset that:**

✅ Shows clear non-monotonic career progression  
✅ Challenges students' intuitions about linearity  
✅ Requires sophisticated thinking about modeling  
✅ Reflects real-world career dynamics  
✅ Provides rich opportunities for exploration  
✅ Has no single "right" answer (by design)  
✅ Teaches both technical skills and critical thinking  

**Perfect for teaching "What is the relationship between x and y?"**

---

## Quick Start

1. Give students: `employee_commits_raw_v3.csv`
2. Ask: "What is the relationship between tenure (x) and monthly commits (y)?"
3. Let them explore and struggle (this is where learning happens!)
4. Reveal patterns using: `employee_commits_v3_plots.png` and `xy_relationship_analysis_v3.png`
5. Discuss: Why did simple approaches fail? What models work better?

**Welcome to the wonderful world of non-linear relationships!**
