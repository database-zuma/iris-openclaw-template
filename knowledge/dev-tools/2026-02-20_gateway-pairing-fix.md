# Gateway Pairing Issue Fix — Scope Mismatch

**Date:** 2026-02-20  
**Issue:** `gateway closed (1008): pairing required` when sending files/messages via WhatsApp  
**Root Cause:** Device paired without `operator.read` + `operator.write` scopes  
**Status:** ✅ Resolved

## Symptoms
- Agent tools (message, sessions_list) fail to connect to gateway WS
- Error: `pairing required` repeated in `/tmp/openclaw/openclaw-*.log`
- Fallback: GDrive share instead of direct WA send
- Affects: File/image delivery via `message` tool

## Root Cause
Device (`39c9fcb8...`, `gateway-client`) was paired initially without sufficient scopes:
- ✅ Had: `operator.admin`, `operator.approvals`, `operator.pairing`
- ❌ Missing: `operator.read`, `operator.write`

Agent tools need read/write scopes to connect back to gateway via WebSocket.

## Fix Steps (In Order)

### 1. Identify Scope Deficit
```bash
grep "pairing required" /tmp/openclaw/openclaw-*.log | wc -l  # Count errors
opencloud devices list  # Check device scopes
```

### 2. Check Pending Repairs
```bash
openclaw devices list --pending  # Any pending requests?
```
If pending: approve latest request to add missing scopes.

### 3. Manually Add Scopes (if openclaw CLI not cooperating)
Edit `~/.openclaw/devices/paired.json`:
```json
{
  "39c9fcb8...": {
    "scopes": [
      "operator.admin",
      "operator.approvals",
      "operator.pairing",
      "operator.read",        // ADD THIS
      "operator.write"         // ADD THIS
    ],
    "tokens": {
      "operator": {
        "scopes": [
          "operator.admin",
          "operator.approvals",
          "operator.pairing",
          "operator.read",
          "operator.write"
        ]
        // ... rest of token
      }
    }
  }
}
```

### 4. Rotate Token
```bash
openclaw devices rotate --device [DEVICE_ID] \
  --scope operator.admin \
  --scope operator.approvals \
  --scope operator.pairing \
  --scope operator.read \
  --scope operator.write
```

### 5. Verify Client-Side Auth
Check `~/.openclaw/identity/device-auth.json` — agent tools use this to connect back to gateway.  
After token rotation, this file should be updated automatically. If not, restart gateway.

### 6. Restart Gateway
```bash
openclaw gateway restart
```

## Verification
- Send test message: `message action=send channel=whatsapp target=+628983539659 message="test"`
- Should succeed without "pairing required" error
- Check logs: `tail -50 /tmp/openclaw/openclaw-*.log | grep -i "pair\|message"`

## Prevention
- When pairing new gateway-client device, ensure **all 5 scopes** are approved:
  - operator.admin (device management)
  - operator.approvals (pairing approvals)
  - operator.pairing (pairing list/approve)
  - operator.read (read WS messages, config)
  - operator.write (write messages, agent tools)
- Default pairing flow should ask for all, but manual pairing may miss scopes.

## Files Modified
- `~/.openclaw/devices/paired.json` — device scopes + token scopes
- `~/.openclaw/identity/device-auth.json` — client-side device token (auto-updated after rotation)

## Related Errors
- `gateway closed (1008): pairing required` — missing scopes
- `gateway closed (1011): internal server error` — other gateway issue
- `LocalMediaAccessError` — media path not in workspace (separate issue)

---

**Tags:** #openclaw #gateway #pairing #troubleshooting #whatsapp #device-auth
