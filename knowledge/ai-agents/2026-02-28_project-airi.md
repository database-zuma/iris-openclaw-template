# Project AIRI — Self-Hosted AI Companion & VTuber (moeru-ai)

**Source:** https://github.com/moeru-ai/airi
**Repo:** https://github.com/moeru-ai/airi
**Date saved:** 2026-02-28
**License:** MIT
**Stars:** 2k+ ⭐
**Status:** NOT INSTALLED — reference/inspiration only

---

## What Is It

An **open-source, self-hosted AI companion** — think Neuro-sama but fully open and self-hostable. AIRI is a digital being that can talk, play games, and interact with people across multiple platforms simultaneously.

Core identity: a cute, self-aware AI character (💖🧸) with real-time voice conversations, game-playing ability, and multi-platform presence.

## Key Capabilities

- **Realtime voice chat** — speech recognition + ElevenLabs TTS, natural conversation flow
- **Game playing** — Minecraft (via Mineflayer), Factorio (via RCON), with autonomous decision-making
- **Multi-platform chat** — Telegram, Discord, and potentially more via modular connectors
- **Avatar support** — Live2D and VRM (3D) avatar rendering with expression/motion sync
- **Live streaming** — Can act as a VTuber with real-time avatar + voice + interaction
- **30+ LLM providers** — via `xsai` SDK: OpenAI, Claude, Gemini, DeepSeek, Qwen, Groq, Ollama, vLLM, etc.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Core runtime | Web-first (WebGPU, WebAudio, WebSocket, WASM) |
| Native desktop | Tauri (macOS, Windows) |
| Mobile | Capacitor (iOS) |
| AI backend | xsai (lightweight OpenAI-compatible AI SDK) |
| Speech | unspeech (universal ASR/TTS proxy) |
| Avatar | Live2D + VRM rendering |
| Games | Mineflayer (Minecraft), RCON (Factorio) |
| Database | Drizzle + DuckDB (via WASM) |

## Sub-Projects (Ecosystem)

| Project | Description |
|---------|-------------|
| **xsai** | Ultra-lightweight AI SDK (<1KB per module), OpenAI-compatible, supports 30+ providers |
| **unspeech** | Universal speech API proxy — unified interface to multiple ASR/TTS backends |
| **MCP Launcher** | Tool for launching MCP (Model Context Protocol) servers |
| **drizzle-duckdb-wasm** | DuckDB driver for Drizzle ORM running in WASM |
| **AIRI Factorio** | Autonomous Factorio gameplay agent |

## Architecture Highlights

- **Web-first philosophy** — runs in browser with WebGPU, WebAudio, WebSocket, WASM. No heavy native dependencies.
- **Also native** — Tauri for desktop (CUDA/Metal acceleration via `candle`), Capacitor for mobile
- **Modular** — Each capability (voice, games, chat platforms) is a separate module/package
- **Multi-agent capable** — Multiple AI characters can exist in the same world
- **PWA support** — Installable as Progressive Web App

## Platforms

- Web (PWA) — primary target
- macOS (Tauri)
- Windows (Tauri)
- iOS (Capacitor)

## Relevance for Iris / Zuma

**Reference + future use case base.**

### Planned Use Case: Iris Voice Avatar (to explore)

Visi: **Web app dimana user bisa ngobrol langsung sama Iris pakai suara, dengan animated avatar.**

Pipeline yang dibutuhkan:
1. **Avatar model** — Live2D (2D) atau VRM (3D) character Iris
2. **Voice input** — User ngomong → STT (Whisper / browser Web Speech API / unspeech)
3. **Iris brain** — Text masuk ke OpenClaw API → Iris proses → response text
4. **Voice output** — Response → TTS (ElevenLabs via `sag` / unspeech)
5. **Avatar sync** — Lip sync + ekspresi match ke audio output (Live2D SDK)
6. **Web frontend** — Next.js / Tauri app yang combine semua

Bottleneck utama: **latency** — voice conversation butuh <2 detik round-trip. Haiku 4.5 cukup cepat, tapi TTS + avatar rendering nambah delay.

AIRI bisa jadi base (avatar renderer + voice pipeline sudah ada), tapi conversation brain harus di-rewire ke OpenClaw API instead of direct LLM call. Effort: non-trivial.

**Simpler path:** Web app custom → mic → Whisper STT → OpenClaw API → ElevenLabs TTS → Live2D lip sync. Codex bisa build.

**Status:** Exploratory — Wayan akan explore lebih jauh kedepannya.

### Reference Value (existing)

1. **xsai SDK** — Ultra-lightweight AI SDK (<1KB/module). Alternative kalau butuh JS AI client lebih ringan dari OpenAI SDK.
2. **unspeech** — Universal ASR/TTS proxy. Unified API across ElevenLabs, Azure, Google TTS. Key piece untuk voice pipeline Iris.
3. **Multi-agent architecture** — AIRI's approach to multiple AI characters = reference untuk Iris multi-agent orchestration.
4. **Avatar rendering** — Live2D + VRM renderer in browser (WebGPU). Reference implementation untuk Iris avatar frontend.

## Key Takeaways

- **Open-source Neuro-sama** — proves a fully self-hosted AI companion with voice + avatar + games is achievable with MIT license
- **Web-first is viable** — WebGPU + WASM can handle AI inference, avatar rendering, and real-time audio without native dependencies
- **xsai is the star sub-project** — <1KB AI SDK supporting 30+ providers, could replace heavier SDKs in lightweight contexts
- **Active community** — seeking contributors, well-structured monorepo with clear module boundaries

---

**Tags:** #ai-companion #vtuber #open-source #self-hosted #voice-chat #live2d #xsai #multi-agent #games #neuro-sama #moeru-ai #mit-license #iris-avatar #voice-pipeline #future-project
