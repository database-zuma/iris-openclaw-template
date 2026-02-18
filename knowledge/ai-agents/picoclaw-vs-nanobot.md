# PicoClaw vs Nanobot — Perbandingan untuk SPG Agent (VPS Deployment)

> **Researched:** 2026-02-19  
> **Sources:**  
> - PicoClaw: https://github.com/sipeed/picoclaw (+ picoclaw.md internal notes)  
> - Nanobot: https://github.com/HKUDS/nanobot  
> - Artikel: https://www.scriptbyai.com/nanobot-ai-assistant/  
> **Context:** Zuma Indonesia VPS (8GB RAM, 2 CPU cores) — SPG agent untuk follow-up stock opname & product knowledge Q&A via WhatsApp

---

## What Is Each?

### 🐾 PicoClaw
Ultra-lightweight AI assistant framework dalam **Go**, dibuat oleh Sipeed (perusahaan hardware China). Lahir 9 Feb 2026, viral dengan 12K stars di minggu pertama. Terinspirasi dari Nanobot & OpenClaw — didesain untuk hardware $10 RISC-V/ARM, target RAM <10MB.

### 🐈 Nanobot (HKUDS)
Ultra-lightweight AI assistant dalam **Python**, dibuat oleh Data Intelligence Lab, University of Hong Kong. Lahir 2 Feb 2026, versi v0.1.4 (per 17 Feb 2026). "99% lebih kecil dari OpenClaw/Clawdbot" dengan ~4,000 baris kode Python. Nanobot adalah inspirasi dari PicoClaw.

---

## Key Points

### 🏆 Kriteria Paling Krusial untuk SPG WhatsApp Use Case

| Kriteria | PicoClaw | Nanobot |
|----------|----------|---------|
| **WhatsApp support** | ❌ **TIDAK** (listed di config tapi `enabled: false`) | ✅ **YA** (QR scan, butuh Node.js ≥18) |
| **Claude/GPT support** | ⚠️ "To be tested" | ✅ **Fully supported** (OpenRouter, Claude, GPT, dll) |
| **Ease of customization** | ⚠️ Go binary — harder to modify | ✅ Python — mudah extend custom skills |
| **VPS 8GB RAM friendly** | ✅ <10–20MB (overkill efficient) | ✅ ~50–200MB (sangat nyaman di 8GB) |

> **TL;DR: WhatsApp adalah kebutuhan utama SPG agent. Nanobot support WhatsApp natively. PicoClaw tidak. Game over.**

---

## Technical Details

### Resource Usage

| Metric | PicoClaw | Nanobot |
|--------|----------|---------|
| **Language** | Go | Python |
| **RAM (idle)** | <10MB (10–20MB dengan PR terbaru) | ~50–150MB (Python baseline) |
| **RAM (di VPS 8GB)** | ✅ Sangat ringan — bisa run puluhan instance | ✅ Masih sangat ringan — sisa 7.8GB untuk service lain |
| **Boot time** | <1 detik (bahkan di 0.6GHz) | Beberapa detik (Python startup) |
| **Codebase size** | ~1 Go binary | ~4,000 baris Python |
| **Dependencies** | None (single binary) | Python + pip packages + Node.js (untuk WhatsApp) |
| **CPU usage** | Minimal (Go goroutines efficient) | Low (mostly idle, spike saat LLM call) |

### Chat Channels Supported

| Channel | PicoClaw | Nanobot |
|---------|----------|---------|
| **WhatsApp** | ❌ Disabled | ✅ QR code scan |
| **Telegram** | ✅ | ✅ |
| **Discord** | ✅ | ✅ |
| **QQ** | ✅ | ✅ |
| **DingTalk** | ✅ | ✅ |
| **Feishu/Lark** | ✅ | ✅ |
| **LINE** | ✅ | ❌ |
| **Slack** | ❌ | ✅ |
| **Email** | ❌ | ✅ |

### LLM Provider Support

| Provider | PicoClaw | Nanobot |
|----------|----------|---------|
| **Anthropic Claude** | ⚠️ "To be tested" | ✅ Fully supported |
| **OpenAI GPT** | ⚠️ "To be tested" | ✅ Fully supported |
| **OpenRouter** | ⚠️ "To be tested" | ✅ Recommended (global) |
| **DeepSeek** | ⚠️ "To be tested" | ✅ Supported |
| **Google Gemini** | ✅ Tested | ✅ Supported |
| **Groq** | ✅ Tested + Whisper voice | ✅ Supported + Whisper voice |
| **Zhipu (GLM)** | ✅ Primary / default | ❌ Not listed |
| **vLLM (local)** | ❌ | ✅ Supported |
| **Qwen** | ❌ | ✅ Supported |

### Core Agent Features

| Feature | PicoClaw | Nanobot |
|---------|----------|---------|
| **Subagents (async)** | ✅ | ✅ |
| **Heartbeat (background tasks)** | ✅ (every 30 min) | ✅ |
| **Cron scheduling** | ✅ | ✅ |
| **Persistent memory** | ✅ (SOUL.md, MEMORY.md) | ✅ (SOUL.md, MEMORY.md, long-term + short-term) |
| **Web search** | ✅ Brave API / DuckDuckGo fallback | ✅ Brave API |
| **File ops (workspace)** | ✅ sandboxed | ✅ sandboxed |
| **Shell exec** | ✅ sandboxed | ✅ sandboxed |
| **MCP support** | ❌ | ✅ (added Feb 14, 2026) |
| **Skills/plugins** | ✅ skill.md URL | ✅ ClawHub marketplace |
| **Docker Compose** | ✅ | ✅ |
| **Voice transcription** | ✅ Groq Whisper (Telegram) | ✅ Groq Whisper (Telegram) |

### Setup & Installation

**PicoClaw:**
```bash
# Binary download
wget https://github.com/sipeed/picoclaw/releases/download/v0.1.1/picoclaw-linux-arm64
chmod +x picoclaw-linux-arm64
./picoclaw-linux-arm64 onboard

# Atau Docker Compose
git clone https://github.com/sipeed/picoclaw.git
cd picoclaw
cp config/config.example.json config/config.json
docker compose --profile gateway up -d
```

**Nanobot:**
```bash
# Simple pip install
pip install nanobot-ai
nanobot onboard

# Atau uv (recommended - faster)
uv tool install nanobot-ai
nanobot onboard

# WhatsApp setup (butuh Node.js ≥18)
nanobot channels login   # Scan QR code dengan WhatsApp
nanobot gateway          # Start gateway
```

### Config Example — Nanobot untuk WhatsApp SPG Agent

```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-sonnet-4-5",
      "workspace": "~/.nanobot/workspace"
    }
  },
  "providers": {
    "openrouter": { "apiKey": "sk-or-v1-xxx" }
  },
  "channels": {
    "whatsapp": {
      "enabled": true,
      "allowFrom": ["+628xxxxxxxxxx"]
    }
  },
  "heartbeat": {
    "enabled": true,
    "interval": 60
  }
}
```

### Workspace Layout (Keduanya Mirip OpenClaw)

```
~/.nanobot/workspace/  (atau ~/.picoclaw/workspace/)
├── SOUL.md         # Agent identity & personality (SPG persona)
├── AGENTS.md       # Behavior guidelines
├── MEMORY.md       # Long-term memory
├── HEARTBEAT.md    # Periodic tasks (daily follow-up reminders)
├── TOOLS.md        # Tool descriptions
├── skills/         # Custom skills (product knowledge base)
└── memory/         # Daily notes
```

---

## Takeaways

### 1. Untuk SPG WhatsApp Use Case → **Nanobot adalah satu-satunya pilihan**

WhatsApp adalah kanal utama SPG Indonesia. PicoClaw tidak mendukung WhatsApp sama sekali. Nanobot mendukung WhatsApp via QR code scan — ini deal-breaker yang menentukan pilihan.

### 2. VPS 8GB RAM → Kedua framework sangat cocok

Nanobot Python ~50–200MB vs PicoClaw Go ~10–20MB. Di VPS 8GB, keduanya menyisakan ampel RAM untuk service lain. Resource usage bukan constraint di hardware ini.

### 3. LLM Support → Nanobot lebih lengkap

Nanobot mendukung Claude, GPT, OpenRouter secara penuh. PicoClaw masih "to be tested" untuk Claude/GPT — risiko tinggi untuk production. SPG agent butuh LLM berkualitas untuk product knowledge Q&A yang akurat.

### 4. Kemudahan kustomisasi → Nanobot menang

Python lebih mudah dimodifikasi untuk business logic (product catalog integration, stock DB queries). Go binary PicoClaw lebih sulit di-extend tanpa recompile.

### 5. PicoClaw lebih baik jika... 

Tidak butuh WhatsApp (Telegram only), resource sangat terbatas (<256MB VPS), atau butuh deployment ke edge device (Raspberry Pi, dll). Untuk Zuma SPG use case, ini tidak relevan.

### 6. Maturity — Keduanya Masih Early Stage

- Nanobot: v0.1.4, diluncurkan 2 Feb 2026, **sangat aktif** (update hampir setiap hari)
- PicoClaw: v0.1.x, diluncurkan 9 Feb 2026, **aktif** tapi "do not deploy to production before v1.0"
- Keduanya sama-sama beta — butuh monitoring dan contingency plan

### 7. Arsitektur SPG Agent yang Direkomendasikan (Nanobot)

```
VPS 8GB RAM
├── nanobot gateway (WhatsApp channel)
│   ├── SOUL.md: "Kamu adalah Bella, SPG Zuma Indonesia..."
│   ├── MEMORY.md: Product catalog, harga, stok terkini
│   ├── HEARTBEAT.md: Daily reminder follow-up stock opname ke SPG
│   └── skills/
│       ├── stock-opname.md: Cara catat & follow-up stock
│       └── product-knowledge.md: Database produk Zuma
└── (sisa RAM: untuk DB, web server, dll)
```

---

## Perbandingan Cepat (Summary Table)

| Aspek | PicoClaw | Nanobot | Winner untuk SPG |
|-------|----------|---------|-----------------|
| **WhatsApp** | ❌ | ✅ | 🏆 **Nanobot** |
| **RAM usage** | ~10–20MB | ~50–200MB | 🏆 PicoClaw (tapi irrelevant di 8GB) |
| **Claude support** | ⚠️ untested | ✅ fully working | 🏆 **Nanobot** |
| **Setup mudah** | ✅ single binary | ✅ pip install | Seri |
| **Customizable** | ⚠️ Go (harder) | ✅ Python (easier) | 🏆 **Nanobot** |
| **MCP support** | ❌ | ✅ | 🏆 Nanobot |
| **VPS deploy** | ✅ Docker | ✅ Docker | Seri |
| **Bahasa docs** | ⚠️ Chinese-first | ✅ English-first | 🏆 Nanobot |
| **Channel variety** | ✅ Telegram+6 | ✅ WhatsApp+8 | 🏆 Nanobot (untuk WA) |
| **Stability** | ⚠️ v0.1.x beta | ⚠️ v0.1.x beta | Seri (keduanya beta) |

**REKOMENDASI FINAL: 🐈 Nanobot (HKUDS) untuk SPG WhatsApp Agent Zuma**

---

## Pros & Cons

### Nanobot untuk SPG Use Case

| | Detail |
|-|--------|
| ✅ WhatsApp native | QR scan setup, allowlist security per nomor SPG |
| ✅ Claude API ready | Product Q&A akurat dengan claude-sonnet atau claude-haiku |
| ✅ Python skills | Mudah tulis custom skill untuk product catalog, stock query |
| ✅ HEARTBEAT | Otomatis kirim reminder follow-up stock opname harian |
| ✅ Memory system | Agent ingat konteks per SPG — personalized experience |
| ✅ OpenRouter | Fallback LLM options jika budget berubah |
| ⚠️ Node.js required | WhatsApp channel butuh Node.js ≥18 di VPS |
| ⚠️ WA QR scan | Session bisa expired, butuh re-scan berkala |
| ⚠️ Beta (v0.1.4) | Masih muda — mungkin ada breaking changes |
| ❌ Python runtime | ~50MB overhead vs PicoClaw's 10MB (tidak masalah di 8GB VPS) |

### PicoClaw untuk SPG Use Case

| | Detail |
|-|--------|
| ✅ Sangat ringan | Bisa run di hardware apapun |
| ✅ Single binary | Zero dependency deploy |
| ✅ Familiar | Mirip OpenClaw workspace model |
| ❌ No WhatsApp | **Fatal untuk SPG Indonesia** |
| ❌ Claude untested | Risiko di production |
| ❌ Go binary | Susah custom tanpa recompile |
| ❌ Chinese-first | Docs kurang lengkap dalam Bahasa Inggris |

---

## Tags

`#nanobot` `#picoclaw` `#lightweight-agent` `#vps-deployment` `#whatsapp-bot` `#spg-agent` `#ai-assistant` `#python-agent` `#go-agent` `#zuma-indonesia` `#hkuds` `#sipeed` `#openclaw-alternative`
