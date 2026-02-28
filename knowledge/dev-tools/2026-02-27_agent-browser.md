# Agent Browser — AI-Optimized Browser Automation (Comprehensive)

**Source:** https://github.com/vercel-labs/agent-browser
**Date Updated:** 2026-02-28 (originally fetched 2026-02-27)
**Author:** Vercel Labs | **License:** Apache 2.0
**Stars:** 16,518 ⭐ | **Forks:** 978 | **Commits:** 259
**Stack:** Rust CLI + Node.js daemon + Chromium (also Firefox/WebKit via Playwright)
**Installed:** ✅ v0.15.1 on Mac Mini (`/Users/database-zuma/homebrew/bin/agent-browser`) — **LATEST**

---

## Key Points

Headless browser automation CLI purpose-built for AI agents. 93% less context output than Playwright MCP (~400 chars vs 4000+), 95% first-try success rate, sub-millisecond Rust CLI parsing.

### Architecture

- **Rust CLI** → parses commands, communicates with daemon (sub-ms overhead)
- **Node.js Daemon** → manages Playwright browser instance, persists between commands
- **Browser:** Chromium default, also supports Firefox + WebKit via Playwright protocol
- **IPC:** WebSocket + JSON between CLI and daemon

### Recent Releases (Feb 2026)

| Version | Date | Highlights |
|---------|------|-----------|
| v0.15.1 | Feb 26 | `chrome://` and `chrome-extension://` URL support |
| v0.15.0 | Feb 25 | **Security hardening:** auth vault, domain allowlist, action policy, content boundaries, output limits |
| v0.14.0 | Feb 23 | `keyboard` command (raw keystrokes), `--color-scheme` dark/light, CDP reconnection fix, IPC fix |
| v0.13.0 | Feb 20 | `diff` commands (snapshot/screenshot/URL comparison), visual pixel diffs |
| v0.12.0 | Feb 19 | `--annotate` screenshots with numbered element labels for multimodal AI |

---

## Full Command Reference

### Core Interaction

```bash
agent-browser open <url>              # Navigate (aliases: goto, navigate)
agent-browser click <sel>             # Click (--new-tab to open in new tab)
agent-browser dblclick <sel>          # Double-click
agent-browser fill <sel> <text>       # Clear + fill input
agent-browser type <sel> <text>       # Type into element
agent-browser press <key>             # Press key (Enter, Tab, Control+a)
agent-browser keyboard type <text>    # Raw keystrokes at current focus (no selector)
agent-browser keyboard inserttext <t> # Insert text without key events
agent-browser keydown <key>           # Hold key down
agent-browser keyup <key>             # Release key
agent-browser hover <sel>             # Hover
agent-browser focus <sel>             # Focus element
agent-browser select <sel> <val>      # Select dropdown option
agent-browser check <sel>             # Check checkbox
agent-browser uncheck <sel>           # Uncheck checkbox
agent-browser scroll <dir> [px]       # Scroll (up/down/left/right, --selector <sel>)
agent-browser scrollintoview <sel>    # Scroll element into view
agent-browser drag <src> <tgt>        # Drag and drop
agent-browser upload <sel> <files>    # Upload files
agent-browser close                   # Close browser
```

### Observation (AI-critical)

```bash
agent-browser snapshot                # Full accessibility tree with refs
agent-browser snapshot -i             # Interactive elements only (buttons, inputs, links)
agent-browser snapshot -i -C          # + cursor-interactive (onclick divs, tabindex)
agent-browser snapshot -c             # Compact (remove empty structural elements)
agent-browser snapshot -d 3           # Limit depth
agent-browser snapshot -s "#main"     # Scope to CSS selector
agent-browser snapshot -i -c -d 5     # Combine options

agent-browser screenshot [path]       # Screenshot (saves to temp if no path)
agent-browser screenshot --full       # Full page
agent-browser screenshot --annotate   # Numbered labels on interactive elements → @eN refs
agent-browser pdf <path>              # Save as PDF

agent-browser eval <js>               # Run JavaScript (-b for base64, --stdin for piped)
```

### Get Info / Check State

```bash
agent-browser get text <sel>          # Text content
agent-browser get html <sel>          # innerHTML
agent-browser get value <sel>         # Input value
agent-browser get attr <sel> <attr>   # Attribute
agent-browser get title               # Page title
agent-browser get url                 # Current URL
agent-browser get count <sel>         # Count matches
agent-browser get box <sel>           # Bounding box
agent-browser get styles <sel>        # Computed styles

agent-browser is visible <sel>        # Visibility check
agent-browser is enabled <sel>        # Enabled check
agent-browser is checked <sel>        # Checked check
```

### Find Elements (Semantic Locators)

```bash
agent-browser find role <role> <action> [value]   # By ARIA role (--name, --exact)
agent-browser find text <text> <action>            # By text content
agent-browser find label <label> <action> [value]  # By label
agent-browser find placeholder <ph> <action> [val] # By placeholder
agent-browser find alt <text> <action>             # By alt text
agent-browser find title <text> <action>           # By title attr
agent-browser find testid <id> <action> [value]    # By data-testid
agent-browser find first <sel> <action> [value]    # First match
agent-browser find nth <n> <sel> <action> [value]  # Nth match
```

Actions: `click`, `fill`, `type`, `hover`, `focus`, `check`, `uncheck`, `text`

### Wait

```bash
agent-browser wait <selector>         # Wait for element visible
agent-browser wait <ms>               # Wait for time
agent-browser wait --text "Welcome"   # Wait for text
agent-browser wait --url "**/dash"    # Wait for URL pattern
agent-browser wait --load networkidle # Wait for load state
agent-browser wait --fn "window.ready === true"  # Wait for JS condition
```

### Navigation

```bash
agent-browser back                    # Go back
agent-browser forward                 # Go forward
agent-browser reload                  # Reload page
```

### Mouse Control

```bash
agent-browser mouse move <x> <y>      # Move mouse
agent-browser mouse down [button]     # Press (left/right/middle)
agent-browser mouse up [button]       # Release
agent-browser mouse wheel <dy> [dx]   # Scroll wheel
```

### Diff (NEW v0.13.0)

```bash
agent-browser diff snapshot                              # Current vs last snapshot
agent-browser diff snapshot --baseline before.txt        # Current vs saved file
agent-browser diff screenshot --baseline before.png      # Visual pixel diff
agent-browser diff screenshot --baseline b.png -o d.png  # Save diff image
agent-browser diff url https://v1.com https://v2.com     # Compare two URLs
agent-browser diff url <a> <b> --screenshot              # + visual diff
agent-browser diff url <a> <b> --selector "#main"        # Scope to element
```

### Tabs & Windows & Frames

```bash
agent-browser tab                     # List tabs
agent-browser tab new [url]           # New tab
agent-browser tab <n>                 # Switch to tab n
agent-browser tab close [n]           # Close tab
agent-browser window new              # New window
agent-browser frame <sel>             # Switch to iframe
agent-browser frame main              # Back to main frame
agent-browser dialog accept [text]    # Accept dialog
agent-browser dialog dismiss          # Dismiss dialog
```

### Browser Settings

```bash
agent-browser set viewport <w> <h>    # Set viewport size
agent-browser set device <name>       # Emulate device ("iPhone 14")
agent-browser set geo <lat> <lng>     # Set geolocation
agent-browser set offline [on|off]    # Toggle offline mode
agent-browser set headers <json>      # Extra HTTP headers
agent-browser set credentials <u> <p> # HTTP basic auth
agent-browser set media [dark|light]  # Emulate color scheme
```

### Cookies & Storage

```bash
agent-browser cookies                 # Get all cookies
agent-browser cookies set <n> <v>     # Set cookie
agent-browser cookies clear           # Clear cookies
agent-browser storage local           # Get all localStorage
agent-browser storage local <key>     # Get specific key
agent-browser storage local set <k> <v>  # Set value
agent-browser storage local clear     # Clear all
agent-browser storage session         # Same for sessionStorage
```

### Network Interception

```bash
agent-browser network route <url>              # Intercept requests
agent-browser network route <url> --abort      # Block requests
agent-browser network route <url> --body <json> # Mock response
agent-browser network unroute [url]            # Remove routes
agent-browser network requests                 # View tracked requests
agent-browser network requests --filter api    # Filter requests
```

### Debug & Profiling

```bash
agent-browser trace start [path]      # Start recording trace
agent-browser trace stop [path]       # Stop and save trace
agent-browser profiler start          # Start Chrome DevTools profiling
agent-browser profiler stop [path]    # Stop and save profile
agent-browser console                 # View console messages
agent-browser console --clear         # Clear console
agent-browser errors                  # View uncaught JS exceptions
agent-browser highlight <sel>         # Highlight element
```

### State Management

```bash
agent-browser state save <path>       # Save auth state
agent-browser state load <path>       # Load auth state
agent-browser state list              # List saved state files
agent-browser state show <file>       # Show state summary
agent-browser state clear [name]      # Clear states for session
agent-browser state clean --older-than <days>  # Delete old states
```

### Security (NEW v0.15.0)

```bash
# Auth vault — encrypted credential storage (LLM never sees passwords)
echo "pass" | agent-browser auth save github --url https://github.com/login --username user --password-stdin
agent-browser auth login github       # Login using saved credentials

# Flags
--content-boundaries                  # Wrap output for LLM safety
--max-output 50000                    # Prevent context flooding
--allowed-domains "example.com,*.cdn.com"  # Domain allowlist
--action-policy ./policy.json         # Gate destructive actions
--confirm-actions eval,download       # Require approval for categories
```

### Sessions & Profiles

```bash
# Isolated sessions (separate browser instances)
agent-browser --session agent1 open site-a.com
agent-browser --session agent2 open site-b.com
agent-browser session list            # List active sessions

# Persistent profiles (cookies, localStorage survive restarts)
agent-browser --profile ~/.myapp-profile open myapp.com

# Auto-save/restore session state
agent-browser --session-name twitter open twitter.com

# State encryption (AES-256-GCM)
export AGENT_BROWSER_ENCRYPTION_KEY=<64-char-hex-key>
```

### CDP Connection

```bash
agent-browser connect 9222            # Connect to Chrome debugging port
agent-browser --cdp 9222 snapshot     # Pass CDP per command
agent-browser --cdp "wss://remote-browser-service/cdp" snapshot  # Remote WebSocket
agent-browser --auto-connect snapshot  # Auto-discover running Chrome
```

### Cloud Providers

```bash
agent-browser -p browserbase open url  # Browserbase (remote infra)
agent-browser -p browseruse open url   # Browser Use (cloud)
agent-browser -p kernel open url       # Kernel (stealth mode, persistent profiles)
agent-browser -p ios --device "iPhone 16 Pro" open url  # iOS Simulator
```

### Streaming (Live Preview)

```bash
AGENT_BROWSER_STREAM_PORT=9223 agent-browser open example.com
# Connect WebSocket ws://localhost:9223 for live viewport + input injection
```

---

## Optimal AI Workflow (Ref-Based)

```bash
# 1. Navigate
agent-browser open example.com

# 2. Get interactive elements as refs
agent-browser snapshot -i --json
# Returns: {"success":true,"data":{"snapshot":"...","refs":{"e1":{"role":"heading","name":"Title"},...}}}

# 3. Interact using refs
agent-browser click @e2
agent-browser fill @e3 "test@example.com"

# 4. Re-snapshot after page changes
agent-browser snapshot -i --json
```

### Selector Priority

1. **@eN refs** (from snapshot) — deterministic, fast, AI-optimal
2. **Semantic locators** (`find role button click`) — readable, resilient
3. **CSS selectors** (`click "#submit"`) — familiar, direct
4. **Text/XPath** (`click "text=Submit"`) — fallback

---

## Who Can Use

✅ Iris (Mac Mini) — Primary
✅ All sub-agents (Metis, Daedalus, Hermes, Oracle)
✅ All nanobots (Eos, Argus, Codex)
✅ All CLIs (opencode, claude-code, kimi-cli)

## When to Use vs Alternatives

| Scenario | Tool |
|----------|------|
| Light automation, token-constrained | **agent-browser** ✅ |
| Complex multi-step with heavy context | Playwright MCP |
| One-off web fetch (no JS) | web_fetch |
| Anti-bot scraping (Cloudflare) | Scrapling |
| Screenshots for user (not AI) | Pinchtab |

## Key Env Vars

| Variable | Description |
|----------|-------------|
| `AGENT_BROWSER_SESSION` | Isolated session name |
| `AGENT_BROWSER_PROFILE` | Persistent profile directory |
| `AGENT_BROWSER_SESSION_NAME` | Auto-save/restore state |
| `AGENT_BROWSER_ENCRYPTION_KEY` | AES-256-GCM encryption for state |
| `AGENT_BROWSER_DEFAULT_TIMEOUT` | Playwright timeout in ms (default: 25000) |
| `AGENT_BROWSER_COLOR_SCHEME` | dark/light/no-preference |
| `AGENT_BROWSER_DOWNLOAD_PATH` | Default download directory |
| `AGENT_BROWSER_STREAM_PORT` | Enable viewport streaming |
| `AGENT_BROWSER_PROVIDER` | Cloud provider (browserbase/browseruse/kernel/ios) |
| `AGENT_BROWSER_ALLOWED_DOMAINS` | Domain allowlist |
| `AGENT_BROWSER_MAX_OUTPUT` | Truncate output to N chars |
| `AGENT_BROWSER_AUTO_CONNECT` | Auto-discover running Chrome |

## Installation

```bash
# Already installed globally via npm
npm install -g agent-browser  # Update
agent-browser install          # Download Chromium (if needed)

# Also available via brew (but brew version lags: 0.13.0 vs npm 0.15.1)
brew install agent-browser

# Install as Claude Code / AI coding assistant skill
npx skills add vercel-labs/agent-browser
```

## Key Takeaways

1. **Massively more capable than v0.12 era.** 50+ commands covering full browser automation, not just the 9 basic ones. Network interception, diff comparison, debug profiling, auth vault, state management.
2. **Security hardening (v0.15.0) makes it production-safe.** Auth vault keeps passwords out of LLM context, domain allowlist prevents navigation hijacking, action policies gate destructive operations.
3. **Diff commands are unique.** No other browser CLI does snapshot + pixel diff comparison out of the box. Useful for regression testing and visual QA.
4. **Sessions + profiles = multi-agent ready.** Each agent can have its own isolated browser session with persistent auth state. Perfect for Iris's sub-agent architecture.
5. **CDP mode enables controlling any browser.** Electron apps, remote debugging, WebSocket URLs — not limited to bundled Chromium.
6. **Cloud providers for serverless.** Browserbase, Browser Use, Kernel integration for when local browser isn't available.
7. **iOS Simulator support.** Real Mobile Safari testing via Appium + XCUITest. Requires Xcode.
8. **No MCP server integration.** Uses skill-based integration (`npx skills add`) instead of MCP protocol. Works with Claude Code, Codex, Cursor, Gemini CLI, etc.

---

**Tags:** #browser-automation #ai-agents #vercel-labs #rust #lightweight #token-efficiency #security #cdp #sessions #profiles #diff #network-interception #ios #cloud-browsers #agent-oriented
