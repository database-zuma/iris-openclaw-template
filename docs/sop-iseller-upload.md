# SOP: Upload Data iSeller (GDrive to PostgreSQL)

Dokumen ini menjelaskan langkah-langkah teknis untuk melakukan update data raw iSeller dari Google Drive ke database PostgreSQL VPS Zuma.

## 📁 Lokasi File Sumber
- **Folder GDrive:** `1dS3M4E8PUwR1mlwnOj_hqCFRsyUVE6Qe` (iSeller 2026 Raw)
- **Tabel Tujuan:** `raw.iseller_2026` (Pastikan tabel sudah ada di schema `raw`)

## 🛠️ Langkah Kerja

### 1. Persiapan Environment
- Gunakan agent **Metis** (atau sub-agent OpenClaw yang memiliki akses SSH & DB).
- Workspace: `~/.openclaw/workspace/`
- Pastikan `.env` berisi `PGHOST`, `PGDATABASE`, `PGUSER`, dan `PGPASSWORD` sudah terkonfigurasi.

### 2. Download File dari GDrive
Gunakan `gog` CLI untuk mendownload file CSV ke folder temporary.
```bash
mkdir -p iseller_temp
/Users/database-zuma/homebrew/Cellar/gogcli/0.9.0/bin/gog drive download [FILE_ID] --out iseller_temp/[FILENAME].csv
```

### 3. Pembersihan Data (Python/Pandas)
iSeller raw data memerlukan **Forward Fill** pada kolom tanggal karena hanya baris pertama struk yang memiliki timestamp.
```python
import pandas as pd

# Load data
df = pd.read_csv('iseller_temp/filename.csv')

# Forward fill tanggal berdasarkan nomor struk (Order Number)
df['Order Date'] = df.groupby('Order Number')['Order Date'].ffill()

# Pastikan format tanggal sesuai untuk PostgreSQL
df['Order Date'] = pd.to_datetime(df['Order Date'])
```

### 4. Update Database
- **Truncate:** Hapus data lama di tabel target (misal: `raw.iseller_2026`).
- **Upload:** Gunakan `copy_expert` atau `to_sql` (Pandas) untuk kecepatan maksimal.

### 5. Verifikasi
Selalu lakukan pengecekan jumlah baris setelah upload:
```sql
SELECT count(*), min("Order Date"), max("Order Date") FROM raw.iseller_2026;
```

---

## ⚡ Jalur Cepat (Iris Prompt)
"Iris, tolong update data iSeller 2026. Ambil file Jan-Feb dari folder GDrive `1dS3M4E8PUwR1mlwnOj_hqCFRsyUVE6Qe`. Lakukan forward fill tanggal, truncate tabel `raw.iseller_2026`, lalu re-upload semua."

---
*Terakhir diupdate: 2026-02-23 oleh Iris*
