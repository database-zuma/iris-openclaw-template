# Automation Reports Pattern — Dual-Component Approach

**Date:** 2026-02-14 23:16 WIB
**Source:** Wayan clarification

---

## The Pattern

Each automated daily report needs **TWO components**:

1. **Script (Automation)** — Python wrapper for cron execution
2. **SKILL.md (Documentation)** — Full documentation for on-the-fly generation

---

## Why Both?

| Component | Purpose | Use Case |
|-----------|---------|----------|
| **Script** | Daily automated execution via cron | Reliable, consistent timing, Atlas monitoring, production use |
| **SKILL.md** | On-demand generation by agents | Ad-hoc queries, testing, troubleshooting, development, one-off analysis |

**Key insight:** Skill documentation allows agents to generate the report WITHOUT waiting for cron schedule. Essential for flexibility.

---

## Examples (Deployed)

### FF/FA/FS (Fill Factor/Article/Stock)
- ✅ **Script:** `/opt/openclaw/scripts/calculate_ff_fa_fs.py` (cron 03:00 WIB)
- ✅ **Skill:** `zuma-business-skills/ops/zuma-inventory-control/zuma-ff-skills/SKILL_ff_fa_fs.md`
- ✅ **Table:** `mart.ff_fa_fs_daily`

### SO L2 (Stock Opname Level 2)
- ✅ **Script:** `/opt/openclaw/scripts/calculate_so_l2.py` (cron 05:00 WIB)
- ⚠️ **Skill:** **TODO** — needs to be created retroactively
- ✅ **Table:** `mart.stock_opname_l2_daily`
- 📝 **Internal docs:** `knowledge/business-ops/2026-02-14_so-l2-stock-opname-daily.md` (not a skill)

---

## Pending Reports (4)

All must follow the dual-component pattern:

1. **Control Stock Report**
   - Script: `calculate_control_stock.py` (TBD)
   - Skill: `SKILL_control_stock.md` (TBD)
   - Table: `mart.control_stock_daily` (TBD)

2. **Planogram Report**
   - Script: `calculate_planogram.py` (TBD, may overlap with FF/FA/FS)
   - Skill: `SKILL_planogram.md` (TBD)
   - Table: `mart.planogram_daily` (TBD)

3. **RO Report (Box & Protol)**
   - Script: `calculate_ro_box_protol.py` (TBD)
   - Skill: `SKILL_ro_box_protol.md` (TBD)
   - Table: `mart.ro_box_protol_daily` (TBD)

4. **Surplus Store Report**
   - Script: `calculate_surplus_store.py` (TBD)
   - Skill: `SKILL_surplus_store.md` (TBD)
   - Table: `mart.surplus_store_daily` (TBD)

---

## Implementation Checklist (Per Report)

- [ ] Define SQL logic & queries
- [ ] Write Python script for cron automation
- [ ] Write SKILL.md documentation with:
  - Purpose & use cases
  - SQL query templates
  - Parameter documentation
  - Expected output schema
  - Example usage
  - Troubleshooting tips
- [ ] Test script locally
- [ ] Deploy script to VPS DB (`/opt/openclaw/scripts/`)
- [ ] Create cron job (stagger timing)
- [ ] Add skill to `zuma-business-skills` repo
- [ ] Sync skill to OpenClaw agents (Mac mini + VPS Atlas/Apollo)
- [ ] Configure Atlas monitoring
- [ ] Integrate into Iris daily report

---

## Skill Structure Reference

See `SKILL_ff_fa_fs.md` as template:
- Overview & purpose
- Data sources & coverage
- SQL query (full, copy-paste ready)
- Schema documentation
- Alert thresholds
- Example queries for common use cases
- Troubleshooting section

---

**Status:** Pattern documented, ready for implementation phase
**Next:** Create missing `SKILL_so_l2.md`, then develop 4 pending reports following this pattern
