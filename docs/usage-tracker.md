# Usage Tracker — Dokumentasi

Script: `~/scripts/usage_tracker.py`  
Output: `~/.openclaw/workspace/usage/usage_YYYY-MM-DD.json`

---

## Cara Pakai

```bash
# Default: usage hari ini (Asia/Jakarta), auto-save JSON
python3 ~/scripts/usage_tracker.py

# Tanggal spesifik
python3 ~/scripts/usage_tracker.py --date 2026-02-18

# 7 hari terakhir
python3 ~/scripts/usage_tracker.py --days 7

# All-time totals
python3 ~/scripts/usage_tracker.py --all

# Lihat per-agent breakdown
python3 ~/scripts/usage_tracker.py --agents

# Cek Gemini API key status
python3 ~/scripts/usage_tracker.py --gemini

# Kombinasi
python3 ~/scripts/usage_tracker.py --days 7 --agents --save
```

---

## Output

### Terminal
```
📊  Daily Usage — 2026-02-19 (Asia/Jakarta)
══════════════════════════════════════════════
  🤖  Anthropic (Claude)
     API Calls     : 530
     Input Tokens  : 1.1K
     Output Tokens : 107.6K
     Cache (r/w)   : 41.23M / 13.05M
     Total Tokens  : 54.39M
     Est. Cost     : $66.9135
     Sessions      : 7
     Models        : claude-sonnet-4-6 (346), claude-opus-4-6 (181)

  🌙  Kimi (kimi-coding)
     API Calls     : ...
     ...

  TOTAL: 582 calls | 54.39M tokens | $66.9135
```

### JSON File
Disimpan otomatis ke `~/.openclaw/workspace/usage/usage_YYYY-MM-DD.json`:
```json
{
  "date": "2026-02-19",
  "generated": "2026-02-19T05:40:57+07:00",
  "timezone": "Asia/Jakarta",
  "providers": {
    "anthropic": {
      "api_calls": 533,
      "input_tokens": 1116,
      "output_tokens": 108001,
      "cache_read_tokens": 41371023,
      "cache_write_tokens": 13051797,
      "total_tokens": 54531937,
      "cost_usd": 66.97,
      "sessions": 7,
      "models": { "claude-sonnet-4-6": 349, "claude-opus-4-6": 181 },
      "agents": { "iris": 519, "daedalus": 14 }
    },
    "kimi-coding": { ... }
  },
  "totals": {
    "api_calls": 585,
    "total_tokens": 54531937,
    "cost_usd": 66.97
  }
}
```

---

## Providers yang Di-track

| Icon | Provider | Catatan |
|------|----------|---------|
| 🤖 | `anthropic` | Claude Sonnet/Opus/Haiku — punya cost data |
| 🌙 | `kimi-coding` | Kimi k2 — free tier, cost $0 |
| 🔵 | `google` | Gemini via Google AI API |
| ✨ | `google-gemini-cli` | Gemini via CLI |
| 🔧 | `openclaw` | Internal OpenClaw (delivery-mirror dll) |
| 🔍 | `brave` | Brave Search API |

---

## Sumber Data

- **Session logs**: `~/.openclaw/agents/{agent}/sessions/*.jsonl`
- **Agents**: iris, daedalus, hermes, metis, oracle, main
- **Data diambil dari**: field `usage` di assistant messages (input/output/cacheRead/cacheWrite tokens + cost)
- **Timezone**: Asia/Jakarta (UTC+7) — semua filter tanggal pakai waktu lokal

---

## Pricing (Anthropic)

Cost diambil dari log jika tersedia. Fallback pricing per 1M tokens:

| Model | Input | Output | Cache Read | Cache Write |
|-------|-------|--------|------------|-------------|
| claude-sonnet-4-5/4-6 | $3.00 | $15.00 | $0.30 | $3.75 |
| claude-opus-4-6 | $15.00 | $75.00 | $1.50 | $18.75 |
| claude-haiku-4-5 | $0.80 | $4.00 | $0.08 | $1.00 |

> **Note**: Cost yang terlihat besar sebagian besar dari **cache write tokens** (prompt caching). Cache write lebih mahal dari input biasa, tapi cache read jauh lebih murah. Net cost sebenarnya lebih rendah dari gross yang ditampilkan karena subsequent requests pakai cache read.

---

## Tidak Ada Dependencies Eksternal

Script hanya menggunakan Python standard library — tidak perlu install package apapun.

---

## Catatan Gemini API

Gemini usage tidak tersimpan di session logs OpenClaw (Google tidak return usage stats via log format yang sama). Flag `--gemini` hanya cek apakah API key valid. Untuk melihat actual Gemini usage, cek Google AI Studio console: https://aistudio.google.com
