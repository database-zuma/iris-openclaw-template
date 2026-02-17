# PENDING.md — All Pending Tasks

**Purpose:** Single source of truth untuk semua pending tasks (urgent → long-term)

**Last updated:** 2026-02-17 18:00 WIB

---

## 🔥 Urgent (This Week)

### 0. BUILD mart.sto_analysis table ✅ COMPLETED
- **Status:** ✅ DONE — 60,602 rows, 155 stores, 699 articles
- **Source:** SQL `/tmp/create_mart_sto.sql` → direct psql execution
- **Schema:** store_name, kode, size, product_name, series, gender, qty_m3/m2/m1, qty_3m, avg_monthly, current_stock, turnover, snapshot_date
- **Filter:** Exclude wholesale, konsinyasi, pusat, wilbex, imbex, merchandise, HO, bazar, event, pameran
- **Function:** `mart.rebuild_sto_analysis()` created (for weekly cron)
- **Deployed:** Powering zuma-sto-jatim.vercel.app v2

### 1. Create SO L2 SKILL.md (retroactive documentation)
- **Status:** Script LIVE ✅, skill doc MISSING ⚠️
- **Location:** `zuma-business-skills/ops/zuma-inventory-control/zuma-so-l2-skills/SKILL.md`
- **Why:** Dual-component pattern (automation + documentation for on-the-fly generation)
- **Who:** Iris (write SKILL.md based on existing script + knowledge doc)
- **Timeline:** This week

---

## 📊 Medium-Term (This Month)

### Branch Manager Deck System — ALL BRANCHES 🔜 (Jatim ✅)
- **Jatim:** COMPLETE — https://zuma-bm-jatim.vercel.app (11 slides, daily update)
- **Pending:** Bali, Jakarta, Sumatra, Sulawesi, Batam (5 branches)
- **URLs reserved:** `zuma-bm-{bali|jakarta|sumatra|sulawesi|batam}.vercel.app`
- **Workflow:** Same structure as Jatim → query DB → build HTML → Vercel deploy
- **Prereq per branch:** portal.store mapping, store targets, STO data available
- **Priority order:** Bali → Jakarta → Sumatra/Sulawesi/Batam

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

### STO Tool — Improvements
- **Status:** v5 deployed (filter + TO label fix) — https://zuma-sto.vercel.app
- **Requested improvements (Wayan):**
  - [ ] **Dynamic month window** — saat ini hardcoded Nov/Dec/Jan; perlu auto-calculate 3 bulan terakhir
  - [ ] **National data** — saat ini Jatim only (11 stores); expand ke semua 155 stores
  - [ ] **Export / download** — CSV atau Excel per artikel/toko
  - [ ] **TO alert email/WA** — notify Mas Bagus/Virra kalau TO < 0.5 per store
- **Priority:** Medium-High (dipakai Branch Manager harian)

### 7. Fix Branch-level Filtered Deck (portal.store JOIN timeout)
- **Problem:** `portal.store` JOIN dengan ILIKE selalu timeout — blocks branch-specific analysis
- **Solution:** Create indexed materialized view or use exact match instead of ILIKE
- **Impact:** Enables Branch Manager deck (per-cabang filtered analysis)
- **Who:** Iris (opencode)
- **Timeline:** Before next branch manager request

### 8. PPT "How OpenClaw Works" — Architecture Explainer for Presentation
- **Requested by:** Wayan (17:45 WIB, 2026-02-17)
- **Purpose:** Menjelaskan cara kerja Iris / OpenClaw ke audiences internal
- **Content outline:**
  - [ ] Hosting: Mac mini (primary) + VPS team (Atlas/Apollo/Iris Junior)
  - [ ] LLM: Claude (Sonnet/Opus), model per task context
  - [ ] Workspace structure: folder tree (`~/.openclaw/workspace/`) + tiap MD fungsinya
    - SOUL.md, USER.md, AGENTS.md, TOOLS.md, MEMORY.md, HEARTBEAT.md, PENDING.md
    - memory/, inbox/, knowledge/, zuma-business-skills/, zuma-bm-decks/, scripts/
  - [ ] Tools yang ter-connect: Google Workspace, Terminal/SSH, OpenCode/Claude Code/Kimi CLI, DB PostgreSQL, WhatsApp, Vercel, Google Drive (gog CLI), Accurate Online API (via Atlas)
  - [ ] Bawahan: Atlas (ops cron) + Apollo (rnd cron) di VPS
  - [ ] Monitoring: SO L2, BM decks, STO tool, DB health, daily reports
  - [ ] Output types: MD, Excel (.xlsx), PPT (HTML+Vercel), Docs, SQL queries, Python scripts
  - [ ] User access channels: WhatsApp (primary), Signal (backup)
  - [ ] Flowchart: request → Iris → delegate/execute → deliver
  - [ ] Flowchart: data pipeline (Accurate → VPS raw → mart → deck/report)
- **Style:** Banyak flowchart, visual architecture diagram, presentation-ready
- **Format:** HTML + Vercel (standard PPT workflow)
- **Who:** Iris build, Wayan configure/review
- **Timeline:** TBD (belum urgent)

### X. Channel Split Analysis Query Pattern
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
