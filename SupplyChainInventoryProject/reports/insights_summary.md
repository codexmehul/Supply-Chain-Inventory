# Supply Chain & Inventory Analytics - Executive Insights Summary

**Dataset Overview:** 15,000 Order & Inventory Records across 5 Indian Regional Hubs  
**Author:** Senior Data Analyst Mentor & Mentee  

---

## 📊 1. Financial Performance Highlights
- **Total Revenue:** **₹2,940,366,139** (~₹2.94 Billion)
- **Total Cost of Goods Sold:** **₹2,353,427,940** (~₹2.35 Billion)
- **Total Net Profit:** **₹586,938,199** (~₹586.94 Million)
- **Overall Profit Margin:** **19.96%** (Consistently healthy across all product lines)
- **Top Revenue & Profit Category:** **Fashion** generated **₹792.04M Revenue** and **₹157.85M Net Profit**.
- **Top Margin Category:** **Sports** yielded the highest profit margin at **20.02%**.

---

## 📦 2. Inventory Health & Stockout Risk
- **Total Stock Value Tied Up:** **₹4.14 Billion** (₹4,140,161,239) in working capital across 3.76M units.
- **Stockout Alert Rate:** **3,015 items (20.10%)** are at or below their designated reorder thresholds.
- **Critical Risk (Out of Stock):** **32 items** have `Stock_Quantity = 0`, causing active sales loss.
- **Tied-up Capital Breakdown:**
  - **Sufficient Stock Items:** ₹3.96 Billion (79.90% of SKUs)
  - **Reorder Needed Items:** ₹180.87 Million (20.10% of SKUs)

---

## 🚚 3. Supplier Lead Time & Reliability
- **Average Fulfillment Lead Time:** **5.50 days** across all suppliers.
- **Fastest Vendor:** **Supplier C** maintains the fastest average lead time at **5.39 days** (₹124.05M Net Profit).
- **Highest Volume Vendor:** **Supplier E** processed the highest units (452,768 units) and highest net profit (₹125.55M), with a 5.55-day average lead time.
- **Lowest Vendor:** **Supplier D** processed the lowest volume (431,563 units) and lowest net profit (₹117.39M).

---

## 🏭 4. Regional Warehouse Hub Comparison

| Warehouse Location | Revenue (INR) | Net Profit (INR) | Avg Lead Time | Stockout Risk Rate |
|---|---|---|---|---|
| **Bangalore** | **₹624.50M** | ₹123.38M | 5.55 days | **18.89%** (Best) |
| **Mumbai** | ₹623.02M | **₹124.65M** | 5.53 days | 20.34% |
| **Hyderabad** | ₹618.36M | ₹124.46M | **5.44 days** | 20.02% |
| **Delhi** | ₹606.45M | ₹120.91M | **5.43 days** (Fastest) | 20.36% |
| **Chennai** | ₹603.98M | ₹119.52M | 5.53 days | **20.90%** (Highest Risk) |

---

## 🎯 5. Top 3 Strategic Recommendations
1. **Automate Reorder Triggers:** Immediately replenish the 3,015 at-risk items (specifically the 32 zero-stock items) to capture lost sales opportunities.
2. **Rebalance Regional Inventory:** Transfer buffer stock from Bangalore (lowest risk at 18.89%) to Chennai (highest risk at 20.90%).
3. **Optimize Supplier Allocation:** Prioritize Supplier C (5.39 days) for high-demand, fast-moving items to minimize stockout windows.
