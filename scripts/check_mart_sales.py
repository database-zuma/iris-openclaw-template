#!/usr/bin/env python3
import psycopg2

conn = psycopg2.connect(
    host='76.13.194.120',
    database='openclaw_ops',
    user='openclaw_app',
    password='Zuma-0psCl4w-2026!'
)

cur = conn.cursor()

# Check mart.sales_by_store for these stores
query = """
SELECT 
  matched_store_name,
  period_start,
  period_type,
  pairs,
  revenue
FROM mart.sales_by_store
WHERE matched_store_name IN ('zuma nagoya hills', 'zuma ska mall')
  AND period_type = 'monthly'
  AND period_start >= '2025-02-01'
  AND period_start < '2026-02-01'
ORDER BY matched_store_name, period_start;
"""

cur.execute(query)
rows = cur.fetchall()

print("📊 Mart Table Data:\n")
for row in rows:
    store, period, ptype, pairs, revenue = row
    print(f"{store} | {period} | {pairs:,} pairs | Rp {revenue:,.0f}")

print(f"\nTotal records: {len(rows)}")

cur.close()
conn.close()
