# OpenManus — Open-Source General AI Agent Framework (Manus Clone)

**Source:** https://github.com/FoundationAgents/OpenManus
**Date:** 2026-02-28
**Stars:** 54,800 ⭐ | **Forks:** 9,600 | **Commits:** 526 | **Contributors:** 58
**License:** MIT | **Language:** Python (97.8%) | **Python:** ≥3.12
**By:** FoundationAgents (MetaGPT team — @mannaandpoem, @XiangJinyu, @MoshiQAQ, @didiforgithub, @stellaHSR)
**Last Release:** v0.3.0 (Apr 2025) | **Last Commit:** Jan 3, 2026 (README update) | **Active development:** Stale-ish (last real code: Sep 2025)

---

## Key Points

1. **Open-source clone of Manus AI** — the viral Chinese AI agent that required invite codes. OpenManus replicates the core idea: a general-purpose AI agent that can browse the web, write code, analyze data, and execute tasks autonomously. Prototype launched in 3 hours by MetaGPT core team.

2. **Architecture:** Single agent (`main.py`) or multi-agent flow (`run_flow.py`). Uses OpenAI-compatible LLM APIs (GPT-4o default, any provider via `base_url`). Built-in tools: browser automation (Playwright), file operations, code execution, web scraping (Crawl4AI). MCP tool integration via `run_mcp.py`.

3. **Three execution modes:**
   - `python main.py` — Single agent, interactive terminal. Input a task → agent plans and executes.
   - `python run_flow.py` — Multi-agent flow with specialized agents (general + data analysis).
   - `python run_mcp.py` — MCP-enabled version with external tool servers.

4. **Data Analysis Agent** (optional) — Specialized agent for data analysis + visualization. Enable in config: `[runflow] use_data_analysis_agent = true`. Separate chart visualization dependencies.

5. **A2A Protocol support** — Has `protocol/a2a/` directory for Agent-to-Agent communication protocol.

6. **Sandbox execution** — `sandbox_main.py` for isolated code execution (Docker-based, Python 3.12 image).

7. **Config-driven** — `config/config.toml` for LLM settings. Supports separate vision model config. Multiple API providers (OpenAI, custom, JiekouAI).

## Architecture

```
User Input (terminal)
    │
    ▼
OpenManus Agent (LLM-powered planning loop)
    ├── Think → Plan → Execute → Observe cycle
    ├── Tools:
    │   ├── Browser (Playwright) — web browsing, form filling, screenshots
    │   ├── Code Execution — Python sandbox
    │   ├── File Operations — read/write workspace files
    │   ├── Web Scraping (Crawl4AI) — structured web extraction
    │   └── MCP Tools — external tool servers
    └── Output → workspace/ directory
```

**Multi-Agent Flow (`run_flow.py`):**
```
User Input → Flow Orchestrator
    ├── General Agent (planning, web browsing, code)
    └── Data Analysis Agent (pandas, visualization)
```

## Quick Start

```bash
# Install
git clone https://github.com/FoundationAgents/OpenManus.git
cd OpenManus
uv venv --python 3.12 && source .venv/bin/activate
uv pip install -r requirements.txt
playwright install  # Optional: browser automation

# Configure
cp config/config.example.toml config/config.toml
# Edit config.toml: set model, base_url, api_key

# Run
python main.py           # Single agent
python run_flow.py       # Multi-agent flow
python run_mcp.py        # MCP-enabled
python sandbox_main.py   # Sandboxed execution
```

## Config Example

```toml
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."
max_tokens = 4096
temperature = 0.0

[llm.vision]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."

[runflow]
use_data_analysis_agent = true  # Optional
```

## Comparison with Our Stack

| Aspect | OpenManus | Iris (OpenClaw + Nanobot) |
|--------|-----------|--------------------------|
| Architecture | Single/multi-agent, Python app | Multi-agent hybrid (OpenClaw gateway + Nanobot) |
| LLM Integration | OpenAI-compatible API only | Direct provider APIs (Anthropic, Google, Kimi, OpenRouter) |
| Communication | Terminal I/O, no messaging | WhatsApp, Discord, multi-channel |
| Browser | Playwright (built-in) | agent-browser (Rust CLI, 93% less tokens) + Playwright MCP |
| Memory | None (stateless per session) | pgvector semantic memory + signal extraction |
| Tools | Built-in (browser, code, files, Crawl4AI) | Skills system (24+ skills) + MCP servers + Nanobot agents |
| Deployment | Python script, Docker | Persistent daemon (launchd), VPS + Mac Mini |
| Heartbeat/Cron | None | Heartbeat cycle, cron automation, proactive follow-up |
| Maturity | Prototype-grade, stale since Sep 2025 | Production, daily use, actively maintained |

## Takeaways

1. **Massively popular but shallow.** 54.8k stars driven by Manus hype (Mar 2025), but architecture is straightforward — LLM planning loop with tool execution. No memory, no persistence, no multi-channel. Prototype quality.

2. **Development stalled.** Last real code change was Sep 2025 (5 months ago). Last release v0.3.0 was Apr 2025 (10 months ago). README update Jan 2026 but no feature work. Community PRs seem to have stopped.

3. **Not relevant for Iris.** Our stack (OpenClaw + Nanobot) is significantly more mature: persistent memory, multi-channel messaging, heartbeat monitoring, skill routing, agent delegation hierarchy. OpenManus doesn't solve any problem we haven't already solved better.

4. **Interesting patterns to note:**
   - **A2A protocol** directory — could be worth watching if the Agent-to-Agent protocol standardizes
   - **Sandbox execution** pattern — Docker-based code isolation, good security practice
   - **Config-driven LLM selection** — TOML config with separate vision model is clean

5. **OpenManus-RL is more interesting.** Their spin-off project [OpenManus-RL](https://github.com/OpenManus/OpenManus-RL) applies reinforcement learning (GRPO) to tune LLM agents. Research-oriented, from UIUC collaboration. This is where the real innovation is, not the base OpenManus framework.

6. **Low priority.** Nothing to adopt. File under "awareness" — it's the most-starred AI agent repo, so worth knowing about when people reference it.

---

**Tags:** #ai-agents #open-source #manus-clone #metagpt #multi-agent #browser-automation #python #low-priority #awareness-only
