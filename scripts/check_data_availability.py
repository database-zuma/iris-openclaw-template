#!/usr/bin/env python3
import psycopg2

conn = psycopg2.connect(
    host='76.13.194.120',
    database='openclaw_ops',
    user='openclaw_app',
    password='Zuma-0psCl4w-2026!'
)

cur = conn.cursor()

# Check available date ranges for both stores
query = """
SELECT 
  nama_gudang,
  MIN(tanggal) as earliest,
  MAX(tanggal) as latest,
  COUNT(*) as total_records,
  SUM(kuantitas) as total_qty
FROM raw.accurate_sales_ddd
WHERE nama_gudang IN ('Zuma Nagoya Hill Batam', 'Zuma SKA MALL')
GROUP BY nama_gudang;
"""

cur.execute(query)
rows = cur.fetchall()

print("📊 Data Availability Check:\n")
for row in rows:
    store, earliest, latest, records, qty = row
    print(f"Store: {store}")
    print(f"  • Earliest: {earliest}")
    print(f"  • Latest: {latest}")
    print(f"  • Records: {records:,}")
    print(f"  • Total pairs: {qty:,.0f}")
    print()

cur.close()
conn.close()
