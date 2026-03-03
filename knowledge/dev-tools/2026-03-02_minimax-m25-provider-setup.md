# MiniMax M2.5 — Provider Setup & Troubleshooting Guide

**Date:** 2026-03-02  
**Author:** Wayan + OpenCode  
**Status:** ✅ Implemented & Verified  
**Tags:** #minimax #model-provider #openclaw #iris #coding-plan #api #troubleshooting

---

## Overview

MiniMax M2.5 adalah primary model untuk SEMUA OpenClaw agents (Iris + sub-agents + VPS agents) sejak 2 Maret 2026. Dipilih karena Coding Plan pricing (flat rate, bukan per-token) dan performa yang sebanding dengan Claude Sonnet.

---

## Provider Details

| Field | Value |
|-------|-------|
| **Provider Name** | `iris-minimax` |
| **Model ID** | `MiniMax-M2.5` |
| **Full reference** | `iris-minimax/MiniMax-M2.5` |
| **API Type** | OpenAI-compatible (`/v1`) dan Anthropic-compatible (`/anthropic`) |
| **Base URL (OpenAI)** | `https://api.minimax.io/v1` |
| **Base URL (Anthropic/OpenClaw)** | `https://api.minimax.io/anthropic` |
| **Pricing** | Coding Plan (flat rate, 5-hour rolling window) |
| **Dashboard** | `https://platform.minimax.io/user-center/payment/coding-plan` |

### Available Models

| Model | Use Case |
|-------|----------|
| `MiniMax-M2.5` | **Primary** — best quality |
| `MiniMax-M2.5-highspeed` | Faster, slightly lower quality |
| `MiniMax-M2.1` | Previous gen |
| `MiniMax-M2.1-highspeed` | Previous gen, fast |
| `MiniMax-M2` | Oldest gen |

### Rate Limits

- 5-hour rolling window (Coding Plan)
- Jika rate limited, akan return HTTP 429
- OpenClaw auto-fallback ke model berikutnya di fallback chain

---

## Configuration Files

### 3 files per agent yang perlu di-update:

#### 1. `models.json` — Provider definition

```json
{
  "providers": {
    "iris-minimax": {
      "displayName": "MiniMax Coding Plan",
      "baseUrl": "https://api.minimax.io/anthropic",
      "api": "anthropic",
      "models": ["MiniMax-M2.5", "MiniMax-M2.5-highspeed"],
      "apiKey": {
        "source": "profile",
        "provider": "iris-minimax",
        "id": "iris-minimax"
      }
    }
  }
}
```

**Lokasi per agent:**
- Local: `~/.openclaw/agents/{agent-name}/agent/models.json`
- VPS: `/root/.openclaw/agents/{agent-name}/agent/models.json`

#### 2. `auth-profiles.json` — API key

```json
{
  "profiles": {
    "iris-minimax:iris-minimax": {
      "token": "sk-cp-XXXXX...actual-key-here",
      "usageStats": {}
    }
  }
}
```

**Lokasi per agent:**
- Local: `~/.openclaw/agents/{agent-name}/agent/auth-profiles.json`
- VPS: `/root/.openclaw/agents/{agent-name}/agent/auth-profiles.json`

#### 3. `openclaw.json` — Model routing (global)

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "iris-minimax/MiniMax-M2.5",
        "fallbacks": [
          "anthropic/claude-sonnet-4-6",
          "google/gemini-3-flash-preview"
        ]
      }
    }
  }
}
```

**Lokasi:**
- Local: `~/.openclaw/openclaw.json`
- VPS: `/root/.openclaw/openclaw.json`

---

## Agent Inventory

### Local Mac Mini (7 agents)

| Agent | Config Path |
|-------|-------------|
| **Iris** (main) | `~/.openclaw/agents/iris/agent/` |
| **Aura** | `~/.openclaw/agents/aura/agent/` |
| **Daedalus** | `~/.openclaw/agents/daedalus/agent/` |
| **Hermes** | `~/.openclaw/agents/hermes/agent/` |
| **Main** | `~/.openclaw/agents/main/agent/` |
| **Metis** | `~/.openclaw/agents/metis/agent/` |
| **Oracle** | `~/.openclaw/agents/oracle/agent/` |

### VPS 76.13.194.103 (3 agents)

| Agent | Config Path |
|-------|-------------|
| **Main** | `/root/.openclaw/agents/main/agent/` |
| **Ops** (Atlas) | `/root/.openclaw/agents/ops/agent/` |
| **Rnd** (Apollo) | `/root/.openclaw/agents/rnd/agent/` |

---

## Fallback Chain

```
Primary:   iris-minimax/MiniMax-M2.5
Fallback 1: anthropic/claude-sonnet-4-6
Fallback 2: google/gemini-3-flash-preview
```

VPS sedikit berbeda:
```
Primary:   iris-minimax/MiniMax-M2.5
Fallback 1: google/gemini-flash-lite
Fallback 2: deepseek/deepseek-chat
Fallback 3: anthropic/claude-sonnet-4-6
```

---

## `<think>` Tag Behavior

MiniMax M2.5 outputs reasoning dalam `<think>...</think>` tags. Ini NORMAL dan DIINGINKAN (thinking = better output quality).

**Handling:**
- **OpenClaw agents:** Tags otomatis di-strip oleh gateway sebelum dikirim ke user via WhatsApp/Telegram
- **accurate-dashboard (Metis chat):** Di-strip oleh `hideThinkTags()` function di `metis-message.tsx` sebelum ReactMarkdown render
- **API direct call:** Caller harus strip sendiri dengan regex: `/^<think>[\s\S]*?<\/think>\s*/`

**JANGAN** tambahkan system prompt instruction untuk suppress thinking — biarkan model mikir, cuma hide dari user.

---

## Troubleshooting

### Problem: Agent stuck pada model lama (bukan MiniMax)

**Root Cause:** OpenClaw caches model per session di `sessions.json`. Jika MiniMax pernah gagal (billing/rate limit), OpenClaw fallback ke model lain dan CACHE model fallback tersebut. Even after fixing config + restarting gateway, cached session tetap pakai model lama.

**Fix:**
```bash
# 1. Clear cached model dari semua sessions
python3 -c "
import json
path = '/Users/database-zuma/.openclaw/agents/iris/sessions/sessions.json'
with open(path) as f: data = json.load(f)
for sid, sess in data.get('sessions', {}).items():
    if 'model' in sess: del sess['model']
    if 'state' in sess and 'model' in sess['state']: del sess['state']['model']
with open(path, 'w') as f: json.dump(data, f, indent=2)
print('Cleared cached models')
"

# 2. Restart gateway
pkill -f openclaw-gateway && sleep 5

# 3. Verify
openclaw agent --agent iris --message "kamu pakai model apa?" --json
```

**Key insight:** `sessions.json` punya field `model` per session yang OVERRIDE global config di `openclaw.json`. Ini by design (untuk session stickiness), tapi jadi gotcha saat switch provider.

### Problem: Billing error / API key rejected

**Symptoms:** Log shows `returned a billing error — your API key has run out of credits or has an insufficient balance`

**Fix:**
1. Check key di `auth-profiles.json` — pastikan key yang benar (Coding Plan key dimulai `sk-cp-`)
2. Check dashboard: `https://platform.minimax.io/user-center/payment/coding-plan`
3. Pastikan key SAMA persis di semua agent auth-profiles (copy-paste, jangan ketik manual)

### Problem: Rate limited (HTTP 429)

**Symptoms:** `⚠️ API rate limit reached. Please try again later.`

**Cause:** Coding Plan punya 5-hour rolling window. Terlalu banyak request dalam waktu singkat.

**Fix:** Tunggu beberapa menit. OpenClaw auto-fallback ke model berikutnya di chain. Check usage di dashboard.

### Problem: Gateway not picking up config changes

**Fix:**
```bash
# Force restart
pkill -f openclaw-gateway && sleep 5

# Verify new config loaded
tail -20 ~/.openclaw/logs/gateway.log | grep -i "reload\|minimax\|model"
```

---

## Verification Commands

```bash
# Test MiniMax API directly (curl)
curl -s https://api.minimax.io/v1/chat/completions \
  -H "Authorization: Bearer sk-cp-YOUR_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-M2.5","messages":[{"role":"user","content":"say hi"}],"max_tokens":10}' | python3 -m json.tool

# Test via OpenClaw CLI
openclaw agent --agent iris --message "kamu pakai model apa sekarang?" --json

# Check which model agent is actually using
grep "agent model" ~/.openclaw/logs/gateway.log | tail -5

# Check for errors
grep -i "minimax\|billing\|rate.limit" ~/.openclaw/logs/gateway.err.log | tail -10

# Check Coding Plan usage
# → https://platform.minimax.io/user-center/payment/coding-plan
```

---

## Accurate Dashboard (Metis) Config

Metis di accurate-dashboard juga pakai MiniMax tapi via **OpenAI-compatible** endpoint (bukan Anthropic):

| File | Value |
|------|-------|
| `app/api/metis/chat/route.ts` | `createOpenAI({ baseURL: "https://api.minimax.io/v1" })` |
| `lib/metis/config.ts` | Model list: `MiniMax-M2.5`, `MiniMax-M2.5-highspeed` |
| `.env.local` + Vercel env | `MINIMAX_API_KEY=sk-cp-...` |
| Deploy | `vercel deploy --prod --token TOKEN --yes` |

---

## History

| Date | Event |
|------|-------|
| 2026-03-02 | Switch ALL agents from OpenRouter/Gemini → MiniMax M2.5 |
| 2026-03-02 | Fixed Iris stuck on Gemini (session cache clearing) |
| 2026-03-02 | Fixed `<think>` tag rendering di accurate-dashboard |
| 2026-03-02 | All 10 agents verified running MiniMax M2.5 |
