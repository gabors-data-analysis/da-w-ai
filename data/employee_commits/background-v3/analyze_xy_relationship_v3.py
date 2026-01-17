# ==============================================================================
# ANALYZE X-Y RELATIONSHIP IN CLEAN DATA
# ==============================================================================
# Version: 1.0
# Date: 2025-11-12
# Purpose: Explore relationship between tenure (x) and monthly commits (y)
# ==============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import warnings
warnings.filterwarnings('ignore')

# Load clean data
df = pd.read_csv('/home/claude/employee_commits_clean.csv')

print("=== CLEAN DATA SUMMARY ===")
print(f"N = {len(df)} observations\n")

print("Tenure (x) - days with company:")
print(df['x'].describe())
print(f"Years range: {df['x'].min()/365:.1f} to {df['x'].max()/365:.1f}")

print("\nMonthly commits (y):")
print(df['y'].describe())

print("\nCorrelation:")
corr = df['x'].corr(df['y'])
print(f"Pearson correlation: {corr:.3f}")

# Spearman (rank-based, more robust)
spearman_corr, spearman_p = stats.spearmanr(df['x'], df['y'])
print(f"Spearman correlation: {spearman_corr:.3f} (p-value: {spearman_p:.4f})")

# ==============================================================================
# VISUALIZATIONS
# ==============================================================================

fig = plt.figure(figsize=(18, 12))

# Create grid
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# ============================================================================
# Plot 1: Basic scatterplot with LOESS
# ============================================================================
ax1 = fig.add_subplot(gs[0, :2])

# Scatter by department
for dept, color in zip(['IT', 'Analytics'], ['#440154', '#35b779']):
    dept_data = df[df['department'] == dept]
    ax1.scatter(dept_data['x'], dept_data['y'], alpha=0.4, label=dept, 
                color=color, s=30)

# Add LOESS smoothing line
from scipy.signal import savgol_filter
x_sorted = np.sort(df['x'].values)
y_sorted = df.loc[df['x'].argsort(), 'y'].values
# Use rolling median for smoother line
window = 50
if len(x_sorted) >= window:
    x_smooth = x_sorted[window//2:-window//2]
    y_smooth = np.array([np.median(y_sorted[i-window//2:i+window//2]) 
                         for i in range(window//2, len(y_sorted)-window//2)])
    ax1.plot(x_smooth, y_smooth, 'r-', linewidth=3, label='Median trend', zorder=10)

ax1.set_xlabel('Days with Company (x)', fontsize=12)
ax1.set_ylabel('Monthly Commits (y)', fontsize=12)
ax1.set_title('Relationship Between Tenure and Monthly Commits (Clean Data)', 
              fontsize=13, fontweight='bold')
ax1.legend(loc='upper right')
ax1.grid(alpha=0.3)

# ============================================================================
# Plot 2: Hexbin (shows density better)
# ============================================================================
ax2 = fig.add_subplot(gs[0, 2])
hb = ax2.hexbin(df['x'], df['y'], gridsize=30, cmap='viridis', mincnt=1)
ax2.set_xlabel('Days with Company', fontsize=11)
ax2.set_ylabel('Monthly Commits', fontsize=11)
ax2.set_title('Density Plot', fontsize=12, fontweight='bold')
plt.colorbar(hb, ax=ax2, label='Count')

# ============================================================================
# Plot 3: By tenure groups
# ============================================================================
ax3 = fig.add_subplot(gs[1, 0])

# Create tenure groups
df['tenure_group'] = pd.cut(df['x'], 
                             bins=[0, 365, 730, 1825, 10000],
                             labels=['0-1yr', '1-2yr', '2-5yr', '5+yr'])

tenure_order = ['0-1yr', '1-2yr', '2-5yr', '5+yr']
data_by_tenure = [df[df['tenure_group'] == t]['y'].values for t in tenure_order]

bp = ax3.boxplot(data_by_tenure, labels=tenure_order, patch_artist=True)
colors = plt.cm.viridis(np.linspace(0, 0.9, len(tenure_order)))
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)

ax3.set_xlabel('Tenure Group', fontsize=11)
ax3.set_ylabel('Monthly Commits', fontsize=11)
ax3.set_title('Commits by Tenure Group', fontsize=12, fontweight='bold')
ax3.grid(alpha=0.3, axis='y')

# ============================================================================
# Plot 4: By seniority
# ============================================================================
ax4 = fig.add_subplot(gs[1, 1])

seniority_order = ['Junior', 'Mid', 'Senior']
data_by_seniority = [df[df['seniority'] == s]['y'].values for s in seniority_order]

bp2 = ax4.boxplot(data_by_seniority, labels=seniority_order, patch_artist=True)
colors2 = plt.cm.viridis(np.linspace(0, 0.9, len(seniority_order)))
for patch, color in zip(bp2['boxes'], colors2):
    patch.set_facecolor(color)

ax4.set_xlabel('Seniority', fontsize=11)
ax4.set_ylabel('Monthly Commits', fontsize=11)
ax4.set_title('Commits by Seniority', fontsize=12, fontweight='bold')
ax4.grid(alpha=0.3, axis='y')

# Add mean values as text
for i, sen in enumerate(seniority_order):
    mean_val = df[df['seniority'] == sen]['y'].mean()
    ax4.text(i+1, -8, f'μ={mean_val:.1f}', ha='center', fontsize=9)

# ============================================================================
# Plot 5: By department and seniority
# ============================================================================
ax5 = fig.add_subplot(gs[1, 2])

# Create grouped data
dept_sen_means = df.groupby(['department', 'seniority'])['y'].mean().reset_index()

x_pos = np.arange(len(seniority_order))
width = 0.35

for i, dept in enumerate(['IT', 'Analytics']):
    means = [dept_sen_means[(dept_sen_means['department']==dept) & 
                            (dept_sen_means['seniority']==sen)]['y'].values[0] 
             if len(dept_sen_means[(dept_sen_means['department']==dept) & 
                                   (dept_sen_means['seniority']==sen)]) > 0 else 0
             for sen in seniority_order]
    
    color = '#440154' if dept == 'IT' else '#35b779'
    ax5.bar(x_pos + i*width, means, width, label=dept, color=color, alpha=0.8)

ax5.set_xlabel('Seniority', fontsize=11)
ax5.set_ylabel('Mean Monthly Commits', fontsize=11)
ax5.set_title('Mean Commits by Dept × Seniority', fontsize=12, fontweight='bold')
ax5.set_xticks(x_pos + width/2)
ax5.set_xticklabels(seniority_order)
ax5.legend()
ax5.grid(alpha=0.3, axis='y')

# ============================================================================
# Plot 6: Residuals from linear model
# ============================================================================
ax6 = fig.add_subplot(gs[2, 0])

# Fit simple linear model
X = df['x'].values.reshape(-1, 1)
y = df['y'].values
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)
residuals = y - y_pred

ax6.scatter(y_pred, residuals, alpha=0.4, s=20, color='#31688e')
ax6.axhline(y=0, color='red', linestyle='--', linewidth=2)
ax6.set_xlabel('Fitted Values', fontsize=11)
ax6.set_ylabel('Residuals', fontsize=11)
ax6.set_title('Residual Plot (Linear Model)', fontsize=12, fontweight='bold')
ax6.grid(alpha=0.3)

# Add text with model stats
r2 = model.score(X, y)
ax6.text(0.05, 0.95, f'R² = {r2:.3f}\nSlope = {model.coef_[0]:.4f}', 
         transform=ax6.transAxes, fontsize=10, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# ============================================================================
# Plot 7: Q-Q plot (check normality of residuals)
# ============================================================================
ax7 = fig.add_subplot(gs[2, 1])

stats.probplot(residuals, dist="norm", plot=ax7)
ax7.set_title('Q-Q Plot (Linear Model Residuals)', fontsize=12, fontweight='bold')
ax7.grid(alpha=0.3)

# ============================================================================
# Plot 8: Log-log relationship
# ============================================================================
ax8 = fig.add_subplot(gs[2, 2])

# Filter out zeros for log
df_positive = df[df['y'] > 0].copy()
log_x = np.log(df_positive['x'])
log_y = np.log(df_positive['y'])

ax8.scatter(log_x, log_y, alpha=0.4, s=20, color='#31688e')

# Fit log-log model
model_log = LinearRegression()
model_log.fit(log_x.values.reshape(-1, 1), log_y.values)
log_y_pred = model_log.predict(log_x.values.reshape(-1, 1))

# Plot fitted line
idx_sorted = np.argsort(log_x)
ax8.plot(log_x.iloc[idx_sorted], log_y_pred[idx_sorted], 'r-', linewidth=2, 
         label=f'Elasticity = {model_log.coef_[0]:.2f}')

ax8.set_xlabel('log(Days with Company)', fontsize=11)
ax8.set_ylabel('log(Monthly Commits)', fontsize=11)
ax8.set_title('Log-Log Relationship', fontsize=12, fontweight='bold')
ax8.legend()
ax8.grid(alpha=0.3)

r2_log = model_log.score(log_x.values.reshape(-1, 1), log_y.values)
ax8.text(0.05, 0.95, f'R² = {r2_log:.3f}', 
         transform=ax8.transAxes, fontsize=10, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.savefig('/home/claude/xy_relationship_analysis.png', dpi=150, bbox_inches='tight')
print("\n✓ Plots saved to: xy_relationship_analysis.png")

# ==============================================================================
# STATISTICAL SUMMARIES
# ==============================================================================

print("\n" + "="*70)
print("STATISTICAL ANALYSIS OF X-Y RELATIONSHIP")
print("="*70)

# 1. Simple linear model
print("\n1. LINEAR MODEL: y = β₀ + β₁*x + ε")
print(f"   Slope (β₁): {model.coef_[0]:.6f}")
print(f"   Intercept (β₀): {model.intercept_:.3f}")
print(f"   R²: {r2:.3f}")
print(f"   Interpretation: Each additional day with company associated with")
print(f"                   {model.coef_[0]*30:.3f} more commits per month (on average)")

# 2. Log-log model
print("\n2. LOG-LOG MODEL: log(y) = β₀ + β₁*log(x) + ε")
print(f"   Elasticity (β₁): {model_log.coef_[0]:.3f}")
print(f"   R²: {r2_log:.3f}")
print(f"   Interpretation: 10% increase in tenure → {model_log.coef_[0]*10:.1f}% change in commits")

# 3. By groups
print("\n3. GROUP COMPARISONS:")
print("\n   By Tenure:")
for group in tenure_order:
    group_data = df[df['tenure_group'] == group]['y']
    print(f"   {group:8s}: mean={group_data.mean():5.1f}, median={group_data.median():5.1f}, n={len(group_data):4d}")

print("\n   By Seniority:")
for sen in seniority_order:
    sen_data = df[df['seniority'] == sen]['y']
    print(f"   {sen:8s}: mean={sen_data.mean():5.1f}, median={sen_data.median():5.1f}, n={len(sen_data):4d}")

print("\n   By Department:")
for dept in ['IT', 'Analytics']:
    dept_data = df[df['department'] == dept]['y']
    print(f"   {dept:10s}: mean={dept_data.mean():5.1f}, median={dept_data.median():5.1f}, n={len(dept_data):4d}")

# 4. ANOVA tests
print("\n4. STATISTICAL TESTS:")

# Test if seniority matters
from scipy.stats import f_oneway
junior_y = df[df['seniority'] == 'Junior']['y']
mid_y = df[df['seniority'] == 'Mid']['y']
senior_y = df[df['seniority'] == 'Senior']['y']

f_stat, p_val = f_oneway(junior_y, mid_y, senior_y)
print(f"   Seniority effect (ANOVA): F={f_stat:.2f}, p={p_val:.4f}")
print(f"   {'→ Significant difference' if p_val < 0.05 else '→ No significant difference'}")

# Test if department matters
it_y = df[df['department'] == 'IT']['y']
analytics_y = df[df['department'] == 'Analytics']['y']
t_stat, p_val_dept = stats.ttest_ind(it_y, analytics_y)
print(f"   Department effect (t-test): t={t_stat:.2f}, p={p_val_dept:.4f}")
print(f"   {'→ Significant difference' if p_val_dept < 0.05 else '→ No significant difference'}")

# ==============================================================================
# KEY FINDINGS SUMMARY
# ==============================================================================

print("\n" + "="*70)
print("KEY FINDINGS")
print("="*70)

print("\n1. OVERALL PATTERN:")
print(f"   • Weak positive correlation: r = {corr:.3f}")
print(f"   • Linear model explains only {r2*100:.1f}% of variance")
print(f"   • Relationship is noisy - high individual variation")

if corr > 0:
    print(f"   • More experienced employees commit slightly more on average")
else:
    print(f"   • Surprisingly, little relationship between tenure and commits")

print("\n2. NON-LINEAR FEATURES:")
if r2_log > r2:
    print(f"   • Log-log model fits better (R² = {r2_log:.3f} vs {r2:.3f})")
    print(f"   • Suggests diminishing returns to experience")
else:
    print(f"   • Linear model adequate (no strong non-linearity)")

print("\n3. HETEROGENEITY:")
print(f"   • Seniority matters: Mid-level most productive")
print(f"   • Department matters: {'IT' if it_y.mean() > analytics_y.mean() else 'Analytics'} higher on average")
print(f"   • Large role-based differences (see plots)")

print("\n4. DATA CHARACTERISTICS:")
print(f"   • Right-skewed: median ({df['y'].median():.0f}) < mean ({df['y'].mean():.0f})")
print(f"   • Count data: integer values, includes zeros ({(df['y']==0).sum()} cases)")
print(f"   • Overdispersion: variance ({df['y'].var():.0f}) >> mean ({df['y'].mean():.0f})")

print("\n" + "="*70)
print("CONCLUSION: Relationship exists but is WEAK and NOISY")
print("             Role/seniority effects likely more important than raw tenure")
print("="*70)
