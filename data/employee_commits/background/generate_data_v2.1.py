# ==============================================================================
# SIMULATE EMPLOYEE COMMIT DATA - PYTHON VERSION v2.1
# ==============================================================================
# Version: v2.1 - Increased extreme values to 50 cases
# Date: 2025-11-12
# Changes in v2.1:
# - 30 very high commits (200-450 range)
# - 10 zero commits with long tenure
# - 5 high commits for juniors
# - 5 high commits for infrastructure
# - Two output files: employee_commits_claude.csv (full) and employee_commits_raw.csv (minimal)
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
seniority_split = {'Junior': 0.35, 'Mid': 0.45, 'Senior': 0.20}

# Tenure ranges by seniority (days)
tenure_ranges = {
    'Junior': (1, 730),
    'Mid': (731, 1825),
    'Senior': (1826, 5475)
}

# MONTHLY commit rates by role (v2.0 change)
base_monthly_rates = {
    'Developer': 35,
    'DevOps': 22,
    'Infrastructure': 7,
    'Data_Scientist': 26,
    'Analyst': 10,
    'Data_Engineer': 38
}

# Seniority multipliers
seniority_mult = {'Junior': 0.6, 'Mid': 1.2, 'Senior': 0.8}

# ==============================================================================
# GENERATE BASE DATA
# ==============================================================================

# Generate departments
depts = np.random.choice(
    list(dept_split.keys()), 
    size=N, 
    p=list(dept_split.values())
)

# Generate seniority
seniority = np.random.choice(
    list(seniority_split.keys()),
    size=N,
    p=list(seniority_split.values())
)

# Generate days with company
days_with_company = []
for sen in seniority:
    range_min, range_max = tenure_ranges[sen]
    days = np.random.uniform(range_min, range_max)
    days_with_company.append(int(days))

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

# Generate MONTHLY commits (v2.0 change)
monthly_commits = []
for i in range(N):
    base_rate = base_monthly_rates[roles[i]]
    adjusted_rate = base_rate * seniority_mult[seniority[i]]
    
    # Individual heterogeneity (log-normal)
    individual_effect = np.random.lognormal(0, 0.45)
    lambda_val = adjusted_rate * individual_effect
    
    # Negative binomial for overdispersion
    commit_count = np.random.negative_binomial(5, 5/(5+lambda_val))
    
    # 5% have zero commits
    if np.random.random() < 0.05:
        commit_count = 0
    
    monthly_commits.append(int(commit_count))

# Create clean DataFrame
df = pd.DataFrame({
    'i': [f'EMP_{str(i).zfill(4)}' for i in range(1, N+1)],
    'x': days_with_company,
    'y': monthly_commits,
    'department': depts,
    'seniority': seniority,
    'role': roles,
    'data_issue': 'CLEAN: No issues'
})

# ==============================================================================
# ADD DATA QUALITY ISSUES
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

# EXTREME 1: Very high monthly commits (30 cases)
# Range: 200-450
used_idx = list(error_idx1) + list(error_idx2) + list(error_idx3) + list(error_idx4)
extreme_idx1 = np.random.choice([i for i in range(N) if i not in used_idx], 30, replace=False)
# Generate random values between 200 and 450
extreme_commits = np.random.uniform(200, 450, size=30).astype(int)
df.loc[extreme_idx1, 'y'] = extreme_commits
df.loc[extreme_idx1, 'data_issue'] = 'EXTREME: Very high commits (possible: bot-assisted or granular style)'
print(f"Injected {len(extreme_idx1)} very high commit extreme values (range 200-450)")

# EXTREME 2: Zero commits but long tenure (10 cases)
used_idx = used_idx + list(extreme_idx1)
candidates = df[(df['x'] > 1000) & (df['seniority'] == 'Senior') & (~df.index.isin(used_idx))].index
if len(candidates) >= 10:
    extreme_idx2 = np.random.choice(candidates, 10, replace=False)
else:
    # If not enough seniors, expand to mid-level with long tenure
    candidates = df[(df['x'] > 1500) & (~df.index.isin(used_idx))].index
    extreme_idx2 = np.random.choice(candidates, min(10, len(candidates)), replace=False)
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
# Generate values between 150-250 for juniors
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
# Generate values between 70-110 for infrastructure
extreme_infra_commits = np.random.uniform(70, 110, size=len(extreme_idx4)).astype(int)
df.loc[extreme_idx4, 'y'] = extreme_infra_commits
df.loc[extreme_idx4, 'data_issue'] = 'EXTREME: High for infrastructure (real: IaC enthusiast, everything in Git)'
print(f"Injected {len(extreme_idx4)} high commits for infrastructure roles")

# ==============================================================================
# SUMMARY STATISTICS
# ==============================================================================

print("\n=== DATASET SUMMARY (WITH DATA QUALITY ISSUES) ===")
print(f"Total employees: {len(df)}\n")

# Quality breakdown
df['issue_category'] = df['data_issue'].apply(lambda x: 
    'Data Error' if x.startswith('ERROR') else 
    'Extreme Value' if x.startswith('EXTREME') else 
    'Clean'
)

print("Data quality breakdown:")
print(df['issue_category'].value_counts())

print("\nSpecific issues:")
print(df['data_issue'].value_counts())

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

# Plot 1: Full view with issues highlighted
clean_data = df[df['issue_category'] == 'Clean']
error_data = df[df['issue_category'] == 'Data Error']
extreme_data = df[df['issue_category'] == 'Extreme Value']

for dept, color in zip(['IT', 'Analytics'], ['#440154', '#35b779']):
    dept_clean = clean_data[clean_data['department'] == dept]
    axes[0, 0].scatter(dept_clean['x'], dept_clean['y'], alpha=0.3, label=f'{dept} (clean)', 
                      color=color, s=20)

# Highlight issues
axes[0, 0].scatter(error_data['x'], error_data['y'], marker='x', s=150, 
                   color='red', linewidths=2, label='Data Errors', zorder=10)
axes[0, 0].scatter(extreme_data['x'], extreme_data['y'], marker='*', s=150,
                   color='orange', linewidths=1.5, label='Extreme Values', zorder=9)

axes[0, 0].set_xlabel('Days with Company', fontsize=11)
axes[0, 0].set_ylabel('Monthly Commits', fontsize=11)
axes[0, 0].set_title('Monthly Commits vs. Tenure (Data Quality Issues Highlighted)', fontsize=12, fontweight='bold')
axes[0, 0].legend(loc='upper left')
axes[0, 0].grid(alpha=0.3)

# Plot 2: Zoomed view (reasonable range)
df_zoom = df[(df['x'] > 0) & (df['x'] < 6000) & (df['y'] >= 0) & (df['y'] < 500)]
clean_zoom = df_zoom[df_zoom['issue_category'] == 'Clean']
extreme_zoom = df_zoom[df_zoom['issue_category'] == 'Extreme Value']

for dept, color in zip(['IT', 'Analytics'], ['#440154', '#35b779']):
    dept_data = clean_zoom[clean_zoom['department'] == dept]
    axes[0, 1].scatter(dept_data['x'], dept_data['y'], alpha=0.4, label=dept, 
                      color=color, s=30)

if len(extreme_zoom) > 0:
    axes[0, 1].scatter(extreme_zoom['x'], extreme_zoom['y'], marker='*', s=150,
                       color='orange', linewidths=1.5, label='Extreme Values', zorder=9)

axes[0, 1].set_xlabel('Days with Company', fontsize=11)
axes[0, 1].set_ylabel('Monthly Commits', fontsize=11)
axes[0, 1].set_title('Monthly Commits vs. Tenure (Reasonable Range)', fontsize=12, fontweight='bold')
axes[0, 1].legend()
axes[0, 1].grid(alpha=0.3)

# Plot 3: Distribution of monthly commits
df_dist = df[(df['y'] >= 0) & (df['y'] < 500)]
for dept, color in zip(['IT', 'Analytics'], ['#440154', '#35b779']):
    dept_data = df_dist[df_dist['department'] == dept]['y']
    axes[1, 0].hist(dept_data, bins=40, alpha=0.6, label=dept, color=color)

axes[1, 0].axvline(df_dist['y'].median(), color='red', linestyle='--', linewidth=2, 
                   label=f'Median: {df_dist["y"].median():.0f}')
axes[1, 0].set_xlabel('Monthly Commits', fontsize=11)
axes[1, 0].set_ylabel('Count', fontsize=11)
axes[1, 0].set_title('Distribution of Monthly Commits (Clean Range)', fontsize=12, fontweight='bold')
axes[1, 0].legend()
axes[1, 0].grid(alpha=0.3, axis='y')

# Plot 4: Boxplot by role (clean data only)
df_box = df[(df['y'] >= 0) & (df['y'] < 500) & (df['issue_category'] == 'Clean')]
roles_order = sorted(df_box['role'].unique())
data_by_role = [df_box[df_box['role'] == r]['y'].values for r in roles_order]

bp = axes[1, 1].boxplot(data_by_role, labels=roles_order, patch_artist=True)
colors = plt.cm.viridis(np.linspace(0, 0.9, len(roles_order)))
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)

axes[1, 1].set_xlabel('Role', fontsize=11)
axes[1, 1].set_ylabel('Monthly Commits', fontsize=11)
axes[1, 1].set_title('Monthly Commits by Role (Clean Data)', fontsize=12, fontweight='bold')
axes[1, 1].tick_params(axis='x', rotation=45)
axes[1, 1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('/home/claude/employee_commits_v2_plots.png', dpi=150, bbox_inches='tight')
print("✓ Plots saved to: employee_commits_v2_plots.png")

# ==============================================================================
# SHOW EXAMPLES
# ==============================================================================

print("\n=== EXAMPLES OF DATA QUALITY ISSUES ===\n")

print("DATA ERRORS (Must be fixed or excluded):")
print(df[df['issue_category'] == 'Data Error'][['i', 'x', 'y', 'role', 'data_issue']].head(10))

print("\n\nEXTREME VALUES (Require analyst judgment):")
print(df[df['issue_category'] == 'Extreme Value'][['i', 'x', 'y', 'role', 'seniority', 'data_issue']].head(10))

print("\n\nNormal cases for comparison:")
print(df[df['issue_category'] == 'Clean'].sample(5)[['i', 'x', 'y', 'department', 'seniority', 'role']])

print("\n=== DATASET READY FOR TEACHING ===")
print("Students can now explore:")
print("1. How to identify data errors vs extreme values")
print("2. What cleaning decisions to make")
print("3. How different cleaning choices affect the x-y relationship")
print("4. Multiple modeling approaches for count data")
print("\n=== FILES CREATED ===")
print("1. employee_commits_claude.csv - Full dataset with all metadata")
print("2. employee_commits_raw.csv - Same data, minimal columns (i, x, y, department, role)")
print("3. employee_commits_clean.csv - Only clean observations")
print("4. data_quality_report.csv - List of all problematic cases")
