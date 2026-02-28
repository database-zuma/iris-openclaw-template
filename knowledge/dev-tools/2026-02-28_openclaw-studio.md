# OpenClaw Studio — Web Dashboard for OpenClaw Gateway

**Source:** https://github.com/grp06/openclaw-studio
**Repo:** https://github.com/grp06/openclaw-studio
**Date saved:** 2026-02-28
**License:** MIT
**Stars:** 660+ ⭐ | Forks: 84 | Commits: 668
**Status:** NOT INSTALLED — high relevance for our OpenClaw setup
**Author:** grp06 (+ claude, jfedor, oelor, cursoragent as contributors)

---

## What Is It

A **clean web dashboard (GUI) for managing OpenClaw agents**. Connect it to your OpenClaw Gateway via WebSocket, and you get a visual interface to:

- See all your agents in a fleet sidebar
- Chat with agents directly from the browser
- Create/rename/delete agents
- Manage exec approvals (Allow once / Always allow / Deny)
- Configure cron jobs / automations (schedules)
- Edit agent personality files (SOUL.md, AGENTS.md, USER.md, IDENTITY.md)
- Configure capabilities (commands, web access, file tools)
- View tool calls, thinking traces, and streaming responses
- Monitor agent status and heartbeat

**Think of it as:** a web-based control panel for OpenClaw — instead of editing `openclaw.json` by hand and reading terminal logs, you get a proper UI.

## How It Connects

Two network paths:

```
Browser  ──HTTP/WS──>  Studio (Next.js :3000)  ──WS──>  OpenClaw Gateway (:18789)
```

1. **Browser → Studio**: HTTP for UI + WebSocket to `/api/gateway/ws`
2. **Studio → Gateway**: Second WebSocket from Studio's Node server to your configured upstream Gateway URL

Studio is a **proxy** — it terminates browser WS, injects auth token server-side, and forwards frames to the gateway. Gateway remains the source of truth for all agent data.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | Next.js 16 (App Router) |
| Language | TypeScript (95.6%) |
| UI | React + shadcn/ui (components.json present) |
| Styling | Tailwind CSS + PostCSS |
| Testing | Playwright (e2e) + Vitest (unit) |
| Server | Custom Node server (WS proxy) |
| Telemetry | @vercel/otel |
| Validation | Zod |

## Setup Options

### A) Gateway local, Studio local (same machine) — OUR SETUP
```bash
npx -y openclaw-studio@latest
cd openclaw-studio
npm run dev
# Open http://localhost:3000
# Set Upstream URL: ws://localhost:18789
# Set Upstream Token: (from `openclaw config get gateway.auth.token`)
```

### B) Gateway remote, Studio local (laptop)
Use Tailscale Serve or SSH tunnel to reach remote gateway.

### C) Both in cloud (always-on)
Run Studio on VPS, expose via Tailscale HTTPS, point to gateway.

## Architecture Highlights

- **Gateway-first**: Agents, sessions, config live in gateway. Studio stores only UI settings.
- **Single-user**: No multi-tenant or multi-user support. Local JSON settings file.
- **Settings stored at**: `~/.openclaw/openclaw-studio/settings.json`
- **Feature-first code org**: `src/features/agents/` for agent UI, `src/lib/` for shared utils
- **Event-driven**: Gateway events (presence/heartbeat/chat/agent) streamed via WS, classified and routed through bridge helpers
- **No direct config writes**: Studio does NOT write to `openclaw.json` directly — all changes via gateway `config.patch` API

## UI Structure

### Main Layout
- **Fleet sidebar** (left): List of all agents with status indicators
- **Chat panel** (center): Primary workspace, streaming responses, tool calls, thinking traces
- **Settings sidebar** (right): Opened via cog icon

### Settings Tabs
1. **Personality** — Edit SOUL.md, AGENTS.md, USER.md, IDENTITY.md. Rename agent.
2. **Capabilities** — Run commands (Off/Ask/Auto), Web access (Off/On), File tools (Off/On). Skills & browser automation: coming soon.
3. **Automations** — Create/manage cron schedules (template → task → schedule → review flow). Heartbeats: coming soon.
4. **Advanced** — Display toggles (tool calls, thinking), Open Full Control UI, Delete agent.

### Agent Creation
- Simple: name + avatar only
- Post-create defaults: Commands Auto, Web On, File tools On
- Auto-opens Capabilities sidebar for onboarding

### Exec Approvals
- In-chat approval cards: "Allow once", "Always allow", "Deny"
- Fleet rows show "Needs approval" badge
- Stale approvals auto-prune by expiry timestamp

## Relevance for Iris / Zuma

**🔴 HIGH RELEVANCE — this is a GUI for exactly our setup.**

### Immediate Benefits
1. **Visual agent management** — Instead of editing `openclaw.json` manually, create/configure agents via web UI
2. **Live chat with Iris** — Chat directly with Iris from browser (useful for testing/debugging, bypassing WhatsApp)
3. **Exec approval UI** — See pending approvals in a dashboard instead of terminal logs
4. **Cron/automation management** — Visual schedule builder instead of editing config
5. **Agent file editing** — Edit SOUL.md, AGENTS.md etc. via browser with instant preview

### Setup for Our Environment
Our gateway runs locally on Mac Mini at port 18789. Setup would be:
```bash
npx -y openclaw-studio@latest
cd openclaw-studio
npm run dev
# Upstream URL: ws://localhost:18789
# Token: our gateway auth token
```
Access via `http://localhost:3000` on Mac Mini, or expose via Tailscale for remote access.

### Considerations
- **Single-user only** — fine for us (only Wayan manages agents)
- **Does NOT replace WhatsApp** — this is for admin/config, not end-user communication
- **Does NOT write openclaw.json directly** — uses gateway API, which is safer than manual edits
- **Active development** — 668 commits, latest commit 15 hours ago (Feb 26, 2026). Actively maintained.

## Key Takeaways

- **Web GUI for OpenClaw** — exactly what we need to stop editing JSON configs by hand
- **One command install** — `npx -y openclaw-studio@latest` + `npm run dev`
- **Gateway-first architecture** — doesn't mess with local config files, all changes via API
- **Chat + approvals + cron** in one UI — replaces multiple terminal workflows
- **MIT license, 660+ stars** — legitimate community project, actively maintained
- **Compatible with our setup** — local gateway on :18789, Studio on :3000

---

**Tags:** #openclaw #dashboard #web-ui #agent-management #next-js #gateway #chat #approvals #cron #studio #grp06 #high-relevance
