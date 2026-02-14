# FF/FA/FS Daily Fill Rate Metrics — Automated Workflow

**Source:** Internal briefing from Wayan  
**Date:** 2026-02-14  
**Status:** LIVE (pipeline running daily since deployment)

---

## What's New

**FF/FA/FS** (Fill Factor / Fill Article / Fill Stock) — daily store fill rate metrics are now calculated automatically. These measure how well each retail store is stocked relative to its planogram (target display plan).

---

## Pipeline (Already Running Daily)

### 03:00 WIB — DB VPS (76.13.194.120)

**cron_stock_pull.sh** triggers:

1. **pull_accurate_stock.py** — pulls stock from Accurate Online for 4 entities (DDD, LJBB, MBB, UBB)
2. **calculate_ff_fa_fs.py** — runs AFTER stock pull completes:
   - Auto-syncs store name mappings (`portal.store_name_map`)
   - Reads planogram from `portal.temp_portal_plannogram`
   - Reads stock from `core.stock_with_product`
   - Calculates FF, FA, FS per store
   - Upserts results → `mart.ff_fa_fs_daily`
   - Writes status → `/opt/openclaw/logs/ff_fa_fs_latest_status.json`

### 05:30 WIB — Atlas (76.13.194.103)

**atlas-daily-db-health** job now includes FF/FA/FS check:
- Reads `ff_fa_fs_latest_status.json` via SSH to DB VPS
- Includes `avg_ff`, `avg_fa`, `avg_fs`, `stores_below_ff_70` in health report
- Flags alert if `avg_ff < 50` or `stores_calculated = 0`

### 06:00 WIB — Iris (Mac Mini)

Iris reads Atlas health report daily. FF/FA/FS data is now included in that report under `mart_reports.ff_fa_fs_daily`.

**No additional action required** — data already flows through existing daily health report pipeline.

---

## Key Table: `mart.ff_fa_fs_daily`

**Location:** PostgreSQL VPS DB (76.13.194.120), schema `mart`

**Columns:**
- `report_date` (DATE) — snapshot date
- `branch` (TEXT) — branch name (e.g., "Jatim")
- `store_label` (TEXT) — human-readable store name
- `store_db_name` (TEXT) — database gudang name (as appears in stock table)
- `ff` (DECIMAL) — Fill Factor (% size slots with stock)
- `fa` (DECIMAL) — Fill Article (% articles with any stock)
- `fs` (DECIMAL) — Fill Stock (actual depth vs plan)
- `calculated_at` (TIMESTAMP) — calculation timestamp

**Primary Key:** `(report_date, store_db_name)`

**Values format:** Decimals (e.g., `0.6809` = 68.09%)

**Current scope:** 11 Jatim stores (will expand to all branches when planogram data added)

**Purpose:** Designed for dashboards and reporting to pull from.

---

## Metric Definitions

| Metric | Full Name | What It Measures | Formula | Healthy Target |
|--------|-----------|-----------------|---------|----------------|
| **FF** | Fill Factor | % of planned SIZE SLOTS that have stock | `sizes_with_stock / total_planned_sizes` | **>= 70%** |
| **FA** | Fill Article | % of planned ARTICLES with at least 1 size in stock | `articles_with_any_stock / total_planned_articles` | **>= 90%** |
| **FS** | Fill Stock | Actual stock DEPTH vs planned quantity | `actual_stock_qty / planned_stock_qty` | **80-120%** |

**Key relationships:**
- FA >= FF (always, by definition)
- FF is most important for customer experience (size availability)
- FS > 100% = overstocked (potential surplus)
- FS < 80% = understocked (potential stockout risk)

**Example interpretation:**
```
Store: Zuma Tunjungan Plaza
FF: 68.09% — 68% of planned size slots have stock (⚠️ below 70% target)
FA: 89.47% — 89% of planned articles have at least 1 size (⚠️ below 90% target)
FS: 95.23% — Stock depth is 95% of plan (✅ healthy range)
```

---

## What's NOT Ready Yet (Do NOT Act On These)

**CRITICAL:** Wayan has decided to wait until ALL daily metrics tables are created in `mart` schema before setting up dashboards and daily email summary.

### Not Yet Deployed:

1. **Looker Studio dashboard** pulling from `mart.ff_fa_fs_daily` — not set up yet
2. **Daily email/Gmail report** summarizing all mart metrics in table format — not set up yet

**Reason for waiting:** More `mart.*` tables are coming:
- Sales summary
- Stock health
- Top/bottom sellers
- Other KPIs

**When Wayan gives green light, Iris will be responsible for:**
- Pulling latest data from all `mart.*` tables
- Formatting daily metrics summary (table format)
- Sending via email to Wayan every morning

**Until then:**
- Just include FF/FA/FS status in daily health report relay as Atlas provides it
- **No additional action needed**
- Do NOT proactively set up email reports or dashboards

---

## Reference

**Skill documentation:**  
https://github.com/database-zuma/zuma-business-skills/tree/main/ops/zuma-inventory-control/zuma-ff-skills

**VPS script location:**  
`/opt/openclaw/scripts/calculate_ff_fa_fs.py`

**Status JSON:**  
`/opt/openclaw/logs/ff_fa_fs_latest_status.json`

**Store name mapping table:**  
`portal.store_name_map` — auto-evolving, no manual maintenance needed

**Current stores covered (11 Jatim stores):**
- Tunjungan Plaza, Galaxy Mall, PTC, Icon Gresik, Lippo Sidoarjo, etc.
- Will expand as planogram data added for other branches

---

## Integration with Existing Workflow

**Atlas health check (05:30 WIB)** already includes FF/FA/FS metrics in JSON report:

```json
{
  "mart_reports": {
    "ff_fa_fs_daily": {
      "status": "success",
      "report_date": "2026-02-14",
      "stores_calculated": 11,
      "avg_ff": 0.6809,
      "avg_fa": 0.8947,
      "avg_fs": 0.9523,
      "stores_below_ff_70": 6,
      "alert": false
    }
  }
}
```

**Iris morning report (06:00 WIB)** relays this data as part of overall health summary.

**No workflow changes needed** — FF/FA/FS metrics flow through existing daily report pipeline.

---

## Tags

#inventory #fill-rate #metrics #automation #planogram #stock-health #daily-pipeline #mart-schema #kpi

---

**Deployment date:** 2026-02-14  
**Current status:** Live, running daily  
**Next phase:** Wait for additional `mart.*` tables → dashboard + email report setup (TBD)
