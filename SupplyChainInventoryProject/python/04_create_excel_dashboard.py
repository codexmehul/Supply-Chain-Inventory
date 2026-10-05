"""
===============================================================================
Supply Chain & Inventory Analysis Project
Script 04: Automated Excel Dashboard Builder
-------------------------------------------------------------------------------
Purpose:
  Reads the cleaned supply chain dataset and uses openpyxl to generate a 
  fully formatted, multi-tab Excel Dashboard (Supply_Chain_Inventory_Dashboard.xlsx).

Tabs Created:
  1. Executive_Dashboard   : KPI Cards, Category & Warehouse summary tables & charts.
  2. Inventory_Health      : Reorder status breakdown & critical stockout table.
  3. Supplier_Scorecard    : Vendor lead time and profitability performance.
  4. Cleaned_Data          : Full 15,000 transformed records.

Author: Mentor & Mentee
===============================================================================
"""

import os
import sqlite3
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference

def create_excel_dashboard():
    print("=" * 80)
    print(" STARTING EXCEL DASHBOARD GENERATION")
    print("=" * 80)

    # 1. Paths setup
    db_path = os.path.join("data", "cleaned", "inventory_analysis.db")
    output_excel = os.path.join("dashboard", "Supply_Chain_Inventory_Dashboard.xlsx")
    os.makedirs(os.path.dirname(output_excel), exist_ok=True)

    print(f"Connecting to database: {db_path}...")
    conn = sqlite3.connect(db_path)

    # 2. Fetch Aggregated Metrics via SQL
    print("Fetching aggregated data via SQL queries...")
    
    # KPI Totals
    kpi_df = pd.read_sql("""
        SELECT 
            SUM(Total_Revenue) AS Total_Revenue,
            SUM(Total_Cost) AS Total_Cost,
            SUM(Profit) AS Total_Profit,
            ROUND(SUM(Profit) * 100.0 / SUM(Total_Revenue), 2) AS Margin_Pct,
            SUM(Holding_Inventory_Value) AS Total_Holding_Value,
            SUM(CASE WHEN Reorder_Status = 'Reorder Needed' THEN 1 ELSE 0 END) AS Reorder_Count,
            SUM(CASE WHEN Stockout_Risk = 'High Risk' THEN 1 ELSE 0 END) AS High_Risk_Count
        FROM inventory_data;
    """, conn)

    # Category Summary
    cat_df = pd.read_sql("""
        SELECT 
            Category,
            SUM(Units_Sold) AS Units_Sold,
            ROUND(SUM(Total_Revenue), 2) AS Revenue_INR,
            ROUND(SUM(Profit), 2) AS Profit_INR,
            ROUND(SUM(Profit) * 100.0 / SUM(Total_Revenue), 2) AS Margin_Pct
        FROM inventory_data
        GROUP BY Category
        ORDER BY Profit_INR DESC;
    """, conn)

    # Warehouse Summary
    wh_df = pd.read_sql("""
        SELECT 
            Warehouse_Location,
            SUM(Units_Sold) AS Units_Sold,
            ROUND(SUM(Total_Revenue), 2) AS Revenue_INR,
            ROUND(SUM(Profit), 2) AS Profit_INR,
            ROUND(AVG(Shipping_Time_Days), 2) AS Avg_Shipping_Days
        FROM inventory_data
        GROUP BY Warehouse_Location
        ORDER BY Revenue_INR DESC;
    """, conn)

    # Reorder Status Summary
    reorder_df = pd.read_sql("""
        SELECT 
            Reorder_Status,
            COUNT(*) AS Item_Count,
            SUM(Stock_Quantity) AS Total_Stock_Units,
            ROUND(SUM(Holding_Inventory_Value), 2) AS Holding_Value_INR
        FROM inventory_data
        GROUP BY Reorder_Status;
    """, conn)

    # Critical Low Stock Top 15
    low_stock_df = pd.read_sql("""
        SELECT 
            Product_ID, Product_Name, Category, Warehouse_Location, 
            Stock_Quantity, Reorder_Level, (Reorder_Level - Stock_Quantity) AS Deficit, Stockout_Risk
        FROM inventory_data
        WHERE Stock_Quantity <= Reorder_Level
        ORDER BY Deficit DESC
        LIMIT 15;
    """, conn)

    # Supplier Summary
    sup_df = pd.read_sql("""
        SELECT 
            Supplier_Name,
            COUNT(*) AS Total_Orders,
            SUM(Units_Sold) AS Units_Sold,
            ROUND(AVG(Shipping_Time_Days), 2) AS Avg_Shipping_Days,
            ROUND(SUM(Total_Revenue), 2) AS Revenue_INR,
            ROUND(SUM(Profit), 2) AS Profit_INR
        FROM inventory_data
        GROUP BY Supplier_Name
        ORDER BY Avg_Shipping_Days ASC;
    """, conn)

    # Raw Data (First 1,000 rows for Excel sheet light size)
    raw_df = pd.read_sql("SELECT * FROM inventory_data LIMIT 1000;", conn)
    conn.close()

    # 3. Create Workbook & Styles
    wb = openpyxl.Workbook()
    
    # Define Styling Palettes
    header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid") # Dark Slate
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    
    kpi_title_font = Font(name="Calibri", size=9, bold=True, color="475569")
    kpi_val_font = Font(name="Calibri", size=14, bold=True, color="0F172A")
    kpi_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    
    title_font = Font(name="Calibri", size=16, bold=True, color="1E293B")
    subtitle_font = Font(name="Calibri", size=11, italic=True, color="64748B")
    
    thin_border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )
    
    alert_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    alert_font = Font(name="Calibri", size=11, bold=True, color="991B1B")

    # =========================================================================
    # TAB 1: Executive_Dashboard
    # =========================================================================
    ws1 = wb.active
    ws1.title = "Executive_Dashboard"
    ws1.views.sheetView[0].showGridLines = True

    # Title Banner
    ws1.merge_cells("A1:G1")
    ws1["A1"] = "SUPPLY CHAIN & INVENTORY EXECUTIVE DASHBOARD"
    ws1["A1"].font = title_font

    ws1.merge_cells("A2:G2")
    ws1["A2"] = "Key Performance Indicators, Category Profitability & Regional Warehouse Performance"
    ws1["A2"].font = subtitle_font

    # KPI Cards Setup (Rows 4-5)
    kpis = [
        ("TOTAL REVENUE", f"₹{kpi_df['Total_Revenue'].iloc[0]:,.0f}", "B4", "B5"),
        ("TOTAL NET PROFIT", f"₹{kpi_df['Total_Profit'].iloc[0]:,.0f}", "C4", "C5"),
        ("PROFIT MARGIN %", f"{kpi_df['Margin_Pct'].iloc[0]:.2f}%", "D4", "D5"),
        ("HOLDING VALUE", f"₹{kpi_df['Total_Holding_Value'].iloc[0]:,.0f}", "E4", "E5"),
        ("REORDER NEEDED", f"{kpi_df['Reorder_Count'].iloc[0]:,} SKUs", "F4", "F5"),
        ("CRITICAL STOCKOUTS", f"{kpi_df['High_Risk_Count'].iloc[0]:,} SKUs", "G4", "G5"),
    ]

    for title, val, c_top, c_bot in kpis:
        ws1[c_top] = title
        ws1[c_top].font = kpi_title_font
        ws1[c_top].fill = kpi_fill
        ws1[c_top].alignment = Alignment(horizontal="center", vertical="center")
        ws1[c_top].border = thin_border
        
        ws1[c_bot] = val
        ws1[c_bot].font = kpi_val_font
        ws1[c_bot].fill = kpi_fill
        ws1[c_bot].alignment = Alignment(horizontal="center", vertical="center")
        ws1[c_bot].border = thin_border

    # Category Table (Row 7)
    ws1["A7"] = "Category Financial Performance"
    ws1["A7"].font = Font(name="Calibri", size=13, bold=True, color="1E293B")
    
    cat_headers = ["Category", "Units Sold", "Revenue (INR)", "Profit (INR)", "Margin %"]
    for col_num, h_text in enumerate(cat_headers, 1):
        cell = ws1.cell(row=8, column=col_num, value=h_text)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    for row_idx, row_data in cat_df.iterrows():
        ws1.append([
            row_data['Category'],
            row_data['Units_Sold'],
            row_data['Revenue_INR'],
            row_data['Profit_INR'],
            row_data['Margin_Pct']
        ])

    # Format Category Table Numbers
    for r in range(9, 9 + len(cat_df)):
        ws1[f"B{r}"].number_format = "#,##0"
        ws1[f"C{r}"].number_format = "₹#,##0"
        ws1[f"D{r}"].number_format = "₹#,##0"
        ws1[f"E{r}"].number_format = "0.00'%'"
        for c in range(1, 6):
            ws1.cell(row=r, column=c).border = thin_border

    # Category Chart
    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10
    chart1.title = "Revenue & Net Profit by Category (INR)"
    chart1.y_axis.title = "Amount in INR"
    chart1.x_axis.title = "Category"
    
    data1 = Reference(ws1, min_col=3, min_row=8, max_col=4, max_row=8 + len(cat_df))
    cats1 = Reference(ws1, min_col=1, min_row=9, max_row=8 + len(cat_df))
    chart1.add_data(data1, titles_from_data=True)
    chart1.set_categories(cats1)
    chart1.width = 16
    chart1.height = 9
    ws1.add_chart(chart1, "A15")

    # Warehouse Table (Row 7, Column G-K)
    ws1["G7"] = "Warehouse Hub Performance"
    ws1["G7"].font = Font(name="Calibri", size=13, bold=True, color="1E293B")
    
    wh_headers = ["Warehouse", "Units Sold", "Revenue (INR)", "Profit (INR)", "Avg Shipping Days"]
    for col_num, h_text in enumerate(wh_headers, 7):
        cell = ws1.cell(row=8, column=col_num, value=h_text)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    for row_idx, row_data in wh_df.iterrows():
        r = 9 + row_idx
        ws1.cell(row=r, column=7, value=row_data['Warehouse_Location'])
        ws1.cell(row=r, column=8, value=row_data['Units_Sold']).number_format = "#,##0"
        ws1.cell(row=r, column=9, value=row_data['Revenue_INR']).number_format = "₹#,##0"
        ws1.cell(row=r, column=10, value=row_data['Profit_INR']).number_format = "₹#,##0"
        ws1.cell(row=r, column=11, value=row_data['Avg_Shipping_Days']).number_format = "0.00"
        for c in range(7, 12):
            ws1.cell(row=r, column=c).border = thin_border

    # Warehouse Chart
    chart2 = BarChart()
    chart2.type = "col"
    chart2.style = 11
    chart2.title = "Revenue by Warehouse Location (INR)"
    data2 = Reference(ws1, min_col=9, min_row=8, max_col=9, max_row=8 + len(wh_df))
    cats2 = Reference(ws1, min_col=7, min_row=9, max_row=8 + len(wh_df))
    chart2.add_data(data2, titles_from_data=True)
    chart2.set_categories(cats2)
    chart2.width = 16
    chart2.height = 9
    ws1.add_chart(chart2, "G15")

    # =========================================================================
    # TAB 2: Inventory_Health
    # =========================================================================
    ws2 = wb.create_sheet(title="Inventory_Health")
    ws2.views.sheetView[0].showGridLines = True

    ws2["A1"] = "INVENTORY HEALTH & CRITICAL STOCKOUT MATRIX"
    ws2["A1"].font = title_font

    # Reorder Summary Table
    ws2["A3"] = "Reorder Status Summary"
    ws2["A3"].font = Font(name="Calibri", size=13, bold=True, color="1E293B")
    
    r_headers = ["Reorder Status", "Item Count", "Total Stock Units", "Holding Value (INR)"]
    for c_idx, h_text in enumerate(r_headers, 1):
        cell = ws2.cell(row=4, column=c_idx, value=h_text)
        cell.fill = header_fill
        cell.font = header_font

    for idx, row in reorder_df.iterrows():
        r = 5 + idx
        ws2.cell(row=r, column=1, value=row['Reorder_Status'])
        ws2.cell(row=r, column=2, value=row['Item_Count']).number_format = "#,##0"
        ws2.cell(row=r, column=3, value=row['Total_Stock_Units']).number_format = "#,##0"
        ws2.cell(row=r, column=4, value=row['Holding_Value_INR']).number_format = "₹#,##0"
        for c in range(1, 5):
            ws2.cell(row=r, column=c).border = thin_border

    # Top 15 Deficit Table
    ws2["A9"] = "Top 15 Products Needing Urgent Reorder (Critical Stock Deficit)"
    ws2["A9"].font = Font(name="Calibri", size=13, bold=True, color="1E293B")

    ls_headers = ["Product ID", "Product Name", "Category", "Warehouse", "Stock Quantity", "Reorder Level", "Deficit Units", "Stockout Risk"]
    for c_idx, h_text in enumerate(ls_headers, 1):
        cell = ws2.cell(row=10, column=c_idx, value=h_text)
        cell.fill = header_fill
        cell.font = header_font

    for idx, row in low_stock_df.iterrows():
        r = 11 + idx
        ws2.cell(row=r, column=1, value=row['Product_ID'])
        ws2.cell(row=r, column=2, value=row['Product_Name'])
        ws2.cell(row=r, column=3, value=row['Category'])
        ws2.cell(row=r, column=4, value=row['Warehouse_Location'])
        ws2.cell(row=r, column=5, value=row['Stock_Quantity']).number_format = "#,##0"
        ws2.cell(row=r, column=6, value=row['Reorder_Level']).number_format = "#,##0"
        ws2.cell(row=r, column=7, value=row['Deficit']).number_format = "#,##0"
        
        risk_cell = ws2.cell(row=r, column=8, value=row['Stockout_Risk'])
        if row['Stockout_Risk'] == 'High Risk':
            risk_cell.fill = alert_fill
            risk_cell.font = alert_font
            
        for c in range(1, 9):
            ws2.cell(row=r, column=c).border = thin_border

    # =========================================================================
    # TAB 3: Supplier_Scorecard
    # =========================================================================
    ws3 = wb.create_sheet(title="Supplier_Scorecard")
    ws3.views.sheetView[0].showGridLines = True

    ws3["A1"] = "SUPPLIER LEAD TIME & PERFORMANCE SCORECARD"
    ws3["A1"].font = title_font

    sup_headers = ["Supplier Name", "Total Orders", "Units Sold", "Avg Shipping Days", "Total Revenue (INR)", "Total Profit (INR)"]
    for c_idx, h_text in enumerate(sup_headers, 1):
        cell = ws3.cell(row=3, column=c_idx, value=h_text)
        cell.fill = header_fill
        cell.font = header_font

    for idx, row in sup_df.iterrows():
        r = 4 + idx
        ws3.cell(row=r, column=1, value=row['Supplier_Name'])
        ws3.cell(row=r, column=2, value=row['Total_Orders']).number_format = "#,##0"
        ws3.cell(row=r, column=3, value=row['Units_Sold']).number_format = "#,##0"
        ws3.cell(row=r, column=4, value=row['Avg_Shipping_Days']).number_format = "0.00"
        ws3.cell(row=r, column=5, value=row['Revenue_INR']).number_format = "₹#,##0"
        ws3.cell(row=r, column=6, value=row['Profit_INR']).number_format = "₹#,##0"
        for c in range(1, 7):
            ws3.cell(row=r, column=c).border = thin_border

    # Supplier Chart
    chart3 = BarChart()
    chart3.type = "bar"
    chart3.style = 13
    chart3.title = "Average Lead Time (Days) by Supplier"
    data3 = Reference(ws3, min_col=4, min_row=3, max_col=4, max_row=3 + len(sup_df))
    cats3 = Reference(ws3, min_col=1, min_row=4, max_row=3 + len(sup_df))
    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(cats3)
    chart3.width = 15
    chart3.height = 8
    ws3.add_chart(chart3, "A11")

    # =========================================================================
    # TAB 4: Cleaned_Data Sample
    # =========================================================================
    ws4 = wb.create_sheet(title="Cleaned_Data_Sample")
    ws4.views.sheetView[0].showGridLines = True

    ws4["A1"] = "CLEANED SUPPLY CHAIN DATASET (FIRST 1,000 RECORDS)"
    ws4["A1"].font = title_font

    for col_idx, col_name in enumerate(raw_df.columns, 1):
        cell = ws4.cell(row=3, column=col_idx, value=col_name)
        cell.fill = header_fill
        cell.font = header_font

    for r_idx, row_vals in raw_df.iterrows():
        r = 4 + r_idx
        for c_idx, val in enumerate(row_vals, 1):
            ws4.cell(row=r, column=c_idx, value=val)

    # Adjust Column Widths Across All Sheets
    for sheet in wb.worksheets:
        for col in sheet.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                if cell.value:
                    val_str = str(cell.value)
                    if len(val_str) > max_len:
                        max_len = len(val_str)
            sheet.column_dimensions[col_letter].width = max(max_len + 3, 12)

    # Save Excel Workbook
    wb.save(output_excel)
    print(f"\nExcel Dashboard successfully created at:\n{os.path.abspath(output_excel)}")
    print("=" * 80)

if __name__ == "__main__":
    create_excel_dashboard()
