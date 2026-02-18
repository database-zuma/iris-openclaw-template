# Clawe — Multi-Agent Coordination System

> **Source:** https://github.com/getclawe/clawe  
> **Researched:** 2026-02-18  
> **Stars:** 343 | **Language:** TypeScript | **Status:** Active (updated ~1 hour before research)

---

## What Is It?

**Clawe** (`getclawe/clawe`) is an open-source **multi-agent coordination system** built on top of [OpenClaw](https://github.com/openclaw/openclaw). Think of it as **"Trello for AI agent squads"** — it gives a team of Claude-powered AI agents distinct identities, isolated workspaces, scheduled heartbeats, a shared task board, and a web dashboard to monitor and interact with them.

> ⚠️ Note: There is a second (unrelated) repo `russmatney/clawe` — a Clojure-based window manager tool. This document covers `getclawe/clawe`.

---

## How It Works

### Core Concepts

- **Agents** have distinct roles, personalities (defined in `SOUL.md`), and isolated workspaces
- **Heartbeats** — each agent wakes on a cron schedule (every 15 min by default) to check for work
- **Kanban task board** — tasks can be assigned, commented on, and tracked through statuses (`in_progress`, `review`, `done`, etc.)
- **Shared context** — agents collaborate via shared files (`WORKING.md`, `WORKFLOW.md`) and a Convex backend
- **Notifications** — @mentions and task updates delivered near-real-time via a watcher service
- **Routines** — recurring scheduled tasks that auto-create inbox items for agents

### Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    DOCKER COMPOSE                        │
├─────────────────┬──────────────────┬────────────────────┤
│   squadhub      │    watcher        │      clawe         │
│                 │                  │                    │
│  Agent Gateway  │ • Register agents│  Web Dashboard     │
│  (runs 4 agents)│ • Setup crons    │  • Squad status    │
│                 │ • Deliver notifs │  • Task board      │
│                 │                  │  • Agent chat      │
└────────┬────────┴────────┬─────────┴────────┬───────────┘
         │                 │                  │
         └─────────────────┼──────────────────┘
                           │
               ┌───────────▼──────────┐
               │       CONVEX         │
               │  (Real-time Backend) │
               │  • Agents            │
               │  • Tasks             │
               │  • Notifications     │
               │  • Activities        │
               └──────────────────────┘
```

### Pre-Configured Agent Squad

| Agent  | Role          | Heartbeat     |
|--------|---------------|---------------|
| 🦞 Clawe | Squad Lead   | Every 15 min  |
| ✍️ Inky  | Content Editor | Every 15 min |
| 🎨 Pixel | Designer     | Every 15 min  |
| 🔍 Scout | SEO          | Every 15 min  |

Heartbeats are staggered to avoid API rate limits.

### Agent Workspace Structure

Each agent gets an isolated filesystem workspace:

```
/data/workspace-{agent}/
├── AGENTS.md     # Instructions and conventions
├── SOUL.md       # Agent identity and personality
├── USER.md       # Info about the human they serve
├── HEARTBEAT.md  # What to do on each wake
├── MEMORY.md     # Long-term memory
├── TOOLS.md      # Local tool notes
└── shared/       # Symlink to shared team state
    ├── WORKING.md   # Current team status
    └── WORKFLOW.md  # Standard operating procedures
```

### CLI (Used by Agents)

Agents interact with the system via a `clawe` CLI:

```bash
clawe check                          # Check notifications
clawe tasks                          # List tasks
clawe task:status <id> in_progress   # Update task status
clawe task:comment <id> "message"    # Add a comment
clawe subtask:add <id> "task name"   # Add subtask
clawe deliver <id> "Name" --path ./file.md  # Register deliverable
clawe notify <session> "message"     # Send notification
clawe squad                          # View squad status
clawe feed                           # View activity feed
```

---

## Setup Requirements

### Prerequisites

| Requirement        | Notes                              |
|--------------------|------------------------------------|
| Docker & Docker Compose | Required to run the stack   |
| [Convex](https://convex.dev) account | Free tier works     |
| Anthropic API key  | For Claude (required)              |
| pnpm               | Node package manager               |
| OpenAI API key     | Optional — for image generation    |

### Environment Variables

| Variable           | Required | Description                  |
|--------------------|----------|------------------------------|
| `ANTHROPIC_API_KEY` | ✅ Yes  | Claude API key               |
| `SQUADHUB_TOKEN`   | ✅ Yes   | Auth token for agent gateway |
| `CONVEX_URL`       | ✅ Yes   | Convex deployment URL        |
| `OPENAI_API_KEY`   | ❌ No    | OpenAI key (image gen only)  |

### Quick Start

```bash
git clone https://github.com/getclawe/clawe.git
cd clawe
cp .env.example .env
# Edit .env with your API keys

pnpm install
cd packages/backend && npx convex deploy   # Deploy Convex backend

./scripts/start.sh   # Build & launch Docker stack
```

Accesses dashboard at `http://localhost:3000`.

### Project Structure

```
clawe/
├── apps/
│   ├── web/          # Next.js dashboard
│   └── watcher/      # Notification watcher + cron service
├── packages/
│   ├── backend/      # Convex schema & serverless functions
│   ├── cli/          # `clawe` CLI for agents
│   ├── shared/       # Shared squadhub client
│   └── ui/           # UI components
└── docker/
    └── squadhub/
        ├── Dockerfile
        ├── entrypoint.sh
        ├── scripts/   # init-agents.sh
        └── templates/ # Agent workspace templates
```

---

## Pros

- ✅ **Built for OpenClaw** — native integration, uses same workspace conventions (SOUL.md, AGENTS.md, HEARTBEAT.md, etc.)
- ✅ **Batteries included** — comes with 4 pre-configured agents with clear roles, ready to deploy
- ✅ **Real-time backend** — Convex provides reactive data sync; no manual polling required
- ✅ **Web dashboard** — visible squad status, task board, and chat in one place
- ✅ **Dockerized** — easy to spin up on any machine; startup script handles most configuration
- ✅ **Extensible** — adding new agents is well-documented and straightforward
- ✅ **CLI-first for agents** — agents use a clean CLI rather than direct DB calls, good separation of concerns
- ✅ **Crash-tolerant routines** — 1-hour trigger window prevents missed scheduled tasks

## Cons

- ❌ **Convex dependency** — requires a third-party real-time backend (vendor lock-in; free tier has limits)
- ❌ **Anthropic-only** — hardwired to Claude/Anthropic API; no multi-LLM support visible
- ❌ **Early stage** — updated very frequently (activity suggests rapid iteration, possible breaking changes)
- ❌ **Content-team focused** — pre-configured squad (SEO, content editor, designer) won't fit all use cases without significant customization
- ❌ **Docker required** — adds complexity for local-only dev; not suitable for serverless/edge deploy without rework
- ❌ **No mentioned auth/ACL** — dashboard appears to run locally with a single shared token; no per-user access control mentioned
- ❌ **pnpm + Convex learning curve** — adds two non-trivial tools to learn if unfamiliar

---

## Relation to OpenClaw

Clawe appears to be purpose-built as a **showcase/extension** of OpenClaw's multi-agent capabilities. It uses the same file conventions (SOUL.md, AGENTS.md, HEARTBEAT.md) that OpenClaw agents use, suggesting it could serve as a reference implementation or production-ready template for deploying OpenClaw agent teams.

---

## Also Note: `russmatney/clawe` (Different Project)

A second repo by the same name exists:
- **URL:** https://github.com/russmatney/clawe
- **What it is:** Clojure-based window manager tool for Linux/macOS (AwesomeWM, yabai)
- **Relevance to AI agents:** None — it's a personal dev environment hacking tool
- **Stars:** 16 | Language: Clojure

Not relevant to AI agent orchestration.
