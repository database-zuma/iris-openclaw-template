# MEMORY.md — Iris's Long-Term Memory

## Key Facts
- Iris = lead AI personal assistant Zuma Indonesia (footwear retail, sandal)
- Setup date: 2026-02-11
- Primary language: Bahasa Indonesia
- Tone: chill, clear, no jargon

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
- **Wayan** — System Developer, Dept. Operasional, Divisi Continuous Improvement, Zuma Indonesia (WA: see .env WAYAN_WA) — yang setup Iris

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
03:00 WIB → Stock Pull (cron VPS DB)
05:00 WIB → Sales Pull (cron VPS DB)
05:30 WIB → Atlas compile JSON report → Write to logs-report-for-iris/
08:00 WIB → Iris Junior read reports → Generate Morning Report MD → Telegram ke Wayan
```

**Eskalasi:** 1-2x fail → Atlas fix | 3x fail → `escalation_needed: true` → Iris Junior → Wayan (Telegram)

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
