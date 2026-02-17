# Product Analysis — Unified Template

**Purpose:** Comprehensive guide for answering ALL product/SKU queries at Zuma Indonesia
**Combines:** SQL query framework + WhatsApp formatting + mart.sku_portfolio usage
**Last Updated:** 2026-02-15

---

## 1. Decision Tree: Which Data Source?

```
User asks about product performance?
│
├─ Need historical monthly breakdown? (Jan vs Feb vs Mar...)
│  └─ ✅ mart.sku_portfolio (has all 12 months pre-computed)
│
├─ Need comprehensive metrics? (sales + stock + turnover in one query)
│  └─ ✅ mart.sku_portfolio (all-in-one table, 101 columns)
│
├─ Need real-time/custom time period? (last 7 days, specific date range)
│  └─ ❌ core.sales_with_product (flexible date filtering)
│
├─ Need store-level breakdown? (per-store sales detail)
│  └─ ❌ core.sales_with_product (has matched_store_name)
│
└─ Need invoice/transaction detail? (COGS, vendor price, invoice number)
   └─ ❌ core.sales_with_product (has all raw columns)
```

**DEFAULT:** Use `mart.sku_portfolio` for 90% of product analysis questions.

---

## 1.1. Size Breakdown? Use `mart.sku_portfolio_size` ⚠️ CRITICAL QUERY RULE

**When to use:**
- User explicitly asks for **size breakdown** (e.g., "per size", "size 42 vs 40", "breakdown by size")
- Need **SKU-level granularity** (kode_besar grain)

**Table:** `mart.sku_portfolio_size`
- **Grain:** kode_besar (SKU with size + version, e.g., M1SPV201Z42)
- **Rows:** 5,220 (all versions × sizes)
- **Columns:** 107 (11 ID/Base + 83 Sales + 13 Stock)

**⚠️ CRITICAL RULE (2026-02-17):**

**ALWAYS aggregate by `kodemix` or `kode_mix_size` — NEVER filter by single `kode_besar`!**

**Why:**
- One article has **multiple kode_besar versions** (M1SPV201, M1SP01, M1SPV101, SJ1A)
- Kode lama → kode baru evolution (same product, different codes over time)
- `kode_besar` = PRIMARY KEY for data integrity (prevent duplicates)
- **Business analysis** = SUM across ALL versions (ignore kode version differences)

**Wrong vs Right Query:**
```sql
-- ❌ WRONG (incomplete — only 1 version):
SELECT size, current_year_qty
FROM mart.sku_portfolio_size
WHERE kode_besar = 'M1SPV201Z42';

-- ✅ CORRECT (complete — all versions):
SELECT 
    size,
    SUM(current_year_qty) AS total_qty,
    SUM(current_year_rp) AS total_rp,
    SUM(stok_global) AS total_stock
FROM mart.sku_portfolio_size
WHERE kodemix = 'M1SP0PV201'
GROUP BY size
ORDER BY total_qty DESC;
```

**Decision:**
- Need **size breakdown** → `mart.sku_portfolio_size` + GROUP BY kodemix, size
- Article-level only (no size) → `mart.sku_portfolio`

---

## 2. Query Framework (WHAT/WHERE/WHEN Pattern)

Every Zuma data question follows:

```
"Berapa [METRIC] dari [WHAT] di [WHERE] selama [WHEN]?"
```

### Step 1 — Identify METRIC

| User Says | mart.sku_portfolio Column | core View Equivalent |
|-----------|--------------------------|---------------------|
| "penjualan / sales 2026" | `current_year_qty` | `SUM(quantity) WHERE EXTRACT(YEAR FROM transaction_date) = 2026` |
| "penjualan / sales 2025" | `last_year_qty` | `SUM(quantity) WHERE EXTRACT(YEAR FROM transaction_date) = 2025` |
| "YoY growth" | `var_year_qty` (%) | Manual calc: `(cy - ly) / ly * 100` |
| "sales mix / kontribusi %" | `current_sales_mix` | `(article_sales / total_sales) * 100` |
| "rata-rata 3 bulan" | `avg_last_3_months` | Custom CTE with tier-aware logic |
| "stock sekarang" | `stok_global` | `SUM(quantity) FROM core.stock_with_product` |
| "stock gudang pusat" | `wh_pusat` | `SUM(quantity) WHERE nama_gudang LIKE '%pusat%'` |
| "stock toko" | `stok_toko` | `SUM(quantity) WHERE gudang_category = 'RETAIL'` |
| "turnover / TO" | `to_total` (months) | `stock / avg_monthly_sales` |

### Step 2 — Identify WHAT (Product Granularity)

| User Says | mart.sku_portfolio | core View GROUP BY |
|-----------|-------------------|-------------------|
| Specific article ("Jet Black") | `WHERE kodemix = 'SJ1ACAV201'` OR `WHERE UPPER(series || ' ' || color) LIKE '%JET BLACK%'` | `kode_mix, article` |
| Series ("Classic", "Stripe") | `WHERE series = 'Classic'` | `series` |
| Gender ("Men", "Ladies") | `WHERE gender = 'MEN'` | `gender` |
| Gender + Tipe ("Men Jepit") | `WHERE gender = 'MEN' AND tipe = 'Jepit'` | `gender, tipe` |
| Tier ("T1 articles") | `WHERE tier = '1'` | `tier` |
| All products | _(no filter)_ | _(no grouping)_ |

### Step 3 — Identify WHERE (Geography)

**⚠️ mart.sku_portfolio has NO store breakdown** — it's NATIONAL aggregate only.

| User Says | mart.sku_portfolio | core View Filter |
|-----------|-------------------|------------------|
| **National** (all stores) | ✅ Use as-is | _(no geo filter)_ |
| Specific store ("Royal Plaza") | ❌ **Cannot do** — use `core.sales_with_product` | `matched_store_name ILIKE '%royal plaza%'` |
| Area ("Jatim", "Bali 1") | ❌ **Cannot do** — use `core` | `area = 'Jatim'` |
| Branch ("Bali", "Jakarta") | ❌ **Cannot do** — use `core` | `branch = 'Bali'` |

**Rule:** If user asks for **store/area/branch breakdown** → SKIP mart.sku_portfolio, go to core views.

### Step 4 — Identify WHEN (Time Period)

**⚠️ mart.sku_portfolio is a SNAPSHOT** — current year vs last year only.

| User Says | mart.sku_portfolio | core View Filter |
|-----------|-------------------|------------------|
| "2026 vs 2025" | ✅ `current_year_*` vs `last_year_*` | `EXTRACT(YEAR FROM transaction_date) IN (2025, 2026)` |
| "Jan 2026 vs Jan 2025" | ✅ `now_jan_qty` vs `last_jan_qty` | `EXTRACT(MONTH ...) = 1 AND EXTRACT(YEAR ...)` |
| "Last 3 months" | ❌ Use `avg_last_3_months` (aggregate only) | `transaction_date >= CURRENT_DATE - INTERVAL '3 months'` |
| "Last 7 days" | ❌ **Cannot do** — use `core` | `transaction_date >= CURRENT_DATE - INTERVAL '7 days'` |
| "Specific date range" | ❌ **Cannot do** — use `core` | `transaction_date BETWEEN '2025-01-01' AND '2025-03-31'` |

**Rule:** If user asks for **custom date range or recent period** → use core views.

---

## 3. SQL Templates

### Template A: mart.sku_portfolio (Primary — Use This First)

**When to use:**
- ✅ National product performance (no store breakdown)
- ✅ Year-over-year comparison (2026 vs 2025)
- ✅ Month-by-month comparison (Jan vs Feb vs Mar...)
- ✅ Stock + Sales + Turnover in one query
- ✅ Top N analysis (best sellers, worst performers)

**Basic Query:**
```sql
-- ⚠️ CRITICAL: ALWAYS include full stock breakdown columns
-- User needs to verify: stok_global = wh_total + stok_toko + stok_online + stok_unlabel
-- Missing columns causes confusion (e.g., negative WH not visible → looks impossible)

SELECT 
  kodemix,
  gender,
  series,
  color,
  tier,
  
  -- Sales (Current Year)
  current_year_qty AS cy_qty,
  current_year_rp AS cy_revenue,
  
  -- Sales (Last Year)
  last_year_qty AS ly_qty,
  last_year_rp AS ly_revenue,
  
  -- YoY Growth
  var_year_qty AS yoy_growth_pct,
  
  -- Sales Mix
  ROUND(current_sales_mix, 2) AS sales_mix_pct,
  
  -- Recent Performance
  avg_last_3_months AS avg_3mo_qty,
  
  -- Stock (ALWAYS show full breakdown for verification)
  stok_global AS total_stock,
  wh_pusat AS wh_surabaya,
  wh_bali AS wh_bali,
  wh_jkt AS wh_jakarta,
  wh_total AS wh_total,
  stok_toko AS store_stock,
  stok_online AS online_stock,
  stok_unlabel AS unlabel_stock,
  
  -- Turnover
  ROUND(to_total::numeric, 2) AS turnover_months,
  ROUND(to_wh::numeric, 2) AS turnover_wh_months
  
FROM mart.sku_portfolio
WHERE 1=1
  -- Add filters based on WHAT/WHERE/WHEN framework
  -- AND series = 'Classic'
  -- AND gender = 'MEN'
  -- AND tier = '1'
  -- AND current_year_qty > 0  (exclude zero sales if needed)
ORDER BY current_year_qty DESC
LIMIT 10;
```

**Monthly Breakdown Example:**
```sql
SELECT 
  kodemix,
  series,
  color,
  
  -- Jan
  now_jan_qty AS jan_2026,
  last_jan_qty AS jan_2025,
  var_jan_qty AS jan_yoy_pct,
  
  -- Feb
  now_feb_qty AS feb_2026,
  last_feb_qty AS feb_2025,
  var_feb_qty AS feb_yoy_pct,
  
  -- Mar
  now_mar_qty AS mar_2026,
  last_mar_qty AS mar_2025,
  var_mar_qty AS mar_yoy_pct
  
FROM mart.sku_portfolio
WHERE series = 'Classic'
  AND current_year_qty > 0
ORDER BY current_year_qty DESC
LIMIT 10;
```

**Fast Movers (Stockout Risk):**
```sql
SELECT 
  kodemix,
  series,
  color,
  avg_last_3_months,
  stok_global,
  ROUND(to_total::numeric, 2) AS turnover_months
FROM mart.sku_portfolio
WHERE to_total < 0.5  -- Less than 0.5 months coverage
  AND avg_last_3_months > 0
ORDER BY to_total ASC
LIMIT 20;
```

**Slow Movers (Overstock):**
```sql
SELECT 
  kodemix,
  series,
  color,
  avg_last_3_months,
  stok_global,
  ROUND(to_total::numeric, 2) AS turnover_months
FROM mart.sku_portfolio
WHERE to_total > 3  -- More than 3 months coverage
ORDER BY to_total DESC
LIMIT 20;
```

### Template B: core.sales_with_product (Fallback — When mart Can't Do It)

**When to use:**
- ❌ Need store/area/branch breakdown
- ❌ Need custom date range (last 7 days, specific quarter)
- ❌ Need transaction-level detail (invoice, vendor price, COGS)

**MANDATORY Filters (ALWAYS include):**
```sql
WHERE is_intercompany = FALSE                          -- Exclude fake inter-entity transfers
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'         -- Exclude non-product items
  AND UPPER(article) NOT LIKE '%HANGER%'
  AND UPPER(article) NOT LIKE '%PAPER BAG%'
  AND UPPER(article) NOT LIKE '%THERMAL%'
  AND UPPER(article) NOT LIKE '%BOX LUCA%'
```

**Basic Query:**
```sql
SELECT
  kode_mix,
  article,
  series,
  gender,
  tier,
  
  -- Sales Metrics
  SUM(quantity) AS total_pairs,
  SUM(total_amount) AS total_revenue,
  ROUND(SUM(total_amount) / NULLIF(SUM(quantity), 0), 0) AS avg_price_per_pair,
  
  -- Transaction Count
  COUNT(DISTINCT nomor_invoice) AS num_transactions,
  COUNT(DISTINCT matched_store_name) AS num_stores
  
FROM core.sales_with_product
WHERE is_intercompany = FALSE
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
  AND UPPER(article) NOT LIKE '%HANGER%'
  AND UPPER(article) NOT LIKE '%PAPER BAG%'
  AND UPPER(article) NOT LIKE '%THERMAL%'
  AND UPPER(article) NOT LIKE '%BOX LUCA%'
  
  -- Add WHAT/WHERE/WHEN filters here
  AND series = 'Classic'
  AND area = 'Jatim'
  AND transaction_date >= CURRENT_DATE - INTERVAL '3 months'
  
GROUP BY 1, 2, 3, 4, 5
ORDER BY total_pairs DESC
LIMIT 10;
```

**Per-Store Breakdown:**
```sql
SELECT
  matched_store_name AS store,
  branch,
  area,
  kode_mix,
  article,
  SUM(quantity) AS total_pairs,
  SUM(total_amount) AS total_revenue
FROM core.sales_with_product
WHERE is_intercompany = FALSE
  AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
  AND UPPER(article) NOT LIKE '%HANGER%'
  AND UPPER(article) NOT LIKE '%PAPER BAG%'
  AND UPPER(article) NOT LIKE '%THERMAL%'
  AND UPPER(article) NOT LIKE '%BOX LUCA%'
  AND series = 'Classic'
  AND transaction_date >= CURRENT_DATE - INTERVAL '1 month'
GROUP BY 1, 2, 3, 4, 5
ORDER BY branch, total_pairs DESC;
```

### Template C: core.stock_with_product (Stock-Only Queries)

**When to use:**
- Need current stock breakdown by warehouse/store
- Need specific warehouse stock (not just totals)

**⚠️ COLUMN DIFFERENCES vs sales_with_product:**
- Store name: `nama_gudang` (NOT `matched_store_name`)
- Branch: `gudang_branch` (NOT `branch`)
- Area: `gudang_area` (NOT `area`)
- Category: `gudang_category` (NOT `store_category`)

**Basic Query:**
```sql
SELECT
  kode_mix,
  article,
  series,
  gender,
  nama_gudang AS warehouse_or_store,
  gudang_branch AS branch,
  gudang_category AS category,
  SUM(quantity) AS total_pairs,
  SUM(quantity * unit_price) AS total_stock_value
FROM core.stock_with_product
WHERE UPPER(article) NOT LIKE '%SHOPPING BAG%'
  AND UPPER(article) NOT LIKE '%HANGER%'
  AND UPPER(article) NOT LIKE '%PAPER BAG%'
  AND UPPER(article) NOT LIKE '%THERMAL%'
  AND UPPER(article) NOT LIKE '%BOX LUCA%'
  
  -- Add filters
  AND series = 'Classic'
  AND nama_gudang ILIKE '%warehouse pusat%'
  
GROUP BY 1, 2, 3, 4, 5, 6, 7
ORDER BY total_pairs DESC;
```

---

## 4. Output Formatting (WhatsApp-Friendly)

### Format Decision Tree

```
How many articles in result?
│
├─ 1 article → **Detailed Block Format** (Section 4.1)
├─ 2-5 articles → **Detailed Block Format** (Section 4.1)
└─ 6+ articles → **Compact List Format** (Section 4.2)
```

### 4.1 Detailed Block Format (1-5 Articles)

**Structure:**
```
📊 HEADER (context)

🥇 #1 - KODEMIX
👤 Gender | 🎨 Series | Color | ⭐ Tier

📈 Sales Performance
• 2026: X,XXX pairs (X.X% share)
• 2025: X,XXX pairs
• YoY: ±X% [emoji]
• Avg 3mo: X,XXX pairs/month

📦 Stock & Turnover
• Total: X,XXX pairs
  - WH: X,XXX [flag if negative]
  - Toko: X,XXX
  - Online: X,XXX
• TO: X.XX months [🔥 or 🐌]

---

[repeat for #2, #3...]

🔍 KEY INSIGHTS
✅ Positives: ...
⚠️ Concerns: ...
🎯 Actions: ...
```

**Example:**
```
📊 TOP 3 CLASSIC SERIES (2026 YTD)

🔢 Data: mart.sku_portfolio
📅 Period: Jan-Feb 2026 vs 2025

---

🥇 #1 - SJ1ACAV201
👤 MEN | 🎨 CLASSIC | JET BLACK | ⭐ T1

📈 Sales Performance
• 2026: 2,221 pairs (2.18% share)
• 2025: 17,288 pairs
• YoY: -87% ⚠️ (down 15,067)
• Avg 3mo: 1,498 pairs/month

📦 Stock & Turnover
• Total: 2,775 pairs
  - WH: 478 pairs
  - Toko: 1,784 pairs
  - Online: 513 pairs
• TO: 1.85 months ✅

---

🥈 #2 - SJ2ACAV201
👤 LADIES | 🎨 CLASSIC | JET BLACK | ⭐ T1

📈 Sales Performance
• 2026: 1,460 pairs (1.54% share)
• 2025: 13,788 pairs
• YoY: -89% ⚠️ (down 12,328)
• Avg 3mo: 1,392 pairs/month

📦 Stock & Turnover
• Total: 1,045 pairs
  - WH: -99 ⚠️ (unlabel/reject)
  - Toko: 924 pairs
  - Online: 220 pairs
• TO: 0.75 months 🔥

---

🔍 KEY INSIGHTS

✅ Positives:
• Both T1 premium tier (high margin)
• Healthy TO 0.75-1.85mo (moving well)
• Strong 3-month avg (1,400+ pairs/mo)

⚠️ Concerns:
• Massive YoY drop -87% to -89%
  → Partial 2026 (Feb) vs full 2025
• Ladies JET BLACK negative WH stock
  → Check unlabel category (reject/transit)

🎯 Actions:
• Monitor Ladies JET BLACK (TO 0.75mo = fast)
• Restock if trend continues
• Review unlabel stock allocation
```

### 4.2 Compact List Format (6+ Articles)

**Structure:**
```
📊 HEADER

1️⃣ Article Name (Gender) — X,XXX pairs | ±X% YoY | X.XXmo TO [emoji]
2️⃣ Article Name (Gender) — X,XXX pairs | ±X% YoY | X.XXmo TO [emoji]
...

💡 Summary: Avg TO X.Xmo | X% avg YoY | All TX tier
```

**Example:**
```
📊 TOP 10 BEST SELLERS (2026 YTD)

1️⃣ STRIPE BLACK BLUE RED (M) — 3,223 | -87% | 0.21mo 🔥
2️⃣ CLASSIC JET BLACK (M) — 2,221 | -87% | 1.85mo
3️⃣ BLACKSERIES COSMIC GREY (M) — 1,734 | -84% | 1.88mo
4️⃣ CLASSIC JET BLACK (L) — 1,460 | -89% | 0.75mo
5️⃣ BLACKSERIES PEANUT (M) — 1,403 | -79% | 1.52mo
6️⃣ BLACKSERIES STONE BLUE (M) — 1,311 | -83% | 1.28mo
7️⃣ DALLAS JET BLACK (M) — 1,301 | -89% | 2.49mo
8️⃣ CLASSIC METALIC GINGER (L) — 1,184 | -87% | 1.29mo
9️⃣ BLACKSERIES BROWN STONE (M) — 1,175 | -67% | 2.69mo 🐌
🔟 CLASSIC NAVY GREY (M) — 992 | -85% | 0.94mo

💡 Avg TO: 1.5mo | All T1 tier | Top 10 = 16.5% total sales
```

### 4.3 Emoji Guide (Use Sparingly)

**Contextual (always relevant):**
- 👤 Gender
- 🎨 Series
- ⭐ Tier
- 📈 Sales trends
- 📦 Stock status
- 🔢 Data source
- 📅 Period

**Status Flags (only when condition met):**
- 🔥 **Fast turnover** — `to_total < 0.5` (urgent restock)
- 🐌 **Slow turnover** — `to_total > 2.5` (overstock)
- ⚠️ **Alert** — Negative stock, big drop (>-70% YoY)
- ✅ **Healthy** — Positive indicators
- 📉 **Declining** — YoY drop
- 📈 **Growing** — YoY gain
- 💰 **High value** — Sales mix >2%

**Ranking:**
- 🥇 #1
- 🥈 #2
- 🥉 #3
- 4️⃣-🔟 Numbers

---

## 5. Common User Requests → Query Mapping

| User Request | Source | Query Pattern |
|--------------|--------|---------------|
| "Top 10 best sellers" | `mart.sku_portfolio` | `ORDER BY current_year_qty DESC LIMIT 10` |
| "Top 10 worst performers" | `mart.sku_portfolio` | `ORDER BY current_year_qty ASC LIMIT 10` (or `var_year_qty ASC` for biggest drops) |
| "CLASSIC series performance" | `mart.sku_portfolio` | `WHERE series = 'Classic' ORDER BY current_year_qty DESC` |
| "Men vs Ladies comparison" | `mart.sku_portfolio` | Two queries: `WHERE gender = 'MEN'` and `WHERE gender = 'LADIES'` |
| "Articles with low stock" | `mart.sku_portfolio` | `WHERE to_total < 1 ORDER BY to_total ASC` |
| "Fast movers (stockout risk)" | `mart.sku_portfolio` | `WHERE to_total < 0.5 ORDER BY to_total ASC` |
| "Slow movers (overstock)" | `mart.sku_portfolio` | `WHERE to_total > 3 ORDER BY to_total DESC` |
| "Negative WH stock (data check)" | `mart.sku_portfolio` | `WHERE wh_total < 0 ORDER BY wh_total ASC` |
| "Sales by store (Jatim)" | `core.sales_with_product` | `WHERE area = 'Jatim' GROUP BY matched_store_name` |
| "Stock in Warehouse Pusat" | `core.stock_with_product` | `WHERE nama_gudang ILIKE '%warehouse pusat%'` |
| "Last 7 days sales" | `core.sales_with_product` | `WHERE transaction_date >= CURRENT_DATE - INTERVAL '7 days'` |

---

## 6. Critical Business Rules (Never Violate)

### Rule 1: ALWAYS exclude intercompany (sales queries)
```sql
WHERE is_intercompany = FALSE
```
**Why:** DDD↔MBB↔UBB↔LJBB fake transfers inflate revenue (~Rp 15Bn total). mart.sku_portfolio already excludes this.

### Rule 2: ALWAYS exclude non-product items (product analysis)
```sql
AND UPPER(article) NOT LIKE '%SHOPPING BAG%'
AND UPPER(article) NOT LIKE '%HANGER%'
AND UPPER(article) NOT LIKE '%PAPER BAG%'
AND UPPER(article) NOT LIKE '%THERMAL%'
AND UPPER(article) NOT LIKE '%BOX LUCA%'
```
**Why:** Accessories inflate article counts. mart.sku_portfolio already excludes this.

### Rule 3: Use kode_mix for version-agnostic analysis
**Why:** V0→V1→V2→V3→V4 = same physical product, different codes. mart.sku_portfolio uses `kodemix` already.

### Rule 4: Understand column name differences
| Concept | mart.sku_portfolio | core.sales_with_product | core.stock_with_product |
|---------|-------------------|------------------------|------------------------|
| Article ID | `kodemix` | `kode_mix` | `kode_mix` |
| Store name | N/A (national only) | `matched_store_name` | `nama_gudang` |
| Branch | N/A | `branch` | `gudang_branch` |
| Area | N/A | `area` | `gudang_area` |
| Category | N/A | `store_category` | `gudang_category` |

### Rule 5: mart.sku_portfolio limitations
- ❌ NO store/area/branch breakdown (national aggregate only)
- ❌ NO custom date ranges (current year vs last year only, snapshot)
- ❌ NO transaction detail (pre-aggregated)
- ✅ YES monthly breakdown (12 months × 2 years)
- ✅ YES comprehensive metrics (sales + stock + turnover)
- ✅ YES fast queries (pre-computed)

---

## 7. Response Checklist

Before sending reply to user:

- [ ] Picked the right data source (mart vs core)?
- [ ] Applied mandatory filters (intercompany, non-product)?
- [ ] Used correct column names (matched_store_name vs nama_gudang)?
- [ ] Formatted for WhatsApp (emoji, bullets, max 30 lines)?
- [ ] Added insights summary (positives, concerns, actions)?
- [ ] Flagged alerts (🔥 stockout, ⚠️ negative stock, 📉 big drop)?
- [ ] Kept it brief (respect mobile reading)?

---

## 8. Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│ PRODUCT ANALYSIS CHEAT SHEET                            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ DATA SOURCE PRIORITY:                                   │
│   1️⃣  mart.sku_portfolio (use this first)              │
│   2️⃣  core.sales_with_product (if need store/date)     │
│   3️⃣  core.stock_with_product (stock breakdown only)   │
│                                                          │
│ MANDATORY FILTERS:                                      │
│   ✓ is_intercompany = FALSE                            │
│   ✓ Exclude SHOPPING BAG, HANGER, etc.                 │
│                                                          │
│ OUTPUT FORMAT:                                          │
│   • 1-5 articles → Detailed blocks                      │
│   • 6+ articles → Compact list                          │
│   • Always add insights summary                         │
│                                                          │
│ AUTO-FLAGS:                                             │
│   🔥 to_total < 0.5 (stockout risk)                    │
│   🐌 to_total > 2.5 (overstock)                        │
│   ⚠️ wh_total < 0 (data quality)                       │
│   📉 var_year_qty < -70% (big drop)                    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Notes

- **Template updated:** 2026-02-15 (merged zuma-data-analyst-skill + product-analysis-template)
- **Primary source:** `mart.sku_portfolio` (101 columns, created today)
- **Fallback sources:** `core.sales_with_product`, `core.stock_with_product`
- **Target audience:** Wayan, R&D (Mbak Dewi, Mbak Desyta, Yuda), Merchandiser (Mas Bagus, Mbak Virra)
- **Platform:** WhatsApp-first (mobile reading, compact format)
