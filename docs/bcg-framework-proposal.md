# 📊 BCG Matrix Framework Proposal — Zuma Indonesia
### Versi: v1.0 | Tanggal: 18 Februari 2026 | Prepared by: Oracle (AI Data Analyst)

---

## 🔴 Problem Statement

BCG Matrix yang sekarang pakai **YoY growth sebagai Y-axis**, dan ini bikin framework-nya broken untuk produk baru. Contoh konkret:

- **Airmove** launch September 2025 → revenue YoY = **-85%** karena bandingin Sep-Dec 2025 vs **nol** tahun lalu
- **Merci series** baru 4 bulan → masuk kuadran **Dog** padahal jualnya oke
- Produk **T8** (new launch < 3 bulan) secara definisi tidak bisa punya YoY valid

Akibatnya? **BCG jadi misleading** dan bisa trigger keputusan salah — misalnya discontinue produk yang sebetulnya potensial.

---

## 💡 Prinsip Dasar Sebelum Pilih Framework

Sebelum propose solusi, ada 3 prinsip yang harus dijaga:

1. **Fairness by Age** — Produk baru dan produk lama harus diukur dengan metrik yang setara secara konteks
2. **Actionability** — Hasilnya harus bisa langsung dipakai buat keputusan (prioritas resource, alokasi stock, discontinue)
3. **Simplicity** — Tim ops harus bisa ngerti, bukan cuma data team

---

## 📋 Tiga Framework Options

---

## Option 1: ⚡ Sales Velocity BCG *(Recommended)*

### Konsep
Ganti YoY growth dengan **Sales Velocity** — seberapa cepat produk ini jual dibanding rata-rata portfolio. Ini fair karena produk baru pun punya avg_monthly_sales yang bisa langsung dibandingkan.

### Definisi Axis

| Axis | Metric | Formula |
|------|--------|---------|
| **X-axis** | Revenue Contribution (%) | `avg_monthly_revenue / SUM(avg_monthly_revenue) × 100` |
| **Y-axis** | Velocity Ratio | `avg_monthly_sales / MEDIAN(avg_monthly_sales portfolio)` |

**Threshold:**
- X-axis threshold: **0.5%** (asumsi 200 SKU → average = 0.5%; pakai median portfolio juga bisa)
- Y-axis threshold: **1.0** (di atas median = "growing", di bawah = "lagging")

### Quadrant Interpretation

```
Y (Velocity)
   High │ ⭐ STAR           │ ❓ QUESTION MARK
  > 1.0 │ Revenue besar,    │ Revenue kecil,
        │ jual cepet        │ tapi jual cepet
        │ → Prioritas utama │ → Scaling candidate
   ─────┼───────────────────┼───────────────────
        │ 🐄 CASH COW       │ 🐕 DOG
  < 1.0 │ Revenue besar,    │ Revenue kecil,
        │ jual lambat       │ jual lambat
        │ → Jaga, efisiensi │ → Review/discontinue
   Low  └───────────────────┴───────────────────
                Small ◄── X (Revenue Share) ──► Large
                         Threshold: 0.5%
```

### Penanganan T8 (New Launch)
- Produk T8 **tetap masuk BCG** tanpa perlakuan khusus
- Karena `avg_monthly_sales` = aktual run rate bulan-bulan mereka jualan, bukan dibanding tahun lalu
- Tambahkan **label visual** `[NEW]` di chart untuk produk `first_sale_date < 90 hari` supaya stakeholder tahu ini masih early stage
- **Interpretasi T8 di Dog quadrant**: bukan "jelek", tapi "belum terbukti" → butuh monitoring 3 bulan lagi

### Pros & Cons

| ✅ Pros | ❌ Cons |
|---------|---------|
| Fair 100% untuk semua umur produk | Tidak capture growth trend (produk bisa stagnant tapi velocity oke) |
| Data tersedia langsung di `avg_monthly_sales` | Velocity tinggi bisa karena seasonality |
| Simple dan intuitif | Perlu re-baseline kalau portfolio berubah drastis |
| Easy to recompute monthly | - |

### SQL Query

```sql
-- ===========================================
-- OPTION 1: Sales Velocity BCG Matrix
-- ===========================================
WITH portfolio_stats AS (
    SELECT
        PERCENTILE_CONT(0.5) WITHIN GROUP (
            ORDER BY avg_monthly_sales
        )::numeric AS median_monthly_sales,
        SUM(avg_monthly_revenue)           AS total_avg_monthly_revenue
    FROM mart.sku_portfolio
    WHERE avg_monthly_sales > 0
      AND tier NOT IN ('T4')  -- exclude discontinued
),

sku_bcg AS (
    SELECT
        s.kode_mix,
        s.series,
        s.tier,
        s.gender,
        s.avg_monthly_sales,
        s.avg_monthly_revenue,
        s.current_stock,
        s.asp,

        -- X-axis: Revenue Contribution (%)
        ROUND(
            s.avg_monthly_revenue::numeric
            / NULLIF(p.total_avg_monthly_revenue, 0) * 100,
        2) AS revenue_share_pct,

        -- Y-axis: Velocity Ratio vs Median
        ROUND(
            s.avg_monthly_sales::numeric
            / NULLIF(p.median_monthly_sales, 0),
        2) AS velocity_ratio,

        -- Product Age (bulan sejak first sale)
        EXTRACT(MONTH FROM AGE(CURRENT_DATE, s.first_sale_date))
            + EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.first_sale_date)) * 12
            AS age_months,

        -- New launch flag
        CASE
            WHEN s.first_sale_date >= CURRENT_DATE - INTERVAL '90 days'
            THEN TRUE ELSE FALSE
        END AS is_new_launch,

        -- BCG Quadrant Assignment
        CASE
            WHEN s.avg_monthly_revenue / NULLIF(p.total_avg_monthly_revenue, 0) * 100 >= 0.5
             AND s.avg_monthly_sales / NULLIF(p.median_monthly_sales, 0) >= 1.0
            THEN 'Star ⭐'

            WHEN s.avg_monthly_revenue / NULLIF(p.total_avg_monthly_revenue, 0) * 100 < 0.5
             AND s.avg_monthly_sales / NULLIF(p.median_monthly_sales, 0) >= 1.0
            THEN 'Question Mark ❓'

            WHEN s.avg_monthly_revenue / NULLIF(p.total_avg_monthly_revenue, 0) * 100 >= 0.5
             AND s.avg_monthly_sales / NULLIF(p.median_monthly_sales, 0) < 1.0
            THEN 'Cash Cow 🐄'

            ELSE 'Dog 🐕'
        END AS bcg_quadrant

    FROM mart.sku_portfolio s
    CROSS JOIN portfolio_stats p
    WHERE s.avg_monthly_sales > 0
      AND s.tier NOT IN ('T4')
)

SELECT
    kode_mix,
    series,
    tier,
    gender,
    revenue_share_pct,
    velocity_ratio,
    age_months,
    CASE WHEN is_new_launch THEN '[NEW] ' ELSE '' END || bcg_quadrant AS quadrant_label,
    avg_monthly_sales,
    avg_monthly_revenue,
    current_stock
FROM sku_bcg
ORDER BY revenue_share_pct DESC, velocity_ratio DESC;
```

---

## Option 2: 🔄 Age-Adjusted Momentum BCG

### Konsep
Pakai Y-axis berbeda tergantung umur produk:
- Produk **>= 12 bulan**: pakai YoY growth (var_year_qty) seperti sekarang
- Produk **6–12 bulan**: pakai annualized growth dari avg_monthly vs periode awal
- Produk **< 6 bulan (T8/baru)**: pakai **Growth Momentum** = apakah monthly sales naik/turun dibanding bulan-bulan awal

### Definisi Axis

| Axis | Metric | Notes |
|------|--------|-------|
| **X-axis** | Revenue Share (avg-based) | Sama dengan Option 1 |
| **Y-axis** | Age-Adjusted Growth Score | -100% hingga +200%, tergantung cohort |

**Formula Y-axis per cohort:**
```
Produk >= 12 bulan  → Y = var_year_qty (standard YoY)
Produk 6-12 bulan   → Y = (avg_monthly_sales / first_3m_avg_sales - 1) × 100
Produk < 6 bulan    → Y = 0 (neutral — masuk "Pending" zone, tidak dinilai)
```

**Problem**: Butuh data monthly sales history (tidak tersedia langsung di `mart.sku_portfolio` kalau tidak ada kolom `first_3m_avg_sales`).

### Penanganan T8
Produk < 6 bulan dimasukkan ke **"Nursery Zone"** — area khusus di luar 4 kuadran BCG utama. Dinilai terpisah dengan metrik: stock turnover rate dan performa vs target launch.

### Pros & Cons

| ✅ Pros | ❌ Cons |
|---------|---------|
| Paling akurat secara teoritis | Kompleks — 3 formula berbeda |
| Menghargai nuansa umur produk | Butuh data tambahan (monthly history) |
| Konsisten dengan spirit BCG original | Tim ops susah ngerti kenapa 2 produk dihitung beda |
| YoY tetap dipakai untuk produk mature | Batas cohort (6/12 bulan) terkesan arbitrary |

### SQL Query (Partial — hanya untuk produk >= 12 bulan)

```sql
-- Option 2: Hanya untuk established products
-- Produk < 12 bulan perlu data monthly history terpisah

WITH established_products AS (
    SELECT
        kode_mix,
        series,
        tier,
        gender,
        avg_monthly_revenue,
        avg_monthly_sales,
        var_year_qty,
        EXTRACT(MONTH FROM AGE(CURRENT_DATE, first_sale_date))
            + EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.first_sale_date)) * 12
            AS age_months
    FROM mart.sku_portfolio s
    WHERE first_sale_date <= CURRENT_DATE - INTERVAL '12 months'
      AND tier NOT IN ('T4')
),
portfolio_rev AS (
    SELECT SUM(avg_monthly_revenue) AS total_rev
    FROM mart.sku_portfolio
    WHERE avg_monthly_sales > 0 AND tier NOT IN ('T4')
),
bcg_established AS (
    SELECT
        e.*,
        ROUND(e.avg_monthly_revenue / p.total_rev * 100, 2) AS revenue_share_pct,
        e.var_year_qty AS growth_score,  -- YoY valid karena >= 12 bulan
        CASE
            WHEN e.avg_monthly_revenue / p.total_rev * 100 >= 0.5
             AND e.var_year_qty >= 0
            THEN 'Star ⭐'
            WHEN e.avg_monthly_revenue / p.total_rev * 100 < 0.5
             AND e.var_year_qty >= 0
            THEN 'Question Mark ❓'
            WHEN e.avg_monthly_revenue / p.total_rev * 100 >= 0.5
             AND e.var_year_qty < 0
            THEN 'Cash Cow 🐄'
            ELSE 'Dog 🐕'
        END AS bcg_quadrant
    FROM established_products e
    CROSS JOIN portfolio_rev p
)

SELECT * FROM bcg_established
ORDER BY revenue_share_pct DESC;

-- Produk < 12 bulan: report terpisah (Nursery Report)
SELECT
    kode_mix, series, tier, first_sale_date,
    avg_monthly_sales, avg_monthly_revenue, current_stock,
    'Nursery — Under Evaluation' AS status
FROM mart.sku_portfolio
WHERE first_sale_date > CURRENT_DATE - INTERVAL '12 months'
  AND tier NOT IN ('T4')
ORDER BY first_sale_date DESC;
```

---

## Option 3: 🎯 Tier-Aligned Portfolio Matrix

### Konsep
Bukan BCG klasik, tapi **2×2 matrix yang align dengan Tier system Zuma sendiri**. Pakai Revenue Contribution vs Sell-Through Rate (seberapa cepat stock habis).

### Definisi Axis

| Axis | Metric | Formula |
|------|--------|---------|
| **X-axis** | Revenue Contribution | `avg_monthly_revenue / total portfolio revenue × 100` |
| **Y-axis** | Stock Efficiency Rate | `avg_monthly_sales / (avg_monthly_sales + current_stock/avg_monthly_sales × avg_monthly_sales)` → disederhanakan: `avg_monthly_sales / (current_stock + avg_monthly_sales) × 100` |

Atau lebih simpel: **Months of Stock (MOS)** sebagai Y-axis inverse:
```
MOS = current_stock / avg_monthly_sales
MOS rendah → terjual cepat (bagus)
MOS tinggi → lambat (perlu tindakan)
```

| Quadrant | Revenue | MOS | Tier Align | Action |
|----------|---------|-----|------------|--------|
| **Priority** | High | Low | T1/T2 | Top-up stock segera |
| **Watch** | Low | Low | T8/T2 | Potensial, scale up |
| **Harvest** | High | High | T3 | Reduce order, jaga level |
| **Exit** | Low | High | T4/T5 | Clearance/discontinue |

### Penanganan T8
MOS berlaku fair untuk semua produk — produk baru yang jual bagus akan punya MOS rendah. T8 dengan MOS rendah = signal positif sejak dini.

### Pros & Cons

| ✅ Pros | ❌ Cons |
|---------|---------|
| Align dengan Tier system yang sudah ada | Tidak ada "growth" dimension — tidak tahu arah |
| MOS langsung actionable untuk ops | MOS bisa distorted kalau overstock di awal launch |
| Fair 100% untuk semua umur produk | Bukan BCG "asli" — perlu reframing ke stakeholder |
| Simple, 2 kolom yang langsung tersedia | - |

### SQL Query

```sql
-- Option 3: Tier-Aligned Portfolio Matrix
WITH portfolio_rev AS (
    SELECT SUM(avg_monthly_revenue) AS total_rev
    FROM mart.sku_portfolio
    WHERE avg_monthly_sales > 0 AND tier NOT IN ('T4')
),
sku_matrix AS (
    SELECT
        s.kode_mix,
        s.series,
        s.tier,
        s.gender,
        s.avg_monthly_sales,
        s.avg_monthly_revenue,
        s.current_stock,
        s.asp,

        -- X: Revenue Contribution
        ROUND(s.avg_monthly_revenue / NULLIF(p.total_rev, 0) * 100, 2) AS revenue_share_pct,

        -- Y: Months of Stock (MOS) — makin kecil makin bagus
        ROUND(
            s.current_stock::numeric / NULLIF(s.avg_monthly_sales, 0),
        1) AS months_of_stock,

        -- Product Age flag
        CASE
            WHEN s.first_sale_date >= CURRENT_DATE - INTERVAL '90 days' THEN 'New (<3m)'
            WHEN s.first_sale_date >= CURRENT_DATE - INTERVAL '365 days' THEN 'Growing (3-12m)'
            ELSE 'Established (>12m)'
        END AS product_age_cohort,

        -- Quadrant (threshold MOS = 3 bulan, Revenue = 0.5%)
        CASE
            WHEN s.avg_monthly_revenue / NULLIF(p.total_rev, 0) * 100 >= 0.5
             AND s.current_stock / NULLIF(s.avg_monthly_sales, 0) <= 3
            THEN 'Priority 🔥'

            WHEN s.avg_monthly_revenue / NULLIF(p.total_rev, 0) * 100 < 0.5
             AND s.current_stock / NULLIF(s.avg_monthly_sales, 0) <= 3
            THEN 'Watch 👀'

            WHEN s.avg_monthly_revenue / NULLIF(p.total_rev, 0) * 100 >= 0.5
             AND s.current_stock / NULLIF(s.avg_monthly_sales, 0) > 3
            THEN 'Harvest 🌾'

            ELSE 'Exit 🚪'
        END AS portfolio_quadrant

    FROM mart.sku_portfolio s
    CROSS JOIN portfolio_rev p
    WHERE s.avg_monthly_sales > 0
      AND s.tier NOT IN ('T4')
)
SELECT
    kode_mix,
    series,
    tier,
    gender,
    product_age_cohort,
    revenue_share_pct,
    months_of_stock,
    portfolio_quadrant,
    avg_monthly_sales,
    current_stock,
    asp
FROM sku_matrix
ORDER BY revenue_share_pct DESC, months_of_stock ASC;
```

---

## 🏆 Rekomendasi: Option 1 (Sales Velocity BCG)

### Kenapa Option 1?

Untuk konteks Zuma — **retail footwear, 200+ SKU, mix produk baru dan lama** — ini yang paling masuk akal:

| Kriteria | Option 1 ✅ | Option 2 | Option 3 |
|----------|-------------|----------|----------|
| Fair untuk T8/new launch | ✅ Fully fair | ⚠️ Partially | ✅ Fully fair |
| Butuh data tambahan | ❌ Tidak perlu | ✅ Perlu history | ❌ Tidak perlu |
| Mudah dipahami tim | ✅ Simple | ❌ Kompleks | ✅ Simple |
| Tetap "BCG" secara konsep | ✅ Ya | ✅ Ya | ⚠️ Modifikasi |
| Actionable untuk decisions | ✅ Ya | ✅ Ya | ✅ Ya |
| Data tersedia di mart | ✅ Semua ada | ⚠️ Partial | ✅ Semua ada |

### Implementasi Rekomendasi: Hybrid Approach

Pakai **Option 1 sebagai BCG utama** + **tambahan kolom "age flag"** untuk konteks:

```
BCG Utama:     X = Revenue Share | Y = Velocity Ratio
Age Context:   Label [NEW], [GROWING], [ESTABLISHED] di setiap titik
MOS Insight:   Tambah kolom Months of Stock di tabel detail (dari Option 3)
```

Ini gives you the best of both worlds — BCG yang fair + ops insight yang actionable.

---

## 📐 Threshold Recommendations (Tunable)

| Parameter | Default Value | Rationale |
|-----------|--------------|-----------|
| Revenue Share threshold (X) | **0.5%** | 100/200 SKU = 0.5% average |
| Velocity threshold (Y) | **1.0** (median ratio) | 50th percentile = neutral |
| "New Launch" window | **90 days** | Align dengan T8 definition |
| "Growing" window | **12 months** | Full year untuk YoY valid |
| MOS threshold (jika pakai Option 3) | **3 months** | Industry standard footwear |

> 💡 **Note:** Threshold X bisa di-adjust ke median revenue share aktual (bukan hardcode 0.5%) supaya selalu 50/50 split di setiap run. Pakai `PERCENTILE_CONT(0.5)` di CTE.

---

## 🔧 Quick Fix untuk Dashboard Sekarang

Kalau mau langsung patch BCG yang ada tanpa rebuild total:

```sql
-- Patch: Filter produk < 12 bulan dari YoY calculation
-- Ganti var_year_qty dengan kondisi berikut:

SELECT
    kode_mix,
    series,
    tier,
    -- Gunakan YoY hanya kalau produk >= 12 bulan
    CASE
        WHEN first_sale_date <= CURRENT_DATE - INTERVAL '12 months'
        THEN var_year_qty  -- YoY valid
        ELSE NULL          -- Set NULL, handle di chart sebagai "N/A"
    END AS growth_metric,

    -- Flag untuk chart
    CASE
        WHEN first_sale_date >= CURRENT_DATE - INTERVAL '90 days'
        THEN 'T8 — New Launch (No YoY)'
        WHEN first_sale_date >= CURRENT_DATE - INTERVAL '12 months'
        THEN 'Growing — YoY Not Valid'
        ELSE 'Established — YoY Valid'
    END AS yoy_validity

FROM mart.sku_portfolio
ORDER BY first_sale_date DESC;
```

---

## ✅ Action Plan

| Priority | Action | Owner | Timeline |
|----------|--------|-------|----------|
| 🔴 Segera | Implement Option 1 SQL query ke dashboard BCG | Data Team | 1 minggu |
| 🔴 Segera | Tambah `[NEW]` label untuk produk < 90 hari | Data Team | 1 minggu |
| 🟡 Next | Validate `first_sale_date` ada di semua SKU | Data Team | 2 minggu |
| 🟡 Next | Set threshold review setiap quarter (jangan hardcode) | Data Team | 1 bulan |
| 🟢 Later | Tambah MOS column di BCG detail table | Data Team | 1 bulan |
| 🟢 Later | Bikin Nursery Report terpisah untuk T8 < 90 hari | Data Team | 1 bulan |

---

## 📝 Catatan Penting

1. **`first_sale_date`** — Perlu di-verify apakah kolom ini exist di `mart.sku_portfolio` atau perlu join ke table lain. Kalau tidak ada, bisa di-proxy dari tier (T8 = < 3 bulan by definition).

2. **Mid-year caveat** — `avg_monthly_revenue` dan `avg_monthly_sales` dihitung dari berapa bulan? Kalau produk baru 2 bulan, average-nya dari 2 bulan aja — ini sudah fair. Tapi kalau ada outlier bulan pertama (launch promo), bisa distort. Consider excluding bulan pertama launch dari average.

3. **Series vs SKU** — Proposal ini di level SKU (kode_mix). Untuk series-level view (Airmove as a whole), aggregate dengan `SUM(avg_monthly_revenue)` per series.

4. **T8 by tier definition** — Kalau `first_sale_date` tidak tersedia, gunakan `tier = 'T8'` sebagai proxy untuk new launch flag.

---

*Document generated by Oracle AI | Workspace: /Users/database-zuma/.openclaw/workspace/docs/bcg-framework-proposal.md*
