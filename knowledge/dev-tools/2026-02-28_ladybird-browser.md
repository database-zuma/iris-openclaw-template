# Ladybird — Browser Engine Baru dari Nol, Bukan Fork

**Source:** https://github.com/LadybirdBrowser/ladybird + https://ladybird.org
**Date:** Feb 2026
**Stars:** 60.6k ⭐ | **Forks:** 2.8k | **Contributors:** 1,240
**License:** BSD-2-Clause
**Status:** ✅ SANGAT AKTIF — last commit: Feb 28, 2026 (hari ini), 75,620 total commits
**Target:** Alpha 2026 (Linux & macOS)

## Apa Ini

Ladybird adalah web browser yang dibangun **dari nol** — bukan fork dari Chromium, WebKit, atau Gecko. Tidak ada satu baris pun kode dari browser existing yang dipakai. Dijalankan oleh nonprofit 501(c)(3), tanpa monetisasi user sama sekali.

Dimulai sebagai built-in browser di SerenityOS (hobby OS project by Andreas Kling), kemudian fork jadi project tersendiri pada **Jun 2024**. Co-founder: **Chris Wanstrath** (pendiri GitHub). Lead dev: **Andreas Kling**.

**Kenapa ini besar:** Saat ini, hampir semua browser di dunia cuma ada 3 engine family:
1. **Gecko** — Firefox (Mozilla)
2. **WebKit** — Safari (Apple) + asal-usul Blink
3. **Blink** — Chrome, Edge, Opera, Brave, Arc, dsb. (Google fork of WebKit)

Ladybird berpotensi jadi **engine ke-4 yang truly independent** pertama dalam >20 tahun.

## Key Points

### Architecture
Multi-process, mirip Chrome:
- **Main UI process** — handles user interface
- **WebContent process** (per tab) — renderer, sandboxed dari OS
- **ImageDecoder process** — decode images out-of-process (security isolation)
- **RequestServer process** — semua network requests terpusat

### Core Libraries (semua dibangun sendiri)
| Library | Fungsi |
|---------|--------|
| **LibWeb** | Web rendering engine (HTML, CSS, layout) |
| **LibJS** | JavaScript engine |
| **LibWasm** | WebAssembly implementation |
| **LibCrypto / LibTLS** | Cryptography + TLS |
| **LibHTTP** | HTTP/1.1 client |
| **LibGfx** | 2D graphics, image decoding |
| **LibUnicode** | Unicode + locale support |
| **LibMedia** | Audio + video playback |
| **LibCore** | Event loop, OS abstraction |
| **LibIPC** | Inter-process communication |

### Tech Stack
- **Primary:** C++ (58.8%), HTML (25.3%), JavaScript (12.4%)
- **Incoming:** Rust (2.0% dan terus naik — lihat breaking news di bawah)
- **Build:** CMake + vcpkg
- **Platforms:** Linux, macOS, Windows (WSL2), "many other *Nixes"

### Sponsorship & Funding
Non-profit 501(c)(3) — tidak ada search deals, tidak ada data monetization.

**Platinum sponsors:** FUTO, Shopify, Cloudflare
**Gold sponsors:** Proton VPN, Guillermo Rauch (CEO Vercel)
**Notable board members:** Mike Shaver (ex-Mozilla CTO), Tim Flynn

## 🔥 Breaking — Feb 2026: Ditching Swift, Adopting Rust (dengan AI)

Ini baru terjadi minggu lalu dan sangat signifikan:

**Feb 17, 2026:** Commit `Everywhere: Abandon Swift adoption`
> "After making no progress on this for a very long time, let's acknowledge it's not going anywhere and remove it from the codebase."

Swift adoption menyebabkan **~1 tahun delay** pada development. Sekarang diganti dengan Rust.

**Feb 24, 2026:** `LibJS: Add alternative source-to-bytecode pipeline in Rust`
- Complete Rust reimplementation of LibJS frontend: lexer, parser, AST, scope collector, bytecode generator
- Diintegrasikan via C FFI layer (Corrosion CMake-Cargo bridge)
- Runtime env vars: `LIBJS_CPP` (revert ke C++) atau `LIBJS_COMPARE_PIPELINES=1` (jalankan keduanya paralel untuk verifikasi)
- AI coding assistants dipakai untuk membantu translate C++ → Rust

**Feb 24, 2026:** Rust toolchain sekarang build dependency secara default (`ENABLE_RUST=ON`)

Artikel The Register (Feb 23, 2026): *"Indie web browser Ladybird flutters toward Rust with a little help from AI"*

## Status Saat Ini

- **Pre-alpha** — hanya cocok untuk developers, bukan daily driver
- **No releases** — nol release di GitHub, belum ada binary untuk umum
- Passing banyak web platform tests tapi masih banyak yang belum
- Fitur yang sudah ada: basic browsing, JavaScript (via LibJS), CSS layout, images, media playback, HTTPS
- Fitur yang belum: ekstensi/extensions, sync, mobile, banyak advanced web APIs
- Active Discord community, kontributor baru welcome

## Kenapa Ini Penting

1. **Browser monoculture problem** — 65%+ web traffic jalan di Blink (Chrome engine). Kalau Google break web, semua orang kena. Ladybird = diversification.
2. **No conflicts of interest** — Google Chrome ada konflik (search revenue), Firefox ~85% dari Google search deal. Ladybird tidak punya tuan.
3. **Standards-first approach** — implement dari spec, bukan dari reverse-engineering existing behavior
4. **Security via isolation** — setiap tab punya renderer process terpisah, image/network out-of-process
5. **Rust transition** — long-term memory safety yang lebih baik dari C++ tanpa runtime overhead

## Relevance untuk Zuma / Iris

Tidak ada use case langsung untuk Zuma operations. Ini **awareness/tracking** item:

- **Browser automation:** Ladybird sedang develop headless mode — bisa jadi alternatif Playwright di masa depan, tapi belum production-ready
- **Web standards tracking:** kalau Ladybird sukses, bisa affect web standards yang perlu Iris/Codex support
- **Technical inspiration:** multi-process sandboxing architecture relevan buat AI agent security isolation design
- **Rust adoption pattern:** cara mereka integrate Rust ke C++ codebase (FFI + parallel pipelines untuk verification) adalah pattern bagus untuk gradual Rust migration

**Verdict:** 🔵 Track & watch. Milestone besar: Alpha 2026. Jika Alpha release keluar dan headless mode tersedia, evaluate sebagai Playwright alternative.

## Takeaways

1. **Satu-satunya truly independent browser engine yang dibangun from scratch secara serius** — semua browser lain adalah fork dari Gecko/WebKit/Blink
2. **Sangat aktif** — 75,620 commits, commit hari ini (Feb 28, 2026), 1,240 contributors
3. **Big names backing it** — GitHub co-founder, Shopify, Cloudflare, Vercel CEO sebagai sponsor
4. **Swift → Rust pivot (Feb 2026)** — dengan AI assistance, significant engineering decision
5. **Pre-alpha, no ETA for stable** — Alpha target 2026, tapi browser development sangat kompleks
6. **Bukan untuk Zuma sekarang** — tapi worth tracking karena bisa jadi browser engine standard masa depan

## Tags

#browser #browser-engine #independent #open-source #rust #cpp #web-standards #serenityos #non-profit #multi-process #libweb #libjs #headless #track
