# Voicebox — Open-Source Voice Synthesis Studio

**Source:** GitHub Repository  
**Author:** Jamie Pine ([@jamiepine](https://github.com/jamiepine))  
**Date Fetched:** 2026-02-19  
**Link:** https://github.com/jamiepine/voicebox  
**Website:** https://voicebox.sh  
**Version:** v0.1.0 (latest at time of research)  
**License:** MIT

---

## Key Points

- **Apa itu:** Voicebox adalah *local-first voice cloning studio* open-source — alternatif gratis dan lokal untuk ElevenLabs. Clone suara dari beberapa detik audio, generate speech, dan buat proyek multi-suara, semua berjalan di mesin sendiri tanpa cloud.
- **Use case utama:** Voice assistant, podcast/video production pipelines, game dialogue systems, accessibility tools, content creation automation, dan integrasi API ke aplikasi custom.
- **Voice cloning instan:** Didukung Alibaba's **Qwen3-TTS** — model yang mampu voice cloning near-perfect dari beberapa detik audio sampel saja. Mendukung English, Chinese, dan akan ada lebih banyak bahasa.
- **REST API built-in:** Expose endpoint `/generate`, `/profiles` di `localhost:8000` — bisa langsung dipanggil dari aplikasi lain (OpenClaw, chatbot, automation pipeline, dll.) tanpa perlu integrasi model secara manual.
- **Super cepat di Apple Silicon:** MLX backend dengan Metal acceleration — **4-5x lebih cepat** dibanding PyTorch biasa. Mac Mini (Apple Silicon) adalah target hardware yang ideal.
- **Stories Editor (DAW-like):** Timeline multi-track untuk compose percakapan, podcast, narasi dengan multiple voice — mirip DAW (Digital Audio Workstation) tapi khusus TTS.
- **Privacy-first:** Semua model dan data suara tersimpan lokal. Tidak ada subscription, tidak ada cloud dependency, tidak ada limit.

---

## Technical Details

### Arsitektur

```
voicebox/
├── app/        # Shared React frontend (React + TypeScript + Tailwind)
├── tauri/      # Desktop app shell (Tauri + Rust)
├── web/        # Web deployment variant
├── backend/    # Python FastAPI server (inference engine)
├── landing/    # Marketing website
└── scripts/    # Build & release scripts
```

### Tech Stack

| Layer | Teknologi |
|-------|-----------|
| Desktop App | Tauri (Rust) — bukan Electron, 10x bundle lebih kecil |
| Frontend | React, TypeScript, Tailwind CSS |
| State Management | Zustand, React Query |
| Backend | FastAPI (Python) — async, auto OpenAPI schema |
| Voice Model | Qwen3-TTS (PyTorch atau MLX) |
| Transcription | Whisper (PyTorch atau MLX) |
| Inference Engine | **MLX** (Apple Silicon) / PyTorch (Windows/Linux/Intel) |
| Database | SQLite |
| Audio | WaveSurfer.js, librosa |

### Dependencies (Dev Setup)
- **Bun** (package manager JS)
- **Rust** + Cargo (untuk Tauri)
- **Python 3.11+** + pip (untuk backend FastAPI)
- **XCode** (khusus macOS)
- Model Qwen3-TTS didownload terpisah via app

### Cara Kerja
1. Backend FastAPI berjalan di `localhost:8000` — expose REST API untuk generate speech dan manage voice profiles
2. Frontend Tauri/React berkomunikasi dengan backend
3. Inference dilakukan lokal: MLX di Apple Silicon, PyTorch di platform lain
4. Voice profile dibuat dari audio sample (upload atau record in-app)
5. Whisper dipakai untuk transcription otomatis
6. SQLite menyimpan history, profiles, metadata

### API Endpoints (Core)

```bash
# Generate speech
POST http://localhost:8000/generate
Body: {"text": "...", "profile_id": "abc123", "language": "en"}

# List voice profiles
GET http://localhost:8000/profiles

# Create profile
POST http://localhost:8000/profiles
Body: {"name": "My Voice", "language": "en"}

# Full docs (saat running)
GET http://localhost:8000/docs
```

### Deployment Mode
- **Local mode:** Semua jalan di mesin yang sama
- **Remote mode:** Connect ke GPU server di jaringan yang sama
- **One-click server:** Jadikan mesin manapun sebagai Voicebox server

### Roadmap (Coming Soon)
- Real-time Synthesis (streaming audio word-by-word)
- Conversation Mode (multi-speaker auto turn-taking)
- Voice Effects (pitch shift, reverb)
- Timeline Editor dengan word-level precision
- More models: XTTS, Bark

---

## Relevansi untuk Zuma Indonesia / OpenClaw Setup

### ✅ Sangat Relevan — Berikut use case konkret:

1. **Voice Assistant untuk Iris/Hermes:** Voicebox REST API bisa dipanggil langsung oleh agent OpenClaw untuk TTS response suara. Iris bisa "berbicara" dengan suara yang dikloning dari voice sample spesifik — lebih personal dari TTS cloud biasa.

2. **Mac Mini Apple Silicon = Hardware Ideal:** Mac Mini `database-zuma` adalah Apple Silicon → langsung dapat manfaat MLX backend 4-5x lebih cepat. Ini berarti latensi TTS rendah, cocok untuk real-time response.

3. **Local API Integration:** FastAPI di `localhost:8000` mudah diintegrasikan ke pipeline OpenClaw yang sudah ada. Cukup HTTP POST — tidak perlu Python wrapper khusus.

4. **Privacy-first untuk Bisnis Zuma:** Suara customer service, demo produk, atau narasi konten bisa di-generate lokal tanpa data keluar ke cloud. Cocok untuk kebutuhan bisnis yang sensitif.

5. **Podcast/Konten Zuma Indonesia:** Stories Editor bisa dipakai untuk buat konten audio multi-speaker (misalnya simulasi percakapan sales, training material, video narasi produk).

6. **Transcription via Whisper:** Bisa dipakai untuk transkripsi meeting, rekaman, atau voice notes — satu stack untuk TTS + STT.

### ⚠️ Catatan:
- Masih v0.1.0 — baru release, mungkin ada bug atau fitur belum stabil
- Bahasa Indonesia belum eksplisit didukung (English + Chinese saat ini) — perlu test kualitas untuk Bahasa Indonesia
- Qwen3-TTS model size belum diketahui — perlu cek disk space requirement
- Linux build belum tersedia (blocked GitHub runner disk space) — jika butuh di server Linux, perlu wait atau build manual

---

## Takeaways

1. **Voicebox adalah ElevenLabs versi lokal open-source** — fitur lengkap, privacy-first, free forever.
2. **Mac Mini setup adalah sweet spot** — Apple Silicon + MLX = performa terbaik untuk inference lokal.
3. **REST API-first design** memudahkan integrasi ke OpenClaw tanpa friction — tinggal HTTP call.
4. **Mulai dengan `make setup && make dev`** untuk development, atau download binary untuk production use.
5. **Prioritaskan testing Bahasa Indonesia** — Qwen3-TTS belum eksplisit mention BI support, tapi model modern biasanya punya kemampuan multilingual yang cukup baik.
6. **Pantau roadmap** — Real-time synthesis dan Conversation Mode akan sangat berguna untuk voice assistant interaktif.

---

## Tags

`#tts` `#voice-cloning` `#voice-synthesis` `#local-ai` `#open-source` `#qwen3-tts` `#fastapi` `#tauri` `#rust` `#mlx` `#apple-silicon` `#voice-assistant` `#elevenlabs-alternative` `#mac-mini` `#openclaw-integration` `#dev-tools`
