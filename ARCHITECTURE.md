# Iris System Architecture
> Last updated: 2026-02-28 | Compiled from comprehensive workspace audit

## 1. System Overview

Iris is a **hybrid multi-agent AI assistant** for Zuma Indonesia, operating via WhatsApp as primary interface. The system runs on a Mac Mini with two gateway processes orchestrating 8 AI agents across 2 frameworks.

**Scale:** ~600MB workspace, 13 core config files, 28 automation scripts, 39 knowledge articles, 24+ business skills, 8 major projects, pgvector semantic memory, daily reflection cycle.

```
┌─────────────────────────────────────────────────────────────┐
│                     WhatsApp / Telegram                      │
│                    (User Interface Layer)                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   🌸 IRIS (Sonnet 4.6)                       │
│              Customer Service + Delegation                   │
│         ┌────────────────┼────────────────┐                  │
│         │                │                │                  │
│    ┌────▼────┐    ┌─────▼─────┐   ┌─────▼─────┐            │
│    │ OpenClaw │    │  Nanobot   │   │  pgvector  │            │
│    │ Gateway  │    │  Gateway   │   │  Memory    │            │
│    │ :18789   │    │  :18790    │   │  (VPS DB)  │            │
│    └────┬─────┘    └─────┬─────┘   └───────────┘            │
│         │                │                                   │
│  ┌──────┼──────┐   ┌────┼────┐                              │
│  │  │   │   │  │   │  │  │   │                              │
│  M  D   H   O  │   E  A  C   │                              │
│  e  a   e   r  │   o  r  o   │                              │
│  t  e   r   a  │   s  g  d   │                              │
│  i  d   m   c  │      u  e   │                              │
│  s  a   e   l  │      s  x   │                              │
│     l   s   e  │             │                              │
│     u        │             │                              │
│     s        │             │                              │
└──────────────┴──────────────┴──────────────────────────────┘
```

---

## 2. Multi-Agent Architecture

### 2.1 OpenClaw Gateway (port 18789)

Node.js-based agent framework. Manages WhatsApp/Telegram bindings, session management, compaction, and sub-agent spawning.

| Agent | ID | Model (Primary) | Fallback 1 | Fallback 2 | Role |
|-------|----|-----------------|-----------|-----------|------|
| 🌸 **Iris** | `iris` | `anthropic/claude-sonnet-4-6` | `kimi-coding/k2p5` | `google/gemini-3-flash-preview` | Customer service + delegation (DEFAULT agent) |
| 🔮 **Metis** | `metis` | `anthropic/claude-sonnet-4-6` | `kimi-coding/k2p5` | `google/gemini-3-flash-preview` | Data/SQL/Analysis |
| 🪶 **Daedalus** | `daedalus` | `anthropic/claude-haiku-4-5` | `kimi-coding/k2p5` | `google/gemini-3-flash-preview` | Code/Build/Scripts/Planogram |
| 🪄 **Hermes** | `hermes` | `anthropic/claude-haiku-4-5` | `kimi-coding/k2p5` | `google/gemini-3-flash-preview` | Research/Web/Files |
| 🏛️ **Oracle** | `oracle` | `anthropic/claude-opus-4-6` | `kimi-coding/k2p5` | `google/gemini-3-flash-preview` | Strategy advisory (READ-ONLY, no exec) |

**Key Rules:**
- Iris is bound to WhatsApp channel (default agent)
- Oracle has restricted tools: no exec, browser, nodes, message, cron, gateway, sessions_spawn, sessions_send, tts, canvas
- All sub-agents spawned via `sessions_spawn agentId: "{id}"`
- Fallback chain: OpenClaw tries PRIMARY → FALLBACK_1 → gives up (known bug: only 2 attempts max)
- Context pruning: cache-ttl mode, 30m TTL, 20K min prunable chars
- Compaction: safeguard mode, 100K token floor, memory flush enabled

### 2.2 Nanobot Gateway (port 18790)

Python-based agent framework. Lighter weight, used for specialized workers with separate rate limits and token budgets.

| Agent | Config | Model (Primary) | Role |
|-------|--------|-----------------|------|
| 🌅 **Eos** | `~/.nanobot/config-eos.json` | `gemini/gemini-3.1-pro-preview` | Visual/PPT/image gen/design |
| 👁️ **Argus** | `~/.nanobot/config-argus.json` | `anthropic/claude-sonnet-4-6` | Data/SQL/research/reports |
| 📖 **Codex** | `~/.nanobot/config-codex.json` | `anthropic/k2p5` | Web apps/full-stack code |

**Key Rules:**
- Nanobot has NO automatic fallback chain — manual override via env var
- Override: `NANOBOT_AGENTS__DEFAULTS__MODEL="provider/model" NANOBOT_CONFIG_PATH=~/.nanobot/config-{agent}.json nanobot agent -m "[task]"`
- ALL nanobot calls MUST use `background: true` (never synchronous)
- Each config has providers: anthropic, gemini, kimi-coding
- OpenRouter pending (API key not yet configured)
- Max tool iterations: 20, memory window: 50, max tokens: 8192

### 2.3 Communication Patterns

**Iris → OpenClaw Sub-agents:** `sessions_spawn` (native OpenClaw mechanism)
**Iris → Nanobot Agents:** `exec` tool with `NANOBOT_CONFIG_PATH` env var, always `background: true`
**Inter-agent:** No direct agent-to-agent communication. All routing through Iris.

```
User (WhatsApp) → Iris → Route decision:
  ├── Quick answer (<2 sec) → Respond directly
  ├── Data/SQL → Argus (nanobot) or Metis (openclaw)
  ├── Visual/PPT → Argus (structure) → Eos (render)
  ├── Code/Scripts → Daedalus (openclaw) or Codex (nanobot)
  ├── Research → Hermes (openclaw)
  └── Strategy → Oracle (openclaw, read-only)
```

---

## 3. Workspace Structure

```
~/.openclaw/workspace/                    # Iris main workspace (~600MB)
├── SOUL.md                               # Agent personality & identity
├── AGENTS.md (21KB)                      # System docs, rules, delegation protocol
├── TOOLS.md (16KB)                       # Tool reference, fallbacks, browser rules
├── ORCHESTRATION.md (15KB)               # Delegation protocol, pipeline patterns
├── SKILLS_INDEX.md (9.8KB)               # Skill routing table (MUST read every session)
├── PENDING.md (13KB)                     # Full backlog (all tasks incl. not started)
├── MEMORY.md (7.2KB)                     # Curated long-term memories
├── IDENTITY.md                           # Agent identity config
├── USER.md                               # User profile (Wayan)
├── HEARTBEAT.md                          # Heartbeat protocol doc
├── ROOT.md                               # Root-level docs
├── README.md (15KB)                      # Workspace overview
├── ARCHITECTURE.md                       # THIS FILE
│
├── scripts/ (28 files, 4K+ LOC)          # Automation scripts
│   ├── embed_memory.py (401 lines)       # pgvector embedding pipeline
│   ├── search_memory.py (309 lines)      # Semantic memory search + signal filters
│   ├── extract_signals.py (368 lines)    # LLM-powered signal classifier (Gemini Flash)
│   ├── generate_planogram.py (20KB)      # Planogram gen for 51 branches
│   ├── ro_benchmark_mckinsey.py (36KB)   # RO analysis (McKinsey framework)
│   ├── bm-deck-updater/                  # Weekly BM deck HTML → Vercel
│   ├── daily-updater/                    # Daily STO tool rebuild + deploy
│   ├── refresh_iseller_data.sh           # iSeller POS data pipeline
│   └── [15+ validation/ETL scripts]      # Data checks, cleaning, syncing
│
├── knowledge/ (39 articles)              # Knowledge base
│   ├── INDEX.md                          # Master index
│   ├── ai-agents/                        # AIRI, Supermemory, etc.
│   ├── business-ops/                     # Zuma operations
│   ├── design/                           # Design references
│   ├── dev-tools/                        # OpenClaw Studio, etc.
│   └── misc/                             # Other
│
├── memory/ (17 daily logs)               # Daily interaction logs
│   ├── YYYY-MM-DD.md                     # Raw daily logs (Feb 11-27)
│   ├── reflections/                      # Daily synthesized insights
│   │   └── YYYY-MM-DD.md                # Pattern/Issue/Tomorrow format
│   └── contexts/
│       └── ops-team.md                   # Curated ops team context
│
├── heartbeat/                            # Per-user task tracking
│   ├── +6285784151229.md                 # Individual user heartbeats
│   ├── +6289502167652.md
│   ├── +628983539659.md                  # Wayan
│   └── [group-id].md                     # Group chat heartbeats
│
├── zuma-business-skills/ (24+ skills)    # Business skill library
│   ├── README.md, CHANGELOG.md           # v1.2.0 (Feb 2026)
│   ├── general/ (7 skills)               # Cross-department
│   ├── ops/ (15 skills)                  # Operations
│   │   ├── zuma-plano-ro-skills/         # Planogram pipeline (4 steps)
│   │   └── zuma-inventory-control/       # Inventory management
│   └── skills/finance/ (2 skills)        # Finance
│
├── outbox/ (~39M)                        # Generated outputs
├── inbox/                                # Incoming data (meeting notes, SQL, POs)
├── templates/                            # Output templates
├── docker/                               # Docker config for OpenClaw agent
│
├── [Major Projects]
│   ├── stock-inventory-dashboard/ (180M)  # Stock dashboard
│   ├── dn-to-po/ (130M)                  # DN→Invoice+PO converter
│   ├── zuma-analysis-dashboard/           # Analysis dashboard
│   ├── zuma-lk-konsolidasi/              # Consolidated reporting
│   ├── zuma-bm-decks/ (11M)             # Branch Manager decks
│   └── [BCG analyses, product analysis]   # Strategy projects
│
└── .env                                  # Credentials (PGHOST, API keys, tokens)
```

### Sub-Agent Workspaces

| Workspace | Size | Purpose |
|-----------|------|---------|
| `~/.openclaw/workspace-iris` | 172M | Iris (symlink to main workspace) |
| `~/.openclaw/workspace-metis` | 3.7M | Metis data/SQL workspace |
| `~/.openclaw/workspace-daedalus` | 948K | Daedalus code workspace |
| `~/.openclaw/workspace-hermes` | 212K | Hermes research workspace |
| `~/.openclaw/workspace-oracle` | 200K | Oracle advisory workspace |
| `~/.openclaw/workspace-eos-nanobot` | 21M | Eos visual outputs |
| `~/.openclaw/workspace-argus-nanobot` | 100K | Argus data outputs |
| `~/.openclaw/workspace-codex-nanobot` | 16K | Codex code outputs |

---

## 4. Memory System (pgvector)

### 4.1 Database

- **Host:** `76.13.194.120:5432` (VPS PostgreSQL)
- **Database:** `openclaw_ops`
- **Schema:** `iris`
- **Table:** `iris.memory_vectors`
- **Extension:** pgvector (v0.6.0 — caps index at 2000 dims)

```sql
CREATE TABLE iris.memory_vectors (
    id SERIAL PRIMARY KEY,
    date DATE,
    content TEXT,                       -- Chunk text (50-2000 chars)
    embedding vector(3072),             -- Gemini embedding
    source_file VARCHAR(255),
    chunk_index INT,
    tags TEXT[],                        -- Tag array
    content_hash VARCHAR(32) UNIQUE,    -- SHA256 dedup
    created_at TIMESTAMP DEFAULT NOW(),
    signal_type VARCHAR(20),            -- decision|preference|correction|lesson|pattern|error|fact|task
    importance SMALLINT,               -- 1 (trivial) to 5 (critical)
    signal_summary TEXT                 -- 1-sentence LLM-generated summary
);
```

### 4.2 Embedding Pipeline

```
Raw Memory (memory/*.md, knowledge/*)
    │
    ▼ Semantic Chunking
Split by: ## headers → paragraphs → single newlines
Skip: chunks < 50 chars | Max: 2000 chars
    │
    ▼ Content Dedup
SHA256 hash → skip if exists in DB
    │
    ▼ Gemini Embedding
Model: gemini-embedding-001 (3072 dims)
Task type: RETRIEVAL_DOCUMENT
Rate: 0.1s between API calls
    │
    ▼ PostgreSQL Upsert
INSERT ... ON CONFLICT (content_hash) DO UPDATE
```

**Scripts:**
- `embed_memory.py` — `--full` (re-embed all), `--file X.md`, `--include-knowledge`, `--stats`
- `search_memory.py` — `"query"`, `--limit N`, `--since DATE`, `--source knowledge`, `--json`, `--type SIGNAL`, `--important`, `--min-importance N`
- `extract_signals.py` — LLM-powered signal classifier (Gemini 2.5 Flash). `--full`, `--since DATE`, `--stats`, `--dry-run`, `--limit N`

**Cost:** ~$0.0001/day (embedding) + ~$0.001/run (signal extraction)

### 4.3 Search Interface

```
Query → Gemini embedding (RETRIEVAL_QUERY) → Cosine similarity (1 - distance)
→ Top-K results (default 5) with filters (date, source, signal_type, importance)
```

### 4.4 Signal Extraction (Supermemory-Inspired)

Enriches existing chunks with structured metadata for smarter retrieval.

```
iris.memory_vectors (440 chunks)
    │
    ▼ extract_signals.py (Gemini 2.5 Flash, thinkingBudget=0)
Classify each chunk → signal_type + importance (1-5) + summary
    │
    ▼ UPDATE iris.memory_vectors SET signal_type, importance, signal_summary
```

**Signal Types:** decision, preference, correction, lesson, pattern, error, fact, task
**Distribution (440 chunks):** 196 facts, 132 lessons, 27 tasks, 25 corrections, 20 decisions, 18 errors, 17 patterns, 5 preferences
**Importance:** 32 critical (⭐5), 223 important (⭐4), 184 normal (⭐3), 1 low (⭐2)

### 4.5 Reflection Cycle (Daily 22:00 WIB)

1. Read today's `memory/YYYY-MM-DD.md`
2. LLM synthesis → 🔁 Patterns, ❌ Issues, 📋 Tomorrow, 💡 Systemic
3. Write to `memory/reflections/YYYY-MM-DD.md`
4. Embed reflection to vector DB
5. If systemic → update AGENTS.md or TOOLS.md

---

## 5. Skill System

### 5.1 Overview

24+ skills organized by domain in `zuma-business-skills/`. Skills are NOT auto-discovered — Iris MUST read `SKILLS_INDEX.md` every session for routing.

### 5.2 Skill Categories

**General (7):**
| Skill | Purpose |
|-------|---------|
| `data-storytelling-skill` | McKinsey/BCG narrative frameworks |
| `deploy-to-live` | git→GitHub→Vercel pipeline |
| `eos-visual-skill` | McKinsey PPT system (2600+ lines) |
| `zuma-business-metrics` | KPI framework & targets |
| `zuma-company-context` | Brand identity (Teal #002A3A, Green #00E273) |
| `zuma-image-gen-skill` | Gemini image generation |
| `zuma-ppt-design` | Professional presentation design |

**Ops (15):**
| Skill | Purpose |
|-------|---------|
| `dn-to-po` | Delivery Note → Invoice + PO conversion |
| `iseller-data-refresh` | iSeller POS data pipeline |
| `notion-metrics` | FF/FA/FS metrics to Notion |
| `zuma-branch` | 6 branches, store categories, supervisors |
| `zuma-data-analyst-skill` | PostgreSQL, SQL templates, business analysis |
| `zuma-database-assistant-skill` | DBA, ETL pipeline, view architecture |
| `stock-opname-level-2` | Inventory procedures |
| `zuma-ff-skills` | Fill Factor/Accuracy/Score metrics |
| `step0.5-pre-planogram` | Pre-planogram data gen (size-level targets) |
| `step1-planogram` | Planogram layout generation |
| `step2-visualizations` | Planogram floor plan visualization |
| `step3-zuma-ro-surplus` | RO Request + Surplus Pull (DEFAULT) |
| `zuma-ro-box-only` | RO Box-Only experimental (Jatim only) |
| `zuma-sku-context` | Product tiers, assortments, kode_mix |
| `zuma-warehouse-and-stocks` | Warehouse ops, RO system, stock tracking |

**Finance (2):**
| Skill | Purpose |
|-------|---------|
| `coretax-faktur-generator` | Coretax DJP-ready invoices |
| `fp-rekon-stock` | Tax invoice parsing, purchase register |

**Cross-cutting:** `zuma-token-usage-report` — Token usage reporting (appended to all outputs)

### 5.3 Planogram Pipeline (Sequential Steps)

```
Step 0.5: pre-planogram-zuma
    │  Output: size-level target quantities
    ▼
Step 1: planogram-zuma
    │  Output: PLANOGRAM_[Store].xlsx
    ▼
Step 2: visualized-planogram-zuma
    │  Output: VISUAL_PLANOGRAM_[Store].xlsx + .txt
    ▼
Step 3 (DEFAULT): zuma-ro-surplus
    │  Input: planogram + current stock from DB
    │  Output: RO_Request_[Store]_[Date].xlsx
    ▼
Step 3 (ALT): zuma-ro-box-only
    │  Jatim only, experimental
```

### 5.4 Skill Routing

| User says... | Skill loaded | Delegate to |
|---|---|---|
| "bikin RO request" | `step3-zuma-ro-surplus` + 3 deps | Daedalus |
| "bikin planogram" | `planogram-zuma` + deps | Daedalus |
| "bikin PPT" | `eos-visual-skill` | Argus → Eos |
| "cek stok" / "data sales" | `zuma-data-analyst-skill` | Argus / Metis |
| "DN" / "delivery note" | `dn-to-po` | Daedalus |

---

## 6. Orchestration Protocol

### 6.1 Message Isolation (MANDATORY)

Every incoming message tagged with:
- `origin_phone` / `origin_channel_id`
- `origin_name`
- `timestamp`

Per-user heartbeat files: `heartbeat/{phone}.md`

**NEVER mix contexts between users. NEVER deliver results to wrong phone.**

### 6.2 Non-Blocking Response (<5 seconds)

```
User message received
    │
    ├── < 2 sec? → Answer directly
    │
    └── > 2 sec? → Acknowledge immediately
                   → Delegate (background: true)
                   → Write to heartbeat/{phone}.md
                   → Follow up on next heartbeat poll
```

### 6.3 Heartbeat Monitoring

- **Interval:** Every 5 minutes
- **Mode 1 (Routine):** Check email, calendar, mentions → `HEARTBEAT_OK` (silent)
- **Mode 2 (Active Task):** Poll sub-agents, deliver results, escalate if stuck

**Escalation Timeline:**
| Time | Action |
|------|--------|
| 0-5 min | Wait (normal) |
| 5-10 min | Poll status, update user |
| 10-15 min | Retry or report error |
| 15-30 min | Hard escalation to Wayan |
| >30 min | Cancel and report |

### 6.4 Multi-Agent Pipeline Patterns

**Pattern A: PPT/Deck Request**
```
Argus (structure JSON + data) → Eos (render HTML + Vercel deploy) → User gets URL
```

**Pattern B: Web App**
```
Argus (schema + data) → Codex (build) → Vercel deploy → User gets URL
```

**Pattern C: Parallel + Merge**
```
Argus ∥ Codex → Eos (merge + render)
```

### 6.5 Pre-Delivery Self-Check

Before sending any result to user:
1. ✅ Correct phone? (crosscheck heartbeat)
2. ✅ Correct task? (not another user's)
3. ✅ Summarized? (>500 words → 3 bullet summary)
4. ✅ Other pending? (mention other tasks in progress)
5. ✅ Other users waiting? (don't forget them)

---

## 7. Automation & Scripts

### 7.1 Scheduled Automation

| Schedule | Script | Pipeline |
|----------|--------|----------|
| 02:30 WIB (cron) | `backup-vps-db.sh` | VPS database backup |
| 06:10 WIB | `daily-updater/update_sto.sh` | Rebuild `mart.sto_analysis` → gen HTML → Vercel deploy |
| Monday 07:00 WIB | `bm-deck-updater/update_bm_decks.py` | Query DB → update HTML markers → Vercel deploy |
| 22:00 WIB | Reflection cycle | Synthesize daily logs → embed to pgvector |

### 7.2 On-Demand Scripts

| Script | Purpose | Size |
|--------|---------|------|
| `embed_memory.py` | pgvector embedding pipeline | 13KB / 401 lines |
| `search_memory.py` | Semantic memory search | 7KB / 236 lines |
| `generate_planogram.py` | Planogram gen (51 branches) | 20KB |
| `ro_benchmark_mckinsey.py` | RO analysis (McKinsey) | 36KB |
| `refresh_iseller_data.sh` | iSeller data refresh | Pipeline script |
| `clean_data_options.py` | Excel data cleaning | 9.2KB |
| `etl_data_options_v2.py` | Data options ETL | 7.5KB |
| `process_pajak_final_reco.py` | Pajak recommendation | 7.5KB |

### 7.3 Validation Scripts

Quick data validation (<2KB each):
`check_data_availability.py`, `check_mart_sales.py`, `check_plano_stores.py`, `check_plano_structure.py`, `check_raw_deep.py`, `list_schemas.py`, `list_all_tables.py`, `fetch_sales.py`, `sync_store_name_map.py`

---

## 8. Infrastructure

### 8.1 LaunchAgents

| Plist | Binary | Port | Purpose |
|-------|--------|------|---------|
| `ai.openclaw.gateway` | Node.js (openclaw) | 18789 | OpenClaw gateway |
| `ai.nanobot.gateway` | Python (nanobot) | 18790 | Nanobot gateway |
| `com.openclaw.gateway-monitor` | Python monitor | — | Gateway health monitor |

### 8.2 Model Providers

| Provider | Auth | Models Used |
|----------|------|-------------|
| **Anthropic** | Token (`anthropic:zuma-macmini-token`) | Sonnet 4.6, Haiku 4.5, Opus 4.6 |
| **Kimi for Coding** | API key | k2p5 (Kimi K2.5) |
| **Google Gemini** | API key | gemini-3.1-pro-preview, gemini-3-flash-preview |
| **OpenRouter** | ⚠️ NOT YET CONFIGURED | Planned: Qwen, DeepSeek, Baidu ERNIE |

### 8.3 External Services

| Service | Purpose | Auth |
|---------|---------|------|
| PostgreSQL (VPS) | Data warehouse + pgvector memory | `openclaw_app@76.13.194.120:5432` |
| Vercel | Dashboard/tool deployment | Token in .env |
| GitHub | Code repos | Token (`buat-iris-macmini`) |
| Notion | Metrics (READ-ONLY) | API key |
| Google Workspace | Drive, Docs | `gog` CLI |
| Brave Search | Web search | API key |
| Firecrawl | JS-rendered scraping | API key |
| ElevenLabs | TTS (voice) | `sag` CLI |

### 8.4 Database Architecture

```
PostgreSQL (openclaw_ops)
├── raw.*          # Raw data (FORBIDDEN for user queries)
├── core.*         # Clean core tables
├── portal.*       # Portal/planogram tables
├── mart.*         # Materialized views for reporting
│   ├── mart.sto_analysis (rebuilt daily 06:10)
│   └── mart.mv_iseller_summary
└── iris.*         # Iris-specific
    └── iris.memory_vectors (pgvector)
```

---

## 9. Knowledge Base

### 9.1 Structure

```
knowledge/
├── INDEX.md                              # Master index (MUST update on new article)
├── ai-agents/                            # AI agent tech
│   ├── 2026-02-28_project-airi.md       # AIRI avatar framework
│   ├── 2026-02-28_claude-supermemory.md # Supermemory analysis
│   └── [more articles]
├── business-ops/                         # Zuma business operations
├── design/                               # Design references
├── dev-tools/                            # Developer tools
│   └── 2026-02-28_openclaw-studio.md    # OpenClaw Studio (HIGH RELEVANCE)
└── misc/                                 # Other
```

### 9.2 Article Format (Style B)

```markdown
# Title
## Key Points
- [bullet points]
## Takeaways
- [actionable insights]
## Tags
`tag1` `tag2` `tag3`
```

---

## 10. Security & Constraints

### 10.1 Iron Laws

1. **HUKUM BESI:** Users NEVER communicate directly with sub-agents. ALL via Iris.
2. **Iris = CUSTOMER SERVICE + DELEGATION.** Iris does NOT execute tasks herself.
3. **Data Security:** NEVER query `raw.*` schema for user responses. Use `core.*`, `portal.*`, `mart.*`.
4. **Message Isolation:** NEVER mix user contexts. NEVER deliver to wrong phone.
5. **Non-Blocking:** Iris MUST respond within 5 seconds. All heavy work → background.

### 10.2 Iris Restrictions

- ❌ Run Python/bash scripts (→ delegate to Daedalus)
- ❌ Write code or edit non-memory files (→ delegate)
- ❌ Install packages (→ delegate)
- ❌ Edit `openclaw.json` (explicit user instruction)
- ✅ Nanobot calls (exec with background: true)
- ✅ Quick status checks (<2 sec)
- ✅ Memory/heartbeat file updates
- ✅ Single CLI commands (gog, git status)

### 10.3 Quiet Hours

23:00 - 08:00 WIB: Heartbeat silent. Exception: urgent email or event <2 hours away.

---

## 11. Known Issues & Pending

### Current Issues (as of 2026-02-28)

- **OpenClaw fallback bug:** Only tries PRIMARY + 1 FALLBACK, then gives up (even with multiple fallbacks configured)
- **OpenRouter not configured:** API key missing for cheap Chinese AI fallbacks on Nanobot
- **pgvector index:** v0.6.0 caps at 2000 dims; Gemini uses 3072 → sequential scan only (no index)
- **Nanobot no auto-fallback:** Single model field, no fallback array support
- **gog auth expired:** Blocking Google Drive uploads (needs Wayan re-auth)

### Future Projects

- **OpenClaw Studio:** Web GUI for OpenClaw (Next.js, 660⭐) — in PENDING.md
- **Iris Voice Avatar:** AIRI-based voice avatar exploration
- **Signal Extraction:** ✅ DONE (2026-02-28) — 440/440 chunks classified. Supermemory-inspired auto-capture for pgvector.
- **pgvector 0.7.0 upgrade:** Would enable HNSW index for 3072-dim embeddings

---

## Appendix: Config File Locations

| File | Purpose |
|------|---------|
| `~/.openclaw/openclaw.json` | Main OpenClaw config (agents, models, channels, gateway) |
| `~/.nanobot/config.json` | Main Nanobot config (providers, gateway, channels) |
| `~/.nanobot/config-eos.json` | Eos agent config |
| `~/.nanobot/config-argus.json` | Argus agent config |
| `~/.nanobot/config-codex.json` | Codex agent config |
| `~/.openclaw/workspace/.env` | Environment credentials |
| `~/Library/LaunchAgents/ai.openclaw.gateway.plist` | OpenClaw LaunchAgent |
| `~/Library/LaunchAgents/ai.nanobot.gateway.plist` | Nanobot LaunchAgent |
| `~/.openclaw/agents/*/agent/auth-profiles.json` | Cooldown state (clear on restart) |
