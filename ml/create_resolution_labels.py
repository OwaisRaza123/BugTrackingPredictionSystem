import pandas as pd

# ==========================
# Load Dataset
# ==========================

data = pd.read_csv("dataset/resolution_processed.csv")

print("Original Shape :", data.shape)

# ==========================
# Create Resolution Category
# ==========================

def resolution_label(time):

    if time <= 24:
        return "1 Day"

    elif time <= 72:
        return "2-3 Days"

    elif time <= 168:
        return "1 Week"

    elif time <= 336:
        return "2 Weeks"

    elif time <= 720:
        return "1 Month"

    else:
        return "More than 1 Month"

# Create new column
data["Resolution_Label"] = data["Fixing_time"].apply(resolution_label)

# Save
data.to_csv(
    "dataset/resolution_labeled.csv",
    index=False
)

print("\nResolution labels created successfully.\n")

print(data[["Fixing_time", "Resolution_Label"]].head())