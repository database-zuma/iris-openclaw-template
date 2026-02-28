# Qwen3.5-35B-A3B — Local Install Guide (Mac Mini M4 16GB)

**Date:** 2026-02-28  
**Tags:** #local-llm #qwen3 #gguf #lm-studio #ollama #mac-mini #apple-silicon #moe

---

## Model Overview

- **Full name:** Qwen3.5-35B-A3B
- **Released:** February 24, 2026 (Alibaba/Qwen Team)
- **Architecture:** Hybrid Gated DeltaNet + Sparse MoE (256 experts, 8 routed + 1 shared active)
- **Params:** 35B total, **3B active per token** (very efficient inference)
- **Context:** 262K native, 1M via YaRN
- **Multimodal:** text + image + video
- **Strengths:** Beats Qwen3-235B-A22B despite 6x fewer active params. Strong at reasoning, coding, tool use, agents, visual understanding.
- **Thinking mode:** ON by default (`<think>...</think>` before response). Can disable via `enable_thinking: false`.

---

## GGUF Quants Available (unsloth — Updated Feb 27, 2026)

Source: `unsloth/Qwen3.5-35B-A3B-GGUF` on HuggingFace  
> Note: GGUFs were refreshed Feb 27 with tool-calling fixes + improved coding performance.

| Quant | Size | Fits 16GB? |
|-------|------|-----------|
| UD-IQ2_XXS | 9.76 GB | ✅ Yes (too lossy) |
| **UD-Q2_K_XL** | **12.9 GB** | ✅ **Recommended for 16GB** |
| UD-IQ3_XXS | 14.1 GB | ✅ Tight (~2GB headroom) |
| UD-IQ3_S | 15.2 GB | ⚠️ Very tight |
| UD-Q3_K_M | 16.7 GB | ❌ |
| UD-Q3_K_XL | 17.2 GB | ❌ |
| UD-MXFP4_MOE | 19.5 GB | ❌ |
| UD-Q4_K_M | 19.9 GB | ❌ |
| UD-Q4_K_XL | 20.6 GB | ❌ |
| UD-Q5_K_XL | 24.9 GB | ❌ |
| UD-Q8_K_XL | 38.7 GB | ❌ |

**Sweet spot for Mac Mini M4 16GB:** `UD-Q2_K_XL` (12.9GB) — best quality that fits with headroom.

---

## LM Studio

Model is available: `qwen/qwen3.5-35b-a3b` on LM Studio Hub  
- Minimum system memory listed: **21 GB** (for Q4+ quants)  
- But lower quants (Q2/Q3 via unsloth) fit in 16GB  
- Search in LM Studio: `unsloth/Qwen3.5-35B-A3B-GGUF`

---

## Install via Ollama

```bash
# Recommended for 16GB (Q2_K_XL — 12.9GB)
ollama run hf.co/unsloth/Qwen3.5-35B-A3B-GGUF:UD-Q2_K_XL

# Better quality, tight fit (IQ3_XXS — 14.1GB)
ollama run hf.co/unsloth/Qwen3.5-35B-A3B-GGUF:UD-IQ3_XXS
```

---

## Key Notes

- **Thinking mode default ON** — adds `<think>` block before response. Disable with `enable_thinking: false` in chat template kwargs.
- **Hosted equivalent:** Qwen3.5-Flash (Alibaba Cloud Model Studio) = same model with 1M context default + built-in tools.
- **Unsloth Dynamic 2.0 quants** = superior accuracy vs standard GGUF quants — prefer `UD-` prefix variants.
- Model too new (Feb 24 release) — community support and integrations still maturing as of Feb 28.
