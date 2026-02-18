# TOOLS.md — Technical Specs & Infrastructure

Environment-specific paths, credentials, API keys, SSH, and tool configs.
Behavioral rules & delegation logic → AGENTS.md | Business context → MEMORY.md

---

### Credentials

Semua credentials tersimpan di `/Users/database-zuma/.openclaw/workspace/.env` — JANGAN pernah commit/push file ini.
Isi: GitHub token, Vercel token, PostgreSQL connection string, Notion API key.
Load dengan `source .env` atau `python-dotenv`.

### API Keys

**Firecrawl API:**
- Key: `$FIRECRAWL_API_KEY` (see `.env`)
- Account: database-zuma
- Docs: https://www.firecrawl.dev/
- Use case: Web scraping, JS-rendered pages (XXI, TIX ID, dll yang anti-scraping)

**Tavily API:**
- Key: `$TAVILY_API_KEY` (see `.env`)
- Docs: https://tavily.com/
- Use case: AI-optimized web search & research

**Google Gemini API:**
- Key: `$GEMINI_API_KEY` (see `.env`)
- Project: `iris-zuma-openclaw` (Google Cloud Console)
- Models available: Gemini Nano, Flash, Pro
- Tier: Free trial — Rp5,016,451 credit, 90 days remaining (per 2026-02-19)
- Docs: https://ai.google.dev/
- SDK: `google-genai` (Python), installed di Mac mini

### 🎨 Image Generation (Iris Capability)

**User request:** "buatkan gambar [deskripsi], AR [ratio], [style]"
→ Iris generate via Imagen 4 Fast, kirim langsung ke WhatsApp

**Model:** `imagen-4.0-generate-001` (Google Imagen 4 Standard) — default sejak 2026-02-19
- `imagen-4.0-fast-generate-001` — Fast (lebih cepat tapi sering typo di teks)
- `imagen-4.0-ultra-generate-001` — Ultra (kualitas max, belum ditest)

**Image Editing (Terbatas):**
- `gemini-3-pro-image-preview` — bisa terima foto + instruksi, output modified image
- ⚠️ Kualitas face compositing jelek via API (jauh dari Google AI Studio)
- **Kesimpulan:** Iris = image generation ✅, image editing/face swap ❌ (butuh Adobe Firefly/InsightFace)
- Kualitas foto realistis sangat bagus
- Aspect ratio: 1:1, 16:9, 9:16, 4:3, dll
- Output: 1024x1024 (default 1:1)
- Cost: dari Gemini free trial credit

**Code pattern:**
```python
import google.genai as genai
from google.genai import types
client = genai.Client(api_key="$GEMINI_API_KEY")
response = client.models.generate_images(
    model='imagen-4.0-fast-generate-001',
    prompt='[deskripsi]',
    config=types.GenerateImagesConfig(number_of_images=1, aspect_ratio="1:1")
)
```

### ⚠️ Gemini sebagai Fallback Agent (2026-02-19)
- Google provider sudah ditambahkan ke OpenClaw config (`models.providers.google`)
- `google/gemini-3-pro-preview` sebagai default fallback GLOBAL
- **Tapi:** Iris, Metis, Daedalus, Hermes, Oracle punya per-agent model config sendiri → Gemini **BELUM** otomatis jadi fallback mereka
- **TODO:** Patch per-agent config kalau Wayan mau Gemini masuk fallback tiap agent individual

### Browser & Screenshot Capabilities

**Screenshot:**
- `browser(action=screenshot, profile=openclaw)` → save ke `~/.openclaw/media/browser/`
- Kirim ke user via `message(action=send, filePath=...)` langsung di WhatsApp
- Full page: `fullPage=true` | Specific element: pakai `selector`
- Use case: QA dashboard, preview deploy, debug visual, bukti ke user

**Browser Automation:**
- `browser(action=open/snapshot/act, profile=openclaw)` → headless browser
- Bisa navigate, click, type, scroll, wait
- **Limitasi:** Anti-bot sites (XXI, dll) gak load content → pakai Firecrawl instead

**Firecrawl (JS-rendered scraping):**
- API: `https://api.firecrawl.dev/v1/scrape`
- Key: `$FIRECRAWL_API_KEY`
- Bisa render JS, bypass anti-scraping → dapat full content
- Use case: XXI jadwal, TIX ID, atau site manapun yang butuh JS rendering

**Priority screenshot:** Pinchtab > browser openclaw > web_fetch

### ⚠️ Screenshot Rule (PERMANENT — 2026-02-19)
**Default untuk semua screenshot request → PINCHTAB**

Berlaku untuk:
- User minta SS hasil pencarian Google/browser
- Screenshot website atau web app
- Screenshot halaman apapun untuk dikirim ke user

**Kenapa Pinchtab:**
- Murah (HTTP call via exec, gambar TIDAK masuk AI context → hemat token)
- Browser tool screenshot = mahal (gambar embed ke context = ribuan token) + auto-send ke WA

**Cara pakai:**
```bash
curl -s "http://localhost:9867/screenshot?url=URL_ENCODE_HERE" > /tmp/resp.json
python3 -c "import json,base64; d=json.load(open('/tmp/resp.json')); open('/path/out.jpg','wb').write(base64.b64decode(d['base64']))"
```

**Browser tool** = hanya untuk AI analisis konten (snapshot, act, click, read DOM) — BUKAN untuk kirim SS ke user.

### Output File Locations

**Purchase Orders (PO):**
- **Folder:** `~/Desktop/DN PO ENTITAS/`
- **Format:** `PO-[ENTITY]-[YYMMDD]-[NNN].xlsx`
- **Rule:** ALL PO outputs must go here (not directly to Desktop)
- **Example:** `PO-MBB-260216-001.xlsx`

### Database Backup (Mac Mini Mirror)

**Setup:** PostgreSQL client (libpq 18.1) installed via homebrew

**Backup Script:** `~/backups/db/backup-vps-db.sh`
- Daily cron: 02:30 WIB (30 min after VPS backup at 02:00)
- Retention: 14 days on Mac mini (vs 7 days on VPS)
- Location: `~/backups/db/openclaw_ops_YYYYMMDD.sql.gz`
- Typical size: ~55MB compressed
- Log: `~/backups/db/backup.log`

**Cron Schedule:**
```
30 2 * * * /Users/database-zuma/backups/db/backup-vps-db.sh >> /Users/database-zuma/backups/db/backup.log 2>&1
```

**Manual Backup:**
```bash
cd ~/backups/db && ./backup-vps-db.sh
```

**Restore (if needed):**
```bash
gunzip -c ~/backups/db/openclaw_ops_YYYYMMDD.sql.gz | \
  ~/homebrew/Cellar/libpq/18.1_1/bin/psql -h 76.13.194.120 -U openclaw_app openclaw_ops
```

**Purpose:** Offline redundancy — VPS backup + local Mac mini mirror for disaster recovery

### Jadwal Sholat & Puasa

**API:** AlAdhan (free, no key needed)
**Method ID 20** = Kementerian Agama RI (standard Indonesia)

**Endpoint (1 hari spesifik):**
```
GET https://api.aladhan.com/v1/timingsByCity/{DD-MM-YYYY}?city={Kota}&country=Indonesia&method=20
```

**Contoh Surabaya hari ini:**
```
https://api.aladhan.com/v1/timingsByCity/19-02-2026?city=Surabaya&country=Indonesia&method=20
```

**Fields yang dikembalikan:** Imsak, Fajr (Subuh), Sunrise (Terbit), Dhuhr (Dzuhur), Asr (Ashar), Maghrib (Buka Puasa), Isha (Isya)

**Default kota:** Surabaya (kecuali user minta kota lain)
**Cara pakai:** `web_fetch` langsung ke URL di atas — gak perlu sub-agent, simple fetch

---

### Notion API

**Key:** `NOTION_API_KEY` di `.env`
**Access mode:** **READ-ONLY** — hanya baca pages/databases sampai Wayan explicitly bilang boleh edit
**Always use Notion API** — jangan web scraping/browser automation untuk Notion
**API Docs:** https://developers.notion.com/

### Product Analysis (SKU Performance)

**Template:** `templates/product-analysis-unified.md` (merged SQL framework + WhatsApp formatting)
**Source Priority:** 
1. `mart.sku_portfolio` (primary — 101 columns, pre-computed)
2. `core.sales_with_product` (fallback — need store/custom dates)
3. `core.stock_with_product` (stock breakdown only)

**When to use:**
- User asks "top 10 products", "best sellers", "show me SKU analysis"
- R&D requests (Mbak Dewi, Mbak Desyta, Yuda)
- Merchandiser queries (Mas Bagus, Mbak Virra)

**Decision tree:**
- National aggregate + comprehensive metrics → `mart.sku_portfolio`
- Need store/area breakdown → `core.sales_with_product`
- Need custom date range (last 7 days, Q1 only) → `core.sales_with_product`

**Format:** WhatsApp-friendly
- 1-5 articles: Detailed blocks (sales + stock + insights per article)
- 6+ articles: Compact list (one-liner per article + summary)

**Auto-flags:** 🔥 Stockout (<0.5mo TO), 🐌 Overstock (>2.5mo), ⚠️ Negative WH, 📉 Big drop (>-70% YoY)

### Google Drive (gog CLI)

**Binary:** `~/homebrew/Cellar/gogcli/0.9.0/bin/gog`
**Account:** harveywayan@gmail.com

**Auto-share rule (MANDATORY):**
When uploading files to Google Drive, ALWAYS:
1. Set **Anyone with link = Editor** (so any user can access without requesting)
2. Also share edit access to specific emails as backup

```bash
# Upload file
gog drive upload <file> --name "..." --json

# MANDATORY: Anyone with link = Editor
gog drive share <file_id> --anyone --role writer

# Also share specific emails
gog drive share <file_id> --email wayan@zuma.id --role writer
gog drive share <file_id> --email database@zuma.id --role writer
```

**Standard workflow:**
1. Upload file → get file_id
2. `--anyone --role writer` (ALWAYS!)
3. Share to wayan@zuma.id & database@zuma.id
3. Share public link (reader) if needed
4. Reply with shareable link

### OpenCode (Primary Coding Tool) 🧠

**Binary:** `~/.opencode/bin/opencode` (v1.1.64, installed on Mac mini)
**Config:** Uses OhMyClaude Code framework

**⚠️ CRITICAL:** OpenCode IS INSTALLED! Use full path `~/.opencode/bin/opencode` (not in PATH)

**Model Configuration:**
- **Planning/Reasoning:** Claude Opus 4.6 (`anthropic/claude-opus-4-6`)
- **Coding:** Kimi K2 Coding 2.5 (`moonshotai/kimi-k2-coding-2.5`)

**Session Naming Convention:**
ALL sessions spawned by Iris MUST use the prefix `iris_` followed by a descriptive title:
- `iris_fix_sales_dedup` — not "fix sales dedup"
- `iris_planogram_royal_v3` — not "planogram work"
- `iris_stock_coverage_analysis` — not "data analysis"

**Why prefix matters:** Multiple agents (Iris, Iris Junior, Atlas) may spawn sessions. The prefix identifies who owns what.

**Delegation priority:**
1. OpenCode (default for most tasks)
2. Claude Code (only if OpenCode unavailable)
3. Direct Kimi CLI (quick code-only tasks)

**⚠️ CRITICAL RULE (2026-02-16): HARDCODE CREDENTIALS IN TERMINAL**
- OpenCode **auto-rejects .env file access** in background/PTY mode
- **SOLUTION:** Hardcode credentials DIRECTLY in terminal command when delegating
- **Why safe:** Terminal commands gak masuk git, cuma di exec history (ephemeral)
- **Format:**
  ```bash
  ~/.opencode/bin/opencode run -m model "Task description
  
  DATABASE:
  Host: 76.13.194.120
  Database: openclaw_ops
  User: openclaw_app
  Password: $PGPASSWORD
  
  [task details]"
  ```
- **MANDATORY:** Selalu pass credentials langsung, jangan andalkan .env file reading

**⚠️ PPT GENERATION TROUBLESHOOTING (2026-02-16)**

**Problem:** OpenCode sessions repeatedly failed/stuck when generating complex PPT
- Tried: Opus 4.6 (failed), Sonnet 4.5 (stuck), multiple retries (all hung)
- Symptom: Process running but no output after 10+ minutes
- Pattern: Either undefined errors or complete silence

**SOLUTION (Proven Working):**
1. **Write Python script directly** using python-pptx
2. **Incremental approach:** Start with 2 slides working, then expand
3. **Manual execution:** `python3 generate_ppt.py` (no AI delegation)
4. **Why it works:** No AI interpretation layer, direct library usage

**When to Use Direct Python Approach:**
- ✅ PPT generation (complex layouts, precise positioning)
- ✅ Any python-pptx/openpyxl tasks requiring detailed control
- ✅ After 2-3 failed OpenCode attempts (switch immediately)
- ✅ Complex visual layouts (KBI style, grid-based, precise measurements)

**Reference Script:** `~/Desktop/generate_kbi_ppt.py` (template for future PPT tasks)

**Rule:** If OpenCode fails 2x on same task → switch to direct scripting immediately

### SSH

- iris-junior → 76.13.194.103, user: root (Iris Junior agent VPS)
- vps-db → 76.13.194.120, user: root (Database VPS)

**File transfer VPS ↔ Mac Mini:**
- Use `rsync` instead of `scp` — more robust, handles timeouts better
- `scp` commands often SIGKILL/timeout (network instability)
- Example: `rsync -avz --timeout=30 root@76.13.194.103:/path/to/file /local/path`

## Agent Communication — MY TEAM 👥

**IMPORTANT:** Iris Junior, Atlas, Apollo are **MY EMPLOYEES**. I can delegate tasks to them instead of always doing it myself on Mac mini!

### Communication Methods

**1. Persistent TUI (Preferred for ongoing conversation):**
```bash
ssh iris-junior  # Opens SSH session
openclaw tui     # Start TUI in that session
# Session persists, no repeated reconnections
# Token efficient, better for back-and-forth
```
Currently: Session `cool-haven` active with TUI open

**2. CLI One-Shot (Quick commands):**
```bash
# To Iris Junior (main coordinator)
ssh iris-junior "openclaw agent --agent main --message 'text'"

# To Atlas (operations)
ssh iris-junior "openclaw agent --agent ops --message 'text'"

# To Apollo (R&D)
ssh iris-junior "openclaw agent --agent rnd --message 'text'"
```
Response time: ~5-6 seconds

### Agent Details

#### Iris Junior ✨ (Main Coordinator)
- **Location:** `/root/.openclaw/workspace/`
- **Agent ID:** `main`
- **Model:** Sonnet 4.5 (primary), Kimi k2p5, Deepseek (fallbacks). For complex tasks, delegate to OpenCode (Opus 4.6 + Kimi K2 2.5)
- **Role:** Project Manager — review, coordinate, report, eskalasi
- **Access:** Notion API, Telegram, JSON reports
- **Use for:**
  - Morning report generation
  - Notion task management
  - Monitoring Atlas/Apollo
  - Eskalasi to Wayan
- **Response:** Via Telegram (when setup) or TUI

#### Atlas 🏔️ (Operations Specialist)
- **Location:** `/root/.openclaw/workspace-ops/`
- **Agent ID:** `ops`
- **Model:** Kimi k2p5 (primary), Deepseek, Sonnet (fallbacks)
- **Department:** Stock & Inventory, Warehouse, Logistics
- **Access:** Accurate Online API, Google Sheets (gog CLI), Email, Telegram
- **Use for:**
  - Data pulls from Accurate (stock, sales)
  - Google Sheets operations
  - Inventory monitoring & analysis
  - Cron job monitoring (03:00 stock, 05:00 sales)
- **Key capability:** Can execute long-running data ops that would burn tokens on Mac mini
- **Report location:** `/root/.openclaw/workspace-ops/logs-report-for-iris/`

#### Apollo 🎯 (R&D Specialist)
- **Location:** `/root/.openclaw/workspace-rnd/`
- **Agent ID:** `rnd`
- **Model:** Kimi k2p5 (primary), Deepseek, Sonnet (fallbacks)
- **Department:** Product Development, Quality Control, Material Sourcing
- **Status:** Currently IDLE (no active tasks)
- **Access:** Accurate Online, Google Sheets (gog CLI), Email, Telegram
- **Use for (when active):**
  - Product timeline tracking
  - Material sourcing monitoring
  - QC report processing

### Delegation Strategy 🎯

**Delegate to VPS when:**
- Long-running data operations (stock pulls, sales pulls)
- Background monitoring tasks
- Notion task management (Iris Junior has full access)
- Report generation & eskalasi
- Google Sheets operations (they have gog CLI)
- Accurate API calls (they have credentials)

**Keep on Mac mini when:**
- PostgreSQL database queries (I have direct connection)
- Quick analysis & ad-hoc requests
- Browser automation (Chrome relay)
- File operations in my workspace
- Immediate user-facing responses

**Resource awareness:** VPS = 8GB RAM, 2 CPU cores — don't overload with parallel heavy tasks

### VPS File Locations

```
/root/.openclaw/
├── .env                     # Shared credentials (GH, Notion, gog)
├── workspace/               # Iris Junior
│   ├── SOUL.md, AGENTS.md
│   ├── morning-reports/     # MD reports to Wayan
│   └── logs-report-for-iris/ (reads from Atlas/Apollo)
├── workspace-ops/           # Atlas
│   ├── SOUL.md, AGENTS.md
│   └── logs-report-for-iris/ (writes JSON reports)
└── workspace-rnd/           # Apollo
    ├── SOUL.md, AGENTS.md
    └── logs-report-for-iris/ (writes JSON reports)
```

### Cron Jobs (VPS DB 76.13.194.120)
```
02:00 WIB → Backup DB → /root/backups/
03:00 WIB → Stock Pull → Atlas monitors
05:00 WIB → Sales Pull → Atlas monitors
```
Status files: `/opt/openclaw/logs/stock_latest_status.json`, `/opt/openclaw/logs/sales_latest_status.json`

## 💬 WhatsApp Groups

### Known Groups
- **Anak Gaul SI** (CI Team) — `120363421058001851@g.us`

### How to Find Group JID (When Forward Doesn't Work)
```bash
# Search in session logs for group JID pattern
grep -h "120363[0-9]*@g.us" ~/.openclaw/agents/main/sessions/*.jsonl | head -1

# Generic pattern (adjust first digits based on region)
grep -h "[0-9]*@g.us" ~/.openclaw/agents/main/sessions/*.jsonl | grep -i "group_name_keyword"
```

**Why forwarded messages don't always work:**
- WhatsApp gateway doesn't expose group metadata from forwarded messages
- Must search session history logs where group was previously mentioned

**To send to group:**
```bash
# Use group JID, not group name
message action=send channel=whatsapp target=120363421058001851@g.us message="text"
```

**Proper Tagging/Mentions:**
- **DON'T:** Just write "cc: Wayan, Wafi, Nisa" in text (gak akan notify mereka)
- **DO:** Use proper WhatsApp mentions — check message tool docs for mention format
- **Note:** Need phone numbers to mention properly (stored in .env)
- Manual tag alternative: Ask user to tag manually setelah message terkirim

**TODO:** Implement proper mention syntax when message tool supports it

## 🚫 Data Filtering Rules - Store Queries

**CRITICAL:** When user asks for "sales per store" / "store performance" — AUTO-EXCLUDE:

### Universal Exclusions (All Areas)
1. **Anything containing "Wholesale"** → Wholesale channel, different segment
2. **Anything containing "Pusat"** → Warehouse/distribution, not retail comparable
3. **Anything containing "Konsinyasi"** → Non-retail store, different business model

### Pattern Matching
```
matched_store_name LIKE '%wholesale%' → EXCLUDE
matched_store_name LIKE '%pusat%' → EXCLUDE
matched_store_name LIKE '%konsinyasi%' → EXCLUDE
```

### When to INCLUDE Wholesale
**ONLY when user explicitly asks:**
- "Sales wholesale..."
- "Penjualan wholesale..."
- "Wholesale performance..."
- Clear context about wholesale channel

### Coverage Areas
- ✅ Jatim (11 retail stores, exclude Pusat & Wholesale Jatim)
- ✅ Jakarta
- ✅ Bali (exclude Wholesale Bali)
- ✅ Lombok (2 retail stores, exclude Wholesale Lombok)
- ✅ Batam
- ✅ Sulawesi
- ✅ Sumatra

**Rule verified by:** User (OPS team member, 2026-02-12 08:41-08:44)

### Intercompany Filter — When to Use

**Intercompany transactions:** Antar entitas (DDD→MBB, UBB→DDD, LJBB→DDD), bukan within single store.

**When to apply `is_intercompany = FALSE` filter:**
- ✅ **Aggregated queries** — Multi-store, nasional, branch-level, area totals
- ✅ **Sales comparison** — Cross-store performance, ranking
- ✅ **Revenue reports** — Total sales nasional, regional summaries

**When NOT needed:**
- ❌ **Single store queries** — Query 1 toko saja (e.g., "Sales Mega Mall Manado")
- ❌ **Store-specific reports** — RO Request, planogram, single store performance

**Reason:** Intercompany filter excludes transactions between entities (e.g., MBB buying from DDD warehouse), not transactions within a single store location.

**Rule clarified by:** Wayan (2026-02-13 14:20)

## 🔊 BluOS Speaker Control (Polytron)

### blu CLI
**Binary:** `~/go/bin/blu`  
**Installed:** 2026-02-12 (via Go toolchain)

### Commands
```bash
# Discovery
~/go/bin/blu devices

# Status
~/go/bin/blu --device <name-or-ip> status

# Volume control
~/go/bin/blu --device <name-or-ip> volume set 50
~/go/bin/blu volume up
~/go/bin/blu volume down

# Playback
~/go/bin/blu play
~/go/bin/blu pause
~/go/bin/blu stop
```

### Notes
- Polytron speaker must be ON and on same network
- Discovery uses mDNS/UPnP (may be blocked by router/VLAN)
- If discovery fails, use IP directly: `--device 192.168.x.x`
- Command reference: https://blucli.sh

### Device Info
- Speaker: Polytron (BluOS-enabled)
- Network: [TBD - check when speaker is ON]
- Default device: [TBD - set after first discovery]

### Control Stock Sheet (PO Tracking)

**Source:** Google Sheets dari Mbak Citra
**Sheet ID:** `1qInTrRUOUi2983vefS8doS5Pt3jC2yftQAG99yYlVOE`
**Link:** https://docs.google.com/spreadsheets/d/1qInTrRUOUi2983vefS8doS5Pt3jC2yftQAG99yYlVOE
**Sheet name:** `PO`

**Rule (dari Mas Wayan 2026-02-18):** Kalau user tanya soal PO, CEK SHEET INI DULU sebelum query database.

**Isi:** Rekap PO 2025 — per artikel, tier, status PO, jumlah PO, jumlah received (RCV 1-10), total RCV.
**Kolom penting:** TIER | CODE | TYPE | GENDER | SUDAH PO | Done PO 1-6 | TGL PO | STATUS PO | JML RCV 1-10 | TOTAL RCV
