-- ===============================================================================
-- Supply Chain & Inventory Analysis Project
-- Query 01: Inventory Health & Stockout Risk Analysis
-- -------------------------------------------------------------------------------
-- Purpose:
--   Analyze stock levels, reorder thresholds, inventory value tied up in warehouses,
--   and identify products at high risk of stockouts.
-- ===============================================================================

-- -------------------------------------------------------------------------------
-- 1.1: Reorder Status Overview
-- Summary count and percentage of products needing stock replenishment.
-- -------------------------------------------------------------------------------
SELECT 
    Reorder_Status,
    COUNT(*) AS Product_Count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM inventory_data), 2) AS Percentage_Share,
    SUM(Stock_Quantity) AS Total_Stock_Units,
    ROUND(SUM(Holding_Inventory_Value), 2) AS Total_Holding_Value_INR
FROM inventory_data
GROUP BY Reorder_Status;


-- -------------------------------------------------------------------------------
-- 1.2: Inventory Holding Value by Category
-- Measures working capital tied up in stock across categories.
-- -------------------------------------------------------------------------------
SELECT 
    Category,
    COUNT(DISTINCT Product_ID) AS Total_Product_Types,
    SUM(Stock_Quantity) AS Total_Units_In_Stock,
    ROUND(SUM(Holding_Inventory_Value), 2) AS Total_Holding_Value_INR,
    ROUND(AVG(Stock_Quantity), 1) AS Avg_Stock_Per_Item
FROM inventory_data
GROUP BY Category
ORDER BY Total_Holding_Value_INR DESC;


-- -------------------------------------------------------------------------------
-- 1.3: Top 10 High Risk / Low Stock Products
-- Identifies specific products where stock is lowest relative to reorder level.
-- -------------------------------------------------------------------------------
SELECT 
    Product_ID,
    Product_Name,
    Category,
    Warehouse_Location,
    Stock_Quantity,
    Reorder_Level,
    (Reorder_Level - Stock_Quantity) AS Deficit_Units,
    Stockout_Risk
FROM inventory_data
WHERE Stock_Quantity <= Reorder_Level
ORDER BY Deficit_Units DESC
LIMIT 10;
