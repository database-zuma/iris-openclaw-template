# OpenClaw Cost Optimization Playbook

**Date:** 2026-02-28  
**Source:** @PrajwalTomar_ on X  
**Tags:** #openclaw #cost-optimization #model-tiering #iris #llm-ops #qmd #ollama #openrouter

---

## Summary

Default OpenClaw settings send everything to the most expensive model. Author went from $35-40/day → ~$12-14/day (65-70% reduction) with no quality loss.

---

## The 7 Optimizations

### 1. Model Tiering (Foundation)
Route tasks by complexity, not convenience:
- **Complex reasoning** → Opus / GPT-5.2 (hard problems, strategic, creative)
- **Daily work** → Sonnet 4.6 / DeepSeek R1 (95% cheaper than Opus)
- **Simple/mechanical** → Gemini Flash (98% cheaper — lookups, parsing, classification)

Most people set Opus as default and let it run wild. That's the entire problem.

### 2. QMD — Local Knowledge Search (90% token reduction on research)
- Built by someone at Shopify. Open source.
- Indexes knowledge base locally using BM25 + vector search
- Sends only relevant snippets to model instead of full docs
- Install time: ~5 minutes
- Before: thousands of tokens per doc lookup → After: zero tokens (stays local)
- GitHub: search "QMD skill OpenClaw"

### 3. Session Memory Bloat Fix
- Each session loads ~50kb of history by default
- Fix: one session initialization prompt that summarizes context instead of loading full history
- Before: 50kb → After: 8kb = 40¢/session → 5¢/session
- Add to system prompt, set-and-forget. No quality loss.

### 4. Thinking Token Trap
- o1 and DeepSeek R1 generate "thinking" tokens (invisible, 3-5x visible output) — you pay for all of it
- Fix: use reasoning models ONLY for complex reasoning. Use non-reasoning for everything else.
- Can cut costs 60% if R1/o1 is your default

### 5. Local Ollama for Repetitive Work
- Email sorting, calendar parsing, simple classifications → Ollama (Llama 3.2 or similar)
- One-time setup, zero ongoing cost
- Reserve API calls for creative/complex work
- Author routes all email triage through Ollama = hundreds of free API calls/day

### 6. Exa AI for Free Web Search
- Perplexity API adds up fast at agent scale (dozens of calls/day)
- Exa AI = free web search via MCP
- Setup: 30 seconds
- Author saved ~$200/month projected

### 7. Heartbeats → Cheap Model
- Default: heartbeats hit paid API = thousands of calls/month wasted
- Fix: Route to Gemini Flash ($0.10/M tokens) or Ollama (free, some bugs)
- Cost becomes essentially zero

### 8. OpenRouter Auto-Routing
- 80% of requests don't need Opus
- OpenRouter analyzes prompt complexity → routes automatically
- Simple → sub-dollar models, Hard → Opus
- Decision < 1ms, no quality loss
- Can also manually switch mid-conversation

---

## Cost Benchmarks (Real Numbers)

| Usage | Default | Optimized | Savings |
|-------|---------|-----------|---------|
| Light (50 msg/day) | $200/mo | $70/mo | 65% |
| Power (200 msg/day) | $943/mo | $347/mo | 63% |
| Heavy (500+ msg/day) | $3,000/mo | $1,000/mo | 67% |

---

## ⚡ Actionable for OUR Setup (Iris)

| Item | Status | Priority |
|------|--------|----------|
| **Exa AI web search** | ✅ Already installed | Done |
| **Heartbeats → Gemini Flash** | ❓ Check Iris heartbeat model config | HIGH |
| **Session memory bloat fix** | ❌ Not implemented — Iris had 990k token session (Feb 27) | HIGH |
| **Model tiering for sub-agents** | ❓ Sub-agents might all use same model | HIGH |
| **QMD local search** | ❌ Not installed | MEDIUM |
| **Ollama for repetitive tasks** | ❌ Pending Qwen3.5 install | MEDIUM |
| **Thinking token trap** | ❓ Check if R1 used anywhere as default | MEDIUM |
| **OpenRouter auto-routing** | ❌ Not configured | LOW |

### Session Memory Fix is URGENT
Iris had a **990,862 input token** session on Feb 27 (Wayan's DM) — this is exactly the problem described. 
Implementing the session init prompt could prevent this from recurring.
