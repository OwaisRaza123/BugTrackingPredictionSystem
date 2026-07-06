import pandas as pd

# ==========================
# Load Severity Dataset
# ==========================

severity_data = pd.read_csv("dataset/sev.csv")

print("\n========== Severity Dataset ==========\n")

print("Original Shape :", severity_data.shape)

# Remove unnecessary columns
severity_data = severity_data.loc[:, ~severity_data.columns.str.contains("^Unnamed")]

# Remove missing values
severity_data.dropna(inplace=True)

print("Clean Shape :", severity_data.shape)

print("\nColumns :")
print(severity_data.columns)

print("\nFirst 5 Records")
print(severity_data.head())


# ==========================
# Load Resolution Dataset
# ==========================

resolution_data = pd.read_csv("dataset/fix.csv")

print("\n========== Resolution Dataset ==========\n")

print("Original Shape :", resolution_data.shape)

# Remove unnecessary columns
resolution_data = resolution_data.loc[:, ~resolution_data.columns.str.contains("^Unnamed")]

# Remove missing values
resolution_data.dropna(inplace=True)

print("Clean Shape :", resolution_data.shape)

print("\nColumns :")
print(resolution_data.columns)

print("\nFirst 5 Records")
print(resolution_data.head())


# ==========================
# Save Clean Dataset
# ==========================

severity_data.to_csv(
    "dataset/severity_clean.csv",
    index=False
)

resolution_data.to_csv(
    "dataset/resolution_clean.csv",
    index=False
)

print("\nDatasets cleaned successfully.")