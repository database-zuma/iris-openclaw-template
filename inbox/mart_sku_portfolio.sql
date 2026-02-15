-- =============================================================================
-- mart.sku_portfolio — ALL-IN-ONE SKU Performance Analysis Table
-- =============================================================================
-- Purpose:  Replace Control Stock report for Merchandiser & R&D teams
-- Grain:    One row per kode_mix (article level, NO size breakdown)
-- Columns:  100 active columns (+ 2 PO placeholders for future + updated_at = 103)
-- Refresh:  Snapshot table — rebuild daily/periodically via TRUNCATE + INSERT
-- Author:   Auto-generated
-- Date:     2026-02-15
--
-- BUSINESS RULES:
--   1. Sales exclude is_intercompany = TRUE (inter-entity DDD↔MBB↔UBB↔LJBB transfers)
--   2. Sales exclude non-product items (SHOPPING BAG, HANGER, PAPER BAG, THERMAL, BOX LUCA)
--   3. Year auto-detected: current_year = EXTRACT(YEAR FROM CURRENT_DATE), last_year = current_year - 1
--   4. kode_mix from portal.kodemix with DISTINCT ON (kode_mix) ORDER BY no_urut — picks latest version
--   5. tier = COALESCE(tier_baru, tier_lama, '3') — NULL defaults to T3
--   6. Stock channels mapped by nama_gudang pattern matching (no portal.legend_warehouse exists)
--   7. avg_last_3_months = avg monthly qty sold in last 3 COMPLETE calendar months
--   8. Turnover (TO) = stock / avg_monthly_sales = months of coverage
--   9. PO columns SKIPPED (po_ongoing, to_plus_po) — future ALTER TABLE when raw.po ready
--
-- JOIN LOGIC & DUPLICATE HANDLING:
--   - Article master: DISTINCT ON (kode_mix) ORDER BY no_urut from portal.kodemix
--     → Ensures exactly ONE row per article regardless of multiple versions (V0-V4)
--   - Sales source: core.sales_with_product (already deduped via fact_sales_unified DISTINCT ON)
--     → Grouped by kode_mix → no duplicate risk since aggregation collapses rows
--   - Stock source: core.stock_with_product (already latest snapshot via MAX(snapshot_date))
--     → Grouped by kode_mix → safe aggregation
--   - NO direct portal.kodemix JOIN in sales/stock CTEs — we use the core views which already
--     handle the DISTINCT ON dedup for kode_besar → kode_mix mapping
--   - Final JOIN: articles LEFT JOIN sales LEFT JOIN stock
--     → LEFT JOIN ensures articles with no sales or no stock still appear (with 0s)
--
-- WAREHOUSE CLASSIFICATION (no portal.legend_warehouse table exists):
--   wh_pusat:    nama_gudang LIKE '%warehouse pusat%' (excl reject)
--   wh_bali:     nama_gudang LIKE '%warehouse bali%' (excl reject)
--   wh_jkt:      nama_gudang LIKE '%warehouse pluit%' OR '%warehouse jakarta%' OR '%warehouse palembang%' (excl reject)
--   stok_toko:   gudang_category = 'RETAIL'
--   stok_online: nama_gudang LIKE '%online%' OR '%agency%' OR '%shopee%'
--   stok_unlabel: everything else (events, wholesale, consignment, bazaar, unmatched)
--
-- STOCK CHANNEL VALIDATION (from exploration 2026-02-15):
--   wh_pusat:    2 locations, ~153K qty  (Warehouse Pusat, Warehouse Pusat Protol)
--   wh_bali:    10 locations, ~81K qty   (Warehouse Bali*, Warehouse Bali Gatsu*)
--   wh_jkt:      3 locations, ~14K qty   (Warehouse Pluit, Warehouse Jakarta, Warehouse Palembang)
--   stok_toko:  53 locations, ~149K qty  (all RETAIL category stores)
--   stok_online: 9 locations, ~34K qty   (Warehouse Online*, Agency*, ZUMA Online*)
--   stok_unlabel: ~151 locations, ~76K qty (events, bazaar, consignment, HO, etc.)
-- =============================================================================


-- =============================================================================
-- SECTION 1: DDL — CREATE TABLE
-- =============================================================================

DROP TABLE IF EXISTS mart.sku_portfolio;

CREATE TABLE mart.sku_portfolio (
    -- GROUP 1: ID / Base (7 columns)
    id                  SERIAL PRIMARY KEY,
    kodemix             TEXT NOT NULL,
    gender              TEXT,
    series              TEXT,
    color               TEXT,
    tipe                TEXT,
    tier                TEXT,

    -- GROUP 2: Year Labels (2 columns)
    current_year_label  TEXT NOT NULL,
    last_year_label     TEXT NOT NULL,

    -- GROUP 2: Monthly Sales — January (6 columns)
    now_jan_rp          NUMERIC(15,2) DEFAULT 0,
    last_jan_rp         NUMERIC(15,2) DEFAULT 0,
    var_jan_rp          NUMERIC(7,2),
    now_jan_qty         INTEGER DEFAULT 0,
    last_jan_qty        INTEGER DEFAULT 0,
    var_jan_qty         NUMERIC(7,2),

    -- GROUP 2: Monthly Sales — February (6 columns)
    now_feb_rp          NUMERIC(15,2) DEFAULT 0,
    last_feb_rp         NUMERIC(15,2) DEFAULT 0,
    var_feb_rp          NUMERIC(7,2),
    now_feb_qty         INTEGER DEFAULT 0,
    last_feb_qty        INTEGER DEFAULT 0,
    var_feb_qty         NUMERIC(7,2),

    -- GROUP 2: Monthly Sales — March (6 columns)
    now_mar_rp          NUMERIC(15,2) DEFAULT 0,
    last_mar_rp         NUMERIC(15,2) DEFAULT 0,
    var_mar_rp          NUMERIC(7,2),
    now_mar_qty         INTEGER DEFAULT 0,
    last_mar_qty        INTEGER DEFAULT 0,
    var_mar_qty         NUMERIC(7,2),

    -- GROUP 2: Monthly Sales — April (6 columns)
    now_apr_rp          NUMERIC(15,2) DEFAULT 0,
    last_apr_rp         NUMERIC(15,2) DEFAULT 0,
    var_apr_rp          NUMERIC(7,2),
    now_apr_qty         INTEGER DEFAULT 0,
    last_apr_qty        INTEGER DEFAULT 0,
    var_apr_qty         NUMERIC(7,2),

    -- GROUP 2: Monthly Sales — May (6 columns)
    now_may_rp          NUMERIC(15,2) DEFAULT 0,
    last_may_rp         NUMERIC(15,2) DEFAULT 0,
    var_may_rp          NUMERIC(7,2),
    now_may_qty         INTEGER DEFAULT 0,
    last_may_qty        INTEGER DEFAULT 0,
    var_may_qty         NUMERIC(7,2),

    -- GROUP 2: Monthly Sales — June (6 columns)
    now_jun_rp          NUMERIC(15,2) DEFAULT 0,
    last_jun_rp         NUMERIC(15,2) DEFAULT 0,
    var_jun_rp          NUMERIC(7,2),
    now_jun_qty         INTEGER DEFAULT 0,
    last_jun_qty        INTEGER DEFAULT 0,
    var_jun_qty         NUMERIC(7,2),

    -- GROUP 2: Monthly Sales — July (6 columns)
    now_jul_rp          NUMERIC(15,2) DEFAULT 0,
    last_jul_rp         NUMERIC(15,2) DEFAULT 0,
    var_jul_rp          NUMERIC(7,2),
    now_jul_qty         INTEGER DEFAULT 0,
    last_jul_qty        INTEGER DEFAULT 0,
    var_jul_qty         NUMERIC(7,2),

    -- GROUP 2: Monthly Sales — August (6 columns)
    now_aug_rp          NUMERIC(15,2) DEFAULT 0,
    last_aug_rp         NUMERIC(15,2) DEFAULT 0,
    var_aug_rp          NUMERIC(7,2),
    now_aug_qty         INTEGER DEFAULT 0,
    last_aug_qty        INTEGER DEFAULT 0,
    var_aug_qty         NUMERIC(7,2),

    -- GROUP 2: Monthly Sales — September (6 columns)
    now_sep_rp          NUMERIC(15,2) DEFAULT 0,
    last_sep_rp         NUMERIC(15,2) DEFAULT 0,
    var_sep_rp          NUMERIC(7,2),
    now_sep_qty         INTEGER DEFAULT 0,
    last_sep_qty        INTEGER DEFAULT 0,
    var_sep_qty         NUMERIC(7,2),

    -- GROUP 2: Monthly Sales — October (6 columns)
    now_oct_rp          NUMERIC(15,2) DEFAULT 0,
    last_oct_rp         NUMERIC(15,2) DEFAULT 0,
    var_oct_rp          NUMERIC(7,2),
    now_oct_qty         INTEGER DEFAULT 0,
    last_oct_qty        INTEGER DEFAULT 0,
    var_oct_qty         NUMERIC(7,2),

    -- GROUP 2: Monthly Sales — November (6 columns)
    now_nov_rp          NUMERIC(15,2) DEFAULT 0,
    last_nov_rp         NUMERIC(15,2) DEFAULT 0,
    var_nov_rp          NUMERIC(7,2),
    now_nov_qty         INTEGER DEFAULT 0,
    last_nov_qty        INTEGER DEFAULT 0,
    var_nov_qty         NUMERIC(7,2),

    -- GROUP 2: Monthly Sales — December (6 columns)
    now_dec_rp          NUMERIC(15,2) DEFAULT 0,
    last_dec_rp         NUMERIC(15,2) DEFAULT 0,
    var_dec_rp          NUMERIC(7,2),
    now_dec_qty         INTEGER DEFAULT 0,
    last_dec_qty        INTEGER DEFAULT 0,
    var_dec_qty         NUMERIC(7,2),

    -- GROUP 2: Year Totals (6 columns)
    current_year_rp     NUMERIC(15,2) DEFAULT 0,
    last_year_rp        NUMERIC(15,2) DEFAULT 0,
    var_year_rp         NUMERIC(7,2),
    current_year_qty    INTEGER DEFAULT 0,
    last_year_qty       INTEGER DEFAULT 0,
    var_year_qty        NUMERIC(7,2),

    -- GROUP 2: Sales Mix & Recent Performance (3 columns)
    current_sales_mix   NUMERIC(7,4),   -- % contribution of this article to total current year Rp
    last_sales_mix      NUMERIC(7,4),   -- % contribution of this article to total last year Rp
    avg_last_3_months   NUMERIC(10,2) DEFAULT 0,  -- avg monthly qty (pairs) sold in last 3 complete months

    -- GROUP 3: Warehouse Stock (4 columns)
    wh_pusat            INTEGER DEFAULT 0,
    wh_bali             INTEGER DEFAULT 0,
    wh_jkt              INTEGER DEFAULT 0,
    wh_total            INTEGER DEFAULT 0,  -- = wh_pusat + wh_bali + wh_jkt

    -- GROUP 3: Channel Stock (3 columns)
    stok_toko           INTEGER DEFAULT 0,  -- RETAIL stores
    stok_online         INTEGER DEFAULT 0,  -- online channel warehouses
    stok_unlabel        INTEGER DEFAULT 0,  -- events, wholesale, consignment, unmapped

    -- GROUP 3: Total Stock (1 column)
    stok_global         INTEGER DEFAULT 0,  -- = wh_total + stok_toko + stok_online + stok_unlabel

    -- GROUP 3: Turnover (2 columns)
    to_wh               NUMERIC(10,2),  -- wh_total / NULLIF(avg_last_3_months, 0)
    to_total            NUMERIC(10,2),  -- stok_global / NULLIF(avg_last_3_months, 0)

    -- GROUP 3: PO Placeholders (SKIPPED — future ALTER TABLE)
    -- po_ongoing       INTEGER,        -- SKIP: waiting for raw.po table
    -- to_plus_po       NUMERIC(10,2),  -- SKIP: (stok_global + po_ongoing) / avg_last_3_months

    -- Metadata
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Column count: 7 (base) + 2 (year labels) + 72 (monthly) + 6 (year totals)
--              + 3 (sales mix/recent) + 4 (wh stock) + 3 (channel stock) + 1 (total stock)
--              + 2 (turnover) + 1 (updated_at) = 101 columns
-- Future PO columns will add 2 more = 103 total

COMMENT ON TABLE mart.sku_portfolio IS 'ALL-IN-ONE SKU performance analysis at article (kode_mix) level. Replaces Control Stock report. Auto-detected YoY comparison.';
COMMENT ON COLUMN mart.sku_portfolio.kodemix IS 'Unified article code from portal.kodemix — version-agnostic, aggregates V0-V4';
COMMENT ON COLUMN mart.sku_portfolio.avg_last_3_months IS 'Average monthly PAIRS sold in last 3 complete calendar months — used as denominator for TO';
COMMENT ON COLUMN mart.sku_portfolio.to_wh IS 'Warehouse turnover = wh_total / avg_last_3_months — months of WH stock coverage';
COMMENT ON COLUMN mart.sku_portfolio.to_total IS 'Total turnover = stok_global / avg_last_3_months — months of total stock coverage';
COMMENT ON COLUMN mart.sku_portfolio.stok_unlabel IS 'Stock in unmapped locations (events, wholesale, consignment, bazaar). Minor = OK. Major = check portal.stock_capacity mapping gaps.';
COMMENT ON COLUMN mart.sku_portfolio.var_jan_rp IS 'YoY % variance: (now_jan_rp - last_jan_rp) / last_jan_rp * 100. NULL if last year = 0.';
COMMENT ON COLUMN mart.sku_portfolio.current_sales_mix IS '% contribution of this article Rp to total current year Rp across all articles';


-- =============================================================================
-- SECTION 2: POPULATION QUERY
-- =============================================================================
-- Strategy: TRUNCATE + INSERT for idempotent refresh
-- Run this daily/periodically to refresh the snapshot

TRUNCATE TABLE mart.sku_portfolio;

INSERT INTO mart.sku_portfolio (
    kodemix, gender, series, color, tipe, tier,
    current_year_label, last_year_label,
    -- Monthly: Jan
    now_jan_rp, last_jan_rp, var_jan_rp, now_jan_qty, last_jan_qty, var_jan_qty,
    -- Monthly: Feb
    now_feb_rp, last_feb_rp, var_feb_rp, now_feb_qty, last_feb_qty, var_feb_qty,
    -- Monthly: Mar
    now_mar_rp, last_mar_rp, var_mar_rp, now_mar_qty, last_mar_qty, var_mar_qty,
    -- Monthly: Apr
    now_apr_rp, last_apr_rp, var_apr_rp, now_apr_qty, last_apr_qty, var_apr_qty,
    -- Monthly: May
    now_may_rp, last_may_rp, var_may_rp, now_may_qty, last_may_qty, var_may_qty,
    -- Monthly: Jun
    now_jun_rp, last_jun_rp, var_jun_rp, now_jun_qty, last_jun_qty, var_jun_qty,
    -- Monthly: Jul
    now_jul_rp, last_jul_rp, var_jul_rp, now_jul_qty, last_jul_qty, var_jul_qty,
    -- Monthly: Aug
    now_aug_rp, last_aug_rp, var_aug_rp, now_aug_qty, last_aug_qty, var_aug_qty,
    -- Monthly: Sep
    now_sep_rp, last_sep_rp, var_sep_rp, now_sep_qty, last_sep_qty, var_sep_qty,
    -- Monthly: Oct
    now_oct_rp, last_oct_rp, var_oct_rp, now_oct_qty, last_oct_qty, var_oct_qty,
    -- Monthly: Nov
    now_nov_rp, last_nov_rp, var_nov_rp, now_nov_qty, last_nov_qty, var_nov_qty,
    -- Monthly: Dec
    now_dec_rp, last_dec_rp, var_dec_rp, now_dec_qty, last_dec_qty, var_dec_qty,
    -- Year totals
    current_year_rp, last_year_rp, var_year_rp,
    current_year_qty, last_year_qty, var_year_qty,
    -- Sales mix & recent
    current_sales_mix, last_sales_mix, avg_last_3_months,
    -- Stock
    wh_pusat, wh_bali, wh_jkt, wh_total,
    stok_toko, stok_online, stok_unlabel, stok_global,
    to_wh, to_total,
    -- Metadata
    updated_at
)
WITH
-- ---------------------------------------------------------------
-- CTE 1: Year parameters (auto-detect, NEVER hardcoded)
-- ---------------------------------------------------------------
params AS (
    SELECT
        EXTRACT(YEAR FROM CURRENT_DATE)::int AS cy,
        (EXTRACT(YEAR FROM CURRENT_DATE) - 1)::int AS ly
),

-- ---------------------------------------------------------------
-- CTE 2: Article master — one row per kode_mix
-- Uses DISTINCT ON (kode_mix) ordered by no_urut to pick latest version
-- NEVER filters by status (Rule 3: include Aktif AND Tidak Aktif)
-- ---------------------------------------------------------------
articles AS (
    SELECT DISTINCT ON (kode_mix)
        kode_mix,
        gender,
        series,
        color,
        tipe,
        COALESCE(tier_baru, tier_lama, '3') AS tier
    FROM portal.kodemix
    WHERE kode_mix IS NOT NULL
    ORDER BY kode_mix, no_urut
),

-- ---------------------------------------------------------------
-- CTE 3: Sales base — cleaned & filtered
-- Source: core.sales_with_product (already deduped via DISTINCT ON in fact_sales_unified)
-- Filters: exclude intercompany, exclude non-products, only current + last year
-- ---------------------------------------------------------------
sales_base AS (
    SELECT
        s.kode_mix,
        EXTRACT(YEAR FROM s.transaction_date)::int  AS sale_year,
        EXTRACT(MONTH FROM s.transaction_date)::int AS sale_month,
        s.quantity,
        s.total_amount
    FROM core.sales_with_product s
    WHERE s.is_intercompany = FALSE
      AND s.kode_mix IS NOT NULL
      AND UPPER(COALESCE(s.article, '')) NOT LIKE '%SHOPPING BAG%'
      AND UPPER(COALESCE(s.article, '')) NOT LIKE '%HANGER%'
      AND UPPER(COALESCE(s.article, '')) NOT LIKE '%PAPER BAG%'
      AND UPPER(COALESCE(s.article, '')) NOT LIKE '%THERMAL%'
      AND UPPER(COALESCE(s.article, '')) NOT LIKE '%BOX LUCA%'
      AND EXTRACT(YEAR FROM s.transaction_date) >= (SELECT ly FROM params)
      AND EXTRACT(YEAR FROM s.transaction_date) <= (SELECT cy FROM params)
),

-- ---------------------------------------------------------------
-- CTE 4: Pivoted sales — one row per kode_mix with all monthly + yearly columns
-- Uses conditional aggregation (CASE WHEN) to pivot months into columns
-- ---------------------------------------------------------------
sales_pivot AS (
    SELECT
        sb.kode_mix,

        -- === JANUARY ===
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 1 THEN sb.total_amount END), 0) AS now_jan_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 1 THEN sb.total_amount END), 0) AS last_jan_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 1 THEN sb.quantity END), 0)::int AS now_jan_qty,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 1 THEN sb.quantity END), 0)::int AS last_jan_qty,

        -- === FEBRUARY ===
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 2 THEN sb.total_amount END), 0) AS now_feb_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 2 THEN sb.total_amount END), 0) AS last_feb_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 2 THEN sb.quantity END), 0)::int AS now_feb_qty,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 2 THEN sb.quantity END), 0)::int AS last_feb_qty,

        -- === MARCH ===
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 3 THEN sb.total_amount END), 0) AS now_mar_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 3 THEN sb.total_amount END), 0) AS last_mar_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 3 THEN sb.quantity END), 0)::int AS now_mar_qty,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 3 THEN sb.quantity END), 0)::int AS last_mar_qty,

        -- === APRIL ===
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 4 THEN sb.total_amount END), 0) AS now_apr_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 4 THEN sb.total_amount END), 0) AS last_apr_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 4 THEN sb.quantity END), 0)::int AS now_apr_qty,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 4 THEN sb.quantity END), 0)::int AS last_apr_qty,

        -- === MAY ===
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 5 THEN sb.total_amount END), 0) AS now_may_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 5 THEN sb.total_amount END), 0) AS last_may_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 5 THEN sb.quantity END), 0)::int AS now_may_qty,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 5 THEN sb.quantity END), 0)::int AS last_may_qty,

        -- === JUNE ===
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 6 THEN sb.total_amount END), 0) AS now_jun_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 6 THEN sb.total_amount END), 0) AS last_jun_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 6 THEN sb.quantity END), 0)::int AS now_jun_qty,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 6 THEN sb.quantity END), 0)::int AS last_jun_qty,

        -- === JULY ===
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 7 THEN sb.total_amount END), 0) AS now_jul_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 7 THEN sb.total_amount END), 0) AS last_jul_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 7 THEN sb.quantity END), 0)::int AS now_jul_qty,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 7 THEN sb.quantity END), 0)::int AS last_jul_qty,

        -- === AUGUST ===
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 8 THEN sb.total_amount END), 0) AS now_aug_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 8 THEN sb.total_amount END), 0) AS last_aug_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 8 THEN sb.quantity END), 0)::int AS now_aug_qty,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 8 THEN sb.quantity END), 0)::int AS last_aug_qty,

        -- === SEPTEMBER ===
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 9 THEN sb.total_amount END), 0) AS now_sep_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 9 THEN sb.total_amount END), 0) AS last_sep_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 9 THEN sb.quantity END), 0)::int AS now_sep_qty,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 9 THEN sb.quantity END), 0)::int AS last_sep_qty,

        -- === OCTOBER ===
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 10 THEN sb.total_amount END), 0) AS now_oct_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 10 THEN sb.total_amount END), 0) AS last_oct_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 10 THEN sb.quantity END), 0)::int AS now_oct_qty,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 10 THEN sb.quantity END), 0)::int AS last_oct_qty,

        -- === NOVEMBER ===
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 11 THEN sb.total_amount END), 0) AS now_nov_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 11 THEN sb.total_amount END), 0) AS last_nov_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 11 THEN sb.quantity END), 0)::int AS now_nov_qty,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 11 THEN sb.quantity END), 0)::int AS last_nov_qty,

        -- === DECEMBER ===
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 12 THEN sb.total_amount END), 0) AS now_dec_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 12 THEN sb.total_amount END), 0) AS last_dec_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy AND sb.sale_month = 12 THEN sb.quantity END), 0)::int AS now_dec_qty,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly AND sb.sale_month = 12 THEN sb.quantity END), 0)::int AS last_dec_qty,

        -- === YEAR TOTALS ===
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy THEN sb.total_amount END), 0) AS current_year_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly THEN sb.total_amount END), 0) AS last_year_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy THEN sb.quantity END), 0)::int AS current_year_qty,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly THEN sb.quantity END), 0)::int AS last_year_qty

    FROM sales_base sb
    CROSS JOIN params p
    GROUP BY sb.kode_mix
),

-- ---------------------------------------------------------------
-- CTE 5: Total sales across ALL articles (for sales_mix calculation)
-- ---------------------------------------------------------------
total_sales AS (
    SELECT
        COALESCE(SUM(CASE WHEN sb.sale_year = p.cy THEN sb.total_amount END), 0) AS total_current_rp,
        COALESCE(SUM(CASE WHEN sb.sale_year = p.ly THEN sb.total_amount END), 0) AS total_last_rp
    FROM sales_base sb
    CROSS JOIN params p
),

-- ---------------------------------------------------------------
-- CTE 6: Average last 3 complete months sales (qty pairs/month)
-- Uses DATE_TRUNC to handle cross-year boundaries correctly
-- Example: If today = 2026-02-15, last 3 complete months = Nov 2025, Dec 2025, Jan 2026
-- ---------------------------------------------------------------
recent_sales AS (
    SELECT
        s.kode_mix,
        ROUND(SUM(s.quantity) / 3.0, 2) AS avg_last_3_months
    FROM core.sales_with_product s
    WHERE s.is_intercompany = FALSE
      AND s.kode_mix IS NOT NULL
      AND UPPER(COALESCE(s.article, '')) NOT LIKE '%SHOPPING BAG%'
      AND UPPER(COALESCE(s.article, '')) NOT LIKE '%HANGER%'
      AND UPPER(COALESCE(s.article, '')) NOT LIKE '%PAPER BAG%'
      AND UPPER(COALESCE(s.article, '')) NOT LIKE '%THERMAL%'
      AND UPPER(COALESCE(s.article, '')) NOT LIKE '%BOX LUCA%'
      AND s.transaction_date >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '3 months'
      AND s.transaction_date <  DATE_TRUNC('month', CURRENT_DATE)  -- exclude current incomplete month
    GROUP BY s.kode_mix
),

-- ---------------------------------------------------------------
-- CTE 7: Stock aggregation by channel
-- Source: core.stock_with_product (latest snapshot, already deduped)
-- Classification: warehouse (pusat/bali/jkt), toko, online, unlabel
-- ---------------------------------------------------------------
stock_agg AS (
    SELECT
        swp.kode_mix,

        -- Warehouse Pusat: "Warehouse Pusat" + "Warehouse Pusat Protol" (excl Reject)
        COALESCE(SUM(CASE
            WHEN LOWER(swp.nama_gudang) LIKE 'warehouse pusat%'
             AND LOWER(swp.nama_gudang) NOT LIKE '%reject%'
            THEN swp.quantity END), 0)::int AS wh_pusat,

        -- Warehouse Bali: all "Warehouse Bali*" variants (excl Reject, Non Sandal)
        COALESCE(SUM(CASE
            WHEN LOWER(swp.nama_gudang) LIKE 'warehouse bali%'
             AND LOWER(swp.nama_gudang) NOT LIKE '%reject%'
             AND LOWER(swp.nama_gudang) NOT LIKE '%non sandal%'
            THEN swp.quantity END), 0)::int AS wh_bali,

        -- Warehouse Jakarta: Pluit + Jakarta + Palembang (excl Reject)
        COALESCE(SUM(CASE
            WHEN (   LOWER(swp.nama_gudang) LIKE 'warehouse pluit%'
                  OR LOWER(swp.nama_gudang) LIKE 'warehouse jakarta%'
                  OR LOWER(swp.nama_gudang) LIKE 'warehouse palembang%'
                 )
             AND LOWER(swp.nama_gudang) NOT LIKE '%reject%'
            THEN swp.quantity END), 0)::int AS wh_jkt,

        -- Toko (Retail stores): gudang_category = 'RETAIL'
        COALESCE(SUM(CASE
            WHEN swp.gudang_category = 'RETAIL'
            THEN swp.quantity END), 0)::int AS stok_toko,

        -- Online: names containing 'online', 'agency', 'shopee'
        COALESCE(SUM(CASE
            WHEN LOWER(swp.nama_gudang) LIKE '%online%'
              OR LOWER(swp.nama_gudang) LIKE '%agency%'
              OR LOWER(swp.nama_gudang) LIKE '%shopee%'
            THEN swp.quantity END), 0)::int AS stok_online,

        -- Unlabel: everything NOT classified above
        -- (events, wholesale, consignment, bazaar, HO, transit, reject, non-sandal)
        COALESCE(SUM(CASE
            WHEN NOT (
                -- Not warehouse pusat
                (LOWER(swp.nama_gudang) LIKE 'warehouse pusat%' AND LOWER(swp.nama_gudang) NOT LIKE '%reject%')
                -- Not warehouse bali
                OR (LOWER(swp.nama_gudang) LIKE 'warehouse bali%' AND LOWER(swp.nama_gudang) NOT LIKE '%reject%' AND LOWER(swp.nama_gudang) NOT LIKE '%non sandal%')
                -- Not warehouse jkt
                OR ((LOWER(swp.nama_gudang) LIKE 'warehouse pluit%' OR LOWER(swp.nama_gudang) LIKE 'warehouse jakarta%' OR LOWER(swp.nama_gudang) LIKE 'warehouse palembang%') AND LOWER(swp.nama_gudang) NOT LIKE '%reject%')
                -- Not toko (COALESCE handles NULL gudang_category to avoid SQL 3-valued logic poisoning NOT)
                OR COALESCE(swp.gudang_category, '') = 'RETAIL'
                -- Not online
                OR LOWER(swp.nama_gudang) LIKE '%online%'
                OR LOWER(swp.nama_gudang) LIKE '%agency%'
                OR LOWER(swp.nama_gudang) LIKE '%shopee%'
            )
            THEN swp.quantity END), 0)::int AS stok_unlabel

    FROM core.stock_with_product swp
    WHERE swp.kode_mix IS NOT NULL
    GROUP BY swp.kode_mix
)

-- ---------------------------------------------------------------
-- FINAL SELECT: Join all CTEs together
-- ---------------------------------------------------------------
SELECT
    -- GROUP 1: Base
    a.kode_mix                          AS kodemix,
    a.gender,
    a.series,
    a.color,
    a.tipe,
    a.tier,

    -- Year Labels
    p.cy::text                          AS current_year_label,
    p.ly::text                          AS last_year_label,

    -- === JANUARY ===
    COALESCE(sp.now_jan_rp, 0),
    COALESCE(sp.last_jan_rp, 0),
    CASE WHEN COALESCE(sp.last_jan_rp, 0) <> 0
         THEN ROUND((COALESCE(sp.now_jan_rp, 0) - sp.last_jan_rp) / sp.last_jan_rp * 100, 2)
    END                                 AS var_jan_rp,
    COALESCE(sp.now_jan_qty, 0),
    COALESCE(sp.last_jan_qty, 0),
    CASE WHEN COALESCE(sp.last_jan_qty, 0) <> 0
         THEN ROUND((COALESCE(sp.now_jan_qty, 0) - sp.last_jan_qty)::numeric / sp.last_jan_qty * 100, 2)
    END                                 AS var_jan_qty,

    -- === FEBRUARY ===
    COALESCE(sp.now_feb_rp, 0),
    COALESCE(sp.last_feb_rp, 0),
    CASE WHEN COALESCE(sp.last_feb_rp, 0) <> 0
         THEN ROUND((COALESCE(sp.now_feb_rp, 0) - sp.last_feb_rp) / sp.last_feb_rp * 100, 2)
    END                                 AS var_feb_rp,
    COALESCE(sp.now_feb_qty, 0),
    COALESCE(sp.last_feb_qty, 0),
    CASE WHEN COALESCE(sp.last_feb_qty, 0) <> 0
         THEN ROUND((COALESCE(sp.now_feb_qty, 0) - sp.last_feb_qty)::numeric / sp.last_feb_qty * 100, 2)
    END                                 AS var_feb_qty,

    -- === MARCH ===
    COALESCE(sp.now_mar_rp, 0),
    COALESCE(sp.last_mar_rp, 0),
    CASE WHEN COALESCE(sp.last_mar_rp, 0) <> 0
         THEN ROUND((COALESCE(sp.now_mar_rp, 0) - sp.last_mar_rp) / sp.last_mar_rp * 100, 2)
    END                                 AS var_mar_rp,
    COALESCE(sp.now_mar_qty, 0),
    COALESCE(sp.last_mar_qty, 0),
    CASE WHEN COALESCE(sp.last_mar_qty, 0) <> 0
         THEN ROUND((COALESCE(sp.now_mar_qty, 0) - sp.last_mar_qty)::numeric / sp.last_mar_qty * 100, 2)
    END                                 AS var_mar_qty,

    -- === APRIL ===
    COALESCE(sp.now_apr_rp, 0),
    COALESCE(sp.last_apr_rp, 0),
    CASE WHEN COALESCE(sp.last_apr_rp, 0) <> 0
         THEN ROUND((COALESCE(sp.now_apr_rp, 0) - sp.last_apr_rp) / sp.last_apr_rp * 100, 2)
    END                                 AS var_apr_rp,
    COALESCE(sp.now_apr_qty, 0),
    COALESCE(sp.last_apr_qty, 0),
    CASE WHEN COALESCE(sp.last_apr_qty, 0) <> 0
         THEN ROUND((COALESCE(sp.now_apr_qty, 0) - sp.last_apr_qty)::numeric / sp.last_apr_qty * 100, 2)
    END                                 AS var_apr_qty,

    -- === MAY ===
    COALESCE(sp.now_may_rp, 0),
    COALESCE(sp.last_may_rp, 0),
    CASE WHEN COALESCE(sp.last_may_rp, 0) <> 0
         THEN ROUND((COALESCE(sp.now_may_rp, 0) - sp.last_may_rp) / sp.last_may_rp * 100, 2)
    END                                 AS var_may_rp,
    COALESCE(sp.now_may_qty, 0),
    COALESCE(sp.last_may_qty, 0),
    CASE WHEN COALESCE(sp.last_may_qty, 0) <> 0
         THEN ROUND((COALESCE(sp.now_may_qty, 0) - sp.last_may_qty)::numeric / sp.last_may_qty * 100, 2)
    END                                 AS var_may_qty,

    -- === JUNE ===
    COALESCE(sp.now_jun_rp, 0),
    COALESCE(sp.last_jun_rp, 0),
    CASE WHEN COALESCE(sp.last_jun_rp, 0) <> 0
         THEN ROUND((COALESCE(sp.now_jun_rp, 0) - sp.last_jun_rp) / sp.last_jun_rp * 100, 2)
    END                                 AS var_jun_rp,
    COALESCE(sp.now_jun_qty, 0),
    COALESCE(sp.last_jun_qty, 0),
    CASE WHEN COALESCE(sp.last_jun_qty, 0) <> 0
         THEN ROUND((COALESCE(sp.now_jun_qty, 0) - sp.last_jun_qty)::numeric / sp.last_jun_qty * 100, 2)
    END                                 AS var_jun_qty,

    -- === JULY ===
    COALESCE(sp.now_jul_rp, 0),
    COALESCE(sp.last_jul_rp, 0),
    CASE WHEN COALESCE(sp.last_jul_rp, 0) <> 0
         THEN ROUND((COALESCE(sp.now_jul_rp, 0) - sp.last_jul_rp) / sp.last_jul_rp * 100, 2)
    END                                 AS var_jul_rp,
    COALESCE(sp.now_jul_qty, 0),
    COALESCE(sp.last_jul_qty, 0),
    CASE WHEN COALESCE(sp.last_jul_qty, 0) <> 0
         THEN ROUND((COALESCE(sp.now_jul_qty, 0) - sp.last_jul_qty)::numeric / sp.last_jul_qty * 100, 2)
    END                                 AS var_jul_qty,

    -- === AUGUST ===
    COALESCE(sp.now_aug_rp, 0),
    COALESCE(sp.last_aug_rp, 0),
    CASE WHEN COALESCE(sp.last_aug_rp, 0) <> 0
         THEN ROUND((COALESCE(sp.now_aug_rp, 0) - sp.last_aug_rp) / sp.last_aug_rp * 100, 2)
    END                                 AS var_aug_rp,
    COALESCE(sp.now_aug_qty, 0),
    COALESCE(sp.last_aug_qty, 0),
    CASE WHEN COALESCE(sp.last_aug_qty, 0) <> 0
         THEN ROUND((COALESCE(sp.now_aug_qty, 0) - sp.last_aug_qty)::numeric / sp.last_aug_qty * 100, 2)
    END                                 AS var_aug_qty,

    -- === SEPTEMBER ===
    COALESCE(sp.now_sep_rp, 0),
    COALESCE(sp.last_sep_rp, 0),
    CASE WHEN COALESCE(sp.last_sep_rp, 0) <> 0
         THEN ROUND((COALESCE(sp.now_sep_rp, 0) - sp.last_sep_rp) / sp.last_sep_rp * 100, 2)
    END                                 AS var_sep_rp,
    COALESCE(sp.now_sep_qty, 0),
    COALESCE(sp.last_sep_qty, 0),
    CASE WHEN COALESCE(sp.last_sep_qty, 0) <> 0
         THEN ROUND((COALESCE(sp.now_sep_qty, 0) - sp.last_sep_qty)::numeric / sp.last_sep_qty * 100, 2)
    END                                 AS var_sep_qty,

    -- === OCTOBER ===
    COALESCE(sp.now_oct_rp, 0),
    COALESCE(sp.last_oct_rp, 0),
    CASE WHEN COALESCE(sp.last_oct_rp, 0) <> 0
         THEN ROUND((COALESCE(sp.now_oct_rp, 0) - sp.last_oct_rp) / sp.last_oct_rp * 100, 2)
    END                                 AS var_oct_rp,
    COALESCE(sp.now_oct_qty, 0),
    COALESCE(sp.last_oct_qty, 0),
    CASE WHEN COALESCE(sp.last_oct_qty, 0) <> 0
         THEN ROUND((COALESCE(sp.now_oct_qty, 0) - sp.last_oct_qty)::numeric / sp.last_oct_qty * 100, 2)
    END                                 AS var_oct_qty,

    -- === NOVEMBER ===
    COALESCE(sp.now_nov_rp, 0),
    COALESCE(sp.last_nov_rp, 0),
    CASE WHEN COALESCE(sp.last_nov_rp, 0) <> 0
         THEN ROUND((COALESCE(sp.now_nov_rp, 0) - sp.last_nov_rp) / sp.last_nov_rp * 100, 2)
    END                                 AS var_nov_rp,
    COALESCE(sp.now_nov_qty, 0),
    COALESCE(sp.last_nov_qty, 0),
    CASE WHEN COALESCE(sp.last_nov_qty, 0) <> 0
         THEN ROUND((COALESCE(sp.now_nov_qty, 0) - sp.last_nov_qty)::numeric / sp.last_nov_qty * 100, 2)
    END                                 AS var_nov_qty,

    -- === DECEMBER ===
    COALESCE(sp.now_dec_rp, 0),
    COALESCE(sp.last_dec_rp, 0),
    CASE WHEN COALESCE(sp.last_dec_rp, 0) <> 0
         THEN ROUND((COALESCE(sp.now_dec_rp, 0) - sp.last_dec_rp) / sp.last_dec_rp * 100, 2)
    END                                 AS var_dec_rp,
    COALESCE(sp.now_dec_qty, 0),
    COALESCE(sp.last_dec_qty, 0),
    CASE WHEN COALESCE(sp.last_dec_qty, 0) <> 0
         THEN ROUND((COALESCE(sp.now_dec_qty, 0) - sp.last_dec_qty)::numeric / sp.last_dec_qty * 100, 2)
    END                                 AS var_dec_qty,

    -- === YEAR TOTALS ===
    COALESCE(sp.current_year_rp, 0),
    COALESCE(sp.last_year_rp, 0),
    CASE WHEN COALESCE(sp.last_year_rp, 0) <> 0
         THEN ROUND((COALESCE(sp.current_year_rp, 0) - sp.last_year_rp) / sp.last_year_rp * 100, 2)
    END                                 AS var_year_rp,
    COALESCE(sp.current_year_qty, 0),
    COALESCE(sp.last_year_qty, 0),
    CASE WHEN COALESCE(sp.last_year_qty, 0) <> 0
         THEN ROUND((COALESCE(sp.current_year_qty, 0) - sp.last_year_qty)::numeric / sp.last_year_qty * 100, 2)
    END                                 AS var_year_qty,

    -- === SALES MIX ===
    CASE WHEN ts.total_current_rp > 0
         THEN ROUND(COALESCE(sp.current_year_rp, 0) / ts.total_current_rp * 100, 4)
    END                                 AS current_sales_mix,
    CASE WHEN ts.total_last_rp > 0
         THEN ROUND(COALESCE(sp.last_year_rp, 0) / ts.total_last_rp * 100, 4)
    END                                 AS last_sales_mix,

    -- === AVERAGE LAST 3 MONTHS ===
    COALESCE(rs.avg_last_3_months, 0)   AS avg_last_3_months,

    -- === WAREHOUSE STOCK ===
    COALESCE(st.wh_pusat, 0)            AS wh_pusat,
    COALESCE(st.wh_bali, 0)             AS wh_bali,
    COALESCE(st.wh_jkt, 0)              AS wh_jkt,
    COALESCE(st.wh_pusat, 0)
        + COALESCE(st.wh_bali, 0)
        + COALESCE(st.wh_jkt, 0)        AS wh_total,

    -- === CHANNEL STOCK ===
    COALESCE(st.stok_toko, 0)           AS stok_toko,
    COALESCE(st.stok_online, 0)         AS stok_online,
    COALESCE(st.stok_unlabel, 0)        AS stok_unlabel,

    -- === GLOBAL STOCK ===
    COALESCE(st.wh_pusat, 0)
        + COALESCE(st.wh_bali, 0)
        + COALESCE(st.wh_jkt, 0)
        + COALESCE(st.stok_toko, 0)
        + COALESCE(st.stok_online, 0)
        + COALESCE(st.stok_unlabel, 0)  AS stok_global,

    -- === TURNOVER (months of coverage) ===
    CASE WHEN COALESCE(rs.avg_last_3_months, 0) > 0
         THEN ROUND(
            (COALESCE(st.wh_pusat, 0) + COALESCE(st.wh_bali, 0) + COALESCE(st.wh_jkt, 0))::numeric
            / rs.avg_last_3_months, 2)
    END                                 AS to_wh,
    CASE WHEN COALESCE(rs.avg_last_3_months, 0) > 0
         THEN ROUND(
            (COALESCE(st.wh_pusat, 0) + COALESCE(st.wh_bali, 0) + COALESCE(st.wh_jkt, 0)
             + COALESCE(st.stok_toko, 0) + COALESCE(st.stok_online, 0) + COALESCE(st.stok_unlabel, 0))::numeric
            / rs.avg_last_3_months, 2)
    END                                 AS to_total,

    -- === METADATA ===
    NOW()                               AS updated_at

FROM articles a
CROSS JOIN params p
CROSS JOIN total_sales ts
LEFT JOIN sales_pivot sp  ON a.kode_mix = sp.kode_mix
LEFT JOIN recent_sales rs ON a.kode_mix = rs.kode_mix
LEFT JOIN stock_agg st    ON a.kode_mix = st.kode_mix
ORDER BY a.kode_mix;


-- =============================================================================
-- SECTION 3: INDEXES
-- =============================================================================

-- Primary key already created via SERIAL id column in DDL above

-- Unique constraint on kodemix (article-level grain)
CREATE UNIQUE INDEX idx_sku_portfolio_kodemix
    ON mart.sku_portfolio (kodemix);

-- Performance indexes for common query patterns
CREATE INDEX idx_sku_portfolio_gender_series
    ON mart.sku_portfolio (gender, series);

CREATE INDEX idx_sku_portfolio_tier
    ON mart.sku_portfolio (tier);

CREATE INDEX idx_sku_portfolio_tipe
    ON mart.sku_portfolio (tipe);

-- Composite for Merchandiser queries (gender + series + tier)
CREATE INDEX idx_sku_portfolio_merch
    ON mart.sku_portfolio (gender, series, tier);

-- Turnover-based queries (for PO/reorder decisions)
CREATE INDEX idx_sku_portfolio_to_wh
    ON mart.sku_portfolio (to_wh NULLS LAST);

CREATE INDEX idx_sku_portfolio_to_total
    ON mart.sku_portfolio (to_total NULLS LAST);

-- Sales mix ranking
CREATE INDEX idx_sku_portfolio_sales_mix
    ON mart.sku_portfolio (current_sales_mix DESC NULLS LAST);


-- =============================================================================
-- SECTION 4: VALIDATION QUERIES
-- =============================================================================

-- 4.1: No duplicates on kodemix (must return 0)
SELECT 'VALIDATION 4.1: Duplicate kodemix check' AS test,
       COUNT(*) AS duplicate_count
FROM (
    SELECT kodemix, COUNT(*) AS cnt
    FROM mart.sku_portfolio
    GROUP BY kodemix
    HAVING COUNT(*) > 1
) dup;

-- 4.2: No duplicates on (kodemix, gender, series, color, tipe, tier) (must return 0)
SELECT 'VALIDATION 4.2: Composite key duplicate check' AS test,
       COUNT(*) AS duplicate_count
FROM (
    SELECT kodemix, gender, series, color, tipe, tier, COUNT(*) AS cnt
    FROM mart.sku_portfolio
    GROUP BY kodemix, gender, series, color, tipe, tier
    HAVING COUNT(*) > 1
) dup;

-- 4.3: Year auto-detection working correctly
SELECT 'VALIDATION 4.3: Year labels' AS test,
       current_year_label,
       last_year_label,
       EXTRACT(YEAR FROM CURRENT_DATE)::text AS expected_current,
       (EXTRACT(YEAR FROM CURRENT_DATE) - 1)::text AS expected_last,
       CASE WHEN current_year_label = EXTRACT(YEAR FROM CURRENT_DATE)::text
             AND last_year_label = (EXTRACT(YEAR FROM CURRENT_DATE) - 1)::text
            THEN 'PASS' ELSE 'FAIL'
       END AS result
FROM mart.sku_portfolio
LIMIT 1;

-- 4.4: Stock totals consistency
-- wh_total must equal wh_pusat + wh_bali + wh_jkt
-- stok_global must equal wh_total + stok_toko + stok_online + stok_unlabel
SELECT 'VALIDATION 4.4: Stock totals consistency' AS test,
       COUNT(*) FILTER (WHERE wh_total <> wh_pusat + wh_bali + wh_jkt) AS wh_total_mismatches,
       COUNT(*) FILTER (WHERE stok_global <> wh_total + stok_toko + stok_online + stok_unlabel) AS global_mismatches
FROM mart.sku_portfolio;

-- 4.5: Sales exclude intercompany (compare totals)
-- Portfolio current_year_qty should match sales_with_product filtered total
SELECT 'VALIDATION 4.5: Intercompany exclusion check' AS test,
       portfolio_qty,
       source_qty,
       ABS(portfolio_qty - source_qty) AS diff,
       CASE WHEN ABS(portfolio_qty - source_qty) <= 1 THEN 'PASS' ELSE 'INVESTIGATE' END AS result
FROM (
    SELECT SUM(current_year_qty) AS portfolio_qty
    FROM mart.sku_portfolio
) portfolio_totals
CROSS JOIN (
    SELECT SUM(quantity)::bigint AS source_qty
    FROM core.sales_with_product
    WHERE is_intercompany = FALSE
      AND kode_mix IS NOT NULL
      AND UPPER(COALESCE(article, '')) NOT LIKE '%SHOPPING BAG%'
      AND UPPER(COALESCE(article, '')) NOT LIKE '%HANGER%'
      AND UPPER(COALESCE(article, '')) NOT LIKE '%PAPER BAG%'
      AND UPPER(COALESCE(article, '')) NOT LIKE '%THERMAL%'
      AND UPPER(COALESCE(article, '')) NOT LIKE '%BOX LUCA%'
      AND EXTRACT(YEAR FROM transaction_date) = EXTRACT(YEAR FROM CURRENT_DATE)
) source_totals;

-- 4.6: Stock totals match source (stok_global vs stock_with_product)
SELECT 'VALIDATION 4.6: Stock total vs source' AS test,
       portfolio_stock,
       source_stock,
       ABS(portfolio_stock - source_stock) AS diff,
       CASE WHEN ABS(portfolio_stock - source_stock) <= 10 THEN 'PASS' ELSE 'INVESTIGATE' END AS result
FROM (
    SELECT SUM(stok_global) AS portfolio_stock
    FROM mart.sku_portfolio
) p
CROSS JOIN (
    SELECT SUM(quantity)::bigint AS source_stock
    FROM core.stock_with_product
    WHERE kode_mix IS NOT NULL
) s;

-- 4.7: Row count sanity check (should be ~598 articles based on portal.kodemix)
SELECT 'VALIDATION 4.7: Row count' AS test,
       COUNT(*) AS portfolio_rows,
       (SELECT COUNT(DISTINCT kode_mix) FROM portal.kodemix WHERE kode_mix IS NOT NULL) AS kodemix_articles,
       CASE WHEN COUNT(*) = (SELECT COUNT(DISTINCT kode_mix) FROM portal.kodemix WHERE kode_mix IS NOT NULL)
            THEN 'PASS' ELSE 'INVESTIGATE'
       END AS result
FROM mart.sku_portfolio;

-- 4.8: Turnover calculation spot check (sample 5 articles)
SELECT 'VALIDATION 4.8: Turnover spot check' AS test,
       kodemix, avg_last_3_months, wh_total, stok_global,
       to_wh,
       CASE WHEN avg_last_3_months > 0
            THEN ROUND(wh_total::numeric / avg_last_3_months, 2) END AS expected_to_wh,
       to_total,
       CASE WHEN avg_last_3_months > 0
            THEN ROUND(stok_global::numeric / avg_last_3_months, 2) END AS expected_to_total
FROM mart.sku_portfolio
WHERE avg_last_3_months > 0
ORDER BY current_year_qty DESC
LIMIT 5;

-- 4.9: Variance calculation spot check
SELECT 'VALIDATION 4.9: Variance spot check' AS test,
       kodemix,
       now_jan_rp, last_jan_rp, var_jan_rp,
       CASE WHEN last_jan_rp <> 0
            THEN ROUND((now_jan_rp - last_jan_rp) / last_jan_rp * 100, 2) END AS expected_var_jan_rp,
       now_jan_qty, last_jan_qty, var_jan_qty,
       CASE WHEN last_jan_qty <> 0
            THEN ROUND((now_jan_qty - last_jan_qty)::numeric / last_jan_qty * 100, 2) END AS expected_var_jan_qty
FROM mart.sku_portfolio
WHERE last_jan_rp > 0
LIMIT 5;


-- =============================================================================
-- SECTION 5: REFRESH SCRIPT (for cron scheduling)
-- =============================================================================
-- To refresh, run sections 2 (TRUNCATE + INSERT) only.
-- The DDL (section 1) and indexes (section 3) are one-time setup.
--
-- Suggested cron schedule: daily at 06:00 WIB (after ETL completes at 05:00)
--
-- Example cron entry (use environment variable from .env or .pgpass for password):
--   0 6 * * * PGPASSWORD="$PGPASSWORD" psql -h localhost -U openclaw_app -d openclaw_ops \
--     -f /opt/openclaw/scripts/refresh_sku_portfolio.sql >> /opt/openclaw/logs/sku_portfolio.log 2>&1
--
-- The refresh script would contain only the TRUNCATE + INSERT from section 2.


-- =============================================================================
-- SECTION 6: FUTURE PO COLUMNS (placeholder documentation)
-- =============================================================================
-- When raw.po table is ready, add PO columns via:
--
-- ALTER TABLE mart.sku_portfolio ADD COLUMN po_ongoing INTEGER DEFAULT 0;
-- ALTER TABLE mart.sku_portfolio ADD COLUMN to_plus_po NUMERIC(10,2);
--
-- Then update the INSERT query to include:
--   po_ongoing = SUM of open PO qty for this kode_mix
--   to_plus_po = (stok_global + po_ongoing) / NULLIF(avg_last_3_months, 0)
--
-- REMINDER: Ingatkan Wayan untuk implement raw.po table dari Accurate API
