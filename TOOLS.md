# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin
- work-vps → ssh user@your-vps-ip

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Credentials

All credentials are stored in `/path/to/your/workspace/.env` — **NEVER commit/push this file.**

Example `.env` contents:
```
GITHUB_TOKEN=ghp_your_token_here
DATABASE_URL=postgresql://user:password@host:5432/dbname
API_KEY=your_api_key_here
```

Load credentials with `source .env` (bash) or use `python-dotenv` (Python), `dotenv` (Node.js), etc.

## OpenCode (Primary Coding Tool) 🧠

**Binary:** `opencode` (install from your package manager or OpenClaw docs)
**Config:** Uses OhMyClaude Code framework

**Session Naming Convention:**
All sessions spawned by your agent should use a prefix followed by a descriptive title:
- `myagent_fix_sales_dedup` — not "fix sales dedup"
- `myagent_data_analysis` — not "data analysis"

**Why prefix matters:** Multiple agents may spawn sessions. The prefix identifies who owns what.

## SSH

Example SSH hosts (replace with your actual infrastructure):
- `my-vps` → `ssh user@your-vps-ip` (your remote server)
- `database-server` → `ssh user@db-host` (your database server)

## Agent Communication (Optional)

If you have multiple agents deployed (e.g., on VPS), document how they communicate:

**Communication Methods:**
- Persistent TUI (for ongoing conversation)
- CLI one-shot (for quick commands)
- Message queues, webhooks, etc.

**Example agents:**
- **Agent 1** — Role, location, how to reach
- **Agent 2** — Role, location, how to reach

## Data Filtering Rules (Optional)

If your agent handles business data with specific exclusion/inclusion rules, document them here.

Example:
```
### Store Queries - Universal Exclusions
When querying sales by store, AUTO-EXCLUDE:
- Stores containing "Wholesale"
- Stores containing "Warehouse"
- Test/demo accounts
```

## BluOS / Smart Home Control (Optional)

If you have smart home integrations:

```bash
# Example: BluOS speaker control
~/go/bin/blu devices
~/go/bin/blu --device speaker-name volume set 50
```

---

**Customize this file** with your actual tools, IPs, preferences, and workflows. Keep it updated as your setup evolves.
