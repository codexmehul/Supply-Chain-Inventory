-- ===============================================================================
-- Supply Chain & Inventory Analysis Project
-- Query 03: Sales & Financial Profitability Analysis
-- -------------------------------------------------------------------------------
-- Purpose:
--   Analyze financial revenue, total costs, net profit, and profit margin % 
--   across categories and individual products.
-- ===============================================================================

-- -------------------------------------------------------------------------------
-- 3.1: Financial Performance by Product Category
-- Compares revenue, total cost, net profit, and margin % across categories.
-- -------------------------------------------------------------------------------
SELECT 
    Category,
    SUM(Units_Sold) AS Total_Units_Sold,
    ROUND(SUM(Total_Revenue), 2) AS Total_Revenue_INR,
    ROUND(SUM(Total_Cost), 2) AS Total_Cost_INR,
    ROUND(SUM(Profit), 2) AS Total_Net_Profit_INR,
    ROUND(SUM(Profit) * 100.0 / SUM(Total_Revenue), 2) AS Profit_Margin_Pct
FROM inventory_data
GROUP BY Category
ORDER BY Total_Net_Profit_INR DESC;


-- -------------------------------------------------------------------------------
-- 3.2: Product Profitability Breakdown
-- Aggregates performance by Product Name to see top profitable products.
-- -------------------------------------------------------------------------------
SELECT 
    Product_Name,
    Category,
    SUM(Units_Sold) AS Total_Units_Sold,
    ROUND(AVG(Purchase_Cost), 2) AS Avg_Purchase_Cost,
    ROUND(AVG(Selling_Price), 2) AS Avg_Selling_Price,
    ROUND(AVG(Unit_Profit), 2) AS Avg_Unit_Profit,
    ROUND(SUM(Total_Revenue), 2) AS Total_Revenue_INR,
    ROUND(SUM(Profit), 2) AS Total_Net_Profit_INR,
    ROUND(SUM(Profit) * 100.0 / SUM(Total_Revenue), 2) AS Profit_Margin_Pct
FROM inventory_data
GROUP BY Product_Name, Category
ORDER BY Total_Net_Profit_INR DESC;
