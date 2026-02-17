# HEARTBEAT.md — Task Tracker & Periodic Checks

**⚠️ Note:** This file tracks **URGENT same-day tasks** only. For full backlog (medium + long-term), see **PENDING.md**

---

## 🔴 CRITICAL RULE: Iris is ORCHESTRATOR ONLY (2026-02-17)
**Iris HARAM ngerjain task sendiri.** Semua pekerjaan → delegasi ke sub-agents:
- 🔮 **Metis** → Data/SQL/Analysis (`sessions_spawn agentId: "metis"`)
- 🪶 **Daedalus** → Code/Scripts/PPT/Build (`sessions_spawn agentId: "daedalus"`)
- 🪄 **Hermes** → Research/Web/Files (`sessions_spawn agentId: "hermes"`)
- 🏛️ **Oracle** → Strategy/Architecture (advisory, MD output only) (`sessions_spawn agentId: "oracle"`)

**Iris boleh langsung:**
- Respond to user (chat)
- Memory updates
- Heartbeat checks
- Simple file reads (<2 files, <2 sec)
- Quick status checks (1 command max)

---

## 📋 Pending Tasks (Urgent - This Week)

- [ ] **PENDING: Item Transfer 6-month backfill** — VPS PID 265877, started 17:39 WIB | pull_accurate_item_transfer.py --days 180 | estimated 2-3 jam | log: /opt/openclaw/logs/item_transfer_backfill.log | Wayan: mau lihat raw data setelah selesai
- [ ] **Upload iSeller data (2024, 2025, 2026)** — Database upload task, waiting for Wayan's download to complete

---

## 🔄 Routine Checks (rotate 2-4x daily)

- **Email:** Last check —
- **Calendar:** Next 24-48h —
- **Weather:** —

---

## 📊 Delegation Tracking

*When delegating with promise to follow-up → add here immediately*

| Task | Agent | Delegated At | Status |
|------|-------|-------------|--------|
| — | — | — | — |

---

**Instructions:**
- When delegating with promise to follow up → add to Pending Tasks AND Delegation Tracking
- Every heartbeat → check pending, poll status, deliver or escalate
- Task done → deliver result → remove from list
- Keep this file clean & current
- **NEVER do tasks yourself — always delegate to Mac Mini sub-agents**
