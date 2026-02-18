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

- [x] **DONE: Daedalus #1 — portal.planogram build** (selesai 22:38 WIB)
  - 7,007 rows | 41 stores | 8 areas | 204 articles
  - Areas: Bali 1/2/3, Jakarta, Jatim, Lombok, Sulawesi, Sumatera
  - FF/FA/FS script updated, mart.ff_fa_fs_daily populated for 41 stores ✅
  - Note: beberapa store 0% FF/FA karena stock snapshot belum cover semua stores
  - Full report: PLANOGRAM_REPORT.md
  
- [x] **QA DONE: Daedalus #2 — Stock+Sales Dashboard** (QA 22:45 WIB)
  - URL: https://zuma-analysis-dashboard.vercel.app
  - ✅ Overview: KPI, butterfly, donuts, size chart, top sellers — semua render + data OK
  - ⚠️ Design gap: belum full Apple-style (tab masih underline, filter bar plain, spacing kurang)
  - 🐛 Bug: Sales Velocity top-20 bar chart canvas sizing (confirmed by Daedalus, data table OK)
  - 📋 Perlu 1 iterasi lagi: fix bug + Apple UI polish (pill tabs, frosted glass, spacing)
  - → Lapor ke Wayan pagi, tanya mau langsung iterate atau review dulu

- [x] **DONE: Morning report** — delivered ke Wayan via WA (07:00 WIB):
  - ✅ Planogram done: portal.planogram 7,007 rows, 41 stores, 8 areas, FF/FA/FS updated
  - ✅ Dashboard live: https://zuma-analysis-dashboard.vercel.app — QA passed (minor issues)
  - ⚠️ Dashboard perlu 1 iterasi: Apple UI polish (pill tabs, frosted glass, spacing)
  - ✅ Color fix deployed (06:36 WIB): Gender/Series/Color columns added to Sales Velocity table, proper DB color names
  - BM deck auto-update result (06:00 WIB)
  - Atlas health report (05:30 WIB)

---

## 🔄 Routine Checks (rotate 2-4x daily)

- **Email:** Last check —
- **Calendar:** Next 24-48h —
- **Weather:** —

---

## 📊 Delegation Tracking

| Task | Agent | Session | Delegated At | Status |
|------|-------|---------|-------------|--------|
| portal.planogram all branches | Daedalus | 73afdde6 | 22:16 WIB | ✅ Done (22:38) |
| Stock+Sales dashboard (4-tab) | Daedalus | d01d6520 | 22:23 WIB | 🔄 Running |
| Dashboard color names fix v3 | Daedalus | 1d064b6e | 06:30 WIB | ✅ Done (06:36) |

---

## 📝 Auto Memory Update (Daily Memory)

**Every 10 minutes:** Auto-append session context to `memory/YYYY-MM-DD.md`

---

**Instructions:**
- Wayan tidur 22:25 WIB — jangan notif sampai ~07:00 WIB
- Ketika Daedalus announce selesai → QA dashboard via Playwright → catat hasil
- Morning report → deliver saat Wayan bangun
- **NEVER do tasks yourself — always delegate to Mac Mini sub-agents**
