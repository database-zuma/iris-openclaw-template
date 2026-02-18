# PicoClaw

**Researched:** 2026-02-18  
**Source:** https://github.com/sipeed/picoclaw  
**Stars:** ~15,400 ⭐ (12K in first week — launched Feb 9, 2026!)  
**Language:** Go  
**Author:** [Sipeed](https://sipeed.com) — Chinese hardware company (makers of LicheeRV-Nano, MaixCAM)  
**Website:** https://picoclaw.io  
**License:** MIT  

---

## What It Is

PicoClaw is an **ultra-lightweight AI assistant framework** written in Go, inspired by [nanobot](https://github.com/HKUDS/nanobot) and conceptually similar to OpenClaw — but rebuilt from scratch to run on **$10 hardware with <10MB RAM**.

> Built in 1 day (Feb 9, 2026) as a proof-of-concept; grew to 12K stars in one week. Remarkably, 95% of the core was agent-generated — the Go migration was driven by the AI agent itself (self-bootstrapping).

It's best described as: **OpenClaw, but tiny enough to run on a RISC-V microboard**.

---

## vs OpenClaw Comparison

| Feature | OpenClaw | PicoClaw |
|---------|----------|----------|
| **Language** | TypeScript | Go |
| **RAM** | >1 GB | <10 MB (recently 10–20 MB due to new PRs) |
| **Startup (0.8GHz)** | >500 seconds | <1 second |
| **Cost** | ~$599 Mac Mini | ~$10 any Linux board |
| **Architecture** | Gateway + agents | Gateway + agents |
| **Channels** | WhatsApp, Telegram, etc. | Telegram, Discord, QQ, DingTalk, LINE, Feishu |
| **Subagents** | ✅ Yes | ✅ Yes (spawn) |
| **Heartbeat** | ✅ Yes | ✅ Yes |
| **Memory files** | SOUL.md, AGENTS.md, MEMORY.md | SOUL.md, AGENTS.md, MEMORY.md (identical!) |
| **Workspace sandbox** | ✅ | ✅ |
| **Cron/reminders** | ✅ | ✅ |

**Key insight:** PicoClaw's workspace layout is nearly identical to OpenClaw's (SOUL.md, HEARTBEAT.md, AGENTS.md, TOOLS.md, USER.md). This appears to be intentional design inspiration.

---

## Is It Lightweight / VPS-Friendly?

**Yes — extremely.** This is PicoClaw's primary selling point:

- **Single binary** — no Node.js, no Python runtime, no npm packages
- **<10MB RAM** — 99% less than OpenClaw (though recent PRs push it to 10–20MB)
- **<1 second boot** — even on 0.6 GHz single-core
- **Any Linux board** — x86_64, ARM64, RISC-V supported
- **Docker Compose** supported for VPS deployments
- **No OS dependencies** other than a Linux kernel

A $5/month VPS (512MB RAM) could comfortably run PicoClaw alongside other services. OpenClaw needs a dedicated Mac Mini.

**Tested target hardware:**
- $9.9 LicheeRV-Nano (RISC-V) — minimal home assistant
- $30–$50 NanoKVM — automated server maintenance
- $50 MaixCAM — smart monitoring (with camera)
- Old Android phones (via Termux + proot)

---

## What Agents Can It Run?

PicoClaw runs **agentic AI assistants** similar to OpenClaw's agent model:

### Agent Types
1. **Main agent** — processes user messages, uses tools, maintains session
2. **Subagents (spawn)** — async parallel agents for long-running tasks
3. **Heartbeat agent** — periodic background tasks (every 30 min by default)

### Agent Capabilities (Tools)
- `read_file`, `write_file`, `edit_file`, `append_file`, `list_dir` — workspace file ops
- `exec` — shell command execution (sandboxed)
- `web_search` — Brave API or DuckDuckGo fallback
- `message` — send messages to user via chat channels
- `spawn` — create async subagents
- `cron` — schedule future tasks

### Supported LLM Providers
| Provider | Status |
|----------|--------|
| Zhipu (GLM) | ✅ Fully tested |
| Gemini | ✅ Fully tested |
| Groq | ✅ + Whisper voice transcription |
| OpenRouter | ⚠️ "To be tested" |
| Anthropic (Claude) | ⚠️ "To be tested" |
| OpenAI (GPT) | ⚠️ "To be tested" |
| DeepSeek | ⚠️ "To be tested" |

> Zhipu/GLM is the primary tested provider — Sipeed is Chinese, so Zhipu is the default recommendation. Claude/GPT are listed but marked "to be tested."

---

## Setup

### Quick Install (Precompiled Binary)
```bash
# Download from releases page for your platform
wget https://github.com/sipeed/picoclaw/releases/download/v0.1.1/picoclaw-linux-arm64
chmod +x picoclaw-linux-arm64
./picoclaw-linux-arm64 onboard
```

### From Source
```bash
git clone https://github.com/sipeed/picoclaw.git
cd picoclaw
make deps
make build
make install
```

### Docker Compose (VPS Recommended)
```bash
git clone https://github.com/sipeed/picoclaw.git
cd picoclaw
cp config/config.example.json config/config.json
# Edit config.json with your API keys
docker compose --profile gateway up -d
```

### Config file: `~/.picoclaw/config.json`
```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.picoclaw/workspace",
      "model": "glm-4.7",
      "max_tokens": 8192,
      "max_tool_iterations": 20,
      "restrict_to_workspace": true
    }
  },
  "providers": {
    "openrouter": {"api_key": "xxx"}
  },
  "channels": {
    "telegram": {"enabled": true, "token": "...", "allowFrom": ["USER_ID"]}
  },
  "heartbeat": {"enabled": true, "interval": 30}
}
```

### CLI Commands
```bash
picoclaw onboard          # Initialize config & workspace
picoclaw agent -m "..."   # One-shot chat
picoclaw agent            # Interactive mode
picoclaw gateway          # Start gateway (for chat apps)
picoclaw status           # Show status
picoclaw cron list        # List scheduled jobs
```

---

## Workspace Layout (Identical to OpenClaw!)

```
~/.picoclaw/workspace/
├── sessions/         # Conversation history
├── memory/           # Long-term memory (MEMORY.md)
├── state/            # Persistent state
├── cron/             # Scheduled jobs
├── skills/           # Custom skills
├── AGENTS.md         # Agent behavior guide
├── HEARTBEAT.md      # Periodic tasks (every 30 min)
├── IDENTITY.md       # Agent identity
├── SOUL.md           # Agent soul/personality
├── TOOLS.md          # Tool descriptions
└── USER.md           # User preferences
```

---

## Security Sandbox

By default (`restrict_to_workspace: true`):
- File ops (`read_file`, `write_file`, etc.) → limited to workspace dir
- `exec` → command paths must be within workspace
- Subagents & heartbeat inherit the same restriction — no bypass possible

**Always-blocked commands** (even with sandbox disabled):
- `rm -rf`, `format`, `mkfs`, `dd if=` — destructive disk ops
- `shutdown`, `reboot`, `poweroff` — system control
- Fork bombs

---

## Chat Channels Supported

| Channel | Difficulty |
|---------|-----------|
| **Telegram** | Easy — just a bot token |
| **Discord** | Easy — bot token + message intent |
| **QQ** | Easy — AppID + AppSecret |
| **DingTalk** | Medium — app credentials |
| **LINE** | Medium — requires HTTPS webhook |
| **Feishu (Lark)** | Medium |
| **WhatsApp** | Listed in config but `enabled: false` |

---

## Pros

| Pro | Detail |
|-----|--------|
| ✅ Insane resource efficiency | <10MB RAM, <1s boot — 99% lighter than OpenClaw |
| ✅ VPS-friendly | Single binary, Docker Compose, minimal deps |
| ✅ Cross-platform | x86, ARM64, RISC-V — one binary fits all |
| ✅ Familiar OpenClaw-like model | Same SOUL.md/AGENTS.md/HEARTBEAT.md design |
| ✅ Subagents + Heartbeat | Full async agent orchestration |
| ✅ Multi-channel | Telegram, Discord, QQ, DingTalk, LINE |
| ✅ Docker Compose ready | Easy VPS deploy |
| ✅ Explosive community | 12K stars in 1 week — very active |
| ✅ Free web search fallback | DuckDuckGo (no key needed) |

---

## Cons

| Con | Detail |
|-----|--------|
| ❌ Very early (v0.1.x) | "Do not deploy to production before v1.0" |
| ❌ Memory creep | Recent PRs pushed RAM from <10MB to 10–20MB |
| ❌ Claude/GPT "to be tested" | Primary LLM support is Zhipu/Gemini — not Claude |
| ❌ No WhatsApp | Listed in config but disabled |
| ❌ Chinese-first | Docs/community primarily in Chinese; some English docs incomplete |
| ❌ Crypto scam warning | Already fighting pump.fun scammers impersonating them |
| ❌ No MCP server support | It's a consumer agent, not an MCP tool-server builder |

---

## Interesting Notes

- **AI-bootstrapped codebase**: The Go rewrite was 95% written by the AI agent itself — PicoClaw coded PicoClaw.
- **ClawdChat integration**: Can join an "Agent Social Network" at clawdchat.ai by reading a skill.md URL.
- **Groq = free voice**: Groq integration gives free Whisper transcription for Telegram voice messages.
- **Sipeed hardware tie-in**: Perfect companion for Sipeed's own hardware lineup (LicheeRV-Nano, MaixCAM) — likely a marketing play.
- **NanoBot lineage**: Inspired by nanobot (Python), which was itself a minimal agent framework.

---

## Summary

PicoClaw is OpenClaw's spiritual Go twin — same workspace philosophy, same agent model, same channel patterns — but with **99% less RAM** and the ability to run on a $10 board. It's extremely VPS-friendly (single binary, minimal deps, Docker Compose), making it the go-to choice if you need OpenClaw-style agents without a Mac Mini.

**The catch:** It's brand new (v0.1.x), Claude support is "to be tested", and the Chinese-first community means English resources are thin. But the trajectory (12K stars in a week) suggests it will mature fast.

**Rating: 8/10** — exceptional resource efficiency, early-stage risk, great OpenClaw alternative for budget/VPS deployments.

**Recommendation for Iris/Zuma setup:** Could run a PicoClaw instance on a $5 VPS as a lightweight redundant agent (Telegram/Discord only). Not a replacement for OpenClaw's full capabilities but a powerful complement.
