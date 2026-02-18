#!/usr/bin/env python3
"""
Sync portal.store_name_map with all planogram stores.
Maps display_options store names to sales/stock store names.
"""
import psycopg2

DB = dict(
    host="76.13.194.120", port=5432, dbname="openclaw_ops",
    user="openclaw_app", password="Zuma-0psCl4w-2026!"
)

# Manual mappings where names don't match exactly
# Format: (planogram_name, sales_name, branch)
MANUAL_MAPPINGS = [
    # Jatim - existing mappings are correct, just need to add missing ones
    ("CITO", "Zuma City Of Tomorrow Mall", "Jatim"),
    ("GM", "Zuma Galaxy Mall", "Jatim"),
    ("ICON MALL GRESIK", "Zuma Icon Gresik", "Jatim"),
    ("LIPPO BATU", "Zuma Lippo Batu", "Jatim"),
    ("LIPPO SIDOARJO", "Zuma Lippo Sidoarjo", "Jatim"),
    ("MATOS", "Zuma Matos", "Jatim"),
    ("MOG", "Zuma Mall Olympic Garden", "Jatim"),
    ("ROYAL", "Zuma Royal Plaza", "Jatim"),
    ("SUNRISE", "Zuma Sunrise Mall Mojokerto", "Jatim"),
    ("TP", "Zuma Tunjungan Plaza 3", "Jatim"),
    
    # Bali 1
    ("ZUMA BAJRA", "Zuma Bajra", "Bali 1"),
    ("ZUMA BATUBULAN", "Zuma Batubulan", "Bali 1"),
    ("ZUMA JEMBRANA", "Zuma Jembrana", "Bali 1"),
    ("ZUMA KAPAL", "Zuma Kapal", "Bali 1"),
    ("ZUMA LEVEL 21", "Zuma Level 21", "Bali 1"),
    ("ZUMA LIPPO BALI", "Zuma Lippo Bali", "Bali 1"),
    ("ZUMA MF UBUD", "Zuma Monkey Forest Ubud", "Bali 1"),
    ("ZUMA TABANAN", "Zuma Tabanan", "Bali 1"),
    
    # Bali 2
    ("BANGLI", "Zuma Bangli", "Bali 2"),
    ("DALUNG", "Zuma Dalung", "Bali 2"),
    ("GIANYAR", "Zuma Gianyar", "Bali 2"),
    ("ICON", "Zuma Icon Bali", "Bali 2"),
    ("KARANG ASEM", "Zuma Karangasem", "Bali 2"),
    ("KLUNGKUNG", "Zuma Klungkung", "Bali 2"),
    ("LEBAH", "Zuma Lebah Peliatan", "Bali 2"),
    ("LIVING", "Zuma Living World", "Bali 2"),
    ("MM", "Zuma Monang Maning", "Bali 2"),
    ("PEMOGAN", "Zuma Pemogan", "Bali 2"),
    # ZUMA MF UBUD moved to Bali 1 in sales, but Bali 2 has: zuma lippo bali, zuma monang maning, zuma peguyangan
    ("PEGUYANGAN", "Zuma Peguyangan", "Bali 2"),
    
    # Bali 3
    ("ZUMA KEDONGANAN", "Zuma Kedonganan", "Bali 3"),
    ("ZUMA KESIMAN", "Zuma Kesiman", "Bali 3"),
    ("ZUMA MBG", "Zuma Mall Bali Galeria", "Bali 3"),
    ("ZUMA PANJER", "Zuma Panjer", "Bali 3"),
    ("ZUMA PELIATAN", "Zuma Peliatan", "Bali 3"),
    ("ZUMA PENATIH", "Zuma Penatih", "Bali 3"),
    ("ZUMA SERIRIT", "Zuma Seririt", "Bali 3"),
    ("ZUMA SINGARAJA", "Zuma Singaraja", "Bali 3"),
    ("ZUMA ULUWATU", "Zuma Uluwatu", "Bali 3"),
    
    # Jakarta
    ("ZUMA BINTARO XCHANGE", "Zuma Bintaro Exchange", "Jakarta"),
    ("ZUMA LMP", "Zuma Lippo Mall Puri", "Jakarta"),
    ("ZUMA MOI", "Zuma MOI", "Jakarta"),
    ("ZUMA PLUIT VILLAGE", "Zuma Pluit Village", "Jakarta"),
    
    # Lombok
    ("ZUMA EPICENTRUM", "Zuma Epicentrum", "Lombok"),
    ("ZUMA MATARAM LOMBOK", "Zuma Mataram", "Lombok"),
    
    # Sulawesi
    ("ZUMA MEGA MALL MANADO", "Zuma Mega Mall", "Sulawesi"),
    
    # Sumatera (Batam area in sales)
    ("ZUMA NAGOYA HILL", "Zuma Nagoya Hills", "Sumatera"),
    ("ZUMA SKA MALL", "Zuma SKA Mall", "Sumatera"),
]

conn = psycopg2.connect(**DB)
cur = conn.cursor()

print("Inserting store name mappings...")
inserted = 0
for plano_name, stock_name, branch in MANUAL_MAPPINGS:
    cur.execute("""
        INSERT INTO portal.store_name_map (planogram_name, stock_nama_gudang, branch, match_method, updated_at)
        VALUES (%s, %s, %s, 'manual_sync', NOW())
        ON CONFLICT (planogram_name) DO UPDATE SET
            stock_nama_gudang = EXCLUDED.stock_nama_gudang,
            branch = EXCLUDED.branch,
            match_method = 'manual_sync_update',
            updated_at = NOW()
    """, (plano_name, stock_name, branch))
    if cur.rowcount > 0:
        inserted += 1
        print(f"  {plano_name} -> {stock_name}")

conn.commit()
cur.close()
conn.close()

print(f"\nTotal mappings inserted/updated: {inserted}")
