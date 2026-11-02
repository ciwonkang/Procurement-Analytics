## Project Overview

An end-to-end procurement analytics portfolio project using **Python, SQL, and Excel** to analyze purchasing expenditures, supplier concentration, and inventory replenishment priorities.

## Tools & Technologies

- **Python (pandas):** Data cleaning, transformation, spend analysis, and ABC classification
- **SQL (SQLite):** Latest inventory identification and reorder candidate extraction
- **Excel:** XLOOKUP, PivotTables, and conditional formatting

## Analysis

### 1. Product Spend Analysis
- Calculated estimated purchasing spend using ordered quantities and product unit costs.
- Performed ABC classification on 76 products.
- A-class products accounted for approximately 78.9% of estimated spend.

### 2. Supplier Spend Analysis
- Analyzed purchasing expenditure across 12 suppliers.
- The largest supplier accounted for approximately 13.9% of estimated spend.
- The top three suppliers accounted for approximately 36.9%.

### 3. Inventory Reorder Analysis
- Identified the latest inventory record for each product and warehouse using SQL window functions.
- Flagged inventory records where stock on hand was at or below the reorder point.
- Identified 6 product–warehouse combinations for replenishment review, with a combined reorder-point gap of 337 units.
- Used Excel XLOOKUP and PivotTables to summarize results by warehouse and product.

## Project Workflow

Raw CSV Data → Python Data Cleaning → Spend & Supplier Analysis

Cleaned Inventory Data → SQLite Reorder Analysis → Excel Reporting

## Repository Structure

- `python/` — Python data preparation and analysis scripts
- `sql/` — SQL inventory analysis
- `excel/` — Excel inventory reporting workbook
- `results/` — Analysis output CSV files

## Data Source

This project uses a synthetic supply chain dataset from [Ritiika16 — Supply Chain Inventory Analytics](https://github.com/Ritiika16/Supply-Chain-Inventory-Analytics).

The analysis and reporting workflow presented here was developed as an independent portfolio exercise.

## Limitations

- Purchasing expenditure is estimated using ordered quantity and unit cost.
- Reorder-point gaps do not represent finalized purchase order quantities.
- The analysis uses synthetic data and does not represent actual LG Electronics operations.
