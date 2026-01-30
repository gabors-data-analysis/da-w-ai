# ==============================================================================
# SIMULATE EMPLOYEE COMMIT DATA - VERSION 3.0
# ==============================================================================
# Version: v3.0 - Improved DGP with realistic career progression
# Date: 2025-11-12
# 
# KEY CHANGES in v3.0:
# 1. Early career ramp-up: Productivity rises from 0-2 years
# 2. Smooth tenure distribution: Exponential decline (no cliff)
# 3. Late career decline: Marked drop after 7-8 years with many zeros
# 
# Iterations: 4 (v1.0 -> v2.0 -> v2.1 -> v3.0)
# Model: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)
# ==============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Set seed
np.random.seed(20251112)

# Parameters
N = 600
dept_split = {'IT': 0.60, 'Analytics': 0.40}

# ==============================================================================
# IMPROVED TENURE DISTRIBUTION (smooth decline, no cliff)
# ==============================================================================

print("\n=== GENERATING IMPROVED TENURE DISTRIBUTION ===\n")

# Use exponential distribution for natural decline
# Most people are new, fewer as tenure increases
mean_tenure_days = 1200  # Average around 3.3 years
days_with_company = np.random.exponential(mean_tenure_days, size=N)

# Cap at reasonable maximum (15 years) and minimum (1 day)
days_with_company = np.minimum(days_with_company, 5475)  # 15 years max
days_with_company = np.maximum(days_with_company, 1)     # 1 day min
days_with_company = days_with_company.astype(int)

print(f"Tenure distribution:")
print(f"  Mean: {days_with_company.mean():.0f} days ({days_with_company.mean()/365:.1f} years)")
print(f"  Median: {np.median(days_with_company):.0f} days ({np.median(days_with_company)/365:.1f} years)")
print(f"  >2000 days (5.5+ years): {(days_with_company > 2000).sum()} employees ({100*(days_with_company > 2000).mean():.1f}%)")

# Assign seniority based on tenure (for reference)
seniority = []
for days in days_with_company:
    if days < 730:
        seniority.append('Junior')
    elif days < 1825:
        seniority.append('Mid')
    else:
        seniority.append('Senior')

# Generate departments
depts = np.random.choice(
    list(dept_split.keys()), 
    size=N, 
    p=list(dept_split.values())
)

# Generate roles
roles = []
for dept, sen in zip(depts, seniority):
    if dept == 'IT':
        if sen == 'Senior':
            role = np.random.choice(['Developer', 'DevOps', 'Infrastructure'], p=[0.3, 0.3, 0.4])
        else:
            role = np.random.choice(['Developer', 'DevOps', 'Infrastructure'], p=[0.6, 0.3, 0.1])
    else:
        if sen == 'Senior':
            role = np.random.choice(['Data_Scientist', 'Analyst', 'Data_Engineer'], p=[0.4, 0.4, 0.2])
        else:
            role = np.random.choice(['Data_Scientist', 'Analyst', 'Data_Engineer'], p=[0.3, 0.4, 0.3])
    roles.append(role)

# ==============================================================================
# IMPROVED COMMIT GENERATION WITH CAREER PROGRESSION
# ==============================================================================

print("\n=== GENERATING COMMITS WITH CAREER PROGRESSION ===\n")

# Base monthly rates by role
base_monthly_rates = {
    'Developer': 35,
    'DevOps': 22,
    'Infrastructure': 7,
    'Data_Scientist': 26,
    'Analyst': 10,
    'Data_Engineer': 38
}

# Seniority multipliers (as before)
seniority_mult = {'Junior': 0.6, 'Mid': 1.2, 'Senior': 0.8}

monthly_commits = []

for i in range(N):
    x = days_with_company[i]
    base_rate = base_monthly_rates[roles[i]]
    sen_mult = seniority_mult[seniority[i]]
    
    # ==================================================================
    # NEW: TENURE-BASED PRODUCTIVITY CURVE
    # ==================================================================
    
    # 1. RAMP-UP PHASE (0-730 days / 0-2 years)
    #    Productivity rises from ~30% to 100%
    if x < 730:
        ramp_factor = 0.3 + 0.7 * (x / 730)  # 30% to 100%
    
    # 2. PEAK PHASE (730-2500 days / 2-6.8 years)
    #    Full productivity
    elif x < 2500:
        ramp_factor = 1.0
    
    # 3. DECLINE PHASE (2500+ days / 7+ years)
    #    Gradual decline as people move to leadership
    else:
        years_past_peak = (x - 2500) / 365
        # Decline by 12% per year, floor at 25%
        ramp_factor = max(0.25, 1.0 - 0.12 * years_past_peak)
    
    # Calculate expected rate with all multipliers
    adjusted_rate = base_rate * sen_mult * ramp_factor
    
    # Individual heterogeneity
    individual_effect = np.random.lognormal(0, 0.45)
    lambda_val = adjusted_rate * individual_effect
    
    # Generate commits (negative binomial)
    commit_count = np.random.negative_binomial(5, 5/(5+lambda_val))
    
    # ==================================================================
    # NEW: INCREASED ZERO PROBABILITY IN LATE CAREER
    # ==================================================================
    
    if x < 2500:
        zero_prob = 0.05  # Baseline 5%
    else:
        years_past_peak = (x - 2500) / 365
        # Increase probability by 7% per year after peak, cap at 35%
        zero_prob = min(0.35, 0.05 + 0.07 * years_past_peak)
    
    if np.random.random() < zero_prob:
        commit_count = 0
    
    monthly_commits.append(int(commit_count))

# ==============================================================================
# CREATE DATAFRAME
# ==============================================================================

df = pd.DataFrame({
    'i': [f'EMP_{str(i).zfill(4)}' for i in range(1, N+1)],
    'x': days_with_company,
    'y': monthly_commits,
    'department': depts,
    'seniority': seniority,
    'role': roles,
    'data_issue': 'CLEAN: No issues'
})

print(f"Generated {N} employees with realistic career progression")
print(f"  Early career (<2yr): mean commits = {df[df['x'] < 730]['y'].mean():.1f}")
print(f"  Peak career (2-7yr): mean commits = {df[(df['x'] >= 730) & (df['x'] < 2500)]['y'].mean():.1f}")
print(f"  Late career (7+yr): mean commits = {df[df['x'] >= 2500]['y'].mean():.1f}")
print(f"  Zeros in late career: {(df[df['x'] >= 2500]['y'] == 0).sum()}/{(df['x'] >= 2500).sum()} ({100*(df[df['x'] >= 2500]['y'] == 0).mean():.1f}%)")

# ==============================================================================
# ADD DATA QUALITY ISSUES (SAME AS v2.1)
# ==============================================================================

print("\n=== INJECTING DATA QUALITY ISSUES ===\n")

# ERROR 1: Negative commits (2 cases)
error_idx1 = np.random.choice(N, 2, replace=False)
df.loc[error_idx1, 'y'] = [-15, -8]
df.loc[error_idx1, 'data_issue'] = 'ERROR: Negative commits (data pipeline bug)'
print(f"Injected {len(error_idx1)} negative commit errors")

# ERROR 2: Impossibly high monthly commits (3 cases)
error_idx2 = np.random.choice([i for i in range(N) if i not in error_idx1], 3, replace=False)
df.loc[error_idx2, 'y'] = [8500, 12000, 6800]
df.loc[error_idx2, 'data_issue'] = 'ERROR: Impossibly high (decimal/aggregation error)'
print(f"Injected {len(error_idx2)} impossibly high commit errors")

# ERROR 3: Negative tenure (1 case)
error_idx3 = np.random.choice([i for i in range(N) if i not in list(error_idx1) + list(error_idx2)], 1)
df.loc[error_idx3, 'x'] = -120
df.loc[error_idx3, 'data_issue'] = 'ERROR: Negative tenure (date calculation error)'
print(f"Injected {len(error_idx3)} negative tenure error")

# ERROR 4: Impossibly long tenure (2 cases)
used_idx = list(error_idx1) + list(error_idx2) + list(error_idx3)
error_idx4 = np.random.choice([i for i in range(N) if i not in used_idx], 2, replace=False)
df.loc[error_idx4, 'x'] = [22000, 19500]
df.loc[error_idx4, 'data_issue'] = 'ERROR: Impossibly long tenure (date entry error)'
print(f"Injected {len(error_idx4)} impossibly long tenure errors")

# EXTREME 1: Very high monthly commits (30 cases, range 200-450)
used_idx = list(error_idx1) + list(error_idx2) + list(error_idx3) + list(error_idx4)
extreme_idx1 = np.random.choice([i for i in range(N) if i not in used_idx], 30, replace=False)
extreme_commits = np.random.uniform(200, 450, size=30).astype(int)
df.loc[extreme_idx1, 'y'] = extreme_commits
df.loc[extreme_idx1, 'data_issue'] = 'EXTREME: Very high commits (possible: bot-assisted or granular style)'
print(f"Injected {len(extreme_idx1)} very high commit extreme values (range 200-450)")

# EXTREME 2: Zero commits but long tenure (10 cases)
used_idx = used_idx + list(extreme_idx1)
candidates = df[(df['x'] > 2000) & (~df.index.isin(used_idx))].index
if len(candidates) >= 10:
    extreme_idx2 = np.random.choice(candidates, 10, replace=False)
else:
    extreme_idx2 = candidates
df.loc[extreme_idx2, 'y'] = 0
df.loc[extreme_idx2, 'data_issue'] = 'EXTREME: Zero commits, long tenure (real: moved to management)'
print(f"Injected {len(extreme_idx2)} zero commits with long tenure")

# EXTREME 3: High commits for junior (5 cases)
used_idx = used_idx + list(extreme_idx2)
candidates = df[(df['seniority'] == 'Junior') & (df['x'] < 365) & (~df.index.isin(used_idx))].index
if len(candidates) >= 5:
    extreme_idx3 = np.random.choice(candidates, 5, replace=False)
else:
    extreme_idx3 = candidates
extreme_junior_commits = np.random.uniform(150, 250, size=len(extreme_idx3)).astype(int)
df.loc[extreme_idx3, 'y'] = extreme_junior_commits
df.loc[extreme_idx3, 'data_issue'] = 'EXTREME: High commits for junior (real: internal transfer from other division)'
print(f"Injected {len(extreme_idx3)} high commits for junior employees")

# EXTREME 4: High commits for infrastructure (5 cases)
used_idx = used_idx + list(extreme_idx3)
candidates = df[(df['role'] == 'Infrastructure') & (~df.index.isin(used_idx))].index
if len(candidates) >= 5:
    extreme_idx4 = np.random.choice(candidates, 5, replace=False)
else:
    extreme_idx4 = candidates
extreme_infra_commits = np.random.uniform(70, 110, size=len(extreme_idx4)).astype(int)
df.loc[extreme_idx4, 'y'] = extreme_infra_commits
df.loc[extreme_idx4, 'data_issue'] = 'EXTREME: High for infrastructure (real: IaC enthusiast, everything in Git)'
print(f"Injected {len(extreme_idx4)} high commits for infrastructure roles")

# Add issue category
df['issue_category'] = df['data_issue'].apply(lambda x: 
    'Data Error' if x.startswith('ERROR') else 
    'Extreme Value' if x.startswith('EXTREME') else 
    'Clean'
)

# ==============================================================================
# SUMMARY STATISTICS
# ==============================================================================

print("\n=== DATASET SUMMARY (v3.0 WITH IMPROVED DGP) ===")
print(f"Total employees: {len(df)}\n")

print("Data quality breakdown:")
print(df['issue_category'].value_counts())

print("\nDepartment breakdown:")
print(df['department'].value_counts().sort_index())

print("\nSeniority breakdown:")
seniority_order = ['Junior', 'Mid', 'Senior']
print(df['seniority'].value_counts()[seniority_order])

print("\nDays with company (x) - INCLUDING ERRORS:")
print(df['x'].describe())

print("\nMonthly commits (y) - INCLUDING ERRORS:")
print(df['y'].describe())

print("\nDays with company (x) - CLEAN DATA ONLY:")
print(df[(df['x'] > 0) & (df['x'] < 10000)]['x'].describe())

print("\nMonthly commits (y) - CLEAN DATA ONLY:")
print(df[(df['y'] >= 0) & (df['y'] < 500)]['y'].describe())

# ==============================================================================
# SAVE DATA
# ==============================================================================

# Save FULL dataset with all columns (employee_commits_claude.csv)
df.to_csv('/home/claude/employee_commits_claude.csv', index=False)
print("\n✓ Full data saved to: employee_commits_claude.csv")

# Save RAW dataset (drop seniority, data_issue, issue_category)
df_raw = df.drop(columns=['seniority', 'data_issue', 'issue_category']).copy()
df_raw.to_csv('/home/claude/employee_commits_raw.csv', index=False)
print("✓ Raw data (minimal columns) saved to: employee_commits_raw.csv")

# Also save clean dataset (for comparison)
df_clean = df[df['issue_category'] == 'Clean'].copy()
df_clean.to_csv('/home/claude/employee_commits_clean.csv', index=False)
print("✓ Clean data saved to: employee_commits_clean.csv")

quality_report = df[df['issue_category'] != 'Clean'][['i', 'x', 'y', 'department', 'seniority', 'role', 'data_issue']].copy()
quality_report = quality_report.sort_values('data_issue')
quality_report.to_csv('/home/claude/data_quality_report.csv', index=False)
print("✓ Data quality report saved to: data_quality_report.csv")

# ==============================================================================
# VISUALIZATIONS
# ==============================================================================

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Plot 1: Tenure distribution (smooth decline)
axes[0, 0].hist(df[(df['x'] > 0) & (df['x'] < 6000)]['x'], bins=50, 
                color='#440154', alpha=0.7, edgecolor='black')
axes[0, 0].axvline(730, color='red', linestyle='--', linewidth=2, label='2 years')
axes[0, 0].axvline(2500, color='orange', linestyle='--', linewidth=2, label='7 years')
axes[0, 0].set_xlabel('Days with Company', fontsize=11)
axes[0, 0].set_ylabel('Count', fontsize=11)
axes[0, 0].set_title('Tenure Distribution (Smooth Exponential Decline)', fontsize=12, fontweight='bold')
axes[0, 0].legend()
axes[0, 0].grid(alpha=0.3, axis='y')

# Plot 2: Career progression curve (clean data)
df_clean_plot = df[df['issue_category'] == 'Clean']
df_clean_plot = df_clean_plot.sort_values('x')

# Calculate rolling median
window = 40
if len(df_clean_plot) >= window:
    rolling_median = df_clean_plot['y'].rolling(window=window, center=True).median()
    axes[0, 1].plot(df_clean_plot['x'], rolling_median, 'r-', linewidth=3, label='Median trend')

axes[0, 1].scatter(df_clean_plot['x'], df_clean_plot['y'], alpha=0.3, s=20, color='#31688e')
axes[0, 1].axvline(730, color='red', linestyle='--', alpha=0.5, label='2 years')
axes[0, 1].axvline(2500, color='orange', linestyle='--', alpha=0.5, label='7 years')
axes[0, 1].set_xlabel('Days with Company', fontsize=11)
axes[0, 1].set_ylabel('Monthly Commits', fontsize=11)
axes[0, 1].set_title('Career Progression Curve (Clean Data)', fontsize=12, fontweight='bold')
axes[0, 1].legend()
axes[0, 1].grid(alpha=0.3)

# Plot 3: Mean by career stage
career_stages = ['Early\n(0-2yr)', 'Peak\n(2-7yr)', 'Late\n(7+yr)']
stage_data = [
    df_clean_plot[df_clean_plot['x'] < 730]['y'].values,
    df_clean_plot[(df_clean_plot['x'] >= 730) & (df_clean_plot['x'] < 2500)]['y'].values,
    df_clean_plot[df_clean_plot['x'] >= 2500]['y'].values
]

bp = axes[1, 0].boxplot(stage_data, labels=career_stages, patch_artist=True)
colors = ['#440154', '#31688e', '#fde724']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)

# Add means as text
for i, data in enumerate(stage_data):
    if len(data) > 0:
        axes[1, 0].text(i+1, -5, f'μ={np.mean(data):.1f}\nn={len(data)}', 
                       ha='center', fontsize=9)

axes[1, 0].set_ylabel('Monthly Commits', fontsize=11)
axes[1, 0].set_title('Productivity by Career Stage', fontsize=12, fontweight='bold')
axes[1, 0].grid(alpha=0.3, axis='y')

# Plot 4: Zero commits over career
bins_x = np.linspace(0, 5000, 20)
zero_rate = []
bin_centers = []

for i in range(len(bins_x)-1):
    bin_data = df_clean_plot[(df_clean_plot['x'] >= bins_x[i]) & (df_clean_plot['x'] < bins_x[i+1])]
    if len(bin_data) > 0:
        zero_rate.append(100 * (bin_data['y'] == 0).mean())
        bin_centers.append((bins_x[i] + bins_x[i+1]) / 2)

axes[1, 1].plot(bin_centers, zero_rate, 'o-', linewidth=2, markersize=8, color='#35b779')
axes[1, 1].axvline(2500, color='orange', linestyle='--', linewidth=2, label='7 years')
axes[1, 1].set_xlabel('Days with Company', fontsize=11)
axes[1, 1].set_ylabel('% with Zero Commits', fontsize=11)
axes[1, 1].set_title('Zero Commits Rate by Tenure (Late Career Effect)', fontsize=12, fontweight='bold')
axes[1, 1].legend()
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('/home/claude/employee_commits_v3_plots.png', dpi=150, bbox_inches='tight')
print("✓ Plots saved to: employee_commits_v3_plots.png")

print("\n=== DATASET v3.0 READY ===")
print("Key improvements:")
print("1. ✓ Rising productivity in first 2 years (ramp-up)")
print("2. ✓ Smooth exponential tenure distribution (no cliff)")
print("3. ✓ Marked decline after 7 years with many zeros")
print("\n=== FILES CREATED ===")
print("1. employee_commits_claude.csv - Full dataset with all metadata")
print("2. employee_commits_raw.csv - Same data, minimal columns (i, x, y, department, role)")
print("3. employee_commits_clean.csv - Only clean observations")
print("4. data_quality_report.csv - List of all problematic cases")
