# Executive Summary: Supply Chain & Inventory Analysis

**Project Title:** Professional Supply Chain & Inventory Analytics  
**Author:** Senior Data Analyst Mentor & Mentee  
**Database:** SQLite (`inventory_analysis.db`) | **Dataset Size:** 15,000 Records  

---

## 1. Executive Summary & Scope

This report presents an end-to-end data analysis of **15,000 supply chain records** spanning inventory levels, procurement costs, sales prices, shipping lead times, supplier performance, and regional warehouse hubs across India (Chennai, Hyderabad, Bangalore, Mumbai, Delhi).

### Key Takeaways:
- **Total Working Capital Tied Up:** **₹4.14 Billion** (₹4,140,161,239) in total stock value.
- **Stockout Vulnerability:** **3,015 records (20.10%)** are currently at or below their designated reorder threshold, representing immediate fulfillment risk.
- **Top Financial Category:** **Fashion** generated **₹792.04M in Revenue** and **₹157.85M in Net Profit**.
- **Most Efficient Supplier:** **Supplier C** maintains the fastest average shipping lead time of **5.39 days**.
- **Top Regional Warehouse:** **Bangalore Hub** leads in revenue generation (**₹624.50M**) and lowest stockout risk (**18.89%**).

---

## 2. Business Problem & Context

Effective inventory management requires balancing **holding costs** (capital tied up in excess inventory) against **stockout risks** (lost sales and customer dissatisfaction due to missing inventory). 

This project addresses four core business challenges:
1. **Inventory Capital Allocation:** Identifying overstocked vs understocked items.
2. **Supplier Reliability & Speed:** Evaluating vendor fulfillment times and profit contribution.
3. **Product Profitability:** Analyzing gross profit margins across categories and products.
4. **Regional Warehouse Optimization:** Assessing operational throughput across regional distribution centers.

---

## 3. Data Pipeline Architecture & Methodology

``` 
| Raw Excel Data   | --> | Python Cleaning & Engineering | --> | SQLite Database       | --> | SQL Business Queries   |
| (15,000 records) |     | (02_data_cleaning.py)         |     | (inventory_data table)|     | (01 to 04 .sql files)  |
   

### Steps Implemented:
1. **Data Exploration (Python):** Audited schema integrity, checked zero nulls, zero duplicates, and verified logical date constraints.
2. **Feature Engineering (Python):** Computed financial metrics (`Total_Revenue`, `Total_Cost`, `Profit`, `Profit_Margin_Pct`, `Holding_Inventory_Value`) and inventory classification flags (`Reorder_Status`, `Stockout_Risk`).
3. **Database Population (SQLite):** Loaded 15,000 cleaned rows into `inventory_analysis.db`.
4. **Analytical SQL Queries (SQL):** Aggregated metrics across inventory, supplier, financial, and warehouse dimensions.

---

## 4. Key Analytical Findings

### 4.1 Inventory Health & Stockout Risk
- **Total Stock Units:** 3,763,769 units across all warehouses.
- **Reorder Needed:** 3,015 items (20.10%) have stock $\le$ reorder level.
- **Stock Sufficient:** 11,985 items (79.90%) have stock above reorder level.

| Reorder Status | Item Count | Share (%) | Total Stock Units | Holding Inventory Value (INR) |
|---|---|---|---|---|
| **Stock Sufficient** | 11,985 | 79.90% | 3,598,539 | ₹3,959,293,000 |
| **Reorder Needed** | 3,015 | 20.10% | 165,230 | ₹180,868,100 |
| **Total** | **15,000** | **100.00%** | **3,763,769** | **₹4,140,161,100** |

---

### 4.2 Supplier Performance & Lead Time Analysis

| Supplier Name | Orders Processed | Units Sold | Avg Shipping Days | Total Revenue (INR) | Net Profit (INR) |
|---|---|---|---|---|---|
| **Supplier C** | 3,042 | 448,597 | **5.39** | ₹614,328,940 | ₹124,050,671 |
| **Supplier A** | 3,025 | 447,389 | **5.48** | ₹615,799,968 | ₹123,069,384 |
| **Supplier B** | 2,980 | 442,191 | **5.52** | ₹617,037,930 | ₹122,865,551 |
| **Supplier D** | 2,944 | 431,563 | **5.54** | ₹598,461,560 | ₹117,388,326 |
| **Supplier E** | 3,009 | 452,768 | **5.55** | ₹630,683,746 | ₹125,550,272 |

- **Lead Time Insights:** Supplier C is the fastest vendor (5.39 days avg). Supplier E handles the highest sales volume and net profit.

---

### 4.3 Sales & Financial Profitability by Category

| Category | Units Sold | Total Revenue (INR) | Total Cost (INR) | Net Profit (INR) | Profit Margin (%) |
|---|---|---|---|---|---|
| **Fashion** | 572,118 | ₹792,044,366 | ₹634,195,854 | ₹157,848,512 | 19.93% |
| **Home Appliances** | 557,625 | ₹774,324,007 | ₹621,183,781 | ₹153,140,226 | 19.78% |
| **Electronics** | 543,810 | ₹755,870,935 | ₹604,876,999 | ₹150,993,936 | 19.98% |
| **Sports** | 548,955 | ₹754,072,836 | ₹603,131,306 | ₹150,941,530 | **20.02%** |

- **Profitability Insights:** Sports yields the highest overall margin % (**20.02%**), while Fashion generates the highest net profit absolute volume (**₹157.85M**).

---

### 4.4 Regional Warehouse Operational Efficiency

| Warehouse Location | Orders Processed | Total Units Sold | Total Holding Value (INR) | Total Revenue (INR) | Net Profit (INR) | Avg Fulfillment Days | At-Risk Stock % |
|---|---|---|---|---|---|---|---|
| **Bangalore** | 3,002 | 449,298 | ₹837,255,203 | ₹624,500,120 | ₹123,382,788 | 5.55 | **18.89%** |
| **Mumbai** | 3,024 | 451,363 | ₹823,716,466 | ₹623,020,591 | ₹124,653,002 | 5.53 | 20.34% |
| **Hyderabad** | 3,032 | 447,781 | ₹837,844,709 | ₹618,364,370 | ₹124,456,767 | 5.44 | 20.02% |
| **Delhi** | 2,932 | 436,032 | ₹810,167,974 | ₹606,447,221 | ₹120,912,118 | **5.43** | 20.36% |
| **Chennai** | 3,010 | 438,034 | ₹831,176,887 | ₹603,979,842 | ₹119,519,529 | 5.53 | **20.90%** |

---

## 5. Strategic Recommendations

1. **Automate Reorder Alerts for 3,015 At-Risk SKUs:**
   Implement automated triggers for items reaching reorder thresholds to prevent stockout losses.
2. **Reallocate Stock to Chennai Warehouse:**
   Chennai has the highest stockout risk rate (20.90%). Balance stock allocation from Bangalore (18.89% risk rate) to Chennai.
3. **Leverage Supplier C for High-Demand SKUs:**
   Supplier C delivers the fastest lead times (5.39 days). Prioritize Supplier C for fast-moving items during peak demand seasons.
4. **Expand High-Margin Categories:**
   Focus sales promotion on **Sports** (20.02% margin) and **Fashion** (₹157.85M profit).

---

## 6. Power BI Dashboard Blueprint (Phase 6 Roadmap)

Once data analysis is reviewed, the Power BI dashboard will feature 4 interactive tabs:
- **Tab 1: Executive KPI Summary Cards** (Total Revenue, Total Profit, Margin %, Stockout Risk Items).
- **Tab 2: Inventory Health & Reorder Matrix** (Decomposition Tree, Stock vs Reorder Level visual).
- **Tab 3: Supplier Lead Time & Scorecard** (Scatter plot of Lead Time vs Profit).
- **Tab 4: Regional Warehouse Map & Fulfillment Slicers** (Decomposition of Regional Revenue & Risk).
