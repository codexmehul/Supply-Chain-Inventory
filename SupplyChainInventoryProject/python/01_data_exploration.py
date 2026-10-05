"""
===============================================================================
Supply Chain & Inventory Analysis Project
Script 01: Initial Data Exploration (EDA)
-------------------------------------------------------------------------------
Purpose:
  This script performs an initial exploratory analysis of the raw Excel dataset.
  It checks data structure, types, missing values, duplicate records, range 
  distributions, and domain-specific supply chain logic (e.g. date validation).

Author: Mentor & Mentee
===============================================================================
"""

import os
import pandas as pd

def explore_supply_chain_data(file_path):
    """
    Reads the raw Excel dataset and prints diagnostic summary reports.
    """
    print("=" * 80)
    print(" STEP 1: LOADING RAW DATASET")
    print("=" * 80)
    
    # Verify file existence before reading
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found at path: {file_path}")
        
    print(f"Loading data from: {file_path} ...")
    df = pd.read_excel(file_path)
    print("Dataset successfully loaded!")
    
    # 1. Dataset Shape (Rows & Columns)
    print("\n" + "=" * 80)
    print(" 1. DATASET DIMENSIONS")
    print("=" * 80)
    rows, cols = df.shape
    print(f"Total Rows (Records):    {rows:,}")
    print(f"Total Columns (Fields): {cols}")
    
    # 2. Schema and Data Types
    print("\n" + "=" * 80)
    print(" 2. COLUMN NAMES & DATA TYPES")
    print("=" * 80)
    for col, dtype in df.dtypes.items():
        print(f" - {col:<22} : {dtype}")
        
    # 3. Missing Values & Null Count Check
    print("\n" + "=" * 80)
    print(" 3. MISSING VALUE / NULL AUDIT")
    print("=" * 80)
    null_counts = df.isnull().sum()
    total_nulls = null_counts.sum()
    if total_nulls == 0:
        print(" SUCCESS: No missing or null values found in any column!")
    else:
        print(" WARNING: Found missing values in the following columns:")
        print(null_counts[null_counts > 0])
        
    # 4. Duplicate Records Check
    print("\n" + "=" * 80)
    print(" 4. DUPLICATE RECORDS AUDIT")
    print("=" * 80)
    duplicate_count = df.duplicated().sum()
    print(f"Duplicate Rows Count: {duplicate_count}")
    
    # 5. Numerical Columns Summary Statistics
    print("\n" + "=" * 80)
    print(" 5. NUMERICAL METRICS SUMMARY (Min, Max, Mean, Median)")
    print("=" * 80)
    num_cols = ['Stock_Quantity', 'Reorder_Level', 'Units_Sold', 'Purchase_Cost', 'Selling_Price', 'Shipping_Time_Days']
    print(df[num_cols].describe().T[['count', 'mean', 'std', 'min', '50%', 'max']])
    
    # 6. Categorical Columns Summary
    print("\n" + "=" * 80)
    print(" 6. CATEGORICAL FIELDS EXPLORATION")
    print("=" * 80)
    print(f"Unique Categories ({df['Category'].nunique()}):", df['Category'].unique().tolist())
    print(f"Unique Warehouses ({df['Warehouse_Location'].nunique()}):", df['Warehouse_Location'].unique().tolist())
    print(f"Unique Suppliers ({df['Supplier_Name'].nunique()}):", df['Supplier_Name'].unique().tolist())
    print(f"Unique Products ({df['Product_Name'].nunique()}):", df['Product_Name'].unique().tolist())
    
    # 7. Supply Chain Business Rule Checks
    print("\n" + "=" * 80)
    print(" 7. DOMAIN & BUSINESS RULE VALIDATIONS")
    print("=" * 80)
    
    # Check 7a: Negative quantities or prices
    neg_stock = (df['Stock_Quantity'] < 0).sum()
    neg_cost = (df['Purchase_Cost'] < 0).sum()
    neg_price = (df['Selling_Price'] < 0).sum()
    print(f" - Negative Stock Records:    {neg_stock}")
    print(f" - Negative Purchase Cost:    {neg_cost}")
    print(f" - Negative Selling Price:    {neg_price}")
    
    # Check 7b: Date integrity (Delivery_Date should be >= Order_Date)
    date_anomalies = (df['Delivery_Date'] < df['Order_Date']).sum()
    print(f" - Date Anomalies (Delivery < Order): {date_anomalies}")
    
    # Check 7c: Shipping Days consistency
    calc_days = (df['Delivery_Date'] - df['Order_Date']).dt.days
    shipping_mismatch = (calc_days != df['Shipping_Time_Days']).sum()
    print(f" - Shipping Days Mismatch:            {shipping_mismatch}")
    
    # Check 7d: Reorder Alert Indicator count
    reorder_alert_count = (df['Stock_Quantity'] <= df['Reorder_Level']).sum()
    print(f" - Items at or below Reorder Level:   {reorder_alert_count:,} ({(reorder_alert_count/rows)*100:.2f}%)")

    print("\n" + "=" * 80)
    print(" EXPLORATION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    # Define relative raw data path
    raw_data_path = os.path.join("data", "raw", "Project-03 supply_chain_inventory_dataset_15000_rows 2.xlsx")
    explore_supply_chain_data(raw_data_path)
