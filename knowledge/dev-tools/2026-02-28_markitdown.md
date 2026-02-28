# MarkItDown — Document → Markdown Converter (Microsoft)

**Date saved:** 2026-02-28  
**Source:** https://github.com/microsoft/markitdown  
**Tags:** #document-processing #markdown #llm-ready #pdf #excel #word #ppt #microsoft #installed  
**Stars:** ~40k | **License:** MIT | **Version installed:** v0.0.1a1 (upgrade recommended)  
**Author:** Microsoft AutoGen Team (Adam Fourney)

---

## Status: ✅ INSTALLED & INTEGRATED

- **Binary:** `~/.local/bin/markitdown`
- **Python:** `pip show markitdown` → v0.0.1a1
- **SKILL.md:** `~/.claude/skills/markitdown/SKILL.md` ✅
- **Referenced in:** `xlsx-skill`, `statistical-analysis`, `zuma-data-analyst-skill`, `iris-openclaw-data-analyst-guided`
- **Iris TOOLS.md:** ✅ sudah tercatat

---

## Apa Ini

Lightweight Python utility dari Microsoft untuk convert berbagai format file ke Markdown — specifically untuk LLM consumption. Token-efficient, preserves document structure (headings, lists, tables, links).

**Core pattern:**
```
User kirim file → markitdown convert → markdown → LLM/skill analisis
```

---

## Supported Formats

PDF, Word (.docx), Excel (.xlsx/.xls), PowerPoint (.pptx), Images (EXIF + OCR), Audio (speech transcription), HTML, CSV, JSON, XML, ZIP, YouTube URLs, EPub

---

## Usage

```bash
# CLI
markitdown file.pdf
markitdown file.xlsx -o output.md

# Python
from markitdown import MarkItDown
result = MarkItDown().convert("report.pdf")
print(result.text_content)
```

---

## Upgrade (Recommended)

Versi terinstall (0.0.1a1) adalah alpha lama. Latest ~0.1.x:

```bash
pip3 install --upgrade 'markitdown[all]'
# Atau format spesifik:
pip3 install 'markitdown[pdf,docx,xlsx,pptx]'
```

---

## Vs OmniDocs

| | markitdown | OmniDocs |
|--|--|--|
| Status | ✅ **Installed** | ❌ Belum install |
| Output | Markdown | Markdown/HTML/DataFrame/Pydantic |
| Approach | Simple text conversion | Vision model (layout-aware) |
| GPU needed | No | Optional (cloud API ok) |
| Use case | General doc → LLM | Visual-heavy docs, scanned PDF |

OmniDocs lebih powerful untuk scanned PDF atau dokumen dengan layout kompleks. Markitdown cukup untuk dokumen text-based standar.
