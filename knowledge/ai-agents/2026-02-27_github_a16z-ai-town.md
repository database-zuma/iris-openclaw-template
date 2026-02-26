# AI Town — Autonomous Agent Town Simulator (a16z-infra)

**Source:** https://x.com/tom_doerr/status/2027013524048769458
**Repo:** https://github.com/a16z-infra/ai-town
**Demo:** https://convex.dev/ai-town
**Date saved:** 2026-02-27
**License:** MIT
**Stars:** 9.3k ⭐ | Forks: 982
**Status:** NOT INSTALLED — reference/inspiration only

---

## What Is It

A deployable starter kit for building a **virtual town where AI characters live, chat, and socialize autonomously**. Inspired by the Stanford research paper *"Generative Agents: Interactive Simulacra of Human Behavior"* (2023).

AI agents in the town:
- **Perceive** their environment (who's nearby, what's happening)
- **Remember** past interactions via vector search over conversation history
- **Reflect** on memories to form opinions and plans
- **Act** autonomously — walk around, start conversations, form relationships
- **Converse** with each other using LLM-generated dialogue

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Game engine + DB + Vector search | Convex (real-time backend) |
| Frontend rendering | PixiJS (2D pixel art) |
| LLM (default) | Ollama (llama3) — local |
| LLM (cloud) | OpenAI, Together.ai, any OpenAI-compatible API |
| Embeddings | mxbai-embed-large (Ollama) or OpenAI |
| Music generation | Replicate (MusicGen) |
| Auth (optional) | Clerk |
| Deploy | Vercel + Convex Cloud, Docker Compose, Fly.io |

## Architecture Patterns (Relevant to Multi-Agent Systems)

### 1. Agent Memory System
- Each agent stores conversation history as **vector embeddings**
- On interaction, agent retrieves **relevant memories** via vector similarity search
- Memories influence agent behavior, personality, and conversation topics
- Configurable `NUM_MEMORIES_TO_SEARCH` for context window management

### 2. Simulation Engine (Tick-Based)
- Convex provides a **deterministic simulation engine** with shared global state
- All agents operate on the same world state with **ACID transactions**
- Cron jobs for periodic tasks (music generation, world maintenance)
- Engine can be paused/resumed/archived via CLI commands

### 3. Agent Behavior Loop
```
perceive → retrieve memories → reflect → plan → act → store new memory
```
- Perception: scan nearby agents, objects, conversations
- Memory retrieval: vector search for relevant past experiences
- Reflection: LLM synthesizes observations + memories into plans
- Action: movement, conversation initiation, idle behavior
- Storage: new experiences → vector embeddings → memory bank

### 4. Real-Time Shared State
- Convex's reactive subscriptions = all clients see world updates instantly
- Server functions are transactional (serializable isolation, OCC/MVCC)
- Suitable for multi-player scenarios with concurrent agent actions

### 5. Agent-to-Agent Communication
- Agents initiate conversations based on proximity + personality + memory
- Conversations are multi-turn, LLM-generated
- Conversation outcomes become new memories for both agents

## Relevance to Iris / OpenClaw

### Direct Architectural Parallels
| AI Town Pattern | OpenClaw Equivalent |
|----------------|---------------------|
| Agent memory (vector embeddings) | Iris memory/ folder + MEMORY.md |
| Simulation tick loop | Heartbeat system (5-min polling) |
| Shared world state (Convex) | Shared workspace filesystem |
| Agent behavior loop (perceive→plan→act) | Iris delegation loop (receive→route→delegate→follow-up) |
| Agent-to-agent conversation | Sub-agent spawning + session continuity |
| Cron-based maintenance | Atlas/Iris Junior/Apollo VPS cron jobs |

### What Iris Can Learn From This
1. **Structured memory retrieval** — AI Town uses vector search to find relevant memories. Iris currently does grep-based memory search. Vector embeddings could make Iris's context recall much smarter.
2. **Agent reflection cycle** — AI Town agents periodically "reflect" on accumulated memories to form higher-level insights. Iris could benefit from a similar consolidation step (daily memory → weekly synthesis → long-term lessons).
3. **Deterministic simulation** — AI Town's Convex backend ensures all state changes are transactional. Iris's heartbeat-based filesystem coordination could adopt similar patterns to prevent race conditions between nanobots.
4. **Personality-driven behavior** — Each AI Town agent has defined personality traits that influence decisions. OpenClaw agents (Metis, Daedalus, etc.) already have role descriptions, but could have more nuanced "personality" parameters for response style.

### What's NOT Directly Useful
- The pixel art / 2D game rendering (PixiJS) — not relevant to business automation
- The spatial proximity model — Iris routes by task type, not physical location
- Ollama as default LLM — Iris already uses Gemini/Opus/Kimi

## Tags

#multi-agent #autonomous-agents #simulation #memory-system #vector-search #convex #a16z #stanford-paper #generative-agents #agent-architecture #reference-only

## Quick Commands

```bash
# Clone & run locally (requires Node.js + Ollama)
git clone https://github.com/a16z-infra/ai-town.git
cd ai-town && npm install && npm run dev
# Visit http://localhost:5173

# Docker Compose (self-contained)
docker compose up --build -d
```
