# Agent Browser — AI-Optimized Browser Automation

**Source:** GitHub Repository
**Date Fetched:** 2026-02-27
**Link:** https://github.com/vercel-labs/agent-browser
**Author:** Vercel Labs
**License:** Apache 2.0 | **Stack:** Rust CLI + Node.js daemon
**Installed:** ✅ v0.15.1 on Mac Mini (`/Users/database-zuma/homebrew/bin/agent-browser`)
**Chromium:** Pre-installed & ready

---

## Key Points

**Apa itu:** Lightweight browser automation CLI purpose-built untuk AI agents. Minimize context output (93% less vs Playwright MCP) tanpa mengorbankan reliability (95% first-try success rate).

### Problem → Solution

| Problem | Solution |
|---|---|
| Playwright MCP output 4000+ chars | agent-browser outputs ~400 chars (93% reduction) |
| High token usage per interaction | Minimal context footprint = cheaper agent runs |
| Retry loops common | 95% first-try success = fewer roundtrips |
| Slow startup | Rust-based CLI = fast invocation |
| Heavy browser overhead | Lightweight daemon architecture |
| Complex API | Simple, focused command set |

### Core Commands

```bash
agent-browser open <url>           # Open URL in browser
agent-browser snapshot -i          # Take snapshot + return as JSON
agent-browser click @ref           # Click element by AI ref
agent-browser fill @ref "text"     # Fill input field
agent-browser screenshot           # Full page screenshot
agent-browser exec <js>            # Execute JavaScript
agent-browser type "text"          # Type text sequentially
agent-browser press <key>          # Press keyboard key (e.g., Enter)
agent-browser wait <selector>      # Wait for element existence
```

### Performance Metrics

- **Context reduction:** 93% vs Playwright MCP (400 vs 4000+ chars per interaction)
- **First-try success:** 95% (fewer retries needed)
- **CLI startup:** Fast (Rust binary)
- **Output format:** JSON refs (compatible with AI model parsing)

### Architecture

- **Frontend:** Rust CLI (`agent-browser` binary)
- **Backend:** Node.js WebSocket daemon (persistent browser session)
- **Browser:** Chromium
- **IPC:** WebSocket + JSON protocol (lightweight, no overhead)

---

## Who Can Use

✅ Iris (Mac Mini) — Primary  
✅ All sub-agents (Metis, Daedalus, Hermes, Oracle)  
✅ All nanobots (Eos, Argus, Codex)  
✅ All CLIs (opencode, claude-code, kimi-cli)  

---

## When to Use vs Alternatives

### agent-browser BEST FOR:
- Light element interactions (click, fill, snapshot)
- Token-budget constrained scenarios
- Rapid multi-step automation (low context overhead)
- First-try success critical (95% reliability)

### Avoid when:
- Complex multi-step with heavy context needed
- Highly interactive app requiring lots of re-renders
- Use **Playwright MCP** instead for complex scenarios

### One-off web fetch?
- Use **web_fetch** tool (simpler, no browser overhead)

### Anti-bot scraping?
- Use **Scrapling** (StealthyFetcher mode)

---

## Installation & Status

```bash
# Already installed
which agent-browser
# Output: /Users/database-zuma/homebrew/bin/agent-browser

# Version check
agent-browser --version
# Output: agent-browser 0.15.1

# Test
agent-browser open https://example.com
agent-browser snapshot -i
# ✅ Works: returns JSON with page content & refs
```

---

## Key Takeaways

1. **Token efficiency:** 93% context reduction vs Playwright = cheaper runs
2. **High reliability:** 95% first-try success = fewer retries
3. **Fast:** Rust CLI = minimal startup overhead
4. **Designed for agents:** Output format optimized for AI parsing
5. **Lightweight:** Perfect for sub-agents with token/latency constraints

---

## Tags

#browser-automation #ai-agents #vercel-labs #rust #lightweight #token-efficiency #high-reliability #automation #web-scraping #agent-oriented #openai-compatible
