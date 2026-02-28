# AI Agents 101 — Best Practices for Building Reliable Agents

**Source:** Article by Varick Agents CEO (3 years at Meta, running $3M agent company)
**URL:** varickagents.com
**Date:** Feb 2026

## Core Concepts

### What Makes an Agent Different from Automation
- **Automation** = follows instructions ("send this email")
- **Agent** = pursues goals ("make sure this customer gets a response within 4 hours") — figures out WHAT needs to happen, handles exceptions, learns from guidance

### The Agent Loop
```
Observe → Decide → Act → Observe result → Repeat until goal met or stopping condition
```

### Three Mandatory Components
1. **Perception** — how the agent sees the world (APIs, databases, document stores)
2. **Decision Logic** — how it chooses actions (structured decision trees for routine, LLM for ambiguous)
3. **Action Interface** — how it affects the world (logged, reversible where possible, gated by permissions, includes reasoning)

## Key Best Practices

### 1. Tools Design
- One tool = one thing. Clear success/failure states.
- Model doesn't execute tools directly — orchestration layer validates permissions, executes, captures result, feeds back.
- If a tool sometimes fails silently, the agent can't learn from it.

### 2. Memory Architecture
- **Context window** = active work (current task)
- **External memory** = history (completed tasks, logs, summaries)
- Agent decides what to load from memory based on current goal
- Memory doubles as audit trail — every decision logged with context

### 3. Planning Before Execution (CRITICAL)
- Most agent failures happen because people skip planning
- For anything non-trivial: break goal into steps → identify dependencies → human reviews plan → approve execution
- Without planning: agent starts executing, misses edge cases, wrong timing
- With planning: schema comparison, volume analysis, edge case identification, verification approach, rollback plan

### 4. Failure Handling (Three Modes)
- **Retry with backoff** — for transient failures (network timeout, rate limit)
- **Human-in-the-loop** — for low-confidence decisions, stop and ask
- **Safe failures** — never delete old data, always fail safely
- Key: make failures **observable** (what was it trying to do? what went wrong?)

### 5. Guardrails & Permissions
- **Guardrails** = hard limits agent can't bypass (never delete data, rate limits)
- **Permissions** = role-based access (can read but not modify)
- Agent doesn't know about constraints — just tries actions, orchestration layer enforces

### 6. The 80/20 Rule
- Handle 80% straightforward cases automatically
- Route 20% complex cases to humans who can apply judgment
- Goal: free human expertise for problems that actually require it

### 7. Start Narrow
- One agent, one task, reliable before expanding scope
- Define goal in specific terms → list info needed → build tools → test → add guardrails → add rate limits

---

## Mapping to Iris/OpenClaw — Gap Analysis

### ✅ ALREADY IMPLEMENTED (Strong)

| Practice | Iris Implementation |
|----------|-------------------|
| **Agent Loop** | Heartbeat system (5-min cycle): observe (check email/calendar/mentions/pending tasks) → decide (routing rules) → act (delegate to sub-agents) → observe result (poll heartbeat files) |
| **Perception Layer** | WhatsApp messages, email (via gog), calendar, PostgreSQL DB, web search (Exa), file system, Notion API (read-only) |
| **Decision Logic** | SKILLS_INDEX.md routing table (keyword → skill → agent), ORCHESTRATION.md pipeline patterns, AGENTS.md rules. Structured routing for routine, LLM reasoning for ambiguous |
| **Action Interface** | 7 agents: Metis (data/SQL), Daedalus (code), Hermes (web), Oracle (strategy), Eos (visual), Argus (research), Codex (full-stack). All via exec/sessions_spawn with background mode |
| **Tools = One Thing** | Each sub-agent has clear role. Each nanobot has clear domain. MCP tools are granular |
| **Memory Architecture** | ✅ Exactly matches best practice: context window for active work, external memory (memory/*.md, MEMORY.md, vector DB iris.memory_vectors with 619 signal-classified chunks) for history. Daily reflections at 22:00 |
| **Guardrails** | HUKUM BESI (users never talk to sub-agents), data security (raw.* schema forbidden), WA isolation (no cross-user data), pre-delivery self-check (5 points), trash > rm |
| **Permissions** | Role-based: Iris = delegation only (no scripts/code), Oracle = advisory only (zero exec), Notion = read-only. Orchestration layer enforces |
| **80/20 Rule** | Explicitly documented: "handle 80% straightforward, route 20% complex to humans" in awesome-openclaw use cases |
| **Human-in-the-loop** | Oracle escalation for strategy, Wayan escalation for stuck tasks (>30min), exec approval gates |
| **Audit Trail** | memory/*.md daily logs, heartbeat/*.md per-user tracking, session JSONL files, vector DB with signal classification |

### ⚠️ PARTIALLY IMPLEMENTED (Needs Improvement)

| Practice | Current State | Gap |
|----------|--------------|-----|
| **Retry with Backoff** | AGENTS.md says "Langsung retry kalau gagal" but no structured backoff pattern. Heartbeat escalation: 5min→10min→15min→30min, tapi ini monitoring bukan retry. | **Missing:** Formal exponential backoff for transient API failures (rate limits, network timeouts). Sub-agent retry is ad-hoc, not systematic. |
| **Planning Before Execution** | Oracle consultation exists for strategy. "Plan mode for any non-trivial task (3+ steps)". But in practice Iris sometimes jumps to execution on complex multi-step tasks. | **Gap:** No formal "generate plan → human reviews → approve → execute" workflow for complex tasks. Planning is encouraged but not enforced. |
| **Action Logging with Reasoning** | Actions are logged (memory/*.md, heartbeat files), but reasoning behind decisions is often missing. Sub-agent results are captured but "why this agent was chosen" isn't always recorded. | **Gap:** Need to log WHY an action was taken, not just WHAT was done. Especially for delegation decisions. |
| **Observable Failures** | Heartbeat escalation tracks stuck tasks. But when sub-agents fail, the error message is captured without structured diagnosis (what was attempted, what failed, what should change). | **Gap:** No structured failure report format. When Daedalus fails a script, Iris logs the error but doesn't systematically capture: attempted approach, failure mode, what to try differently. |

### ✅ NOW IMPLEMENTED (Added 2026-02-28)

| Practice | Implementation |
|----------|---------------|
| **Formal Retry Policy** | Added to `ORCHESTRATION.md § Step 4b`: retry table with 8 failure types, max retries, exponential backoff schedule (2s→4s→8s for network, 30s→60s→120s for rate limits), escalation paths. Transient vs permanent failure distinction. |
| **Plan-Review-Execute Gate** | Added to `ORCHESTRATION.md § Step 2b`: activation table (5+ steps, cross-system, destructive, ambiguous), full flow (generate plan → send to requesting USER → wait approval → execute), WhatsApp-friendly plan template. Approval from requesting user, not Wayan. |
| **Reasoning Annotations** | Added to `AGENTS.md § Workflow Discipline`: mandatory format (DELEGASI → REASONING → ALTERNATIVE), good/bad examples, required for every delegation and retry decision. |

## Takeaways

1. **Iris already follows ~80% of the article's best practices** — the architecture is mature and well-documented
2. **Biggest gap: formal retry with backoff** — currently "retry if fail" without structure. Should be exponential backoff with max attempts per tool type
3. **Second gap: planning enforcement** — planning exists as guidance but not as a gate. Complex tasks should require plan → review → approve → execute
4. **Third gap: reasoning in logs** — actions are logged but WHY decisions were made is often implicit. Adding reasoning annotations would improve future debugging
5. **The article validates our 80/20 approach** — "handle 80% straightforward, route 20% to humans" is exactly how Iris operates with Wayan escalation

## Tags

#ai-agents #best-practices #agent-architecture #iris-audit #failure-handling #planning #retry #guardrails #perception #decision-logic #action-interface #memory #varick-agents
