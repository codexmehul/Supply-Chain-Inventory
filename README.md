# Supply Chain & Inventory Analytics

An end-to-end data analytics project focused on evaluating stock levels, supplier performance, fulfillment delays, and product profitability across 15,000 transaction records to optimize inventory management and operational efficiency[cite: 3].

---

## 📌 Project Overview
Inefficient inventory planning and fulfillment delays directly impact working capital, customer satisfaction, and profitability# Supply Chain & Inventory Performance Analysis

## Executive Summary
This project analyzes end-to-end supply chain operations and inventory dynamics using an enterprise dataset of 15,000 records. The primary objective is to evaluate supplier reliability, mitigate delivery bottlenecks, prevent stockouts/overstocking, and identify high-margin product lines. Through structured data cleaning, exploratory data analysis (EDA), and interactive business intelligence dashboards, this project translates raw operational logs into actionable inventory optimization strategies.

---

## Key Business Objectives & Questions Addressed
* **Stock Optimization:** Which products are frequently understocked (stockout risk) versus overstocked (high holding costs)[cite: 1]?
* **Vendor Accountability:** Which suppliers consistently incur the longest delivery delays, and how does this affect lead times[cite: 1]?
* **Profitability Mapping:** Which product categories and SKUs drive the highest aggregate profit margins versus those operating at thin or negative spreads[cite: 1]?
* **Operational Velocity:** What are the fastest-moving SKUs versus slow-moving inventory across different warehouse locations[cite: 1]?

---

## Dataset Schema
The underlying operational dataset contains 15,000 transaction records with the following attributes[cite: 1]:

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `Product_ID`[cite: 1] | Categorical / String | Unique identifier for the product[cite: 1] |
| `Product_Name`[cite: 1] | String | SKU name[cite: 1] |
| `Category`[cite: 1] | Categorical | High-level product segment[cite: 1] |
| `Supplier_Name`[cite: 1] | String | Vendor responsible for fulfillment[cite: 1] |
| `Order_Date`[cite: 1] | Date | Timestamp of order placement[cite: 1] |
| `Delivery_Date`[cite: 1] | Date | Timestamp of warehouse receipt[cite: 1] |
| `Stock_Quantity`[cite: 1] | Integer | Current available warehouse inventory[cite: 1] |
| `Reorder_Level`[cite: 1] | Integer | Minimum threshold triggering replenishment[cite: 1] |
| `Units_Sold`[cite: 1] | Integer | Total units sold across the tracked period[cite: 1] |
| `Purchase_Cost`[cite: 1] | Decimal | Unit cost of acquisition[cite: 1] |
| `Selling_Price`[cite: 1] | Decimal | Unit price sold to customer[cite: 1] |
| `Warehouse_Location`[cite: 1] | Categorical | Geographic or facility identifier[cite: 1] |
| `Shipping_Time_Days`[cite: 1] | Integer | Total transit time from order to delivery[cite: 1] |

---

## Analytical Workflow

### 1. Data Cleaning & Integrity Audits
* Deduplicated records across unique order and product instances[cite: 1].
* Handled missing/null values across cost and operational metrics[cite: 1].
* Standardized date parsing for `Order_Date` and `Delivery_Date`[cite: 1].
* Enforced schema integrity and validated numeric fields (e.g., verifying `Stock_Quantity >= 0` and `Selling_Price >= Purchase_Cost`)[cite: 1].

### 2. Core Metrics & KPI Formulations
* **Total Revenue:** Calculated as $\sum (\text{Units\_Sold} \times \text{Selling\_Price})$[cite: 1].
* **Gross Profit:** Evaluated per transaction as $(\text{Selling\_Price} - \text{Purchase\_Cost}) \times \text{Units\_Sold}$[cite: 1].
* **Inventory Ratio:** Stock Available vs. Units Sold to classify SKUs into overstocked, balanced, or critical stockout territory[cite: 1].
* **Supplier Lead Time:** Mean and variance analysis of `Shipping_Time_Days` per supplier[cite: 1].

### 3. Business Insights Extracted
* **Inventory Classification:** Segmented inventory into fast-moving vs. deadstock/slow-moving units based on sales velocity and holding periods[cite: 1].
* **Vendor Benchmarking:** Ranked suppliers based on average shipping delays and fulfillment consistency[cite: 1].
* **Margin Profiling:** Identified top-grossing products versus low-margin SKUs requiring pricing or supplier renegotiation[cite: 1].

---

## Dashboard Architecture
The interactive dashboard (Excel / Power BI) provides executive decision-makers with real-time operational monitoring[cite: 1]:
* **Executive Summary KPIs:** Total Revenue, Gross Profit, Total Units Sold, Average Shipping Delay[cite: 1].
* **Inventory Health View:** Stock Level vs. Reorder Level gauge, highlighting products at immediate risk of depletion[cite: 1].
* **Vendor Scorecard:** Scatter/bar visualization comparing supplier shipping delays against overall volume fulfilled[cite: 1].
* **Product Performance Matrix:** Top 10 revenue-generating SKUs vs. bottom-margin performers[cite: 1].

---

## Project Structure
```text
├── data/
│   ├── raw/
│   │   └── supply_chain_inventory_raw.csv
│   └── processed/
│       └── supply_chain_inventory_cleaned.csv
├── sql/
│   ├── 01_data_cleaning.sql
│   ├── 02_kpi_calculations.sql
│   └── 03_business_queries.sql
├── dashboard/
│   └── supply_chain_executive_dashboard.pbix (or .xlsx)
├── reports/
│   └── supply_chain_insights_summary.pdf
└── README.md
