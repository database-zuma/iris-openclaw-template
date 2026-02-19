# 🤖 Botasaurus — All-in-One Web Scraping Framework

**Source:** GitHub Repository  
**Author:** Omkar Khilari (omkarcloud)  
**Date Fetched:** 2026-02-19  
**Link:** https://github.com/omkarcloud/botasaurus  
**Stars:** 3.9k ⭐ | **Forks:** 339 | **License:** MIT  

---

## Key Points

- **Apa itu:** Botasaurus adalah Python framework all-in-one untuk web scraping yang di-design khusus untuk bypass bot detection — tagline-nya "The All in One Framework to Build Undefeatable Scrapers"
- **Anti-bot bypass kelas berat:** Bisa bypass Cloudflare WAF, BrowserScan, Fingerprint.com, Datadome, dan Cloudflare Turnstile CAPTCHA — diklaim lebih stealthy dari `undetected-chromedriver` dan `puppeteer-stealth`
- **Dua mode scraping:** `@browser` (Selenium-based, full browser) dan `@request` (HTTP-based, browser-like requests tanpa buka browser) — bisa dipilih per use case
- **Built-in Web UI:** Bisa langsung buat scraper jadi web app dengan dashboard, REST API, input form, dan data export (JSON/CSV/Excel) — semua dengan minimal code
- **Produktivitas tinggi:** Parallelization, caching, proxy management, profiles, dan data cleaning sudah built-in — hemat ratusan jam development
- **Hemat proxy cost:** Klaim hemat hingga 97% biaya proxy dengan browser-based fetch requests
- **Scalable:** Support Kubernetes untuk multi-machine scaling

---

## Technical Details

### Arsitektur

```
Botasaurus Framework
├── @browser decorator     → Humane Selenium Driver (AntiDetectDriver)
├── @request decorator     → Browser-like HTTP requests (stealth mode)
├── soupify()              → BeautifulSoup wrapper
├── botasaurus_server      → Web UI backend (Python Flask/FastAPI)
├── botasaurus-controls    → Frontend input controls (React/JS)
└── Output utilities       → Auto-save JSON/CSV/Excel
```

### Core Dependencies
- **Selenium** (underlying browser automation)
- **BeautifulSoup** (HTML parsing via `soupify()`)
- **Python** — install via `pip install botasaurus`
- Node.js + React (untuk UI mode)

### Cara Kerja Anti-Bot Bypass

**1. Google Referrer Technique**
```python
driver.google_get("https://target-site.com/")  
# Membuat request terlihat datang dari Google Search
```
Efektif untuk Cloudflare "Connection Challenge" — halaman produk, blog, search results.

**2. Full Cloudflare JS+CAPTCHA Bypass**
```python
driver.google_get("https://target-site.com/", bypass_cloudflare=True)
# Menjalankan JS computations yang dibutuhkan untuk solve CAPTCHA
```

**3. Stealth HTTP Requests**
```python
@request(use_stealth=True, max_retry=10)
def scrape(request: Request, data):
    response = request.get(url)  # Browser-like headers & fingerprint
```

**4. Human-like Mouse Movements**
Simulates realistic mouse movements untuk bypass behavior-based detection.

**5. Browser Profiles**
Bisa pakai persistent Chrome profiles untuk maintain cookies dan session.

### Pattern Penggunaan

```python
# Browser mode (untuk JS-heavy sites)
@browser(headless=True, profile='Profile1')
def scrape_task(driver: Driver, data):
    driver.get("https://example.com")
    return {"data": driver.get_text("h1")}

# Request mode (lebih cepat, tanpa buka browser)
@request(max_retry=5)
def scrape_task(request: Request, data):
    response = request.get("https://example.com")
    soup = soupify(response)
    return {"data": soup.find("h1").get_text()}
```

### UI Scraper (3 Steps)
1. Buat scraper function dengan decorator
2. `Server.add_scraper(scrape_func)` — 1 baris kode
3. Define input controls di JS file

Hasilnya: Web app di `localhost:3000` dengan dashboard task, API docs, dan data export.

### Limitations (dari 3rd-party testing)
- **Datadome:** Bisa bypass halaman listing produk, tapi **blocked di product detail pages** (Datadome mengumpulkan browser session events — susah di-fake tanpa full browser interaction)
- **@request mode:** Tidak bisa solve JS CAPTCHA — butuh `@browser` + `bypass_cloudflare=True`
- **Retry diperlukan:** Cloudflare dengan @request kadang butuh beberapa retry

---

## Relevance untuk Zuma Indonesia

### ❌ Bukan Pengganti Firecrawl

Botasaurus dan Firecrawl memiliki use case yang **berbeda dan komplementer**:

| Aspek | Botasaurus | Firecrawl |
|-------|-----------|-----------|
| **Focus** | Anti-bot scraping automation | Web → Markdown/structured data untuk AI |
| **Target user** | Developer scraper | AI/RAG pipeline builder |
| **Output** | Raw data (JSON/CSV/Excel) | Clean markdown for LLM consumption |
| **Bot bypass** | ✅ Built-in, advanced | ❌ Basic / via proxy |
| **AI integration** | ❌ Tidak ada | ✅ Dirancang untuk RAG |
| **Setup** | Python framework | Managed API / self-hosted |

**Verdict:** Pakai Firecrawl untuk AI pipeline; pakai Botasaurus untuk raw data scraping dari situs yang protektif.

### ✅ Use Cases Spesifik untuk Zuma

1. **Competitive Pricing Intelligence**  
   Scrape harga kompetitor (Tokopedia, Shopee, Blibli) secara otomatis — terutama yang ada Cloudflare protection. Berguna untuk live price tracking.

2. **Lead Generation — Google Maps Scraping**  
   Creator sendiri punya project `google-maps-scraper` berbasis Botasaurus. Bisa dipakai untuk generate database prospek toko, distributor, atau vendor baru di seluruh Indonesia.

3. **Market Research Otomatis**  
   Monitor harga dan produk kompetitor FMCG, generate laporan price intelligence secara scheduled.

4. **B2B Data Collection**  
   Scrape data kontak bisnis, katalog supplier, atau informasi pasar yang tidak tersedia via API.

5. **Internal Scraper Tool sebagai SaaS**  
   Fitur UI-nya memungkinkan scraper dikemas jadi web app — bisa jadi produk internal Zuma atau tools untuk tim tanpa coding skill.

### Effort Estimate
- Setup dasar: **< 1 hari**
- Scraper sederhana anti-Cloudflare: **1–3 hari**
- Full web UI scraper: **3–7 hari**

---

## Takeaways

1. **Sangat powerful untuk bypass Cloudflare** — ini adalah differentiator utamanya vs Selenium/Playwright biasa
2. **Developer experience bagus** — decorator pattern (`@browser`, `@request`) membuat kode bersih dan modular
3. **All-in-one tapi Python-only** — tidak ada TypeScript SDK resmi
4. **UI scraper feature unik** — kemampuan package scraper jadi web app dalam sehari adalah value prop yang langka
5. **Datadome masih jadi tantangan** — untuk situs dengan Datadome yang ketat, mungkin perlu kombinasi dengan residential proxy
6. **Open source & MIT** — bebas digunakan untuk komersial
7. **Aktif dikembangkan** — 3.9k stars, terakhir di-update aktif per 2024–2025

---

## Tags

`#web-scraping` `#python` `#anti-bot` `#cloudflare-bypass` `#selenium` `#automation` `#dev-tools` `#data-collection` `#competitive-intelligence` `#open-source` `#lead-generation`
