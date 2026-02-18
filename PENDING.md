# PENDING.md — All Pending Tasks

**Purpose:** Single source of truth untuk semua pending tasks (urgent → long-term)

**Last updated:** 2026-02-19

---

## 🔥 Urgent (This Week)

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

---

## 📝 Notes

- **HEARTBEAT.md:** For urgent/same-day tasks requiring active monitoring
- **PENDING.md:** Full backlog (urgent + medium + long-term)
- **inbox/*.md:** Detailed planning docs, reference from PENDING.md when needed
- **Review frequency:** Weekly (clean up completed tasks, reprioritize)

**Reminder:** When tasks move from PENDING → HEARTBEAT (becomes urgent), remove from PENDING to avoid duplication.
