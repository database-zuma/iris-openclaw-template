#!/usr/bin/env python3
import psycopg2
import csv

conn = psycopg2.connect(
    host='76.13.194.120',
    database='openclaw_ops',
    user='openclaw_app',
    password='Zuma-0psCl4w-2026!'
)

cur = conn.cursor()

# Query with exact lowercase store names
query = """
SELECT 
  TO_CHAR(transaction_month, 'Mon YYYY') AS month,
  kode_mix AS article_mix,
  tipe AS type,
  gender,
  series,
  product_name AS article,
  tier,
  store_name_raw AS store,
  total_quantity AS sales_qty
FROM public.sales_summary_plano
WHERE store_name_raw IN ('zuma nagoya hills', 'zuma ska mall')
  AND transaction_month >= '2025-02-01'
  AND transaction_month < '2026-02-01'
ORDER BY store_name_raw, transaction_month, kode_mix;
"""

cur.execute(query)
rows = cur.fetchall()

# Separate by store
nagoya_rows = [r for r in rows if 'nagoya' in r[7]]
ska_rows = [r for r in rows if 'ska' in r[7]]

# Write Nagoya Hills
nagoya_file = '/Users/database-zuma/.openclaw/workspace/sales_nagoya_hills_detail.csv'
with open(nagoya_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Month', 'Article Mix', 'Type', 'Gender', 'Series', 'Article', 'Tier', 'Sales Qty'])
    for row in nagoya_rows:
        writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[8]])

# Write SKA Mall  
ska_file = '/Users/database-zuma/.openclaw/workspace/sales_ska_mall_detail.csv'
with open(ska_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Month', 'Article Mix', 'Type', 'Gender', 'Series', 'Article', 'Tier', 'Sales Qty'])
    for row in ska_rows:
        writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[8]])

cur.close()
conn.close()

print(f"✅ Nagoya Hills: {nagoya_file} ({len(nagoya_rows)} records)")
print(f"✅ SKA Mall: {ska_file} ({len(ska_rows)} records)")
print(f"Total: {len(rows)} article-month combinations")

# Show sample
if len(nagoya_rows) > 0:
    print(f"\n📋 Sample Nagoya (first 5 rows):")
    for i, row in enumerate(nagoya_rows[:5]):
        print(f"  {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[6]} | {row[8]} pairs")
