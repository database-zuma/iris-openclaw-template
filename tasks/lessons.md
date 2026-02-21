# lessons.md — What I've Learned

Ini adalah daftar pelajaran dari koreksi Wayan, bugs, dan mistakes. Dibaca saat session start untuk project yang relevan.

---

## Data & SQL

### [2026-02-17] YoY Analysis — Jangan Pakai var_year_qty Mid-Year
Mid-year comparison harus pakai same-period, bukan full-year vs YTD.
→ `SUM(now_jan+now_feb)` vs `SUM(last_jan+last_feb)` (bukan var_year_qty)
→ Detail: MEMORY.md § YoY Analysis

### [2026-02-17] kodemix adalah Business Key
NEVER filter/group by `kode_besar` saja. One article bisa punya beberapa kode_besar (evolution kode lama→baru).
→ ALWAYS GROUP BY `kodemix`

### [2026-02-17] Store Location ≠ Store Name
Jangan assume lokasi dari nama toko. Epicentrum=Lombok, Level 21=Bali.
→ ALWAYS JOIN `portal.store` untuk branch/area info.

### [2026-02-18] FF/FA/FS — Size Key Mismatch
Paired size `"36/37"` di planogram vs individual `"37"` di stock = mismatch → FF=0%.
→ Fix: fallback lookup individual sizes. Detail: `docs/known-bugs.md`

### [2026-02-18] Store Name Mapping — Case-Sensitive
`portal.store_name_map.stock_nama_gudang` harus EXACT match (case-sensitive) dengan `core.stock_with_product.nama_gudang`.
→ Verify exact string sebelum deploy script.

---

## Delegation & Workflow

### [2026-02-13] Selalu Track Promise ke User di HEARTBEAT.md
Kalau bilang "nanti kabarin" → WAJIB tulis di HEARTBEAT.md sebelum lanjut.
Tanpa tracking = broken promise = Wayan nunggu 3 jam.

### [2026-02-13] Technical Tasks → OpenCode, Bukan Iris Langsung
Delegate ke opencode untuk DB ops, scripting, analysis → Iris tetap bisa respons user.

### [2026-02-16] VPS Agents = CRON ONLY
Atlas/Iris Junior/Apollo bukan untuk ad-hoc queries — mereka lebih lemah dari Mac mini.
Ad-hoc analysis → opencode on Mac mini.

### [2026-02-16] Hardcode Credentials di Terminal
OpenCode auto-reject .env in background mode. Hardcode langsung di command string.

### [2026-02-18] Iris = Orchestrator ONLY
Bahkan query "simpel" harus delegate kalau >2 detik. Iris tidak kerja kasar.

### [2026-02-21] IRIS ROLE RULE (Iron Law) — No Script Execution
Iris dilarang keras menjalankan Python/bash scripts atau melakukan "kerja kasar" via `exec`.
→ Script/Code/Build → SELALU delegate ke Daedalus via `sessions_spawn`.
→ `exec` hanya untuk: nanobot calls, quick status checks (<2 detik), memory updates, gog/git single commands.
→ Pelanggaran = Uninstalled.

---

## UX & Communication

### [2026-02-18] Jangan Expose Internal Tools ke User
Exec output, SQL errors, SSH logs = internal. User lihat hasil akhir saja.

### [2026-02-18] No IT Jargon ke User
SKU → "artikel", ASP → "harga rata-rata", MOS → "sisa stok (bulan)", dll.
→ MEMORY.md § UX & Communication Rules

### [2026-02-17] Data Transaksi dari Accurate = Bukan Transaksi Nyata
Invoice Accurate = keperluan pajak. Transaksi nyata = iSeller (belum ada).
→ JANGAN sebut jumlah transaksi ke user dari Accurate.

---

## Web & Scraping

### [2026-02-18] Coba Mobile Site Dulu Sebelum Menyerah
XXI: m.21cineplex.com (PHP, curl works) vs 21cineplex.com (Next.js + reCAPTCHA).
→ Detail: `docs/web-scraping-tips.md`
