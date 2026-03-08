# 🌸 Iris — OpenClaw AI Agent Workspace Template

**A production-ready OpenClaw workspace for building your own personalized AI assistant.**

Iris is a lead AI agent designed to orchestrate tasks, manage data, coordinate other agents, and provide intelligent assistance. This template gives you everything you need to create your own version.

---

## ✨ Features

- **🎭 Persona-Driven**: Configurable identity, soul, and communication style
- **🧠 Long-Term Memory**: Structured memory system (daily logs + curated learnings)
- **💓 Proactive Heartbeats**: Optional periodic check-ins and background tasks
- **🔐 Multi-Level Access Control**: Admin vs. regular user permissions
- **🤝 Multi-Agent Orchestration**: Iris coordinates a 4-agent Mac Mini team
- **🗄️ Database Integration**: PostgreSQL connection via environment variables
- **📝 Notion Integration**: Built-in support for Notion API workspace access
- **🛡️ Security-First**: Anti-prompt-injection, credential management via .env
- **🌐 WhatsApp/Telegram/Discord Ready**: Works with OpenClaw messaging channels
- **🖥️ Virtual Computer**: Full Ubuntu desktop in Docker — headed Chrome, CDP automation, web desktop for spectating

---

## 🤖 Agent Team Architecture

Iris is **orchestrator-only** — all actual work is delegated to specialized sub-agents:

| Agent | ID | Role | Model | Notes |
|-------|----|------|-------|-------|
| 🌸 **Iris** | `main` | Orchestrator, user comms | Sonnet 4.5 | Responds to users, delegates everything |
| 🔮 **Metis** | `metis` | Data analyst, SQL queries | Sonnet 4.5 + Kimi K2.5 | PostgreSQL, business analysis |
| 🪶 **Daedalus** | `daedalus` | Code builder, PPT/HTML | Kimi K2.5 + Sonnet 4.5 | Scripts, Vercel deploys |
| 🪄 **Hermes** | `hermes` | Research, web, file ops | Sonnet 4.5 + Kimi K2.5 | Web search, knowledge dump |
| 🏛️ **Oracle** | `oracle` | Strategic advisor only | Opus 4.6 🔒 | MD output only, zero exec |

**Delegation rules:**
- Iris NEVER does task work herself → always `sessions_spawn` to the right agent
- Oracle has zero execution tools (advisory/strategy memos only)
- Each agent has its own workspace with `.env` symlinked from main

---

## 🖥️ Virtual Computer — Iris Has Her Own Desktop

Iris doesn't just run in a terminal — she has a **full virtual computer** running on a VPS. A complete Ubuntu XFCE desktop inside Docker, with a real headed Chrome browser, persistent sessions, and remote access for both AI automation and human spectating.

### Why This Exists

Most AI browser automation uses **headless Chrome** — Chrome running without a visible window. The problem? **Google blocks it.** Try logging into Gmail with headless Chrome and you'll hit CAPTCHA walls, security challenges, and account lockouts. Google's bot detection has gotten extremely sophisticated.

The solution: give Iris a **real computer with a real display**. Chrome runs in headed mode on a virtual XFCE desktop, making it indistinguishable from a human browsing. No CAPTCHAs, no blocks, persistent Gmail sessions that survive for weeks.

### Architecture

```
VPS (iris-junior)
│
├── 🌐 Port 3000/3001 → Web Desktop (human spectating)
│   └── Open in any browser → see Iris's desktop live
│   └── Click, type, interact — or just watch
│
├── 🔌 Port 9222 → Chrome DevTools Protocol (AI automation)
│   └── Iris connects via CDP → full browser control
│   └── Navigate, click, read DOM, fill forms, screenshot
│
└── 🖥️ Docker: iris-desktop (linuxserver/webtop:ubuntu-xfce)
    ├── Full Ubuntu OS (not just a browser)
    ├── XFCE desktop environment
    ├── Google Chrome 145+ (headed, with display)
    ├── Persistent volume (/config) — survives restarts
    └── Extensible — install any Linux tool
```

### The Chrome CDP Localhost Bug (Critical Discovery)

**Chrome M113+ (2023) silently hardcodes the CDP debug listener to `127.0.0.1`.** The `--remote-debugging-address=0.0.0.0` flag is ignored — Chrome's source code (`headless_browser_main_parts.cc`) explicitly overrides it. This means Docker's port mapping can't reach Chrome's CDP.

Hundreds of guides online recommend the `0.0.0.0` flag. **They're all outdated.**

**The fix: a `socat` TCP bridge.**

```
External :9222 (0.0.0.0) ──socat──▶ Internal :9223 (127.0.0.1/Chrome CDP)
```

socat listens on `0.0.0.0:9222`, forwards to Chrome's `127.0.0.1:9223`. Simple, reliable, zero Chrome patching needed.

### What Makes This Special

| Feature | Detail |
|---------|--------|
| **Headed Chrome** | Real browser with display — Google can't distinguish from human |
| **Web Desktop** | Human opens a URL → sees Iris's desktop live, can interact |
| **CDP Automation** | AI connects via WebSocket → full programmatic browser control |
| **Persistent Sessions** | Gmail login survives container restarts (persistent Chrome profile) |
| **Full OS** | Not just Chrome — install Python, Node.js, htop, anything |
| **Auto-Recovery** | Watchdog script + XFCE autostart → Chrome & socat restart if they die |
| **Lightweight** | ~600MB RAM idle, ~1.2GB active browsing |

### Human Spectating

Open `https://YOUR_VPS_IP:3001/` in any browser — you see Iris's desktop in real time. You can:

- Watch Iris navigate websites, fill forms, click buttons
- Take over and interact (login to Gmail, Shopee Seller, etc.)
- Debug when automation goes wrong — see exactly what Iris sees
- It's like screen-sharing, but for your AI agent

### AI Automation via CDP

Connect with Playwright, Puppeteer, or any CDP client:

```javascript
// Playwright
const browser = await chromium.connectOverCDP('http://VPS_IP:9222');
const page = browser.contexts()[0].pages()[0];
await page.goto('https://mail.google.com');

// Puppeteer
const browser = await puppeteer.connect({ browserURL: 'http://VPS_IP:9222' });
```

### Failed Approaches (So You Don't Repeat Them)

| Approach | Why It Failed |
|----------|---------------|
| **browserless/chrome** | Headless only → Google blocks with CAPTCHA |
| **linuxserver/chromium** | Web UI but no CDP, port 6080 unreachable |
| **Custom Ubuntu + apt-get** | Chrome crashes (missing dbus), zombie processes (no init system) |

The winning combo: **linuxserver/webtop** (proper s6-overlay init, persistent volumes, built-in web desktop) + **socat bridge** (bypasses Chrome's CDP localhost hardcode).

### Full Technical Guide

See [`knowledge/dev-tools/2026-03-03_virtual-computer-docker-setup.md`](knowledge/dev-tools/2026-03-03_virtual-computer-docker-setup.md) for the complete step-by-step reproduction guide — including `docker-compose.yml`, init scripts, watchdog setup, troubleshooting, and all the gotchas we discovered.

---

## 🧭 Tool Routing & Decision Trees

Iris has multiple execution environments. She picks the right one automatically based on the task — not randomly.

### 🌐 Browser Task Decision Tree

Iris has four browser options, each with a specific use case:

```
User requests a web task
  │
  ├─ Needs login / persistent session?
  │   (Gmail, Shopee Seller, Tokopedia, any Google service)
  │   └─ YES → 🖥️  Virtual Computer (CDP ws://VPS_IP:9222)
  │               Full Ubuntu desktop, headed Chrome, persists login
  │
  ├─ Simple public scrape, no login needed?
  │   (competitor prices, articles, web search)
  │   └─ YES → 🔥 Firecrawl / Exa
  │               Fastest option, no browser overhead
  │
  ├─ Anti-bot site + needs clicking/filling, but no login?
  │   (Cloudflare-protected forms, JS-heavy sites)
  │   └─ YES → 🦊 Camofox (Firefox anti-detection, localhost:9377)
  │               Firefox fingerprint, C++ anti-detection layer
  │
  └─ Complex multi-step browser automation?
      └─ YES → 🖥️  Virtual Computer
```

**Rule of thumb:** If it needs a real login — virtual computer. If it's just fetching data — Firecrawl.

### 🧱 Code Execution Decision Tree (OpenSandbox)

OpenSandbox (Alibaba open-source, running at `http://127.0.0.1:8080`) creates isolated Docker containers for safe code execution. Daedalus is required to use it for untrusted code.

```
Sub-agent needs to execute a script
  │
  ├─ Short script, already known safe, one-liner?
  │   └─ OK → 💻 Mac Mini directly (fast, no overhead)
  │
  ├─ Script from user / external source / not yet reviewed?
  │   └─ MUST → 🧱 OpenSandbox (isolated Docker container)
  │
  ├─ Needs pip install / clean Python environment?
  │   └─ MUST → 🧱 OpenSandbox (fresh container per task)
  │
  ├─ Multiple scripts running in parallel?
  │   └─ MUST → 🧱 OpenSandbox (spin up N containers simultaneously)
  │
  └─ Long-running daemon / background process?
      └─ OK → 💻 Mac Mini directly (sandbox has 24h max timeout)
```

**Why this matters:** Without sandboxing, malicious code from an external source runs directly on the host machine. OpenSandbox ensures that even if untrusted code misbehaves, it’s contained.

**After every sandbox task:** Daedalus MUST delete the sandbox (`DELETE /v1/sandboxes/{id}`) to prevent resource leaks.

### 🤖 Agent Routing Table

Iris is orchestrator-only. Every task type is routed to the right specialist:

| Task Type | Primary Agent | Fallback | Notes |
|-----------|--------------|----------|-------|
| **PPT / deck / report** | Argus → Eos | — | Argus queries data → Eos renders. Zero exceptions. |
| **Code / web app / script** | Codex (nanobot) | Daedalus | Daedalus only if Mac Mini file system / git access needed |
| **Data / SQL / analysis** | Argus (nanobot) | Metis | Metis only if Argus context window insufficient |
| **Web research / scraping** | Argus (nanobot) | Hermes | Hermes only if login session required |
| **Browser automation w/ login** | Hermes | — | Shopee Seller, Tokopedia, X/Twitter |
| **Architecture / strategy** | Oracle | — | Advisory only — zero execution tools |

**Nanobots = Primary.** Sub-agents (Hermes, Daedalus, Metis) are fallbacks when nanobots can't handle the specific constraint (login session, Mac Mini file system, etc.).

### 📊 Execution Environment Summary

| Environment | Location | Best For |
|-------------|----------|----------|
| **Mac Mini direct** | Local bash/python | Internal scripts, git ops, file I/O |
| **OpenSandbox** | Isolated Docker (localhost:8080) | External code, clean env, parallel execution |
| **Virtual Computer (iris-desktop)** | VPS Ubuntu XFCE | Browser automation, login sessions |
| **Firecrawl / Exa** | API service | Public web scraping, no browser needed |
| **Camofox** | Local Firefox (localhost:9377) | Anti-bot sites without login |
---

## 🚀 Quick Start

### 1. Prerequisites

- [OpenClaw](https://openclaw.ai) installed and running
- Node.js 18+ (for OpenClaw)
- Optional: PostgreSQL database, Notion workspace, GitHub account

### 2. Clone This Template

```bash
git clone https://github.com/database-zuma/iris-openclaw-template.git
cd iris-openclaw-template
```

### 3. Configure Your Agent

#### A. Set up credentials

```bash
cp .env.example .env
# Edit .env with your actual tokens and credentials
```

#### B. Personalize your agent

Edit these files to match your needs:

- **`IDENTITY.md`** — Name, emoji, avatar
- **`SOUL.md`** — Personality, tone, boundaries
- **`USER.md`** — Your info, access levels, context
- **`MEMORY.md`** — Start building your agent's long-term memory
- **`TOOLS.md`** — Local setup notes (SSH, cameras, etc.)
- **`HEARTBEAT.md`** — Optional periodic tasks

### 4. Deploy to OpenClaw

Copy this workspace to your OpenClaw workspace directory:

```bash
# macOS/Linux default
cp -r . ~/.openclaw/workspace/

# Or specify custom workspace
export OPENCLAW_WORKSPACE=/path/to/workspace
cp -r . $OPENCLAW_WORKSPACE/
```

### 5. Start OpenClaw

```bash
openclaw gateway start  # Start the gateway daemon
openclaw tui            # Launch the text UI
```

---

## 🔄 Gateway Monitor (Auto-Restart)

Keep your OpenClaw gateway running 24/7 with automatic health checks and recovery.

### What It Monitors

| Check | Trigger Restart |
|-------|-----------------|
| **Gateway HTTP** | If `localhost:18789` unreachable |
| **WhatsApp channel** | If stopped or disconnected |
| **Agent health** | If bootstrapping >5min or stale >10min |

### Setup

1. **Create the monitor script** at `~/.openclaw/monitor-gateway.py`:

```python
#!/usr/bin/env python3
"""
OpenClaw Gateway + WhatsApp Health Monitor
Restarts gateway when WhatsApp disconnects or agent is stuck.
"""

import subprocess
import logging
import time
import re
from pathlib import Path

GATEWAY_URL = "http://127.0.0.1:18789"
OPENCLAW_BIN = "/Users/database-zuma/homebrew/bin/openclaw"
CHECK_INTERVAL = 120
AGENT_STALE_THRESHOLD = 600
BOOTSTRAPPING_GRACE = 300
RESTART_COOLDOWN = 600
LOG_FILE = Path.home() / ".openclaw" / "monitor-gateway.log"

# ... full script at: https://github.com/database-zuma/iris-openclaw-template
```

2. **Create LaunchAgent** (macOS) at `~/Library/LaunchAgents/com.openclaw.gateway-monitor.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.gateway-monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/database-zuma/.openclaw/monitor-gateway.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/Users/database-zuma/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/database-zuma/.openclaw/monitor-gateway-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/database-zuma/.openclaw/monitor-gateway-stderr.log</string>
</dict>
</plist>
```

3. **Load the service**:

```bash
launchctl load ~/Library/LaunchAgents/com.openclaw.gateway-monitor.plist
```

> **Note:** Update paths (`database-zuma`, `homebrew/bin`) to match your system.

### Check Logs

```bash
tail -f ~/.openclaw/monitor-gateway.log
```

Example output:
```
[INFO] OK | WA connected | agent active 2m ago | maxed sessions: 0
[WARNING] WhatsApp channel check FAILED: WhatsApp disconnected
[WARNING] Triggering restart: WhatsApp disconnected
[INFO] Gateway restart command succeeded
```

---

## 📂 Workspace Structure

```
.
├── AGENTS.md           # Agent behavior, delegation strategy, memory rules
├── BOOTSTRAP.md        # First-run setup guide (delete after initial setup)
├── HEARTBEAT.md        # Periodic background tasks (optional)
├── IDENTITY.md         # Agent name, emoji, role
├── MEMORY.md           # Long-term curated memories
├── SOUL.md             # Personality, tone, boundaries, security rules
├── TOOLS.md            # Local setup notes (SSH, devices, preferences)
├── USER.md             # Your info, access control, context
├── .env.example        # Template for credentials (copy to .env)
├── .gitignore          # Protects sensitive files
├── memory/             # Daily memory logs (YYYY-MM-DD.md)
│   └── reflections/    # Daily synthesized insights (auto-generated)
├── knowledge/          # Curated knowledge dump (links, tools, research)
│   ├── INDEX.md        # Master index
│   ├── ai-agents/      # Multi-agent architecture, tools, research
│   ├── dev-tools/      # Installed tools, libraries, CLIs
│   ├── business-ops/   # Operational processes, SOPs
│   └── design/         # Design references, brand guidelines
├── scripts/            # Automation scripts
│   ├── embed_memory.py # Vector memory indexer (pgvector)
│   └── search_memory.py# Semantic memory search CLI
└── README.md           # This file

---

## 🧠 Memory System

Iris uses a **three-tier memory system** with semantic search:

### Tier 1: Daily Logs (`memory/YYYY-MM-DD.md`)
- Raw logs of conversations and events
- Created automatically for each day
- Great for recent context (yesterday + today)

### Tier 2: Long-Term Memory (`MEMORY.md`)
- Curated learnings and key facts
- Manually updated (by you or the agent during heartbeats)
- Persistent knowledge across sessions

### Tier 3: Vector Memory Search (`iris.memory_vectors` via pgvector)

**NEW (2026-02-27)** — Iris now has **semantic memory search** powered by pgvector on PostgreSQL. Instead of exact keyword matching (`grep`), Iris retrieves memories by meaning using vector similarity.

**How it works:**

```
User asks: "kapan terakhir bahas masalah pengiriman?"

BEFORE (grep):  searches for exact word "pengiriman" → misses "delay ekspedisi JNE"
AFTER (vector):  understands MEANING → finds "delay ekspedisi JNE", "stock sync terlambat", "PO belum sampai"
```

**Architecture:**

```
Memory Write:  Iris writes memory/YYYY-MM-DD.md
                → embed_memory.py reads + chunks entries
                → Gemini embedding API generates vectors (3072 dims)
                → Upserts to iris.memory_vectors table (PostgreSQL + pgvector)

Memory Search: User asks question needing context
                → search_memory.py embeds the query
                → Cosine similarity search against all stored memories
                → Returns top-K most relevant memory chunks
                → Iris uses as context for response
```

**Components:**

| Component | Detail |
|-----------|--------|
| Database | PostgreSQL + pgvector extension |
| Embedding model | Gemini `gemini-embedding-001` (3072 dims, free tier) |
| Index script | `scripts/embed_memory.py` — batch embed memory + knowledge files |
| Search script | `scripts/search_memory.py` — semantic query CLI |
| Cost | ~$0.0001/day (effectively free) |

**Usage:**

```bash
# Search memories semantically
python3 scripts/search_memory.py "what was discussed about planogram?"
python3 scripts/search_memory.py "database error" --limit 10 --since 2026-02-20
python3 scripts/search_memory.py --json "query"  # JSON output for programmatic use
python3 scripts/search_memory.py "query" --source knowledge  # search knowledge only

# Embed new/changed memories into vector DB
python3 scripts/embed_memory.py                    # incremental (new entries only)
python3 scripts/embed_memory.py --include-knowledge  # also embed knowledge/ files
python3 scripts/embed_memory.py --full               # re-embed everything
python3 scripts/embed_memory.py --stats               # show embedding statistics
```

**When to use which:**
- **Semantic search**: context retrieval, finding related past discussions, pattern discovery
- **Grep (fallback)**: exact keywords, error codes, phone numbers, file names

### 🪞 Daily Reflection Cycle

**NEW (2026-02-27)** — At the last heartbeat before quiet hours (22:00), Iris automatically synthesizes the day's interactions into structured insights.

**The loop:** `log raw interactions → reflect at end of day → extract patterns → improve tomorrow`

**Output:** `memory/reflections/YYYY-MM-DD.md`

```markdown
## Reflection — 2026-02-27
### 🔁 Patterns
- User focused on planogram 3 days straight → likely preparing store revamp
### ❌ Issues
- Metis failed SQL 2x due to schema change → need schema sync job
### 📋 Tomorrow
- Prioritize planogram-related requests
- Run schema check on raw.* tables
### 💡 Systemic
- Update AGENTS.md: add schema validation before SQL queries
```

Reflections are also embedded into the vector DB, so future queries can recall synthesized insights — not just raw logs.

**Inspired by:** [a16z-infra/ai-town](https://github.com/a16z-infra/ai-town) — Stanford's *Generative Agents* research (perceive → remember → reflect → act loop).

**Best Practice**: Load daily logs + MEMORY.md in main sessions, only daily logs in shared contexts (security). Semantic search handles the rest.
---

## 🔐 Security & Access Control

### Core Principles

1. **Admin-only config**: `SOUL.md`, `AGENTS.md`, `USER.md` — only you can modify
2. **Anti-injection**: Built-in protection against prompt manipulation
3. **Credential isolation**: All secrets in `.env` (never committed)
4. **Selective memory**: Private memories stay private (`.gitignore` memory files)

### Access Levels (defined in `USER.md`)

- **Master/Admin (You)**: Full system access, config modification, all data
- **Company Users** (optional): Operational tasks, read-only configs
- **Public** (if exposed): Minimal, read-only, sandboxed

---

## 🛠️ Customization Guide

### Change Agent Personality

Edit `SOUL.md`:
- Adjust tone (formal ↔ casual, technical ↔ simple)
- Set language preference
- Define boundaries and ethical guidelines

### Add New Skills

Install skills from [ClawHub](https://clawhub.com):

```bash
clawhub install <skill-name>
```

Or create your own — see [skill-creator](https://clawhub.com/skill/skill-creator).

### Multi-Agent Orchestration

Iris is designed as a **coordinator**, not a worker. For heavy tasks:

1. Spawn sub-agents via `sessions_spawn`
2. Delegate to coding agents (Claude Code, Kimi, etc.)
3. Coordinate VPS-hosted agents (see `AGENTS.md` delegation strategy)

---

## 📡 Integrations

### PostgreSQL

```bash
# .env
PGHOST=your_host
PGPORT=5432
PGDATABASE=your_db
PGUSER=your_user
PGPASSWORD=your_password
```

Use `psql` or query tools directly.

### Notion

```bash
# .env
NOTION_API_KEY=ntn_your_key_here
```

Use Notion API to read/write databases.

### GitHub

```bash
# .env
GITHUB_TOKEN=ghp_your_token_here
```

Use for repo operations, issue tracking, etc.

---

## 💡 Example Use Cases

- **Personal Assistant**: Calendar, email, reminders, note-taking
- **Data Analyst**: Query databases, generate reports, answer business questions
- **DevOps Coordinator**: Monitor systems, manage deployments, run health checks
- **Project Manager**: Track tasks in Notion, coordinate sub-agents, generate status reports
- **Customer Support**: Answer questions, escalate complex issues, integrate with ticketing systems

---

## 🤝 Contributing

This is a template — fork it, customize it, make it yours! If you build something cool:

1. Share your workspace as a new template
2. Publish skills to [ClawHub](https://clawhub.com)
3. Join the [OpenClaw Discord](https://discord.com/invite/clawd)

---

## 📚 Resources

- **OpenClaw Docs**: [docs.openclaw.ai](https://docs.openclaw.ai)
- **ClawHub (Skills)**: [clawhub.com](https://clawhub.com)
- **Discord Community**: [discord.com/invite/clawd](https://discord.com/invite/clawd)
- **GitHub**: [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)

---

## 📄 License

MIT License — Free to use, modify, and distribute.

---

## 🌸 About Iris

Iris (Dewi Yunani — messenger of the gods) is a lead AI personal assistant originally built for **Zuma Indonesia**, a footwear retail company. This template is the sanitized, production-ready version of that workspace.

**Maintainer:** database@zuma.id

**Personality traits:**
- Clear, concise, no-nonsense communication
- Proactive but respects boundaries
- Orchestrator mindset (delegate, don't do everything yourself)
- Security-conscious (anti-injection, access control)

---

**Happy building! 🚀**

If you create something cool with this template, tag [@openclaw](https://twitter.com/openclaw) or share in the Discord!
