# AgentSkillOS — Analysis & Skill Gap Assessment for Iris

**Source:** https://github.com/ynulihao/AgentSkillOS  
**Date:** 2026-02-28  
**Tags:** #openclaw #skills #agent-skills #skill-tree #dag #iris-upgrade #skill-gap  
**Stars:** 194 ⭐ | **Paper:** Preprint 2026 (Li et al.)

---

## What It Is

Research framework + tool for **discovering, composing, and running skill pipelines** end-to-end.

Tagline: "Build your agent from 90,000+ skills via Skill RETRIEVAL & ORCHESTRATION"

Core idea: The agent skill ecosystem has 90,000+ skills publicly available (via skills.sh marketplace). AgentSkillOS acts as the "OS" — helping agents find and chain the right ones via a **Skill Tree** hierarchy + **DAG** orchestration.

---

## Key Concepts

### 1. Skill Tree (lebih baik dari pure semantic search)

Pure semantic search (embedding similarity) cenderung miss skills yang "terlihat tidak relevan di embedding space tapi crucial untuk solve task."

AgentSkillOS menggunakan **LLM + Skill Tree** — navigasi hirarki kapabilitas dari coarse ke fine, sehingga bisa surface non-obvious skills yang actually dibutuhkan.

**Contoh:** Task "generate cat meme video" → pure semantic search mungkin tidak return `ffmpeg-color-grading-chromakey` karena kata "meme" tidak mirip "chromakey". Skill Tree mengerti bahwa video meme butuh video processing.

### 2. DAG-based Orchestration

Multiple skills dikompose dalam **Directed Acyclic Graph** — otomatis manage execution order, dependencies, dan data flow antar steps.

### 3. SKILL.md Format (validated)

Iris sudah pakai format ini — **ini format yang benar**. AgentSkillOS confirm bahwa SKILL.md-based skill definition adalah standard yang baik.

### 4. skills.sh Marketplace

90,000+ community skills tersedia. Bisa download pre-built tree (top500, top1000).

---

## 50 Skill Seeds (Curated List)

Ini skill seeds berkualitas tinggi yang dipilih berdasarkan GitHub stars dan download volume:

| Skill | Deskripsi |
|-------|-----------|
| algorithmic-art | Generative art via code |
| analyzing-financial-statements | Parse & analyze laporan keuangan |
| api-integration-specialist | Integrasi API kompleks |
| auth-implementation-patterns | Auth patterns (JWT, OAuth, etc.) |
| baoyu-xhs-images | Xiaohongshu/RedNote infographic generator |
| beads | Bead pattern generation |
| brand-guidelines | Generate brand-compliant content |
| browser-automation | Browser automation general |
| canvas-design | Canvas-based design |
| clinical-decision-support | Medical decision support |
| code-review-excellence | Code review best practices |
| creating-financial-models | Financial modeling (DCF, etc.) |
| **data-storytelling** | ← Iris punya ini |
| **data-visualization** | Charts & graphs generation |
| **dev-browser** | Browser automation dengan persistent state |
| diagramming | Flowcharts, architecture diagrams |
| doc-coauthoring | Collaborative document editing |
| **docx** | Create/edit Word documents |
| email-composer | Professional email drafting |
| employment-contract-templates | HR document templates |
| fabric | Python image processing library |
| **ffmpeg-color-grading-chromakey** | Video: green screen, color grading |
| **firecrawl-scraper** | Web scraping via Firecrawl |
| frontend-design | Production-grade frontend UI |
| **generate-image** | AI image gen (FLUX, Gemini) |
| internal-comms | Internal communications |
| joke-engineering | Humor analysis & improvement |
| marketing-demand-acquisition | Marketing & growth strategy |
| **markitdown** | Convert files (PDF/Word/Excel/PPT) to Markdown |
| mcp-builder | Build MCP servers |
| **media-processing** | Video/audio/image via FFmpeg & ImageMagick |
| microsim-generator | Micro-simulation builder |
| openai-api | OpenAI API patterns |
| **pdf** | PDF creation & manipulation |
| performance-optimization | Code/system performance |
| **postgresql-table-design** | PostgreSQL schema design |
| **pptx** | PowerPoint creation & editing |
| product-requirements | PRD writing |
| prompt-engineering-patterns | Prompt design patterns |
| research-grants | Academic grant writing |
| resolve-conflicts | Conflict resolution frameworks |
| skill-creator | **META: Create new skills autonomously** |
| slack-gif-creator | Slack GIF generation |
| **social-media-generator** | Platform-optimized social content |
| **sql-optimization-patterns** | SQL query optimization |
| **statistical-analysis** | Statistical methods & analysis |
| theme-factory | UI theme generation |
| tooluniverse | Tool discovery & integration |
| transformers | HuggingFace transformers |
| treatment-plans | Medical treatment planning |
| web-artifacts-builder | Interactive HTML/JS artifacts |
| webapp-testing | Web app testing |
| **xlsx** | Excel file creation & manipulation |

**Bold** = relevan untuk Iris/Zuma

---

## Gap Analysis: Iris vs AgentSkillOS Seeds

### Iris sudah punya:
- `data-storytelling` ✅
- `generate-image` (via zuma-image-gen-skill) ✅
- `pptx` (via eos-visual-skill + zuma-ppt-design) ✅
- `postgresql-table-design` (via zuma-database-assistant-skill) ✅
- `sql-optimization-patterns` (partial, via zuma-data-analyst-skill) ✅
- `dev-browser` (via Playwright MCP) ✅
- `firecrawl-scraper` (via Firecrawl MCP) ✅
- `brand-guidelines` (via BRAND.md + zuma-company-context) ✅

### Iris TIDAK punya (gap yang perlu diisi):

#### 🔴 HIGH PRIORITY

**1. `markitdown`** — Convert PDF/Word/Excel/PPT ke Markdown untuk AI processing
- Iris sering terima dokumen dari supplier/manager (invoice PDF, laporan Excel, kontrak Word)
- Sekarang tidak ada cara structured untuk parse dokumen ini
- **Action:** Buat skill `ops/markitdown-processor/SKILL.md` menggunakan [markitdown](https://github.com/microsoft/markitdown) Python library

**2. `xlsx`** — Excel file creation & manipulation dengan python-openpyxl/xlsxwriter
- Excel central di operasi Zuma (planogram output, RO request, sales report)
- Iris bisa generate data tapi output ke Excel masih manual/basic
- **Action:** Enhance existing skills (planogram, RO) dengan dedicated Excel output capability

**3. `statistical-analysis`** — Statistical methods (mean, median, std dev, percentile, regression)
- Iris generate laporan tapi mostly aggregation sederhana, belum statistical insights
- Bisa drastically improve kualitas analysis untuk Wayan
- **Action:** Buat skill `general/statistical-analysis/SKILL.md` atau add ke zuma-data-analyst-skill

**4. `data-visualization`** — Chart/graph generation (matplotlib, plotly, atau HTML Canvas)
- Laporan Iris sekarang: tabel teks. Bisa lebih visual
- **Action:** Add chart generation capability ke eos-visual-skill atau buat skill terpisah

#### 🟡 MEDIUM PRIORITY

**5. `social-media-generator`** — Platform-optimized content untuk Instagram/TikTok/WA Status
- Zuma punya Instagram dan WhatsApp touchpoints
- Bisa otomasi konten promosi produk, event announcements
- **Action:** Buat skill `general/zuma-social-media/SKILL.md` dengan Zuma brand guidelines

**6. `docx`** — Proper Word document generation (python-docx)
- Laporan formal ke management masih manual atau plaintext
- **Action:** Buat skill untuk generate .docx dengan Zuma branding

**7. `pdf`** — PDF generation dari HTML/data
- Invoice, purchase orders, laporan formal
- **Action:** Buat skill `ops/pdf-generator/SKILL.md` (weasyprint atau reportlab)

**8. `brand-guidelines` (formal)** — Skill terstruktur untuk brand-compliant output
- Iris punya BRAND.md tapi belum ada formal skill yang enforce ini di setiap output
- **Action:** Formalize existing brand context menjadi actionable skill

#### 🟢 LOW / FUTURE PRIORITY

**9. `skill-creator`** — META-SKILL: Agent bisa create skills sendiri
- Iris bisa jadi autonomous dalam extend kemampuannya
- **Action:** Perlu research dulu — high risk kalau skill yang di-generate Iris tidak di-review

**10. `ffmpeg-color-grading-chromakey` + `media-processing`** — Video processing
- Untuk konten Zuma social media (product videos, event highlight reel)
- **Action:** Low priority sekarang, high effort setup FFmpeg di VPS

**11. `diagramming`** — Flowcharts (Mermaid, Graphviz)
- Useful untuk dokumentasi proses operasional Zuma
- **Action:** Easy to add — Mermaid sudah bisa di Markdown

**12. `mcp-builder`** — Build MCP servers
- Advanced use case: extend Iris tools via custom MCP
- **Action:** Future, when there's a specific tool gap that needs custom MCP

---

## Rekomendasi Implementasi (Prioritized)

### Batch 1 (Quick wins, high value):
1. **`markitdown` skill** — Install `markitdown` di Mac Mini + VPS, buat SKILL.md
2. **Enhance `zuma-data-analyst-skill`** dengan statistical analysis patterns dari AgentSkillOS seeds
3. **Enhance `eos-visual-skill`** dengan data visualization (chart HTML generation)

### Batch 2 (Medium effort):
4. **`zuma-social-media` skill** — Content generation untuk Instagram/WA dengan Zuma brand
5. **`xlsx` enhancement** — Better Excel output untuk planogram & RO skills
6. **`pdf-generator` skill** — PDF output untuk formal documents

### Batch 3 (Future):
7. **`skill-creator`** — Setelah arsitektur skills lebih mature
8. **Video processing** — Kalau ada kebutuhan konkret dari Wayan

---

## AgentSkillOS Architecture — Key Takeaways

1. **Skill Tree > Semantic Search** untuk skill discovery. Iris saat ini manual routing. Kalau skill library Iris bertumbuh >20 skills, consider implementing skill tree hierarchy di SKILLS_INDEX.md

2. **DAG orchestration** = apa yang Iris sudah lakukan via ORCHESTRATION.md tapi informal. Formalize pipeline definitions untuk reusable workflows (e.g., "data report pipeline" = query → analyze → visualize → format → deliver)

3. **SKILL.md format validated** — Iris sudah di jalur yang benar. Keep consistent.

4. **skills.sh marketplace** — 90,000+ community skills available. Before building new skill, check if community skill exists first.

---

## Skill Seeds yang Bisa Langsung Dipinjam/Adaptasi

Skills berikut bisa langsung di-fetch dari AgentSkillOS dan diadaptasi untuk Iris:

```bash
# Fetch specific skill content dari repo
curl -s https://raw.githubusercontent.com/ynulihao/AgentSkillOS/main/data/skill_seeds/markitdown/SKILL.md
curl -s https://raw.githubusercontent.com/ynulihao/AgentSkillOS/main/data/skill_seeds/xlsx/SKILL.md
curl -s https://raw.githubusercontent.com/ynulihao/AgentSkillOS/main/data/skill_seeds/statistical-analysis/SKILL.md
curl -s https://raw.githubusercontent.com/ynulihao/AgentSkillOS/main/data/skill_seeds/data-visualization/SKILL.md
curl -s https://raw.githubusercontent.com/ynulihao/AgentSkillOS/main/data/skill_seeds/social-media-generator/SKILL.md
curl -s https://raw.githubusercontent.com/ynulihao/AgentSkillOS/main/data/skill_seeds/docx/SKILL.md
```

Lalu adapt ke Zuma context (bahasa Indonesia, brand guidelines, DB schema, dll).

---

## Sources

- GitHub: https://github.com/ynulihao/AgentSkillOS
- Paper: https://github.com/ynulihao/AgentSkillOS/blob/main/assets/AgentSkillOS.pdf
- Landing page: https://ynulihao.github.io/AgentSkillOS/
- Skill seeds: https://github.com/ynulihao/AgentSkillOS/tree/main/data/skill_seeds
- skills.sh marketplace: https://skills.sh
