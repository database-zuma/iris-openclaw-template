# ROOT.md — Iris Workspace Index

_Quick reference for session boot. Last updated: 2026-02-25._

## Core Identity Files (Read on EVERY session)
| File | Purpose |
|------|---------|
| `SOUL.md` | Who Iris is — personality, authority, access control, analytical edge |
| `AGENTS.md` | Delegation rules, agent roster, heartbeat protocol, WA isolation, non-blocking rules |
| `USER.md` | Wayan (admin) profile |
| `MEMORY.md` | Long-term curated memories (main session only) |

## Operational Files (Read as needed)
| File | Purpose |
|------|---------|
| `SKILLS_INDEX.md` | **Skill routing table** — trigger keywords → skill file path → agent. WAJIB baca untuk task delegation |
| `ORCHESTRATION.md` | Delegation quality guide — 5-part prompt template, message isolation, pipelines |
| `TOOLS.md` | Credentials, API keys, SSH, nanobot fallback configs |
| `PENDING.md` | Full task backlog (all tasks, including not-yet-started) |
| `HEARTBEAT.md` | Legacy global heartbeat (DEPRECATED — use `heartbeat/{phone}.md` per-user) |
| `IDENTITY.md` | Extended identity reference |

## Memory System
| Path | Purpose |
|------|---------|
| `memory/YYYY-MM-DD.md` | Daily session logs — raw what-happened-today |
| `MEMORY.md` | Curated long-term memories |
| `heartbeat/{phone}.md` | Per-user active task tracking (check on every heartbeat) |
| `inbox/` | Temporary notes — capture → process → distribute |
| `tasks/lessons.md` | Post-correction learnings |

## Business Skills
| Path | Purpose |
|------|---------|
| `zuma-business-skills/` | All Zuma-specific skills (planogram, RO, PPT, analysis) |
| `templates/` | Reusable prompt/report templates |
| `knowledge/` | Scraped & summarized knowledge base (indexed in `knowledge/INDEX.md`) |

## Agent Workspaces (NOT in this folder — siblings)
| Path | Agent |
|------|-------|
| `~/.openclaw/workspace-metis/` | Metis 🔮 — Data/SQL (kimi-coding/k2p5) |
| `~/.openclaw/workspace-daedalus/` | Daedalus 🪶 — Code/Build (kimi-coding/k2p5) |
| `~/.openclaw/workspace-hermes/` | Hermes 🪄 — Research/Web (kimi-coding/k2p5) |
| `~/.openclaw/workspace-oracle/` | Oracle 🏛️ — Strategy (claude-opus-4-6) |
| `~/.openclaw/workspace-eos-nanobot/` | Eos 🌅 — Visual/PPT (gemini-3.1-pro) |
| `~/.openclaw/workspace-argus-nanobot/` | Argus 👁️ — Data/Research (kimi-coding/k2p5) |
| `~/.openclaw/workspace-codex-nanobot/` | Codex 📖 — Web apps/Code (kimi-coding/k2p5) |

## Config Files (OUTSIDE workspace)
| Path | Purpose |
|------|---------|
| `~/.openclaw/openclaw.json` | Master config — models, channels, session, hooks |
| `~/.openclaw/agents/iris/agent/auth-profiles.json` | Auth keys & profiles |
| `~/.nanobot/config-{eos,argus,codex}.json` | Nanobot model & provider configs |

## Project Folders (Active)
| Path | What |
|------|------|
| `zuma-bm-decks/` | Business Manager presentation decks |
| `zuma-analysis-dashboard/` | Analysis dashboard project |
| `ro-benchmark-vercel/` | RO benchmark Vercel deployment |
| `stock-inventory-dashboard/` | Stock inventory dashboard |

## Session Boot Order
1. Read `SOUL.md` → know who you are
2. Read `AGENTS.md` → know your rules and team
3. Read `SKILLS_INDEX.md` → know which skills exist and how to route them
4. Read `USER.md` → know who you're helping
5. Read `memory/today.md` + `memory/yesterday.md` → recent context
6. If main session: also read `MEMORY.md`
7. Check `heartbeat/` folder → any pending deliveries?
