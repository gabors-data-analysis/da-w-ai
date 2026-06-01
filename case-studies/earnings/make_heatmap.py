"""
Heatmap of mean hourly wages by occupation group and education level.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# -- Load data ---------------------------------------------------------------
df = pd.read_csv("data/morg-2014-emp-state5.csv")
df["hourly_wage"] = df["earnwke"] / df["uhours"]

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

# -- Occupation major groups (Census 2010 codes) -----------------------------
OCC_GROUPS = [
    (0,    430,  "Management"),
    (500,  950,  "Business & Finance"),
    (1000, 1240, "Computer & Math"),
    (1300, 1560, "Architecture &\nEngineering"),
    (1600, 1980, "Science"),
    (2000, 2060, "Community &\nSocial Service"),
    (2100, 2160, "Legal"),
    (2200, 2550, "Education"),
    (2600, 2920, "Arts & Media"),
    (3000, 3540, "Healthcare\nPractitioners"),
    (3600, 3650, "Healthcare\nSupport"),
    (3700, 3950, "Protective\nService"),
    (4000, 4150, "Food Prep\n& Serving"),
    (4200, 4250, "Cleaning &\nMaintenance"),
    (4300, 4650, "Personal Care"),
    (4700, 4965, "Sales"),
    (5000, 5940, "Office &\nAdmin Support"),
    (6000, 6130, "Farming &\nFishing"),
    (6200, 6765, "Construction"),
    (6800, 6940, "Installation\n& Repair"),
    (7000, 7630, "Production"),
    (7700, 8965, "Transportation"),
    (9000, 9750, "Military"),
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

# Drop groups with too few observations in any cell
cell_counts = (
    df.groupby(["occ_group", "education"]).size()
    .reset_index(name="n")
    .pivot(index="occ_group", columns="education", values="n")
    .reindex(index=row_order, columns=EDU_ORDER)
    .fillna(0)
)
# Keep rows where at least 3 of 5 education cells have 20+ observations
mask = (cell_counts >= 20).sum(axis=1) >= 3
heatmap_data = heatmap_data.loc[mask]

# -- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 9))

im = ax.imshow(heatmap_data.values, aspect="auto", cmap="viridis",
               vmin=8, vmax=55)

# Axis labels
ax.set_xticks(range(len(EDU_ORDER)))
ax.set_xticklabels(EDU_ORDER, fontsize=10, ha="center")
ax.xaxis.tick_top()
ax.xaxis.set_label_position("top")

ax.set_yticks(range(len(heatmap_data)))
ax.set_yticklabels(heatmap_data.index, fontsize=9)

# Annotate cells with dollar values
for i in range(heatmap_data.shape[0]):
    for j in range(heatmap_data.shape[1]):
        val = heatmap_data.iloc[i, j]
        if np.isnan(val):
            continue
        # Dark text on light cells, white on dark
        color = "white" if val < 30 else "black"
        ax.text(j, i, f"${val:.0f}", ha="center", va="center",
                fontsize=8, fontweight="bold", color=color)

# Colorbar
cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.04)
cbar.set_label("Mean Hourly Wage ($)", fontsize=11)
cbar.ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:.0f}"))

ax.set_title("Mean Hourly Wage by Occupation and Education Level",
             fontsize=14, fontweight="bold", pad=50)

fig.tight_layout()
fig.savefig("exhibits/heatmap_wage_occ_edu.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close(fig)
print("Saved: exhibits/heatmap_wage_occ_edu.png")
