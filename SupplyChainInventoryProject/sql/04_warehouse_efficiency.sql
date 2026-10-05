-- ===============================================================================
-- Supply Chain & Inventory Analysis Project
-- Query 04: Regional Warehouse Operational Performance
-- -------------------------------------------------------------------------------
-- Purpose:
--   Evaluate fulfillment speed, inventory distribution, total sales volume, 
--   and revenue across regional warehouse hubs (Chennai, Hyderabad, Bangalore, Mumbai, Delhi).
-- ===============================================================================

-- -------------------------------------------------------------------------------
-- 4.1: Warehouse Hub Performance Overview
-- Compares sales volume, revenue, current inventory, and shipping speed across hubs.
-- -------------------------------------------------------------------------------
SELECT 
    Warehouse_Location,
    COUNT(*) AS Total_Orders_Processed,
    SUM(Units_Sold) AS Total_Units_Sold,
    SUM(Stock_Quantity) AS Total_Current_Stock_Units,
    ROUND(SUM(Holding_Inventory_Value), 2) AS Total_Holding_Value_INR,
    ROUND(SUM(Total_Revenue), 2) AS Total_Revenue_INR,
    ROUND(SUM(Profit), 2) AS Total_Profit_INR,
    ROUND(AVG(Shipping_Time_Days), 2) AS Avg_Fulfillment_Days
FROM inventory_data
GROUP BY Warehouse_Location
ORDER BY Total_Revenue_INR DESC;


-- -------------------------------------------------------------------------------
-- 4.2: Stockout Risk Distribution by Warehouse Location
-- Identifies warehouses with disproportionate stockout risk levels.
-- -------------------------------------------------------------------------------
SELECT 
    Warehouse_Location,
    SUM(CASE WHEN Stockout_Risk = 'High Risk' THEN 1 ELSE 0 END) AS High_Risk_Items,
    SUM(CASE WHEN Stockout_Risk = 'Medium Risk' THEN 1 ELSE 0 END) AS Medium_Risk_Items,
    SUM(CASE WHEN Stockout_Risk = 'Low Risk' THEN 1 ELSE 0 END) AS Low_Risk_Items,
    ROUND(SUM(CASE WHEN Stockout_Risk IN ('High Risk', 'Medium Risk') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS At_Risk_Pct
FROM inventory_data
GROUP BY Warehouse_Location
ORDER BY At_Risk_Pct DESC;
