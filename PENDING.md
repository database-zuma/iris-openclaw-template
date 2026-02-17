# PENDING.md — All Pending Tasks

**Purpose:** Single source of truth untuk semua pending tasks (urgent → long-term)

**Last updated:** 2026-02-17 13:57 WIB

---

## 🔥 Urgent (This Week)

### 0. BUILD mart.sto_analysis table ✅ COMPLETED
- **Status:** ✅ DONE — 60,602 rows, 155 stores, 699 articles
- **Source:** SQL `/tmp/create_mart_sto.sql` → direct psql execution
- **Schema:** store_name, kode, size, product_name, series, gender, qty_m3/m2/m1, qty_3m, avg_monthly, current_stock, turnover, snapshot_date
- **Filter:** Exclude wholesale, konsinyasi, pusat, wilbex, imbex, merchandise, HO, bazar, event, pameran
- **Function:** `mart.rebuild_sto_analysis()` created (for weekly cron)
- **Deployed:** Powering zuma-sto-jatim.vercel.app v2

### 1. Upload iSeller data (2024, 2025, 2026)
- **Status:** Waiting for Wayan's download to complete
- **Action:** Upload ke PostgreSQL (raw schema or new table)
- **Who:** Iris (Mac mini or delegate to opencode)
- **Timeline:** As soon as files ready

### 2. Monitor Atlas report generation (2026-02-17)
- **Status:** Monitoring now (every 1-min heartbeat)
- **Expected:** `/root/.openclaw/workspace-ops/logs-report-for-iris/2026-02-17_atlas-report.json`
- **Timeline:** Within 5-10 min from HEARTBEAT.md setup (07:11)
- **Action:** Report to Wayan when confirmed

### 3. Create SO L2 SKILL.md (retroactive documentation)
- **Status:** Script LIVE ✅, skill doc MISSING ⚠️
- **Location:** `zuma-business-skills/ops/zuma-inventory-control/zuma-so-l2-skills/SKILL.md`
- **Why:** Dual-component pattern (automation + documentation for on-the-fly generation)
- **Who:** Iris (write SKILL.md based on existing script + knowledge doc)
- **Timeline:** This week

---

## 📊 Medium-Term (This Month)

### Branch Manager Deck System — ALL BRANCHES ✅ JATIM DONE
- **Status Jatim:** COMPLETE (11 slides + STO tool)
- **URL:** https://zuma-bm-jatim.vercel.app + https://zuma-sto-jatim.vercel.app
- **Next:** Build Bali, Jakarta, Sumatra, Sulawesi, Batam
- **Prereq:** mart.sto_analysis table (see urgent #0 above)
- **Workflow:** Add branch to config.py → build HTML → push zuma-bm-decks → deploy Vercel
- **OLD STATUS WAS:** Discussion done, blocked on 2 data gaps
- **Structure agreed (7 slides):**
  1. Branch Scorecard (revenue, YoY, # stores, avg FF/FA/FS)
  2. Store ABC (ranking + YoY per store)
  3. Product Mix Jatim (top articles, vs nasional)
  4. Stock & Planogram Health (FF/FA/FS per store, color-coded)
  5. MoM Trend (Jan vs Feb trajectory)
  6. Jatim vs Nasional benchmark
  7. 3 Action Items
- **Blocked on:**
  - [ ] **Monthly target per store dari Finance** — Wayan cariin (needed for achievement % vs target)
  - [ ] **Branch mapping fix** — portal.store JOIN timeout, needs index/materialized view
- **When unblocked:** build Jatim dulu, lalu replicate ke semua cabang
- **Note:** Tanpa target data, sementara pakai YoY sebagai proxy

### 4. Five Automation Reports — Script + SKILL.md each

**Pattern:** Each needs TWO components:
1. Python wrapper script (cron automation)
2. SKILL.md documentation (on-the-fly generation capability)

**Reference:** `inbox/pending-tasks-automation-reports.md` for detailed specs

#### A. Control Stock Report
- **Purpose:** Stock control metrics & alerts
- **Table:** `mart.control_stock_daily` (TBD schema)
- **Status:** Planning stage (query design needed)

#### B. Planogram Report
- **Purpose:** Planogram compliance & fill rate
- **Table:** `mart.planogram_daily` (TBD schema, may overlap with FF/FA/FS)
- **Status:** Planning stage (query design needed)

#### C. RO Report (Box & Protol)
- **Purpose:** Replenishment Order status & fulfillment
- **Table:** `mart.ro_box_protol_daily` (TBD schema)
- **Status:** Planning stage (query design needed)

#### D. Surplus Store Report
- **Purpose:** Store surplus inventory for redistribution
- **Table:** `mart.surplus_store_daily` (TBD schema, related to Distribution Flow v3)
- **Status:** Planning stage (query design needed)

#### E. SKU Analysis Report (R&D/Apollo territory)
- **Purpose:** SKU performance analysis untuk Product Development decisions
- **Table:** `mart.sku_analysis` (flat structure, TBD)
- **Key users:** Mbak Dewi (R&D Manager), Mbak Desyta (SPV ProdDev), Yuda, Apollo
- **Priority:** Medium-High (strategic data)
- **Status:** Planning stage (schema design needed)
- **Note:** SKILL.md MANDATORY for Apollo (ad-hoc analysis capability)

**Next steps:**
1. Define SQL queries for each report (collaborate with Wayan)
2. Test queries on mart/core tables
3. Write Python wrappers + SKILL.md docs
4. Deploy to VPS cron + add to Atlas monitoring

---

## 🔧 Operational Improvements (This Quarter)

### 7. Fix Branch-level Filtered Deck (portal.store JOIN timeout)
- **Problem:** `portal.store` JOIN dengan ILIKE selalu timeout — blocks branch-specific analysis
- **Solution:** Create indexed materialized view or use exact match instead of ILIKE
- **Impact:** Enables Branch Manager deck (per-cabang filtered analysis)
- **Who:** Iris (opencode)
- **Timeline:** Before next branch manager request

### 8. Channel Split Analysis Query Pattern
- **Goal:** Clean separation: DDD=retail, MBB=online/marketplace, UBB=wholesale
- **Use case:** Channel overview deck for CEO/GM, BusDev
- **Action:** Test entity-based channel split query, document pattern in SKILL.md
- **Who:** Iris
- **Timeline:** TBD (lower priority until Finance data available)

### 9. Finance Role Data — COGS / Gross Margin from Accurate
- **Blocker:** No COGS/margin data in DB — Finance deck (Contribution Margin) can't be built yet
- **Action:** Coordinate with Wayan when Accurate margin data becomes available
- **Impact:** Unlocks Finance role deck + proper profitability analysis
- **Who:** Wayan (data source) + Iris (implementation)
- **Timeline:** TBD (data dependency)

### 5. Tim SI Coordination — SO Level 1 Manual Input
- **Task:** Coordinate dengan Tim SI soal kolom "fisik" di SO Level 1 AppSheet
- **Context:** Manual entry via AppSheet, bukan automated
- **Action items:**
  - [ ] Identify PIC di Tim SI (who manages SO Level 1 AppSheet?)
  - [ ] Confirm current process (frequency, coverage, pain points)
  - [ ] Discuss sustainability of manual entry
  - [ ] Propose improvements (automation potential, validation rules)
- **Who:** Iris coordinate with Wayan, then reach out to Tim SI PIC
- **Timeline:** TBD (coordinate with Wayan)

### 6. Official WhatsApp API Setup
- **Purpose:** Migrate Iris to official WhatsApp Business API (dedicated number)
- **Current:** Using personal WhatsApp (relay-based)
- **Target:** Official API for reliability, scalability, business features
- **Steps:**
  - [ ] Beli kartu perdana baru (Telkomsel/XL/Indosat)
  - [ ] Register number
  - [ ] Setup Official WhatsApp Business API (via Facebook Business Manager)
  - [ ] Migrate gateway config to official number
  - [ ] Test end-to-end
- **Who:** Wayan (purchase SIM) + Iris (setup API)
- **Priority:** Medium (not urgent, but good to plan ahead)
- **Timeline:** Q1 2026

---

## 📝 Notes

- **HEARTBEAT.md:** For urgent/same-day tasks requiring active monitoring
- **PENDING.md:** Full backlog (urgent + medium + long-term)
- **inbox/*.md:** Detailed planning docs, reference from PENDING.md when needed
- **Review frequency:** Weekly (clean up completed tasks, reprioritize)

**Reminder:** When tasks move from PENDING → HEARTBEAT (becomes urgent), remove from PENDING to avoid duplication.
