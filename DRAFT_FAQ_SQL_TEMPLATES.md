# DRAFT: FAQ SQL Templates for Zuma Data Ops

> **Purpose:** Quick-reference SQL templates for common business questions
> **Target users:** Non-technical team members, BI analysts, reporting
> **Status:** DRAFT — review before adding to SKILL.md

---

## FAQ SQL Templates

### 1. Stock Queries (Latest Snapshot Only)

Stock queries always use `core.stock_with_product` with latest snapshot. No date filter needed — snapshot is auto-refreshed daily.

#### 1.1 Stock by Gender (Nasional)

```sql
-- National-level stock breakdown by gender
SELECT
    gender,
    COUNT(DISTINCT kode_mix) AS unique_articles,
    SUM(quantity) AS total_pairs,
    ROUND(SUM(quantity * unit_price), 0) AS total_stock_value
FROM core.stock_with_product
WHERE gender IS NOT NULL
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
  AND UPPER(article) NOT LIKE '%HANGER%'
  AND UPPER(article) NOT LIKE '%PAPER BAG%'
  AND UPPER(article) NOT LIKE '%THERMAL%'
  AND UPPER(article) NOT LIKE '%BOX LUCA%'
GROUP BY gender
ORDER BY total_pairs DESC;
```

#### 1.2 Stock by Gender (Branch-Level)

```sql
-- Stock breakdown by gender per branch
SELECT
    gudang_branch AS branch,
    gender,
    COUNT(DISTINCT kode_mix) AS unique_articles,
    SUM(quantity) AS total_pairs
FROM core.stock_with_product
WHERE gender IS NOT NULL
  AND gudang_branch IS NOT NULL
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
  AND UPPER(article) NOT LIKE '%HANGER%'
GROUP BY gudang_branch, gender
ORDER BY branch, total_pairs DESC;
```

#### 1.3 Stock by Gender (Area-Level)

```sql
-- Stock breakdown by gender per area
SELECT
    gudang_area AS area,
    gender,
    SUM(quantity) AS total_pairs
FROM core.stock_with_product
WHERE gender IS NOT NULL
  AND gudang_area IS NOT NULL
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
GROUP BY gudang_area, gender
ORDER BY area, total_pairs DESC;
```

#### 1.4 Stock by Gender (Store-Level)

```sql
-- Stock breakdown by gender per store
SELECT
    nama_gudang AS store,
    gudang_branch AS branch,
    gudang_area AS area,
    gender,
    SUM(quantity) AS total_pairs
FROM core.stock_with_product
WHERE gender IS NOT NULL
  AND nama_gudang IS NOT NULL
  AND gudang_category = 'RETAIL'  -- Exclude warehouses
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
GROUP BY nama_gudang, gudang_branch, gudang_area, gender
ORDER BY branch, area, store, total_pairs DESC;
```

---

#### 1.5 Stock by Series (Nasional)

```sql
-- National-level stock breakdown by series
SELECT
    series,
    COUNT(DISTINCT kode_mix) AS unique_articles,
    SUM(quantity) AS total_pairs,
    ROUND(SUM(quantity * unit_price), 0) AS total_stock_value
FROM core.stock_with_product
WHERE series IS NOT NULL
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
  AND UPPER(article) NOT LIKE '%HANGER%'
GROUP BY series
ORDER BY total_pairs DESC;
```

#### 1.6 Stock by Series (Branch-Level)

```sql
SELECT
    gudang_branch AS branch,
    series,
    SUM(quantity) AS total_pairs
FROM core.stock_with_product
WHERE series IS NOT NULL
  AND gudang_branch IS NOT NULL
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
GROUP BY gudang_branch, series
ORDER BY branch, total_pairs DESC;
```

#### 1.7 Stock by Series (Area-Level)

```sql
SELECT
    gudang_area AS area,
    series,
    SUM(quantity) AS total_pairs
FROM core.stock_with_product
WHERE series IS NOT NULL
  AND gudang_area IS NOT NULL
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
GROUP BY gudang_area, series
ORDER BY area, total_pairs DESC;
```

#### 1.8 Stock by Series (Store-Level)

```sql
SELECT
    nama_gudang AS store,
    gudang_branch AS branch,
    series,
    SUM(quantity) AS total_pairs
FROM core.stock_with_product
WHERE series IS NOT NULL
  AND nama_gudang IS NOT NULL
  AND gudang_category = 'RETAIL'
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
GROUP BY nama_gudang, gudang_branch, series
ORDER BY branch, store, total_pairs DESC;
```

---

#### 1.9 Stock by Article (Nasional)

```sql
-- National-level stock breakdown by article (top 50)
SELECT
    kode_mix,
    article,
    series,
    gender,
    tier,
    SUM(quantity) AS total_pairs,
    ROUND(SUM(quantity * unit_price), 0) AS total_stock_value
FROM core.stock_with_product
WHERE kode_mix IS NOT NULL
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
  AND UPPER(article) NOT LIKE '%HANGER%'
GROUP BY kode_mix, article, series, gender, tier
ORDER BY total_pairs DESC
LIMIT 50;
```

#### 1.10 Stock by Article (Branch-Level)

```sql
SELECT
    gudang_branch AS branch,
    kode_mix,
    article,
    SUM(quantity) AS total_pairs
FROM core.stock_with_product
WHERE kode_mix IS NOT NULL
  AND gudang_branch IS NOT NULL
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
GROUP BY gudang_branch, kode_mix, article
ORDER BY branch, total_pairs DESC;
```

#### 1.11 Stock by Article (Area-Level)

```sql
SELECT
    gudang_area AS area,
    kode_mix,
    article,
    SUM(quantity) AS total_pairs
FROM core.stock_with_product
WHERE kode_mix IS NOT NULL
  AND gudang_area IS NOT NULL
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
GROUP BY gudang_area, kode_mix, article
ORDER BY area, total_pairs DESC;
```

#### 1.12 Stock by Article (Store-Level)

```sql
-- Stock by article for a specific store
SELECT
    kode_mix,
    article,
    series,
    gender,
    SUM(quantity) AS total_pairs
FROM core.stock_with_product
WHERE nama_gudang = 'Zuma Royal Plaza'  -- Replace with target store
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
GROUP BY kode_mix, article, series, gender
ORDER BY total_pairs DESC;
```

---

### 2. Sales Queries (Period-Based)

Sales queries ALWAYS need a date filter. Default to last 3 months if period unspecified.

**Auto-applied filters (already in core view):**
- `is_intercompany = FALSE` (excludes fake inter-entity transactions)
- Non-product items excluded (SHOPPING BAG, HANGER, etc.)

#### 2.1 Sales by Gender (Nasional × Periode)

```sql
-- National sales by gender for a period
SELECT
    gender,
    COUNT(DISTINCT kode_mix) AS unique_articles,
    SUM(quantity) AS total_pairs,
    SUM(total_amount) AS total_revenue,
    ROUND(AVG(unit_price), 0) AS avg_selling_price
FROM core.sales_with_product
WHERE gender IS NOT NULL
  AND transaction_date >= CURRENT_DATE - INTERVAL '3 months'
  AND is_intercompany = FALSE
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
  AND UPPER(article) NOT LIKE '%HANGER%'
GROUP BY gender
ORDER BY total_pairs DESC;
```

#### 2.2 Sales by Gender (Branch-Level × Periode)

```sql
SELECT
    branch,
    gender,
    SUM(quantity) AS total_pairs,
    SUM(total_amount) AS total_revenue
FROM core.sales_with_product
WHERE gender IS NOT NULL
  AND branch IS NOT NULL
  AND transaction_date >= DATE_TRUNC('month', CURRENT_DATE)  -- Current month
  AND is_intercompany = FALSE
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
GROUP BY branch, gender
ORDER BY branch, total_pairs DESC;
```

#### 2.3 Sales by Gender (Area-Level × Periode)

```sql
SELECT
    area,
    gender,
    SUM(quantity) AS total_pairs,
    SUM(total_amount) AS total_revenue
FROM core.sales_with_product
WHERE gender IS NOT NULL
  AND area IS NOT NULL
  AND transaction_date BETWEEN '2026-01-01' AND '2026-01-31'  -- Specific month
  AND is_intercompany = FALSE
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
GROUP BY area, gender
ORDER BY area, total_pairs DESC;
```

#### 2.4 Sales by Gender (Store-Level × Periode)

```sql
-- Sales by gender per store (last 30 days)
SELECT
    matched_store_name AS store,
    branch,
    gender,
    SUM(quantity) AS total_pairs
FROM core.sales_with_product
WHERE gender IS NOT NULL
  AND matched_store_name IS NOT NULL
  AND transaction_date >= CURRENT_DATE - INTERVAL '30 days'
  AND is_intercompany = FALSE
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
  -- Auto-exclude Wholesale/Pusat/Konsinyasi stores
  AND UPPER(matched_store_name) NOT LIKE '%WHOLESALE%'
  AND UPPER(matched_store_name) NOT LIKE '%PUSAT%'
  AND UPPER(matched_store_name) NOT LIKE '%KONSINYASI%'
GROUP BY matched_store_name, branch, gender
ORDER BY branch, store, total_pairs DESC;
```

---

#### 2.5 Sales by Series (Nasional × Periode)

```sql
SELECT
    series,
    SUM(quantity) AS total_pairs,
    SUM(total_amount) AS total_revenue,
    COUNT(DISTINCT kode_mix) AS unique_articles
FROM core.sales_with_product
WHERE series IS NOT NULL
  AND transaction_date >= CURRENT_DATE - INTERVAL '3 months'
  AND is_intercompany = FALSE
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
GROUP BY series
ORDER BY total_pairs DESC;
```

#### 2.6 Sales by Series (Branch-Level × Periode)

```sql
SELECT
    branch,
    series,
    SUM(quantity) AS total_pairs
FROM core.sales_with_product
WHERE series IS NOT NULL
  AND branch IS NOT NULL
  AND transaction_date >= DATE_TRUNC('month', CURRENT_DATE)
  AND is_intercompany = FALSE
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
GROUP BY branch, series
ORDER BY branch, total_pairs DESC;
```

#### 2.7 Sales by Series (Area-Level × Periode)

```sql
SELECT
    area,
    series,
    SUM(quantity) AS total_pairs
FROM core.sales_with_product
WHERE series IS NOT NULL
  AND area IS NOT NULL
  AND transaction_date >= CURRENT_DATE - INTERVAL '1 month'
  AND is_intercompany = FALSE
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
GROUP BY area, series
ORDER BY area, total_pairs DESC;
```

#### 2.8 Sales by Series (Store-Level × Periode)

```sql
SELECT
    matched_store_name AS store,
    series,
    SUM(quantity) AS total_pairs
FROM core.sales_with_product
WHERE series IS NOT NULL
  AND matched_store_name IS NOT NULL
  AND transaction_date >= CURRENT_DATE - INTERVAL '30 days'
  AND is_intercompany = FALSE
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
  AND UPPER(matched_store_name) NOT LIKE '%WHOLESALE%'
  AND UPPER(matched_store_name) NOT LIKE '%PUSAT%'
  AND UPPER(matched_store_name) NOT LIKE '%KONSINYASI%'
GROUP BY matched_store_name, series
ORDER BY store, total_pairs DESC;
```

---

#### 2.9 Sales by Article (Nasional × Periode — Top 50)

```sql
SELECT
    kode_mix,
    article,
    series,
    gender,
    tier,
    SUM(quantity) AS total_pairs,
    SUM(total_amount) AS total_revenue,
    ROUND(AVG(unit_price), 0) AS avg_selling_price
FROM core.sales_with_product
WHERE kode_mix IS NOT NULL
  AND transaction_date >= CURRENT_DATE - INTERVAL '3 months'
  AND is_intercompany = FALSE
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
  AND UPPER(article) NOT LIKE '%HANGER%'
GROUP BY kode_mix, article, series, gender, tier
ORDER BY total_pairs DESC
LIMIT 50;
```

#### 2.10 Sales by Article (Branch-Level × Periode)

```sql
SELECT
    branch,
    kode_mix,
    article,
    SUM(quantity) AS total_pairs,
    SUM(total_amount) AS total_revenue
FROM core.sales_with_product
WHERE kode_mix IS NOT NULL
  AND branch IS NOT NULL
  AND transaction_date >= DATE_TRUNC('month', CURRENT_DATE)
  AND is_intercompany = FALSE
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
GROUP BY branch, kode_mix, article
ORDER BY branch, total_pairs DESC;
```

#### 2.11 Sales by Article (Area-Level × Periode)

```sql
SELECT
    area,
    kode_mix,
    article,
    SUM(quantity) AS total_pairs
FROM core.sales_with_product
WHERE kode_mix IS NOT NULL
  AND area IS NOT NULL
  AND transaction_date >= CURRENT_DATE - INTERVAL '1 month'
  AND is_intercompany = FALSE
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
GROUP BY area, kode_mix, article
ORDER BY area, total_pairs DESC;
```

#### 2.12 Sales by Article (Store-Level × Periode)

```sql
-- Sales by article for a specific store
SELECT
    kode_mix,
    article,
    series,
    gender,
    SUM(quantity) AS total_pairs,
    SUM(total_amount) AS total_revenue
FROM core.sales_with_product
WHERE matched_store_name = 'Zuma Royal Plaza'  -- Replace with target store
  AND transaction_date >= CURRENT_DATE - INTERVAL '3 months'
  AND is_intercompany = FALSE
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
GROUP BY kode_mix, article, series, gender
ORDER BY total_pairs DESC;
```

---

### 3. Auto-Applied Rules (Built Into Templates)

**Every query above already applies these filters:**

#### 3.1 Intercompany Exclusion

```sql
WHERE is_intercompany = FALSE
```

This filters out ~284K pairs (~Rp 15.2Bn) of fake sales between Zuma entities (DDD ↔ MBB ↔ UBB ↔ LJBB).

**Matched customers (auto-excluded):**
- `CV MAKMUR BESAR BERSAMA` (DDD → MBB)
- `CV. UNTUNG BESAR BERSAMA` (DDD → UBB)
- `CV Lancar Jaya Besar Bersama` (DDD → LJBB)
- `PT Dream Dare Discover` (MBB → DDD)
- `CV. Makmur Besar Bersama` (UBB → MBB)

#### 3.2 Store Category Exclusion (Store-Level Queries Only)

```sql
WHERE UPPER(matched_store_name) NOT LIKE '%WHOLESALE%'
  AND UPPER(matched_store_name) NOT LIKE '%PUSAT%'
  AND UPPER(matched_store_name) NOT LIKE '%KONSINYASI%'
```

**When to INCLUDE these:** Only when user explicitly asks for "wholesale sales", "sales ke konsinyasi", etc.

**Examples of excluded stores:**
- Warehouse Pusat (Jatim/Jakarta/Sumatra) — distribution center, not retail
- Konsinyasi Jatim / Jakarta / Bali — non-retail, different channel
- Wholesale Jatim / Bali / Lombok — wholesale channel, not comparable to retail

#### 3.3 Non-Product Item Exclusion

```sql
WHERE UPPER(article) NOT LIKE '%SHOPPING BAG%'
  AND UPPER(article) NOT LIKE '%HANGER%'
  AND UPPER(article) NOT LIKE '%PAPER BAG%'
  AND UPPER(article) NOT LIKE '%THERMAL%'
  AND UPPER(article) NOT LIKE '%BOX LUCA%'
```

These are packaging/accessory items that inflate article counts and skew product rankings. Always excluded from product-level analysis.

---

### 4. Period Filter Patterns

**Common date filters:**

| Period | SQL |
|--------|-----|
| Last 30 days | `transaction_date >= CURRENT_DATE - INTERVAL '30 days'` |
| Last 3 months | `transaction_date >= CURRENT_DATE - INTERVAL '3 months'` |
| Current month (MTD) | `transaction_date >= DATE_TRUNC('month', CURRENT_DATE)` |
| Specific month | `transaction_date BETWEEN '2026-01-01' AND '2026-01-31'` |
| Last month (full) | `transaction_date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month') AND transaction_date < DATE_TRUNC('month', CURRENT_DATE)` |
| Year-to-date | `transaction_date >= DATE_TRUNC('year', CURRENT_DATE)` |
| Last 12 months | `transaction_date >= CURRENT_DATE - INTERVAL '12 months'` |

---

### 5. How to Use These Templates

1. **Identify the question type:**
   - Stock = latest snapshot (no date filter needed)
   - Sales = period-based (ALWAYS needs date filter)

2. **Choose the right granularity:**
   - Gender → 1.1-1.4 or 2.1-2.4
   - Series → 1.5-1.8 or 2.5-2.8
   - Article → 1.9-1.12 or 2.9-2.12

3. **Choose the right geography:**
   - Nasional → nationwide aggregate
   - Branch → by branch (Jatim, Jakarta, Bali, etc.)
   - Area → by area (Jatim, Bali 1, Bali 2, Lombok, etc.)
   - Store → individual store level

4. **Adjust the period filter (sales only):**
   - Replace `CURRENT_DATE - INTERVAL '3 months'` with your target period
   - Use Section 4 patterns as reference

5. **Copy, paste, run** — all auto-applied rules already baked in!

---

**Status:** DRAFT
**Next step:** Review → Approve → Add to `zuma-data-ops/SKILL.md` Section 15 (after current Section 14)
