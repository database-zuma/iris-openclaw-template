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

# Query with article detail breakdown
query = """
SELECT 
  TO_CHAR(s.tanggal, 'Mon YYYY') AS month,
  k.kode_mix AS article_mix,
  k.tipe AS type,
  k.gender,
  k.series,
  k.article,
  k.tier_baru AS tier,
  s.nama_gudang AS store,
  SUM(s.kuantitas) AS sales_qty
FROM raw.accurate_sales_ddd s
LEFT JOIN portal.kodemix k ON s.kode_produk = k.kode_mix_size
WHERE s.nama_gudang IN ('Zuma Nagoya Hill Batam', 'Zuma SKA MALL')
  AND s.tanggal >= '2025-02-01'
  AND s.tanggal < '2026-02-01'
GROUP BY TO_CHAR(s.tanggal, 'Mon YYYY'), k.kode_mix, k.tipe, k.gender, k.series, k.article, k.tier_baru, s.nama_gudang
ORDER BY s.nama_gudang, TO_CHAR(s.tanggal, 'Mon YYYY'), k.kode_mix;
"""

cur.execute(query)
rows = cur.fetchall()

# Separate by store
nagoya_rows = [r for r in rows if 'Nagoya' in r[7]]
ska_rows = [r for r in rows if 'SKA' in r[7]]

# Write Nagoya Hills
nagoya_file = '/Users/database-zuma/.openclaw/workspace/sales_nagoya_hills_detail.csv'
with open(nagoya_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Month', 'Article Mix', 'Type', 'Gender', 'Series', 'Article', 'Tier', 'Sales Qty'])
    for row in nagoya_rows:
        writer.writerow(row[:7] + (row[8],))  # Exclude store column in output

# Write SKA Mall
ska_file = '/Users/database-zuma/.openclaw/workspace/sales_ska_mall_detail.csv'
with open(ska_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Month', 'Article Mix', 'Type', 'Gender', 'Series', 'Article', 'Tier', 'Sales Qty'])
    for row in ska_rows:
        writer.writerow(row[:7] + (row[8],))

cur.close()
conn.close()

print(f"✅ Nagoya Hills: {nagoya_file} ({len(nagoya_rows)} records)")
print(f"✅ SKA Mall: {ska_file} ({len(ska_rows)} records)")
print(f"Total: {len(rows)} article-month combinations")
