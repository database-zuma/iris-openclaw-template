# ✈️ Zuma Business Cockpit — Architecture Overview

> Saved by Wayan on 2026-02-14. "I LOVE THIS FLOWCHART"

---

## Current Architecture (Phase 1-2)

```
✈️  ZUMA BUSINESS COCKPIT
═══════════════════════════════════════════════════════════════

THE COCKPIT  (Dashboard — for human eyes)
┌────────────────────────────────────────────────────────────┐
│  Sales │ Finance │ Operations │ KPIs │ FF/FA/FS │ Data     │
│  ██████████████████████████████████████████████████████████ │
│  Real-time metrics, summaries, alerts, trends              │
│  Notion dashboards (Phase 1) → Web dashboard (Phase 2)     │
└──────────────────────────────┬─────────────────────────────┘
                               │ monitors & interprets
                        ┌──────┴──────┐
THE CO-PILOT            │    IRIS     │  ← Helps humans read the cockpit
(AI assistant)          │  (Sonnet)   │     Answers questions, flags anomalies,
                        │  Mac Mini   │     recommends actions
                        └──────┬──────┘
                               │ directs
              ┌────────────────┼────────────────┐
              │                │                │
         ┌────┴────┐    ┌─────┴─────┐   ┌─────┴─────┐
THE      │  ATLAS  │    │  APOLLO   │   │  Future   │  ← Do the actual work
CABIN    │  (Ops)  │    │  (R&D)    │   │  Workers  │     ETL, reports, monitoring,
CREW     │         │    │           │   │           │     scheduled tasks
         └─────────┘    └───────────┘   └───────────┘
              VPS              VPS            VPS
           Haiku/Kimi       Haiku/Kimi     Haiku/Kimi
```

---

## Full Scale Architecture (Phase 3)

```
✈️  ZUMA BUSINESS COCKPIT — FULL CREW
═══════════════════════════════════════════════════════════════

THE COCKPIT  (Full web dashboard + Notion + WhatsApp alerts)
┌────────────────────────────────────────────────────────────┐
│  Sales │ Finance │ Ops │ KPIs │ FF/FA/FS │ Data │ Strategy │
│  ██████████████████████████████████████████████████████████ │
└──────────────────────────────┬─────────────────────────────┘
                               │
                        ┌──────┴──────┐
THE CAPTAIN             │   JARVIS    │  Opus 4.6 · Mac Mini
(Strategic brain)       │  Captain    │  Talks to CEO & leadership
                        └──────┬──────┘  Cross-domain decisions
                               │
              ┌────────────────┼────────────────┐
              │                │                │
         ┌────┴────┐    ┌─────┴─────┐   ┌─────┴─────┐
THE      │IRIS-OPS │    │ IRIS-BIZ  │   │ IRIS-ADM  │  Sonnet 4.5
CO-PILOTS│Co-Pilot │    │ Co-Pilot  │   │ Co-Pilot  │  Monitor their domain
         └────┬────┘    └─────┬─────┘   └─────┬─────┘  Orchestrate cabin crew
              │               │               │
    ┌─────────┴──┐    ┌──────┴────┐    ┌─────┴────────┐
    │ CABIN CREW │    │CABIN CREW │    │ CABIN CREW   │
    │            │    │           │    │              │
    │ Atlas      │    │ Sales-bot │    │ Notion-bot   │  Haiku / Kimi
    │ ETL-bot    │    │ KPI-bot   │    │ Report-bot   │  Cron-scheduled
    │ Stock-bot  │    │ Plano-bot │    │ Alert-bot    │  Cheap & reliable
    │ DQ-bot     │    │ Tier-bot  │    │ Calendar-bot │
    │ Backup-bot │    │ Apollo    │    │ Meeting-bot  │
    └────────────┘    └───────────┘    └──────────────┘
         VPS               VPS              Mac Mini
```

---

## Growth Path

```
Phase 1 (NOW)        →  Phase 2 (8-20 weeks)  →  Phase 3 (20+ weeks)
1 Co-Pilot               2 Co-Pilots               Captain + 3 Co-Pilots
5-8 cabin crew            10-15 cabin crew           Full cabin crew fleet
Notion cockpit            Notion + Web cockpit       Full web cockpit
$55-85/month              $120-215/month             $270-380/month
```

## Cockpit Crew Roles

| Role | Agent | Model | What They Do |
|------|-------|-------|-------------|
| **Captain** | Jarvis | Opus 4.6 | Strategic decisions, CEO conversations, cross-domain judgment |
| **Co-Pilot** | Iris (x1-3) | Sonnet 4.5 | Monitor cockpit, answer questions, orchestrate crew, flag anomalies |
| **Cabin Crew** | Atlas, Apollo, Workers | Haiku/Kimi | ETL, reports, KPIs, monitoring, scheduled tasks — the actual work |
| **Cockpit** | Dashboard | — | Human-readable display of all metrics, alerts, and trends |
