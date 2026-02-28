# Awesome OpenClaw Use Cases — Community Collection

**Source:** https://github.com/hesamsheikh/awesome-openclaw-usecases  
**Date:** 2026-02-28  
**Tags:** #openclaw #use-cases #multi-agent #automation #community #iris-inspiration  
**Stars:** 11k ⭐ | **Forks:** 836

---

## What It Is

Community-curated collection of 30 real, verified OpenClaw use cases. Contributors only submit use cases they've personally run for at least a day. Covers automation from home server infrastructure to customer service to content pipelines.

---

## Use Cases by Category

### Social Media
- **Daily Reddit Digest** — summarize curated subreddits based on preferences, delivered daily
- **Daily YouTube Digest** — summaries of new videos from followed channels
- **X Account Analysis** — qualitative analysis of an X account
- **Multi-Source Tech News Digest** — 109+ sources (RSS, Twitter/X, GitHub, web search), quality-scored

### Creative & Building
- **Goal-Driven Autonomous Tasks** — brain dump goals → agent autonomously generates, schedules, and completes daily tasks (including building surprise mini-apps overnight)
- **YouTube Content Pipeline** — automate idea scouting, research, and tracking
- **Multi-Agent Content Factory** — research + writing + thumbnail agents working in Discord channels
- **Autonomous Game Dev Pipeline** — full lifecycle: backlog → implementation → git commit → "Bugs First" policy enforced

### Infrastructure & DevOps
- **n8n Workflow Orchestration** — delegate API calls to n8n webhooks; agent never touches credentials
- **Self-Healing Home Server** — SSH access + kubectl + cron-based health checks + self-healing (see deep dive below)

### Productivity
- **Autonomous Project Management** — STATE.yaml pattern for subagent coordination (see deep dive below)
- **Multi-Channel Customer Service** — WhatsApp + Instagram + Gmail + Google Reviews unified inbox, 80% auto-handled
- **Phone-Based Personal Assistant** — access via voice call or SMS
- **Inbox De-clutter** — newsletter summarizer → email digest
- **Personal CRM** — discover and track contacts from email and calendar
- **Health & Symptom Tracker** — food/symptom log with trigger identification
- **Multi-Channel Personal Assistant** — Telegram + Slack + email + calendar from one AI
- **Project State Management** — event-driven tracking, replaces Kanban boards
- **Dynamic Dashboard** — real-time parallel data fetching (APIs, DB, social)
- **Todoist Task Manager** — agent reasoning/progress synced to Todoist for transparency
- **Family Calendar & Household Assistant** — aggregate all family calendars, morning briefing, household inventory
- **Multi-Agent Specialized Team** — multiple agents via single Telegram group (see deep dive below)
- **Custom Morning Brief** — news + tasks + content drafts + AI actions texted every morning
- **Second Brain** — text anything to bot → searchable Next.js dashboard, zero-friction capture
- **Event Guest Confirmation** — AI voice calls list of guests to confirm attendance, compiles summary

### Research & Learning
- **AI Earnings Tracker** — tech/AI earnings reports, automated previews and alerts
- **Personal Knowledge Base (RAG)** — drop URLs/tweets/articles into chat, builds searchable KB
- **Market Research & Product Factory** — mine Reddit/X for pain points → build MVPs
- **Semantic Memory Search** — vector-powered search over OpenClaw markdown memory files

### Finance
- **Polymarket Autopilot** — paper trading on prediction markets with backtesting and daily reports

---

## Deep Dives

### 1. Self-Healing Home Server

**What it does:**
- Cron-based health checks every 15 min (services, pods, disk)
- Auto-restart crashed pods, fix configs, scale resources autonomously
- Morning briefing at 8 AM: weather, calendars, system health, task board
- Email triage: labels actionable, archives noise
- Knowledge base extraction from notes (one user: 49,079 atomic facts from ChatGPT history)
- Blog publishing: draft → banner → publish CMS → deploy
- Security audits: hardcoded secrets, privileged containers, overly permissive access

**Key lesson (CRITICAL for Iris):**  
> "AI will hardcode secrets. They don't have the same instincts humans do."

Setup: TruffleHog pre-push hooks, local Gitea staging, CI scanning pipeline before public GitHub pushes.

**Cron schedule example:**
```
Every 15 min: check kanban for in-progress tasks → continue
Every 1h: health checks, email triage
Every 6h: knowledge base entry, self-health check (openclaw doctor)
Daily 8AM: morning briefing
Daily 4AM: nightly brainstorm (connect notes)
Weekly: security audit
```

**Inspired by:** Nathan's writeup at madebynathan.com (2026-02-03)

---

### 2. STATE.yaml Pattern (Autonomous Project Management)

Solves orchestrator bottleneck. Main agent stays thin (CEO pattern — strategy only). Subagents self-coordinate via shared file.

```yaml
# STATE.yaml — single source of truth
tasks:
  - id: api-auth
    status: done
    owner: pm-backend
  - id: content-migration
    status: blocked
    blocked_by: api-auth
    notes: "Waiting for endpoint schema"
next_actions:
  - "pm-content: Resume migration now that api-auth is done"
```

**Flow:**
1. Main agent spawns subagent with specific scope
2. Subagent reads STATE.yaml, finds its tasks
3. Subagent works, updates STATE.yaml
4. Other agents poll STATE.yaml, pick up unblocked work
5. Main agent checks in periodically, adjusts priorities

**AGENTS.md pattern:**
```
Main session = coordinator ONLY. All execution goes to subagents.
Main session: 0-2 tool calls max (spawn/send only)
PMs own their STATE.yaml files
```

**Key insight:** STATE.yaml scales better than message-passing. Git-commit STATE.yaml for full audit history.

---

### 3. Multi-Agent Specialized Team (Solo Founder Setup)

Separate agents with distinct roles, personalities, and models. All controlled via **one Telegram group**.

**Example config:**
| Agent | Role | Model | Scheduled Tasks |
|-------|------|-------|-----------------|
| Milo | Strategy Lead | Claude Opus | 8AM standup, 6PM recap |
| Josh | Business Analyst | Sonnet (fast) | 9AM metrics pull |
| Marketing | Content & Research | Gemini | 10AM content ideas, 2h Reddit/X monitor |
| Dev | Engineering | Opus/Codex | CI/CD health, PR review |

**Shared memory structure:**
```
team/
├── GOALS.md      ← all agents read
├── DECISIONS.md  ← append-only
├── PROJECT_STATUS.md ← all agents update
└── agents/
    ├── milo/      ← private context
    ├── josh/
    └── dev/
```

**Telegram routing:**
```
@milo → strategy agent
@josh → business agent
@marketing → marketing agent
@dev → dev agent
@all → broadcast
No tag → Milo by default
```

**Key insights:**
- Personality matters — naming agents makes it feel like a real team
- Right model for right job: don't use Opus for keyword monitoring
- Scheduled tasks = the flywheel; real value is proactive, not reactive
- **Start with 2 agents, not 4**

**Inspired by:** Trebuh (@iamtrebuh on X, 2026-02-11). Also: @jdrhyne (15+ agents, 3 machines, 1 Discord), @nateliason (multi-model pipeline), @danpeguine (2 OpenClaw instances in same WhatsApp group).

---

### 4. Multi-Channel Customer Service

Unify WhatsApp Business + Instagram DMs + Gmail + Google Reviews → single AI-powered inbox.

**Results:** One restaurant → response time 4 hours → 2 minutes. 80% inquiries handled automatically.

**AGENTS.md config pattern:**
```
When receiving customer messages:
1. Identify channel
2. Check if test mode enabled
3. Classify intent:
   - FAQ → respond from knowledge base
   - Appointment → check availability, confirm
   - Complaint → flag for human review
   - Review → thank, address concerns
Response: friendly, professional, match customer's language (auto-detect)
Never invent info not in knowledge base
Test mode: prefix [TEST], log but don't send
```

**Heartbeat config:**
```
Every 30 min: check unanswered messages >5 min old, alert if queue backing up
```

---

### 5. Second Brain

Zero-friction knowledge capture via messaging.

**Setup:**
1. Connect to Telegram/Discord/iMessage
2. Text anything: "remember to read X" / "save this link" / "John recommended Y"
3. Prompt OpenClaw to build Next.js dashboard: searchable list of all memories, Cmd+K global search, filter by date/type

**Key insight:** Capture = texting a friend. Retrieval = search. No folders, no tags, no friction. OpenClaw memory is cumulative.

---

## Key Patterns Across All Use Cases

1. **Heartbeat/Cron = the real product** — scheduled proactive work > reactive responses
2. **STATE.yaml > orchestrator** — file-based coordination scales without bottleneck
3. **Right model per task** — don't use Opus for simple classification
4. **Test mode first** — always demo before going live
5. **Security: hardcode-proof your agent** — TruffleHog + local Git staging before public push
6. **Thin main session** — delegate everything, main agent = CEO/coordinator only

---

## Relevance for Iris/Zuma

| Pattern | Iris Applicability |
|---------|-------------------|
| Self-healing server | Iris is on VPS — add cron health checks, self-healing |
| Multi-agent team | Directly maps to Iris + Daedalus/Argus/Metis/Eos/Codex team |
| STATE.yaml | Better subagent coordination than current approach |
| Customer service | Zuma has WhatsApp customer touchpoints — 80% auto-handling possible |
| Morning brief | Daily Zuma business summary (sales, stock, alerts, calendar) |
| Second brain | Already partially done via Iris knowledge/memory system |

---

## Security Checklist (from Self-Healing Server use case)

1. Pre-push hooks: TruffleHog or similar — block commits with hardcoded API keys/tokens
2. Local-first Git: private Gitea staging before public GitHub
3. CI scanning pipeline (Woodpecker or similar) before any public push
4. Dedicated secrets vault with limited scope (e.g. 1Password AI vault, read-only)
5. Network segmentation for sensitive services
6. Daily automated security audits

**Source:** Nathan's writeup: https://madebynathan.com/2026/02/03/everything-ive-done-with-openclaw-so-far/
