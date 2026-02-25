# Security Audit Report - 2026-02-22

Berikut adalah hasil audit keamanan konfigurasi Iris:

1.  **API keys exposure**: ✅ OK
    *   Tidak ada API key, password, atau token yang ditemukan tersimpan secara plaintext di file-file workspace (SOUL.md, AGENTS.md, TOOLS.md, MEMORY.md, heartbeat/, memory/).
    *   Referensi API keys adalah dalam bentuk environment variables atau ditandai sebagai `__OPENCLAW_REDACTED__` di `openclaw.json`. File sensitif seperti `.env` sudah di-gitignore.

2.  **openclaw.json**: ⚠️ Warning
    *   API keys/tokens (Google, Brave Search, Telegram, Gateway) ditemukan tersimpan langsung di `openclaw.json` dalam format plaintext. Meskipun instruksi audit memungkinkan lokasi ini, praktik terbaik keamanan merekomendasikan penggunaan environment variables untuk kerahasiaan yang lebih baik.
    *   Tidak ada provider yang berlebihan atau tidak terpakai yang teridentifikasi.

3.  **Cron jobs**: ⚠️ Warning
    *   Dua cron jobs (`daily-usage-report` dan `Sync Stock Daily Retail → GSheet SO Rekonsiliasi`) secara konsisten gagal dalam proses `announce` delivery dengan error `cron announce delivery failed`. Ini perlu investigasi lebih lanjut.
    *   Semua cron jobs lainnya terlihat masuk akal dan berfungsi normal, dengan status `lastStatus: ok`.

4.  **Gateway**: ✅ OK
    *   Gateway dikonfirmasi hanya bind ke loopback (127.0.0.1) dan tidak ke 0.0.0.0, yang sesuai dengan konfigurasi yang aman untuk lingkungan lokal.

5.  **WhatsApp contact policy**: ✅ OK
    *   File `AGENTS.md` secara jelas mendefinisikan kebijakan kontak WhatsApp: hanya Wayan (+628983539659) untuk laporan teknis, dan Nisa untuk laporan pagi harian saja.
    *   File `SOUL.md` mendukung struktur kontrol akses yang mendukung kebijakan ini.

6.  **Session logs**: ✅ OK
    *   Pemindaian cepat log sesi utama terbaru (10 pesan terakhir) tidak menemukan aktivitas mencurigakan atau tool calls yang tidak biasa. (Catatan: Hanya sesi utama yang tersedia dalam output `sessions_list` untuk request ini).

---
**Rekomendasi:**
- Investigate dan perbaiki masalah `cron announce delivery failed` untuk dua cron jobs yang bermasalah.
- Pertimbangkan untuk memindahkan API keys/tokens yang saat ini ada di `openclaw.json` ke environment variables untuk meningkatkan keamanan, meskipun lokasi saat ini diizinkan oleh scope audit.
