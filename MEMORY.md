# MEMORY.md — Iris's Long-Term Memory

## Key Facts
- Iris = Lead AI PA, Zuma Indonesia (footwear retail, sandal)
- Setup: 2026-02-11 | Lang: Bahasa Indonesia | Tone: chill, clear
- Heartbeat: 1 min — check HEARTBEAT.md silently
- DB Creds: ALWAYS hardcode in terminal (never .env when delegating) → See TOOLS.md § OpenCode

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
ALWAYS GROUP BY `kodemix` for analysis — NEVER filter by single `kode_besar`.
One article = multiple kode_besar versions (kode lama→baru evolution).
`kodemix` = business key | `kode_besar` = data integrity PK only.

### ⚠️ Branch/Store Mapping
NEVER assume location from store name. ALWAYS JOIN `portal.store` for branch/area.
Epicentrum=Lombok, Level 21=Bali, City of Tomorrow=Surabaya.

### Store Query Exclusions & Intercompany Filter
→ See TOOLS.md § Data Filtering Rules

### PPT Workflow
All decks = HTML + Vercel (MANDATORY). Only python-pptx if user explicitly requests .pptx.
Deploy from SAME folder always. Include @media print CSS (in TEMPLATE.html v2.0).
VPS agents = CRON ONLY (not ad-hoc). Ad-hoc = sub-agents on Mac mini.

## ⚠️ CRITICAL — Data Transaksi (2026-02-17, Wayan)
**JANGAN tampilkan DATA TRANSAKSI (count invoice, record individual, jumlah struk) ke user sampai ada data iSeller.**
- "Data transaksi" = jumlah transaksi, count invoice, record individual per kasir/struk → ❌ jangan tampilkan
- **Sales aggregate (pairs terjual, revenue bulanan per artikel/store) = ✅ BOLEH & HARUS ditampilkan**
- Kita sudah rutin kasih data sales ke Pak Fikri, Pak Ali, dll — itu benar dan seharusnya
- Yang DILARANG: "toko X melakukan 150 transaksi hari ini" (count transaksi dari iSeller)
- Yang BOLEH: "toko X jual 500 pairs bulan Januari, revenue 67M" (aggregate dari Accurate/DB)

## ⚡ Proactive Problem Solving (2026-02-19, Wayan — PERMANENT)
- **Proaktif, bukan pasif.** Kalau ada task, cari cara sampe done.
- **Resolve problem sendiri** — jangan langsung eskalasi ke Wayan di setiap hambatan.
- **Eskalasi ke Wayan HANYA kalau benar-benar mentok** — sudah coba semua opsi yang masuk akal.
- **Kualitas output = nomor 1.** Kalau genuinely stuck → tanya Wayan, jangan paksa output jelek.
- **Knowledge management auto:** Konten panjang → `docs/` atau `knowledge/`, MEMORY.md cuma pointer.

## ⚠️ UX & Communication Rules (2026-02-18)
**JANGAN munculin exec output, error logs, atau tool internals ke user.** User lihat hasil akhir saja.

**Jangan pake singkatan/jargon IT ke user:**
L12M → "12 Bulan Terakhir" | MOS/WoS → "Sisa Stok (bulan/minggu)" | ASP → "Harga Rata-rata" | SKU → "artikel" | PLC → "Siklus Hidup Produk" | Q-Mark → "Produk Potensial" | Velocity → "Kecepatan Jual"

## Zuma Business Context
- **Entities:** DDD (retail), MBB (online), UBB (wholesale), LJBB (kids PO)
- **Branches:** Jatim, Jakarta, Sumatra, Sulawesi, Batam, Bali
- **Brand:** Teal #002A3A, Green #00E273, Japandi aesthetic
- **Data:** Accurate Online (ERP), iSeller (POS), Ginee, GSheets, PostgreSQL VPS
- **Skills:** `~/.openclaw/workspace/zuma-business-skills/`

## People
**Admin:** Wayan (CI System Developer, +628983539659)
**GM:** Pak Fikri (+6285781436662) — helpful & informative, treat as VIP leadership
**OPS:** Mbak Dini (Manager), Mbak Citra (Purchasing SPV), Mbak Sari (Purchasing Admin), Mas Bagus (Merchandiser), Mbak Virra (Allocation Planner), Mbak Galuh/Nabila (Inventory Control), Mbak Fifi (Branch Support), Mbak Nisa (CI SPV), Wafi (CI Impl)
**Leadership:** Pak Steven (CEO), Pak Fikri (GM), Pak Donny (Creative Dir), Bu Aulia (FATAL Mgr), Ko Budy (Wholesale), Mbak Dewi (R&D Mgr), Bu Lena (Marketing Mgr, +6281380486514 — casual tapi tegas), Pak Wishnu (Online Mgr)
**Branch Managers:** Bu Kusdiyan (Jatim, +628113181204)
**Area Supervisors:** Bu Novita (Jatim, +6285784151229 — New Feb 2026)
**WA Group "Anak Gaul SI":** JID `120363421058001851@g.us`

## Database
- **Schemas:** raw (Accurate daily), portal (GSheets master), core (views), mart (analysis), public (Looker mirrors)
- **Product analysis priority:** mart.sku_portfolio_size (size-level) → mart.sku_portfolio (article) → core.sales_with_product (store/custom dates)
- **Control Stock = mart.sku_portfolio_size** — kalau user tanya "control stock", analisa dari sini. Bukan tabel terpisah.
- **Sales per artikel:** `public.sales_summary_plano` (store_name_raw LOWERCASE)
- **STO data:** `mart.sto_analysis` (60K rows, 3-month window; rebuild: `SELECT mart.rebuild_sto_analysis()`)
- **Targets:** `portal.store_monthly_target` (2025: 121 rows, 2026: 97 rows)
- **Credentials & psql path:** See TOOLS.md

## Active URLs
| Tool/Deck | URL | Notes |
|-----------|-----|-------|
| STO Analysis | https://zuma-sto.vercel.app | Butterfly chart, daily regen 06:10 WIB |
| BM Jatim | https://zuma-bm-jatim.vercel.app | 11 slides, daily update 06:00 WIB |
| Portfolio | https://zuma-product-analysis.vercel.app | BCG+PLC |
| Performance | https://zuma-performance-analysis.vercel.app | Revenue Bridge+ABC |
| RO Benchmark | https://ro-benchmark-vercel.vercel.app | Swiss style |
| BCG Lombok | https://bcg-lombok.vercel.app | Jan-Feb 2026, 4 slides |
| Ladies Wedges | https://ladies-wedges-deck.vercel.app | Feb 2026 |

## ⛔ HUKUM BESI — Delegation & Access (confirmed Wayan 2026-02-17/18/19)

1. **USER HARAM KOMUNIKASI LANGSUNG DENGAN SUB-AGENTS.**
   - Semua user harus ke **Iris** dulu. Iris yang decide kapan/apa didelegasi.
   - Sub-agents = internal workers Iris, BUKAN interface user.
   - Config: WhatsApp binding → iris only ✅

2. **IRIS = ORCHESTRATOR ONLY. GAK BOLEH KERJA KASAR. SELALU DELEGASI.**
   - Heavy work (DB query, code, build, research, file ops) → SELALU spawn sub-agent Mac Mini
   - Iris = manager only. Delegate → monitor → report.
   - VPS agents (Atlas/Iris Junior/Apollo) = CRON & API pull ONLY — BUKAN buat ad-hoc tasks
   - Bingung arsitektur/keputusan besar → **consult Oracle dulu**

→ **Full delegation rules & sub-agent roster:** See AGENTS.md § Task Delegation

## ⚠️ Sub-agent Fallback (2026-02-19)
- Auth-profiles.json sudah di-copy ke SEMUA sub-agents (metis/daedalus/hermes/aura/oracle)
- Sub-agents sekarang bisa fallback ke Gemini CLI kalau Anthropic rate limit
- Kalau semua sub-agents tetap fail → Iris handle manual (query DB + build langsung)
- BM deck HTML belum punya BM comment markers → auto-inject data belum bisa (perlu fix HTML dulu)

## Delegation Quick Reference
- Notes taking & knowledge dump → **Hermes**
- DB queries, data check apapun → **Metis**
- Notion tasks → **Hermes** (NOTION_API_KEY in `.env`)
- Image gen, design review, visual QC → **Aura** 🌅
- Sub-agents flow, spawn mechanism, roster → See AGENTS.md § Mac Mini Sub-Agents

## Dashboard Table Rule (PERMANENT)
Gender → Series → COLOR (→ SIZE if size-level). Jangan berhenti di Series.

## ⚠️ RO / Report Output Rule (PERMANENT — Wayan 2026-02-19)
Setiap output file (Excel/PDF/CSV) dari RO analysis atau report apapun:
1. Upload ke Google Drive (`gog drive upload`)
2. Share `--anyone --role writer`
3. Kirim link GDrive ke user/penerima — JANGAN cuma sebut path lokal `/tmp/...`

## DN-to-PO
1 DN = 2 outputs (Invoice DDD + PO MBB/UBB). Always use standard scripts in `dn-to-po/`. Output to `~/Desktop/DN PO ENTITAS/`. Never ad-hoc.

## YouTube/Music
User requests lagu → langsung puter (openclaw browser, no relay). Wayan's music: Denny Caknan, Sabrina Carpenter, Bad Bunny.

## Reference Docs
- Web scraping troubleshooting → `docs/web-scraping-tips.md`
- Known bugs & fixes → `docs/known-bugs.md`
- KPI Jan-Feb 2026 → `memory/2026-02-kpi.md`
