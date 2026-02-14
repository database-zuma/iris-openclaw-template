# Stock Opname Level 2 (SO L2) — Daily Stock vs Sales Reconciliation

**Source:** Internal briefing (Wayan)
**Date:** 2026-02-14 23:04 WIB
**Category:** Inventory Control, Stock Integrity, Automated Reporting

---

## What It Is

`mart.stock_opname_l2_daily` tracks daily stock levels per store × gender group, compares them against yesterday's sales, and flags discrepancies (**selisih**).

**Core Question:** "Does today's stock = yesterday's stock minus yesterday's sales? If not, why?"

---

## The Logic

Every morning after sales pull (05:00 WIB):

```
expected_stock_today = yesterday_stock - yesterday_sales
actual_stock_today = fresh stock from Accurate (pulled 03:00 WIB)
selisih = actual_stock_today - expected_stock_today
```

**Interpretation:**
- **selisih = 0** → Stock checks out perfectly ✅
- **selisih > 0** → More stock than expected (RO received, customer returns, transfer in — usually normal)
- **selisih < 0** → Less stock than expected ⚠️ (potential shrinkage, theft, damage, unrecorded transfer out — **red flag**)

**Note:** Day 1 (Feb 14, 2026) has no selisih because there's no previous day to compare against. From Day 2 onward, the chain works.

---

## Table Schema

**Table:** `mart.stock_opname_l2_daily`

| Column | Type | Description |
|--------|------|-------------|
| `snapshot_date` | DATE | Today's date |
| `store_name` | TEXT | Canonical store name (lowercase, from `portal.store.nama_accurate`) |
| `gender_group` | TEXT | MEN \| LADIES \| BABY & KIDS |
| `branch` | TEXT | Bali, Jatim, Jakarta, Lombok, Batam, Sulawesi, Sumatra, Online |
| `stock_qty` | INTEGER | Today's morning stock count |
| `sales_qty` | INTEGER | Yesterday's sales quantity |
| `prev_stock_qty` | INTEGER | Yesterday's stock (from yesterday's row in this table) |
| `expected_stock_qty` | INTEGER | `prev_stock - sales` |
| `selisih` | INTEGER | `stock_qty - expected_stock_qty` |
| `selisih_pct` | NUMERIC | `selisih / prev_stock × 100` |
| `calculated_at` | TIMESTAMPTZ | When this row was calculated |

**Primary Key:** `(snapshot_date, store_name, gender_group)`

---

## Data Sources

- **Stock:** `core.stock_with_product` — today's snapshot (pulled at 03:00 WIB)
- **Sales:** `core.sales_with_product` — yesterday's sales, filtered to `source_entity = 'DDD'`
- **Store mapping:** `portal.store` — bridges stock names (`nama_department_old`) to sales names (`nama_accurate`), filtered to `category = 'RETAIL'` and `LIKE 'zuma%'`
- **Gender grouping:** `BABY, BOYS, GIRLS, JUNIOR, KIDS` → collapsed to `BABY & KIDS`. `MEN` and `LADIES` stay as-is.

---

## Coverage

- **56 retail stores** across 8 branches
  - Bali: 31 stores
  - Jatim: 12 stores
  - Jakarta: 5 stores
  - Lombok: 2 stores
  - Batam: 2 stores
  - Online: 2 stores
  - Sulawesi: 1 store
  - Sumatra: 1 store
- **3 gender groups per store = 168 rows per day**
- **First data:** Feb 14, 2026. Selisih starts populating from Feb 15 onward.

---

## Cron Schedule

### DB VPS (76.13.194.120)

```
03:00 WIB → cron_stock_pull.sh
            ├── Stock pull (DDD, LJBB, MBB, UBB)
            └── calculate_ff_fa_fs.py ← chained after stock

05:00 WIB → cron_sales_pull.sh
            ├── Sales pull (DDD, MBB, UBB)
            └── calculate_so_l2.py ← NEW, chained after sales
```

### Atlas VPS (76.13.194.103)

```
05:30 WIB → atlas-daily-db-health
            └── Now also checks /opt/openclaw/logs/so_l2_latest_status.json
```

---

## Status File

**Location:** `/opt/openclaw/logs/so_l2_latest_status.json`

**Example:**
```json
{
  "snapshot_date": "2026-02-14",
  "sales_date": "2026-02-13",
  "stores": 56,
  "rows_inserted": 168,
  "total_stock": 122231,
  "total_sales": 1051,
  "selisih_nonzero_count": 0,
  "calculated_at": "2026-02-14T23:00:45.123456",
  "overall": "success"
}
```

---

## Alert Conditions

When reporting to Wayan, flag these:

| Condition | Severity | What To Say |
|-----------|----------|-------------|
| `overall ≠ success` | 🔴 Critical | "SO L2 calculation failed. Check VPS logs." |
| `selisih_nonzero_count > 30` | 🟡 Warning | "More than half of store-gender combos have unexplained stock changes." |
| `stores < 50` | 🟡 Warning | "Only {n} stores calculated. Some stores may be missing from portal.store mapping." |
| Large negative selisih on a single store | 🟡 Warning | "Store X has {selisih} fewer {gender} items than expected. Possible shrinkage." |

---

## Useful Queries for Daily Reports

### 1. Today's Summary by Branch
```sql
SELECT 
  branch, 
  SUM(stock_qty) as stock, 
  SUM(sales_qty) as sales, 
  SUM(CASE WHEN selisih != 0 THEN 1 ELSE 0 END) as anomaly_count
FROM mart.stock_opname_l2_daily
WHERE snapshot_date = CURRENT_DATE
GROUP BY branch
ORDER BY branch;
```

### 2. Stores with Biggest Negative Selisih (Potential Shrinkage)
```sql
SELECT 
  store_name, 
  gender_group, 
  stock_qty, 
  sales_qty, 
  prev_stock_qty, 
  expected_stock_qty, 
  selisih, 
  selisih_pct
FROM mart.stock_opname_l2_daily
WHERE snapshot_date = CURRENT_DATE
  AND selisih < 0
ORDER BY selisih ASC
LIMIT 10;
```

### 3. Week-over-Week Stock Trend for Specific Store
```sql
SELECT 
  snapshot_date, 
  gender_group, 
  stock_qty, 
  sales_qty, 
  selisih
FROM mart.stock_opname_l2_daily
WHERE store_name = 'zuma galaxy mall'
  AND snapshot_date >= CURRENT_DATE - 7
ORDER BY snapshot_date, gender_group;
```

---

## File Locations

| Item | Path |
|------|------|
| **VPS Script** | `/opt/openclaw/scripts/calculate_so_l2.py` |
| **Cron Chain** | `/opt/openclaw/scripts/cron_sales_pull.sh` (SO L2 appended at end) |
| **Status File** | `/opt/openclaw/logs/so_l2_latest_status.json` |
| **Local Copy** | `/Users/database-zuma/zuma-so-l2/calculate_so_l2.py` |

---

## Big Picture: Two Automated Mart Tables

This is the **second automated mart table** (after `mart.ff_fa_fs_daily`). Together they give Wayan daily visibility into:

1. **FF/FA/FS** — Are stores displaying the right products? *(planogram compliance)*
2. **SO L2** — Is stock moving as expected? Are there unexplained losses? *(stock integrity)*

Both run automatically every morning. Atlas monitors both. Iris includes both in daily summary to Wayan.

---

## Key Takeaways

- **SO L2 = daily stock reconciliation** — catch shrinkage, theft, unrecorded transfers early
- **selisih < 0 = red flag** — investigate immediately (potential loss)
- **selisih > 0 = usually normal** — RO received, returns, transfers in
- **First meaningful data: Feb 15, 2026** (Feb 14 has no baseline to compare)
- **168 rows/day** (56 stores × 3 gender groups)
- **Atlas monitors automatically** — Iris reads status, reports anomalies to Wayan

**Tags:** #inventory-control #stock-opname #reconciliation #automation #shrinkage-detection #daily-reporting

---

**Status:** Live as of Feb 14, 2026 23:04 WIB  
**Monitoring:** Atlas (05:30 WIB daily health check)  
**Reporting:** Iris (06:00 WIB morning report, include SO L2 status alongside FF/FA/FS)
