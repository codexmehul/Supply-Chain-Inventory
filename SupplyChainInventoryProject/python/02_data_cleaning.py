"""
===============================================================================
Supply Chain & Inventory Analysis Project
Script 02: Python Data Cleaning & Feature Engineering
-------------------------------------------------------------------------------
Purpose:
  This script reads the raw Excel dataset, performs feature engineering to create
  essential financial and inventory metrics, exports a cleaned CSV file, and 
  populates an SQLite database for subsequent SQL business queries.

Key Metrics Created:
  1. Total_Revenue       = Units_Sold * Selling_Price
  2. Total_Cost          = Units_Sold * Purchase_Cost
  3. Profit              = Total_Revenue - Total_Cost
  4. Profit_Margin_Pct   = (Profit / Total_Revenue) * 100
  5. Unit_Profit         = Selling_Price - Purchase_Cost
  6. Holding_Value       = Stock_Quantity * Purchase_Cost
  7. Reorder_Status      = 'Reorder Needed' or 'Stock Sufficient'
  8. Stockout_Risk       = 'High Risk', 'Medium Risk', or 'Low Risk'

Author: Mentor & Mentee
===============================================================================
"""

import os
import sqlite3
import pandas as pd
import numpy as np

def clean_and_transform_data():
    """
    Main function to load raw data, perform transformations, and output CSV & SQLite DB.
    """
    print("=" * 80)
    print(" STEP 2: STARTING DATA CLEANING & FEATURE ENGINEERING")
    print("=" * 80)
    
    # 1. Define file paths
    raw_file = os.path.join("data", "raw", "Project-03 supply_chain_inventory_dataset_15000_rows 2.xlsx")
    cleaned_csv = os.path.join("data", "cleaned", "cleaned_supply_chain_data.csv")
    db_file = os.path.join("data", "cleaned", "inventory_analysis.db")
    
    # Ensure cleaned output directory exists
    os.makedirs(os.path.dirname(cleaned_csv), exist_ok=True)
    
    # 2. Read raw dataset
    print(f"Reading raw dataset from: {raw_file}...")
    df = pd.read_excel(raw_file)
    print(f"Loaded {len(df):,} rows successfully.")
    
    # 3. Feature Engineering - Financial Calculations
    print("\nCalculating Financial Metrics...")
    df['Total_Revenue'] = df['Units_Sold'] * df['Selling_Price']
    df['Total_Cost'] = df['Units_Sold'] * df['Purchase_Cost']
    df['Profit'] = df['Total_Revenue'] - df['Total_Cost']
    
    # Calculate Profit Margin % safely (handling zero revenue edge cases)
    df['Profit_Margin_Pct'] = np.where(
        df['Total_Revenue'] > 0,
        (df['Profit'] / df['Total_Revenue']) * 100,
        0.0
    ).round(2)
    
    df['Unit_Profit'] = df['Selling_Price'] - df['Purchase_Cost']
    df['Holding_Inventory_Value'] = df['Stock_Quantity'] * df['Purchase_Cost']
    
    # 4. Feature Engineering - Inventory Status Flags
    print("Calculating Inventory & Stockout Flags...")
    
    # Reorder Status: Simple binary indicator based on Reorder Level threshold
    df['Reorder_Status'] = np.where(
        df['Stock_Quantity'] <= df['Reorder_Level'],
        'Reorder Needed',
        'Stock Sufficient'
    )
    
    # Stockout Risk Categorization: 3-tier risk level
    conditions = [
        (df['Stock_Quantity'] == 0),
        (df['Stock_Quantity'] <= df['Reorder_Level'])
    ]
    choices = ['High Risk', 'Medium Risk']
    df['Stockout_Risk'] = np.select(conditions, choices, default='Low Risk')
    
    # 5. Format Dates for Consistency (YYYY-MM-DD)
    df['Order_Date'] = pd.to_datetime(df['Order_Date']).dt.strftime('%Y-%m-%d')
    df['Delivery_Date'] = pd.to_datetime(df['Delivery_Date']).dt.strftime('%Y-%m-%d')
    
    # 6. Display Sample Cleaned Data
    print("\nSample Cleaned & Transformed Records:")
    sample_cols = [
        'Product_ID', 'Product_Name', 'Category', 'Stock_Quantity', 
        'Reorder_Level', 'Reorder_Status', 'Total_Revenue', 'Profit', 'Profit_Margin_Pct'
    ]
    print(df[sample_cols].head(3).to_string())
    
    # 7. Export to Cleaned CSV
    print(f"\nExporting cleaned dataset to CSV: {cleaned_csv}...")
    df.to_csv(cleaned_csv, index=False)
    print("CSV export complete!")
    
    # 8. Export to SQLite Database
    print(f"Populating SQLite Database: {db_file}...")
    conn = sqlite3.connect(db_file)
    
    # Write dataframe to table 'inventory_data'
    df.to_sql('inventory_data', conn, if_exists='replace', index=False)
    
    # Verify row count in SQLite table
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM inventory_data;")
    db_count = cursor.fetchone()[0]
    conn.close()
    
    print(f"SQLite database population complete! Table 'inventory_data' contains {db_count:,} records.")
    print("=" * 80)
    print(" STEP 2 COMPLETE: CLEANING & DATABASE LOADING SUCCESSFUL")
    print("=" * 80)

if __name__ == "__main__":
    clean_and_transform_data()
