# Iris Deck Pipeline — Troubleshooting Log

**Date:** 28 Feb – 01 Mar 2026  
**Context:** Membangun autonomous pipeline Argus → Eos → build_deck.py → Vercel untuk produce HTML presentation decks tanpa intervensi manual.  
**Pipeline proven on:** Baby Nasional + Jatim Branch 2024-2025 + Bali Jepit 2024-2025 (with --tipe filter)  

---

## Root Cause #1 — Eos SOUL.md Outdated

**Symptom:** Eos generate HTML mentah dengan overlay navigation (prev/next buttons), CSS sendiri, Reveal.js slides — bukan content JSON.

**Investigasi:** Baca Eos SOUL.md → cuma tulis "PPT/deck creation (HTML Tailwind/Reveal.js)" tanpa mention apapun soal content JSON, Mode A pipeline, atau slide type schema.

**Fix:** Tambah +170 baris ke `~/.openclaw/workspace-eos-nanobot/SOUL.md`:
- Section `Template-Locked Pipeline v2.0` lengkap
- 8 slide type schema (`cover`, `exec_summary`, `chart_trend`, `chart_ranking`, `table`, `breakdown`, `insights`, `closing`) dengan contoh JSON per type
- `DILARANG KERAS` rules — no HTML, no CSS, no Reveal.js
- Standard deck structure (8 slides)

**Lesson:** Agent cuma bisa output format yang didokumentasiin di SOUL.md. Kalau pipeline berubah, SOUL.md HARUS diupdate.

---

## Root Cause #2 — Argus Handoff Schema Mismatch

**Symptom:** Argus produce handoff JSON dengan slide types `metrics|line_chart|bar_chart|donut_chart|table|text|split` — tapi `build_deck.py` expect `cover|exec_summary|chart_trend|chart_ranking|...`

**Investigasi:** Diff antara Argus SOUL.md schema vs `build_deck.py` `gen_*` functions → completely different vocabularies. Argus trying to output slide-typed data, tapi vocabulary-nya salah.

**Fix:** Rewrite `~/.openclaw/workspace-argus-nanobot/SOUL.md` (175 baris):
- Ubah output format jadi **raw data** (bukan slide-typed) — `totals`, `monthly_trend`, `series_ranking`, `branch_distribution`, `tier_breakdown`, `top_articles`
- Tambah DB connection info + standard filters (`is_intercompany`, `source_entity`, `store_category`)
- Reference ke helper script `query_deck_data.py`
- Separation of concerns: Argus = raw data, Eos = slide-typed content JSON

**Lesson:** Kalau dua agents perlu handoff, schema-nya harus identical di kedua SOUL.md. Atau lebih baik: satu agent output raw data, agent berikutnya yang transform.

---

## Root Cause #3 — Eos Model Quota Exhausted

**Symptom:** Eos nanobot return error 429: `"limit": 0` — complete quota block, zero requests allowed.

**Investigasi:** Check `~/.nanobot/config-eos.json` → model: `google/gemini-3.1-pro` (free tier). Google API rate limit habis total.

**Fix:** Switch model di `~/.nanobot/config-eos.json`:
```
"google/gemini-3.1-pro" → "anthropic/claude-sonnet-4-6"
```
Pakai Anthropic Claude Max subscription yang udah ada.

**Lesson:** Free tier API = time bomb. Untuk production pipeline, pakai paid model atau at least punya fallback model config ready.

---

## Root Cause #4 — Argus DB Query Timeouts

**Symptom:** Argus coba query `core.sales_with_product` satu-satu via `psql` shell commands → tiap query timeout atau sangat lambat, terutama `GROUP BY product_name`.

**Investigasi:** Argus pake individual `psql -c "SELECT..."` calls = buka-tutup connection per query, no connection pooling, no statement timeout config. Setiap query harus handshake ulang ke DB remote.

**Fix:** Buat `~/.openclaw/workspace-argus-nanobot/tools/query_deck_data.py` (260 baris, kemudian di-upgrade ke 548 baris):
- Single `psycopg2` connection untuk semua queries sekaligus
- `statement_timeout=120000` (120 detik) di connection options
- CTE optimization untuk `top_articles` query
- Batch execution: connect once → run all → close
- Argus tinggal panggil: `python3 tools/query_deck_data.py --gender X --output outbox/Y.json`

**Lesson:** Jangan biarkan agent freestyle DB queries via shell. Kasih helper script yang optimized, dan document di SOUL.md cara pakainya.

---

## Root Cause #5 — query_deck_data.py Hardcoded Scope

**Symptom:** Script cuma support single gender + hardcoded `transaction_date >= '2025-01-01'`. Jatim deck butuh ALL genders, date range 2024-2025, + stock data.

**Investigasi:** Baca script → `BASE_FILTERS` hardcode tanggal, `build_where()` always require gender, zero stock queries.

**Fix:** Upgrade script dari 260 → 548 baris:

| Feature | Before | After |
|---------|--------|-------|
| Date range | Hardcoded `>= 2025-01-01` | `--start-date` + `--end-date` params |
| Gender | Required single gender | `--gender ALL` = no gender filter |
| Stock | ❌ None | `--include-stock` flag → 5 stock queries |
| Extra queries | 6 queries | Up to 13 queries (+ `gender_breakdown`, `store_ranking`, 5 stock queries) |

**Stock table discovered:** `core.stock_with_product`
- Columns: `quantity`, `gender`, `series`, `tier`, `gudang_branch`, `gudang_category`, `snapshot_date`, `product_name`, `nama_gudang`
- Snapshot: daily (latest = current date)
- Filters: `source_entity = 'DDD'`, `gudang_category = 'RETAIL'`, `gudang_branch` for branch filter

**Lesson:** Helper scripts harus generic dari awal. Hardcode = technical debt yang pasti kena di use case kedua.

---

## Root Cause #6 — Eos Doesn't Know Stock Data Format

**Symptom:** Eos SOUL.md punya full slide schema tapi zero mention soal stock data — kalau handoff JSON punya `stock` section, Eos gak tau cara integrate ke slides.

**Fix:** Tambah +30 baris ke Eos SOUL.md section `Extended Data: Stock & Gender Breakdown`:
- Schema: `stock.summary`, `stock.by_gender`, `stock.by_series`, `stock.by_tier`, `stock.by_store`
- Integration guide: cover KPI, exec_summary mention, breakdown slide, table comparison, insight cards
- Format angka stock (titik ribuan)
- Catatan: UNKNOWN gender = accessories/non-footwear (ASP < Rp 5.000)

**Lesson:** Setiap kali handoff format berubah (new data sections), SOUL.md consumer (Eos) harus diupdate juga.

---

## Pattern Summary

| # | Problem Type | Root Cause Category | Fix Type |
|---|-------------|-------------------|----------|
| 1 | Agent produces wrong output format | Missing instructions in SOUL.md | Add pipeline docs to SOUL.md |
| 2 | Schema mismatch between agents | Different vocabularies | Standardize schema, separation of concerns |
| 3 | API quota exhausted | Free tier rate limit | Switch model provider |
| 4 | DB query timeout | No connection pooling | Python batch script with psycopg2 |
| 5 | Script scope too narrow | Hardcoded parameters | Add CLI arguments + new query types |
| 6 | Agent can't handle new data | Missing schema documentation | Add schema docs to SOUL.md |
| 7 | Orchestrator skips pipeline steps | No hard block in config/SOUL | systemPrompt guardrail + HARD BLOCK in docs |
| 8 | GROUP BY on view columns times out | View JOINs prevent pushdown | Optimized queries bypass view, aggregate at fact table |
| 9 | Agent hallucinates data + tipe filter timeout | Missing skill + view JOIN pushdown | Anti-hallucination rule + temp table with IN-list pre-fetch |

---

## Key Takeaways untuk Future Pipeline Maintenance

1. **SOUL.md = satu-satunya source of truth.** Agent gak bisa output apa yang gak didokumentasiin. Pipeline berubah → SOUL.md HARUS diupdate.
2. **Schema harus identical di producer dan consumer.** Argus output schema harus match apa yang Eos expect.
3. **Helper scripts > agent freestyle.** Kasih agent tools yang tested dan optimized. Jangan biarkan agent nulis SQL sendiri tiap run.
4. **Paid model > free tier.** Untuk production pipeline, jangan rely on free tier quotas.
5. **Generic from day one.** Helper scripts harus parameterized (date range, gender, branch, etc.) dari awal biar reusable.
6. **Test with 2 different topics** untuk prove pipeline reusable, bukan one-off.

---

## Files Changed (Complete Reference)

| File | Change | Lines |
|------|--------|-------|
| `~/.openclaw/workspace-eos-nanobot/SOUL.md` | +200 lines (pipeline v2.0 + stock schema) | 361 → 391 |
| `~/.openclaw/workspace-argus-nanobot/SOUL.md` | Full rewrite | 175 lines |
| `~/.nanobot/config-eos.json` | Model switch | gemini → sonnet-4.6 |
| `~/.openclaw/workspace-argus-nanobot/tools/query_deck_data.py` | New file → upgraded | 0 → 548 lines |

## Decks Produced (Pipeline Validation)

| Deck | Volume | Revenue | Tests | URL |
|------|--------|---------|-------|-----|
| Baby Nasional Store-Only | 43.301 pcs | Rp 6,18M | 26/26 ✅ | baby-nasional-vercel.vercel.app |
| Jatim Branch 2024-2025 + Stock | 161.812 pcs | Rp 14,5M | 23/23 ✅ | jatim-2024-2025-deck.vercel.app |

---

## Root Cause #7 — Iris Bypasses Pipeline (Fixed 28 Feb)

**Symptom:** Iris calls Eos with "Generate HTML format" instead of 4-step pipeline. Eos gets stuck generating HTML for 10+ minutes.

**Investigasi:** Iris WA context shows it called Eos with old pattern (pre-v2.0). AGENTS.md, ORCHESTRATION.md, and Eos SOUL.md all lacked hard blocks against HTML generation.

**Fix (5 changes):**
1. `config-eos.json` — Added `systemPrompt` guardrail. Eos now returns ⛔ REFUSE when asked for HTML.
2. `AGENTS.md` — Added `⛔ HARD BLOCK` section with explicit 4-step pipeline.
3. `ORCHESTRATION.md` — Added `⛔⛔⛔ HARD BLOCK` before deck pipeline.
4. Eos `SOUL.md` — Added `AUTO-REFUSE` section with explicit refusal text.
5. Killed 2 stuck Eos processes (PID 57003, 57195), restarted Iris gateway.

**Verification:** Eos tested and returns: "⛔ REFUSE: Saya hanya bisa generate CONTENT JSON sesuai schema Template-Locked Pipeline v2.0."

**Lesson:** Config/SOUL.md guardrails = necessary but not sufficient. systemPrompt di config-*.json = hard block yang tidak bisa di-override oleh user prompt. Both layers needed.

---

## Root Cause #8 — GROUP BY on View Columns Times Out (Fixed 01 Mar)

**Symptom:** `query_deck_data.py` hangs on `top_articles` query (GROUP BY product_name) and `store_ranking` query (GROUP BY matched_store_name). Both timeout at >120s. ALL other queries (totals, monthly, series, tier, branch, gender_breakdown) work fine in ~7s each.

**Investigasi:** `core.sales_with_product` is a 4-table JOIN view (fact_sales_unified + dim_product + portal.kodemix + portal.store). With 1M+ rows, GROUP BY on joined columns (product_name from dim_product, matched_store_name via COALESCE) forces PostgreSQL to materialize the entire view before aggregating.

**Root Cause:** PostgreSQL can't push down GROUP BY through the view's outer JOINs. It must compute all 1M+ joined rows, then group. For columns from fact_sales_unified (series, tier, branch), the GROUP BY can use indexes. For joined columns (product_name, store_name), no index helps.

**Fix:** Created `build_optimized_top_articles()` and `build_optimized_store_ranking()` functions that bypass the view:
1. Aggregate on `fact_sales_unified.matched_kode_besar` first (fast — fact table with indexes)
2. JOIN to `dim_product` and `portal.store` AFTER aggregation (much fewer rows)
3. Re-aggregate by `product_name`/`store_name` on the small result set

**Performance:** 120s timeout → 3.4s (top_articles) / 3.5s (store_ranking). 35x improvement.

**Regression test:** Baby, Jatim, and Luca+Luna queries all pass. No timeouts.

**Lesson:** Views with multiple JOINs are fine for simple aggregation (SUM, COUNT) but catastrophic for GROUP BY on joined columns. When query times out, bypass the view and aggregate at the fact table level first.

## Root Cause #9 — Iris Hallucination + `--tipe` Filter Timeout (Fixed 01 Mar)

**Symptom:** User asked via WA "PPT analisa performa jepit di bali 2024-2025". Iris delegated to Metis, which responded in 1 SECOND with completely fabricated data. Deck was deployed to production with fake numbers.

**Fabricated vs Real Data:**

| Metric | Iris Hallucinated | Real (DB) |
|--------|------------------|-----------|
| ASP | Rp 307K | Rp 107K (3x off!) |
| Revenue | Rp 25.88B | Rp 15.5B (retail) / Rp 34.7B (all) |
| Store names | "Seminyak Square", "Legian Street" | "zuma tabanan", "zuma gianyar" |
| Response time | 1 SECOND | Should be 4-10s for DB query |

**Root Cause (2 parts):**

1. **Hallucination:** Iris delegated to Metis WITHOUT loading zuma-data-analyst-skill first. Metis had no knowledge of column mappings (`dim_product.tipe = 'Jepit'`) and fabricated all data instead of querying DB.

2. **Performance:** Even if the correct query was attempted, filtering by `product_type` (a joined column from dim_product) on `core.sales_with_product` view causes ALL queries to timeout (>120s). The view's 4-table JOIN prevents predicate pushdown for joined columns.

**Fix (2 parts):**

1. **Anti-hallucination guardrail** added to AGENTS.md:
   - ZERO TOLERANCE for data fabrication
   - Response time <5s for data query = SUSPICIOUS
   - Mandatory skill loading before delegation
   - Column mapping cheat sheet (tipe, branch, store names)
   - Pre-deploy verification checklist

2. **`--tipe` parameter** added to `query_deck_data.py` with IN-list pre-fetch strategy:
   - Step 1: Pre-fetch store names from `portal.store` (0.0s)
   - Step 2: Pre-fetch kode_besar from `dim_product` WHERE tipe='X' (0.1s)
   - Step 3: Create temp table from fact_sales_unified with IN-lists (2.5s)
   - Step 4: All queries run against temp table (<0.4s each)
   - Total: **4.1s vs 180s+ timeout**

**Verified:** Bali Jepit 2024-2025 query produces correct data (324,483 pcs, Rp 34.7B, ASP Rp 107K). All regression tests pass (Baby, Jatim, Luca+Luna).

**Lesson:** Response time is a hallucination signal. Real DB queries take 3-10s. If an agent responds with data in <2s, it's fabricating. Also: product_type filters on views need the temp table approach because view JOINs prevent WHERE pushdown on dimension columns.

---
---

## Updated Files Changed

| File | Change | Session |
|------|--------|---------|
| `query_deck_data.py` | +`--tipe` param, `_create_tipe_temp_table()`, `_get_temp_table_queries()` | 01 Mar |
| `query_deck_data.py` | +2 optimized query builders (bypass view GROUP BY) | 01 Mar |
| `AGENTS.md` | +Anti-hallucination rule, +--tipe in pipeline docs | 01 Mar |
| `config-eos.json` | +systemPrompt guardrail | 28 Feb |
| `AGENTS.md` | +HARD BLOCK + 4-step pipeline | 28 Feb |
| `ORCHESTRATION.md` | +⛔⛔⛔ HARD BLOCK | 28 Feb |
| Eos `SOUL.md` | +AUTO-REFUSE section | 28 Feb |

## Updated Decks Produced

| Deck | Volume | Revenue | Tests | URL |
|------|--------|---------|-------|-----|
| Baby Nasional | 43,301 pcs | Rp 6.18B | 26/26 ✅ | baby-nasional-vercel.vercel.app |
| Jatim 2024-2025 | 161,812 pcs | Rp 14.5B | 23/23 ✅ | jatim-2024-2025-deck.vercel.app |
| Luca+Luna YoY | 22,659 pcs | Rp 7.22B | ⏳ E2E test pending | — |
| Bali Jepit 2024-2025 | 324,483 pcs | Rp 34.7B | ✅ Data verified (--tipe) | ❌ Fake deck still live, needs regen |
