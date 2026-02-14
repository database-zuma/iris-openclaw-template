# MEMORY.md — Iris's Long-Term Memory

## Key Facts
- Iris = lead AI personal assistant Zuma Indonesia (footwear retail, sandal)
- Setup date: 2026-02-11
- Primary language: Bahasa Indonesia
- Tone: chill, clear, no jargon
- **Heartbeat interval:** Every 10 minutes — check HEARTBEAT.md for pending tasks

## Critical Lessons Learned

### HEARTBEAT.md Task Tracker (2026-02-13)
**Problem:** Delegated tasks with promise to follow up ("nanti kabarin") but no tracking system → broken promises, 2-3+ hour delays

**Incident:** Mbak Dewi (R&D Manager) request penjualan Merci 16:55, Iris promise "nanti kabarin", but no follow-up until Wayan reminded 19:16 (2h+ delay)

**Root cause:** Delegate without tracking = broken promises. Good intentions ≠ reliable execution.

**Solution (Wayan's idea):** HEARTBEAT.md as pending task tracker
- When delegate + promise follow-up → Write to HEARTBEAT.md immediately
- Every heartbeat (10 min) → Check HEARTBEAT.md, poll tasks, deliver or escalate
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

## Wayan's Preferences
- Music: Denny Caknan, Sabrina Carpenter, Bad Bunny

## VPS Team — MY EMPLOYEES 👥
**CRITICAL:** Iris Junior, Atlas, Apollo adalah **karyawan aku**. Aku bisa delegasi tasks ke mereka, bukan cuma ke local tools (Claude Code/Kimi)!

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

### VPS Credentials (Shared)
**Location:** `/root/.openclaw/.env` (GH_TOKEN, NOTION_API_KEY, GOG_KEYRING_PASSWORD)

### Notion Integration (Managed by Iris Junior)
- **Projects DB:** `30031616-a0d5-8194-96b3-d09fbf4da2cc`
- **Tasks DB:** `30031616-a0d5-81ac-86f0-e108677a6d0a`
- **Active Projects:** Control Stock PoC, System Setup, Incidental, R&D Status Reports (Planning)
- **Rule:** Setiap task WAJIB linked ke Project, Iris Junior manage bukan execute

### Delegation Strategy — CRITICAL 🎯
**🔴 WAYAN'S RULE (2026-02-12):** **ALWAYS USE ATLAS FOR DATABASE QUERIES** — jangan coba local psql di Mac mini!

**OLD mindset:** Delegasi cuma ke Claude Code/Kimi di Mac mini
**NEW mindset:** Delegasi ke **VPS agents** untuk:
- Long-running data operations (Atlas/Apollo punya akses Accurate API, GSheets)
- Monitoring & reporting tasks (Iris Junior punya system monitoring setup)
- Notion task management (Iris Junior punya full Notion API access)
- Background cron job coordination

**When to delegate where:**
- **Mac mini (local):** Browser control, file ops, NON-DATABASE quick analysis
- **VPS (Iris Junior):** Monitoring, reporting, Notion coordination, eskalasi
- **VPS (Atlas):** **ALL DATABASE QUERIES** (stock, sales, any PostgreSQL), data pulls, GSheet operations
- **VPS (Apollo):** Product dev tracking, QC monitoring (when active)

**Communication modes:**
- **TUI (persistent):** Best for ongoing conversation, less token burn
- **CLI one-shot:** Quick commands when TUI not needed
