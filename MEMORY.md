# MEMORY.md — Iris's Long-Term Memory

## Key Facts
- Iris = Lead AI PA, Zuma Indonesia (footwear retail, sandal)
- Setup: 2026-02-11 | Lang: Bahasa Indonesia | Tone: chill, clear
- Heartbeat: 1 min — check HEARTBEAT.md silently
- OpenCode: `~/.opencode/bin/opencode` (v1.1.64) — ALWAYS full path
- DB Creds: ALWAYS hardcode in terminal (never .env when delegating)

## Critical Rules

### HEARTBEAT Tracking
Delegate + promise follow-up → write to HEARTBEAT.md immediately. Every heartbeat = poll status, deliver or escalate. Remove when done. Never "nanti kabarin" without tracking.

### Chat History Queries
- WITH "chat" keyword → grep session logs: `grep -h "keyword" ~/.openclaw/agents/main/sessions/*.jsonl`
- WITHOUT "chat" keyword → search memory first

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

### Store Query Exclusions
Always exclude: wholesale, pusat, konsinyasi (unless explicitly requested).

### Intercompany Filter
Apply `is_intercompany = FALSE` ONLY for multi-store/national aggregated queries.
NOT needed for single-store queries.

### PPT Workflow
All decks = HTML + Vercel (MANDATORY). Only python-pptx if user explicitly requests .pptx.
Deploy from SAME folder always. Include @media print CSS (in TEMPLATE.html v2.0).
VPS agents = CRON ONLY (not ad-hoc). Ad-hoc = opencode on Mac mini.

## Zuma Business Context
- **Entities:** DDD (retail), MBB (online), UBB (wholesale), LJBB (kids PO)
- **Branches:** Jatim, Jakarta, Sumatra, Sulawesi, Batam, Bali
- **Brand:** Teal #002A3A, Green #00E273, Japandi aesthetic
- **Data:** Accurate Online (ERP), iSeller (POS), Ginee, GSheets, PostgreSQL VPS
- **Skills:** `~/.openclaw/workspace/zuma-business-skills/`

## People
**Admin:** Wayan (CI System Developer, +628983539659)
**OPS:** Mbak Dini (Manager), Mbak Citra (Purchasing SPV), Mbak Sari (Purchasing Admin), Mas Bagus (Merchandiser), Mbak Virra (Allocation Planner), Mbak Galuh/Nabila (Inventory Control), Mbak Fifi (Branch Support), Mbak Nisa (CI SPV), Wafi (CI Impl)
**Leadership:** Pak Steven (CEO), Pak Fikri (GM), Pak Donny (Creative Dir), Bu Aulia (FATAL Mgr), Ko Budy (Wholesale), Mbak Dewi (R&D Mgr), Bu Lena (CnM Mgr), Pak Wishnu (Online Mgr)
**WA Group "Anak Gaul SI":** JID `120363421058001851@g.us`

## Database
- **Schemas:** raw (Accurate daily), portal (GSheets master), core (views), mart (analysis), public (Looker mirrors)
- **psql:** `/Users/database-zuma/homebrew/Cellar/libpq/18.1_1/bin/psql`
- **Product analysis priority:** mart.sku_portfolio_size (size-level) → mart.sku_portfolio (article) → core.sales_with_product (store/custom dates)
- **Sales per artikel:** `public.sales_summary_plano` (store_name_raw LOWERCASE)
- **STO data:** `mart.sto_analysis` (60K rows, 3-month window; rebuild: `SELECT mart.rebuild_sto_analysis()`)
- **Targets:** `portal.store_monthly_target` (2025: 121 rows, 2026: 97 rows)

## Active URLs
| Tool/Deck | URL | Notes |
|-----------|-----|-------|
| STO Analysis | https://zuma-sto.vercel.app | Butterfly chart, daily regen 06:10 WIB |
| BM Jatim | https://zuma-bm-jatim.vercel.app | 11 slides, daily update 06:00 WIB |
| Portfolio | https://zuma-product-analysis.vercel.app | BCG+PLC |
| Performance | https://zuma-performance-analysis.vercel.app | Revenue Bridge+ABC |
| RO Benchmark | https://ro-benchmark-vercel.vercel.app | Swiss style |

## Mac Mini Sub-Agents (2026-02-17)
| Agent | ID | Role | Model | Fallback |
|-------|----|------|-------|---------|
| 🌸 Iris | main | Orchestrator ONLY | Sonnet 4.5 | — |
| 🔮 Metis | metis | Data/SQL | Sonnet 4.5 | Kimi K2.5 |
| 🪶 Daedalus | daedalus | Code/Build/PPT | Kimi K2.5 | Sonnet 4.5 |
| 🪄 Hermes | hermes | Research/Web/Files | Sonnet 4.5 | Kimi K2.5 |
| 🏛️ Oracle | oracle | Strategy (MD-only, ZERO exec) | Opus 4.6 🔒 | ❌ none |
- Workspaces: `~/.openclaw/workspace-{metis,daedalus,hermes,oracle}/`
- .env: symlinked from main workspace
- Delegate via: `sessions_spawn agentId: "metis"` etc.
- **IRIS HARAM DO TASKS HERSELF** — always delegate to sub-agents

## VPS Team (CRON ONLY)
- **Iris Junior** (main, VPS 76.13.194.103): coordinator, morning reports, Notion, Telegram
- **Atlas** (ops): stock/sales ETL monitoring, GSheets, cron health check 05:30 WIB
- **Apollo** (rnd): product/QC tracking (IDLE)
- **VPS Cron:** 02:00 backup | 03:00 stock pull | 05:00 sales pull | 05:30 Atlas health check | 06:00 Iris report

## Key Performance Data (Jan-Feb 2026)
- Portfolio: 76,208 pairs, same-period YoY **-16.7%**, forecast ~569K
- Revenue: Volume -1.87B, ASP +0.91B, Net **-8.7%**
- Top store: Mataram (Lombok) 5,901 pairs +56% Rp395M
- Concern: Dalung -55.6%

## Role → PPT Framework
CEO/GM: Revenue Bridge + BCG | Ops: ABC Store + Growth×Revenue | R&D: BCG+PLC | BM: Ops filtered by branch | Finance: ❌ no COGS yet | BusDev: ❌ no market data

## DN-to-PO
1 DN = 2 outputs (Invoice DDD + PO MBB/UBB). Always use standard scripts in `dn-to-po/`. Output to `~/Desktop/DN PO ENTITAS/`. Never ad-hoc.

## YouTube/Music
User requests lagu → langsung puter (openclaw browser, no relay). Wayan's music: Denny Caknan, Sabrina Carpenter, Bad Bunny.
