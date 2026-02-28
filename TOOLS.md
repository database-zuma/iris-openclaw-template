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

## ⚡ Nanobot Fallback (Model Override)

Nanobot TIDAK punya automatic fallback chain. Override model via env var kalau primary gagal:

### Current Primary Models (Updated 2026-02-28)
- **Eos:** `gemini/gemini-3.1-pro-preview` (visual/PPT/design)
- **Argus:** `anthropic/claude-sonnet-4-6` (data/SQL/reports)
- **Codex:** `anthropic/k2p5` (web apps/full-stack)

### Fallback Commands (manual override)
```bash
# Eos fallback → Kimi K2.5 (cheapest capable)
NANOBOT_AGENTS__DEFAULTS__MODEL="kimi-coding/k2p5" NANOBOT_CONFIG_PATH=~/.nanobot/config-eos.json nanobot agent -m "[task]"
# Eos fallback → Sonnet 4.6 (highest quality)
NANOBOT_AGENTS__DEFAULTS__MODEL="anthropic/claude-sonnet-4-6" NANOBOT_CONFIG_PATH=~/.nanobot/config-eos.json nanobot agent -m "[task]"

# Argus fallback → Kimi K2.5
NANOBOT_AGENTS__DEFAULTS__MODEL="kimi-coding/k2p5" NANOBOT_CONFIG_PATH=~/.nanobot/config-argus.json nanobot agent -m "[task]"
# Argus fallback → Gemini 3 Flash
NANOBOT_AGENTS__DEFAULTS__MODEL="gemini/gemini-3-flash-preview" NANOBOT_CONFIG_PATH=~/.nanobot/config-argus.json nanobot agent -m "[task]"

# Codex fallback → Sonnet 4.6
NANOBOT_AGENTS__DEFAULTS__MODEL="anthropic/claude-sonnet-4-6" NANOBOT_CONFIG_PATH=~/.nanobot/config-codex.json nanobot agent -m "[task]"
# Codex fallback → Gemini 3 Flash
NANOBOT_AGENTS__DEFAULTS__MODEL="gemini/gemini-3-flash-preview" NANOBOT_CONFIG_PATH=~/.nanobot/config-codex.json nanobot agent -m "[task]"
```

### 🇨🇳 OpenRouter Cheap Chinese AI (PENDING — need API key)
Kalau OpenRouter API key sudah dikonfigurasi, fallback ultra-murah:
- Eos → `openrouter/qwen/qwen3-coder-30b-a3b-instruct` ($0.07/$0.27 per M tokens)
- Argus → `openrouter/baidu/ernie-4.5-21b-a3b` ($0.07/$0.28 per M tokens)
- Codex → `openrouter/deepseek/deepseek-v3.2` ($0.25/$0.40 per M tokens)
- Budget: `openrouter/qwen/qwen3-coder:free` (rate-limited, $0)

**TODO:** Tambahkan OpenRouter API key ke semua nanobot configs (providers.openrouter.apiKey).

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

## Agent Browser (Vercel Labs)

**Binary:** `/Users/database-zuma/homebrew/bin/agent-browser` (v0.15.1 — LATEST) ✅ INSTALLED & TESTED
**Repo:** https://github.com/vercel-labs/agent-browser (16.5k stars, Apache 2.0)
**Tech:** Rust CLI + Node.js daemon | **Browser:** Chromium (also Firefox/WebKit)
**Install date:** 2026-02-27 | **Status:** Production-ready

### Keunggulan vs Playwright MCP
- **93% less context** — ~400 chars output vs 4000+ chars Playwright
- **95% first-try success rate** — fewer retry loops needed
- **Speed:** Rust-based CLI = sub-millisecond parsing overhead
- **50+ commands** — full browser automation (not just basic 9)
- **Security:** Auth vault (encrypted), domain allowlist, action policies (v0.15.0)

### Quick Reference (Most Used)
```bash
agent-browser open <url>              # Navigate
agent-browser snapshot -i             # Interactive elements only (AI-optimal)
agent-browser snapshot -i --json      # Machine-readable output
agent-browser click @e2               # Click by ref from snapshot
agent-browser fill @e3 "text"          # Clear + fill input
agent-browser screenshot --annotate   # Numbered labels on elements
agent-browser get text @e1            # Get element text content
agent-browser find role button click --name "Submit"  # Semantic locator
agent-browser wait --load networkidle # Wait for page load
agent-browser eval <js>               # Run JavaScript
agent-browser diff snapshot           # Compare current vs last snapshot
agent-browser network requests        # View tracked network requests
agent-browser --session agent1 open url  # Isolated session per agent
```

### Full Command Categories
50+ commands across: **Core Interaction** | **Observation** (snapshot, screenshot, get, is) | **Semantic Find** | **Wait** | **Mouse** | **Diff** (v0.13+) | **Tabs/Windows/Frames** | **Settings** | **Cookies/Storage** | **Network Interception** | **Debug/Profiling** | **State Management** | **Security/Auth** (v0.15+) | **Sessions/Profiles** | **CDP Connect** | **Cloud Providers** (Browserbase, Kernel, BrowserUse) | **iOS Simulator**

**Full reference:** `knowledge/dev-tools/2026-02-27_agent-browser.md`

### Who Can Use?
✅ Iris (Mac Mini) | ✅ All sub-agents (Metis, Daedalus, Hermes, Oracle) | ✅ All nanobots (Eos, Argus, Codex) | ✅ All CLIs (opencode, claude-code, kimi-cli)

### When to Use
- Prefer when: Light automation, token budget tight, 1st-try matters, multi-agent sessions
- Avoid when: Complex multi-step with heavy context (use Playwright MCP instead)
- Best for: Quick snapshots, form fills, element clicks, network inspection, visual diff
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

## Daily Automation — Q1 2026 (Updated 2026-02-27)

### Planogram
- **Main source:** `portal.planogram_existing_q1_2026` (51 toko, 606 artikel, 42 size cols + BOX)
- **For:** RO requests, planogram analysis, store-level queries

### FF/FA/FS Metrics (Daily)
- **Table:** `mart.ff_fa_fs_daily_q1_2026` (51 toko, refreshed daily at 03:XX+ WIB)
- **Script:** `/opt/openclaw/scripts/calculate_ff_fa_fs_q12026.py` (runs after 03:00 stock pull)
- **Status JSON:** `/opt/openclaw/logs/ff_fa_fs_q12026_latest_status.json` (→ use for daily morning report)
- **OLD (deprecated):** `/opt/openclaw/logs/ff_fa_fs_latest_status.json` ❌ DO NOT USE
- **Cron:** 03:00 stock pull → 03:XX+ FF/FA/FS calc → 05:30 Atlas health check reads status JSON

## Google Drive (gog CLI)

**Binary:** `~/homebrew/Cellar/gogcli/0.9.0/bin/gog` | **Account:** harveywayan@gmail.com
**Auth Status:** ✅ Authenticated (drive, sheets) — 2026-02-20
**Services:** drive, sheets

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

### gog OAuth Troubleshooting
Unlock keychain → `gog auth add --manual harveywayan@gmail.com --services drive,sheets` → state harus match (jangan restart antara URL & paste). Detail: `docs/gog-oauth-troubleshooting.md`

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

## OpenClaw Skills

**Location:** `~/homebrew/lib/node_modules/openclaw/skills/`

| Skill | Use Case |
|-------|---------|
| `nano-pdf` | PDF generation via AI |
| `nano-banana-pro` | Image generation (Gemini 3 Pro Image) |
| `openai-whisper` | Speech-to-text |
| `peekaboo` | Screen capture/analysis |
| `video-frames` | Extract frames from video |
| `voice-call` | Voice call capability |
| `obsidian` | Obsidian vault skill |

**PPT/DECK RULE (2026-02-20, Wayan — PERMANENT):**
- **Agent:** ALWAYS Eos 🌅 (Gemini 3.1 Pro)
- **Format:** HTML + Tailwind CSS (single .html file, self-contained, print-friendly)
- **Style:** Reference Zuma deck templates (see workspace/zuma-business-skills/ + Active URLs in MEMORY.md)
- **Design:** Zuma brand (teal #002A3A, green #00E273) + smooth animations on slides
- **Animations:** Include CSS transitions/fade effects on slide navigation (tested & approved by Wayan on tier8-analysis.vercel.app)
- **Never:** python-pptx (unless user explicitly requests ".pptx")
- **⚠️ DELIVERY (MANDATORY):** Vercel live URL ONLY (NOT GDrive)
  - Vercel live URL is the final output to user
  - .html files deploy directly to Vercel (no build needed)
  - Example: https://tier8-analysis.vercel.app
- **NEVER send GDrive link** for PPT requests — always deliver Vercel live deck URL

## Python Libraries
All installed: `pdfplumber`, `PyMuPDF`, `reportlab`, `gspread`, `matplotlib`, `firecrawl-py`, `google-genai`, `psycopg2-binary`, `openpyxl`, `xlsxwriter`, `python-pptx`, `pandas`, `numpy`.

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
| Duo D | `120363426622392503@g.us` |

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

## Obsidian Vault
Path: `~/.openclaw/obsidian-vault/` | MCP: `mcp-obsidian` | Also direct file access.

## MCP Servers
Installed (perlu config): `mcp-obsidian`, `figma-developer-mcp`, `shadcn-ui-mcp-server`

## Control Stock Sheet (PO Tracking)

**Source:** Google Sheets dari Mbak Citra
**Sheet ID:** `1qInTrRUOUi2983vefS8doS5Pt3jC2yftQAG99yYlVOE` | **Sheet:** `PO`
**Rule (Wayan 2026-02-18):** Kalau user tanya PO → CEK SHEET INI DULU sebelum query database.
**Isi:** Rekap PO 2025 — per artikel, tier, status PO, jumlah PO/RCV.

## 🧠 Vector Memory Search (NEW — 2026-02-27)

**Semantic search over Iris memory + knowledge via pgvector.**

| Component | Detail |
|-----------|--------|
| DB Table | `iris.memory_vectors` (PostgreSQL VPS) |
| Embedding Model | Gemini `gemini-embedding-001` (3072 dims) |
| Scripts | `scripts/embed_memory.py`, `scripts/search_memory.py`, `scripts/extract_signals.py` |
| Data | 438 chunks from 18 memory files + 18 knowledge files |
| Cost | ~$0.0001/day (basically free) |

### Quick Reference
```bash
# Search memories semantically
python3 scripts/search_memory.py "query here"
python3 scripts/search_memory.py "query" --limit 10 --since 2026-02-20
python3 scripts/search_memory.py --json "query"  # for programmatic use
python3 scripts/search_memory.py "query" --source memory  # memory only
python3 scripts/search_memory.py "query" --source knowledge  # knowledge only

# Signal-aware search (NEW — 2026-02-28)
python3 scripts/search_memory.py "query" --type decision     # filter by signal type
python3 scripts/search_memory.py "query" --important          # importance >= 4 only
python3 scripts/search_memory.py "query" --min-importance 3   # importance >= N
python3 scripts/search_memory.py "query" --type lesson --important  # combine filters

# Embed new/changed memories
python3 scripts/embed_memory.py                  # incremental (new only) + auto-classify
python3 scripts/embed_memory.py --include-knowledge  # + knowledge files + auto-classify
python3 scripts/embed_memory.py --full             # re-embed everything + auto-classify
python3 scripts/embed_memory.py --no-classify       # embed only, skip signal classification
python3 scripts/embed_memory.py --stats             # show stats

# Signal extraction (classify existing chunks)
python3 scripts/extract_signals.py                  # unclassified chunks only
python3 scripts/extract_signals.py --full            # re-classify all
python3 scripts/extract_signals.py --since 2026-02-20  # from date
python3 scripts/extract_signals.py --stats           # show distribution
python3 scripts/extract_signals.py --dry-run         # preview without writing
python3 scripts/extract_signals.py --limit 20        # process N chunks max
```

### When to Use
- **Semantic search**: context retrieval, "kapan terakhir bahas X?", finding related memories
- **Signal-filtered search**: find decisions (`--type decision`), lessons (`--type lesson`), critical items (`--important`)
- **Grep (fallback)**: exact keyword, error codes, phone numbers, file names
- **After writing memory**: run `embed_memory.py` to index new entries (auto-classifies signals)
- **Manual classify**: run `extract_signals.py` directly if needed (embed_memory.py now calls it automatically)

### 🏷️ Signal Types
| Type | Description | Example |
|------|------------|---------|
| `decision` | Choice or decision made | "Switched Iris to Sonnet 4.6" |
| `preference` | User preference expressed | "Wayan prefers HTML+Tailwind for PPT" |
| `correction` | Mistake corrected | "Fixed fallback chain — only tries 2 models" |
| `lesson` | Something learned | "Nanobot doesn't support auto fallback" |
| `pattern` | Recurring behavior/issue | "User asks about planogram every Monday" |
| `error` | Technical failure/bug | "Gemini API 429 rate limit during embed" |
| `fact` | Factual information | "VPS IP: 76.13.194.120" |
| `task` | Task done/requested/pending | "Compiled ARCHITECTURE.md" |

Importance: 1 (trivial) → 5 (critical). `--important` = importance ≥ 4.

### 🪞 Daily Reflection
- Triggered at **22:00 WIB** (last heartbeat before quiet hours)
- Output: `memory/reflections/YYYY-MM-DD.md`
- See `AGENTS.md § Daily Reflection Protocol` for format
---

## MarkItDown (File → Markdown Converter)

Convert file apapun ke Markdown — biar kamu bisa baca isinya.

```bash
# Basic usage
markitdown /path/to/file.pdf
markitdown /path/to/file.pptx
markitdown /path/to/file.xlsx
markitdown /path/to/file.docx

# Save ke file
markitdown /path/to/file.pdf -o /tmp/output.md
```

**Supported:** PDF, PPTX, DOCX, XLSX, XLS, HTML, CSV, JSON, XML, ZIP, images (OCR), audio, YouTube URLs, EPub.

**Kapan pakai:** User kirim file via WA → convert dulu pakai markitdown → baru baca & proses isinya. Exec via `exec` tool.
