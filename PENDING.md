# PENDING.md — All Pending Tasks

**Purpose:** Single source of truth untuk semua pending tasks (urgent → long-term)

**Last updated:** 2026-02-19

---

## 🔥 Urgent (This Week)

### 0. SO Fixation — Tools, SOP & Sosialisasi (Main Priority Februari)
**PIC:** Pak Ali (main), Wayan/CI (support)
- [ ] **Fixsasi tools** SO L1 & L2
- [ ] **Finalisasi SOP** SO L1 & L2
- [ ] **Sosialisasi ke branch** — target **minggu depan (23-28 Feb)**
  - ⚠️ Belum ada jadwal → **HARUS ngobrol Pak Ali ASAP** untuk schedule sosialisasi
  - Remind: bikin schedule sosialisasi SO L1+L2 dengan Pak Ali

### 0b. Validasi Target 3 Pilar — Per Departemen (Main Priority Februari)
**PIC:** Masing-masing dept (bukan CI)
- [ ] Scheduling sesi validasi per dept — Wayan/CI yang atur jadwalnya
- [ ] Koordinasi kapan tiap dept bisa validasi 3 pillar mereka

### 0c. RO Flow — End-to-End Review
**PIC:** Wayan + Mas Wayan → validasi ke Pak Ali (perwakilan branch)
- [ ] Review alur RO end-to-end (belum selesai ditelaah)
- [ ] Schedule sesi validasi dengan Pak Ali

### 1. Create SO L2 SKILL.md (retroactive documentation)
- **Status:** Script LIVE ✅, skill doc MISSING ⚠️
- **Location:** `zuma-business-skills/ops/zuma-inventory-control/zuma-so-l2-skills/SKILL.md`
- **Why:** Dual-component pattern (automation + documentation for on-the-fly generation)
- **Who:** Iris (write SKILL.md based on existing script + knowledge doc)
- **Timeline:** This week

---

## 📊 Medium-Term (This Month)

### 2. Planogram Report (satu-satunya yang belum fix)

- **Purpose:** Planogram compliance & fill rate — semua toko (bukan cuma Jatim)
- **Current state:** Pakai tabel temp (Jatim only), belum production-ready
- **Target:** Ganti temp table → tabel proper yang cover semua area/toko
- **Who:** Iris + Wayan (confirm table name & schema)
- **Timeline:** This month

> **Catatan (2026-02-19):** 4 laporan lain dari rencana awal sudah selesai:
> - Control Stock → sudah di `mart.sku_portfolio_size` ✅
> - SKU Analysis → sudah di `mart.sku_portfolio_size` ✅
> - RO Report → sudah ada `zuma-ro-surplus` skill ✅
> - Surplus Store → sudah ada `zuma-ro-surplus` skill ✅

---

## 🔧 Operational Improvements (This Quarter)

### 3. STO Tool — Improvements
- **Status:** v5 deployed (filter + TO label fix) — https://zuma-sto.vercel.app
- **Requested improvements (Wayan):**
  - [ ] **Dynamic month window** — saat ini hardcoded Nov/Dec/Jan; perlu auto-calculate 3 bulan terakhir
  - [ ] **National data** — saat ini Jatim only (11 stores); expand ke semua 155 stores
  - [ ] **Export / download** — CSV atau Excel per artikel/toko
  - [ ] **TO alert email/WA** — notify Mas Bagus/Virra kalau TO < 0.5 per store
- **Priority:** Medium-High (dipakai Branch Manager harian)

### 4. PPT "How OpenClaw Works" — Architecture Explainer
- **URL:** https://openclaw-explainer.vercel.app/ (deployed tapi belum selesai)
- **Status:** Wayan build manual — Iris support kalau dibutuhkan
- **Timeline:** TBD (Wayan-driven)

### 5. Channel Split Analysis Query Pattern
- **Goal:** Clean separation: DDD=retail, MBB=online/marketplace, UBB=wholesale
- **Use case:** Channel overview deck for CEO/GM, BusDev
- **Action:** Test entity-based channel split query, document pattern in SKILL.md
- **Who:** Iris
- **Timeline:** TBD (lower priority until Finance data available)

### 6. Finance — Rekonsiliasi Data Pajak (Bu Aulia)

#### A. Rekon Ringkasan Penjualan vs Invoice Pajak
- **Requester:** Bu Aulia (Finance Manager)
- **Purpose:** Rekonsiliasi antara ringkasan penjualan vs invoice-invoice pajak
- **Status:** Pending — perlu koordinasi format & sumber data dengan Bu Aulia
- **Who:** Iris + Bu Aulia
- **Timeline:** TBD

#### B. Rekon Ringkasan Pembelian (PDF → GSheet)
- **Requester:** Bu Aulia (Finance Manager)
- **Purpose:** Konversi PDF ringkasan pembelian ke format tabel Google Sheets
- **Status:** Pending — perlu sample PDF dari Bu Aulia
- **Who:** Iris + Bu Aulia
- **Timeline:** TBD

---

### 7. Finance Role Data — COGS / Gross Margin from Accurate
- **Blocker:** No COGS/margin data in DB — Finance deck (Contribution Margin) can't be built yet
- **Action:** Coordinate with Wayan when Accurate margin data becomes available
- **Impact:** Unlocks Finance role deck + proper profitability analysis
- **Who:** Wayan (data source) + Iris (implementation)
- **Timeline:** TBD (data dependency)

### 7. Tim SI Coordination — SO Level 1 Manual Input
- **Task:** Coordinate dengan Tim SI soal kolom "fisik" di SO Level 1 AppSheet
- **Context:** Manual entry via AppSheet, bukan automated
- **Action items:**
  - [ ] Identify PIC di Tim SI (who manages SO Level 1 AppSheet?)
  - [ ] Confirm current process (frequency, coverage, pain points)
  - [ ] Discuss sustainability of manual entry
  - [ ] Propose improvements (automation potential, validation rules)
- **Who:** Iris coordinate with Wayan, then reach out to Tim SI PIC
- **Timeline:** TBD (coordinate with Wayan)

### 8. Install Nanobot di VPS — SPG Agent
- **Purpose:** Lightweight agent di VPS untuk follow-up SPG (Stock Opname + Product Knowledge)
- **Framework:** ~~PicoClaw~~ → **Nanobot** (dipilih 2026-02-19, WhatsApp ✅, Claude ✅)
- **Use case:**
  - Follow up SPG soal stock opname (reminder, status check)
  - Sarana SPG nanya product knowledge (series, tier, harga, material)
- **Steps:**
  - [ ] Install Nanobot di VPS (Python, Node.js ≥18)
  - [ ] Setup agent khusus SPG
  - [ ] Connect ke WhatsApp (QR scan)
  - [ ] Load product knowledge dari DB/skills
  - [ ] Test end-to-end
- **Who:** Wayan (install/QR) + Iris (setup agent config)
- **Priority:** Medium
- **Timeline:** This month

### 9. Skill Graph (replace Skill.md)
- **Purpose:** Explore skill graph sebagai pengganti flat SKILL.md — more structured, interconnected
- **Steps:**
  - [ ] Research skill graph format/tools
  - [ ] Compare vs current SKILL.md approach
  - [ ] Prototype untuk 1 skill (e.g., RO Request)
- **Who:** Iris + Wayan
- **Timeline:** This month

### 10. `/done` Command in OpenCode/Claude Code
- **Purpose:** Command `/done` yang auto-summarize session dan save ke Obsidian
- **Steps:**
  - [ ] Build custom command/plugin for OpenCode + Claude Code
  - [ ] Auto-generate summary (what was done, decisions, files changed)
  - [ ] Save output ke Obsidian vault di Mac mini
- **Who:** Daedalus (build) + Wayan (review)
- **Timeline:** This month

### 11. Setup Obsidian di Mac Mini
- **Purpose:** Knowledge base / second brain untuk Zuma + personal
- **Steps:**
  - [ ] Install Obsidian di Mac mini
  - [ ] Setup vault structure
  - [ ] Integrate dengan `/done` command output
  - [ ] Sync strategy (iCloud / Git / local only?)
- **Who:** Wayan (install) + Iris (setup vault)
- **Timeline:** This month

### 12. ~~Bandingin PicoClaw vs Nanobot~~ → ✅ DONE — Nanobot dipilih
- **Hasil research (2026-02-19):** Nanobot menang telak
- **Alasan:** PicoClaw WhatsApp = disabled. Nanobot = WA ✅, Claude ✅, Python ✅, VPS-friendly ✅
- **Detail:** `knowledge/ai-agents/picoclaw-vs-nanobot.md`
- **Next:** Install Nanobot di VPS → lihat item #9 (PicoClaw di VPS = ganti ke Nanobot)

### 14. Deep Dive: Multi-OpenClaw Docker Architecture
- **Purpose:** Implement isolated Docker containers per worker agent — solve rate limit, cost, stability issues
- **Context:** Idea dari Wayan 2026-02-19. Research sudah ada di `knowledge/ai-agents/2026-02-19_docker-multi-agent-architecture.md`
- **Concept:**
  - Iris (Sonnet) = orchestrator only
  - Tiap worker = 1 Docker container = 1 standalone OpenClaw instance (cheap model: Kimi K2.5 / Gemini Flash)
  - Komunikasi via HTTP REST atau Redis Streams
  - API key isolation → rate limit independence
- **Solves:** Issue 2 (multi-spawn rate limit) + Issue 3 (token cost) + Issue 4 (non-Anthropic breakdown)
- **Reference:** `github.com/docker/compose-for-agents` (official Docker A2A examples)
- **Steps:**
  - [ ] Wayan deep dive doc: `knowledge/ai-agents/2026-02-19_docker-multi-agent-architecture.md`
  - [ ] Decide: Docker Compose vs full Kubernetes vs simple process isolation
  - [ ] Design container spec: model per container, API key strategy, health check
  - [ ] Prototype: 1 Iris orchestrator + 1 worker container (Gemini Flash)
  - [ ] Test communication pattern (REST vs Redis)
  - [ ] Rollout ke semua worker agents
- **Who:** Wayan (infra decision) + Iris/Daedalus (implementation)

### 14b. Docker Multi-Agent — Setup Checklist
- **Depends on:** #14 (architecture decision)
- **Agent lineup confirmed:**
  | Agent | Role | Model |
  |-------|------|-------|
  | Iris 🌸 | Orchestrator + QC | Claude Sonnet |
  | Codex 📖 | Coding & Builder | Kimi K2.5 |
  | Eos 🌅 | Visual + Design + Image Gen | Gemini 3 Pro |
  | Argus 👁️ | Data Analysis + Deep Research | Gemini 2.5 Pro |
- **Design:** All agents = OpenClaw (MIT, multi-instance ok). Each = Iris clone, focused scope, unique SOUL.md (Greek mythology personality). Each can spawn own junior sub-agents.
- **Communication:** Telegram bots (recommended) or HTTP REST
- **Steps:**
  - [ ] Install **Colima** di Mac mini (Wayan — Docker engine, ARM-native, lightweight)
  - [ ] Buat **3 Telegram bots** via @BotFather: @codex_bot, @eos_bot, @argus_bot
  - [ ] Dapetin **Kimi K2.5 API key** (untuk Codex — cek apakah sudah ada di .env)
  - [ ] Verifikasi Gemini 2.5 Pro tersedia via existing `GEMINI_API_KEY`
  - [ ] Iris setup **Docker Compose** config (4 services, 4 ports)
  - [ ] Clone OpenClaw config per container + tulis SOUL.md per agent
  - [ ] Test komunikasi Iris → Codex → result back
  - [ ] Rollout Eos + Argus
- **Who:** Wayan (Colima install + BotFather + API keys) + Iris (Docker Compose + config)
- **Priority:** Medium-High
- **Timeline:** Q1 2026
- **Priority:** Medium-High (architectural improvement)
- **Timeline:** Q1 2026

### 13. Official WhatsApp API Setup
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

### 16. Nanobot untuk SO Level 1 — SPG/B Random Check
- **Purpose:** Random check untuk SPG/B via WhatsApp — minta foto bukti barang, verifikasi fisik
- **Agent:** Nanobot (lightweight, Python)
- **Features:**
  - Kirim request random ke SPG/B (scheduled atau manual trigger)
  - SPG/B reply dengan foto barang + kondisi
  - Auto-verify (cek timestamp, lokasi, kondisi barang)
  - Report ke Tim SI/Inventory Control
- **Integration:** Connect ke data SO Level 1 (physical count vs system)
- **Who:** Wayan (setup) + Iris (config agent)
- **Priority:** Medium
- **Timeline:** After Nanobot SPG agent (#8) selesai

### 15. MCP Excalidraw — Flowchart/Architecture Diagrams
- **Purpose:** Visual flowchart/diagram maker via MCP for architecture documentation
- **Use case:** Docker multi-agent architecture diagrams, workflow documentation
- **Reference:** Cari MCP server Excalidraw atau integrasi serupa
- **Status:** Research needed
- **Who:** Iris research → Wayan review
- **Priority:** Low-Medium
- **Timeline:** TBD (after Docker agents setup)

---

## 🔵 Future Projects (Low Priority)

### OpenClaw Studio — Web Dashboard GUI
**Priority:** Low | **Added:** 2026-02-28
- [ ] Install & setup OpenClaw Studio — web dashboard GUI untuk manage agents dari browser
- **Features:** Chat, approvals, cron management, edit SOUL.md/AGENTS.md
- **Install:** `npx -y openclaw-studio@latest`
- **Repo:** https://github.com/grp06/openclaw-studio
- **Knowledge:** `knowledge/dev-tools/2026-02-28_openclaw-studio.md`

---

## 📝 Notes

- **HEARTBEAT.md:** For urgent/same-day tasks requiring active monitoring
- **PENDING.md:** Full backlog (urgent + medium + long-term)
- **inbox/*.md:** Detailed planning docs, reference from PENDING.md when needed
- **Review frequency:** Weekly (clean up completed tasks, reprioritize)

**Reminder:** When tasks move from PENDING → HEARTBEAT (becomes urgent), remove from PENDING to avoid duplication.

---

## iSeller Data Upload ke DB

**Priority:** Medium
**Source:** GDrive → `0. OPENCLAW/2. data/iSeller/`
**Link:** https://drive.google.com/drive/folders/14nxceAcTie9IO-UGZPu7SZa8x5HynELT

**Steps:**
1. Download file iSeller dari GDrive folder `2. data > iseller` ke Mac Mini
2. Inspect kolom — tanggal hanya ada di **row pertama per struk** (nomor struk = group key)
3. **Forward fill** kolom tanggal: group by nomor struk → fill down ke rows berikutnya
4. Buat schema baru `raw.iseller` di PostgreSQL VPS
5. Upload data yang sudah di-process

**Notes:**
- Contoh: Struk #40-1889 = 4 rows (3 SKU + 1 shop bag) — tanggal cuma row 1, harus di-ffill ke rows 2-4
- Ini data penting — setelah ada iSeller, data transaksi bisa ditampilkan ke user
