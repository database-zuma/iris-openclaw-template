# Pinchtab — Browser Control for AI Agents

> **Source:** https://github.com/pinchtab/pinchtab  
> **Researched:** 2026-02-18  
> **Stars:** ~510 | **Language:** Go | **License:** MIT

---

## What It Is

Pinchtab is a **standalone HTTP server** that gives AI agents full browser control via a plain REST API. It wraps Chrome/Chromium using the Chrome DevTools Protocol (CDP) and exposes an accessibility-tree-first interface — no framework lock-in, no SDK, just HTTP calls.

**Core philosophy:** Most browser-automation tools (Playwright MCP, Browser Use, OpenClaw's internal browser) are tightly coupled to their own agent framework. Pinchtab is deliberately decoupled — any agent, any language, even `curl`, can drive it.

```bash
# Read a page — 800 tokens instead of 10,000
curl localhost:9867/text?tabId=X

# Click a button by ref
curl -X POST localhost:9867/action -d '{"kind":"click","ref":"e5"}'
```

---

## How It Works

### Architecture

```
┌─────────────┐   HTTP :9867    ┌──────────────┐          ┌─────────┐
│  Any Agent  │ ─────────────►  │  Pinchtab    │ ─ CDP ─► │ Chrome  │
│ (OpenClaw,  │  snapshot, act, │              │          │         │
│  curl,      │  navigate, eval │  stealth +   │          │  tabs   │
│  scripts)   │                 │  sessions +  │          │         │
│             │                 │  a11y tree   │          │         │
└─────────────┘                 └──────────────┘          └─────────┘
```

1. **Pinchtab starts** → launches its own Chrome instance (headless or headed)
2. **Agent sends HTTP requests** → Pinchtab translates to CDP commands
3. **Responses** return accessibility trees, page text, or action confirmations
4. **Refs** (`e0`, `e1`, `e5`...) are stable element IDs assigned per snapshot, used for clicks/fills

### Key Mechanism: Accessibility Tree (Not Screenshots)
Pinchtab reads the browser's **accessibility tree** — structured semantic data — instead of taking screenshots. This is dramatically more token-efficient:

| Method | ~Tokens |
|--------|---------|
| Full a11y snapshot | ~10,500 |
| Interactive-only filter | ~3,600 |
| `/text` extraction | ~800 |
| Screenshot (vision model) | ~2,000 |

For a 50-page monitoring task: screenshots cost ~$0.30, Pinchtab `/text` costs ~$0.01.

---

## Full API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/tabs` | List open tabs |
| `GET` | `/snapshot` | Accessibility tree (primary interface) |
| `GET` | `/screenshot` | JPEG screenshot |
| `GET` | `/text` | Readable page text (readability or raw innerText) |
| `POST` | `/navigate` | Navigate to URL |
| `POST` | `/action` | click, type, fill, press, focus, hover, select, scroll |
| `POST` | `/evaluate` | Execute arbitrary JavaScript |
| `POST` | `/tab` | Open/close tabs |
| `POST` | `/tab/lock` | Lock tab for exclusive agent access |
| `POST` | `/tab/unlock` | Release tab lock |
| `POST` | `/cookies` | Inject session cookies (headless login) |

### Useful Snapshot Query Params
- `?filter=interactive` — buttons/links/inputs only (~75% fewer tokens)
- `?format=text` — indented plain text (~40-60% fewer tokens than JSON)
- `?format=compact` — one-line-per-node (56-64% fewer tokens than JSON)
- `?diff=true` — only changes since last snapshot
- `?selector=CSS` — scope to a CSS subtree
- `?maxTokens=N` — truncate to ~N tokens

---

## Setup Requirements

### Runtime
- **Google Chrome** or Chromium must be installed
- **Go 1.25+** (if building from source)

### Install Options

```bash
# Docker (easiest — no Go needed)
docker run -d -p 9867:9867 --security-opt seccomp=unconfined pinchtab/pinchtab

# From source
go install github.com/pinchtab/pinchtab@latest

# Clone and build
git clone https://github.com/pinchtab/pinchtab.git && cd pinchtab
go build -o pinchtab .
./pinchtab
```

### Run Modes
```bash
# Headless (recommended for automation)
BRIDGE_HEADLESS=true ./pinchtab

# Headed (default — Chrome window visible, good for debugging)
./pinchtab
```

### Key Configuration (env vars)
| Variable | Default | Notes |
|----------|---------|-------|
| `BRIDGE_PORT` | `9867` | HTTP server port |
| `BRIDGE_TOKEN` | *(none)* | **Set this!** Bearer auth token |
| `BRIDGE_HEADLESS` | `false` | Headless mode |
| `BRIDGE_PROFILE` | `~/.pinchtab/chrome-profile` | Chrome profile dir |
| `BRIDGE_STEALTH` | `light` | `light` or `full` (canvas/WebGL spoofing) |
| `BRIDGE_BLOCK_IMAGES` | `false` | Skip image downloads |
| `BRIDGE_NO_ANIMATIONS` | `false` | Freeze CSS animations |
| `CDP_URL` | *(none)* | Connect to existing Chrome instead of launching |
| `CHROME_BINARY` | *(auto)* | Custom Chrome path |

### Session / Login
- Uses persistent Chrome profile at `~/.pinchtab/chrome-profile/`
- **Headed mode**: log in manually via the Chrome window; cookies persist
- **Headless mode**: copy an existing Chrome profile or use `POST /cookies`

---

## Features Summary

- 🌲 **Accessibility-first** — stable element refs (`e0`, `e1`...) for reliable interaction
- 🎯 **Smart filters** — interactive-only mode cuts tokens by ~75%
- 🕵️ **Stealth mode** — patches `navigator.webdriver`, spoofs UA, hides automation flags
- 💾 **Session persistence** — cookies, auth, and tabs survive restarts
- 🔄 **Smart diff** — only return what changed since last snapshot
- 📝 **Text extraction** — readability mode strips nav/ads automatically
- ⚡ **JS escape hatch** — `POST /evaluate` for anything the API doesn't cover
- 📸 **Screenshots** — JPEG with quality control for visual verification
- 🚫 **Media blocking** — skip images/fonts/CSS/video for faster, leaner browsing
- 🔒 **Tab locking** — exclusive access per agent for multi-agent setups

---

## Pros

| ✅ | Detail |
|----|--------|
| **Framework-agnostic** | Pure HTTP — works with any LLM, any agent, any language |
| **Token-efficient** | `/text` mode is 5-13x cheaper than screenshots; 13x vs full snapshots |
| **Self-contained** | Single 12MB Go binary; launches its own Chrome |
| **Zero config** | Works out of the box; Docker image available |
| **Stealth mode** | Bypasses bot detection (navigator.webdriver patching, UA spoofing) |
| **Persistent sessions** | Log in once, stays logged in across restarts |
| **100+ tests** | Full test suite runs against headless mode |
| **OpenClaw integration** | Has an official OpenClaw skill for agent-driven setup |
| **MIT license** | Open source, commercial use OK |
| **Active** | Updated very recently (within hours of research) |

---

## Cons / Limitations

| ⚠️ | Detail |
|----|--------|
| **Headed mode is experimental** | Not fully tested; window management not handled |
| **Requires Chrome** | Not truly self-contained if Chrome isn't installed (Docker image handles this) |
| **No auth by default** | `BRIDGE_TOKEN` must be set manually — easy to forget in dev |
| **Binds all interfaces** | Exposed on 0.0.0.0 by default; needs firewall on shared networks |
| **Security surface** | Full real-browser access with your real sessions — agents can act as you |
| **Go 1.25+ required** | Very new Go version for source builds |
| **No built-in multi-agent coordination** | Tab locking helps, but no higher-level agent routing |
| **Profile sharing limitation** | Two Chrome instances can't share the same profile simultaneously |

---

## Security Notes (Important)

> "Think of Pinchtab like giving someone your unlocked laptop."

- Sessions (cookies, tokens) persist in `~/.pinchtab/chrome-profile/` — treat as sensitive
- **Always set `BRIDGE_TOKEN`** in any non-localhost environment
- Use a firewall or reverse proxy on shared networks
- Test with throwaway accounts before connecting to critical accounts
- All processing is local — no data leaves your machine via Pinchtab itself

---

## Relevance to Zuma / OpenClaw

- Pinchtab has **first-class OpenClaw integration** and is explicitly built to complement it
- Has an official [OpenClaw skill](https://github.com/pinchtab/pinchtab/blob/main/skill/pinchtab/SKILL.md) — agents can self-install and configure it
- Could serve as a cheaper/stealthier browser backend for Iris or other agents
- Particularly useful for read-heavy web tasks (monitoring, scraping) at ~1/13th the token cost of screenshots

---

## Built With

| Library | Role |
|---------|------|
| [chromedp](https://github.com/chromedp/chromedp) | CDP driver for Go (MIT) |
| [cdproto](https://github.com/chromedp/cdproto) | Generated CDP types (MIT) |
| [gobwas/ws](https://github.com/gobwas/ws) | Low-level WebSocket (MIT) |
| [go-json-experiment/json](https://github.com/go-json-experiment/json) | JSON v2 (BSD-3-Clause) |

Everything else is Go standard library.
