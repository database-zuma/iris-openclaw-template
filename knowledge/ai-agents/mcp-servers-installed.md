# MCP Servers Installed on Mac Mini

> Installed: 2026-02-18 | Host: database-zuma Mac mini (arm64, macOS Darwin 24.6.0)
> Node: v25.6.0 | npm: 11.8.0 | uv: 0.10.2

---

## ✅ Installation Summary

| MCP Server | Package | Binary | Status | Auth Required? |
|---|---|---|---|---|
| shadcn/ui MCP | `@jpisnice/shadcn-ui-mcp-server` | `/Users/database-zuma/homebrew/bin/shadcn-mcp` | ✅ INSTALLED | Optional (GitHub token) |
| Context7 | `@upstash/context7-mcp` | `/Users/database-zuma/homebrew/bin/context7-mcp` | ✅ INSTALLED | ⚠️ API key needed |
| Figma MCP | `figma-developer-mcp` | `/Users/database-zuma/homebrew/bin/figma-developer-mcp` | ✅ INSTALLED | ⚠️ Figma API key needed |
| NotebookLM MCP | `notebooklm-mcp-cli` v0.3.3 | `~/.local/bin/notebooklm-mcp` | ✅ INSTALLED | ⚠️ Google auth needed (`nlm login`) |
| Obsidian MCP | `@mauricio.wolff/mcp-obsidian` | `/Users/database-zuma/homebrew/bin/mcp-obsidian` | ✅ INSTALLED | No auth needed |

---

## 1. shadcn/ui MCP Server ✅

**Repo:** https://github.com/Jpisnice/shadcn-ui-mcp-server  
**Package:** `@jpisnice/shadcn-ui-mcp-server` (npm global)  
**Binary:** `/Users/database-zuma/homebrew/bin/shadcn-mcp`  
**Stars:** 2.7k+ | Framework support: React, Svelte, Vue, React Native

### What it does
Gives AI assistants full access to shadcn/ui v4 component source code, demos, blocks, metadata, and framework implementations.

### Auth / API Keys
- **No API key required** to run
- Optional: GitHub Personal Access Token (60 req/hr without vs 5000/hr with)
- Get token: https://github.com/settings/tokens (no scopes needed)

### Run / Verify
```bash
# Run with no auth (60 req/hr)
shadcn-mcp

# Run with GitHub token (recommended)
shadcn-mcp --github-api-key ghp_YOUR_TOKEN_HERE

# Switch framework
shadcn-mcp --framework svelte
shadcn-mcp --framework vue
shadcn-mcp --framework react-native
```

### MCP Config (Claude Code / OpenClaw)
```json
{
  "mcpServers": {
    "shadcn-ui": {
      "command": "/Users/database-zuma/homebrew/bin/shadcn-mcp",
      "args": ["--github-api-key", "YOUR_GITHUB_TOKEN"]
    }
  }
}
```

Or with npx:
```json
{
  "mcpServers": {
    "shadcn-ui": {
      "command": "/Users/database-zuma/homebrew/bin/npx",
      "args": ["-y", "@jpisnice/shadcn-ui-mcp-server", "--github-api-key", "YOUR_GITHUB_TOKEN"]
    }
  }
}
```

### Claude Code CLI
```bash
claude mcp add shadcn -- /Users/database-zuma/homebrew/bin/shadcn-mcp --github-api-key YOUR_TOKEN
```

---

## 2. Context7 MCP ✅

**Repo:** https://github.com/upstash/context7  
**Package:** `@upstash/context7-mcp` (npm global)  
**Binary:** `/Users/database-zuma/homebrew/bin/context7-mcp`  
**Stars:** Very popular | By Upstash

### What it does
Pulls up-to-date, version-specific documentation and code examples straight from the source for any library — places them directly into your LLM's context. Add `use context7` to prompts.

### Auth / API Keys
- **API key required** from https://context7.com
- Get free API key: `npx ctx7 setup` (OAuth flow)
- Or manually: sign up at https://context7.com → Settings → API Keys

### Setup API Key
```bash
export PATH="/Users/database-zuma/homebrew/bin:$PATH"
npx ctx7 setup --claude  # auto-configures for Claude Code
```

### MCP Config (with API key)
```json
{
  "mcpServers": {
    "context7": {
      "command": "/Users/database-zuma/homebrew/bin/context7-mcp",
      "args": ["--api-key", "YOUR_CONTEXT7_API_KEY"]
    }
  }
}
```

Or use the **remote HTTP endpoint** (no binary needed):
```json
{
  "mcpServers": {
    "context7": {
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

### Claude Code CLI
```bash
claude mcp add --scope user context7 -- /Users/database-zuma/homebrew/bin/context7-mcp --api-key YOUR_API_KEY
# Or remote:
claude mcp add --scope user --header "CONTEXT7_API_KEY: YOUR_API_KEY" --transport http context7 https://mcp.context7.com/mcp
```

### Usage tip
Add a rule to CLAUDE.md or agent config:
```
Always use Context7 MCP when I need library/API documentation, code generation, setup or configuration steps.
```

---

## 3. Figma MCP (Framelink) ✅

**Repo:** https://github.com/GLips/Figma-Context-MCP  
**Package:** `figma-developer-mcp` (npm global)  
**Binary:** `/Users/database-zuma/homebrew/bin/figma-developer-mcp`  
**Also known as:** Framelink MCP for Figma

### What it does
Gives AI coding agents (Claude, Cursor) access to Figma file layout data. Paste a Figma link → AI implements the design accurately.

### Auth / API Keys
- **Figma Personal Access Token REQUIRED**
- Get it: https://www.figma.com/settings → Security → Personal Access Tokens
- Token needs read access to files

### MCP Config
```json
{
  "mcpServers": {
    "figma": {
      "command": "/Users/database-zuma/homebrew/bin/figma-developer-mcp",
      "args": ["--figma-api-key=YOUR_FIGMA_TOKEN", "--stdio"]
    }
  }
}
```

Or via environment variable:
```json
{
  "mcpServers": {
    "figma": {
      "command": "/Users/database-zuma/homebrew/bin/figma-developer-mcp",
      "args": ["--stdio"],
      "env": {
        "FIGMA_API_KEY": "YOUR_FIGMA_TOKEN"
      }
    }
  }
}
```

### Claude Code CLI
```bash
claude mcp add figma -- /Users/database-zuma/homebrew/bin/figma-developer-mcp --figma-api-key=YOUR_FIGMA_TOKEN --stdio
```

### Usage
1. Open Cursor/Claude with Figma MCP enabled
2. Paste a Figma file/frame URL in chat
3. Ask AI to implement the design → it fetches layout metadata automatically

---

## 4. NotebookLM MCP ✅

**Repo:** https://github.com/jacob-bd/notebooklm-mcp-cli  
**Package:** `notebooklm-mcp-cli` v0.3.3 (PyPI via uv)  
**Binaries:** 
- `~/.local/bin/notebooklm-mcp` (MCP server)  
- `~/.local/bin/nlm` (CLI tool)  
**Full path:** `/Users/database-zuma/.local/share/uv/tools/notebooklm-mcp-cli/bin/notebooklm-mcp`

### What it does
Programmatic access to Google NotebookLM — create notebooks, add sources (URLs, text, YouTube, Drive), query with AI chat, generate audio overviews, download artifacts, and more. 29 MCP tools total.

### Auth / API Keys
- **Google account authentication required** (uses internal NotebookLM API + browser cookies)
- Uses cookie extraction — no official API
- Cookies expire every 2-4 weeks (auto-refresh if Chrome profile saved)

### Authentication Setup (REQUIRED before use)
```bash
export PATH="$HOME/.local/bin:$PATH"

# Login via Chrome (auto-extracts cookies)
nlm login

# Check auth status
nlm login --check

# Using OpenClaw-managed browser (CDP)
nlm login --provider openclaw --cdp-url http://127.0.0.1:18800

# Check health
nlm doctor
```

### Auto-configure for Claude Code
```bash
nlm setup add claude-code
```

### Manual MCP Config
```json
{
  "mcpServers": {
    "notebooklm-mcp": {
      "command": "/Users/database-zuma/.local/bin/notebooklm-mcp"
    }
  }
}
```

Or via uvx (no install needed):
```json
{
  "mcpServers": {
    "notebooklm-mcp": {
      "command": "uvx",
      "args": ["--from", "notebooklm-mcp-cli", "notebooklm-mcp"]
    }
  }
}
```

### Claude Code CLI
```bash
claude mcp add --scope user notebooklm-mcp /Users/database-zuma/.local/bin/notebooklm-mcp
```

### Install OpenClaw Skill (optional)
```bash
nlm skill install openclaw
```

### ⚠️ Limitations
- Rate limits: ~50 queries/day (free tier)
- Unofficial API — may break if Google changes NotebookLM internals
- Cookies expire every few weeks, need to re-run `nlm login`

---

## 5. Obsidian MCP (mcp-obsidian) ✅

**Repo:** https://github.com/bitbonsai/mcp-obsidian  
**Package:** `@mauricio.wolff/mcp-obsidian` (npm global)  
**Binary:** `/Users/database-zuma/homebrew/bin/mcp-obsidian`  
**Stars:** 496+ | By bitbonsai (Mauricio Wolff) | v0.7.5

### What it does
Universal AI bridge for Obsidian vaults. Read/write/search notes, manage tags, frontmatter, batch operations. Works directly on vault files — **no Obsidian app required**.

### Auth / API Keys
- **No auth required** — runs locally on vault directory

### Vault Location
`~/.openclaw/obsidian-vault/` — Folders: Daily/, Projects/, Templates/, Attachments/

### Run / Verify
```bash
mcp-obsidian /Users/database-zuma/.openclaw/obsidian-vault
```

### mcporter Config (OpenClaw)
Already configured via `mcporter config add`:
```bash
mcporter list obsidian                              # Check health
mcporter call obsidian.list_directory               # List vault
mcporter call obsidian.read_note path=Welcome.md    # Read note
mcporter call obsidian.write_note path=test.md content="Hello"  # Write
mcporter call obsidian.search_notes query="keyword" # Search
```

### OpenCode Config
Already in `~/.config/opencode/opencode.json`:
```json
{
  "obsidian": {
    "type": "local",
    "command": [
      "/Users/database-zuma/homebrew/bin/mcp-obsidian",
      "/Users/database-zuma/.openclaw/obsidian-vault"
    ]
  }
}
```

### Tools (13 total)
read_note, write_note, patch_note, list_directory, delete_note, search_notes, move_note, read_multiple_notes, update_frontmatter, get_notes_info, get_frontmatter, manage_tags, get_vault_stats

---

## OpenClaw / Claude Code MCP Config (All Servers)

Combined config block for `~/.claude/mcp.json` or equivalent OpenClaw config:

```json
{
  "mcpServers": {
    "shadcn-ui": {
      "command": "/Users/database-zuma/homebrew/bin/shadcn-mcp",
      "args": ["--github-api-key", "REPLACE_WITH_GITHUB_TOKEN"]
    },
    "context7": {
      "command": "/Users/database-zuma/homebrew/bin/context7-mcp",
      "args": ["--api-key", "REPLACE_WITH_CONTEXT7_API_KEY"]
    },
    "figma": {
      "command": "/Users/database-zuma/homebrew/bin/figma-developer-mcp",
      "args": ["--figma-api-key=REPLACE_WITH_FIGMA_TOKEN", "--stdio"]
    },
    "notebooklm-mcp": {
      "command": "/Users/database-zuma/.local/bin/notebooklm-mcp"
    },
    "obsidian": {
      "command": "/Users/database-zuma/homebrew/bin/mcp-obsidian",
      "args": ["/Users/database-zuma/.openclaw/obsidian-vault"]
    }
  }
}
```

> **Note:** `REPLACE_WITH_*` placeholders must be filled in before use.  
> NotebookLM also requires running `nlm login` once to authenticate.

---

## Pending Setup Actions (Manual Steps Required)

| Server | Action Needed | Where |
|---|---|---|
| **shadcn/ui** | Get GitHub token (optional, for 5000 req/hr) | https://github.com/settings/tokens |
| **Context7** | Get API key (required) | `npx ctx7 setup --claude` or https://context7.com |
| **Figma** | Get Personal Access Token (required) | https://www.figma.com/settings → Security |
| **NotebookLM** | Run `nlm login` (required, opens Chrome for Google auth) | `~/.local/bin/nlm login` |

---

## Quick Reinstall / Upgrade Commands

```bash
export PATH="/Users/database-zuma/homebrew/bin:/Users/database-zuma/homebrew/sbin:$HOME/.local/bin:$PATH"

# shadcn
npm install -g @jpisnice/shadcn-ui-mcp-server

# context7  
npm install -g @upstash/context7-mcp

# figma
npm install -g figma-developer-mcp

# notebooklm
uv tool upgrade notebooklm-mcp-cli
# or force reinstall:
uv tool install --force notebooklm-mcp-cli

# obsidian
npm install -g @mauricio.wolff/mcp-obsidian
```
