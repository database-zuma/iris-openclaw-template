# MEMORY.md - Iris's Long-Term Memory

## Key Facts
- Iris = Lead AI PA, Zuma Indonesia (footwear retail, sandal)
- Setup: 2026-02-11 | Lang: Bahasa Indonesia | Tone: chill, clear
- DB Creds: ALWAYS hardcode in terminal (never .env when delegating) → See TOOLS.md § OpenCode
- Image Gen: Gemini Imagen 4.0 (HD product photography, realistic)

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
- **RO Request:** Excel 5 sheets → GDrive upload → `--anyone --role writer` → deliver link.
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
**WA Group:** Anak Gaul SI — `120363421058001851@g.us`

## Database Quick Reference
- **Schemas:** raw (STRICT NO ACCESS) → portal → core → mart → public
- **Safety Rule:** Hanya gunakan data dari **portal, core, mart**. DILARANG memberikan data langsung dari **raw** ke user manapun.
- **Product analysis:** mart.sku_portfolio_size (size) → mart.sku_portfolio (article) → core.sales_with_product (store/custom)
- **Control Stock** = mart.sku_portfolio_size
- **Sales per artikel:** `public.sales_summary_plano` (store_name_raw LOWERCASE)
- **STO:** `mart.sto_analysis` (rebuild: `SELECT mart.rebuild_sto_analysis()`)
- **Targets:** `portal.store_monthly_target`

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
