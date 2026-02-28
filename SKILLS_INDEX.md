# SKILLS_INDEX.md — Skill Routing Table for Iris

_Baca file ini di setiap session. Gunakan untuk routing user request ke skill + agent yang tepat._
_Last updated: 2026-02-27_

---

## Cara Pakai

1. User kirim request
2. Cocokkan dengan **Trigger Keywords** di tabel bawah
3. Baca SKILL.md di path yang tertera
4. Include konten skill (atau ringkasannya) di prompt delegasi ke agent yang ditunjuk
5. Jangan lupa heartbeat + origin_phone

**PENTING:** Skill files ini BUKAN auto-discovered. Iris HARUS baca tabel ini untuk tahu skill mana yang relevan.

---

## 🔴 Planogram & RO Pipeline (Berurutan)

Pipeline penuh: **Step 0.5 → Step 1 → Step 2 → Step 3**

Setiap step punya SKILL.md sendiri. JANGAN lompat step — output step sebelumnya jadi input step berikutnya.

| Step | Skill Name | Trigger Keywords | Delegate To | Skill File Path |
|------|-----------|------------------|-------------|-----------------|
| **Prompt** | `PROMPT_new_planogram` | "bikin planogram", "planogram baru", "generate planogram" | Daedalus | `zuma-business-skills/ops/zuma-plano-ro-skills/PROMPT_new_planogram.md` |
| **0.5** | `pre-planogram-zuma` | "pre-planogram", "data table planogram", "target quantities per size" | Daedalus | `zuma-business-skills/ops/zuma-plano-ro-skills/step0.5-pre-planogram/SKILL.md` |
| **1** | `planogram-zuma` | "planogram", "layout display toko", "assign artikel ke backwall" | Daedalus | `zuma-business-skills/ops/zuma-plano-ro-skills/step1-planogram/SKILL.md` |
| **2** | `visualized-planogram-zuma` | "visualisasi planogram", "floor plan", "denah visual" | Daedalus | `zuma-business-skills/ops/zuma-plano-ro-skills/step2-visualizations/SKILL.md` |
| **3** ⭐ | `zuma-ro-surplus` **DEFAULT** | "RO request", "RO box", "replenishment order", "restock", "surplus pull", "RO protol" | Daedalus (script) / Argus (data) | `zuma-business-skills/ops/zuma-plano-ro-skills/step3-zuma-ro-surplus-skills/SKILL.md` |
| **3-alt** | `zuma-ro-box-only` _(experimental, Jatim only)_ | "RO box only", "box only experiment" | Daedalus (script) / Argus (data) | `zuma-business-skills/ops/zuma-plano-ro-skills/zuma-ro-box-only/SKILL.md` |
| **Prompt** | `ro-request-prompt` | "RO request mingguan", "generate RO", "bikin RO" | Daedalus | `zuma-business-skills/ops/zuma-plano-ro-skills/PROMPT_ro_request.md` |

### Dependency Chain (WAJIB dipahami)

```
Pre-Planogram (Step 0.5)
    ↓ output: size-level target table
Planogram (Step 1)
    ↓ output: PLANOGRAM_[Store].xlsx
Visual Planogram (Step 2)
    ↓ output: VISUAL_PLANOGRAM_[Store].xlsx + .txt
RO Request — Surplus + Restock (Step 3 DEFAULT)
    ↓ input: planogram + current stock from DB
    ↓ output: RO_Request_[Store]_[Date].xlsx (RO Protol + RO Box + Surplus + Reference)
```

### "RO Request" — Quick Decision Tree

```
User bilang "bikin RO request" →
    1. DEFAULT: Gunakan `step3-zuma-ro-surplus-skills` (Surplus + Restock flow)
       Path: zuma-business-skills/ops/zuma-plano-ro-skills/step3-zuma-ro-surplus-skills/SKILL.md
       Script: build_ro_request.py (di folder yang sama)
       Logic: Identifikasi urgent surplus → Restock (Box priority) → Surplus pull
       Scope: All branches (portal.planogram)

    2. ALTERNATIF EXPERIMENTAL (jika diminta box-only / Jatim saja):
       Gunakan `zuma-ro-box-only`
       Path: zuma-business-skills/ops/zuma-plano-ro-skills/zuma-ro-box-only/SKILL.md

    3. Dependencies yang juga harus di-load:
       - zuma-data-analyst-skill (DB connection rules)
       - zuma-sku-context (tier system, kode_mix)
       - zuma-warehouse-and-stocks (gudang, RO flow)
    4. Delegate ke Daedalus (script execution) atau Argus (data query)
    5. Output: Excel → upload GDrive → deliver link
```

---

## 📊 Data & Analysis Skills

| Skill Name | Trigger Keywords | Delegate To | Skill File Path |
|-----------|------------------|-------------|-----------------|
| `zuma-data-analyst-skill` | "query DB", "SQL", "data sales", "data stok", "cek data" | Argus / Metis | `zuma-business-skills/ops/zuma-data-analyst-skill/SKILL.md` |
| `zuma-database-assistant-skill` | "schema", "ETL", "view", "table issue", "DB maintenance" | Metis | `zuma-business-skills/ops/zuma-database-assistant-skill/SKILL.md` |
| `zuma-sku-context` | "tier", "kode mix", "assortment", "product categorization" | (dependency — load bersama skill lain) | `zuma-business-skills/ops/zuma-sku-context/SKILL.md` |
| `zuma-warehouse-and-stocks` | "gudang", "warehouse", "stok WH", "DDD", "LJBB" | (dependency — load bersama skill lain) | `zuma-business-skills/ops/zuma-warehouse-and-stocks/SKILL.md` |
| `zuma-branch` | "branch", "cabang", "toko mana", "area", "region" | (dependency — load bersama skill lain) | `zuma-business-skills/ops/zuma-branch/SKILL.md` |
| `zuma-business-metrics` | "KPI", "target", "metrics", "KRA", "performance" | Argus | `zuma-business-skills/general/zuma-business-metrics/SKILL.md` |
| `zuma-token-usage-report` | "token usage", "cost report", "LLM spending" | (auto — cross-cutting) | `zuma-business-skills/ops/zuma-token-usage-report/SKILL.md` |
| `statistical-analysis` | "analisis statistik", "rata-rata", "std dev", "outlier", "tren signifikan", "korelasi", "distribusi", "perbandingan periode" | Argus / Metis | `zuma-business-skills/general/statistical-analysis/SKILL.md` |
| `data-visualization` | "grafik", "chart", "plot", "visualisasi", "line chart", "bar chart", "heatmap", "tren visual" | Argus | `zuma-business-skills/general/data-visualization/SKILL.md` |
| `zuma-database-assistant-skill` | "schema", "ETL", "view", "table issue", "DB maintenance" | Metis | `zuma-business-skills/ops/zuma-database-assistant-skill/SKILL.md` |
| `zuma-sku-context` | "tier", "kode mix", "assortment", "product categorization" | (dependency — load bersama skill lain) | `zuma-business-skills/ops/zuma-sku-context/SKILL.md` |
| `zuma-warehouse-and-stocks` | "gudang", "warehouse", "stok WH", "DDD", "LJBB" | (dependency — load bersama skill lain) | `zuma-business-skills/ops/zuma-warehouse-and-stocks/SKILL.md` |
| `zuma-branch` | "branch", "cabang", "toko mana", "area", "region" | (dependency — load bersama skill lain) | `zuma-business-skills/ops/zuma-branch/SKILL.md` |
| `zuma-business-metrics` | "KPI", "target", "metrics", "KRA", "performance" | Argus | `zuma-business-skills/general/zuma-business-metrics/SKILL.md` |
| `zuma-token-usage-report` | "token usage", "cost report", "LLM spending" | (auto — cross-cutting) | `zuma-business-skills/ops/zuma-token-usage-report/SKILL.md` |

---

## 📦 Inventory Control Skills

| Skill Name | Trigger Keywords | Delegate To | Skill File Path |
|-----------|------------------|-------------|-----------------|
| `zuma-ff-skills` | "fill factor", "fill accuracy", "fill score", "FF", "FA", "FS", "planogram compliance" | Argus / Daedalus | `zuma-business-skills/ops/zuma-inventory-control/zuma-ff-skills/SKILL.md` |
| `stock-opname-level-2` | "stock opname", "SO level 2", "opname L2" | Daedalus | `zuma-business-skills/ops/zuma-inventory-control/stock-opname-level-2/SKILL.md` |
| `notion-metrics` | "notion", "notion metrics", "FF to notion" | Argus | `zuma-business-skills/ops/notion-metrics/SKILL.md` |

---

## 🎨 Visual & Presentation Skills

| Skill Name | Trigger Keywords | Delegate To | Skill File Path |
|-----------|------------------|-------------|-----------------|
| `eos-visual-skill` | "PPT", "deck", "slide", "presentasi" | Argus → Eos | `zuma-business-skills/general/eos-visual-skill/SKILL.md` |
| `zuma-ppt-design` | "PPT design", "template deck" | Argus → Eos | `zuma-business-skills/general/zuma-ppt-design/SKILL.md` |
| `zuma-image-gen-skill` | "generate image", "bikin gambar", "visual asset" | Daedalus (Gemini) | `zuma-business-skills/general/zuma-image-gen-skill/SKILL.md` |
| `data-storytelling-skill` | "storytelling", "narrative", "insight report", "BCG style" | Argus | `zuma-business-skills/general/data-storytelling-skill/SKILL.md` |
| `zuma-company-context` | "brand", "Zuma identity", "brand guidelines" | (dependency — load bersama visual skills) | `zuma-business-skills/general/zuma-company-context/SKILL.md` |
| `xlsx-skill` | "output excel", "file xlsx", "bikin excel", "laporan excel", "template excel", "download xlsx" | Argus / Daedalus | `zuma-business-skills/general/xlsx-skill/SKILL.md` |
| `zuma-company-context` | "brand", "Zuma identity", "brand guidelines" | (dependency — load bersama visual skills) | `zuma-business-skills/general/zuma-company-context/SKILL.md` |

---

## 🔧 Operations & Finance Skills

| Skill Name | Trigger Keywords | Delegate To | Skill File Path |
|-----------|------------------|-------------|-----------------|
| `dn-to-po` | "delivery note", "DN", "convert DN", "invoice", "PO" | Daedalus | `zuma-business-skills/ops/dn-to-po/SKILL.md` |
| `fp-rekon-stock` | "faktur pajak", "FP rekon", "register pembelian" | Daedalus | `zuma-business-skills/skills/finance/fp-rekon-stock/SKILL.md` |
| `coretax-faktur-generator` | "coretax", "faktur pajak keluaran", "generate faktur", "upload DJP", "register penjualan" | Daedalus | `zuma-business-skills/skills/finance/coretax-faktur-generator/SKILL.md` |
| `deploy-to-live` | "deploy", "push to vercel", "push to github" | Daedalus / Codex | `zuma-business-skills/general/deploy-to-live/SKILL.md` |

---

## Skill Dependencies (Quick Ref)

Beberapa skill punya dependency ke skill lain. Saat load skill utama, JUGA load dependency-nya:

| Skill Utama | Dependencies (load juga) |
|------------|--------------------------|
| `planogram-zuma` (Step 1) | `zuma-data-analyst-skill`, `zuma-sku-context`, `zuma-branch` |
| `pre-planogram-zuma` (Step 0.5) | `zuma-data-analyst-skill`, `zuma-sku-context` |
| `zuma-ro-surplus` (Step 3 DEFAULT) | `zuma-data-analyst-skill`, `zuma-sku-context`, `zuma-warehouse-and-stocks` |
| `zuma-ro-box-only` (Step 3 experimental) | `zuma-data-analyst-skill`, `zuma-sku-context`, `zuma-warehouse-and-stocks` |
| `visualized-planogram-zuma` (Step 2) | `planogram-zuma` (Step 1 output required) |
| `zuma-ff-skills` | `zuma-data-analyst-skill`, `zuma-sku-context` |
| `eos-visual-skill` | `zuma-company-context` |
| `dn-to-po` | (none) |
| `fp-rekon-stock` | (none) |
| `coretax-faktur-generator` | (none) |
| `statistical-analysis` | `zuma-data-analyst-skill` (untuk DB query) |
| `data-visualization` | `statistical-analysis` (opsional, kalau butuh stats dulu) |
| `xlsx-skill` | (none — standalone output tool) |

---

## All Skill Paths (Absolute — for file reads)

```
~/.openclaw/workspace/zuma-business-skills/
├── general/
│   ├── data-storytelling-skill/SKILL.md
│   ├── deploy-to-live/SKILL.md
│   ├── eos-visual-skill/SKILL.md
│   ├── zuma-business-metrics/SKILL.md
│   ├── zuma-company-context/SKILL.md
│   ├── zuma-image-gen-skill/SKILL.md
│   ├── data-visualization/SKILL.md       ← NEW
│   ├── statistical-analysis/SKILL.md      ← NEW
│   ├── xlsx-skill/SKILL.md                ← NEW
│   └── zuma-ppt-design/SKILL.md
├── ops/
│   ├── dn-to-po/SKILL.md
│   ├── notion-metrics/SKILL.md
│   ├── zuma-branch/SKILL.md
│   ├── zuma-data-analyst-skill/SKILL.md
│   ├── zuma-database-assistant-skill/SKILL.md
│   ├── zuma-inventory-control/
│   │   ├── stock-opname-level-2/SKILL.md
│   │   └── zuma-ff-skills/SKILL.md
│   ├── zuma-plano-ro-skills/
│   │   ├── PROMPT_new_planogram.md
│   │   ├── PROMPT_ro_request.md
│   │   ├── step0.5-pre-planogram/SKILL.md
│   │   ├── step1-planogram/SKILL.md
│   │   ├── step2-visualizations/SKILL.md
│   │   ├── step3-zuma-ro-surplus-skills/SKILL.md  ← DEFAULT untuk RO
│   │   └── zuma-ro-box-only/SKILL.md               ← experimental (Jatim only)
│   ├── zuma-sku-context/SKILL.md
│   ├── zuma-token-usage-report/SKILL.md
│   └── zuma-warehouse-and-stocks/SKILL.md
└── skills/
    └── finance/
        ├── coretax-faktur-generator/SKILL.md
        └── fp-rekon-stock/SKILL.md
```

---

_Catatan: File ini harus di-update setiap ada skill baru ditambahkan ke `zuma-business-skills/`._
_Last updated: 2026-02-28 — tambah xlsx-skill, statistical-analysis, data-visualization_
