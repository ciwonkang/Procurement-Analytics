import pandas as pd

## Spend Analysis ##

#1. Loading cleaned data
products=pd.read_csv("products_clean.csv")
purchase_orders=pd.read_csv("purchase_orders_clean.csv")

#2. Merging products and purchase orders
spend=purchase_orders.merge(products[["product_id","product_name","category","unit_cost"]],
                            on="product_id",
                            how="left",
                            validate="many_to_one")

print(spend.head())
print(spend.shape)

#3. calculating estimated purchase order value
spend["estimated_value"]=(spend["quantity_ordered"]*spend["unit_cost"])
print(spend[
    ["po_id","product_id","quantity_ordered","unit_cost","estimated_value"]
].head(10).to_string(index=False))

#4. Spend Analysis by product id
#calculating total estimated purchase value by product id
product_spend=spend.groupby(
    ["product_id","product_name","category"],
    as_index=False
)["estimated_value"].sum(min_count=1)
#excluding products with missing estimated purchase price
product_spend=product_spend.dropna(subset=["estimated_value"])
#sorting products by total purchase value
product_spend = product_spend.sort_values(
    by="estimated_value",
    ascending=False
)
#displaying top 10 products by purchase value
print(product_spend.head(10).to_string(index=False))

#5. ABC analysis
#calculating percentage of total estimated purchase value
product_spend["spend_pct"]=(
    product_spend["estimated_value"]/
    product_spend["estimated_value"].sum()*100
)
#calculating cumulative percentage
product_spend["cumulative_pct"]=product_spend["spend_pct"].cumsum()
#assigning ABC categories
product_spend["abc_category"]="C"
product_spend.loc[product_spend["cumulative_pct"]<=80, "abc_category"]="A"
product_spend.loc[(product_spend["cumulative_pct"]>80) & (product_spend["cumulative_pct"]<=95), "abc_category"]="B"
#displaying ABC analysis
print(product_spend.head(15).to_string(index=False))
print(product_spend.head(100).to_string(index=False))
print(product_spend.shape)

#checking negative estimated purchase values
print(spend[spend["estimated_value"] < 0][
    ["po_id", "product_id", "quantity_ordered",
     "unit_cost", "estimated_value"]
].to_string(index=False))

#6. Saving
product_spend.to_csv("product_spend.csv", index=False)