# Knowledge Dump System

**Auto-mode knowledge capture from links → structured summaries**

## How It Works

1. **Send link** (Twitter, Reddit, article) via WhatsApp
2. **Iris detects** → scrapes content
3. **Summarizes** in structured format (Key Points, Technical Details, Takeaways)
4. **Auto-saves** to topic folder
5. **Updates INDEX.md** automatically

## Folder Structure

```
knowledge/
├── ai-agents/          # AI, ML, LLM, automation, agents
├── business-ops/       # Operations, retail, logistics, inventory
├── dev-tools/          # Code, infra, devtools, frameworks
├── misc/               # Uncategorized
└── INDEX.md            # Master searchable index
```

## Summary Format

Each file follows this structure:

```markdown
# [Title/Topic]

**Source:** Twitter/Reddit/Article
**Author:** @username / r/subreddit
**Date:** YYYY-MM-DD
**Link:** https://...

**Key Points:**
- Main insight 1
- Main insight 2
- Main insight 3

**Technical Details:**
- Implementation specifics
- Architecture/approach

**Takeaways:**
- What matters for Zuma/Wayan
- Action items (if any)

**Tags:** #tag1 #tag2 #tag3
```

## Supported Sources

- **Twitter/X:** Via Nitter instances (no login required) or browser fallback
- **Reddit:** Native JSON API (append `.json` to URL)
- **Articles:** web_fetch (Readability extraction)
- **Fallback:** Browser automation (Chrome relay) for any site

## Search & Browse

```bash
# Search all knowledge
grep -r "scaling" knowledge/

# Search by tag
grep -r "#ai-agents" knowledge/

# Recent entries (last 7 days)
find knowledge/ -name "*.md" -mtime -7

# Browse INDEX
cat knowledge/INDEX.md
```

## Auto-Categorization Logic

- AI, LLM, agents, prompts → `ai-agents/`
- Ops, retail, business, logistics → `business-ops/`
- Code, frameworks, tools → `dev-tools/`
- Unclear → `misc/` (Iris may ask for manual category)

---

**Setup date:** 2026-02-14  
**Maintained by:** Iris (auto-mode)
