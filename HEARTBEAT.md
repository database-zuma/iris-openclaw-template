# HEARTBEAT.md — Active Task Tracker

**Heartbeat interval: 5 menit**

## ⚡ ATURAN HEARTBEAT (Wayan 2026-02-21 — Multi-User Per-File Tracking)

Mulai sekarang, task untuk multi-user **TIDAK** dicampur di file ini. Ini bisa menyebabkan race-condition jika banyak user me-request task bersamaan. 
Semua task yang sedang berjalan wajib disimpan di file individu dalam folder `heartbeat/` (misalnya: `heartbeat/+62812345678.md`).

Setiap heartbeat (saat kamu menerima pesan sistem untuk periodic check-in):

1. **JANGAN CEK FILE INI** untuk mencari daftar task.
2. **LIST FOLDER `heartbeat/`**: Cek apakah ada file `.md` di dalam folder `heartbeat/`.
3. **BACA SETIAP FILE**: Untuk setiap file yang ada, baca status task-nya.
   - Poll sub-agent (`session_status`) atau cek `outbox/` untuk nanobot.
   - Jika SELESAI: Deliver hasilnya via WA ke user yang bersangkutan (ambil nomor/nama grup dari nama file), lalu HAPUS/KOSONGKAN file heartbeat tersebut.
   - Jika MASIH JALAN: Beri update jika sudah terlalu lama.
4. **Penting**: JANGAN ngobrol ke WhatsApp jika semua sub-agent masih proses normal (jangan "halo aku lagi ngecek"). Cukup reply ke sistem `HEARTBEAT_OK`. Hanya chat user jika ada progress selesai atau error.

*(File ini sekarang hanya berisi instruksi cron-job, bukan daftar task aktif)*
