--1. Checking cleaned inventory data
SELECT *
FROM inventory_clean
LIMIT 10;

--2. Counting inventory records
SELECT COUNT(*) AS total_records
FROM inventory_clean;

--3. Finding latest inventory records
SELECT
    *,
    ROW_NUMBER() OVER (
        PARTITION BY product_id, warehouse_id
        ORDER BY date DESC
    ) AS rn
FROM inventory_clean
LIMIT 20;

--4. Creating latest inventory table
DROP TABLE IF EXISTS latest_inventory;

CREATE TABLE latest_inventory AS
SELECT
    inventory_id,
    product_id,
    warehouse_id,
    date,
    stock_on_hand,
    reorder_point,
    safety_stock
FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY product_id, warehouse_id
            ORDER BY date DESC, inventory_id DESC
        ) AS rn
    FROM inventory_clean
)
WHERE rn = 1;


--5. Checking latest inventory
SELECT *
FROM latest_inventory
LIMIT 20;

--6. Identifying products requiring reorder
SELECT
    product_id,
    warehouse_id,
    date,
    stock_on_hand,
    reorder_point,
    safety_stock,
    reorder_point - stock_on_hand AS shortage
FROM latest_inventory
WHERE stock_on_hand IS NOT NULL
  AND reorder_point IS NOT NULL
  AND stock_on_hand >= 0
  AND stock_on_hand <= reorder_point
ORDER BY shortage DESC;