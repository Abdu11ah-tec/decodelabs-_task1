import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Set a cohesive styling theme for business stakeholder presentations
sns.set_theme(style="whitegrid")
plt.rcParams["font.size"] = 12
plt.rcParams["axes.labelsize"] = 14
plt.rcParams["axes.titlesize"] = 16


# 1. INPUT PHASE
print("=" * 60)
print("PHASE 1: INPUT - DIGITAL EVIDENCE AUDIT")
print("=" * 60)

df = pd.read_csv("netflix_titles.csv")

print(f"Total Operational Records Analyzed : {df.shape[0]}")
print(f"Total Structural Features Inspected: {df.shape[1]}\n")

missing_counts = df.isnull().sum()
missing_percentages = (df.isnull().sum() / len(df)) * 100

print("Missing Evidence Summary:")
for col in df.columns:
    if missing_counts[col] > 0:
        print(
            f" -> Feature '{col}': Missing {missing_counts[col]} records ({missing_percentages[col]:.2f}%)"
        )
print("-" * 60 + "\n")


# 2. PROCESS PHASE

df["country"] = df["country"].fillna("Unknown")
df["cast"] = df["cast"].fillna("No Cast Listed")
df["director"] = df["director"].fillna("Unknown")

df = df.dropna(subset=["date_added", "rating", "duration"])


# 3. PROCESS PHASE: Descriptive Statistics & Center of Gravity Proofs

print("=" * 60)
print("PHASE 2: PROCESS - STATISTICAL PROOFS & PATTERNS")
print("=" * 60)

type_counts = df["type"].value_counts()
type_shares = df["type"].value_counts(normalize=True) * 100
print("Content Catalog Mix Split:")
for category in type_counts.index:
    print(
        f" -> {category}: {type_counts[category]} titles ({type_shares[category]:.2f}%)"
    )
print("-" * 60)

print("Release Year Geometry (The Logic Skeleton):")
five_num = df["release_year"].describe()
print(f" -> Minimum (The Floor)   : {int(five_num['min'])}")
print(f" -> Q1 (25th Percentile)  : {int(five_num['25%'])}")
print(f" -> Median (50th % Center): {int(five_num['50%'])}")
print(f" -> Q3 (75th Percentile)  : {int(five_num['75%'])}")
print(f" -> Maximum (The Ceiling) : {int(five_num['max'])}")
print("-" * 60)

movies_df = df[df["type"] == "Movie"].copy()
# Standardize string inputs like '90 min' into pure operational integers
movies_df["duration_mins"] = (
    movies_df["duration"].str.replace(" min", "", regex=False).astype(int)
)

mean_dur = movies_df["duration_mins"].mean()
median_dur = movies_df["duration_mins"].median()

print("Mathematical Symmetry Check (Movie Run-Times):")
print(f" -> Calculated Mean Duration  : {mean_dur:.2f} minutes")
print(f" -> Calculated Median Duration: {median_dur:.2f} minutes")

if abs(mean_dur - median_dur) < 3:
    print(
        " -> Business Verdict: Distribution is Symmetrical. Mean is a valid center of gravity."
    )
else:
    print(
        " -> Business Verdict: Distribution is Skewed. Fall back to Median for KPI reporting."
    )
print("=" * 60 + "\n")


# 4. OUTPUT PHASE

print("Generating analytical plots...")

fig, axes = plt.subplots(1, 2, figsize=(18, 7))

sns.histplot(
    data=df,
    x="release_year",
    hue="type",
    multiple="stack",
    kde=True,
    bins=40,
    ax=axes[0],
    palette="dark",
)
axes[0].set_xlim(1970, 2022)  # Cut off vintage temporal anomalies for cluster clarity
axes[0].set_title(
    "The Geometry of Distribution:\nContent Release Volume Density", pad=15
)
axes[0].set_xlabel("Release Year")
axes[0].set_ylabel("Total Catalog Additions")

exploded_countries = (
    df[df["country"] != "Unknown"]["country"]
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)
)

sns.barplot(
    x=exploded_countries.values,
    y=exploded_countries.index,
    ax=axes[1],
    palette="viridis",
)
axes[1].set_title("Top 10 Global Production Repositories\n(Exploded Country Records)", pad=15)
axes[1].set_xlabel("Total Unique Titles Identified")
axes[1].set_ylabel("Country Origin")

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
sns.histplot(
    data=movies_df, x="duration_mins", kde=True, color="crimson", bins=30
)
plt.axvline(
    mean_dur,
    color="blue",
    linestyle="--",
    linewidth=2,
    label=f"Mean: {mean_dur:.1f}m",
)
plt.axvline(
    median_dur,
    color="yellow",
    linestyle="-",
    linewidth=2,
    label=f"Median: {median_dur:.1f}m",
)
plt.title(
    "Movie Runtime Configuration: Verifying Bell-Curve Symmetry Check", pad=15
)
plt.xlabel("Duration in Minutes")
plt.ylabel("Movie Counts")
plt.legend(facecolor="white", frameon=True)
plt.show()
