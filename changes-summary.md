# Changes Summary - Case Studies Reorganization

**Date:** 2026-01-30
**Session:** Reorganizing website structure from code/data to case-study-centric

---

## Additional Fixes (Round 2)

### Created Data/Code Subfolder Landing Pages

Added `index.qmd` to all data and code subfolders:

| Case Study | data/index.qmd | code/index.qmd |
|------------|----------------|----------------|
| austria-hotels | File list with download links | Placeholder |
| VWS | File list + external links | Links to cleaning.R |
| interviews | Primary data + sentiment files | R and Python scripts |
| earnings | CPS data + codebook | Links to earnings.R |
| employee_commits | CSV files + AI outputs | Placeholder |
| common-support-r | Notes simulated data | All 9 prompt files |

### Additional Link Fixes

| File | Change |
|------|--------|
| `resources.qmd` | Replaced old Data/Code sections with Case Studies listing |
| `week00/assets/creating-graphs.qmd` | Updated `/data/earnings/` link to `/case-studies/earnings/data/` |

---

## Overview

Restructured the `case-studies/` folder and website navigation to organize content by **case study** rather than by file type (code vs data). Each case study now has its own landing page with data, code, and documentation links.

---

## Folder Structure Changes

### Before
```
case-studies/
├── code/
│   ├── common-support-r/
│   ├── earnings/
│   └── interviews/
├── data/
│   ├── austria-hotels/
│   ├── earnings/
│   ├── employee_commits/
│   ├── interviews/
│   └── VWS/
├── index.qmd (code index)
└── data-index.qmd (data index)
```

### After
```
case-studies/
├── index.qmd (main landing page)
├── austria-hotels/
│   ├── index.qmd
│   ├── code/
│   ├── data/
│   └── exhibits/
├── common-support-r/
│   ├── index.qmd
│   ├── code/
│   ├── data/
│   └── exhibits/
├── earnings/
│   ├── index.qmd
│   ├── code/
│   ├── data/
│   └── exhibits/
├── employee_commits/
│   ├── index.qmd
│   ├── code/
│   ├── data/
│   └── exhibits/
├── interviews/
│   ├── index.qmd
│   ├── creating-code-sentiment-analysis.qmd
│   ├── code/
│   ├── data/
│   └── exhibits/
└── VWS/
    ├── index.qmd
    ├── code/
    ├── data/
    └── exhibits/
```

---

## Files Created

### Case Study Landing Pages
| File | Description |
|------|-------------|
| `case-studies/index.qmd` | Main case studies overview page |
| `case-studies/VWS/index.qmd` | World Values Survey case study |
| `case-studies/austria-hotels/index.qmd` | Austrian Hotels case study |
| `case-studies/interviews/index.qmd` | Football Manager Interviews case study |
| `case-studies/earnings/index.qmd` | US Earnings (CPS) case study |
| `case-studies/employee_commits/index.qmd` | Employee Commits case study |
| `case-studies/common-support-r/index.qmd` | Common Support R Analysis case study |

Each landing page includes:
- Overview and description
- Data files table with descriptions
- Code files table with descriptions
- Key features and learning objectives
- Direct download links
- Which weeks use this case study

---

## Files Modified

### Navigation (`_quarto.yml`)
- Added new "Case Studies" section in sidebar with links to all 6 case studies
- Removed old "Data" and "Code" links from Resources section

### Homepage and Weekly Overview
| File | Changes |
|------|---------|
| `index.qmd` | Updated 5 case study links to point to `/case-studies/` |
| `weeks.qmd` | Updated 5 case study links to point to `/case-studies/` |

### Weekly Content Pages
| File | Changes |
|------|---------|
| `week02/index.qmd` | Updated VWS data links to `/case-studies/VWS/` |
| `week03/index.qmd` | Updated VWS data links to `/case-studies/VWS/` |
| `week04/index.qmd` | Updated austria-hotels links to `/case-studies/austria-hotels/` |
| `week05/index.qmd` | Updated interviews/lexicon links to `/case-studies/interviews/` |
| `week06/index.qmd` | Updated interviews code links to `/case-studies/interviews/` |

### Assignments
| File | Changes |
|------|---------|
| `assignments/assignment_02.qmd` | Updated VWS codebook and data links |
| `assignments/assignment_05.qmd` | Updated interviews data link |

---

## Files Moved/Cleaned Up

| Action | File |
|--------|------|
| Moved | `VWS/data/cleaning.R` → `VWS/code/cleaning.R` |
| Moved | `creating-code-sentiment-analysis.qmd` → `interviews/` folder |
| Removed | Old `case-studies/index.qmd` (was code-only index) |
| Removed | Old `case-studies/data-index.qmd` |
| Removed | Redundant `index.qmd` files in data/code subfolders |

---

## Link Pattern Changes

### Old Pattern
```
/data/VWS/file.csv
/data/austria-hotels/file.csv
/data/interviews/file.xlsx
/code/interviews/script.R
```

### New Pattern
```
/case-studies/VWS/data/file.csv
/case-studies/austria-hotels/data/file.csv
/case-studies/interviews/data/file.xlsx
/case-studies/interviews/code/script.R
```

---

## Suggestions for Improvement

### 1. Add Exhibits Content
The `exhibits/` folders are currently empty. Consider adding:
- Sample output graphs and visualizations
- Example reports created with each dataset
- Screenshots of AI conversations/workflows
- Before/after comparisons

### 2. Create Data Download Packages
For each case study, create a downloadable ZIP containing:
- All data files
- README with quick start instructions
- Sample code snippet

### 3. Add Interactive Previews
Consider adding to each case study page:
- Data preview tables (first 10 rows)
- Variable summary statistics
- Interactive data dictionary

### 4. Cross-Reference Matrix
Create a reference table showing:
| Case Study | Weeks Used | Assignments | Key Skills |
|------------|------------|-------------|------------|
| VWS | 2, 3 | 2, 3 | Documentation, Reports |
| Austrian Hotels | 4 | 4 | Joins, Wrangling |
| Interviews | 5, 6 | 5, 6 | NLP, Sentiment, APIs |

### 5. Version Control for Data
Add version numbers or dates to datasets so students know if they have current versions.

### 6. Add Case Study Tags
Tag case studies by:
- Difficulty level (beginner, intermediate, advanced)
- Data type (survey, text, relational, time series)
- AI skills practiced (documentation, coding, analysis, NLP)

### 7. Student Showcase Section
Add a section for exemplary student work using each case study (with permission).

### 8. Expand Earnings and Employee Commits
These case studies have minimal documentation. Consider:
- Adding more detailed descriptions
- Creating code examples
- Linking to specific weeks if used

### 9. Add Quick Start Guides
For each case study, add a "5-minute quick start" section with:
- Minimal setup instructions
- One simple analysis to run
- Expected output

### 10. Consider Adding New Case Studies
Potential additions aligned with course content:
- SQL/database case study for Week 8
- Time series data for forecasting exercises
- Web scraping example dataset for Week 7

---

## Testing Checklist

After building the site, verify:
- [ ] All case study landing pages render correctly
- [ ] Navigation sidebar shows Case Studies section
- [ ] All data download links work
- [ ] All code file links work
- [ ] Week pages link correctly to case studies
- [ ] Assignment pages link correctly to case studies
- [ ] No 404 errors in browser console

---

## Notes

- Empty `code/`, `data/`, and `exhibits/` folders were created for all case studies to maintain consistent structure, even if currently unused
- The `README.md` in case-studies root was preserved
- Copy files (`index - Copy.qmd`) in week folders were not modified - consider cleaning these up separately
