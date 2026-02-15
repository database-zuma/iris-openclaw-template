# Product Analysis Template (WhatsApp-Friendly)

**Source:** mart.sku_portfolio
**Use Cases:** Top N analysis, specific SKU requests, category performance
**Last Updated:** 2026-02-15

---

## Template Structure

### 1. SQL Query Pattern

```sql
SELECT 
  kodemix,
  gender,
  series,
  color,
  tier,
  current_year_qty AS cy_qty,
  last_year_qty AS ly_qty,
  var_year_qty AS yoy_growth_pct,
  ROUND(current_sales_mix, 2) AS sales_mix_pct,
  avg_last_3_months AS avg_3mo,
  stok_global AS stock,
  wh_total AS wh_stock,
  stok_toko AS store_stock,
  ROUND(to_total::numeric, 2) AS turnover_mo
FROM mart.sku_portfolio
WHERE current_year_qty > 0
ORDER BY current_year_qty DESC
LIMIT 10;
```

**Variations:**
- Top N: Change LIMIT
- Specific SKU: Add `WHERE kodemix = 'XXX'` or `WHERE series = 'XXX'`
- By gender: Add `WHERE gender = 'MEN'`
- By tier: Add `WHERE tier = '1'`
- Low turnover: `ORDER BY to_total DESC` (slow movers)
- High turnover: `ORDER BY to_total ASC` (fast movers, stockout risk)

---

## 2. WhatsApp Format (Compact & Readable)

### Header
```
📊 TOP 10 BEST-SELLING ARTICLES (2026 YTD)

🔢 Data: mart.sku_portfolio
📅 Period: Jan-Feb 2026 vs 2025
```

### Per-Article Format (One Block Per Article)

```
🥇 #1 - M1SP0PV201
👤 MEN | 🎨 STRIPE | BLACK BLUE RED | ⭐ T1

📈 Sales:
• 2026: 3,223 pairs (2.87% share)
• 2025: 24,732 pairs
• YoY: -87% ⚠️ (down 21,509)
• Avg 3mo: 1,894 pairs/month

📦 Stock & Turnover:
• Total: 402 pairs
  - WH: -1,465 ⚠️ (negative = unlabel/reject)
  - Toko: 1,681 pairs
• TO: 0.21 months 🔥 (FAST! selling 4.7x/month)

---
```

**Emoji Legend:**
- 👤 Gender
- 🎨 Series
- ⭐ Tier
- 📈 Sales trends
- 📦 Stock status
- 🔥 Fast turnover (<0.5 mo)
- 🐌 Slow turnover (>2.5 mo)
- ⚠️ Alert (negative stock, big drop)
- ✅ Healthy
- 💰 Revenue/sales mix

### Summary Section

```
🔍 KEY INSIGHTS

✅ Positives:
• All T1 premium tier (high margin)
• Top 10 = 16.5% total sales
• Healthy turnover 1-2 months (most)

⚠️ Concerns:
• Massive YoY decline -67% to -89%
  → Likely: Feb partial vs full 2025 year
• 7/10 articles have negative WH stock
  → Check unlabel category (reject/transit)

🎯 Action Items:
• STRIPE BLACK BLUE RED: Restock urgent (0.21mo TO)
• Review negative WH stock (data quality?)
• Monitor if YoY trend continues beyond Feb
```

---

## 3. Compact List Format (Top 10 Summary)

For quick overview without full details:

```
📊 TOP 10 ARTICLES (2026 YTD)

1️⃣ STRIPE BLACK BLUE RED (M) — 3,223 pairs | -87% YoY | 0.21mo TO 🔥
2️⃣ CLASSIC JET BLACK (M) — 2,221 | -87% | 1.85mo
3️⃣ BLACKSERIES COSMIC GREY (M) — 1,734 | -84% | 1.88mo
4️⃣ CLASSIC JET BLACK (L) — 1,460 | -89% | 0.75mo
5️⃣ BLACKSERIES PEANUT (M) — 1,403 | -79% | 1.52mo
6️⃣ BLACKSERIES STONE BLUE (M) — 1,311 | -83% | 1.28mo
7️⃣ DALLAS JET BLACK (M) — 1,301 | -89% | 2.49mo
8️⃣ CLASSIC METALIC GINGER (L) — 1,184 | -87% | 1.29mo
9️⃣ BLACKSERIES BROWN STONE (M) — 1,175 | -67% | 2.69mo 🐌
🔟 CLASSIC NAVY GREY (M) — 992 | -85% | 0.94mo

💡 Avg TO: 1.5 months | All T1 tier
```

---

## 4. Decision Tree: When to Use Each Format

**Full Detailed (One-Block-Per-Article):**
- When: User asks "show me analysis", "detail top 10"
- Audience: Wayan, Mbak Dewi (R&D), management
- Use case: Deep dive, decision making

**Compact List:**
- When: User asks "list top 10", "quick overview"
- Audience: Ops team, quick check
- Use case: Fast reference, daily check

**Single Article Deep Dive:**
- When: User asks "how's [article] doing?", "analyze [kodemix]"
- Format: Full block (sales + stock + insights) for ONE article
- Add: Monthly breakdown (now_jan_qty, now_feb_qty...) if requested

---

## 5. Common User Requests & Queries

### "Top 10 best sellers"
→ Use template above, ORDER BY current_year_qty DESC LIMIT 10

### "Top 10 worst performers"
→ ORDER BY current_year_qty ASC (or var_year_qty ASC for biggest drops)

### "Show me CLASSIC series performance"
→ WHERE series = 'CLASSIC' ORDER BY current_year_qty DESC

### "Articles with low stock"
→ WHERE stok_global / NULLIF(avg_last_3_months, 0) < 1 (less than 1 month coverage)

### "Fast movers (stockout risk)"
→ WHERE to_total < 0.5 ORDER BY to_total ASC

### "Slow movers (overstock)"
→ WHERE to_total > 3 ORDER BY to_total DESC

### "Negative warehouse stock (data quality check)"
→ WHERE wh_total < 0 ORDER BY wh_total ASC

### "Men vs Ladies top sellers"
→ Two separate queries with WHERE gender = 'MEN' / 'LADIES'

### "Tier performance"
→ GROUP BY tier, show aggregates (total qty, avg TO, etc.)

---

## 6. Alerts & Flags

Auto-flag these conditions in analysis:

- **🔥 Stockout Risk:** to_total < 0.5 months
- **🐌 Overstock:** to_total > 3 months
- **⚠️ Negative WH Stock:** wh_total < 0 (data quality issue)
- **📉 Big Drop:** var_year_qty < -70% (significant decline)
- **📈 Big Growth:** var_year_qty > 100% (doubled or more)
- **💰 High Share:** sales_mix_pct > 2% (significant contributor)

---

## 7. Response Flow

1. **Run Query** → Get data from mart.sku_portfolio
2. **Format** → Choose compact or detailed based on request
3. **Add Insights** → 3-5 bullet points (positives, concerns, actions)
4. **Emoji** → Use sparingly, only for clarity (not decoration)
5. **Keep Short** → WhatsApp = mobile reading, max 20-30 lines per message

---

## Notes

- **Always use mart.sku_portfolio** for SKU analysis (not raw tables)
- **Turnover (TO):** Months of coverage = stock / avg_monthly_sales. Lower = faster turnover.
- **Negative WH stock:** Usually unlabel category (reject, transit, consignment adjustments) — not a bug, just classification
- **YoY comparisons:** Be mindful of partial year (Feb 2026 vs full 2025) when interpreting variance
- **Sales mix %:** Contribution to total current year revenue (Rp basis)
