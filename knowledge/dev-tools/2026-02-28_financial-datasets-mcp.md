# Financial Datasets MCP Server — Stock Market API for AI Agents

**URL:** https://github.com/financial-datasets/mcp-server
**API:** https://financialdatasets.ai
**Stars:** 915 ⭐ | **Forks:** 140 | **License:** MIT
**Language:** Python | **Requires:** Python 3.10+, uv
**Created:** Mar 2025 | **Last updated:** Active (Feb 2026)

## Key Points

- **MCP server** that wraps Financial Datasets API — gives AI agents (Claude, OpenClaw, etc.) direct access to US stock market data
- **10 MCP tools available:**
  - `get_income_statements` — income statements by ticker
  - `get_balance_sheets` — balance sheets by ticker
  - `get_cash_flow_statements` — cash flow by ticker
  - `get_current_stock_price` — latest price
  - `get_historical_stock_prices` — historical OHLCV
  - `get_company_news` — company-specific news
  - `get_available_crypto_tickers` — list crypto tickers
  - `get_crypto_prices` / `get_historical_crypto_prices` / `get_current_crypto_price` — crypto data
- **Data coverage:** 30,000+ US tickers, 30+ years historical, SEC filings, insider trades, analyst estimates, institutional ownership
- **Market focus: US only** — SEC filings, insider trades, institutional ownership = all US-centric. No IDX/BEI (Indonesia Stock Exchange) coverage.

## Pricing

| Plan | Cost | Notes |
|------|------|-------|
| Developer | $200/mo | 1,000 req/min, individual license, no crypto |
| Pro | $2,000/mo | Unlimited, data redistribution, crypto included |
| Enterprise | Custom | Dedicated compute, early access |
| Pay-as-you-go | $0.00–$0.10/req | Company Facts & Earnings = free (through Q1 2026) |

**Per-request costs (pay-as-you-go):**
- Free: Company Facts, Earnings
- $0.01: Crypto Prices, Interest Rates
- $0.02: Financial Metrics, Insider Trades, News, SEC Filings, Institutional Holdings
- $0.04: Income Statements, Balance Sheets, Cash Flow, Analyst Estimates
- $0.10: All Financial Statements (bundle)

## Relevance Assessment for Zuma/Iris

### ❌ NOT Relevant for Current Operations
- Zuma = offline retail footwear (sandals/apparel). Bukan fintech, bukan investasi.
- Data pure US market — **zero IDX/BEI coverage**. Tidak ada data saham Indonesia.
- $200/mo minimum = terlalu mahal untuk use case yang bukan core business.

### 🤔 Potential Future Relevance (Low Priority)
- **Personal investment tool for Wayan** — IF Wayan trades US stocks/crypto and wants Iris to help analyze fundamentals (income statements, P/E ratios, company news). Tapi ini personal, bukan Zuma ops.
- **MCP server pattern reference** — good example of how to build a simple MCP server wrapping a REST API. Bisa jadi template kalau kita mau bikin MCP server sendiri (e.g., wrapping Accurate API atau internal Zuma data).
- **Crypto monitoring** — kalau Wayan punya crypto portfolio, $0.01/request untuk crypto prices cukup murah via pay-as-you-go.

### Verdict: 🟡 AWARENESS ONLY
Simpan sebagai referensi. Jangan install/integrate kecuali Wayan explicitly minta fitur investment analysis. Pattern MCP server-nya berguna sebagai template.

## Takeaways

- Clean MCP server implementation (single `server.py`, 10 tools, env-based config) — good template
- US market only, no international/IDX support
- Expensive subscription, but pay-as-you-go exists for light usage
- If Iris ever needs stock/crypto data, this is a ready-made MCP server — just plug API key

## Tags

#mcp-server #financial-data #stock-market #api #us-stocks #crypto #paid-service #low-priority #template-reference
