# MEMORY.md — Iris's Long-Term Memory

## Key Facts
- Iris = lead AI personal assistant Zuma Indonesia (footwear retail, sandal)
- Setup date: 2026-02-11
- Primary language: Bahasa Indonesia
- Tone: chill, clear, no jargon
- **Heartbeat interval:** Every 1 minute — check HEARTBEAT.md for pending tasks
- **⚠️ OpenCode IS INSTALLED:** Binary at `~/.opencode/bin/opencode` (v1.1.64) — ALWAYS use full path!
- **⚠️ DB Credentials:** ALWAYS hardcode in terminal when delegating to OpenCode/Claude Code/Kimi (.env auto-rejected). Safe karena gak masuk git.

## Critical Lessons Learned

### HEARTBEAT.md Task Tracker (2026-02-13)
**Problem:** Delegated tasks with promise to follow up ("nanti kabarin") but no tracking system → broken promises, 2-3+ hour delays

**Incident:** Mbak Dewi (R&D Manager) request penjualan Merci 16:55, Iris promise "nanti kabarin", but no follow-up until Wayan reminded 19:16 (2h+ delay)

**Root cause:** Delegate without tracking = broken promises. Good intentions ≠ reliable execution.

**Solution (Wayan's idea):** HEARTBEAT.md as pending task tracker
- When delegate + promise follow-up → Write to HEARTBEAT.md immediately
- Every heartbeat (1 min) → Check HEARTBEAT.md, poll tasks, deliver or escalate
- Task done → Deliver result + remove from HEARTBEAT.md

**Files:** `HEARTBEAT.md` (template), `AGENTS.md` (mandatory workflow section)

**Workflow enforced:** Never promise "nanti kabarin" without tracking in HEARTBEAT.md

### Chat History Query Pattern (2026-02-13)
**Rule:** Keyword "chat" triggers different search behavior

**WITH "chat" keyword** ("km chat [person] apa") → Directly grep session logs:
```bash
grep -h "person\|keyword" ~/.openclaw/agents/main/sessions/*.jsonl
```

**WITHOUT "chat" keyword** ("apa km udah [task]?") → Search memory first (memory_search or memory/*.md), then logs if needed

**Why:** "Chat" = raw conversation history request. No "chat" = context/facts from curated memory.

## Zuma Indonesia Business Context
- **Industry:** Footwear (sandal & flip-flops), manufacturing + retail + e-commerce + wholesale + consignment
- **HQ:** Surabaya, Jawa Timur
- **4 Entitas:** DDD (main, retail), MBB (online marketplace), UBB (wholesale), LJBB (PO receiving Baby & Kids)
- **6 Cabang:** Jatim, Jakarta, Sumatra, Sulawesi, Batam, Bali
- **Brand:** Zuma Teal #002A3A, Zuma Green #00E273, Japandi aesthetic
- **Supplier utama:** HJS (PT Halim Jaya Sakti / Ando Footwear)
- **Data sources:** Accurate Online (ERP), iSeller (POS), Ginee (marketplace), Supabase, Google Sheets
- **Skills repo:** `/Users/database-zuma/.openclaw/workspace/zuma-business-skills/` — 10 skills covering ops, planogram, RO, brand
- **Transaksi affiliasi:** Inter-company transactions (DDD↔MBB↔UBB↔LJBB) harus di-exclude dari analisis, sudah di-handle di mart.* tables

## Database Access
- **PostgreSQL VPS:** see .env (PGHOST, PGDATABASE, PGUSER, DATABASE_URL)
- **Schemas:** raw (Accurate API daily), portal (Google Sheets master), core (transformed views), mart (ad-hoc analysis), public (Looker Studio mirrors)
- **psql client:** installed via brew (libpq 18.1)

### Sales Detail Per Artikel (Learned 2026-02-16)
**When user requests:** "sales data per artikel/article mix" dengan breakdown Type/Gender/Series/Tier

**Query from:** `public.sales_summary_plano` (bukan raw/mart!)

**Key columns:**
- transaction_month (timestamp) → format jadi Month
- kode_mix → Article Mix
- tipe → Type
- gender → Gender
- series → Series
- product_name → Article
- tier → Tier
- total_quantity → Sales Qty

**Store names:** LOWERCASE! ('zuma nagoya hills', 'zuma ska mall', dll)

**Example query:**
```sql
SELECT 
  TO_CHAR(transaction_month, 'Mon YYYY') AS month,
  kode_mix, tipe, gender, series, product_name, tier,
  total_quantity
FROM public.sales_summary_plano
WHERE store_name_raw = 'zuma nagoya hills'
  AND transaction_month >= '2025-02-01'
ORDER BY transaction_month, kode_mix;
```

**Output format:** Month | Article Mix | Type | Gender | Series | Article | Tier | Sales Qty

## People

### Core Team
- **Wayan** — System Developer, Dept. Operasional, Divisi Continuous Improvement, Zuma Indonesia (WA: see .env WAYAN_WA) — yang setup Iris

### OPS Team (WhatsApp Group)
**Detailed context:** See `memory/contexts/ops-team.md` for full team profiles, ongoing projects, and conversation history.

**Quick reference:**
- **Mbak Dini** — OPS Manager (head of team)
- **Mbak Citra** — Purchasing Supervisor
- **Mbak Sari** — Purchasing Admin
- **Mas Bagus** — Merchandiser (stock optimization)
- **Mbak Virra** — Allocation Planner (distribution flow)
- **Mbak Galuh** — Staff Inventory Control
- **Nabila** — Staff Inventory Control
- **Mbak Fifi** — Branch Support Specialist
- **Mbak Nisa** — CI Supervisor
- **Wafi** — CI Implementation Specialist
- **Wayan** — CI System Developer (admin/master)

### Strategic Leadership & Department Heads
- **Pak Steven Eka Halim** — CEO & Founder Zuma Indonesia
- **Bu Melissa** — Istri Pak Steven
- **Pak Fikri** — General Manager
- **Mas Grady** — Business Project Manager (under Pak Steven)
- **Pak Donny** — Creative Director (oversees Product Development & Creative Marketing)
- **Bu Aulia** — FATAL Manager (Finance, Accounting, Tax, Asset, Legal)
- **Bu Ary** — HRGA Manager (Human Resources, General Affairs)
- **Ko Budy** — Manager Wholesale & Business Development
- **Mbak Dewi** — Manager Product Development (R&D)
- **Bu Lena Yulinar** — Creative & Marketing Manager (CnM)
- **Mbak Desy** — SPV Product Development
- **Pak Wishnu** — Manager Online
- **Pak Wahyu** — SPV Online (e-commerce/marketplace)
- **Pak Ali Ihsan** — SPV Warehouse Pusat (Warehouse Surabaya / WHS)

## Browser Control
- Chrome profile: wayan@zuma.id — relay must be manually ON per tab
- YouTube SPA navigation keeps relay alive (don't navigate away from youtube.com)
- Always skip YouTube ads
- OpenClaw browser (profile "openclaw") works without relay but has no login

### YouTube Music Policy (2026-02-16)
**User requests lagu → langsung puter, no relay needed**
- Don't ask about relay setup
- Switch existing YouTube tab OR open new browser
- Use openclaw browser profile (standalone, works immediately)
- Quick execution > relay configuration

## Wayan's Preferences
- Music: Denny Caknan, Sabrina Carpenter, Bad Bunny

## VPS Team — MY EMPLOYEES 👥
**CRITICAL:** Iris Junior, Atlas, Apollo adalah **karyawan aku**. Aku bisa delegasi tasks ke mereka, bukan cuma ke local tools (Claude Code/Kimi)!

**⚠️ VPS DELEGATION SCOPE (2026-02-16): CRON JOB ONLY!**
- VPS agents = automated scheduled tasks (cron monitoring, ETL health checks, daily reports)
- **NOT for:** Ad-hoc queries, exploratory analysis, experimental work
- **Why:** VPS = 8GB RAM, 2 CPU cores (limited vs Mac mini M4 with stronger computing power)
- **Ad-hoc work** (Mbak Dewi queries, product analysis, etc) → **opencode on Mac mini** with zuma-business-skills

### VPS Infrastructure (76.13.194.103 - Hostinger KVM 2)
- **Specs:** 8GB RAM, 100GB NVMe SSD, 2 CPU cores
- **SSH Access:** `ssh iris-junior` (configured in ~/.ssh/config)
- **Persistent TUI:** Via `openclaw tui` di SSH session

### Iris Junior ✨ (Coordinator - VPS)
- **Location:** `/root/.openclaw/workspace/`
- **Role:** Project Manager/Reviewer — generate morning reports, eskalasi ke Wayan
- **Model:** Sonnet 4.5 (primary), Kimi k2p5, Deepseek (fallbacks)
- **Workflow:** Review laporan Atlas/Apollo → Generate morning report 08:00 WIB → Telegram ke Wayan
- **Tools:** Notion API, read JSON reports, Telegram
- **Communication:** Via TUI (persistent SSH session) or `openclaw agent --agent main --message`
- **Personality:** Dewi Pelangi — jembatan komunikasi, review bukan execute, hemat kata

### Atlas 🏔️ (Operations Agent - VPS)
- **Location:** `/root/.openclaw/workspace-ops/`
- **Agent ID:** `ops`
- **Model:** Kimi k2p5 (primary), Deepseek, Sonnet (fallbacks)
- **Department:** Stock & Inventory, Warehouse, Logistics
- **Role:** DATA MOVER — tarik data mentah, paste ke GSheet, formulas yang ngitung
- **Tools:** Accurate Online API, Google Sheets (gog CLI), Email, Telegram
- **Key Tasks:**
  - Monitor cron jobs (Stock Pull 03:00, Sales Pull 05:00 WIB)
  - Auto-fix errors (max 3x retry)
  - Write JSON reports to `/root/.openclaw/workspace-ops/logs-report-for-iris/`
  - Eskalasi ke Iris Junior kalau 3x gagal
- **Key PICs:** Mas Bagus Kiswoyo, Mbak Virra, Bu Dini Tri Mart, Mbak Citra, Mbak Sari, Galuh, Nabila, Mbak Fifi
- **Communication:** `ssh iris-junior "openclaw agent --agent ops --message 'text'"`
- **Personality:** Steady, reliable, to the point, paranoid soal stok

### Apollo 🎯 (R&D Agent - VPS)
- **Location:** `/root/.openclaw/workspace-rnd/`
- **Agent ID:** `rnd`
- **Model:** Kimi k2p5 (primary), Deepseek, Sonnet (fallbacks)
- **Department:** Product Development, Quality Control, Material Sourcing
- **Role:** DATA MOVER — track product timeline, monitor material sourcing, QC reports
- **Status:** Currently IDLE (belum ada tugas aktif)
- **Tools:** Accurate Online, Google Sheets (gog CLI), Email, Telegram
- **Key PICs:** Mbak Dewi Kartikawati (R&D Manager), Mbak Desyta, Yuda
- **Communication:** `ssh iris-junior "openclaw agent --agent rnd --message 'text'"`
- **Personality:** Presisi, elegan, terobsesi kualitas, sabar tapi presisi

### VPS Daily Workflow
```
02:00 WIB → Backup DB (pg_dump daily, pg_dumpall weekly on Sunday)
03:00 WIB → Stock Pull (cron VPS DB) + FF/FA/FS calculation
            ├─ pull_accurate_stock.py (4 entities)
            └─ calculate_ff_fa_fs.py → mart.ff_fa_fs_daily
05:00 WIB → Sales Pull (cron VPS DB) + SO L2 calculation
            ├─ pull_accurate_sales.py (3 entities: DDD, MBB, UBB)
            └─ calculate_so_l2.py → mart.stock_opname_l2_daily (NEW as of 2026-02-14)
05:30 WIB → Atlas health check → JSON report (Stock/Sales/Backup/FF-FA-FS/SO-L2 status)
06:00 WIB → Iris morning report → Format & deliver via WhatsApp
```

**Pending expansion (noted 2026-02-14):**
- [x] ~~SO Level 2 Report automation~~ ✅ DEPLOYED 2026-02-14 23:04 (mart.stock_opname_l2_daily live!)
- [ ] Control Stock Report automation
- [ ] Planogram Report automation
- [ ] RO Report (Box & Protol) automation
- [ ] Surplus Store Report automation
- Pattern: API pull → SQL script → Atlas logs → Iris daily summary
- Details: `inbox/pending-tasks-automation-reports.md`

**Health Check Coverage (updated 2026-02-14 23:04):**
1. Stock Pull monitoring (status, errors, timing)
2. Sales Pull monitoring (status, errors, timing)
3. **Backup verification** (daily file exists, size reasonable)
4. **FF/FA/FS metrics** (Fill Factor/Article/Stock — store fill rates vs planogram)
   - avg_ff, avg_fa, avg_fs across all stores
   - stores_below_ff_70 count
   - Alert if avg_ff < 50% or stores_calculated = 0
5. **SO L2 metrics** (Stock Opname Level 2 — daily stock vs sales reconciliation)
   - snapshot_date, stores calculated, rows_inserted
   - selisih_nonzero_count (anomaly detection)
   - total_stock, total_sales
   - Alert if overall ≠ success or selisih_nonzero_count > 30

**Backup System (VPS DB):**
- Location: `/root/backups/` on 76.13.194.120
- Daily: 02:00 WIB, retain 7 days
- Weekly: Sunday 02:00 WIB (pg_dumpall), retain 4 weeks
- Typical size: ~50-55MB daily

**Eskalasi:** 1-2x fail → Atlas fix | 3x fail → `escalation_needed: true` → Iris Junior → Wayan (Telegram)

### Query Pattern: R&D/Product Development (Apollo Territory)
**Delegation Rule (2026-02-13):**
- **R&D/Product Development requests** (Mbak Dewi, Mbak Desyta, Yuda) → **Apollo**
- **National product performance queries** (anyone) → **Apollo**

**Format Standard:**
- Article level: Gender + Series + Color (e.g., LADIES MERCI MOCCA)
- NO size breakdown unless explicitly requested
- Output: Product Name | Total Pairs | Total Revenue

**Mandatory Filters:**
1. `is_intercompany = FALSE` (exclude inter-entity transactions)
2. Exclude non-SKU items (bags, hangers, accessories) unless requested
3. National aggregate (all stores)

**Example:** Merci sales query → Group by color only → Brief output

### Product Analysis Template (2026-02-17) — UPDATED PRIMARY SOURCE

**Template:** `templates/product-analysis-unified.md` (merged SQL query framework + WhatsApp formatting)
**Combines:** zuma-data-analyst-skill query patterns + output formatting best practices

**Data Source Priority (updated 2026-02-17):**
1. **mart.sku_portfolio_size** (primary) — 107 columns, size-level (most granular), can aggregate to article-level, YoY comparison, monthly breakdown
2. **mart.sku_portfolio** (fallback) — 101 columns, article-level only, use when already have aggregates or prefer simpler structure
3. **core.sales_with_product** (fallback) — when need store/area breakdown or custom date ranges
4. **core.stock_with_product** — stock breakdown by warehouse/store

**Query Framework (WHAT/WHERE/WHEN):**
```
"Berapa [METRIC] dari [WHAT] di [WHERE] selama [WHEN]?"
→ Identify metric, product level, geography, time period
→ Pick data source based on requirements
→ Apply mandatory filters (intercompany, non-product)
→ Format output (detailed blocks vs compact list)
```

**Use cases:**
- Top N analysis (best sellers, worst performers, fast/slow movers)
- Specific SKU performance (by kodemix, series, gender, tier)
- Stock alerts (stockout risk, overstock, negative WH)
- YoY comparisons, monthly trends, sales mix %, turnover analysis

**Output Format:**
- **Detailed blocks** (1-5 articles): Sales + Stock + Insights per article
- **Compact list** (6+ articles): One-liner per article + summary

**Auto-flags:** 🔥 Stockout (<0.5mo TO), 🐌 Overstock (>2.5mo), ⚠️ Negative WH, 📉 Big drop (>-70% YoY)

**Key metrics from mart.sku_portfolio:**
- Sales: current_year_qty/rp, last_year_qty/rp, var_year_qty (YoY %), now_jan_qty...now_dec_qty (monthly)
- Stock: stok_global, wh_pusat, wh_bali, wh_jkt, stok_toko, stok_online, stok_unlabel
- Turnover: to_wh, to_total (months of coverage)
- Other: sales_mix %, avg_last_3_months, current_year_label, last_year_label

### mart.sku_portfolio_size (2026-02-17) — SIZE-LEVEL ANALYSIS ⚠️ CRITICAL QUERY RULE

**Table Design:**
- **Grain:** `kode_besar` (SKU with size + version, e.g., M1SPV201Z42)
- **Primary Key:** `kode_besar` (UNIQUE constraint)
- **Rows:** 5,220 (all SKU versions × sizes)
- **Columns:** 107 (11 ID/Base + 83 Sales + 13 Stock)
- **Purpose:** Most granular level for size-level analysis

**⚠️ CRITICAL ANALYSIS RULE (2026-02-17 from Wayan):**

**ALWAYS use `kodemix` or `kode_mix_size` for analysis — NEVER filter by single `kode_besar`!**

**Why:**
- One article has **multiple kode_besar versions** (M1SPV201, M1SP01, M1SPV101, SJ1A)
- Kode lama → kode baru evolution (same product, different codes over time)
- Filtering `kode_besar = 'M1SPV201Z42'` = only 1 version (incomplete!)
- Filtering `kodemix = 'M1SP0PV201'` = SUM ALL versions = true article performance

**Table Design Purpose:**
- `kode_besar` as PK = enforce data integrity (prevent duplicate rows at granular level)
- Analysis purpose = aggregate by `kodemix` (ignore version differences)

**Query Pattern:**
```sql
-- ✅ CORRECT (business analysis — sum all versions):
SELECT 
    kodemix, size, 
    SUM(current_year_qty) AS total_qty,
    SUM(current_year_rp) AS total_rp
FROM mart.sku_portfolio_size
WHERE kodemix = 'M1SP0PV201'
GROUP BY kodemix, size;

-- ❌ WRONG (only 1 version, incomplete):
SELECT current_year_qty, current_year_rp
FROM mart.sku_portfolio_size
WHERE kode_besar = 'M1SPV201Z42';
```

**Example:**
- User asks: "MEN STRIPE BLACK BLUE RED size 42"
- Correct approach:
  1. Find kodemix: `M1SP0PV201`
  2. Query: `WHERE kodemix = 'M1SP0PV201' AND size = '42'`
  3. GROUP BY kodemix, size
  4. Result: SUM(M1SPV201Z42 + M1SP01Z42 + M1SPV101Z42 + ...) = ALL versions combined

**Case-Sensitivity Fix (2026-02-17):**
- Sales/Stock data = lowercase `kode_besar` (m1spv201z39)
- portal.kodemix = UPPERCASE `kode_besar` (M1SPV201Z39)
- Solution: `UPPER(kode_besar)` in all CTEs to ensure JOIN success

**Data Sources:**
- Articles: portal.kodemix (DISTINCT ON kode_besar)
- Sales: core.sales_with_product (with `UPPER(kode_besar)`)
- Stock: core.stock_with_product (with `UPPER(kode_besar)`)

**When to use mart.sku_portfolio_size vs mart.sku_portfolio:**
- Need **size breakdown** → mart.sku_portfolio_size
- Article-level only (no size) → mart.sku_portfolio
- Both tables: Same business rules, same metrics, different grain

### VPS Credentials (Shared)
**Location:** `/root/.openclaw/.env` (GH_TOKEN, NOTION_API_KEY, GOG_KEYRING_PASSWORD)

### Notion Integration (Managed by Iris Junior)
- **Projects DB:** `30031616-a0d5-8194-96b3-d09fbf4da2cc`
- **Tasks DB:** `30031616-a0d5-81ac-86f0-e108677a6d0a`
- **Active Projects:** Control Stock PoC, System Setup, Incidental, R&D Status Reports (Planning)
- **Rule:** Setiap task WAJIB linked ke Project, Iris Junior manage bukan execute

### Delegation Strategy — CRITICAL 🎯
**🔴 WAYAN'S RULE (2026-02-12):** See AGENTS.md "Task Delegation" for full details.
**Quick ref:** Mac mini=browser/file ops | Atlas=ALL DB queries/GSheets | Iris Junior=monitoring/Notion/eskalasi | Apollo=R&D (when active)
**Comms:** TUI (persistent, less tokens) or CLI one-shot

### Presentation Workflow — MANDATORY 🚨
**POLICY (2026-02-16):** ALL PPT requests = HTML (Tailwind CSS) + Vercel deploy (`vercel --prod --yes`) → Share URL. ONLY python-pptx if user explicitly requests .pptx or HTML fails.

**Why:** Web-shareable, fast iteration (10s redeploy), better print quality (Cmd+P), no layout struggles.

**Reference:** https://ro-benchmark-vercel.vercel.app | **Skill:** `zuma-business-skills/general/zuma-ppt-design/SKILL.md`
**Covers:** Visual design (KBI-inspired) + HTML/Vercel tech + Data storytelling (SCQA, Pyramid Principle, Narrative Arc)

## Critical Lessons: Branch/Store Mapping (2026-02-16)

**NEVER ASSUME store locations from names!** Epicentrum=Lombok (not Jakarta), Level 21=Bali, City of Tomorrow=Surabaya.

**MANDATORY:** Always JOIN `portal.store` (source of truth) for branch/area — NEVER use `CASE WHEN` pattern matching on store names.
```sql
LEFT JOIN portal.store ps ON s.store_name_raw = ps.nama_accurate OR s.store_name_raw = ps.nama_iseller
```
**Rule:** `portal.store` > assumptions. Always query first, never guess.

## DN-to-PO Workflow (2026-02-16)

**Purpose:** Convert Delivery Note (DN) documents to Invoice (DDD) + Purchase Order (MBB/UBB) formats for Accurate Online import

**CRITICAL:** 1 DN = 2 outputs (Invoice + PO) — both files MANDATORY

### Standard Scripts (MUST USE):
1. `~/.openclaw/workspace/dn-to-po/convert-dn-to-invoice.js` — Generate Invoice for DDD (seller)
2. `~/.openclaw/workspace/dn-to-po/convert-dn-to-po.js` — Generate PO for MBB/UBB (buyer)

### Supported Input Formats:
- ✅ Excel (.xlsx) — Sheet "Pengiriman Pesanan"
- ✅ PDF (.pdf) — Text extraction with pdf-parse library (added 2026-02-16)

### Workflow:
```bash
# Step 1: Generate Invoice for DDD
node convert-dn-to-invoice.js <file_DN>

# Step 2: Generate PO for entity (ask user: MBB atau UBB?)
node convert-dn-to-po.js <file_DN> <MBB|UBB>
```

### Features:
- Pricing auto-load from `template/Master Harga.xlsx` | PDF+Excel auto-detected | Same output structure

### Output:
- **Invoice:** `INV-DDD-dari-{NO_DN}-{TANGGAL}-{JAM}.xlsx` | **PO:** `PO-{ENTITY}-dari-{NO_DN}.xlsx`
- **Location:** `~/Desktop/DN PO ENTITAS/`
- **Delivery:** Send BOTH files (Invoice+PO) with caption (filename, DN#, SKU count, date) + Google Sheets link

### Critical Rules:
1. ALWAYS use standard scripts (NEVER ad-hoc Python)
2. ALWAYS deliver Excel + GSheets link TOGETHER
3. ALWAYS generate BOTH files (Invoice + PO)
4. **Bu Aulia incident (2026-02-16):** Ad-hoc output + link-only = "tidak sesuai". Lesson: Consistency = trust

**Skill location:** `zuma-business-skills/ops/dn-to-po/SKILL.md`
**Repo:** https://github.com/database-zuma/dn-to-po
