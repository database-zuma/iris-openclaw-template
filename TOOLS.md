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

- home-server → ${PGHOST} (reference from .env)
- work-server → user@example.com

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

### Credentials

All credentials stored in `.env` — **NEVER** commit/push this file.
Load with `source .env` or use python-dotenv.

### SSH

- my-server → ${PGHOST} (example: reference .env variables)

## Agent Communication (if using multi-agent setup)

### Communication Methods

**1. Persistent TUI:**
```bash
ssh my-agent-host
openclaw tui
```

**2. CLI One-Shot:**
```bash
ssh my-host "openclaw agent --agent [agent-id] --message 'task'"
```

### Example Agent Setup

#### Agent 1 (Coordinator)
- **Location:** `/path/to/workspace/`
- **Agent ID:** `main`
- **Role:** [Role description]
- **Use for:** [What tasks to delegate]

---

**Instructions:**
- Replace examples with your actual setup
- Reference .env variables instead of hardcoding credentials
- Keep this file private (gitignored by default in some setups)
