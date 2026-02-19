# Docker Multi-Agent Architecture: Multi-Instance AI Agent Systems

**Date:** 2026-02-19  
**Tags:** #docker #multi-agent #ai-agents #orchestration #isolation #kimi-k2 #gemini-flash #openclaw #iris  
**Sources:** Docker Docs, Northflank, DEV.to, IBM, Speakeasy, Collabnix, Moonshot AI (VentureBeat), Medium, arXiv  
**Use Case:** Multiple OpenClaw worker agents in Docker containers, coordinated by Iris on Mac mini M4

---

## 📋 TL;DR

**Pattern yang direkomendasikan untuk Zuma's use case:**

> **Supervisor/Orchestrator + Container-per-Worker via Docker Compose**  
> Iris (main agent) mengorkestrasi N worker containers melalui HTTP REST API atau Redis message queue.  
> Setiap worker = 1 Docker container = 1 OpenClaw instance dengan LLM murah (Kimi K2.5 / Gemini Flash).  
> Resources dikontrol per-container (`--cpus`, `--memory`). API keys diisolasi per-environment.

---

## 🏗️ Architecture Patterns yang Terbukti (Production-Ready)

### Pattern 1: Supervisor-Worker (⭐ Recommended untuk Iris)

```
┌─────────────────────────────────────────┐
│           Mac mini M4 Host              │
│                                         │
│  ┌──────────────────────────────────┐   │
│  │    Iris (Orchestrator)           │   │
│  │    [OpenClaw container / native] │   │
│  │    Model: Claude Sonnet          │   │
│  └───┬──────────────────────────────┘   │
│      │ HTTP REST / Redis                │
│      ├──────────┬────────────┐          │
│      ▼          ▼            ▼          │
│  ┌────────┐ ┌────────┐ ┌────────┐      │
│  │Worker-1│ │Worker-2│ │Worker-N│      │
│  │Kimi K2.5│ │Gemini  │ │Flash  │      │
│  │port:8001│ │port:8002│ │:800N  │      │
│  └────────┘ └────────┘ └────────┘      │
│                                         │
│  [Shared: Redis, PostgreSQL, volumes]   │
└─────────────────────────────────────────┘
```

**Karakteristik:**
- Iris sebagai supervisor agent: task decomposition → assignment → aggregation
- Worker agents bersifat stateless, menerima task via HTTP/queue, return result
- Setiap worker container isolated: env vars, API keys, filesystem, network
- Docker Compose mengatur seluruh stack di satu Mac mini

**Referensi:** Microsoft TaskWeaver, LangGraph supervisor pattern, OpenAI Swarm

---

### Pattern 2: Network/Peer-to-Peer (A2A Protocol)

```
┌──────────┐    A2A    ┌──────────┐
│  Agent-A │ ◄─────── │  Agent-B │
│ (Iris)   │ ──────► │ (Worker) │
└──────────┘  HTTP    └──────────┘
      │                    │
      └──────┬─────────────┘
          ┌──▼───┐
          │Agent-C│
          └───────┘
```

**Google's Agent2Agent (A2A) Protocol** (April 2025, sekarang di Linux Foundation):
- Open standard untuk inter-agent HTTP communication
- Agent Card (JSON): advertises capabilities, endpoint, auth requirements
- Supports: API key, OAuth 2.0, OpenID Connect
- Task lifecycle: submitted → working → input-required → completed/failed
- Sudah dipakai: Google ADK, LangGraph, CrewAI containers

**GitHub:** `github.com/a2aproject/A2A`  
**Compose example:** `github.com/docker/compose-for-agents/a2a/`

---

### Pattern 3: Event-Driven / Message Queue

```
Iris → [Redis/RabbitMQ Queue] → Worker-1
                              → Worker-2  
                              → Worker-N
Workers → [Result Queue] → Iris aggregator
```

**Best untuk:** Async tasks, variable load, worker bisa offline/restart
**Tools:** Redis Streams, RabbitMQ, BullMQ (Node.js), Celery (Python)

---

## 🐳 Docker Compose untuk Multi-Agent

### Minimal Docker Compose Template

```yaml
# docker-compose.yml — Multi-OpenClaw Worker Setup
version: '3.8'

services:
  # ── Shared Infrastructure ──────────────────────────
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
    volumes: [redis-data:/data]
  
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: agents
      POSTGRES_USER: agent_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes: [pg-data:/var/lib/postgresql/data]

  # ── Worker Agents ──────────────────────────────────
  worker-1:
    build: ./openclaw-worker
    container_name: worker-1
    ports: ["8001:8000"]
    environment:
      - AGENT_NAME=worker-1
      - LLM_PROVIDER=moonshot      # Kimi K2.5
      - LLM_MODEL=kimi-k2.5-turbo
      - MOONSHOT_API_KEY=${WORKER1_MOONSHOT_KEY}
      - REDIS_URL=redis://redis:6379
      - WORKER_ROLE=research
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.25'
          memory: 256M
    restart: unless-stopped

  worker-2:
    build: ./openclaw-worker
    container_name: worker-2
    ports: ["8002:8000"]
    environment:
      - AGENT_NAME=worker-2
      - LLM_PROVIDER=google
      - LLM_MODEL=gemini-2.5-flash
      - GOOGLE_API_KEY=${WORKER2_GOOGLE_KEY}
      - REDIS_URL=redis://redis:6379
      - WORKER_ROLE=writing
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
    restart: unless-stopped

  worker-3:
    build: ./openclaw-worker
    container_name: worker-3
    ports: ["8003:8000"]
    environment:
      - AGENT_NAME=worker-3
      - LLM_PROVIDER=google
      - LLM_MODEL=gemini-2.5-flash
      - GOOGLE_API_KEY=${WORKER3_GOOGLE_KEY}  # Key terpisah!
      - REDIS_URL=redis://redis:6379
      - WORKER_ROLE=analysis
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
    restart: unless-stopped

volumes:
  redis-data:
  pg-data:

networks:
  default:
    name: agent-network
```

**Keunggulan setup ini:**
- Setiap worker punya **API key terpisah** → rate limit per-key, bukan shared
- Resource limits mencegah 1 worker memonopoli Mac mini M4 resources
- Workers bisa restart independen tanpa mempengaruhi Iris
- Docker network internal → workers tidak bisa diakses dari luar host

---

## 🔌 Communication Patterns: Orchestrator ↔ Workers

### Option A: REST HTTP (Simplest, Recommended untuk Start)

```python
# Worker exposes FastAPI endpoint
# worker/main.py
from fastapi import FastAPI
app = FastAPI()

@app.post("/task")
async def handle_task(task: TaskRequest) -> TaskResult:
    result = await run_llm_task(task)
    return result

@app.get("/status")
async def health():
    return {"status": "ready", "model": MODEL_NAME}
```

```python
# Iris calls workers
import httpx

async def delegate_to_worker(worker_url: str, task: dict):
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(f"{worker_url}/task", json=task)
        return resp.json()

# Docker internal DNS resolves by service name
await delegate_to_worker("http://worker-1:8000", {...})
```

**Pros:** Simple, familiar, easy to debug  
**Cons:** Synchronous (caller blocks), no retry built-in

---

### Option B: Redis Queue (Async, Production-Grade)

```python
# Iris enqueues tasks
import redis.asyncio as redis
r = await redis.from_url("redis://redis:6379")

await r.xadd("tasks:research", {
    "task_id": "t123",
    "role": "research",
    "payload": json.dumps(task_data),
    "assigned_worker": "worker-1"
})

# Worker consumes from queue
entries = await r.xread({"tasks:research": "$"}, block=5000)
for stream, messages in entries:
    for msg_id, data in messages:
        result = await process_task(data)
        await r.xadd("results", {"task_id": data["task_id"], "result": result})
```

**Pros:** Async, workers can scale up/down, built-in retry, persistent  
**Cons:** More infrastructure, harder to debug

---

### Option C: Google A2A Protocol (Future-Proof)

Setiap worker expose HTTP endpoint dengan **Agent Card** di `/.well-known/agent.json`:

```json
{
  "name": "research-worker-1",
  "description": "Research agent using Kimi K2.5",
  "version": "1.0.0",
  "url": "http://worker-1:8000",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false
  },
  "skills": [
    {
      "id": "web-research",
      "name": "Web Research",
      "description": "Research topics from the web"
    }
  ],
  "authentication": {
    "schemes": ["Bearer"]
  }
}
```

**Pros:** Interoperability dengan framework lain (CrewAI, LangGraph, ADK), standar terbuka  
**Cons:** Overhead protokol, lebih kompleks untuk setup awal

---

## ⚖️ Trade-offs: Docker vs venv vs Process Isolation

| Dimensi | **Docker Container** | **Python venv** | **OS Process** |
|---------|---------------------|-----------------|----------------|
| **Isolation** | ✅ Full (filesystem, network, env) | ⚠️ Partial (Python packages only) | ❌ Shared host state |
| **Security** | ✅ Namespaces + cgroups | ❌ Same user, same FS | ❌ Same user |
| **Resource Control** | ✅ Hard CPU/memory limits | ❌ None | ⚠️ OS-level priority only |
| **API Key Isolation** | ✅ Per-container env vars | ⚠️ Need careful management | ❌ Shared env |
| **Rate Limit Isolation** | ✅ Different keys per container | ⚠️ Requires different key per venv | ❌ Hard to separate |
| **Startup Time** | ⚠️ ~500ms-2s | ✅ Instant | ✅ Instant |
| **Memory Overhead** | ⚠️ +50-100MB per container | ✅ Minimal | ✅ Minimal |
| **Reproducibility** | ✅ Identical across machines | ⚠️ OS-dependent | ❌ |
| **Restart/Crash Recovery** | ✅ `restart: unless-stopped` | ❌ Manual | ❌ Manual |
| **Deployment** | ✅ Docker Hub / compose | ⚠️ Script-based | ❌ Manual |
| **Debugging** | ⚠️ `docker logs`, `exec -it` | ✅ Direct | ✅ Direct |
| **Mac mini M4 Fit** | ✅ Good | ✅ Good | ✅ Good |

**Verdict untuk Zuma's use case:**
> Docker adalah pilihan terbaik untuk **production multi-agent** karena:
> 1. Isolasi API keys → setiap worker agent bisa punya Gemini/Kimi key sendiri → rate limit tidak shared
> 2. Resource guarantee → Mac mini M4 (16-32GB RAM) dibagi adil antar workers
> 3. Independent restart → worker crash tidak crash Iris
> 4. Reproducible → mudah deploy ulang atau tambah worker baru

---

## 🔒 Security Hardening per Container

Docker containers (default runc) share host kernel — cukup untuk trusted code, tapi perlu hardening flags:

```bash
# Hardened worker container command
docker run -d \
  --name worker-1 \
  --read-only \                          # Root FS read-only
  --tmpfs /tmp:rw,size=256m \            # Writable /tmp di RAM
  --cap-drop ALL \                        # Drop semua kernel capabilities
  --security-opt no-new-privileges \     # No privilege escalation
  --pids-limit 256 \                     # Limit child processes
  --memory 1g \                          # Hard memory limit
  --cpus 1.0 \                           # CPU limit
  --user 1000:1000 \                     # Non-root user
  --network agent-network \             # Dedicated network, no host
  -p 127.0.0.1:8001:8000 \             # Bind to localhost only!
  openclaw-worker:latest
```

**Isolation tiers untuk 2026:**

| Level | Technology | Boot Time | Best For |
|-------|-----------|-----------|----------|
| **Process** | Docker default runc | ms | Trusted code, internal workers |
| **Syscall** | gVisor (runsc) | ms | Multi-tenant, untrusted LLM code |
| **VM** | Firecracker / Kata | ~125-200ms | Production, untrusted code exec |

Untuk Zuma's workers (trusted code, internal use): **Docker default + hardening flags** cukup.

---

## 💰 Cost & Performance Considerations

### LLM Cost Comparison untuk Worker Agents

| Model | Input | Cached Input | Output | Best For |
|-------|-------|--------------|--------|----------|
| **Kimi K2.5 Turbo** | $0.60/M | $0.10/M | $3.00/M | Agentic tasks, coding, research |
| **Gemini 2.5 Flash** | ~$0.075/M | $0.018/M | ~$0.30/M | Fast turnaround, simple tasks |
| **Gemini 2.0 Flash** | $0.10/M | — | $0.40/M | Balanced |
| **Claude Sonnet 4** | $3/M | $0.30/M | $15/M | Iris orchestrator (high quality) |
| **Claude Haiku 3.5** | $0.80/M | $0.08/M | $4/M | Medium tasks |

**Strategi biaya optimal:**
- Iris (orchestrator): Claude Sonnet — perlu reasoning terbaik untuk task decomposition
- Workers (execution): Kimi K2.5 ($0.10/M cached) atau Gemini Flash ($0.018/M cached)
- Cached inputs sangat murah karena system prompts bisa di-cache

### Mac mini M4 Resource Allocation (16GB RAM)

```
Host OS + OpenClaw base:    ~2GB
Iris container:             ~1GB  
Worker-1 (Kimi):           ~512MB - 1GB
Worker-2 (Gemini Flash):   ~512MB - 1GB
Worker-3 (Gemini Flash):   ~512MB - 1GB
Redis:                     ~256MB
PostgreSQL:                ~512MB
──────────────────────────────────
Total:                     ~6-8GB (headroom 8-10GB untuk burst)
```

**Mac mini M4 dengan 16GB RAM bisa handle 3-5 workers nyaman.**  
**Mac mini M4 Pro dengan 24-32GB bisa handle 6-10 workers.**

### Performance: Kimi K2.5 Agent Swarm vs. Sequential

Berdasarkan Moonshot AI benchmarks:
- Single agent: baseline
- 4 parallel workers: ~3.2x faster
- Agent swarm (up to 100 sub-agents): **4.5x faster** dari single agent
- Parallel execution mengurangi wall-clock time drastically untuk research tasks

---

## 📦 Referensi GitHub Repos & Contoh Nyata

### Official Docker
- **`github.com/docker/compose-for-agents`** ⭐ — Official Docker repo, contoh untuk: CrewAI, LangGraph, A2A, Agno, Spring AI, Vercel AI, MinionsLM
- **`docker.com/blog/docker-mcp-ai-agent-developer-setup`** — MCP Gateway dengan Docker Compose

### Multi-Agent Frameworks (Docker-ready)
- **CrewAI** — `github.com/crewAIInc/crewAI` — Production-ready, ada subfolder di compose-for-agents
- **LangGraph** — Supervisor pattern, graph-based, ada di compose-for-agents
- **AutoGen (Microsoft)** — Conversational multi-agent, Docker examples tersedia
- **Swarms** — `github.com/kyegomez/swarms` — Enterprise multi-agent, director→worker pattern
- **A2A Protocol** — `github.com/a2aproject/A2A` — Google's open standard, Docker Compose examples

### Academic/Production
- **arXiv 2511.15755** — "Multi-Agent LLM Orchestration for Incident Response" — semua code + Docker configs public
- **arXiv 2502.13681** — "Repo2Run: LLM Agent in Isolated Docker Container" — pola isolasi LLM agent

---

## 🎯 Key Insights untuk Zuma / Iris / OpenClaw

### 1. Iris sebagai A2A-Compatible Supervisor
Iris bisa implement A2A protocol sebagai **client agent**, dengan workers sebagai **remote agents**. Ini future-proof karena A2A sekarang jadi Linux Foundation standard. Worker cards bisa berisi: model yang dipakai, role, rate limits, endpoint.

### 2. API Key per Worker = Rate Limit Independence
**Critical insight:** Dengan Docker, setiap worker container bisa punya API key berbeda untuk LLM yang sama. Misalnya 3 Gemini Flash workers dengan 3 API keys berbeda → 3x effective rate limit → ~60 RPM per key × 3 = 180 RPM total. Ini sangat berguna untuk high-throughput tasks.

### 3. Worker Specialization Reduces Cost
```
Iris (Claude Sonnet) ──→ decomposes task
                    ──→ Worker-research (Kimi K2.5): web research, agentic browsing
                    ──→ Worker-writing  (Gemini Flash): draft/writing
                    ──→ Worker-analysis (Gemini Flash): data analysis, summarize
                    ←── aggregates results
```
Workers menggunakan cheap LLMs untuk bulk work. Iris hanya pakai Claude untuk orchestration logic.

### 4. Shared State via Redis
Workers bisa berkolaborasi tanpa direct communication:
- Redis sebagai **shared context store** (current task state, partial results)
- Workers bisa "read what other workers produced" tanpa coupling langsung
- Iris bisa monitor progress semua workers via Redis keys

### 5. Docker Compose File per "Project"
Pattern yang bagus:
```
/workspace/projects/
  project-a/
    docker-compose.yml  (iris + workers untuk project ini)
    .env                (API keys)
  project-b/
    docker-compose.yml
```
Setiap project punya worker pool sendiri, bisa distart/stop independen.

### 6. Kimi K2.5 Built-in Agent Swarm
Kimi K2.5 sudah punya **built-in swarm** (sampai 100 sub-agents, 1500 tool calls). Ini artinya satu worker container yang pakai Kimi K2.5 sudah secara internal multi-agent. Untuk Zuma's use case:
- Worker-1 = Kimi K2.5 container → internally can spawn sub-agents
- Iris tidak perlu micro-manage Kimi; cukup assign high-level task

### 7. Docker MCP Gateway (Nov 2025)
Docker sendiri sekarang punya MCP Gateway yang bisa connect LLM agents ke tools via standard protocol. Available di Docker Compose sebagai service. Relevant untuk OpenClaw jika ingin expose tools ke workers.

### 8. Resource Limits Penting di Mac mini Shared Host
```yaml
# Pastikan selalu set limits untuk setiap worker!
deploy:
  resources:
    limits:
      cpus: '1.0'    # Max 1 core
      memory: 1G     # Max 1GB RAM  
    reservations:
      cpus: '0.1'    # Guaranteed 0.1 core
      memory: 256M   # Guaranteed 256MB
```
Tanpa limits, 1 worker yang busy bisa starve yang lain.

---

## 🚀 Implementation Roadmap untuk OpenClaw Multi-Worker

### Phase 1: Proof of Concept (1-2 hari)
1. Buat Dockerfile untuk OpenClaw worker (slim, tanpa UI)
2. Expose REST endpoint: `POST /task`, `GET /status`
3. Test 2 workers + Redis di Docker Compose
4. Iris calls worker via HTTP

### Phase 2: Production-Ready (1 minggu)
1. Implement A2A protocol di workers (Agent Card JSON)
2. Add Redis queue untuk async tasks
3. Add observability: Prometheus metrics, structured logging
4. Resource limits tuning di Mac mini M4

### Phase 3: Scale & Optimize (ongoing)
1. Dynamic worker spawning (Iris bisa `docker compose scale worker=N`)
2. Worker specialization by task type
3. Cost tracking per worker per task
4. Health checks + auto-restart

---

## 📚 Additional Resources

- **Docker Blog (Nov 2025):** "Docker Brings Compose to the AI Agent Era" — agentic Compose features
- **Docker Blog (Jan 2026):** "Docker Sandboxes: Run Claude Code and Other Agents Safely" — microVM sandboxes
- **Docker 3Cs Framework:** Containment, Capabilities, Context — AI agent security framework
- **Northflank Blog:** "How to Sandbox AI Agents in 2026" — MicroVMs vs gVisor vs Docker comparison table
- **IBM:** "What is A2A Protocol" — comprehensive A2A explanation

---

*Research compiled: 2026-02-19 by Hermes (subagent) for Iris 🌸*  
*Context: Zuma / OpenClaw platform / Mac mini M4 multi-worker architecture*
