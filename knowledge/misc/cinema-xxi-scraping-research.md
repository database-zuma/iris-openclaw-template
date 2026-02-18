# Cinema XXI Scraping Research
**Last updated:** 2026-02-18  
**Target:** Royal Plaza XXI Surabaya

---

## ✅ WORKING SOLUTION FOUND

**Base URL:** `https://m.21cineplex.com` (mobile site — server-side rendered, no JavaScript required, no CAPTCHA)  
**Schedule endpoint:** `https://m.21cineplex.com/gui.schedule.php?sid=&find_by=1&cinema_id={CINEMA_ID}&movie_id=`  
**Correct cinema_id for Royal Plaza Surabaya:** `SBYROYA` (NOT `RLPLSB`)

---

## ❌ Approaches Yang Gagal

| Approach | Status | Alasan Gagal |
|----------|--------|-------------|
| `web_fetch` 21cineplex.com | ❌ | Client-side rendered, butuh JavaScript |
| Browser headless (openclaw profile) | ❌ | Anti-bot detection, showtime kosong |
| Firecrawl API | ❌ | reCAPTCHA blocking |
| Google Search | ❌ | Gak nunjukin jadwal inline |
| jadwalnonton.com | ❌ | 404 / city list only |
| rajatiket.com | ❌ | 502 error |
| TIX ID | ❌ | 404 |
| M-TIX API `mtixapi/v1/theater/RLPLSB/schedule` | ❌ | 404 (wrong endpoint + wrong ID format) |
| `m.21cineplex.com` dengan `cinema_id=RLPLSB` | ❌ | Template vars unfilled (wrong ID) |

---

## ✅ Approach Baru Yang Berhasil

### Mobile Site Scraping — m.21cineplex.com

Ditemukan dari GitHub repo `heirro/21cineplex-api` dan `tfkhdyt/21cineplex-api`.

**Key insight:**
- `21cineplex.com` (desktop) = client-side rendered, butuh JS, ada anti-bot
- `m.21cineplex.com` (mobile) = server-side rendered PHP, bisa di-curl langsung, no CAPTCHA!
- City IDs numerik (bukan nama kota): Surabaya = `12`
- Cinema IDs format: `{CITY_PREFIX}{THEATER_CODE}` (contoh: `SBYROYA` = Surabaya + Royal)

**Endpoint Flow:**
```
1. Get city list:    GET https://m.21cineplex.com/gui.list_city.php
2. Get theaters:     GET https://m.21cineplex.com/gui.list_theater.php?sid=&city_id=12
3. Get schedules:    GET https://m.21cineplex.com/gui.schedule.php?sid=&find_by=1&cinema_id=SBYROYA&movie_id=
```

### Cinema IDs Surabaya (discovered 2026-02-18)

| Cinema ID | Nama |
|-----------|------|
| SBYCIWO | CIPUTRA WORLD XXI |
| SBYDELT | DELTA XXI |
| SBYLENM | FAIRWAY NINE XXI |
| SBYGALA | GALAXY XXI |
| SBYGRCI | GRAND CITY XXI |
| SBYPACI | PAKUWON CITY XXI |
| SBYPAFJ | PAKUWON FOOD JUNCTION XXI |
| SBYPAMA | PAKUWON MALL XXI |
| SBYSTUO | PTC XXI |
| **SBYROYA** | **ROYAL XXI** ← target kita |
| SBYTRIC | TRANS ICON MALL XXI |
| SBYTRNG | TRANSMART NGAGEL XXI |
| SBYTRRU | TRANSMART RUNGKUT XXI |
| SBYTUNJ | TUNJUNGAN 3 XXI |
| SBYTUN5 | TUNJUNGAN 5 XXI |
| SBYTUNU | TUNJUNGAN PLAZA XXI |
| SBYIXPM | PAKUWON MALL IMAX |
| SBYIXT5 | TUNJUNGAN 5 IMAX |
| SBYPRCW | CIPUTRA WORLD PREMIERE |
| SBYPRLE | FAIRWAY NINE PREMIERE |
| SBYPRGA | GALAXY PREMIERE |
| SBYPRGC | GRAND CITY PREMIERE |
| SBYPRPM | PAKUWON MALL PREMIERE |
| SBYPRT5 | TUNJUNGAN 5 PREMIERE |

---

## 🧪 Test Result (Live Data 2026-02-18)

**Theater:** ROYAL XXI  
**Address:** JL. JEND A.YANI, ROYAL PLAZA LT. 3  
**Phone:** (031) 827-1521  
**Coordinates:** -7.308804, 112.734522

**Jadwal hari ini (18 Feb 2026):**

| Film | Format | Rating | Durasi | Harga | Showtime |
|------|--------|--------|--------|-------|---------|
| GOAT | 2D | SU | 100 mnt | Rp 35,000 | 15:35 (sold out) |
| RUMAH TANPA CAHAYA | 2D | R13+ | 102 mnt | Rp 35,000 | 13:25 (sold out) |
| KUYANK | 2D | R13+ | 98 mnt | Rp 35,000 | 13:40 (sold out), **20:05** ✅ |
| KAFIR, GERBANG SUKMA | 2D | D17+ | 108 mnt | Rp 35,000 | 15:25 (sold out), **20:15** ✅ |
| SEBELUM DIJEMPUT NENEK | 2D | R13+ | 103 mnt | Rp 35,000 | 13:30, 15:30 (sold out), **20:20** ✅ |
| ALAS ROBAN | 2D | D17+ | 111 mnt | Rp 35,000 | 13:10, 15:20 (sold out), **20:10** ✅ |

> ✅ = masih tersedia beli tiket | sold out = semua kursi habis

---

## 💻 Working Code

### Python Scraper (requests + BeautifulSoup)

```python
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

BASE_URL = "https://m.21cineplex.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15"
}

def get_cities():
    """Get all available cities"""
    resp = requests.get(f"{BASE_URL}/gui.list_city.php", headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")
    cities = []
    for li in soup.select("ul.list-group li"):
        div = li.find("div")
        if div and div.get("onclick"):
            city_id = div["onclick"].split("city_id=")[1].split("'")[0]
            cities.append({"id": city_id, "name": div.get_text(strip=True)})
    return cities

def get_theaters(city_id):
    """Get all theaters in a city"""
    resp = requests.get(f"{BASE_URL}/gui.list_theater.php?sid=&city_id={city_id}", headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")
    theaters = []
    for div in soup.select("div.nav_theater_content div[onclick]"):
        onclick = div.get("onclick", "")
        if "cinema_id=" in onclick:
            cinema_id = onclick.split("cinema_id=")[1].split("&")[0].rstrip("'")
            name = div.get_text(strip=True)
            theaters.append({"id": cinema_id, "name": name})
    return theaters

def get_schedule(cinema_id):
    """Get today's schedule for a theater"""
    url = f"{BASE_URL}/gui.schedule.php?sid=&find_by=1&cinema_id={cinema_id}&movie_id="
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Theater info
    theater = {
        "id": cinema_id,
        "name": soup.select_one("h4 > span > strong").get_text(strip=True) if soup.select_one("h4 > span > strong") else None,
    }
    addr_span = soup.select_one('h4 > span[style="font-size:14px"]')
    if addr_span:
        addr_text = addr_span.get_text(separator=" ")
        parts = addr_text.split("TELEPON")
        theater["address"] = parts[0].strip()
        theater["phone"] = parts[1].replace(":", "").strip() if len(parts) > 1 else None
    
    # Map link
    map_link = soup.select_one("a.map-link")
    if map_link:
        theater["maps_url"] = map_link.get("href", "").replace("&output=embed", "")
    
    # Movies
    movies = []
    for li in soup.select("ul.list-group li.list-group-item"):
        movie_link = li.select_one("a.movie-detail-link")
        movie_id = movie_link["href"].split("movie_id=")[1] if movie_link else None
        title = li.select_one("a:not(.movie-detail-link)").get_text(strip=True) if li.select_one("a:not(.movie-detail-link)") else None
        
        format_spans = li.select("span.btn.btn-outline")
        fmt = format_spans[0].get_text(strip=True) if len(format_spans) > 0 else None
        rating = format_spans[1].get_text(strip=True) if len(format_spans) > 1 else None
        
        duration_span = li.select_one("span.glyphicon-time")
        duration = duration_span.parent.get_text(strip=True) if duration_span else None
        
        banner = li.select_one("img")
        banner_url = banner["src"] if banner else None
        
        showtimes = []
        for row in li.select("div.row"):
            date_el = row.select_one(".p_date")
            price_el = row.select_one(".p_price")
            date = date_el.get_text(strip=True) if date_el else None
            price = price_el.get_text(strip=True) if price_el else None
            
            times = []
            for slot in row.select(".div_schedule"):
                time_text = slot.get_text(strip=True)
                available = "disabled" not in slot.get("class", []) or "btn-outline-primary" in slot.get("class", [])
                # More accurate: check if background is grey (disabled/sold out)
                style = slot.get("style", "")
                sold_out = "#737373" in style
                times.append({"time": time_text, "available": not sold_out})
            
            if date or times:
                showtimes.append({"date": date, "price": price, "times": times})
        
        if title:
            movies.append({
                "id": movie_id,
                "title": title,
                "format": fmt,
                "rating": rating,
                "duration": duration,
                "banner_url": banner_url,
                "showtimes": showtimes
            })
    
    return {"theater": theater, "movies": movies}


if __name__ == "__main__":
    # Example: Get Royal XXI Surabaya schedule
    result = get_schedule("SBYROYA")
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

### Node.js Scraper (axios + cheerio — mirip GitHub repos)

```javascript
const axios = require('axios');
const cheerio = require('cheerio');

const BASE_URL = 'https://m.21cineplex.com';
const HEADERS = {
  'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15'
};

async function getSchedule(cinemaId) {
  const { data } = await axios.get(
    `${BASE_URL}/gui.schedule.php?sid=&find_by=1&cinema_id=${cinemaId}&movie_id=`,
    { headers: HEADERS }
  );
  const $ = cheerio.load(data);

  const theater = {
    id: cinemaId,
    name: $('h4 > span > strong').text(),
    address: $('h4 > span[style="font-size:14px"]').text().split('TELEPON')[0].trim(),
    phone: $('h4 > span[style="font-size:14px"]').text().split('TELEPON')[1]?.replace(':', '').trim()
  };

  const movies = [];
  $('ul.list-group li.list-group-item').each((_, el) => {
    const title = $(el).find('a:not(.movie-detail-link)').text().trim();
    const format = $(el).find('span.btn').first().text();
    const rating = $(el).find('span.btn').first().next().text();
    const duration = $(el).find('span.glyphicon-time').parent().text().trim();

    const showtimes = [];
    $(el).find('div.row').each((_, row) => {
      const date = $(row).find('.p_date').text().trim();
      const price = $(row).find('.p_price').text().trim();
      const times = [];
      $(row).find('.div_schedule').each((_, slot) => {
        const isSoldOut = $(slot).css('background-color') === '#737373' ||
                          $(slot).attr('style')?.includes('#737373');
        times.push({ time: $(slot).text().trim(), available: !isSoldOut });
      });
      if (date) showtimes.push({ date, price, times });
    });

    if (title) movies.push({ title, format, rating, duration, showtimes });
  });

  return { theater, movies };
}

getSchedule('SBYROYA').then(data => console.log(JSON.stringify(data, null, 2)));
```

### Quick cURL Test

```bash
# Get Royal XXI Surabaya schedule
curl -s "https://m.21cineplex.com/gui.schedule.php?sid=&find_by=1&cinema_id=SBYROYA&movie_id=" \
  -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)" \
  | grep -oE '<a [^>]*div_schedule[^>]*>[^<]+</a>' \
  | sed 's/<[^>]*>//g'
```

---

## 📋 Rekomendasi Solusi Terbaik

**Gunakan `m.21cineplex.com` mobile site scraping** — ini yang terbaik karena:

1. ✅ **No CAPTCHA** — plain HTML dari PHP server
2. ✅ **No JavaScript required** — bisa pakai `requests` / `curl` biasa
3. ✅ **No anti-bot** — User-Agent mobile iPhone cukup
4. ✅ **Gratis** — tidak perlu API key
5. ✅ **Real-time** — data fresh dari server
6. ✅ **Reliable** — 2 GitHub repos sudah validasi approach ini

**Catatan penting:**
- Cinema ID RLPLSB itu **salah** — format yang benar adalah `SBYROYA`
- Pattern cinema_id: `{CITY_ABBR}{THEATER_CODE}` (SBY = Surabaya)
- Untuk discover cinema_id baru: scrape `/gui.list_theater.php?sid=&city_id=12`

---

## 📱 WhatsApp Output Template

WhatsApp gak support monospace alignment / tabel. Format terbaik:

```
🎬 *{Nama Bioskop} — {Tanggal}*

🎥 *{Film 1}* — {jam} · {jam} · {jam}
🎥 *{Film 2}* — {jam} · {jam}
🎥 *{Film 3}* — {jam}
🎥 *{Film 4}* · *{Film 5}* · *{Film 6}*

💰 Regular {harga}K · Premiere {harga}K
```

**Rules:**
- Judul film di-bold (`*...*`)
- Jam dipisah titik tengah (`·`) bukan pipe (`|`)
- Film tanpa jam spesifik digabung 1 baris
- Gak usah pake code block / monospace — berantakan di WA
- Keep it short, gak perlu genre/durasi kecuali diminta

## 🔗 Referensi

- GitHub: `heirro/21cineplex-api` (10 stars, JS/Express)
- GitHub: `tfkhdyt/21cineplex-api` (7 stars, NestJS/TypeScript/Cheerio)
- Mobile site: `https://m.21cineplex.com`
- City IDs: JAKARTA=10, SURABAYA=12, BANDUNG=2, SEMARANG=14, YOGYAKARTA=23, BALI=9, MEDAN=17
