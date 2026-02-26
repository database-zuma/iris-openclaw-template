# Iris Vector Memory + Reflection Cycle — Implementation Plan

**Date:** 2026-02-27
**Source:** AI Town (a16z) architecture analysis → applied to Iris/OpenClaw
**Status:** IMPLEMENTING

---

## Overview

Two patterns from AI Town's generative agent architecture applied to Iris:

1. **Vector Memory Search** — Replace grep-based memory retrieval with semantic vector similarity search via pgvector on existing PostgreSQL
2. **Daily Reflection Cycle** — Add end-of-day synthesis step where Iris reflects on accumulated interactions to form higher-level insights

## Pattern 1: Vector Memory Search

### Problem
Iris's current memory system uses flat markdown files + grep. Grep only finds exact keyword matches. "kapan terakhir bahas shipping delay?" won't match a memory entry that says "delay ekspedisi JNE ke Surabaya".

### Solution
Mirror memory entries as vector embeddings in PostgreSQL (pgvector). Semantic search via cosine similarity returns relevant memories regardless of exact wording.

### Architecture
```
Memory Write Flow:
  Iris writes memory/YYYY-MM-DD.md (unchanged)
  → embed_memory.py reads new entries
  → OpenAI text-embedding-3-small generates embeddings
  → Upsert to memory_vectors table in PostgreSQL

Memory Read Flow:
  Iris receives query needing context
  → search_memory.py embeds the query
  → SELECT * FROM memory_vectors ORDER BY embedding <=> query_embedding LIMIT 5
  → Returns top-K semantically relevant memory chunks
  → Iris uses as context for response
```

### Components
- **PostgreSQL**: pgvector extension + `memory_vectors` table
- **embed_memory.py**: Batch embed memory files → PostgreSQL
- **search_memory.py**: Semantic query interface
- **Embedding model**: OpenAI text-embedding-3-small (1536 dims, $0.02/1M tokens)
- **Fallback**: grep if pgvector unavailable

### Cost
~$0.0001/day (Iris daily memory ≈ 5-10K tokens)

## Pattern 2: Daily Reflection Cycle

### Problem
Iris logs raw interactions but never synthesizes patterns. Repeated requests, recurring failures, and behavioral patterns go unnoticed.

### Solution
At last heartbeat before quiet hours (22:00), Iris reads today's memory and generates a reflection:
- What patterns emerged?
- What failed and why?
- What should change tomorrow?

### Architecture
```
22:00 Heartbeat Trigger:
  → Read memory/YYYY-MM-DD.md
  → LLM synthesize into 3-5 insights
  → Write to memory/reflections/YYYY-MM-DD.md
  → If systemic insight → update AGENTS.md or relevant skill
```

### Output Format
```markdown
## Reflection — YYYY-MM-DD
### Patterns
- [observed pattern + implication]
### Issues
- [failure + root cause]
### Tomorrow
- [actionable priority for next day]
```

## Tags
#vector-memory #pgvector #semantic-search #reflection-cycle #iris-upgrade #ai-town-inspired #implementation
