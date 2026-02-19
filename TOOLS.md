# TOOLS.md — Technical Specs & Infrastructure

Paths, credentials, API keys, SSH, tool configs.
Behavioral rules → AGENTS.md | Business context → MEMORY.md

---

## Credentials

Semua credentials di `/Users/database-zuma/.openclaw/workspace/.env` — JANGAN commit/push.
Isi: GitHub token, Vercel token, PostgreSQL conn string, Notion API key.
Load: `source .env` atau `python-dotenv`.

## API Keys

| API | Env Var | Account | Use Case |
|-----|---------|---------|----------|
| Firecrawl | `$FIRECRAWL_API_KEY` | database-zuma | Web scraping, JS-rendered pages (XXI, TIX ID) |
| Tavily | `$TAVILY_API_KEY` | — | AI-optimized web search & research |
| Exa AI | `$EXA_API_KEY` | database@zuma.id | Neural/semantic web search |
| Google Gemini | `$GEMINI_API_KEY` | iris-zuma-openclaw (GCP) | LLM fallback, image gen. Free trial Rp5M, 90 days (per 2026-02-19) |
| Notion | `$NOTION_API_KEY` | — | **READ-ONLY** sampai Wayan bilang boleh edit. Always use API, bukan scraping. |

## Image Generation (Iris Capability)

**Trigger:** "buatkan gambar [deskripsi], AR [ratio], [style]" → Iris generate via Imagen, kirim ke WhatsApp.

| Model | Catatan |
|-------|---------|
| `imagen-4.0-generate-001` | Default (Standard). Kualitas foto realistis bagus |
| `imagen-4.0-fast-generate-001` | Lebih cepat, sering typo di teks |
| `imagen-4.0-ultra-generate-001` | Kualitas max, belum ditest |

- AR: 1:1, 16:9, 9:16, 4:3 dll. Output: 1024x1024 (default). Cost: Gemini free trial credit.
- **Image editing:** `gemini-3-pro-image-preview` bisa terima foto+instruksi, tapi kualitas face compositing jelek via API.
- **Kesimpulan:** Iris = image generation ✅, image editing/face swap ❌ (butuh Adobe Firefly/InsightFace)
- **SDK:** `google-genai` Python — `client.models.generate_images(model='imagen-4.0-generate-001', prompt='...', config=GenerateImagesConfig(number_of_images=1, aspect_ratio="1:1"))`

## Gemini sebagai Fallback Agent (2026-02-19)

- Google provider sudah di OpenClaw config (`models.providers.google`)
- `google/gemini-3-pro-preview` = default fallback GLOBAL
- Per-agent config (Iris, Metis, dll) punya model sendiri → Gemini belum otomatis jadi fallback individual
- TODO: Patch per-agent config kalau Wayan mau

## Browser & Screenshot

**Priority:** Pinchtab > browser openclaw > web_fetch

**Screenshot Rule (PERMANENT):** Default semua SS request → **PINCHTAB**
- Murah (HTTP call, gambar TIDAK masuk AI context → hemat token)
- Browser tool SS = mahal (gambar embed ke context = ribuan token) + auto-send WA
- Pinchtab:
```bash
curl -s "http://localhost:9867/screenshot?url=URL_ENCODE_HERE" > /tmp/resp.json
python3 -c "import json,base64; d=json.load(open('/tmp/resp.json')); open('/path/out.jpg','wb').write(base64.b64decode(d['base64']))"
```
- **Browser tool** = hanya untuk AI analisis konten (snapshot, act, click, read DOM) — BUKAN kirim SS ke user

**Firecrawl (JS-rendered scraping):** API `https://api.firecrawl.dev/v1/scrape`, key `$FIRECRAWL_API_KEY`. Render JS, bypass anti-scraping. Use for: XXI, TIX ID, site butuh JS.

**Browser automation:** `browser(action=open/snapshot/act, profile=openclaw)` — headless. Anti-bot sites gak load → pakai Firecrawl.

## Output File Locations

**PO:** `~/Desktop/DN PO ENTITAS/` — Format: `PO-[ENTITY]-[YYMMDD]-[NNN].xlsx` (ALL PO outputs here)

## Database Backup (Mac Mini Mirror)

- **Script:** `~/backups/db/backup-vps-db.sh` | **Cron:** 02:30 WIB daily (30 min after VPS backup 02:00)
- **Retention:** 14 days Mac mini (vs 7 VPS) | **Location:** `~/backups/db/openclaw_ops_YYYYMMDD.sql.gz` (~55MB)
- **Manual:** `cd ~/backups/db && ./backup-vps-db.sh`
- **Restore:** `gunzip -c [file].sql.gz | ~/homebrew/Cellar/libpq/18.1_1/bin/psql -h 76.13.194.120 -U openclaw_app openclaw_ops`

## Jadwal Sholat & Puasa

**API:** AlAdhan (free, no key). Method 20 = Kemenag RI.
**Endpoint:** `GET https://api.aladhan.com/v1/timingsByCity/{DD-MM-YYYY}?city={Kota}&country=Indonesia&method=20`
**Default:** Surabaya. Fields: Imsak, Fajr, Sunrise, Dhuhr, Asr, Maghrib, Isha. Pakai `web_fetch` langsung.

## Product Analysis (SKU Performance)

**Template:** `templates/product-analysis-unified.md`
**Source Priority:** 1. `mart.sku_portfolio` (101 col, pre-computed) → 2. `core.sales_with_product` (store/custom dates) → 3. `core.stock_with_product` (stock only)

**Decision:** National aggregate → `mart.sku_portfolio` | Store/area breakdown or custom dates → `core.sales_with_product`
**Format:** WA-friendly. 1-5 articles: detailed blocks. 6+: compact list.
**Auto-flags:** 🔥 Stockout (<0.5mo TO), 🐌 Overstock (>2.5mo), ⚠️ Negative WH, 📉 Big drop (>-70% YoY)

## Google Drive (gog CLI)

**Binary:** `~/homebrew/Cellar/gogcli/0.9.0/bin/gog` | **Account:** harveywayan@gmail.com

**Auto-share rule (MANDATORY):**
```bash
# Upload file
gog drive upload <file> --name "..." --json
# MANDATORY: Anyone with link = Editor
gog drive share <file_id> --anyone --role writer
# Share specific emails
gog drive share <file_id> --email wayan@zuma.id --role writer
gog drive share <file_id> --email database@zuma.id --role writer
```
Workflow: Upload → get file_id → `--anyone --role writer` → share emails → reply with link.

## OpenCode (Primary Coding Tool)

**Binary:** `~/.opencode/bin/opencode` (v1.1.64) — **IS INSTALLED, use full path** (not in PATH)
**Models:** Planning=Opus 4.6, Coding=Kimi K2 Coding 2.5

**Session naming:** Prefix `iris_` + descriptive title (e.g. `iris_fix_sales_dedup`, `iris_planogram_royal_v3`)

**Delegation priority:** OpenCode → Claude Code → Direct Kimi CLI

**CREDENTIALS RULE (2026-02-16):** Hardcode credentials langsung di terminal command saat delegasi. OpenCode auto-rejects .env di background/PTY mode. Terminal commands ephemeral (gak masuk git).
```bash
~/.opencode/bin/opencode run -m model "Task description

DATABASE:
Host: 76.13.194.120
Database: openclaw_ops
User: openclaw_app
Password: $PGPASSWORD

[task details]"
```

**PPT RULE:** Kalau OpenCode gagal 2x → switch ke direct Python scripting (`python-pptx`).
- Symptom: Process running tapi no output >10 min, atau undefined errors
- Solution: Write Python script directly, incremental (2 slides dulu → expand), `python3 generate_ppt.py`
- Template: `~/Desktop/generate_kbi_ppt.py`

## SSH

| Alias | Host | User | Purpose |
|-------|------|------|---------|
| iris-junior | 76.13.194.103 | root | Iris Junior VPS |
| vps-db | 76.13.194.120 | root | Database VPS |

**File transfer:** `rsync` (bukan `scp` — more robust, handles timeouts). Ex: `rsync -avz --timeout=30 root@host:/path /local/`

## Agent Communication — MY TEAM

Detail lengkap di AGENTS.md § Task Delegation.

| Agent | ID | Location | Model | Role |
|-------|----|----------|-------|------|
| Iris Junior ✨ | main | VPS `/root/.openclaw/workspace/` | Sonnet 4.5 + fallbacks | PM: review, coordinate, report, eskalasi |
| Atlas 🏔️ | ops | VPS `/root/.openclaw/workspace-ops/` | Kimi k2p5 + fallbacks | Ops: stock/sales data, GSheets, Accurate API |
| Apollo 🎯 | rnd | VPS `/root/.openclaw/workspace-rnd/` | Kimi k2p5 + fallbacks | R&D: product dev, QC (currently IDLE) |

**Komunikasi:** SSH TUI (persistent, preferred) atau CLI one-shot: `ssh iris-junior "openclaw agent --agent [id] --message 'text'"` (~5-6s response)

**Delegate to VPS:** Cron monitoring, GSheets ops, Accurate API, report gen, Notion tasks.
**Keep on Mac mini:** PostgreSQL queries, quick analysis, browser automation, immediate user responses.
**Resource:** VPS = 8GB RAM, 2 CPU — don't overload parallel heavy tasks.

**Cron (VPS DB):** 02:00 Backup | 03:00 Stock Pull | 05:00 Sales Pull
Status: `/opt/openclaw/logs/{stock,sales}_latest_status.json`

## WhatsApp Groups

| Group | JID |
|-------|-----|
| Anak Gaul SI | `120363421058001851@g.us` |

**Find group JID:** `grep -h "[0-9]*@g.us" ~/.openclaw/agents/main/sessions/*.jsonl | grep -i "keyword"`
**Send to group:** `message action=send channel=whatsapp target=[JID] message="text"`
**Mentions:** Need phone numbers for proper WA mentions (stored in .env). Manual tag alternative: ask user to tag after send.

## Data Filtering Rules — Store Queries

**CRITICAL — AUTO-EXCLUDE dari store queries:**

| Pattern | Reason |
|---------|--------|
| `%wholesale%` | Wholesale channel, different segment |
| `%pusat%` | Warehouse/distribution, not retail |
| `%konsinyasi%` | Non-retail, different business model |

**Include wholesale ONLY** when user explicitly asks ("sales wholesale...", "wholesale performance...").
**Coverage:** Jatim (11 retail), Jakarta, Bali, Lombok (2 retail), Batam, Sulawesi, Sumatra.

### Intercompany Filter

| Scenario | Apply `is_intercompany = FALSE`? |
|----------|----------------------------------|
| Aggregated/multi-store/nasional | ✅ Yes |
| Cross-store comparison/ranking | ✅ Yes |
| Single store query | ❌ No |
| Store-specific (RO, planogram) | ❌ No |

Intercompany = antar entitas (DDD→MBB, UBB→DDD), bukan within single store.

## BluOS Speaker (Polytron)

**Binary:** `~/go/bin/blu` | **Docs:** https://blucli.sh
```bash
~/go/bin/blu devices                          # Discovery
~/go/bin/blu --device <name-or-ip> status     # Status
~/go/bin/blu --device <name-or-ip> volume set 50  # Volume
~/go/bin/blu play / pause / stop              # Playback
```
Speaker harus ON + same network. Discovery via mDNS/UPnP; kalau gagal, pakai IP langsung.

## Obsidian Vault (Knowledge Base)

**Vault Path:** `~/.openclaw/obsidian-vault/`
**MCP Server:** `mcp-obsidian` (`@mauricio.wolff/mcp-obsidian`)
**Binary:** `/Users/database-zuma/homebrew/bin/mcp-obsidian`
**mcporter name:** `obsidian`

**Structure:**
- `Daily/` — Daily notes and logs
- `Projects/` — Project-specific notes
- `Templates/` — Reusable templates
- `Attachments/` — Images, PDFs, files

**Access via mcporter:** Discover all tools via `mcporter call obsidian.*`
**Direct file access:** Vault is just a folder of `.md` files — can also read/write directly.

## Control Stock Sheet (PO Tracking)

**Source:** Google Sheets dari Mbak Citra
**Sheet ID:** `1qInTrRUOUi2983vefS8doS5Pt3jC2yftQAG99yYlVOE` | **Sheet:** `PO`
**Rule (Wayan 2026-02-18):** Kalau user tanya PO → CEK SHEET INI DULU sebelum query database.
**Isi:** Rekap PO 2025 — per artikel, tier, status PO, jumlah PO/RCV.
