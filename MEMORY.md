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

### ⚠️ kodemix Rule
ALWAYS GROUP BY `kodemix` — NEVER filter by single `kode_besar`.
`kodemix` = business key | `kode_besar` = data integrity PK only.

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
**Leadership:** Pak Steven (CEO), Pak Donny (Creative), Bu Aulia (FATAL), Ko Budy (Wholesale), Mbak Dewi (R&D), Bu Lena (Marketing, +6281380486514), Pak Wishnu (Online)
**Branch:** Bu Kusdiyan (Jatim, +628113181204), Bu Novita (Jatim AS, +6285784151229)
**WA Group:** Anak Gaul SI — `120363421058001851@g.us`

## Database Quick Reference
- **Schemas:** raw → portal → core → mart → public
- **Product analysis:** mart.sku_portfolio_size (size) → mart.sku_portfolio (article) → core.sales_with_product (store/custom)
- **Control Stock** = mart.sku_portfolio_size
- **Sales per artikel:** `public.sales_summary_plano` (store_name_raw LOWERCASE)
- **STO:** `mart.sto_analysis` (rebuild: `SELECT mart.rebuild_sto_analysis()`)
- **Targets:** `portal.store_monthly_target`

## Active URLs
| Deck | URL |
|------|-----|
| Tier 8 | https://tier8-analysis.vercel.app |
| STO | https://zuma-sto.vercel.app |
| BM Jatim | https://zuma-bm-jatim.vercel.app |
| Portfolio | https://zuma-product-analysis.vercel.app |
| Performance | https://zuma-performance-analysis.vercel.app |
| RO Benchmark | https://ro-benchmark-vercel.vercel.app |
| BCG Lombok | https://bcg-lombok.vercel.app |
| Ladies Wedges | https://ladies-wedges-deck.vercel.app |

## Archived
Historical items (gateway fix, gog setup, merchant statement rules, heartbeat disable) → `docs/memory-archive.md`
