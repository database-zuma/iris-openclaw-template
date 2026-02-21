# Memory Archive — Historical Reference

Moved from MEMORY.md on 2026-02-21 to reduce system prompt size.
Iris can read this file when needed, but it's NOT injected into every session.

---

## ✅ gog CLI Setup (DONE 2026-02-20)
- Status: Authenticated ✅ (drive + sheets) for `harveywayan@gmail.com`
- Troubleshooting: See TOOLS.md § gog OAuth Troubleshooting
- Key lesson: Unlock keychain + `--manual` flag + state must match

## ⚙️ Gateway Pairing Fix (2026-02-20)
- Issue: Message tool failed "pairing required" → fallback to GDrive
- Root Cause: Device 39c9fcb8 paired without `operator.read` + `operator.write` scopes
- Fix: Device rotation with all 5 scopes → token regen → gateway restart
- Prevention: Always approve ALL 5 scopes when pairing
- Reference: `knowledge/dev-tools/2026-02-20_gateway-pairing-fix.md`

## ⚙️ Heartbeat Disable (2026-02-20)
- Correct: `"heartbeat": { "every": "0m", "ackMaxChars": 2000 }`
- Wrong: `"heartbeat": { "enabled": false }`
- Only Wayan can edit openclaw.json

## Merchant Statement Mandiri (Processing Rule)
- Source: CSV (often inside password-protected ZIP)
- Logic: Skip first 5 rows (metadata headers), comma delimiter
- Output: Excel (.xlsx) + Cleaned CSV → GDrive upload → share link
- Trigger: "Tolong rapihin file ini kayak kemarin" + Password

## YouTube/Music
Wayan's music: Denny Caknan, Sabrina Carpenter, Bad Bunny.
User requests lagu → langsung puter (openclaw browser, no relay).

## Reference Docs
- Web scraping troubleshooting → `docs/web-scraping-tips.md`
- Known bugs & fixes → `docs/known-bugs.md`
- KPI Jan-Feb 2026 → `memory/2026-02-kpi.md`
