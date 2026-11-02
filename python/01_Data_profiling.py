import pandas as pd

## Products Data Profiling & Cleaning ##
#1. Loading Products data
products = pd.read_csv("products_raw.csv")
# checking basic info
print(products.head())
print(products.shape)
print(products.info())

#2. Checking for Duplicates
print(products[products.duplicated(subset="product_id",keep=False)].to_string())
#dropping duplicates
products_clean=products.drop_duplicates(subset="product_id")
#checking number of products after dropping duplicates
print(products_clean.shape)

#3. Standardizing formats

#standardizing category names
products_clean["category"] = products_clean["category"].str.strip().str.upper()
#standardizing subcategory names
products_clean["sub_category"] = products_clean["sub_category"].str.strip().str.upper()

#4. Checking for missing values
print(products_clean.isnull().sum())
#displaying products with missing values
print(products_clean[products_clean.isnull().any(axis=1)].to_string())

#5-1. Handling missing values (Supplier IDs)
#loading purchase orders to identify missing supplier IDs
purchase_orders = pd.read_csv("purchase_orders_raw.csv")
#finding missing supplier IDs in purchase orders
missing_products = ["P0016", "P0047", "P0060"]

print(
    purchase_orders[purchase_orders["product_id"].isin(missing_products)]
    [["product_id", "supplier_id"]].drop_duplicates().to_string(index=False)
)
#mapping missing supplier IDs
supplier_mapping = {
    "P0016": "SUP007",
    "P0047": "SUP011",
    "P0060": "SUP010"
}

#filling missing supplier IDs
products_clean["supplier_id"] = products_clean["supplier_id"].fillna(
    products_clean["product_id"].map(supplier_mapping)
)

#checking corrected supplier IDs
print(
    products_clean[
        products_clean["product_id"].isin(missing_products)
    ].to_string(index=False)
)

#checking remaining missing values
print(products_clean.isnull().sum())
#5-2. Handling missing values (Unit Cost)
#finding missing unit cost
print(products_clean[products_clean["unit_cost"].isnull()].to_string(index=False))

#checking purchase orders for product P0023
print(purchase_orders[purchase_orders["product_id"] == "P0023"].to_string(index=False))

#checking unit cost of similar products from the same supplier
print(
    products_clean[
        (products_clean["supplier_id"] == "SUP003") &
        (products_clean["category"].str.strip().str.upper() == "APPAREL") &
        (products_clean["sub_category"].str.strip().str.upper() == "MEN")
    ][["product_id", "supplier_id", "unit_cost"]].to_string(index=False)
)

# did not find any similar products from the same supplier, checking other suppliers for similar products

#checking unit cost of similar products across all suppliers
print(
    products_clean[
        (products_clean["category"].str.strip().str.upper() == "APPAREL") &
        (products_clean["sub_category"].str.strip().str.upper() == "MEN")
    ][["product_id", "supplier_id", "unit_cost"]].to_string(index=False)
)

# not enough similar products found to impute unit cost for P0023, 
# so we will keep it as NaN

#5-3. Validating unit costs

#checking zero or negative unit costs
print(
    products_clean[
        products_clean["unit_cost"] <= 0
    ][["product_id", "unit_cost"]].to_string(index=False)
)

#replacing invalid unit costs with NaN
products_clean.loc[
    products_clean["unit_cost"] <= 0,
    "unit_cost"
] = float("nan")

#checking remaining missing unit costs
print(
    products_clean[
        products_clean["unit_cost"].isnull()
    ][["product_id", "unit_cost"]].to_string(index=False)
)

#6. Saving cleaned data

#saving cleaned products data to a new CSV file
products_clean.to_csv("products_clean.csv", index=False)




## Purchase order Data Profiling & Cleaning ##
#1. Loading Purchase Orders data
#checking basic info
print(purchase_orders.head())
print(purchase_orders.shape)
print(purchase_orders.info())

#2. Checking for Duplicates
print(purchase_orders[purchase_orders.duplicated(subset="po_id",keep=False)].to_string())
#dropping duplicates
purchase_orders_clean=purchase_orders.drop_duplicates(subset="po_id")
#checking number of purchase orders after dropping duplicates
print(purchase_orders_clean.shape)

#3. Standardizing formats
#standardizing purchase order statuses
purchase_orders_clean["status"]=purchase_orders_clean["status"].str.strip().str.upper()
#checking formats
print(purchase_orders_clean["status"].unique())

#4. Checking for missing values
print(purchase_orders_clean.isnull().sum())
#displaying purchase orders with missing values
print(purchase_orders_clean[purchase_orders_clean.isnull().any(axis=1)].to_string())

#5. Handling missing values (Quantity received & Actual delivery date)
print(
    purchase_orders_clean[
        purchase_orders_clean["quantity_received"].isnull()]["status"].value_counts()
)

print(
    purchase_orders_clean[
        purchase_orders_clean["actual_delivery_date"].isnull()]["status"].value_counts()
)

#keeping missing values as NaN until verified

#6 Validating cleaned data
#checking zero or negative quantity ordered
print(
    purchase_orders_clean[
        purchase_orders_clean["quantity_ordered"] <= 0].to_string(index=False)
)
#checking negative received quantities
print(
    purchase_orders_clean[
        purchase_orders_clean["quantity_received"] <0].to_string(index=False)
)
#checking received quantities > ordered quantities
print(
    purchase_orders_clean[
        purchase_orders_clean["quantity_received"] > purchase_orders_clean["quantity_ordered"]].to_string(index=False)
)

#replacing invalid negative received quantities with NaN
purchase_orders_clean.loc[
    purchase_orders_clean["quantity_received"] < 0,
    "quantity_received"
] = float("nan")

#checking remaining negative received quantities
print(
    purchase_orders_clean[
        purchase_orders_clean["quantity_received"] < 0
    ].to_string(index=False)
)

#7 Saving cleaned data
purchase_orders_clean.to_csv("purchase_orders_clean.csv", index=False)




## Supplier data Profiling & Cleaning ##
#1. Loading suppliers data
suppliers=pd.read_csv("suppliers_raw.csv")
#checking basic info
print(suppliers.head())
print(suppliers.shape)
print(suppliers.info())

#2. Checking for duplicates
print(
    suppliers[
        suppliers.duplicated(subset="supplier_id",keep=False)
    ].to_string(index=False)
)
suppliers_clean=suppliers.drop_duplicates(subset="supplier_id")
#3. Standardizing formats
#standardizing country names
suppliers_clean["country"]=(
    suppliers_clean["country"].str.strip().str.upper()
)
print(suppliers_clean["country"].unique())

#4. Checking for missing values
print(suppliers_clean.isnull().sum())
#displaying suppliers with missing values
print(
    suppliers_clean[
        suppliers_clean.isnull().any(axis=1)].to_string(index=False) 
)
#5. Validating lead times
#checking zero or negative lead times
print(
    suppliers_clean[
        suppliers_clean["lead_time_days"] <= 0
    ][["supplier_id", "lead_time_days"]].to_string(index=False)
)
#replacing invalid lead times with NaN
suppliers_clean.loc[
    suppliers_clean["lead_time_days"] <= 0,
    "lead_time_days"
] = float("nan")
#checking remaining missing lead times
print(
    suppliers_clean[
        suppliers_clean["lead_time_days"].isnull()
    ][["supplier_id", "lead_time_days"]].to_string(index=False)
)
#7. Checking final missing values
print(suppliers_clean.isnull().sum())

#8. Saving cleaned supplier data
suppliers_clean.to_csv("suppliers_clean.csv", index=False)

#checking final cleaned data
print(suppliers_clean.to_string(index=False))