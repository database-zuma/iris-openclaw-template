#!/usr/bin/env python3
import psycopg2

conn = psycopg2.connect(
    host='76.13.194.120',
    database='openclaw_ops',
    user='openclaw_app',
    password='Zuma-0psCl4w-2026!'
)

cur = conn.cursor()

# Check raw table WITHOUT snapshot_date filter
query = """
SELECT 
  nama_gudang,
  MIN(tanggal) as earliest,
  MAX(tanggal) as latest,
  COUNT(DISTINCT tanggal) as unique_dates,
  COUNT(*) as records,
  SUM(kuantitas) as total_qty
FROM raw.accurate_sales_ddd
WHERE nama_gudang IN ('Zuma Nagoya Hill Batam', 'Zuma SKA MALL')
GROUP BY nama_gudang;
"""

cur.execute(query)
rows = cur.fetchall()

print("📊 Raw Table Full Check (no date filter):\n")
for row in rows:
    print(f"Store: {row[0]}")
    print(f"  Earliest: {row[1]}")
    print(f"  Latest: {row[2]}")
    print(f"  Unique dates: {row[3]}")
    print(f"  Records: {row[4]:,}")
    print(f"  Total qty: {row[5]:,.0f}\n")

# Now check specific period with different filter
query2 = """
SELECT COUNT(*), SUM(kuantitas)
FROM raw.accurate_sales_ddd
WHERE nama_gudang IN ('Zuma Nagoya Hill Batam', 'Zuma SKA MALL')
  AND tanggal BETWEEN '2025-02-01' AND '2026-01-31';
"""

cur.execute(query2)
row = cur.fetchone()
print(f"Period Feb 2025 - Jan 2026: {row[0]} records, {row[1] if row[1] else 0} pairs")

cur.close()
conn.close()
