# Stable Diffusion Web UI (AUTOMATIC1111) — The OG Local Image Gen Interface

**Source:** https://github.com/AUTOMATIC1111/stable-diffusion-webui
**Date:** Feb 2026
**Stars:** 161k ⭐ | **Forks:** 30.1k | **Contributors:** 586
**License:** AGPL-3.0
**Status:** ⚠️ Semi-abandoned — last commit Jul 2024, latest release v1.10.1 (Feb 2025)

## Apa Ini

Web interface untuk Stable Diffusion, built on Gradio. Dulu (2022–2024) ini THE standard tool untuk generate gambar AI secara lokal. Dikenal sebagai "A1111" (dari username creator). One-click install, form-based UI yang beginner-friendly, ekosistem extension masif.

## Key Points

### Core Features
- **txt2img + img2img** — generate dari text prompt atau transform existing image
- **Inpainting / Outpainting** — edit bagian tertentu dari gambar, extend canvas
- **Upscaling** — ESRGAN, RealESRGAN, SwinIR, LDSR (neural network upscalers)
- **Face restoration** — GFPGAN, CodeFormer
- **LoRA, Hypernetwork, Textual Inversion** — fine-tuning dan style transfer
- **Extension system** — ratusan community extensions (ControlNet, ADetailer, dll)
- **Checkpoint merger** — merge up to 3 models
- **Training tab** — train embeddings dan hypernetworks langsung dari UI
- **CLIP interrogator** — reverse-engineer prompt dari gambar
- **X/Y/Z plot** — compare parameter combinations visually
- **API mode** — full REST API via `--api` flag (Gradio-based, localhost:7860/sdapi/v1/)

### Hardware Requirements
- **GPU:** NVIDIA recommended (CUDA), AMD supported (ROCm), Apple Silicon (MPS)
- **VRAM:** Minimum 4GB (reports 2GB working), recommended 8GB+
- **Python:** 3.10 specifically (newer versions break torch compatibility)
- **OS:** Windows, Linux, macOS (Apple Silicon via MPS backend)
- **Disk:** ~10GB base + model files (2-7GB per checkpoint)

### Model Support
- Stable Diffusion 1.x, 2.0, 2.1
- SD3 (initial support, added Jun 2024)
- SDXL (via extensions/forks)
- Safetensors format supported
- **NOT supported natively:** Flux, newer architectures (need Forge/ComfyUI)

## Community Status (Feb 2026)

### ⚠️ Development Stalled
- **Last meaningful commit:** Jul 27, 2024 (1.5 years ago)
- **Last release:** v1.10.1 (Feb 9, 2025) — likely maintenance/bugfix only
- Creator AUTOMATIC1111 has effectively stopped active development
- 7,689 total commits, but activity flat since mid-2024

### Landscape Shift — A1111 Is Now Legacy
Community consensus per multiple comparison articles (Oct 2025 – Feb 2026):

| Tool | Role | Interface | Status |
|------|------|-----------|--------|
| **ComfyUI** | Industry standard for power users | Node-based (visual programming) | ✅ Active, rapid development |
| **Forge** (lllyasviel) | Improved A1111 fork | Form-based (same as A1111) | ✅ Active, better VRAM + newer models |
| **A1111** | Legacy / beginner entry point | Form-based (Gradio) | ⚠️ Stalled |
| **Fooocus** | Simplest option for beginners | Minimal GUI | ✅ Active |

**Key shifts:**
- **ComfyUI** dominates for: production workflows, video gen (LTX-2, Wan), Flux models, complex multi-model pipelines
- **Forge** preferred over A1111 for: same UI but better VRAM efficiency, SDXL/Flux support, actively maintained
- **A1111** still OK for: simple txt2img, beginners who want form-based UI, legacy extension compatibility

### API Integration
A1111 exposes full REST API saat dijalankan dengan `--api` flag:
```
GET  /sdapi/v1/txt2img
POST /sdapi/v1/txt2img
POST /sdapi/v1/img2img
GET  /sdapi/v1/sd-models
GET  /sdapi/v1/samplers
POST /sdapi/v1/interrogate
```
Bisa di-hit dari script/agent manapun via HTTP. ComfyUI juga punya API tapi format berbeda (workflow JSON).

## Relevance untuk Zuma / Iris

### Potential Use Cases
- **Product photography** — generate/enhance marketing images sandal/footwear
- **Social media content** — automated image gen for Instagram/Shopee listings
- **Background removal/replacement** — via inpainting
- **Upscaling** — enhance low-res product photos

### Practical Considerations
- **Hardware:** Mac Mini M2 bisa run via MPS backend tapi LAMBAT (no NVIDIA GPU). Kualitas OK tapi speed 10-30x lebih lambat dari dedicated NVIDIA GPU
- **Better alternatives for Zuma production:**
  - **API services** (DALL-E, Midjourney, Flux via API) — no local GPU needed, pay-per-use
  - Iris sudah punya `iris-openclaw-product-photo` skill untuk generate photo prompts
  - ComfyUI lebih future-proof kalau mau local setup
- **Jika mau local setup:** Install Forge (bukan A1111) — same UI, better performance, actively maintained

### Verdict
🟡 **Reference only.** A1111 adalah sejarah penting di AI image gen tapi sudah superseded. Kalau Zuma butuh local image gen di masa depan, gunakan **ComfyUI** (power) atau **Forge** (simplicity). Untuk production sekarang, API services (DALL-E/Flux) lebih practical tanpa butuh hardware GPU.

## Takeaways

1. **A1111 = pioneering tool yang define local AI image gen** — 161k stars, terbesar di kategorinya
2. **Tapi development stalled sejak Jul 2024** — creator effectively retired dari project
3. **ComfyUI sekarang industry standard** — node-based, lebih powerful, video gen support, aktif dikembangkan
4. **Forge = best of both worlds** kalau mau form-based UI — fork A1111 yang improved, actively maintained
5. **Untuk Zuma: API services >> local setup** — Mac Mini M2 tidak punya dedicated GPU, API services lebih cost-effective
6. **API mode berguna** — kalau suatu hari mau integrate image gen ke Iris pipeline, A1111/Forge/ComfyUI semua punya REST API

## Tags

#stable-diffusion #image-generation #ai-art #webui #gradio #automatic1111 #comfyui #forge #local-ai #product-photography #reference
