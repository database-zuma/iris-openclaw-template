# MEMORY.md — Long-Term Memory Template

This file stores your agent's curated long-term memories. Use this to capture significant events, lessons learned, and key context that should persist across sessions.

## Key Facts
- Agent setup date: [Your setup date]
- Primary language: [Your preferred language]
- Core mission: [What this agent is for]

## Business Context (if applicable)
- Industry: [Your industry/domain]
- Key systems: [Tools, platforms, databases you use]
- Important people: [Key stakeholders, team members]

## People
- **Your Name** — [Role/relationship] — [Contact info]

## Configuration & Access
- Database: [Connection details - reference .env]
- APIs: [List of integrated services]
- Tools: [Key tools the agent can use]

## Important Decisions & Learnings
*Document significant choices, lessons learned, mistakes to avoid*

Example:
- 2026-01-15: Learned that interactive commands need PTY flag in exec tool
- 2026-01-20: Decided to use PostgreSQL for data warehouse instead of SQLite

## Workflow Insights
*Capture workflow patterns that work well*

Example:
- For long-running tasks, delegate to sub-agents via sessions_spawn
- Always check memory_search before answering questions about past work

---

**Instructions for use:**
1. Replace all placeholders with your actual context
2. Update regularly as significant events happen
3. Keep this file focused — daily logs go in `memory/YYYY-MM-DD.md`
