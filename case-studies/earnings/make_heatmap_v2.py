"""
Heatmap of mean hourly wages by occupation group and education level.
v2: Condensed to 10 broad occupation groups.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# -- Load data ---------------------------------------------------------------
df = pd.read_csv("data/morg-2014-emp-state5.csv")
df["hourly_wage"] = df["earnwke"] / df["uhours"]

# Trim extreme hourly wages (likely data errors: e.g. 1 hr/week with high earnings)
df = df[(df["hourly_wage"] >= 3) & (df["hourly_wage"] <= 150)]

# -- Education labels --------------------------------------------------------
def edu_label(g):
    if g <= 38: return "Less than HS"
    if g == 39: return "High School"
    if g <= 42: return "Some College /\nAssociate"
    if g == 43: return "Bachelor's"
    return "Graduate"

EDU_ORDER = ["Less than HS", "High School", "Some College /\nAssociate",
             "Bachelor's", "Graduate"]
df["education"] = df["grade92"].apply(edu_label)
df["education"] = pd.Categorical(df["education"], categories=EDU_ORDER, ordered=True)

# -- 10 broad occupation groups (Census 2010 codes) --------------------------
OCC_GROUPS = [
    (0,    950,  "Management &\nBusiness"),           # Management + Business & Finance
    (1000, 1560, "STEM &\nTechnical"),                # Computer, Math, Architecture, Engineering
    (1600, 1980, "STEM &\nTechnical"),                # Science
    (2000, 2060, "Education, Legal\n& Social Service"), # Community & Social Service
    (2100, 2160, "Education, Legal\n& Social Service"), # Legal
    (2200, 2550, "Education, Legal\n& Social Service"), # Education
    (2600, 2920, "Education, Legal\n& Social Service"), # Arts & Media
    (3000, 3650, "Healthcare"),                        # Practitioners + Support
    (3700, 3950, "Protective Service\n& Military"),    # Protective Service
    (9000, 9750, "Protective Service\n& Military"),    # Military
    (4000, 4250, "Food, Cleaning\n& Personal Care"),   # Food Prep + Cleaning
    (4300, 4650, "Food, Cleaning\n& Personal Care"),   # Personal Care
    (4700, 4965, "Office &\nSales"),                   # Sales
    (5000, 5940, "Office &\nSales"),                   # Office & Admin
    (6000, 6130, "Trades &\nConstruction"),            # Farming
    (6200, 6765, "Trades &\nConstruction"),            # Construction
    (6800, 6940, "Trades &\nConstruction"),            # Installation & Repair
    (7000, 7630, "Production &\nTransportation"),      # Production
    (7700, 8965, "Production &\nTransportation"),      # Transportation
]

def occ_group(code):
    for lo, hi, label in OCC_GROUPS:
        if lo <= code <= hi:
            return label
    return "Other"

df["occ_group"] = df["occ2012"].apply(occ_group)
df = df[df["occ_group"] != "Other"]

# -- Compute weighted mean hourly wage ---------------------------------------
def wmean(g):
    return np.average(g["hourly_wage"], weights=g["weight"])

heatmap_data = (
    df.groupby(["occ_group", "education"])
    .apply(wmean, include_groups=False)
    .reset_index(name="hourly_wage")
    .pivot(index="occ_group", columns="education", values="hourly_wage")
)

# Order rows by overall mean wage (highest at top)
row_order = heatmap_data.mean(axis=1).sort_values(ascending=True).index
heatmap_data = heatmap_data.loc[row_order]

# -- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))

im = ax.imshow(heatmap_data.values, aspect="auto", cmap="viridis",
               vmin=8, vmax=50)

# Axis labels
ax.set_xticks(range(len(EDU_ORDER)))
ax.set_xticklabels(EDU_ORDER, fontsize=11, ha="center")
ax.xaxis.tick_top()
ax.xaxis.set_label_position("top")

ax.set_yticks(range(len(heatmap_data)))
ax.set_yticklabels(heatmap_data.index, fontsize=10)

# Annotate cells with dollar values
for i in range(heatmap_data.shape[0]):
    for j in range(heatmap_data.shape[1]):
        val = heatmap_data.iloc[i, j]
        if np.isnan(val):
            continue
        color = "white" if val < 28 else "black"
        ax.text(j, i, f"${val:.0f}", ha="center", va="center",
                fontsize=10, fontweight="bold", color=color)

# Colorbar
cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.04)
cbar.set_label("Mean Hourly Wage ($)", fontsize=11)
cbar.ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:.0f}"))

ax.set_title("Mean Hourly Wage by Occupation and Education Level",
             fontsize=14, fontweight="bold", pad=50)

fig.tight_layout()
fig.savefig("exhibits/heatmap_wage_occ_edu_v2.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close(fig)
print("Saved: exhibits/heatmap_wage_occ_edu_v2.png")
