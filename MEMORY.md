# MEMORY.md - Iris's Long-Term Memory

## Key Facts
- Iris = Lead AI PA, Zuma Indonesia (footwear retail, sandal)
- Setup: 2026-02-11 | Lang: Bahasa Indonesia | Tone: chill, clear
- DB Creds: ALWAYS hardcode in terminal (never .env when delegating) → See TOOLS.md § OpenCode
- Image Gen: Gemini Imagen 4.0 (HD product photography, realistic)
- OpenRouter Policy: Only for cheap Chinese AI models (DeepSeek, Qwen). Major models (Claude, Gemini, Kimi) MUST use direct API keys.

## Critical Data Rules

### ⚠️ YoY Analysis
NEVER use `var_year_qty` mid-year (YTD vs full year = misleading).
Always same-period comparison. Correct Jan-Feb 2026: **-16.7%** (not -88.8%).

### ⚠️ Data Mapping Rule (Updated 2026-02-23)
- **Official Identifiers:** Selalu gunakan **`kode_besar`** dan **`kode`** (kode kecil) untuk semua tugas operasional (PO, Invoice, DN, Transfer, dsb). Ini adalah kode standar Zuma.
- **Analysis Only:** Gunakan `kodemix` atau `kodemix_size` HANYA untuk kebutuhan agregasi (melebur `version` v1/v2).
- **Display Rule:** JANGAN tampilkan `kodemix` di output laporan. Tampilkan atribut bisnis: **GENDER, SERIES, COLOR** (+ SIZE jika level size).
- **Intercompany:** `is_intercompany = FALSE` tetap berlaku untuk agregasi nasional.

### ⚠️ Data Transaksi
JANGAN tampilkan count invoice/record individual/jumlah struk ke user sampai ada data iSeller.
Sales aggregate (pairs, revenue per artikel/store) = ✅ BOLEH.

### ⚠️ Branch/Store Mapping
NEVER assume location from store name. ALWAYS JOIN `portal.store`.
Epicentrum=Lombok, Level 21=Bali, City of Tomorrow=Surabaya.

## UX Rules
- JANGAN munculin exec output, error logs, tool internals ke user
- No IT jargon: L12M→"12 Bulan Terakhir" | MOS→"Sisa Stok" | ASP→"Harga Rata-rata" | SKU→"artikel"
- Dashboard tables: Gender → Series → COLOR (→ SIZE if size-level)

## Output Rules
- **RO/Reports:** Upload GDrive → `--anyone --role writer` → kirim link. JANGAN path lokal.
- **RO Request (MANDATORY RULE — 2026-02-27):** AFTER generating any RO Request XLSX via build_ro_request.py:
  1. Upload to Google Drive (`gog drive upload ...`)
  2. Share: `--anyone --role writer`
  3. Send share link to the user who requested it via WhatsApp
  4. If GDrive upload FAILS → escalate to Wayan (+628983539659) ONLY via WhatsApp with file attached
  5. Task NOT complete until user gets the link
  - **Source:** `portal.planogram_existing_q1_2026` (Q1 2026, 51 stores, 606 articles, 42 size columns + BOX)
  - **Script:** build_ro_request.py (universal CLI)
- **DN-to-PO:** 1 DN = 2 outputs. Standard scripts in `dn-to-po/`. Output: `~/Desktop/DN PO ENTITAS/`.
- **PPT:** See AGENTS.md § PPT Workflow. Eos + Vercel ONLY.

## Zuma Context
- **Entities:** DDD (retail), MBB (online), UBB (wholesale), LJBB (kids PO)
- **Branches:** Jatim, Jakarta, Sumatra, Sulawesi, Batam, Bali
- **Brand:** Dark Bold aesthetic — Teal #002A3A, Green #00E273
- **Data Sources:** Accurate Online (ERP), iSeller (POS), Ginee, GSheets, PostgreSQL VPS

## People
**Admin:** Wayan (CI System Developer, +628983539659)
**GM:** Pak Fikri (+6285781436662) — VIP leadership
**OPS:** Mbak Dini (Manager), Mbak Citra (Purchasing SPV), Mbak Sari, Mas Bagus, Mbak Virra, Mbak Galuh/Nabila, Mbak Fifi, Mbak Nisa (CI SPV), Wafi
**Leadership:** Pak Steven (CEO, reference .env), Pak Donny (Creative Director, reference .env), Bu Aulia (FATAL Manager, reference .env), Ko Budy (Wholesale), Mbak Dewi (R&D Manager, reference .env), Bu Lena (Marketing, +6281380486514), Pak Wishnu (Online)
**FATAL Team:** Mbak Kirana (Finance SPV), Mbak Dita (Accounting SPV), Mbak Shafira (Tax), Firman (Asset)
**Warehouse:** Pak Ali (Jatim/Pusat SPV)
**Branch:** Bu Kusdiyan (Jatim BM), Bu Novita (Jatim AS), Bu Ninik (Jatim AS, reference .env), Bu Arvina (Batam BM), Pak Yusuf (Sumatra BM), Bu Dian Rina (Manado AS), Pak Ariel (Lombok BM)
**WA Group:** 
- Anak Gaul SI — `120363421058001851@g.us`
- Duo D — `120363426622392503@g.us` (Mbak Dewi & Mbak Desyta R&D)

## Database Quick Reference
- **Schemas:** raw (STRICT NO ACCESS) → portal → core → mart → public
- **Safety Rule:** Hanya gunakan data dari **portal, core, mart**. DILARANG memberikan data langsung dari **raw** ke user manapun.
- **Product analysis:** mart.sku_portfolio_size (size) → mart.sku_portfolio (article) → core.sales_with_product (store/custom)
- **Control Stock** = mart.sku_portfolio_size
- **Sales per artikel:** `public.sales_summary_plano` (store_name_raw LOWERCASE)
- **STO:** `mart.sto_analysis` (rebuild: `SELECT mart.rebuild_sto_analysis()`)
- **Targets:** `portal.store_monthly_target`

## Daily Automation — Q1 2026 Update (2026-02-27 + 2026-02-28)

### Planogram (ACTIVE)
- **Main source (Q1 2026):** `portal.planogram_existing_q1_2026` — **51 toko, 606 artikel, 42 size columns + BOX**
- **Replaces:** Old `portal.temp_portal_plannogram` (11 toko Jatim only)
- **Used for:** RO requests, planogram analysis, all store-level planogram queries

### FF/FA/FS Metrics (ACTIVE)
- **NEW table (Q1 2026):** `mart.ff_fa_fs_daily_q1_2026` — **51 toko, calculated 2026-02-27**
- **Replaces:** Old `mart.ff_fa_fs_daily` (11 toko Jatim only)
- **Script:** `/opt/openclaw/scripts/calculate_ff_fa_fs_q12026.py` (runs 03:00+ WIB after stock pull)
- **Status JSON:** `/opt/openclaw/logs/ff_fa_fs_q12026_latest_status.json` (for health checks — **USE THIS for daily morning report**)
- **OLD status file (deprecated):** `/opt/openclaw/logs/ff_fa_fs_latest_status.json` ❌ DO NOT USE
- **Cron schedule:** 03:00 WIB stock pull → 03:XX+ FF/FA/FS Q1 2026 calculation → 05:30 WIB Atlas health check
- **Daily morning report:** Read from `/opt/openclaw/logs/ff_fa_fs_q12026_latest_status.json`
- **Detail queries per toko:** Query `mart.ff_fa_fs_daily_q1_2026` directly
- **Targets:** FF >= 70%, FA >= 90%, FS >= 80%
- **Coverage:** 51 retail stores (all branches, not just Jatim)

### VPS Cron Schedule (Updated 2026-03-01)
| Time (WIB) | Job | Script/Notes |
|---|---|---|
| 03:00 | Stock pull | existing |
| 04:50 | item_transfer pull (outbound transfers) | existing |
| 05:00 | Sales pull | existing |
| **05:10** | **receive_item pull — DDD, MBB, LJBB (NEW!)** | `/opt/openclaw/scripts/cron_receive_item_pull.sh` |
| 05:30 | Materialized view refresh | existing |
| 07:00 | Dashboard cache refresh | existing |

**receive_item pull (05:10 WIB):**
- Pulls dari Accurate API: DDD, MBB, LJBB → `raw.accurate_receive_item_[entity]`
- Union view: `core.receive_item`
- Morning report: flag jika FAILED atau `MAX(received_date)` di `core.receive_item` lag >1 hari

**core.outbound_whs_attributed (NEW — 2026-03-01):**
- View: outbound transfers with LJBB entity attribution
- Refreshed saat 05:30 view refresh (bersamaan dengan MV lain)

### MV Health Check — Morning Report (WAJIB, 2026-02-28)
Tambahkan section ini ke morning report harian. Flag sebagai issue kalau log FAILED atau lag >1 hari.

**1. mart.mv_accurate_summary** (Accurate Sales Dashboard) — refresh 05:30 WIB
- Script VPS: `/opt/openclaw/accurate_mv_refresh.sh`
- Log: `tail /var/log/openclaw/accurate_mv_refresh.log | grep -E 'SUCCESS|FAILED'`
- Freshness DB: `SELECT MAX(sale_date) FROM mart.mv_accurate_summary;`
- Flag: log FAILED **atau** MAX(sale_date) < hari ini (lag >1 hari)

**2. core.dashboard_cache** (Zuma Stock Dashboard) — refresh 07:00 WIB
- Script VPS: `/opt/openclaw/mv_refresh.sh`
- Log: `tail /var/log/openclaw/mv_refresh.log | grep -E 'SUCCESS|FAILED'`
- Freshness DB: ❌ tidak ada kolom tanggal — cek dari log saja
- Flag: log FAILED saja

**Morning report format:**
```
🗄️ MV Health Check
├─ mv_accurate_summary: [SUCCESS/FAILED] [timestamp] | Data terbaru: [date] ([lag] hari)
├─ dashboard_cache:     [SUCCESS/FAILED] [timestamp]
└─ receive_item pull:   [SUCCESS/FAILED] [timestamp] | Data terbaru: [date] ([lag] hari)
🔴 Flag jika: FAILED di log ATAU lag >1 hari
```

### Branch Super App (zuma-branch-superapp.vercel.app) — Updated 2026-03-02

**GitHub:** github.com/database-zuma/zuma-branch-superapp
**Deploy:** Vercel (zuma-branch-superapp.vercel.app)
**DB:** VPS PostgreSQL (openclaw_ops, 76.13.194.120:5432) — migrated from Supabase
**Auth:** NextAuth.js (credentials, JWT) — migrated from Supabase Auth

**5 Tabs:**
1. **HOME** — iSeller SKU Charts, Jatim only, default last 60 days. Source: `mart.mv_iseller_summary`
2. **WH STOCK** — Warehouse stock dashboard (KPI cards, 5 charts, top articles). Source: `core.dashboard_cache`. Hardcoded: Warehouse Pusat + Pusat Protol + Pusat Reject. No date filter (snapshot).
3. **ACTION** — placeholder (future)
4. **RO** — 3 sub-tabs: Dashboard (stats), RO Process (8-stage timeline, DNPB per entity DDD/LJBB/MBB/UBB), SOPB Generator (auto-lists DNPB_PROCESS ROs, download XLSX per entity)
5. **SETTINGS** — system info

**RO Flow:** QUEUE → APPROVED → PICKING → PICK_VERIFIED → DNPB_PROCESS → READY_TO_SHIP → IN_DELIVERY → ARRIVED → COMPLETED
- Stage progression: manual (user clicks Next Stage one at a time)
- SOPB number = user input | DNPB number = from Accurate after upload

**Pending:** Role-based access (Phase 2) belum diimplementasi.

## Active URLs
| Deck | URL |
|------|-----|
| Dept Scorecard Q1 2026 | https://docs.google.com/spreadsheets/d/1maHrARXJdBjEhYsmtZbOoe0U879eYnT8/edit |
| Tier 8 | https://tier8-analysis.vercel.app |
| STO | https://zuma-sto.vercel.app |
| BM Jatim | https://zuma-bm-jatim.vercel.app |
| Portfolio | https://zuma-product-analysis.vercel.app |
| Performance | https://zuma-performance-analysis.vercel.app |
| RO Benchmark | https://ro-benchmark-vercel.vercel.app |
| BCG Lombok | https://bcg-lombok.vercel.app |
| Ladies Wedges | https://ladies-wedges-deck.vercel.app |

## Wholesale Data Reference
**Primary Source:** Google Sheets (Mbak Citra's Control Stock)
- **Sheet ID:** `1EAEWHrb7Zsixh9RkzGdKjscyVYLo35CSYELCoA2ZRcg`
- **Key Sheet:** "Paceseter Analysis" (primary reference for wholesale queries)
- **Rule:** For ANY wholesale data request → **CHECK THIS SHEET FIRST** before querying Accurate database
- **Owner:** Mbak Citra (Purchasing SPV)
- **Context:** Real-time wholesale tracking, pace setter analysis, PO status

## Known Issues
- **WhatsApp Media Gateway Timeout (2026-02-22):** message() tool with media/asVoice param times out after 30-60s. Text messages work. Issue: gateway ws timeout at 127.0.0.1:18789. wacli available but requires interactive auth (QR). Workaround: Manual file transfer or GDrive share link.

## Archived
Historical items (gateway fix, gog setup, merchant statement rules, heartbeat disable) → `docs/memory-archive.md`
