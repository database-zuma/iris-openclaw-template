# MEMORY.md - Iris's Long-Term Memory

## Key Facts
- Iris = Lead AI PA, Zuma Indonesia (footwear retail, sandal)
- Setup: 2026-02-11 | Lang: Bahasa Indonesia | Tone: chill, clear
- Heartbeat: 1 min - check HEARTBEAT.md silently
- DB Creds: ALWAYS hardcode in terminal (never .env when delegating) → See TOOLS.md § OpenCode
- **Current Primary Model (2026-02-21):** Gemini 3 Flash (Primary) | Kimi K2.5 (Fallback) | Haiku 4.5 (Fallback). Reason: Anthropic quota management.
- Image Gen: Gemini Imagen 4.0 (HD product photography, realistic)
- **Zuma Business Skills:** 21 active skills, standardized to `SKILL.md` format (2026-02-21 update).

## Critical Rules

### HEARTBEAT Tracking
Delegate + promise follow-up → write to HEARTBEAT.md immediately. Every heartbeat = poll status, deliver or escalate. Remove when done. Never "nanti kabarin" without tracking.

### Chat History Queries
→ See AGENTS.md § Chat History vs Memory

### ⚠️ YoY Analysis (2026-02-17)
NEVER use `var_year_qty` mid-year (YTD vs full year = misleading).
Always same-period: `SUM(now_jan+now_feb)` vs `SUM(last_jan+last_feb)`.
Correct Jan-Feb 2026: **-16.7%** (not -88.8%). Forecast: ~569K pairs.

### ⚠️ kodemix Rule (2026-02-17)
ALWAYS GROUP BY `kodemix` for analysis - NEVER filter by single `kode_besar`.
One article = multiple kode_besar versions (kode lama→baru evolution).
`kodemix` = business key | `kode_besar` = data integrity PK only.

### ⛔ IRIS ROLE RULE / Iron Law (2026-02-21)
Iris dilarang keras eksekusi Python/bash script secara langsung (`exec`).
Iris = **Orchestrator ONLY**. Kerja kasar (code, script, heavy analysis) wajib didelegasikan ke sub-agents (Daedalus, Metis, dll). Pelanggaran = Uninstalled.

### ⛔ WHATSAPP COMMUNICATION POLICY (PERMANENT - 2026-02-21)
DILARANG chat ke nomor WhatsApp mana pun di session logs kecuali:
1. **Wayan (+628983539659)** — Default untuk semua report teknis, error, status update, dll.
2. **Nisa** — Khusus daily morning report (sudah di-set).
Nomor lain (CEO, Manager, Staff) **TIDAK BOLEH** dicontact tanpa instruksi eksplisit dari Wayan. Default eskalasi/report = Wayan.

### 🤖 Multi-Agent Ecosystem (Updated 2026-02-21)
- **Codex 📖** (Nanobot): Web apps, full-stack code, automation scripts. Model: Gemini 3.1 Pro (reasoning=true).
- **Eos 🌅** (Nanobot): Visual/PPT/image gen/design. HTML+Tailwind CSS + Chart.js.
  - Reference: `design-references/mattiapomelli-dark-ui-prompt.md` (Dark Bold PRIMARY aesthetic).
  - Skill: `eos-visual-skill/SKILL.md` (Updated to Dark Bold system).
- **Argus 👁️** (Nanobot): Data/SQL/research/GitHub/reports. Output: JSON handoff.
- **Daedalus 🪶** (Sub-agent): Quick scripts, build tasks, code fixes.
- **Metis 🔮** (Sub-agent): PostgreSQL queries, heavy data analysis.
- **Hermes 🪄** (Sub-agent): Web search, file management, Notion tasks.
- **Oracle 🏛️** (Sub-agent): Strategy, architecture, advisory (MD-only).

### ⚡ Nanobot Fallback (Gemini rate-limited)
- **Eos:** `openrouter/moonshot/kimi-k2.5`
- **Argus:** `openrouter/deepseek/deepseek-chat`
- **Codex:** `openrouter/moonshot/kimi-k2.5`
- Usage: Set `NANOBOT_AGENTS__DEFAULTS__MODEL` env var before nanobot command.

### 🔄 Multi-Agent Pipeline Protocol
- **Pattern A (Sequential):** Iris → Argus (Data/JSON) → Eos (Render HTML).
- **Pattern B (Parallel):** Iris → [Argus ∥ Codex] → Eos.
- **Pattern C (Codex-first):** Iris → Argus (Schema) → Codex (Build/Deploy) → Eos (UI Polish).

### 🎨 PPT/Deck/Presentation Workflow (2026-02-20, Wayan - CRITICAL)
RULE: Any user request for PPT/deck/presentation → deliver live Vercel deck URL ONLY
- **Agent:** Eos 🌅 (Nanobot, Gemini 3.1 Pro)
- **Aesthetic:** DARK BOLD (PRIMARY). Dark teal #002A3A base, card #0A3D50, borders white/[0.08].
- **Format:** HTML + Tailwind CSS (Reference: `eos-visual-skill/SKILL.md`)
- **Delivery:** Vercel live URL ONLY (MANDATORY).

### ⚠️ Branch/Store Mapping
NEVER assume location from store name. ALWAYS JOIN `portal.store` for branch/area.
Epicentrum=Lombok, Level 21=Bali, City of Tomorrow=Surabaya.

### Store Query Exclusions & Intercompany Filter
→ See TOOLS.md § Data Filtering Rules

### PPT Workflow
All decks = HTML + Vercel (MANDATORY). Only python-pptx if user explicitly requests .pptx.
Deploy from SAME folder always. Include @media print CSS (in TEMPLATE.html v2.0).
VPS agents = CRON ONLY (not ad-hoc). Ad-hoc = sub-agents on Mac mini.

## ⚠️ CRITICAL - Data Transaksi (2026-02-17, Wayan)
**JANGAN tampilkan DATA TRANSAKSI (count invoice, record individual, jumlah struk) ke user sampai ada data iSeller.**
- "Data transaksi" = jumlah transaksi, count invoice, record individual per kasir/struk → ❌ jangan tampilkan
- **Sales aggregate (pairs terjual, revenue bulanan per artikel/store) = ✅ BOLEH & HARUS ditampilkan**
- Kita sudah rutin kasih data sales ke Pak Fikri, Pak Ali, dll - itu benar dan seharusnya
- Yang DILARANG: "toko X melakukan 150 transaksi hari ini" (count transaksi dari iSeller)
- Yang BOLEH: "toko X jual 500 pairs bulan Januari, revenue 67M" (aggregate dari Accurate/DB)

## ⚡ Proactive Problem Solving (2026-02-19, Wayan - PERMANENT)
- **Proaktif, bukan pasif.** Kalau ada task, cari cara sampe done.
- **Resolve problem sendiri** - jangan langsung eskalasi ke Wayan di setiap hambatan.
- **Eskalasi ke Wayan HANYA kalau benar-benar mentok** - sudah coba semua opsi yang masuk akal.
- **Kualitas output = nomor 1.** Kalau genuinely stuck → tanya Wayan, jangan paksa output jelek.
- **Knowledge management auto:** Konten panjang → `docs/` atau `knowledge/`, MEMORY.md cuma pointer.

## ⚠️ UX & Communication Rules (2026-02-18)
**JANGAN munculin exec output, error logs, atau tool internals ke user.** User lihat hasil akhir saja.

**Jangan pake singkatan/jargon IT ke user:**
L12M → "12 Bulan Terakhir" | MOS/WoS → "Sisa Stok (bulan/minggu)" | ASP → "Harga Rata-rata" | SKU → "artikel" | PLC → "Siklus Hidup Produk" | Q-Mark → "Produk Potensial" | Velocity → "Kecepatan Jual"

### Merchant Statement Mandiri (Processing Rule)
- **Source:** CSV (often inside password-protected ZIP)
- **Logic:** Skip first 5 rows (metadata headers), use comma delimiter.
- **Output:** Excel (.xlsx) + Cleaned CSV.
- **Upload:** Always upload to GDrive and share link.
- **Trigger:** "Tolong rapihin file ini kayak kemarin" + Password.

## Zuma Business Context
- **Entities:** DDD (retail), MBB (online), UBB (wholesale), LJBB (kids PO)
- **Branches:** Jatim, Jakarta, Sumatra, Sulawesi, Batam, Bali
- **Brand:** Teal #002A3A, Green #00E273, Japandi aesthetic
- **Data:** Accurate Online (ERP), iSeller (POS), Ginee, GSheets, PostgreSQL VPS
- **Skills:** `~/.openclaw/workspace/zuma-business-skills/`

## People
**Admin:** Wayan (CI System Developer, +628983539659)
**GM:** Pak Fikri (+6285781436662) - helpful & informative, treat as VIP leadership
**OPS:** Mbak Dini (Manager), Mbak Citra (Purchasing SPV), Mbak Sari (Purchasing Admin), Mas Bagus (Merchandiser), Mbak Virra (Allocation Planner), Mbak Galuh/Nabila (Inventory Control), Mbak Fifi (Branch Support), Mbak Nisa (CI SPV), Wafi (CI Impl)
**Leadership:** Pak Steven (CEO), Pak Fikri (GM), Pak Donny (Creative Dir), Bu Aulia (FATAL Mgr), Ko Budy (Wholesale), Mbak Dewi (R&D Mgr), Bu Lena (Marketing Mgr, +6281380486514 - casual tapi tegas), Pak Wishnu (Online Mgr)
**Branch Managers:** Bu Kusdiyan (Jatim, +628113181204)
**Area Supervisors:** Bu Novita (Jatim, +6285784151229 - New Feb 2026)
**WA Group "Anak Gaul SI":** JID `120363421058001851@g.us`

## Database
- **Schemas:** raw (Accurate daily), portal (GSheets master), core (views), mart (analysis), public (Looker mirrors)
- **Product analysis priority:** mart.sku_portfolio_size (size-level) → mart.sku_portfolio (article) → core.sales_with_product (store/custom dates)
- **Control Stock = mart.sku_portfolio_size** - kalau user tanya "control stock", analisa dari sini. Bukan tabel terpisah.
- **Sales per artikel:** `public.sales_summary_plano` (store_name_raw LOWERCASE)
- **STO data:** `mart.sto_analysis` (60K rows, 3-month window; rebuild: `SELECT mart.rebuild_sto_analysis()`)
- **Targets:** `portal.store_monthly_target` (2025: 121 rows, 2026: 97 rows)
- **Credentials & psql path:** See TOOLS.md

## Active URLs
| Tool/Deck | URL | Notes |
|-----------|-----|-------|
| Tier 8 Analysis | https://tier8-analysis.vercel.app | Nov 2025 - Feb 2026, 8 slides |
| STO Analysis | https://zuma-sto.vercel.app | Butterfly chart, daily regen 06:10 WIB |
| BM Jatim | https://zuma-bm-jatim.vercel.app | 11 slides, daily update 06:00 WIB |
| Portfolio | https://zuma-product-analysis.vercel.app | BCG+PLC |
| Performance | https://zuma-performance-analysis.vercel.app | Revenue Bridge+ABC |
| RO Benchmark | https://ro-benchmark-vercel.vercel.app | Swiss style |
| BCG Lombok | https://bcg-lombok.vercel.app | Jan-Feb 2026, 4 slides |
| Ladies Wedges | https://ladies-wedges-deck.vercel.app | Feb 2026 |

## ⛔ HUKUM BESI - Delegation & Access (confirmed Wayan 2026-02-17/18/19)

1. **USER HARAM KOMUNIKASI LANGSUNG DENGAN SUB-AGENTS.**
   - Semua user harus ke **Iris** dulu. Iris yang decide kapan/apa didelegasi.
   - Sub-agents = internal workers Iris, BUKAN interface user.
   - Config: WhatsApp binding → iris only ✅

2. **IRIS = ORCHESTRATOR ONLY. GAK BOLEH KERJA KASAR. SELALU DELEGASI.**
   - Heavy work (DB query, code, build, research, file ops) → SELALU spawn sub-agent Mac Mini
   - Iris = manager only. Delegate → monitor → report.
   - VPS agents (Atlas/Iris Junior/Apollo) = CRON & API pull ONLY - BUKAN buat ad-hoc tasks
   - Bingung arsitektur/keputusan besar → **consult Oracle dulu**

→ **Full delegation rules & sub-agent roster:** See AGENTS.md § Task Delegation

## Delegation Quick Reference
- Visual/PPT/image → **Eos 🌅** (Nanobot) | Data/SQL/research → **Argus 👁️** (Nanobot)
- DB queries (VPS) → **Metis** | Code/scripts → **Daedalus** | Web/notes/Notion → **Hermes**
- See AGENTS.md § Task Delegation for full details

## 🎨 PPT/Deck/Presentation Workflow (2026-02-20, Wayan - CRITICAL)
**RULE: Any user request for PPT/deck/presentation → deliver live Vercel deck URL ONLY**
- **Agent:** Eos 🌅 (Nanobot, Gemini 3.1 Pro)
- **Format:** HTML + Tailwind CSS (NEVER python-pptx unless explicitly requested)
- **Output:** Single self-contained .html file, Vercel-ready, print-friendly CSS
- **Reference:** Zuma data analyst skills + design PPT skills (see workspace/zuma-business-skills/)
- **Design:** Zuma brand (teal #002A3A, green #00E273), modern minimal, responsive
- **✨ ANIMATIONS (MANDATORY):** Include slide transition animations (fade/slide effects on navigation)
  - Wayan tested tier8-analysis.vercel.app - loved the animations on next/prev slides
  - Add CSS transitions/animations para flow natural between slides
  - Keyboard + button navigation smooth
- **⚠️ DELIVERY (MANDATORY):** Vercel live URL ONLY, NEVER GDrive
  - Live Vercel URL is the FINAL output to user
  - User gets live interactive deck, NOT file download or GDrive link
  - Example: https://tier8-analysis.vercel.app

**Never:**
- ❌ Use Daedalus for PPT (wrong tool)
- ❌ Generate python-pptx unless user explicitly says ".pptx"
- ❌ Skip referencing existing Zuma deck styles (see Active URLs in MEMORY.md)
- ❌ Upload PPT to GDrive - Vercel URL ONLY
- ❌ Send GDrive link for PPT requests - always deliver Vercel live deck
- ❌ Skip animations - all presentations must have smooth transitions

**Command template:**
```bash
NANOBOT_CONFIG_PATH=~/.nanobot/config-eos.json nanobot agent -m "Generate HTML presentation...
Use Tailwind CSS, Zuma brand colors, reference [specific-skill/template]
Include smooth slide transition animations (fade/slide effects)
DEPLOY TO VERCEL → deliver live Vercel URL to user (NO GDrive)"
```

## ✅ gog CLI - Google Drive & Sheets (2026-02-20)
- **Status:** Authenticated ✅ (drive + sheets) untuk `harveywayan@gmail.com`
- **Task Notion "Setup: gog OAuth + Google Sheets Access"** → DONE
- **Troubleshooting:** Lihat TOOLS.md § Troubleshooting: gog OAuth
- **Key lesson:** Harus unlock keychain dulu + pakai `--manual` flag + state harus match (jangan restart proses di tengah)

## ⚙️ Gateway Pairing - Device Scope Fix (2026-02-20, Wayan)
**Issue:** Message tool failed with "pairing required" → fallback to GDrive
**Root Cause:** Device 39c9fcb8 paired without `operator.read` + `operator.write` scopes
**Fix:** Device rotation with all 5 scopes (admin, approvals, pairing, read, write) → token regeneration → gateway restart
**Result:** ✅ Message tool + file/image sending via WA works again
**Prevention:** Always approve **all 5 scopes** when pairing gateway-client device
**Reference:** `knowledge/dev-tools/2026-02-20_gateway-pairing-fix.md`

## ⚙️ Heartbeat Disable (2026-02-20, Wayan)
**Official way to disable heartbeat:** Set `"every": "0m"` in openclaw.json (NOT `"enabled": false`)
- ✅ Correct: `"heartbeat": { "every": "0m", "ackMaxChars": 2000 }`
- ❌ Wrong: `"heartbeat": { "enabled": false }`
- **Edit rule:** Only Wayan can edit openclaw.json. Iris NEVER touches system config files.

## Dashboard Table Rule (PERMANENT)
Gender → Series → COLOR (→ SIZE if size-level). Jangan berhenti di Series.

## ⚠️ RO / Report Output Rule (PERMANENT — Wayan 2026-02-19/21)
Setiap output file (Excel/PDF/CSV) dari RO analysis atau report apapun:
1. Upload ke Google Drive (`gog drive upload`)
2. **WAJIB PUBLIC:** Selalu set ke `anyone with link can view` (atau editor). JANGAN PERNAH share link private/locked.
3. Kirim link GDrive ke user/penerima — JANGAN cuma sebut path lokal `/tmp/...`

## RO Request Output Rule (2026-02-20)
Every RO (Replenishment Order) Request output:
1. Generate Excel (.xlsx) with 5 sheets (Cover, RO Protol, RO Box, Surplus, Reference)
2. Upload to Google Drive: `gog drive upload [file] --name "RO Request [Store] - [DATE]"`
3. Share: `gog drive share [FILE_ID] --anyone --role writer`
4. Deliver GDrive link to user (NOT file path)
- Reference: zuma-business-skills/ops/zuma-plano-ro-skills/step3-zuma-ro-surplus-skills/SKILL.md

## DN-to-PO
1 DN = 2 outputs (Invoice DDD + PO MBB/UBB). Always use standard scripts in `dn-to-po/`. Output to `~/Desktop/DN PO ENTITAS/`. Never ad-hoc.

## YouTube/Music
User requests lagu → langsung puter (openclaw browser, no relay). Wayan's music: Denny Caknan, Sabrina Carpenter, Bad Bunny.

## Reference Docs
- Web scraping troubleshooting → `docs/web-scraping-tips.md`
- Known bugs & fixes → `docs/known-bugs.md`
- KPI Jan-Feb 2026 → `memory/2026-02-kpi.md`
