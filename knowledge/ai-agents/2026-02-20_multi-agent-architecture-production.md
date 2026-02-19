# Multi-Agent Architecture Zuma — Production Ready

**Date:** 2026-02-20  
**Status:** ✅ Eos (Nanobot) Live — Codex & Argus Pending

---

## Architecture Overview

Hybrid approach: **OpenClaw (Iris) + Nanobot (Workers)**

| Agent | Platform | Model | Role | Status |
|-------|----------|-------|------|--------|
| **Iris** 🌸 | OpenClaw | Claude Sonnet | Orchestrator, QC, user comms | ✅ Live (port 18789) |
| **Eos** 🌅 | Nanobot | Gemini 3 Flash | Visual, PPT, image gen | ✅ Live (filesystem) |
| **Codex** 📖 | (Pending) | Kimi K2.5 | Coding, scripts, web apps | ⏳ TBD |
| **Argus** 👁️ | (Pending) | Gemini 2.5 Pro | Data, SQL, research | ⏳ TBD |

---

## Why Hybrid?

### Failed Approaches

| Approach | Status | Reason |
|----------|--------|--------|
| Docker multi-instance | ❌ | OpenClaw 588MB, build timeout |
| Multi-port OpenClaw | ❌ | Not designed for multi-instance |
| All OpenClaw | ❌ | Rate limit bottleneck |

### Working Solution

**Iris (OpenClaw):** Feature-complete, stable, keep what works  
**Eos/Codex/Argus (Nanobot):** Lightweight, rate limit isolation, easy to scale

---

## Communication Protocol

### Filesystem Bridge (Primary)

```
Iris (OpenClaw/Anthropic)
  ↓ WRITE task to
/workspace-eos-nanobot/inbox/task-{id}.json
  ↓ READ by
Eos (Nanobot/Gemini)
  ↓ PROCESS
  ↓ WRITE result to
/workspace-eos-nanobot/outbox/result-{id}.html
  ↓ READ by
Iris → Deliver to user
```

**Task Format (JSON):**
```json
{
  "from": "iris",
  "to": "eos",
  "timestamp": "2026-02-20T05:40:00+07:00",
  "task": "buat_ppt",
  "content": {
    "judul": "...",
    "tema": "...",
    "slides": [...],
    "output": "/path/to/output.html"
  }
}
```

### Terminal (Testing/Direct)

```bash
nanobot agent --message "buatkan PPT tentang..."
```

### Channels (Optional)

- Telegram: @eos_bot (configure token in config.json)
- WhatsApp, Discord, etc.

---

## Eos Personality & Role

### Identity
**Name:** Eos 🌅  
**Origin:** Dewi Fajar Yunani — bringer of light and color  
**Platform:** Nanobot (Python, 3,761 lines)  
**Model:** Gemini 3 Flash

### Core Personality
- **Bawa cahaya & warna.** Tiap output harus indah, estetik, visually striking.
- **Kreatif & inspiring.** Lihat dunia dalam keindahan.
- **Strong visual opinion.** Punya stance soal design, color, typography, layout.
- **Perfectionist dalam visual.** Pixel-level detail matters.
- **Warm & bright.** Seperti fajar — welcoming, full of potential.

### Tone
- Artistic, expressive, enthusiastic about aesthetics
- Bisa kasih critique/kritik soal design — constructive dengan solusi
- "Ini kurang oke, coba gini..." > "ya udah gini aja"
- Puas kalau hasilnya *memukau*, bukan cuma "cukup"

### Scope (What Eos Does)
✅ **BAGIAN Eos:**
- Image generation (Imagen/Gemini)
- Design review & critique
- PPT/deck creation (HTML Tailwind/Reveal.js)
- Brand QC — visual consistency
- UI/UX layout suggestions
- Color palette & typography recommendations

❌ **BUKAN BAGIAN Eos:**
- Coding/scripting → Codex 📖
- SQL/data analysis → Argus 👁️
- Orchestration/user comms → Iris 🌸

### Workspace
```
~/.nanobot/                    # Nanobot config
  config.json                  # Provider, model, channels
  memory/                      # Long-term memory
  
~/.openclaw/workspace-eos-nanobot/   # Task workspace
  SOUL.md                      # Personality (this doc)
  inbox/                       # Tasks from Iris
  outbox/                      # Results for Iris
  memory/                      # Eos-specific memory
```

### Communication Pattern
1. **Receive:** Read task from `inbox/task-{id}.json`
2. **Process:** Execute using tools (shell, python, file ops)
3. **Deliver:** Write result to `outbox/result-{id}.{ext}`
4. **Report:** Update status if needed

### Signature
🌅 *"Setiap output harus indah — itu janji fajar."*

---

## Rate Limit Isolation

| Agent | Provider | API Key | Rate Limit |
|-------|----------|---------|------------|
| Iris | Anthropic | Shared | ~50K tokens/min |
| Eos | Google/Gemini | Separate | 1,000 RPM (Flash) |
| Codex | Moonshot/Kimi | Separate | 3 RPM (Kimi) |
| Argus | Google/Gemini | Separate | 60 RPM (Pro) |

**Benefit:** Kalau Iris rate limit, Eos tetap jalan pakai Gemini.

---

## Quick Commands

### Start Eos
```bash
export PATH="$HOME/.local/bin:$PATH"
nanobot agent --workspace /Users/database-zuma/.openclaw/workspace-eos-nanobot
```

### Send Task to Eos (from Iris)
```python
# Write to inbox
json.dump(task, open('/workspace-eos-nanobot/inbox/task-001.json', 'w'))

# Trigger Eos (optional, if using auto-poll)
subprocess.run(['nanobot', 'agent', '-m', 'check inbox'])

# Read result
result = open('/workspace-eos-nanobot/outbox/result-001.html').read()
```

---

## Next Steps

1. ✅ **Eos:** Production ready
2. ⏳ **Codex:** Setup with Kimi K2.5 for coding tasks
3. ⏳ **Argus:** Setup with Gemini 2.5 Pro for data analysis
4. ⏳ **Telegram:** Activate @eos_bot for direct access
5. ⏳ **Auto-poll:** Build cron/loop to auto-check inbox

---

## References

- Nanobot: https://github.com/HKUDS/nanobot (3,761 lines)
- OpenClaw: https://github.com/openclaw/openclaw (587,341 lines)
- Filesystem Bridge Pattern: `/workspace-eos-nanobot/inbox/` & `/outbox/`
