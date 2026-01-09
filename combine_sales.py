import pandas as pd

# ===============================
# CONFIG
# ===============================
DATA_PATH = "data/"
OUTPUT_PATH = "output/"
OUTPUT_FILE = "Master_Sales_Outward.csv"

# ===============================
# LOAD CSV FILES
# ===============================
print("Loading CSV files...")

df_achala = pd.read_csv(
    DATA_PATH + "outward_achala.csv",
    low_memory=False
)

df_bhiwandi = pd.read_csv(
    DATA_PATH + "outward_bhiwandi.csv",
    low_memory=False
)

df_virtual = pd.read_csv(
    DATA_PATH + "outward_bhiwandi_virtual.csv",
    low_memory=False
)

print("Files loaded successfully")

# ===============================
# BASIC SHAPE CHECK
# ===============================
print("\nRow & Column Counts:")
print("Achala:", df_achala.shape)
print("Bhiwandi:", df_bhiwandi.shape)
print("Bhiwandi Virtual:", df_virtual.shape)

# ===============================
# COLUMN CONSISTENCY CHECK
# ===============================
print("\nChecking column consistency...")

if not df_achala.columns.equals(df_bhiwandi.columns):
    raise ValueError("❌ Column mismatch between Achala and Bhiwandi")

if not df_achala.columns.equals(df_virtual.columns):
    raise ValueError("❌ Column mismatch between Achala and Virtual")

print("✅ Columns are consistent across all files")

# ===============================
# ADD SOURCE COLUMN
# ===============================
df_achala["Source_Fulfillment"] = "fc_achala"
df_bhiwandi["Source_Fulfillment"] = "fc_bhiwandi"
df_virtual["Source_Fulfillment"] = "bhiwandi_virtual"

# ===============================
# APPEND / CONCATENATE
# ===============================
print("\nCombining all data...")

master_df = pd.concat(
    [df_achala, df_bhiwandi, df_virtual],
    ignore_index=True
)

print("Combined dataset shape:", master_df.shape)

# ===============================
# SANITY CHECKS
# ===============================
print("\nRunning sanity checks...")

print("Total rows:", len(master_df))

if "Total Sale Price" in master_df.columns:
    print(
        "Missing Total Sale Price:",
        master_df["Total Sale Price"].isna().sum()
    )
    print(
        "Negative Total Sale Price:",
        (master_df["Total Sale Price"] < 0).sum()
    )
else:
    print("⚠️ 'Total Sale Price' column not found")

if "SO Quantity" in master_df.columns and "Dispatched Quantity" in master_df.columns:
    qty_mismatch = master_df[
        master_df["SO Quantity"] != master_df["Dispatched Quantity"]
    ]
    print("SO vs Dispatched Qty mismatch rows:", len(qty_mismatch))
else:
    print("⚠️ Quantity columns not found")

# ===============================
# BASIC KPI CALCULATION
# ===============================
print("\nBasic KPI check:")

if "Total Sale Price" in master_df.columns and "Dispatched Quantity" in master_df.columns:
    total_revenue = master_df["Total Sale Price"].sum()
    total_units = master_df["Dispatched Quantity"].sum()
    asp = total_revenue / total_units if total_units != 0 else 0

    print("Total Revenue:", round(total_revenue, 2))
    print("Total Units Sold:", total_units)
    print("Average Selling Price (ASP):", round(asp, 2))
else:
    print("⚠️ KPI columns missing")

# ===============================
# SAVE FINAL CSV
# ===============================
print("\nSaving final CSV...")

master_df.to_csv(
    OUTPUT_PATH + OUTPUT_FILE,
    index=False
)

print("✅ Master CSV saved at:", OUTPUT_PATH + OUTPUT_FILE)

print("\nPROCESS COMPLETED SUCCESSFULLY 🚀")
