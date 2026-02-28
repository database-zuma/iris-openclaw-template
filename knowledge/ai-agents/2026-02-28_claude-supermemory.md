# Claude Supermemory — Persistent Memory Plugin for Claude Code

**Source:** https://github.com/supermemoryai/claude-supermemory
**Product:** https://supermemory.ai
**Docs:** https://supermemory.ai/docs/integrations/claude-code
**Date saved:** 2026-02-28
**License:** MIT (plugin code) — but requires paid hosted API
**Stars:** 2.2k ⭐ | Forks: 118 | Commits: 37
**Author:** Dhravya (supermemoryai)
**Status:** NOT INSTALLED — evaluate for opencode CLI, NOT for Iris

---

## What Is It

A **Claude Code plugin** that gives persistent memory across sessions. When you work in Claude Code (or opencode CLI), your conversations and learnings are automatically saved to Supermemory's cloud API. Next session, the agent can recall past work, decisions, and patterns.

**Key insight:** This is for YOUR coding sessions (opencode CLI on Mac Mini), not for Iris on WhatsApp. Iris already has her own pgvector memory system.

## How It Works

1. **Auto Capture** — When a session ends, important conversation turns are saved to Supermemory API
2. **super-search** — Ask "what did we work on last week?" → searches your saved memories
3. **super-save** — Explicitly save something important (architectural decisions, bug fixes, patterns)
4. **Signal Extraction** — Only captures turns with keywords like "remember", "architecture", "decision", "bug", "fix" (configurable)
5. **Team Memory** — Per-repo container tags let team members share project knowledge

## Architecture

```
Claude Code / opencode CLI
    ↕ (plugin hooks)
claude-supermemory plugin (local JS)
    ↕ (HTTPS API calls)
Supermemory Cloud API (hosted SaaS)
    → embeddings, vector search, storage
```

**NOT self-hosted.** All memory storage + search runs on Supermemory's cloud. You get an API key from their console.

## Installation

```bash
# In Claude Code:
/plugin marketplace add supermemoryai/claude-supermemory
/plugin install claude-supermemory

# Set API key:
export SUPERMEMORY_CC_API_KEY="sm_..."
```

For opencode CLI: would need to check if plugin system is compatible (OpenClaw uses different plugin architecture).

## Configuration

**Global:** `~/.supermemory-claude/settings.json`

| Option | Default | Description |
|--------|---------|-------------|
| `maxProfileItems` | 5 | Max memories injected into context |
| `signalExtraction` | false | Only capture important turns (keyword-based) |
| `signalKeywords` | remember, architecture, decision, bug, fix | Trigger keywords |
| `signalTurnsBefore` | 3 | Context turns saved before signal |
| `includeTools` | Edit, Write | Tool calls to capture |

**Per-project:** `.claude/.supermemory-claude/config.json`
- Project-specific API key
- Custom container tags (for team sharing)
- Override signal settings

## Commands

| Command | Description |
|---------|-------------|
| `/claude-supermemory:index` | Index codebase architecture and patterns |
| `/claude-supermemory:project-config` | Configure project settings |
| `/claude-supermemory:logout` | Clear credentials |

## Pricing

| Tier | Price | Tokens | Search Queries |
|------|-------|--------|----------------|
| **Free** | $0/mo | 1M tokens | 10K searches |
| **Pro** | $19/mo | 3M tokens | 100K searches |
| **Scale** | $399/mo | 80M tokens | 20M searches |
| **Enterprise** | Custom | Unlimited | Unlimited |

⚠️ README says **"Requires Supermemory Pro or above"** — meaning Free tier may not be sufficient for the Claude Code plugin specifically.

## Comparison: Supermemory vs Our pgvector Setup

| Aspect | Supermemory | Our pgvector (Iris) |
|--------|-------------|---------------------|
| **Hosting** | Cloud SaaS (their servers) | Self-hosted (our PostgreSQL VPS) |
| **Cost** | $19+/mo | ~$0.0001/day (Gemini embedding API) |
| **Auto-capture** | ✅ Yes (session hooks) | ❌ Manual (daily memory files + embed script) |
| **Search** | API call → cloud | SQL query → local pgvector |
| **Team sharing** | ✅ Container tags | ❌ Single-user |
| **Signal extraction** | ✅ Keyword-based filtering | ❌ Everything embedded |
| **Latency** | Network round-trip | Local (~ms) |
| **Data ownership** | Their cloud | Our database |
| **Scope** | Claude Code sessions | Iris WhatsApp + knowledge base |
| **Privacy** | Data on their servers | Data stays on our infra |

### Verdict

**For Iris:** ❌ Not relevant. Iris has her own memory system (pgvector + daily reflections + semantic search). Supermemory is a Claude Code plugin, not an OpenClaw/WhatsApp integration.

**For opencode CLI (this session):** 🟡 Potentially useful. Would give persistent memory across opencode coding sessions on Mac Mini. But:
- $19/mo minimum (Pro required)
- Data goes to their cloud (privacy concern for Zuma business data)
- Not clear if opencode CLI supports Claude Code plugins
- Our handoff notes + session search already provide cross-session context

**Bottom line:** Interesting concept, but we already have a self-hosted solution that's cheaper and more private. The auto-capture feature is nice but not worth $19/mo and cloud data dependency. Could inspire improvements to our own pgvector system (signal extraction, auto-capture from sessions).

## Ideas to Steal (for our pgvector system)

1. **Signal extraction** — Instead of embedding everything, detect important turns by keywords ("remember", "decision", "bug fix") and only embed those with surrounding context
2. **Auto-capture from sessions** — Script that post-processes opencode session logs and auto-embeds important exchanges
3. **Container tags** — Tag memories by project/repo for filtered recall

## Key Takeaways

- **Hosted SaaS memory layer** for Claude Code — not self-hostable
- **$19/mo minimum** for actual Claude Code plugin usage
- **Not compatible with OpenClaw/Iris** — different plugin ecosystem
- **Auto-capture is the killer feature** — we should build this into our pgvector system
- **Data goes to cloud** — privacy concern for business data
- **2.2k stars in 1 month** — shows strong demand for persistent AI memory

---

**Tags:** #memory #claude-code #persistent-memory #saas #supermemory #vector-search #auto-capture #team-memory #paid-service #comparison-pgvector
