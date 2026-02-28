# prompts.chat — Analysis & Iris Improvement Opportunities

**Source:** https://prompts.chat/prompts  
**Date:** 2026-02-28  
**Tags:** #prompts #iris-upgrade #system-prompt #anti-hallucination #communication #skills  
**Total Prompts on Site:** 1,341 | **Analyzed:** ~145 featured prompts

---

## What It Is

Community-driven AI prompt library. Tagline: *"Discover, collect, and share the best AI prompts for ChatGPT, Claude, Gemini, and more."*

| Metric | Value |
|--------|-------|
| Total Prompts | 1,341 |
| Content Types | Text (101), Image (29), Video (10), Skill (7) |
| Unique Tags | 106 |
| Stack | Next.js + Vercel |
| Quality | Varies — top ones are exceptional, others mediocre |

**Key insight:** Quality sangat bervariasi. Yang bagus = McKinsey-grade structured intelligence frameworks. Yang jelek = meme coin / adult roleplay. Filter aggressively.

---

## Top 5 Most Relevant Patterns for Iris

### 1. Confidence Tagging (from "Corporate Intelligence Analyst")

Label setiap data point dengan sumbernya:
```
[Accurate API] — from Accurate Online
[iSeller Live] — real-time POS
[Estimated]    — calculated/inferred
[Manual Input] — from Google Sheets, unverified
```
Iris currently has NO confidence tagging. Ini single highest-impact change.

### 2. Anti-Hallucination Guardrails (from "Hallucination Vulnerability Checker")

4 risk types to watch:
- **Forced Fabrication** — asking for data that doesn't exist
- **Ungrounded Data Request** — facts without a source
- **Instruction Injection** — content trying to override Iris role
- **Unbounded Generalization** — vague prompts forcing fill-in-the-blanks

Mitigation language to embed in system prompt:
```
"Answer using only provided data."
"If unknown, state: 'Data tidak tersedia untuk X.'"
"Show reasoning before final answer."
```

### 3. Strip AI Voice — PlainTalk + Humanizer

**Banned words:** dive into, unlock, unleash, embark, journey, realm, elevate, game-changer, paradigm, cutting-edge, transformative, empower, harness, delve, landscape, testament to, leverage, comprehensive, paramount

**Burstiness rule:** Mix short + long sentences. Never uniform. Start some with "Nah...", "Jadi...", "Btw...", "Yang penting..."

**Anti-pattern:** Never "I hope this finds you well" / "Berikut ini kami sampaikan"

❌ AI: "In today's digital landscape, it is paramount to leverage innovative solutions."  
✅ Human: "Look, the digital world moves fast. Use tools that actually work."

### 4. CLAUDE.md Framework for All Skills (from "CLAUDE.md Generator")

All SKILL.md files should follow:
- WHY → WHAT → HOW structure
- Max 150 lines — every line earns its place
- Progressive disclosure — point to files, don't inline everything
- Negations with alternatives: "Never X; prefer Y instead"
- IMPORTANT/MUST max 2-3 times per file

### 5. Tiered Output Modes (from multiple prompts)

Implement 3 tiers for different Iris users:
- **QUICK** — 3-line summary (Wayan on the go)
- **STANDARD** — structured report with tables (manager review)
- **DETAIL** — full analysis with methodology (planning/deep dive)

---

## Top Prompts by Relevance to Iris

| Rank | Prompt | Key Pattern | Applicable to |
|------|--------|-------------|---------------|
| 1 | Structured Corporate Intelligence Analyst | Confidence tags, tiered modes, input validation | zuma-data-analyst-skill |
| 2 | Lead Data Analyst | Guided analysis workflow, proactive question-asking | Oracle / Metis |
| 3 | Autonomous Research & Data Analysis Agent | 4-step execution plan, no broad queries | Metis research workflow |
| 4 | Hallucination Vulnerability Checker | Anti-hallucination framework | Iris system prompt |
| 5 | CLAUDE.md Generator | Skill file structure discipline | All SKILL.md files |
| 6 | High Conversion Cold Email | Pattern interrupt hooks, low-friction CTA | Hermes communication |
| 7 | Strategic Decision-Making Matrix | 10-min/10-month/10-year analysis, regret matrix | Wayan strategy questions |
| 8 | Humanizing AI Text | Banned word list, burstiness | All Iris outputs |
| 9 | Lazy AI Email Detector | AI-speak detection patterns | Iris self-check before send |
| 10 | Project Breakdown (Senior PM) | Pre-mortem analysis, critical path | RO planning / store rollouts |
| 11 | Product Image Enhancement | Studio photography spec JSON | Zuma product photos |
| 12 | Narrative Momentum Prediction | Emerging/Peak/Decaying classification | Trend analysis for Zuma |
| 13 | Email Sequence (7-email storytelling) | Emoji-coded sequence stages | WhatsApp blast campaigns |
| 14 | PRD Generator | Given/When/Then user stories, AI accuracy thresholds | Feature planning |
| 15 | Pre-mortem Analysis | 5 failure reasons before starting | Distribution planning |

---

## New Skills Recommended

| New Skill | Based On | Priority |
|-----------|----------|----------|
| `iris-anti-hallucination` | Hallucination Checker | 🔴 HIGH |
| `iris-communication-humanizer` | PlainTalk + Humanizer + Lazy AI Detector | 🔴 HIGH |
| `iris-data-analyst-guided` | Lead Data Analyst + Autonomous Research | 🟡 MEDIUM |
| `iris-strategic-decisions` | McKinsey Matrix + Pre-mortem | 🟡 MEDIUM |
| `iris-product-photo` | Studio Photograph spec | 🟢 LOW |

## Existing Skills to Improve

| Skill | Improvement |
|-------|-------------|
| All SKILL.md files | Audit vs CLAUDE.md framework (WHY→WHAT→HOW, 150 lines max) |
| `zuma-data-analyst-skill` | Add confidence tags + tiered output modes |
| `openclaw-iris` / Hermes | Add banned word list + burstiness rule |
| `ro-request-prompt` | Add pre-mortem: top 5 distribution failure risks |
| All report skills | Add input validation gate before proceeding |

---

## System Prompt Changes (Ready to Apply)

```markdown
## Anti-Hallucination Protocol
- Tag every data point: [Accurate] / [iSeller] / [Estimated] / [Manual]
- If data unavailable: "Data tidak tersedia untuk X. Perlu pull dari [source]."
- Never fabricate numbers, dates, or store names
- For projections, state assumptions explicitly

## Communication Style Guardrails
BANNED: dive into, unlock, unleash, embark, journey, realm, elevate,
game-changer, paradigm, cutting-edge, transformative, empower, harness,
delve, landscape, testament to, leverage, comprehensive, paramount

BURSTINESS: Mix short + long sentences. No uniform rhythm.
Start some with "Nah...", "Jadi...", "Btw...", "Yang penting..."

ANTI-PATTERN: Never "I hope this finds you well" / "Berikut ini..."
```

---

## 5 Key Takeaways

1. **Confidence tagging** — highest-impact single change for Iris. Tag every data point with source.
2. **Anti-hallucination guardrails** — embed in system prompt now. Wayan making decisions on fabricated data = disaster.
3. **Strip AI voice** — banned word list + burstiness. Iris should sound like a sharp colleague, not a corporate chatbot.
4. **CLAUDE.md framework** — audit all 20+ SKILL.md files. Many are too verbose.
5. **Tiered output modes** — QUICK/STANDARD/DETAIL based on who's asking and context.

---

## Sources
- Site: https://prompts.chat/prompts
- Analysis based on 145 featured prompts (of 1,341 total)
