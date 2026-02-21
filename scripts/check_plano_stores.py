#!/usr/bin/env python3
import psycopg2

conn = psycopg2.connect(
    host='76.13.194.120',
    database='openclaw_ops',
    user='openclaw_app',
    password='Zuma-0psCl4w-2026!'
)

cur = conn.cursor()

# Check all store names containing "batam" or "sumatra" or anything related
cur.execute("""
SELECT DISTINCT store_name_raw, area
FROM public.sales_summary_plano
WHERE store_name_raw LIKE '%atam%' 
   OR store_name_raw LIKE '%SKA%'
   OR store_name_raw LIKE '%Sumatra%'
   OR area = 'Batam'
   OR area = 'Sumatra'
ORDER BY store_name_raw;
""")

stores = cur.fetchall()

print("📊 Batam/Sumatra Stores in sales_summary_plano:\n")
for store in stores:
    print(f"  • {store[0]} (Area: {store[1]})")

# Also check date range
cur.execute("""
SELECT 
  MIN(transaction_month) as earliest,
  MAX(transaction_month) as latest
FROM public.sales_summary_plano;
""")

dates = cur.fetchone()
print(f"\n📅 Date Range: {dates[0]} to {dates[1]}")

cur.close()
conn.close()
