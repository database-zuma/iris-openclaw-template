#!/usr/bin/env python3
"""
Generate Pre-Planogram for ALL Zuma Branches
=============================================
Pipeline:
1. Load stores from portal.store_display_options
2. Load sales (12mo) per AREA (indexed/fast), match to stores in Python
3. Load assortment from portal.kodemix
4. Calculate tier-adjusted averages + sales mix per store
5. Distribute by size ratios
6. Insert into portal.planogram

Usage:
    python3 generate_planogram.py [--dry-run] [--area AREA] [--no-reset]

Areas processed: Bali 1, Bali 2, Bali 3, Jakarta, Jatim, Lombok, Sulawesi, Sumatera
Consignment: SKIPPED (not retail)
"""

import sys
import argparse
import logging
from collections import defaultdict
from datetime import datetime

import psycopg2
import psycopg2.extras

# ==============================================================================
# CONFIG
# ==============================================================================

DB = dict(
    host="76.13.194.120",
    port=5432,
    dbname="openclaw_ops",
    user="openclaw_app",
    password="Zuma-0psCl4w-2026!"
)

# 12 month window
SALES_START = "2025-02-01"
SALES_END   = "2026-01-31"
ALL_MONTHS  = [
    "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
    "2025-07", "2025-08", "2025-09", "2025-10", "2025-11",
    "2025-12", "2026-01"
]

# Map store_display_options.area -> list of sales_with_product.area to query
# Handles area naming mismatches between the two tables
AREA_SALES_MAP = {
    "Bali 1":    ["Bali 1"],
    "Bali 2":    ["Bali 2"],
    "Bali 3":    ["Bali 3"],
    "Jakarta":   ["Jakarta"],
    "Jatim":     ["Jatim"],
    "Lombok":    ["Lombok"],
    "Sulawesi":  ["Sulawesi"],
    "Sumatera":  ["Sumatra", "Batam"],  # Two different area names in sales
    "Consignment": None,  # Skip
}

SIZE_COLUMNS = [
    '18/19', '20/21', '21/22', '22/23', '23/24', '24/25', '25/26',
    '27/28', '29/30', '31/32', '33/34',
    '34', '35', '35/36', '36', '37', '37/38', '38',
    '39', '39/40', '40', '41', '41/42', '42', '43', '43/44', '44', '45/46'
]

# DB column name for each size - match portal.temp_portal_plannogram convention (size_X_Y)
SIZE_TO_DB_COL = {s: f"size_{s.replace('/', '_')}" for s in SIZE_COLUMNS}
DB_SIZE_COLUMNS = [SIZE_TO_DB_COL[s] for s in SIZE_COLUMNS]

# Tiers to EXCLUDE from planogram
EXCLUDE_TIERS = {"4", "5"}

# Article name filters (exclude accessories)
ARTICLE_EXCLUDE_WORDS = [
    "SHOPPING BAG", "HANGER", "PAPER BAG", "THERMAL", "BOX LUCA"
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger(__name__)


# ==============================================================================
# DATABASE QUERIES
# ==============================================================================

def load_stores(conn, area_filter=None):
    """
    Load stores from portal.store_display_options.
    Also fetches the planogram_name -> sales_name mapping from portal.store_name_map
    for matching with sales data.
    Returns dict of store dicts, grouped by area.
    """
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Load store_name_map (planogram_name -> sales_name mapping)
    cur.execute("SELECT planogram_name, stock_nama_gudang FROM portal.store_name_map")
    name_map = {r["planogram_name"]: r["stock_nama_gudang"] for r in cur.fetchall()}
    log.info(f"Loaded {len(name_map)} store name mappings from portal.store_name_map")

    if area_filter:
        cur.execute("""
            SELECT area, store_name, store_name_map, SUM(capacity) AS max_display
            FROM portal.store_display_options
            WHERE area = %s AND store_name_map IS NOT NULL
            GROUP BY area, store_name, store_name_map
            ORDER BY area, store_name
        """, (area_filter,))
    else:
        cur.execute("""
            SELECT area, store_name, store_name_map, SUM(capacity) AS max_display
            FROM portal.store_display_options
            WHERE store_name_map IS NOT NULL
            GROUP BY area, store_name, store_name_map
            ORDER BY area, store_name
        """)

    stores_by_area = defaultdict(list)
    total = 0
    for row in cur.fetchall():
        area = row["area"]
        if AREA_SALES_MAP.get(area) is None:
            continue  # Skip Consignment or unknown areas

        # Get the sales_name from portal.store_name_map if available
        store_name = row["store_name"]
        sales_name = name_map.get(store_name)
        if sales_name:
            # Override store_name_map with the sales-matched name
            row["store_name_map"] = sales_name
        # else: use original store_name_map, may need fuzzy matching later

        stores_by_area[area].append(dict(row))
        total += 1

    cur.close()
    log.info(f"Loaded {total} stores from store_display_options across {len(stores_by_area)} areas")
    return stores_by_area


def load_assortment(conn):
    """
    Load size distribution ratios from portal.kodemix.
    Returns dict: kode_mix -> {size: count}
    """
    cur = conn.cursor()
    cur.execute("""
        SELECT kode_mix, size, count_by_assortment::int AS cnt
        FROM (
            SELECT DISTINCT ON (kode_mix, size)
                kode_mix, size, count_by_assortment, no_urut
            FROM portal.kodemix
            WHERE kode_mix IS NOT NULL AND size IS NOT NULL
              AND count_by_assortment IS NOT NULL
              AND count_by_assortment::text ~ '^[0-9]'
              AND count_by_assortment::int > 0
            ORDER BY kode_mix, size, no_urut
        ) sub
        ORDER BY kode_mix, size
    """)

    assortment = defaultdict(dict)
    for kode_mix, size, count in cur.fetchall():
        assortment[kode_mix][size] = count

    cur.close()
    log.info(f"Loaded assortment for {len(assortment)} kode_mix")
    return assortment


def load_sales_for_area(conn, sales_areas):
    """
    Load 12-month sales for given area(s) from core.sales_with_product.
    Queries by area (indexed path in underlying tables via view).
    
    Returns dict: store_name_lower -> {(kode_mix, article, gender, series, tier) -> {bulan: qty}}
    """
    if not sales_areas:
        return {}

    # Build exclusion filter
    exclude_clauses = " AND ".join(
        [f"UPPER(article) NOT LIKE '%%{word}%%'" for word in ARTICLE_EXCLUDE_WORDS]
    )

    area_placeholders = ",".join(["%s"] * len(sales_areas))

    query = f"""
        SELECT
            LOWER(TRIM(matched_store_name)) AS store_lower,
            kode_mix,
            article,
            gender,
            series,
            COALESCE(tier, '3') AS tier,
            TO_CHAR(transaction_date, 'YYYY-MM') AS bulan,
            SUM(quantity) AS total_qty
        FROM core.sales_with_product
        WHERE area IN ({area_placeholders})
          AND store_category = 'RETAIL'
          AND (is_intercompany IS NULL OR is_intercompany = FALSE)
          AND transaction_date >= '{SALES_START}'
          AND transaction_date <= '{SALES_END}'
          AND quantity > 0
          AND kode_mix IS NOT NULL
          AND {exclude_clauses}
        GROUP BY LOWER(TRIM(matched_store_name)), kode_mix, article, gender, series, tier,
                 TO_CHAR(transaction_date, 'YYYY-MM')
    """

    cur = conn.cursor()
    cur.execute(query, sales_areas)
    rows = cur.fetchall()
    cur.close()

    # Organize: store_lower -> article_key -> {bulan: qty}
    sales = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for row in rows:
        store_lower, kode_mix, article, gender, series, tier, bulan, qty = row
        article_key = (kode_mix, article, gender, series, str(tier))
        sales[store_lower][article_key][bulan] = int(qty)

    log.info(f"  Loaded {len(rows)} sales rows for {len(sales)} unique stores")
    return sales


# ==============================================================================
# TIER ADJUSTMENT LOGIC
# ==============================================================================

def calc_tier_adjusted_avg(monthly_data, tier):
    """
    Given 12 months of sales data, apply tier logic to get adjusted average.
    monthly_data: {bulan: qty} - only months with sales, missing months = 0
    Returns (adj_avg, n_months_used)
    """
    ordered_values = [monthly_data.get(m, 0) for m in ALL_MONTHS]
    tier = str(tier).strip()

    if tier in EXCLUDE_TIERS:
        return 0.0, 0

    if tier == "1":
        # T1: Exclude zero months (OOS treatment - don't penalize for stockouts)
        nonzero = [v for v in ordered_values if v > 0]
        if not nonzero:
            return 0.0, 0
        return sum(nonzero) / len(nonzero), len(nonzero)

    elif tier == "8":
        # T8: Exclude pre-launch (leading zeros) + post-launch (trailing zeros)
        first_nz = next((i for i, v in enumerate(ordered_values) if v > 0), None)
        if first_nz is None:
            return 0.0, 0
        last_nz = len(ordered_values) - 1 - next(
            (i for i, v in enumerate(reversed(ordered_values)) if v > 0), 0
        )
        trimmed = ordered_values[first_nz:last_nz + 1]
        if not trimmed:
            return 0.0, 0
        return sum(trimmed) / len(trimmed), len(trimmed)

    elif tier in ("2", "3", "0"):
        # T2/T3: Contextual zero exclusion
        # Exclude zero months where surrounding months indicate OOS (surroundings > 50% of avg)
        nonzero_vals = [v for v in ordered_values if v > 0]
        if not nonzero_vals:
            return 0.0, 0
        overall_avg = sum(nonzero_vals) / len(nonzero_vals)

        active = []
        for i, qty in enumerate(ordered_values):
            if qty > 0:
                active.append(qty)
            else:
                # Look at surrounding months (window ±2)
                surrounding = [ordered_values[j] for j in range(max(0, i-2), min(len(ordered_values), i+3)) if j != i and ordered_values[j] > 0]
                if surrounding:
                    surr_avg = sum(surrounding) / len(surrounding)
                    if surr_avg > overall_avg * 0.5:
                        # Surrounding is strong -> this zero is likely OOS -> exclude
                        pass
                    else:
                        active.append(0)  # Weak surroundings -> include the zero
                else:
                    active.append(0)  # No surrounding data -> include zero

        if not active:
            return 0.0, 0
        return sum(active) / len(active), len(active)

    else:
        # Default / NULL treated as T3
        nonzero = [v for v in ordered_values if v > 0]
        if not nonzero:
            return 0.0, 0
        return sum(nonzero) / len(nonzero), len(nonzero)


# ==============================================================================
# PLANOGRAM CALCULATION PER STORE
# ==============================================================================

def calculate_store_planogram(store_info, store_sales, assortment):
    """
    Calculate planogram rows for a single store.
    Returns list of row dicts ready for DB insertion.
    """
    area = store_info["area"]
    store_name = store_info["store_name"]
    store_db_name = store_info["store_name_map"]
    max_display = float(store_info["max_display"] or 100)

    if not store_sales:
        return []

    # Step 1: Calculate adjusted average per article
    article_avgs = {}
    for article_key, monthly_data in store_sales.items():
        kode_mix, article, gender, series, tier = article_key
        if tier in EXCLUDE_TIERS:
            continue
        adj_avg, _ = calc_tier_adjusted_avg(monthly_data, tier)
        if adj_avg > 0:
            article_avgs[article_key] = adj_avg

    if not article_avgs:
        return []

    # Step 2: Calculate sales mix
    total_avg = sum(article_avgs.values())
    if total_avg <= 0:
        return []

    rows = []
    for article_key, adj_avg in article_avgs.items():
        kode_mix, article, gender, series, tier = article_key

        sales_mix = adj_avg / total_avg
        reko_pairs = sales_mix * max_display
        reko_box = max(1, round(reko_pairs))

        # Step 3: Size distribution using assortment ratios
        sizes = assortment.get(kode_mix, {})
        size_total = sum(sizes.values()) if sizes else 0

        row = {
            "area": area,
            "store_name": store_name,
            "store_db_name": store_db_name,
            "gender": gender,
            "series": series,
            "article": article,
            "tier": tier,
            "article_mix": kode_mix,
            "avg_sales_3mo_pairs": round(adj_avg, 4),
            "sales_mix": round(sales_mix, 6),
            "rekomendasi_pairs": round(reko_pairs, 4),
            "rekomendasi_box": reko_box,
        }

        # Fill size columns
        for size in SIZE_COLUMNS:
            db_col = SIZE_TO_DB_COL[size]
            if size_total > 0 and size in sizes:
                # Size applies to this article, compute target
                row[db_col] = round(reko_pairs * (sizes[size] / size_total), 4)
            else:
                # NULL = size doesn't apply to this article
                row[db_col] = None

        rows.append(row)

    return rows


# ==============================================================================
# DB OPERATIONS
# ==============================================================================

def create_planogram_table(conn):
    """Create portal.planogram table if not exists."""
    cur = conn.cursor()

    log.info("Creating/verifying portal.planogram table...")

    size_cols_ddl = "\n".join(
        [f"    {col} NUMERIC," for col in DB_SIZE_COLUMNS]
    )

    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS portal.planogram (
            id SERIAL PRIMARY KEY,
            area TEXT NOT NULL,
            store_name TEXT NOT NULL,
            store_db_name TEXT,
            gender TEXT,
            series TEXT,
            article TEXT,
            tier TEXT,
            article_mix TEXT NOT NULL,
            {size_cols_ddl}
            avg_sales_3mo_pairs NUMERIC,
            sales_mix NUMERIC,
            rekomendasi_pairs NUMERIC,
            rekomendasi_box INTEGER,
            generated_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_planogram_area ON portal.planogram(area)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_planogram_store ON portal.planogram(store_name)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_planogram_article_mix ON portal.planogram(article_mix)")
    cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_planogram_store_article
        ON portal.planogram(store_name, article_mix)
    """)

    conn.commit()
    log.info("Table portal.planogram ready")
    cur.close()


def reset_planogram_area(conn, area):
    """Delete existing rows for an area."""
    cur = conn.cursor()
    cur.execute("DELETE FROM portal.planogram WHERE area = %s", (area,))
    deleted = cur.rowcount
    conn.commit()
    cur.close()
    if deleted:
        log.info(f"  Cleared {deleted} existing rows for area={area}")


def insert_planogram_rows(conn, rows, dry_run=False):
    """Insert planogram rows using ON CONFLICT DO UPDATE."""
    if not rows:
        return 0
    if dry_run:
        log.info(f"  [DRY RUN] Would insert {len(rows)} rows")
        return len(rows)

    all_cols = (
        ["area", "store_name", "store_db_name", "gender", "series",
         "article", "tier", "article_mix"]
        + DB_SIZE_COLUMNS
        + ["avg_sales_3mo_pairs", "sales_mix", "rekomendasi_pairs",
           "rekomendasi_box", "generated_at"]
    )
    update_cols = [c for c in all_cols if c not in ("store_name", "article_mix")]

    col_list     = ", ".join(all_cols)
    placeholders = ", ".join([f"%({c})s" for c in all_cols])
    update_clause = ", ".join([f"{c} = EXCLUDED.{c}" for c in update_cols])

    sql = f"""
        INSERT INTO portal.planogram ({col_list})
        VALUES ({placeholders})
        ON CONFLICT (store_name, article_mix) DO UPDATE SET {update_clause}
    """

    now = datetime.now()
    for row in rows:
        row["generated_at"] = now

    cur = conn.cursor()
    psycopg2.extras.execute_batch(cur, sql, rows, page_size=500)
    conn.commit()
    cur.close()
    return len(rows)


# ==============================================================================
# MAIN PIPELINE
# ==============================================================================

def run_pipeline(args):
    log.info("=" * 60)
    log.info("Zuma Planogram Generator - All Branches")
    log.info("=" * 60)

    conn = psycopg2.connect(**DB)

    if not args.dry_run:
        create_planogram_table(conn)

    log.info("Loading assortment data...")
    assortment = load_assortment(conn)

    log.info("Loading store display options...")
    stores_by_area = load_stores(conn, area_filter=args.area)

    total_rows = 0
    area_summary = {}

    for area in sorted(stores_by_area.keys()):
        if args.area and area != args.area:
            continue

        sales_areas = AREA_SALES_MAP.get(area)
        if sales_areas is None:
            log.info(f"Skipping area: {area} (no sales mapping)")
            continue

        area_stores = stores_by_area[area]
        log.info(f"\n{'='*50}")
        log.info(f"Processing: {area} ({len(area_stores)} stores) -> sales areas: {sales_areas}")

        # Load sales for this area (query by area = fast)
        log.info(f"  Querying sales from area(s): {sales_areas}...")
        raw_sales = load_sales_for_area(conn, sales_areas)

        # Log coverage
        store_name_maps_lower = {s["store_name_map"].lower().strip() for s in area_stores}
        sales_store_names = set(raw_sales.keys())

        matched_stores = store_name_maps_lower & sales_store_names
        unmatched = store_name_maps_lower - sales_store_names
        extra_in_sales = sales_store_names - store_name_maps_lower

        if unmatched:
            log.warning(f"  Stores with NO sales data: {unmatched}")
        if extra_in_sales:
            log.info(f"  Stores in sales NOT in display_options (excluded): {extra_in_sales}")

        # Reset area before inserting
        if not args.dry_run and not args.no_reset:
            reset_planogram_area(conn, area)

        area_rows = 0
        area_store_count = 0

        for store_info in area_stores:
            store_db_name_lower = store_info["store_name_map"].lower().strip()
            store_sales = raw_sales.get(store_db_name_lower, {})

            n_articles = len(store_sales)
            rows = calculate_store_planogram(store_info, store_sales, assortment)

            action = f"{len(rows)} rows" if rows else "SKIPPED (no sales)"
            log.info(f"  {store_info['store_name']:<30} | {n_articles:3} articles -> {action}")

            if rows:
                insert_planogram_rows(conn, rows, dry_run=args.dry_run)
                area_rows += len(rows)
                area_store_count += 1

        area_summary[area] = {
            "stores_with_data": area_store_count,
            "total_stores": len(area_stores),
            "rows": area_rows,
        }
        log.info(f"  Area {area}: {area_store_count}/{len(area_stores)} stores, {area_rows} planogram rows")
        total_rows += area_rows

    # Final summary
    log.info("\n" + "=" * 60)
    log.info("FINAL SUMMARY")
    log.info("=" * 60)
    for area, s in sorted(area_summary.items()):
        log.info(f"  {area:15} | {s['stores_with_data']:2}/{s['total_stores']:2} stores | {s['rows']:5} rows")
    log.info(f"\n  TOTAL: {total_rows} planogram rows")
    if args.dry_run:
        log.info("  [DRY RUN] No data was written to DB")

    conn.close()
    return total_rows


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Zuma planogram for all branches")
    parser.add_argument("--dry-run", action="store_true", help="Calculate but don't write to DB")
    parser.add_argument("--area", type=str, default=None, help="Process only one area (e.g. 'Jatim')")
    parser.add_argument("--no-reset", action="store_true", help="Don't delete existing rows first")
    args = parser.parse_args()

    result = run_pipeline(args)
    sys.exit(0 if result >= 0 else 1)
