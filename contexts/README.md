# contexts/ — Project-Specific Context

Folder ini untuk **brief context notes per project aktif** — supaya Iris atau sub-agent bisa langsung paham state project tanpa baca history panjang.

---

## Format

Satu file per project: `{project-slug}.md`

Isi tiap file (ringkas):
- **Goal:** Apa tujuannya?
- **Status:** Sejauh mana progress?
- **Key files:** Path penting (script, deck, DB table)
- **Notes:** Keputusan desain, gotchas, hal yang perlu diingat

---

## Contoh Naming

```
contexts/zuma-sto-dashboard.md
contexts/bm-jatim-deck.md
contexts/dn-to-po-workflow.md
contexts/portfolio-analysis.md
```

---

## Rule

- Satu file = satu project (jangan campur)
- Keep short — kalau butuh lebih dari 1 halaman, ada yang salah
- Delete file kalau project sudah selesai/archived
