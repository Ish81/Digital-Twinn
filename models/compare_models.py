# models/eda.py

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# LOAD DATA
# -----------------------------
data = pd.read_csv("data/full_simulation_output.csv")

print("\n===== DATASET OVERVIEW =====")
print("Shape:", data.shape)
print("\nColumns:")
print(data.columns.tolist())

print("\n===== DATA TYPES =====")
print(data.dtypes)

print("\n===== MISSING VALUES =====")
print(data.isnull().sum())

print("\n===== DUPLICATES =====")
print("Duplicate Rows:", data.duplicated().sum())

print("\n===== STATISTICAL SUMMARY =====")
print(data.describe())

# -----------------------------
# SELECT NUMERIC COLUMNS
# -----------------------------
numeric_data = data.select_dtypes(include=[np.number])

# -----------------------------
# CORRELATION MATRIX
# -----------------------------
corr = numeric_data.corr()

plt.figure(figsize=(12,8))
plt.imshow(corr, cmap="coolwarm", aspect="auto")
plt.colorbar()
plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
plt.yticks(range(len(corr.columns)), corr.columns)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()

# -----------------------------
# HISTOGRAMS
# -----------------------------
numeric_data.hist(figsize=(14,10), bins=30)
plt.tight_layout()
plt.show()

# -----------------------------
# SCATTER: Turbidity vs PAC Dose
# -----------------------------
plt.figure(figsize=(8,5))
plt.scatter(data["turbidity"], data["pac_dose_ppm"], alpha=0.4)
plt.xlabel("Raw Turbidity")
plt.ylabel("PAC Dose (ppm)")
plt.title("PAC Dose vs Turbidity")
plt.show()

# -----------------------------
# SCATTER: PAC Dose vs Treated Turbidity
# -----------------------------
plt.figure(figsize=(8,5))
plt.scatter(data["pac_dose_ppm"], data["treated_turbidity"], alpha=0.4)
plt.xlabel("PAC Dose (ppm)")
plt.ylabel("Treated Turbidity")
plt.title("PAC Dose vs Treated Turbidity")
plt.show()

# -----------------------------
# TIME TREND
# -----------------------------
plt.figure(figsize=(14,5))
plt.plot(data["turbidity"][:500], label="Raw Turbidity")
plt.plot(data["treated_turbidity"][:500], label="Treated Turbidity")
plt.legend()
plt.title("First 500 Hours Trend")
plt.show()
