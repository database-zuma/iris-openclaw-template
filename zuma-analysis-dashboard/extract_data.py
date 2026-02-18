#!/usr/bin/env python3
"""
Zuma Analysis Dashboard — Data Extractor v2
FULL REBUILD: uses mart.sku_portfolio (primary) + core tables for area/store breakdown
Output: data.json with monthly sales breakdown for 12-month date filtering
"""
import psycopg2
import json
import sys
from collections import defaultdict
from datetime import datetime

DB = "host=76.13.194.120 dbname=openclaw_ops user=openclaw_app password=Zuma-0psCl4w-2026!"

# ── Area → Warehouse mapping ───────────────────────────────────────────────────
AREA_WH_MAP = {
    'Bali 1':    'Warehouse Bali',
    'Bali 2':    'Warehouse Bali',
    'Bali 3':    'Warehouse Bali',
    'Jakarta':   'Warehouse Jakarta',
    'Jatim':     'Jatim',
}
# Retail areas to display (from ff_fa_fs_daily branches)
RETAIL_AREAS = ['Bali 1','Bali 2','Bali 3','Jakarta','Jatim','Lombok','Sulawesi','Sumatra']

# Canonical store name aliases — maps alternate spellings to the stock-canonical name
# Used to merge sales data (lowercase/short) with stock data (proper names)
STORE_CANONICAL = {
    # Jakarta: sales uses "exchange", stock uses "xchange"
    'ZUMA BINTARO EXCHANGE':         'ZUMA BINTARO XCHANGE',
    # Jakarta: sales uses "pluit village", stock uses "pluit village mall"
    'ZUMA PLUIT VILLAGE':            'ZUMA PLUIT VILLAGE MALL',
    # Jakarta: sales uses "moi", stock uses full name
    'ZUMA MOI':                      'ZUMA MALL OF INDONESIA (MOI)',
    # Jatim: sales uses "icon gresik", stock uses "icon mall gresik"
    'ZUMA ICON GRESIK':              'ZUMA ICON MALL GRESIK',
    # Jatim: sales uses "sunrise mall", stock uses "sunrise mall mojokerto"
    'ZUMA SUNRISE MALL':             'ZUMA SUNRISE MALL MOJOKERTO',
    # Jatim: sales uses "tunjungan plaza", stock uses "tunjungan plaza 3"
    'ZUMA TUNJUNGAN PLAZA':          'ZUMA TUNJUNGAN PLAZA 3',
    # Lombok: sales uses "mataram", stock uses "mataram lombok"
    'ZUMA MATARAM':                  'ZUMA MATARAM LOMBOK',
    # Sulawesi: sales uses "mega mall", stock uses "mega mall manado"
    'ZUMA MEGA MALL':                'ZUMA MEGA MALL MANADO',
    # Bali 2: ff has "icon bali", stock has "mall bali icon"
    'ZUMA ICON BALI':                'ZUMA MALL BALI ICON',
    # Sumatra: ff has "nagoya hills" (no s in db), stock has "nagoya hill batam"
    'ZUMA NAGOYA HILLS':             'ZUMA NAGOYA HILL BATAM',
}

def norm(name):
    if not name:
        return None
    ns = name.strip().upper()
    return STORE_CANONICAL.get(ns, ns)

print("Connecting to DB...")
conn = psycopg2.connect(DB)
cur = conn.cursor()

# ─── 1. PRODUCT LIST from mart.sku_portfolio ──────────────────────────────────
print("1/12 Fetching product list from mart.sku_portfolio...")
cur.execute("""
    SELECT kodemix, gender, series, color, tipe, tier,
           wh_pusat, wh_bali, wh_jkt, wh_total, stok_toko,
           avg_last_3_months
    FROM mart.sku_portfolio
    WHERE kodemix IS NOT NULL AND kodemix != ''
    ORDER BY gender, series, color
""")
products = {}
for row in cur.fetchall():
    km, g, s, c, tipe, tier, wh_p, wh_b, wh_j, wh_t, st, avg3m = row
    products[km] = {
        'km':    km,
        'g':     g or '',
        's':     s or '',
        'c':     c or '',
        'tipe':  tipe or '',
        't':     str(tier) if tier else '',
        'swh':   int(wh_t or 0),
        'sst':   int(st or 0),
        'swh_w': {  # WH stock by warehouse area
            'Jatim':             int(wh_p or 0),
            'Warehouse Bali':    int(wh_b or 0),
            'Warehouse Jakarta': int(wh_j or 0),
        },
        'avg3m': float(avg3m or 0),
    }
print(f"   {len(products)} products found")

# ─── 2. SIZE PRODUCTS from mart.sku_portfolio_size ────────────────────────────
print("2/12 Fetching size data from mart.sku_portfolio_size...")
cur.execute("""
    SELECT kode_besar, kode_kecil, kodemix, gender, series, color, tier, size,
           wh_total, stok_toko, avg_last_3_months
    FROM mart.sku_portfolio_size
    WHERE kodemix IS NOT NULL AND kode_besar IS NOT NULL
    ORDER BY kodemix, size
""")
size_products = {}  # kode_besar → info
km_to_sizes   = defaultdict(list)  # kodemix → list of kode_besar
for row in cur.fetchall():
    kb, kk, km, g, s, c, tier, sz, wh_t, st, avg3m = row
    size_products[kb] = {
        'kb': kb,
        'kk': kk or km,
        'km': km,
        'g':  g or '',
        's':  s or '',
        'c':  c or '',
        't':  str(tier) if tier else '',
        'sz': sz or '',
        'swh': int(wh_t or 0),
        'sst': int(st or 0),
        'avg3m': float(avg3m or 0),
    }
    km_to_sizes[km].append(kb)
print(f"   {len(size_products)} size rows, {len(km_to_sizes)} kodemix groups")

# ─── 3. RETAIL STOCK by area ──────────────────────────────────────────────────
print("3/12 Fetching retail stock by area...")
cur.execute("""
    SELECT kode_mix, gudang_area, SUM(quantity)
    FROM core.stock_with_product
    WHERE gudang_category='RETAIL'
      AND kode_mix IS NOT NULL AND kode_mix != ''
      AND gudang_area IS NOT NULL AND gudang_area != ''
    GROUP BY kode_mix, gudang_area
""")
stock_by_area = defaultdict(dict)
for km, area, qty in cur.fetchall():
    if area in RETAIL_AREAS:
        stock_by_area[km][area] = int(qty or 0)

# ─── 4. RETAIL STOCK by store ─────────────────────────────────────────────────
print("4/12 Fetching retail stock by store...")
cur.execute("""
    SELECT kode_mix, nama_gudang, gudang_area, SUM(quantity)
    FROM core.stock_with_product
    WHERE gudang_category='RETAIL'
      AND kode_mix IS NOT NULL AND kode_mix != ''
      AND nama_gudang IS NOT NULL AND nama_gudang != ''
    GROUP BY kode_mix, nama_gudang, gudang_area
""")
stock_by_store  = defaultdict(dict)
store_area_raw  = {}  # store_norm → area
for km, store, area, qty in cur.fetchall():
    ns = norm(store)
    if ns:
        stock_by_store[km][ns] = int(qty or 0)
        if area in RETAIL_AREAS:
            store_area_raw[ns] = area

# ─── 5. SIZE RETAIL STOCK by area ─────────────────────────────────────────────
print("5/12 Fetching size retail stock by area...")
cur.execute("""
    SELECT kode_mix_size, gudang_area, SUM(quantity)
    FROM core.stock_with_product
    WHERE gudang_category='RETAIL'
      AND kode_mix_size IS NOT NULL AND kode_mix_size != ''
      AND gudang_area IS NOT NULL AND gudang_area != ''
    GROUP BY kode_mix_size, gudang_area
""")
sz_stock_by_area = defaultdict(dict)  # kode_mix_size (≈ kode_besar) → area → qty
for kb, area, qty in cur.fetchall():
    if area in RETAIL_AREAS:
        sz_stock_by_area[kb][area] = int(qty or 0)

# ─── 6. SIZE RETAIL STOCK by store ────────────────────────────────────────────
print("6/12 Fetching size retail stock by store...")
cur.execute("""
    SELECT kode_mix_size, nama_gudang, SUM(quantity)
    FROM core.stock_with_product
    WHERE gudang_category='RETAIL'
      AND kode_mix_size IS NOT NULL AND kode_mix_size != ''
      AND nama_gudang IS NOT NULL AND nama_gudang != ''
    GROUP BY kode_mix_size, nama_gudang
""")
sz_stock_by_store = defaultdict(dict)
for kb, store, qty in cur.fetchall():
    ns = norm(store)
    if ns:
        sz_stock_by_store[kb][ns] = int(qty or 0)

# ─── 7. MONTHLY RETAIL SALES total + by area + by store ───────────────────────
print("7/12 Fetching monthly retail sales by area...")
cur.execute("""
    SELECT kode_mix,
           to_char(date_trunc('month', transaction_date), 'YYYY-MM') AS month,
           area,
           SUM(quantity)
    FROM core.sales_with_product
    WHERE store_category = 'RETAIL'
      AND area IS NOT NULL AND area != ''
      AND transaction_date >= date_trunc('month', NOW()) - INTERVAL '12 months'
      AND kode_mix IS NOT NULL AND kode_mix != ''
    GROUP BY kode_mix, month, area
""")
smr_area = defaultdict(lambda: defaultdict(dict))  # [km][month][area] = qty
for km, month, area, qty in cur.fetchall():
    if area in RETAIL_AREAS:
        smr_area[km][month][area] = int(qty or 0)

print("8/12 Fetching monthly retail sales by store...")
cur.execute("""
    SELECT kode_mix,
           to_char(date_trunc('month', transaction_date), 'YYYY-MM') AS month,
           matched_store_name,
           SUM(quantity)
    FROM core.sales_with_product
    WHERE store_category = 'RETAIL'
      AND matched_store_name IS NOT NULL AND matched_store_name != ''
      AND transaction_date >= date_trunc('month', NOW()) - INTERVAL '12 months'
      AND kode_mix IS NOT NULL AND kode_mix != ''
    GROUP BY kode_mix, month, matched_store_name
""")
smr_store = defaultdict(lambda: defaultdict(dict))  # [km][month][store] = qty
for km, month, store, qty in cur.fetchall():
    ns = norm(store)
    if ns:
        smr_store[km][month][ns] = int(qty or 0)

# ─── 9. MONTHLY ONLINE SALES ──────────────────────────────────────────────────
print("9/12 Fetching monthly online sales...")
cur.execute("""
    SELECT kode_mix,
           to_char(date_trunc('month', transaction_date), 'YYYY-MM') AS month,
           SUM(quantity)
    FROM core.sales_with_product
    WHERE (store_name_raw = 'online'
           OR (area = 'Online' AND store_category = 'RETAIL'))
      AND transaction_date >= date_trunc('month', NOW()) - INTERVAL '12 months'
      AND kode_mix IS NOT NULL AND kode_mix != ''
    GROUP BY kode_mix, month
""")
smo = defaultdict(dict)  # [km][month] = qty
for km, month, qty in cur.fetchall():
    smo[km][month] = smo[km].get(month, 0) + int(qty or 0)

# ─── 10. MONTHLY NON-RETAIL SALES ─────────────────────────────────────────────
print("10/12 Fetching monthly non-retail sales...")
cur.execute("""
    SELECT kode_mix,
           to_char(date_trunc('month', transaction_date), 'YYYY-MM') AS month,
           SUM(quantity)
    FROM core.sales_with_product
    WHERE store_category IN ('NON-RETAIL', 'EVENT')
      AND store_name_raw != 'online'
      AND transaction_date >= date_trunc('month', NOW()) - INTERVAL '12 months'
      AND kode_mix IS NOT NULL AND kode_mix != ''
    GROUP BY kode_mix, month
""")
smn = defaultdict(dict)  # [km][month] = qty
for km, month, qty in cur.fetchall():
    smn[km][month] = int(qty or 0)

# ─── 11. SIZE MONTHLY RETAIL SALES ────────────────────────────────────────────
print("11/12 Fetching size-level monthly retail sales...")
cur.execute("""
    SELECT kode_mix_size,
           to_char(date_trunc('month', transaction_date), 'YYYY-MM') AS month,
           SUM(quantity)
    FROM core.sales_with_product
    WHERE store_category = 'RETAIL'
      AND kode_mix_size IS NOT NULL AND kode_mix_size != ''
      AND transaction_date >= date_trunc('month', NOW()) - INTERVAL '12 months'
    GROUP BY kode_mix_size, month
""")
sz_smr = defaultdict(dict)  # [kode_mix_size][month] = qty
for kb, month, qty in cur.fetchall():
    sz_smr[kb][month] = int(qty or 0)

# ─── 12. STORE → AREA mapping from ff_fa_fs_daily ────────────────────────────
print("12/12 Building store→area map from ff_fa_fs_daily...")
# Normalize area names (ff_fa_fs_daily uses 'Sumatera', stock/sales use 'Sumatra')
AREA_NORM = {'Sumatera': 'Sumatra'}
cur.execute("""
    SELECT DISTINCT branch, store_label, store_db_name
    FROM mart.ff_fa_fs_daily
    ORDER BY branch, store_label
""")
stores_by_area  = defaultdict(list)   # area → [store labels]
ff_store_map    = {}                   # store_db_name_norm → area
for branch, label, db_name in cur.fetchall():
    # Normalize branch name (Sumatera → Sumatra)
    area = AREA_NORM.get(branch, branch)
    # Use store_db_name (canonical) as key, not store_label
    ns = norm(db_name)
    if ns and area in RETAIL_AREAS:
        if ns not in ff_store_map:  # first occurrence wins
            ff_store_map[ns] = area

# Merge: store_area_raw (from stock) takes priority over ff_store_map (from ff_fa_fs_daily)
# store_area_raw is the ground truth since it comes from actual stock data
final_store_area = {**ff_store_map, **store_area_raw}  # store_area_raw wins on conflict

# All retail stores: must have actual stock OR sales data, AND have known area
stores_with_data = set(
    list(s for km_d in stock_by_store.values() for s in km_d) +
    list(s for km_d in smr_store.values() for m_d in km_d.values() for s in m_d)
)
all_stores = sorted(
    stores_with_data & set(final_store_area.keys())
)

# Build stores_by_area ONLY from stores with actual data (eliminates phantom/duplicate names)
stores_by_area_final = defaultdict(list)
for st in all_stores:
    ar = final_store_area[st]
    if st not in stores_by_area_final[ar]:
        stores_by_area_final[ar].append(st)
for ar in stores_by_area_final:
    stores_by_area_final[ar].sort()

# ─── COMPUTE ALL MONTHS ────────────────────────────────────────────────────────
all_months_set = set()
for km in products:
    all_months_set.update(smr_area.get(km, {}).keys())
    all_months_set.update(smo.get(km, {}).keys())
    all_months_set.update(smn.get(km, {}).keys())
all_months = sorted(all_months_set)
if not all_months:
    # Fallback: last 12 months
    from datetime import date, timedelta
    d = date.today().replace(day=1)
    all_months = []
    for i in range(12):
        all_months.insert(0, d.strftime('%Y-%m'))
        d = (d - timedelta(days=1)).replace(day=1)

# ─── BUILD ARTICLES ARRAY ─────────────────────────────────────────────────────
print("\nBuilding articles array...")
articles = []
for km, prod in products.items():
    # Retail stock by area (from core, overrides simple stok_toko)
    sba_data = dict(stock_by_area.get(km, {}))
    sbs_data = dict(stock_by_store.get(km, {}))
    sst_computed = sum(sba_data.values()) if sba_data else prod['sst']

    # Monthly retail sales: merged structure
    smr_months = set(smr_area.get(km, {}).keys()) | set(smr_store.get(km, {}).keys())
    smr_data = {}
    for month in smr_months:
        ad = smr_area[km].get(month, {})
        sd = smr_store[km].get(month, {})
        t  = sum(ad.values()) if ad else sum(sd.values())
        entry = {'t': t}
        if ad: entry['a'] = ad
        if sd: entry['s'] = sd
        smr_data[month] = entry

    smo_data = dict(smo.get(km, {}))
    smn_data = dict(smn.get(km, {}))

    # Size breakdown from sku_portfolio_size
    sz_arr = []
    for kb in sorted(km_to_sizes.get(km, []), key=lambda x: (len(x), x)):
        sp = size_products.get(kb)
        if not sp:
            continue
        sz_sba = dict(sz_stock_by_area.get(kb, {}))
        sz_sbs = dict(sz_stock_by_store.get(kb, {}))
        sz_sst = sum(sz_sba.values()) if sz_sba else sp['sst']
        sz_arr.append({
            'kb':  kb,
            'sz':  sp['sz'],
            'swh': sp['swh'],
            'sst': sz_sst,
            'sba': sz_sba,
            'sbs': sz_sbs,
            'smr': dict(sz_smr.get(kb, {})),
        })

    articles.append({
        'km':   km,
        'g':    prod['g'],
        's':    prod['s'],
        'c':    prod['c'],
        't':    prod['t'],
        'tipe': prod['tipe'],
        'swh':  prod['swh'],
        'swh_w': prod['swh_w'],
        'sst':  sst_computed,
        'sba':  sba_data,
        'sbs':  sbs_data,
        'smr':  smr_data,
        'smo':  smo_data,
        'smn':  smn_data,
        'avg3m': prod['avg3m'],
        'sz':   sz_arr,
    })

# ─── VALIDATION SUMMARY ────────────────────────────────────────────────────────
total_swh   = sum(a['swh'] for a in articles)
total_sst   = sum(a['sst'] for a in articles)
total_smr   = sum(sum(m['t'] for m in a['smr'].values()) for a in articles)
total_smo   = sum(sum(a['smo'].values()) for a in articles)
total_smn   = sum(sum(a['smn'].values()) for a in articles)
total_sizes = sum(len(a['sz']) for a in articles)

print(f"\n=== DATA SUMMARY ===")
print(f"Articles    : {len(articles)}")
print(f"Size rows   : {total_sizes}")
print(f"Months      : {len(all_months)} ({all_months[0] if all_months else '-'} → {all_months[-1] if all_months else '-'})")
print(f"Areas       : {RETAIL_AREAS}")
print(f"Stores      : {len(all_stores)}")
print(f"Stock WH    : {total_swh:,}")
print(f"Stock Store : {total_sst:,}")
print(f"Sales Retail: {total_smr:,} (12-month)")
print(f"Sales Online: {total_smo:,}")
print(f"Sales NonRet: {total_smn:,}")

# ─── WRITE JSON ───────────────────────────────────────────────────────────────
data = {
    'generated_at':    datetime.now().isoformat(),
    'months':          all_months,
    'areas':           RETAIL_AREAS,
    'area_wh_map':     AREA_WH_MAP,
    'stores':          all_stores,
    'stores_by_area':  dict(stores_by_area_final),
    'store_area_map':  final_store_area,
    'articles':        articles,
}

print("\nWriting data.json...")
with open('data.json', 'w') as f:
    json.dump(data, f, separators=(',', ':'))

import os
size_mb = os.path.getsize('data.json') / 1024 / 1024
print(f"Done! data.json = {size_mb:.2f} MB")

cur.close()
conn.close()
