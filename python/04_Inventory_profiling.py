import pandas as pd

## Inventory Data Profiling ##

#1. Loading inventory data
inventory = pd.read_csv("inventory_raw.csv")

#Checking basic info
print(inventory.head().to_string(index=False))
print(inventory.shape)
print(inventory.isnull().sum())


## Inventory Data Cleaning ##

#2. Removing duplicate inventory records
inventory_clean = inventory.drop_duplicates(
    subset="inventory_id"
).copy()


#3. Standardizing date formats

#Identify dates already in YYYY-MM-DD format
iso_dates = inventory_clean["date"].str.match(
    r"^\d{4}-\d{2}-\d{2}$"
)

#Create a separate datetime column
inventory_clean["clean_date"] = pd.NaT
inventory_clean["clean_date"] = inventory_clean["clean_date"].astype("datetime64[ns]")

#Convert YYYY-MM-DD dates
inventory_clean.loc[iso_dates, "clean_date"] = pd.to_datetime(
    inventory_clean.loc[iso_dates, "date"],
    format="%Y-%m-%d",
    errors="coerce"
)

#Convert other date formats
inventory_clean.loc[~iso_dates, "clean_date"] = pd.to_datetime(
    inventory_clean.loc[~iso_dates, "date"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)


#4. Checking invalid dates
print("\nInvalid dates:")
print(inventory_clean["clean_date"].isnull().sum())


#5. Replacing original date column
inventory_clean["date"] = inventory_clean["clean_date"].dt.strftime("%Y-%m-%d")

inventory_clean = inventory_clean.drop(columns=["clean_date"])


#6. Checking missing values
print("\nMissing values:")
print(inventory_clean.isnull().sum())


#7. Saving cleaned inventory data
inventory_clean.to_csv("inventory_clean.csv", index=False)


#8. Checking cleaned data
print("\nCleaned inventory:")
print(inventory_clean.head(20).to_string(index=False))