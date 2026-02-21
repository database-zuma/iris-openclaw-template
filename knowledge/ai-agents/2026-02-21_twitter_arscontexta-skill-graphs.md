# Arscontexta — Skill Graphs > SKILL.md

**Source:** Twitter/X Thread  
**Author:** Heinrich (@arscontexta)  
**Date Fetched:** 2026-02-21  
**Tweet:** https://x.com/arscontexta/status/2023957499183829467  
**GitHub:** https://github.com/agenticnotetaking/arscontexta  
**Website:** https://arscontexta.org  
**Stars:** 706  
**Version:** v0.8.0  
**License:** MIT

---

## Key Points

### Inti Argumen: Skill Graphs > SKILL.md

- **Problem:** Monolithic SKILL.md files (satu file besar) menyaturasi context window LLM. Agent dipaksa baca seluruh isi padahal hanya butuh 5% yang relevan untuk percakapan saat ini.
- **Solution:** **Skill Graphs** — jaringan file markdown kecil yang saling terhubung via `[[wikilinks]]`. Setiap file = satu pemikiran/teknik/skill utuh. Agent **menavigasi** graf, bukan membaca monolith.
- **Key insight:** Perbedaan antara agent yang *mengikuti instruksi* vs agent yang *memahami domain*. Skill Graphs memungkinkan yang kedua.

### Apa itu Arscontexta

- Claude Code plugin yang generate **individualized knowledge systems** dari percakapan.
- User mendeskripsikan cara berpikir dan bekerja → engine me-derive cognitive architecture (folder structure, context files, processing pipeline, hooks, navigation maps, note templates).
- Backed by **249 research claims** yang saling terhubung (cognitive science, network theory, Zettelkasten, agent architecture).
- Bukan template — **derivation**. Setiap keputusan struktural di-trace ke research claim spesifik.

### Cara Kerja Skill Graphs

**Progressive disclosure** (revelasi progresif):
```
index → descriptions → links → sections → full content
```

Mayoritas keputusan agent terjadi **sebelum membaca satu file penuh**:
1. Setiap node punya YAML frontmatter dengan deskripsi — agent scan tanpa buka file
2. Wikilinks embedded dalam prosa — membawa makna semantik, bukan sekedar referensi
3. Agent ikuti path yang relevan, skip yang tidak penting

**Tiga primitif:**
- **Wikilinks dalam prosa** — `[[konsep]]` ditulis dalam kalimat, memberi konteks *mengapa* link itu relevan
- **YAML frontmatter** — metadata yang bisa di-scan tanpa baca konten
- **MOCs (Maps of Content)** — peta yang mengorganisir cluster skill terkait

### Arsitektur: Three-Space Separation

| Space | Isi | Kecepatan Tumbuh |
|-------|-----|-------------------|
| **self/** | Identitas & metodologi agent | Lambat (~puluhan file) |
| **notes/** | Knowledge graph — pembelajaran nyata | Konstan (10-50 file/minggu) |
| **ops/** | State operasional & koordinasi task | Fluktuatif |

### Pipeline: 6 Rs (Cornell Note-Taking inspired)

1. **Record** — Capture tanpa friction
2. **Reduce** — Ekstraksi insight domain-spesifik
3. **Reflect** — Temukan koneksi, update navigation maps
4. **Reweave** — Hubungkan konteks baru ke notes yang ada
5. **Verify** — Quality checks (description, schema, health)
6. **Rethink** — Challenge asumsi sistem sendiri

Setiap fase dieksekusi di **subagent dengan context segar** — karena perhatian LLM degradasi seiring context penuh.

### Setup Process

```bash
# Install via Claude Code plugin marketplace
/plugins:add-marketplace agenticnotetaking
/install arscontexta
/arscontexta:setup  # 20-min conversational setup
```

6 fase setup:
1. Detection — deteksi environment
2. Understanding — percakapan tentang cara berpikir
3. Derivation — reasoning dengan confidence scores
4. Proposal — tampilkan yang akan di-generate
5. Generation — generate semua file
6. Validation — cek terhadap 15 kernel primitives

### Yang Di-generate

- Vault Markdown dengan wikilinks (tanpa database)
- Hierarki MOCs (hub → domain → topic)
- Note templates dengan `_schema` blocks
- Processing pipeline dengan 16 command templates
- 4 automation hooks untuk quality enforcement
- 7-halaman user manual native domain
- Context file untuk orientasi agent

### Presets

| Preset | Fokus | Use Case |
|--------|-------|----------|
| **Research** | Atomic claims, citation tracking, methodology MOCs | Academic research, paper analysis |
| **Personal** | Reflective notes, goal tracking, relation networks | Journal, professional development |
| **Experimental** | Lightweight structure for rapid prototyping | Exploring new domains |

---

## Relevansi untuk Zuma / OpenClaw

### Langsung Relevan

1. **Kita sudah pake pola serupa** — `zuma-business-skills/` dengan subfolder terstruktur dan SKILL.md files per domain. Arscontexta memvalidasi arsitektur ini.

2. **Progressive disclosure = apa yang Iris butuhkan** — Saat ini AGENTS.md sudah berperan sebagai "index" yang mengarahkan ke skill files. Konsep Skill Graph memformalisasi ini.

3. **Wikilink pattern bisa diadopsi** — Menambahkan `[[cross-references]]` antar skill files membantu navigasi. Misalnya eos-visual-skill bisa link ke `[[zuma-brand-colors]]` di company-context.

4. **Three-space separation sudah ada** — `self/` ≈ SOUL.md + AGENTS.md, `notes/` ≈ knowledge/ + memory/, `ops/` ≈ tasks/ + inbox/outbox/.

### Potensi Improvement

- **MOCs (Maps of Content):** Buat index files per domain di `zuma-business-skills/` yang list semua skill files dengan 1-line descriptions — supaya agent bisa scan tanpa baca semua.
- **YAML frontmatter:** Tambahkan metadata (tags, description, last-updated) di setiap skill file untuk faster scanning.
- **6 Rs pipeline:** Bisa di-adopt untuk knowledge dump workflow — saat ini kita Record + Reduce tapi belum Reflect/Reweave secara sistematis.

### ⚠️ Catatan

- **v0.8.0** — belum 1.0, API bisa berubah
- **Claude Code only** — plugin ini spesifik Claude Code, tidak portable ke IDE lain
- **Token-heavy setup** — 20 menit setup = banyak token consumed
- **Kita tidak perlu install arscontexta** — konsep Skill Graphs bisa diadopsi secara manual tanpa plugin
- **Skala belum teruji** — 10-50 file/minggu → ribuan file dalam beberapa bulan, belum ada data performa long-term

---

## Alternatives & Competitors

- [remember-md](https://github.com/remember-md/remember) — Alternatif second brain untuk Claude Code
- [COG-second-brain](https://github.com/huytieu/COG-second-brain) — Claude Code + Obsidian + GitHub
- [second-brain-skills](https://github.com/coleam00/second-brain-skills) — Skills-based approach
- [skill-retriever](https://github.com/AnthonyAlcaraz/skill-retriever) — Graph-based MCP server for component retrieval (1,189 components indexed)

---

## Takeaways

1. **Skill Graphs > SKILL.md** — graf navigable lebih efektif dari file monolith untuk domain yang dalam.
2. **Progressive disclosure** adalah pattern kunci — agent scan metadata dulu, baru baca konten yang relevan.
3. **Arsitektur kita sudah di jalur yang benar** — folder structure + SKILL.md + AGENTS.md routing = proto-Skill Graph.
4. **Next step realistis:** Tambahkan YAML frontmatter + MOC index files ke existing skill structure — tanpa perlu install plugin.
5. **Wikilinks dalam prosa** (bukan sebagai daftar) memberi konteks semantik yang lebih kaya untuk navigasi agent.

---

## Tags

`#skill-graphs` `#knowledge-management` `#claude-code-plugin` `#second-brain` `#zettelkasten` `#wikilinks` `#progressive-disclosure` `#agent-architecture` `#moc` `#arscontexta` `#ai-agents`
