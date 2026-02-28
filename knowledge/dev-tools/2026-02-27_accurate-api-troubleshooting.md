# Accurate API Troubleshooting — Stock/Sales Pull Failures

**Date:** 2026-02-27
**Incident:** DDD stock pull 401 Unauthorized, token update, Accurate API downtime

---

## Symptom Mapping

| Symptom | Root Cause | Fix |
|---------|------------|-----|
| `401 Unauthorized` di cron log | Token expired/revoked di Accurate | Regenerate token di Accurate dashboard |
| `500 "Error or Invalid API Token"` dari curl | Accurate API down (bukan token issue) | Tunggu recover, test lagi |
| Script works, curl fails | Wrong auth header format in manual test | Pakai exact format dari script |
| Token "baru" tapi identik dengan lama | Token tidak di-delete dulu sebelum generate baru | Delete lama → Buat baru |

---

## Diagnosis Flow (Step-by-Step)

### Step 1 — Cek log cron dulu
```bash
ssh vps-db "cat /opt/openclaw/logs/stock_YYYYMMDD.log | grep -A5 'ERROR\|FAIL\|401\|500'"
```

### Step 2 — Isolasi: token issue atau API down?
Test entity LAIN yang harusnya jalan (misal UBB):
```bash
ssh vps-db "source /opt/openclaw/venv/bin/activate && cd /opt/openclaw/scripts && python3 pull_accurate_stock.py ubb --dry-run"
```
- Kalau UBB juga gagal → **Accurate API down** (tunggu, bukan masalah kita)
- Kalau UBB sukses tapi DDD gagal → **Token DDD bermasalah**

### Step 3 — Kalau token bermasalah: regenerate
1. Login accurate.id → entity yang bermasalah (e.g. DDD = Dream Dare Discover)
2. **Accurate Store → API Token**
3. **Hapus token lama dulu** (kalau tidak dihapus, "Buat API Token" akan blocked: *"API Token untuk aplikasi tersebut sudah ada"*)
4. Klik **Buat API Token** → copy token baru
5. Update di VPS: `ssh vps-db "sed -i 's/aat\\.NTA\\..*/<TOKEN_BARU>/' /opt/openclaw/scripts/.env.ddd"`

### Step 4 — Fix common VPS script issues
```bash
# Fix Windows CRLF line endings (kalau .env diedit dari Windows/Iris)
ssh vps-db "sed -i 's/\r//' /opt/openclaw/scripts/.env.ddd"

# Pastikan pakai venv yang benar (bukan system python3)
ssh vps-db "source /opt/openclaw/venv/bin/activate && python3 -c 'import pandas; print(ok)'"
```

### Step 5 — Manual trigger (bypass cron)
```bash
# Test API dulu sebelum run full
ssh vps-db "curl -s -o /dev/null -w '%{http_code}' -H 'Authorization: Bearer <TOKEN>' 'https://zeus.accurate.id/accurate/api/item/list.do?sp.page=1&sp.pageSize=1'"
# 200 = OK, 401 = token invalid, 500 = API down

# Run full pull
ssh vps-db "source /opt/openclaw/venv/bin/activate && cd /opt/openclaw/scripts && python3 pull_accurate_stock.py ddd > /tmp/ddd_stock_manual.log 2>&1 &"

# Monitor
ssh vps-db "tail -f /tmp/ddd_stock_manual.log"
```

---

## Key Gotchas

1. **Token lama harus dihapus dulu** di Accurate sebelum bisa generate baru
2. **Accurate API kadang down** (~06:00 WIB pernah terjadi) — kedua 401 dan 500 bisa muncul. Bedakan dengan test entity lain
3. **Selalu pakai venv**: `source /opt/openclaw/venv/bin/activate` — system python3 tidak punya pandas
4. **CRLF issue**: kalau .env diedit via tool yang tidak Linux-native, jalankan `sed -i 's/\r//' .env.ddd`
5. **Script butuh `entity` argument**: `python3 pull_accurate_stock.py ddd` (bukan tanpa argument)
6. **Stock + Sales DDD pakai .env yang sama**: update `.env.ddd` → fix keduanya sekaligus
7. **Mac Mini tidak punya script** — pull scripts hanya ada di VPS `/opt/openclaw/scripts/`

---

## Entity → Env File Mapping

| Entity | Env File | Accurate Account |
|--------|----------|-----------------|
| DDD (Dream Dare Discover) | `.env.ddd` | zeus.accurate.id, db 222277 |
| UBB | `.env.ubb` | zeus.accurate.id, db 739128 |
| MBB | `.env.mbb` | — |
| LJBB | `.env.ljbb` | — |

---

## Accurate API Health Check (quick)
```bash
# Cek apakah Accurate zeus server up
curl -s -o /dev/null -w '%{http_code}' https://zeus.accurate.id/accurate/api/item/list.do
# 401 = server up tapi butuh auth (NORMAL)
# 500 = server error / maintenance
# timeout = network issue
```

