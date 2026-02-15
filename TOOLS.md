# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

### Credentials

Semua credentials tersimpan di `/Users/database-zuma/.openclaw/workspace/.env` — JANGAN pernah commit/push file ini.
Isi: GitHub token, Vercel token, PostgreSQL connection string, Notion API key.
Load dengan `source .env` atau `python-dotenv`.

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
When uploading files to Google Drive, ALWAYS grant edit access to:
- `wayan@zuma.id` (role: writer)
- `database@zuma.id` (role: writer)

```bash
# Upload file
gog drive upload <file> --name "..." --json

# Share with edit access
gog drive share <file_id> --email wayan@zuma.id --role writer
gog drive share <file_id> --email database@zuma.id --role writer

# Public link (optional)
gog drive share <file_id> --anyone --role reader
```

**Standard workflow:**
1. Upload file → get file_id
2. Share edit access to wayan@zuma.id & database@zuma.id
3. Share public link (reader) if needed
4. Reply with shareable link

### OpenCode (Primary Coding Tool) 🧠

**Binary:** `opencode` (installed on Mac mini)
**Config:** Uses OhMyClaude Code framework

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
- **Note:** Need phone numbers to mention properly (e.g., +628983539659 for Wayan)
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

**Rule verified by:** User +6285101726716 (2026-02-12 08:41-08:44)

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
