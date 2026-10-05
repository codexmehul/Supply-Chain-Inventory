"""
===============================================================================
Supply Chain & Inventory Analysis Project
Script 03: SQL Analysis Execution Runner
-------------------------------------------------------------------------------
Purpose:
  Connects to the SQLite database (data/cleaned/inventory_analysis.db),
  reads and executes all SQL analytical files in the sql/ folder, and prints 
  formatted result tables for mentor & mentee review.


===============================================================================
"""

import os
import sqlite3
import pandas as pd

def run_sql_script(db_path, sql_file_path):
    """
    Executes all queries inside a .sql file against the SQLite database
    and displays each query's output using pandas DataFrame formatting.
    """
    if not os.path.exists(sql_file_path):
        print(f"Error: File {sql_file_path} not found.")
        return

    print("\n" + "=" * 80)
    print(f" EXECUTING SQL FILE: {os.path.basename(sql_file_path)}")
    print("=" * 80)

    # Read SQL file content
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Separate individual SQL queries by semicolon ';'
    raw_queries = sql_content.split(';')
    
    conn = sqlite3.connect(db_path)
    
    query_index = 1
    for raw_query in raw_queries:
        # Strip comments and whitespace to check if query contains SQL statements
        lines = [line for line in raw_query.strip().split('\n') if not line.strip().startswith('--')]
        clean_query = "\n".join(lines).strip()
        
        if not clean_query:
            continue
            
        print(f"\n--- Query {query_index} Results ---")
        try:
            df = pd.read_sql(clean_query, conn)
            print(df.to_string(index=False))
            query_index += 1
        except Exception as e:
            print(f"Execution Error: {e}")
            
    conn.close()
    print("\n" + "=" * 80)

def main():
    db_path = os.path.join("data", "cleaned", "inventory_analysis.db")
    sql_files = [
        os.path.join("sql", "01_inventory_health.sql"),
        os.path.join("sql", "02_supplier_performance.sql"),
        os.path.join("sql", "03_sales_profitability.sql"),
        os.path.join("sql", "04_warehouse_efficiency.sql")
    ]

    print(f"Connecting to SQLite Database: {db_path}...")
    for sql_file in sql_files:
        run_sql_script(db_path, sql_file)

if __name__ == "__main__":
    main()