# Known Bugs & Solutions

> Moved from MEMORY.md (2026-02-19). Reference: `MEMORY.md § Reference Docs`

---

## FF/FA/FS Size Key Mismatch (Fixed 2026-02-18)

**Symptom:** FF=0% untuk banyak stores padahal stock ada di DB.

**Root cause:** Planogram columns pakai paired sizes (`size_36_37` → `"36/37"`), tapi stock di `core.stock_with_product` ada yang individual (`"37"` saja). Script `calculate_ff_fa_fs.py` cuma exact match → individual sizes gak pernah ke-match → FF=0.

**Fix:** Fallback lookup — kalau paired size (`"36/37"`) return 0, coba individual sizes (`"36"` + `"37"`):
```python
if stock_qty == 0 and "/" in stock_size:
    for part in stock_size.split("/"):
        individual_key = (db_lower, article_mix_lower, part.strip())
        stock_qty += stock.get(individual_key, 0)
```

**Script:** `/opt/openclaw/scripts/calculate_ff_fa_fs.py` line ~358

**Impact:** National avg FF jumped from 30% → 69% after fix.

---

## FF/FA/FS Store Name Mapping (Fixed 2026-02-18)

**Symptom:** FF=0% karena store name gak match antara planogram dan stock.

**Root cause:** `portal.store_name_map.stock_nama_gudang` case mismatch atau nama terpotong vs `core.stock_with_product.nama_gudang`.

**Fix:** UPDATE `portal.store_name_map` dengan exact nama_gudang dari stock table. Contoh: `Zuma Dalung` → `ZUMA Dalung`, `Zuma MOI` → `ZUMA MALL OF INDONESIA (MOI)`.

**Lesson:** Selalu verify exact string match (case-sensitive) antara mapping tables dan source tables.
