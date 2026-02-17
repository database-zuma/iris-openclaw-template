#!/usr/bin/env python3
import psycopg2
import csv
from collections import defaultdict

# Database connection
conn = psycopg2.connect(
    host='76.13.194.120',
    database='openclaw_ops',
    user='openclaw_app',
    password='Zuma-0psCl4w-2026!'
)

cur = conn.cursor()

# Query sales data with product details
query = """
SELECT 
  s.nama_gudang,
  TO_CHAR(s.tanggal, 'YYYY-MM') AS month,
  k.kode_mix AS article_mix,
  k.tipe AS type,
  k.gender,
  k.series,
  k.article,
  k.tier_baru AS tier,
  SUM(s.kuantitas) AS sales_qty
FROM raw.accurate_sales_ddd s
LEFT JOIN portal.kodemix k ON s.kode_produk = k.kode_mix_size
WHERE s.nama_gudang IN ('Zuma Nagoya Hill Batam', 'Zuma SKA MALL')
  AND s.tanggal >= '2025-02-01'
  AND s.tanggal < '2026-02-01'
GROUP BY s.nama_gudang, TO_CHAR(s.tanggal, 'YYYY-MM'), k.kode_mix, k.tipe, k.gender, k.series, k.article, k.tier_baru
ORDER BY s.nama_gudang, month, k.kode_mix;
"""

cur.execute(query)
rows = cur.fetchall()

# Write to CSV
output_file = '/Users/database-zuma/.openclaw/workspace/sales_nagoya_ska_1year.csv'

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    # Header
    writer.writerow(['Store', 'Month', 'Article Mix', 'Type', 'Gender', 'Series', 'Article', 'Tier', 'Sales Qty'])
    
    # Data rows
    for row in rows:
        writer.writerow(row)

cur.close()
conn.close()

print(f"✅ Generated: {output_file}")
print(f"Total records: {len(rows)}")
