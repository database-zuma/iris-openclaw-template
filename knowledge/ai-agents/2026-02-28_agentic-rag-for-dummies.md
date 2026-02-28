# Agentic RAG for Dummies — Modular RAG dengan LangGraph

**Date saved:** 2026-02-28  
**Source:** https://github.com/GiovanniPasq/agentic-rag-for-dummies  
**Tags:** #rag #agentic-rag #langgraph #vector-db #qdrant #hierarchical-indexing #conversation-memory #iris-reference  
**Stars:** 2.2k | **Forks:** 314 | **License:** MIT  
**Author:** GiovanniPasq  
**Notebook:** [Google Colab](https://colab.research.google.com/gist/GiovanniPasq/a74f077444ba21fc917dd8828bd92f23/agentic_rag_for_dummies.ipynb)

---

## Apa Ini

Tutorial + modular codebase untuk membangun **Agentic RAG** dengan LangGraph. Beda dari RAG tutorial biasa — ini agent-driven, dengan retrieval yang lebih smart: hierarchical indexing, conversation memory, query clarification, multi-agent parallel retrieval, self-correction.

**Dua cara pakai:**
1. **Learning** — Jupyter notebook step-by-step
2. **Building** — Modular project, swap komponen dengan 1 baris

---

## Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| **Hierarchical Indexing** | Small child chunks untuk precision search → fetch large parent chunks untuk context |
| **Conversation Memory** | Maintain context antar pertanyaan, summary-based |
| **Query Clarification** | Rewrite ambiguous queries + pause untuk tanya user kalau perlu |
| **Multi-Agent Map-Reduce** | Query kompleks dipecah → parallel sub-agents → agregasi |
| **Self-Correction** | Re-query otomatis kalau hasil pertama insufficient |
| **Context Compression** | Working memory tetap lean di long retrieval loops |

---

## Workflow

```
User Query
  → Conversation Summary (context dari history)
  → Query Rewriting (self-contained, disambiguate)
  → Query Clarification (tanya user kalau unclear)
  → Parallel Agent Reasoning (multi-agent map-reduce)
  → Aggregation
  → Final Response
```

**Contoh:** *"What is JavaScript? What is Python?"*
→ 2 parallel agents jalan bersamaan, masing-masing cari info sendiri → hasilnya digabung.

---

## Stack

```
Python 3.10+
LangGraph 1.0+          # Agent orchestration + graph
Qdrant                  # Vector DB (lokal, file-based)
HuggingFace Embeddings  # Dense: sentence-transformers/all-mpnet-base-v2
FastEmbedSparse (BM25)  # Sparse: Qdrant/bm25
pymupdf4llm             # PDF → Markdown converter
```

**LLM Provider-agnostic** — switch dengan 1 baris:
```python
# Lokal
llm = ChatOllama(model="qwen3:4b-instruct-2507-q4_K_M")
# Cloud
llm = ChatAnthropic(model="claude-sonnet-4-5-20250929")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm = ChatOpenAI(model="gpt-4o-mini")
```

---

## Hierarchical Indexing — Core Pattern

```
PDF → Markdown
  → Parent Chunks (by Markdown headers H1/H2/H3, 2000-4000 chars)
      → Child Chunks (500 chars, overlap 100)

Search: child chunks (precision)
Retrieve: parent chunks (context richness)
```

Parent chunks disimpan sebagai JSON files, child chunks di Qdrant vector store.

---

## Relevansi untuk Iris

**MEDIUM — reference architecture yang bagus.**

Pattern yang bisa diadopsi ke sistem kita:

1. **Hierarchical Indexing** — Iris vector memory kita saat ini flat. Parent/child pattern bisa improve recall quality untuk knowledge yang panjang (SKILL.md, laporan, dll)

2. **Query Clarification** — Iris sometimes langsung jawab query ambigu. Pattern "pause → tanya user kalau query unclear" → bisa di-adopt ke Iris communication skill

3. **Multi-Agent Map-Reduce** — Complex research queries bisa dipecah ke Argus sub-tasks paralel. Kita sudah punya konsepnya tapi belum formalized

4. **Context Compression** — Relevan untuk session memory Iris yang cepat besar. Compress retrieved context biar tidak redundant

**Yang TIDAK perlu di-implement dari sini:**
- LangGraph stack (kita pakai OpenClaw, beda ekosistem)
- Qdrant (kita pakai pgvector)
- pymupdf4llm (kita sudah punya markitdown)

**Action:** Baca notebook-nya kalau mau redesign Iris vector memory ke hierarchical indexing.
