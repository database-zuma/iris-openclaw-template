# Open-Notebook — Research Notes

**Source**: https://github.com/lfnovo/open-notebook  
**Dibaca**: 2026-02-28  
**Versi**: v1.8.0 (dirilis Feb 27, 2026)  
**Status project**: Aktif — commit harian, 20K+ stars

---

## TL;DR

Self-hosted open-source alternative to Google NotebookLM. Ingest dokumen, audio, video, URL ke "notebook" yang terisolasi, lalu query via RAG, chat, atau structured AI transformation. Model-agnostic (15+ provider LLM), bisa fully local (Ollama + local TTS).

---

## Core Features

- **3 AI interaction modes**:
  - **Chat** — conversational, full-content context (pilih source mana yang visible)
  - **Ask** — RAG-based: auto-search semua source, retrieve relevant chunks, synthesize jawaban
  - **Transformations** — reusable prompt template yang diapply per-source → hasilkan structured notes (e.g., "extract methodology, findings, limitations")
- **Podcast generation** — research → multi-speaker audio dialogue, support OpenAI/Google/ElevenLabs/local TTS
- **Dual search** — BM25 keyword + vector semantic search (embeddings di SurrealDB)
- **Per-source context control** — Full Content / Summary Only / Not in Context
- **REST API** — 22 FastAPI routers, semua fitur accessible via HTTP
- **Docker-first** — single container atau multi-container compose
- **Multi-provider** — OpenAI, Anthropic, Gemini, Groq, Ollama, LM Studio, OpenRouter, Azure, Mistral, DeepSeek

---

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python 3.11–3.12, FastAPI, Uvicorn |
| AI Orchestration | LangChain + **LangGraph** (StateGraph-based agents) |
| Database | **SurrealDB** (graph DB + vector store sekaligus) |
| Embeddings | `esperanto` abstraction layer (multi-provider) |
| Content Extraction | `content-core` (PDF, audio, video, web) |
| Podcast | `podcast-creator` library |
| Frontend | TypeScript / React |
| Deployment | Docker, supervisord, Makefile |

---

## Architecture

```
Frontend (React/TS)
    │ REST API
FastAPI Backend (22 routers)
    │
open_notebook/ (core package)
  ├─ domain/         — data models (notebook, source, note, credential)
  ├─ graphs/         — LangGraph StateGraph agents (ask, chat, transformation, source)
  ├─ ai/             — model discovery, key provider, provisioning
  ├─ podcasts/       — async podcast generation
  ├─ database/       — repository.py → SurrealDB client
  └─ prompts/        — Jinja2 prompt templates
    │
SurrealDB
  └─ tables: notebook, source, note, chunk (+ vectors), chat_session, credential, podcast
  └─ relations: reference, artifact, refers_to
```

### Key architectural pattern — LangGraph multi-step agents

Setiap AI workflow (ask, chat, transformation) diimplementasi sebagai LangGraph StateGraph:

Contoh `ask.py` graph:
1. `agent` node — generate multi-search strategy (up to 5 parallel searches)
2. `provide_answer` nodes — parallel via `Send()`, masing-masing vector search + chunk synthesis
3. `write_final_answer` node — synthesize semua partial answers

Ini proper multi-step agentic pipeline, bukan single LLM call.

---

## Database: SurrealDB vs PostgreSQL

> ❌ **PostgreSQL tidak bisa dipakai** — SurrealDB hardcoded, tidak ada abstraction layer.

Sudah dikonfirmasi dari source code (`repository.py`) dan issue resmi [#372 — SurrealDB: Architecture Decision & Known Challenges](https://github.com/lfnovo/open-notebook/issues/372).

**Kenapa SurrealDB dipilih secara intentional:**
SurrealDB menggantikan *4 services sekaligus* dalam satu database:
```
Stack lama (tipikal):          Open-Notebook pakai SurrealDB:
├── PostgreSQL (data)          └── SurrealDB (does it all)
├── Redis (cache)                   ├── Data storage
├── Celery (background jobs)        ├── Background jobs (surreal-commands)
└── Vector DB (embeddings)          └── Vector embeddings
```

Ini architectural decision yang deliberate — bukan oversight. Tidak ada rencana PostgreSQL support.

**`repository.py` — hardcoded SurrealDB:**
- Import: `from surrealdb import AsyncSurreal, RecordID`
- Semua query pakai SurrealQL (bukan SQL standard)
- Connection via WebSocket (`ws://host/rpc:port`)
- Tidak ada interface/abstract class yang bisa di-swap

**Opsi kalau tetap mau deploy:**
- ✅ **Jalankan SurrealDB via Docker** (paling mudah, ~5 menit) — bukan ganti PostgreSQL, tapi *tambah* SurrealDB sebagai service baru
- ❌ Fork + refactor `repository.py` ke pgvector — effort sangat tinggi, tidak worth it

---

## Relevansi ke Iris/OpenClaw

**High relevance** — bisa jadi external knowledge management layer untuk Iris.

### Potential integration pattern

```
Iris (Orchestrator)
  └─→ Hermes (fetcher)     → POST /sources       (add URLs, PDFs, docs)
  └─→ Oracle (knowledge)   → POST /ask            (RAG query ke semua sources)
  └─→ Daedalus (processing)→ POST /transformations(structured extraction)
  └─→ Metis (analysis)     → GET /notes           (baca synthesized notes)
```

### Kelebihan
- REST API lengkap — bisa di-call langsung dari Iris sub-agents
- LangGraph internals — compatible dengan agent patterns yang sudah ada
- RAG-as-a-service — embed → chunk → vector search → synthesize, tanpa perlu build sendiri
- Multi-model registry — clean abstraction untuk manage multiple LLM providers
- Structured Transformations — ini yang paling berguna: prompt template → structured notes dari raw docs

### Pertimbangan
- SurrealDB = database baru di stack (existing: PostgreSQL)
- Belum ada MCP server native — perlu wrap REST API jadi Iris tools
- Single-user focus — multi-tenant perlu custom work
- Tidak dirancang sebagai headless agent tool — more of a user-facing research app

### Effort estimate untuk deployment
- Docker Compose + SurrealDB: ~30 menit setup
- Wrap REST API jadi Iris tools: ~2–4 jam
- Production hardening: depends

---

## Links
- GitHub: https://github.com/lfnovo/open-notebook
- Docs: https://open-notebook.ai (inferred)
- Stars: 20,299 | Forks: 2,298 | Issues: 114
- License: Check repo (kemungkinan MIT/Apache)
