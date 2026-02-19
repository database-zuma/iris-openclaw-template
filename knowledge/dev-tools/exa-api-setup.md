# Exa AI API — Setup & Reference

**Source:** Exa dashboard onboarding  
**Account:** database@zuma.id  
**Key:** `$EXA_API_KEY` (see `.env`)  
**Docs:** https://docs.exa.ai  
**Dashboard:** https://dashboard.exa.ai

## Config (Wayan's setup)
- Coding tool: Claude
- Framework: Other (agentic workflow)
- Search type: `auto` (balanced relevance & speed)
- Content: Full text (`max_characters: 20000`)

## MCP Server (Claude Code)
```bash
claude mcp add -e EXA_API_KEY=$EXA_API_KEY exa -- npx -y exa-mcp-server
```
Or via HTTP:
```json
{ "mcpServers": { "exa": { "type": "http", "url": "https://mcp.exa.ai/mcp?exaApiKey=YOUR_API_KEY" } } }
```

**Available MCP tools:** `web_search_exa`, `get_code_context_exa`, `company_research_exa`, `crawling_exa`, `linkedin_search_exa`, `deep_researcher_start`

## Quick Search (cURL)
```bash
curl -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query": "your query", "type": "auto", "num_results": 10, "contents": {"text": {"max_characters": 20000}}}'
```

## Python (Anthropic Tool Use)
```python
from exa_py import Exa
exa = Exa(api_key="$EXA_API_KEY")
results = exa.search(query="...", type="auto", num_results=10, contents={"text": {"max_characters": 20000}})
```

## Search Types
| Type | Best For | Speed |
|------|----------|-------|
| `fast` | Real-time, autocomplete | Fastest |
| `auto` | Most queries ← **default** | Medium |

## Content Types (choose one)
- **Text** `"text": {"max_characters": 20000}` — full content, RAG
- **Highlights** `"highlights": {"max_characters": 2000}` — snippets, cheaper

⚠️ `text: true` = token-heavy. Always set `max_characters`.

## Categories
`people` | `company` | `news` | `research paper` | `tweet`

## Other Endpoints
- `/contents` — get content for known URLs
- `/answer` — Q&A with citations

## Tags
`#exa #search #web-search #agentic #tools`
