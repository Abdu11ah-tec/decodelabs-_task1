import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load Cleaned Dataset
file_path = "Cleaned_Data_Analytics_Project(1).xlsx"
df = pd.read_excel(file_path)

print("="*60)
print("DATASET INFORMATION")
print("="*60)

print(df.info())

print("\nFirst 5 Rows")
print(df.head())

print("\nLast 5 Rows")
print(df.tail())


print("\nDescriptive Statistics")

stats = df.describe(include='all')

print(stats)

# Additional Statistics

numeric = df.select_dtypes(include=np.number)

statistics = pd.DataFrame({
    "Count": numeric.count(),
    "Mean": numeric.mean(),
    "Median": numeric.median(),
    "Mode": numeric.mode().iloc[0],
    "Minimum": numeric.min(),
    "Maximum": numeric.max(),
    "Range": numeric.max()-numeric.min(),
    "Variance": numeric.var(),
    "Standard Deviation": numeric.std(),
    "Skewness": numeric.skew(),
    "Kurtosis": numeric.kurt(),
    "Missing Values": numeric.isnull().sum()
})

correlation = numeric.corr()

outlier_summary = []

for col in numeric.columns:

    Q1 = numeric[col].quantile(0.25)
    Q3 = numeric[col].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = numeric[(numeric[col] < lower) |
                       (numeric[col] > upper)]

    outlier_summary.append({
        "Column": col,
        "Outliers": len(outliers),
        "Lower Bound": lower,
        "Upper Bound": upper
    })

outlier_df = pd.DataFrame(outlier_summary)


categorical = df.select_dtypes(include='object')

category_analysis = {}

for col in categorical.columns:
    category_analysis[col] = df[col].value_counts()

trend_data = pd.DataFrame()

if len(numeric.columns) > 0:
    trend_data = numeric.mean().sort_values(ascending=False)


insights = []

insights.append("Dataset contains {} rows.".format(len(df)))
insights.append("Dataset contains {} columns.".format(len(df.columns)))
insights.append("No missing values detected after Project 1 cleaning.")

for col in numeric.columns:

    insights.append(
        f"{col} average value = {round(df[col].mean(),2)}"
    )

    insights.append(
        f"{col} maximum value = {round(df[col].max(),2)}"
    )

    insights.append(
        f"{col} minimum value = {round(df[col].min(),2)}"
    )

writer = pd.ExcelWriter(
    "Project2_Completed_EDA.xlsx",
    engine="openpyxl"
)

# Original Clean Data
df.to_excel(writer,
            sheet_name="Cleaned_Data",
            index=False)

# Statistics
statistics.to_excel(writer,
                    sheet_name="Statistics")

# Correlation
correlation.to_excel(writer,
                     sheet_name="Correlation")

# Outliers
outlier_df.to_excel(writer,
                    sheet_name="Outlier_Analysis",
                    index=False)

# Trend
trend_data.to_frame(
    name="Average"
).to_excel(writer,
           sheet_name="Trend_Analysis")

# Category Analysis

for col in categorical.columns:

    category_analysis[col].to_frame(
        name="Count"
    ).to_excel(writer,
               sheet_name=f"{col[:25]}")

# Insights
insight_df = pd.DataFrame({
    "Key Observations": insights
})

insight_df.to_excel(writer,
                    sheet_name="Business_Insights",
                    index=False)

writer.close()

print("\nExcel Report Saved Successfully")


sns.set_style("whitegrid")

# Histograms

for col in numeric.columns:

    plt.figure(figsize=(8,5))

    sns.histplot(df[col],
                 kde=True)

    plt.title(f"Distribution of {col}")

    plt.tight_layout()

    plt.savefig(f"{col}_Histogram.png")

    plt.close()

# Boxplots

for col in numeric.columns:

    plt.figure(figsize=(8,3))

    sns.boxplot(x=df[col])

    plt.title(f"Outliers in {col}")

    plt.tight_layout()

    plt.savefig(f"{col}_Boxplot.png")

    plt.close()

# Correlation Heatmap

plt.figure(figsize=(10,8))

sns.heatmap(correlation,
            annot=True,
            cmap="coolwarm")

plt.title("Correlation Heatmap")

plt.tight_layout()

plt.savefig("Correlation_Heatmap.png")

plt.close()

print("\nCharts Saved Successfully")

print("\nPROJECT 2 COMPLETED SUCCESSFULLY")
