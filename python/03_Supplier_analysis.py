import pandas as pd


## Supplier Analysis ##
#1. Loading cleaned data
products=pd.read_csv("products_clean.csv")
purchase_orders=pd.read_csv("purchase_orders_clean.csv")
suppliers=pd.read_csv("suppliers_clean.csv")

#2. Merging products and purchase orders
supplier_data=purchase_orders.merge(
    products[["product_id","unit_cost"]],
    on="product_id",
    how="left",
    validate="many_to_one"
)
supplier_data=supplier_data.merge(
    suppliers[["supplier_id",
               "supplier_name",
               "country",
               "lead_time_days",
               "reliability_score"]],
               on="supplier_id",
               how="left",
               validate="many_to_one"
)
print(supplier_data.head().to_string(index=False))

#3. Calculating estimated purchase order value
supplier_data["estimated_value"]=(
    supplier_data["quantity_ordered"]*supplier_data["unit_cost"]
)

#4. Supplier Spend Analysis
supplier_spend=supplier_data.groupby(
    ["supplier_id","supplier_name"],
    as_index=False
)["estimated_value"].sum(min_count=1)

#5. Sorting suppliers by total spend
supplier_spend=supplier_spend.sort_values(
    by="estimated_value",
    ascending=False
)

print(supplier_spend.to_string(index=False))

#6. Calculating supplier spend percentage
supplier_spend["spend_pct"]=(
    supplier_spend["estimated_value"]/
    supplier_spend["estimated_value"].sum()*100
)
print(supplier_spend.to_string(index=False))

#6. Calculating cumulative spend percentage
supplier_spend["cumulative_pct"]=supplier_spend["spend_pct"].cumsum()

print(supplier_spend.to_string(index=False))

#7 Saving
supplier_spend.to_csv("supplier_spend.csv", index=False)