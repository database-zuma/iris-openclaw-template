#!/usr/bin/env python3
"""Replace technical jargon with plain Indonesian in index.html"""

import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
with open('index.html.bak', 'w', encoding='utf-8') as f:
    f.write(content)

counts = {}

def rcount(pattern, replacement, text, desc, flags=0):
    new_text, n = re.subn(pattern, replacement, text, flags=flags)
    counts[desc] = counts.get(desc, 0) + n
    return new_text

# =========================================================
# 0. PROTECT: database table names containing "sku_"
#    Use placeholder tokens to shield them temporarily
# =========================================================
# Protect mart.sku_portfolio, core.sku_*, pairs_l12m etc.
content = content.replace('sku_portfolio', '§§SKU_PORTFOLIO§§')
content = content.replace('pairs_l12m', '§§PAIRS_L12M§§')

# =========================================================
# 1. BCG — first visible mention (in subtitle text) gets explanation
# =========================================================
# Title tag stays as-is (users don't see it), but first slide's text mention gets labeled
content = content.replace(
    'BCG Matrix · Product Lifecycle',
    'BCG Matrix — Peta Performa Produk · Siklus Hidup Produk',
    1
)
counts['BCG first-mention label'] = 1

# =========================================================
# 2. Compound MOS patterns — handle BEFORE standalone MOS
# =========================================================
content = rcount(r'HIGH-MOS ALERT', 'PERINGATAN STOK KRITIS', content, 'HIGH-MOS ALERT')
content = rcount(r'HIGH MOS ALERT', 'PERINGATAN STOK KRITIS', content, 'HIGH MOS ALERT')
content = rcount(r'Stars with High-MOS', 'Stars dengan Stok Berlebih', content, 'Stars with High-MOS')
content = rcount(r'High-MOS', 'Stok Kritis', content, 'High-MOS')
content = rcount(r'High MOS', 'Stok Kritis', content, 'High MOS')
content = rcount(r'high-MOS', 'stok kritis', content, 'high-MOS')
content = rcount(r'high MOS', 'stok kritis', content, 'high MOS')
content = rcount(r'HIGH MOS', 'STOK KRITIS', content, 'HIGH MOS')

# "⚠️MOS" → "⚠️Stok Berlebih"
content = rcount(r'⚠️MOS\b', '⚠️Stok Berlebih', content, '⚠️MOS')

# "MOS <number>mo" → "Sisa Stok <number> bulan"
content = rcount(r'MOS (\d+(?:\.\d+)?)mo\b', r'Sisa Stok \1 bulan', content, 'MOS Xmo')

# "MOS overstock" → "stok berlebih"
content = rcount(r'MOS overstock', 'stok berlebih', content, 'MOS overstock')

# "MOS <number>" → "Sisa Stok <number>"  (no unit follows, will be clear from context)
content = rcount(r'MOS (\d)', r'Sisa Stok \1', content, 'MOS <number>')

# Remaining standalone MOS
content = rcount(r'\bMOS\b', 'Sisa Stok (bulan)', content, 'MOS standalone')

# =========================================================
# 3. WoS — compound patterns first
# =========================================================
content = rcount(
    r'STOCK vs SALES PACE — WEEKS OF SUPPLY \(WoS\)',
    'Perbandingan Stok vs Laju Penjualan — Sisa Stok (minggu)',
    content, 'WoS header'
)
content = rcount(r'WEEKS OF SUPPLY \(WoS\)', 'Sisa Stok (minggu)', content, 'WEEKS OF SUPPLY (WoS)', re.IGNORECASE)
content = rcount(r'weeks of supply \(WoS\)', 'Sisa Stok (minggu)', content, 'weeks of supply (WoS)')
# In footnote: "WoS = stok_global ÷ ..." → keep formula but translate label
content = rcount(r'WoS = stok_global', 'Sisa Stok (minggu) = stok_global', content, 'WoS formula')
content = rcount(r'\bWoS\b', 'Sisa Stok (minggu)', content, 'WoS standalone')

# =========================================================
# 4. L12M → "12 Bulan Terakhir"
# =========================================================
content = rcount(r'\bL12M\b', '12 Bulan Terakhir', content, 'L12M')

# =========================================================
# 5. ASP → "Harga Rata-rata"
# =========================================================
content = rcount(r'\bASP\b', 'Harga Rata-rata', content, 'ASP')

# =========================================================
# 6. vel/velocity → "Kecepatan Jual"
# =========================================================
# "vel <number>" patterns
content = rcount(r'\bvel ([0-9])', r'Kecepatan Jual \1', content, 'vel <number>')
# "vel &lt;" (HTML encoded <)
content = rcount(r'\bvel &lt;', 'Kecepatan Jual &lt;', content, 'vel &lt;')
# "vel <" (raw less-than)
content = rcount(r'\bvel <', 'Kecepatan Jual <', content, 'vel <')
# Remaining standalone vel
content = rcount(r'\bvel\b', 'Kecepatan Jual', content, 'vel standalone')

# velocity / Velocity / Sales Velocity
content = rcount(r'Sales Velocity', 'Kecepatan Jual', content, 'Sales Velocity')
content = rcount(r'Sales velocity', 'Kecepatan Jual', content, 'Sales velocity')
content = rcount(r'sales velocity', 'Kecepatan Jual', content, 'sales velocity')
content = rcount(r'Velocity-based', 'Berbasis Kecepatan Jual', content, 'Velocity-based')
content = rcount(r'velocity-based', 'berbasis Kecepatan Jual', content, 'velocity-based')
content = rcount(r'[Vv]elocity framework', 'framework Kecepatan Jual', content, 'velocity framework')
content = rcount(r'\bVelocity\b', 'Kecepatan Jual', content, 'Velocity')
content = rcount(r'\bvelocity\b', 'Kecepatan Jual', content, 'velocity')

# =========================================================
# 7. SKU / SKUs — protect database "sku_portfolio" first (already done above)
# =========================================================
content = rcount(r'\bSKUs\b', 'artikel', content, 'SKUs')
content = rcount(r'/SKU\b', '/artikel', content, '/SKU')
content = rcount(r'\bSKU\b', 'artikel', content, 'SKU')

# =========================================================
# 8. PLC → "Siklus Hidup Produk"
# =========================================================
content = rcount(r'\bPLC\b', 'Siklus Hidup Produk', content, 'PLC')

# =========================================================
# 9. Q-Marks / Q-Mark → "Produk Potensial"
# =========================================================
content = rcount(r'Q-Marks', 'Produk Potensial', content, 'Q-Marks')
content = rcount(r'Q-Mark', 'Produk Potensial', content, 'Q-Mark')

# =========================================================
# 10. T1-3 / standalone T1/T2/T3
# =========================================================
content = rcount(r'\bT1-3\b', 'Tier 1-3', content, 'T1-3')
content = rcount(r'\bT1\b', 'Tier 1', content, 'T1')
content = rcount(r'\bT2\b', 'Tier 2', content, 'T2')
content = rcount(r'\bT3\b', 'Tier 3', content, 'T3')

# =========================================================
# 11. Other jargon cleanup
# =========================================================
# "Check velocity" → "Cek Kecepatan Jual" (already handled by velocity above... but let's be explicit)
# "v = velocity ratio" in footnote → already handled

# "rationalization" → "pemangkasan"
content = rcount(r'SKU rationalization', 'pemangkasan artikel', content, 'SKU rationalization')
content = rcount(r'rationalization', 'pemangkasan', content, 'rationalization')

# "Wkly Rate" → "Laju Mingguan"
content = rcount(r'Wkly Rate', 'Laju Mingguan', content, 'Wkly Rate')

# =========================================================
# 12. Restore protected tokens
# =========================================================
content = content.replace('§§SKU_PORTFOLIO§§', 'sku_portfolio')
content = content.replace('§§PAIRS_L12M§§', 'pairs_l12m')

# =========================================================
# Write back
# =========================================================
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n=== Replacement Summary ===")
total = 0
for desc, n in sorted(counts.items()):
    if n > 0:
        print(f"  {desc}: {n}")
        total += n
print(f"\n  TOTAL REPLACEMENTS: {total}")
