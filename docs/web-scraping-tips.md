# Web Scraping Troubleshooting

> Moved from MEMORY.md (2026-02-19). Reference: `MEMORY.md § Reference Docs`

---

## When Website Can't Be Scraped (Anti-Bot / JS-Rendered / reCAPTCHA)

1. **Coba mobile site** (`m.xxx.com`) — sering server-side rendered (PHP), gak pake JS
2. **Coba Firecrawl API** dengan `waitFor` — render JS di server
3. **Cari hidden API endpoints** — inspect network traffic, cek GitHub repos
4. **Coba different User-Agent** (mobile iPhone/Android)
5. **Coba agregator sites** (jadwalnonton.com, rajatiket.com, dll)
6. **Last resort:** Chrome extension relay (manual attach tab)

**Priority:** Firecrawl > browser openclaw > web_fetch (untuk JS-heavy sites)

---

## Case Study — XXI Cinema (2026-02-18)

**Problem:** Desktop site (21cineplex.com) = Next.js + reCAPTCHA = impossible.

**Solution:** Mobile site (`m.21cineplex.com`) = PHP server-rendered = curl langsung works. Cinema ID format juga beda antara desktop dan mobile API.

**Lesson:** Selalu coba mobile version dulu sebelum menyerah.

**Firecrawl API:**
- Endpoint: `https://api.firecrawl.dev/v1/scrape`
- Key: in `.env` as `FIRECRAWL_API_KEY` (also hardcoded in TOOLS.md)
