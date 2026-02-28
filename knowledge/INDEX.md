# Knowledge Dump Index

Auto-generated index of saved links, articles, and threads.

## Recent Additions

- **2026-02-28** | [Clawbox — OpenClaw-Ready macOS VMs](dev-tools/2026-02-28_clawbox-macos-vm.md) | #openclaw #macos #vm #virtualization #tart #mutagen | Spin up isolated macOS VMs for OpenClaw via 2 commands. Standard mode (latest release) + Developer mode (bidirectional Mutagen sync). Max 2 VMs/host (Apple EULA). Playwright, Tailscale, signal-cli optional. Low priority for Iris (already on VPS).
- **2026-02-28** | [Awesome OpenClaw Use Cases — Community Collection](dev-tools/2026-02-28_awesome-openclaw-usecases.md) | #openclaw #use-cases #multi-agent #automation #community #iris-inspiration | 11k⭐ repo, 30 verified use cases. Key patterns: STATE.yaml subagent coordination, cron heartbeat as the real product, multi-agent team via Telegram, self-healing server, customer service 80% auto-handled. Security: TruffleHog pre-push + local Gitea staging (AI WILL hardcode secrets).
- **2026-02-28** | [OpenClaw Cost Optimization Playbook](dev-tools/2026-02-28_openclaw-cost-optimization-playbook.md) | #openclaw #cost-optimization #model-tiering #iris #llm-ops #qmd #ollama #openrouter | 65-70% cost reduction. 7 tactics: model tiering, QMD local search, session memory fix (50kb→8kb), thinking token trap, Ollama for repetitive tasks, Exa free search, OpenRouter auto-routing. Session memory fix URGENT for Iris (990k token issue).
- **2026-02-28** | [Qwen3.5-35B-A3B — Local Install Guide (Mac Mini M4 16GB)](dev-tools/2026-02-28_qwen35-35b-a3b-local-install.md) | #local-llm #qwen3 #gguf #lm-studio #ollama #mac-mini #moe | 35B total / 3B active params, released Feb 24 2026. Unsloth GGUFs refreshed Feb 27. Recommended for 16GB: UD-Q2_K_XL (12.9GB). LM Studio & Ollama install commands included.
- **2026-02-27** | [Public APIs — Curated for Zuma & Iris (Full Analysis)](dev-tools/2026-02-27_public-apis-zuma-relevant.md) | #public-apis #indonesia #payment-gateway #nlp #google-maps #email #notifications #finance | 268-line analysis: 60+ APIs filtered for Zuma retail ops & Iris AI. Tier-1: Google Maps, Sendinblue, NewsAPI, NLP Cloud (Indonesian support), Xendit/Midtrans. Critical: Sendgrid free tier ended Jul 2025, MercadoPago no IDR support.
- **2026-02-27** | [Public APIs — Verification & Action Items Summary](dev-tools/2026-02-27_public-apis-verification-summary.md) | #public-apis #verification #indonesia #payment-gateway #cors-analysis #action-items | Executive summary: payment gateway comparison (Xendit/Midtrans/Doku), CORS analysis (60% need backend proxy), critical findings & integration priority roadmap
- **2026-02-27** | [Iris Vector Memory + Reflection Cycle — Implementation](ai-agents/2026-02-27_iris-vector-memory-implementation.md) | #vector-memory #pgvector #semantic-search #reflection-cycle #iris-upgrade #implementation | IMPLEMENTED: pgvector semantic search over 438 memory+knowledge chunks (Gemini embeddings), daily reflection cycle at 22:00, scripts in workspace/scripts/
- **2026-02-27** | [AI Town — Autonomous Agent Town Simulator](ai-agents/2026-02-27_github_a16z-ai-town.md) | #multi-agent #autonomous-agents #simulation #memory-system #vector-search #a16z #generative-agents | Stanford-inspired multi-agent simulation: agents perceive→remember→reflect→act. Architecture patterns: vector memory retrieval, tick-based simulation, shared state, agent-to-agent communication. Reference for Iris memory/heartbeat evolution
- **2026-02-27** | [Scrapling — Adaptive Web Scraping Framework](dev-tools/2026-02-27_scrapling.md) | #web-scraping #anti-bot #cloudflare-bypass #adaptive #concurrent #mcp-server | Adaptive scraping (survive redesigns), 784x faster than BeautifulSoup, anti-bot Cloudflare Turnstile bypass, concurrent crawling, MCP-ready for AI agents
- **2026-02-27** | [Agent Browser — AI-Optimized Browser Automation](dev-tools/2026-02-27_agent-browser.md) | #browser-automation #ai-agents #rust #lightweight #token-efficiency #vercel-labs | Minimal context footprint (93% less vs Playwright), 95% first-try success, Rust CLI + Node.js daemon, purpose-built for AI agents
- **2026-02-25** | [World Monitor — Real-Time Global Intelligence Dashboard](dev-tools/2026-02-25_github_worldmonitor.md) | #osint #intelligence-dashboard #tauri #typescript #local-ai #open-source | Real-time geopolitical/news/financial dashboard — 100+ feeds, 3D globe, local LLM, native desktop (Tauri), AGPL
- **2026-02-25** | [Vibe Coding 2.0 — 18 Rules to Be the Top 1% Builder](dev-tools/2026-02-25_vibe-coding-2-rules.md) | #vibe-coding #mvp #ship-fast #nextjs #tailwind #shadcn #best-practices | 18 DO's & DON'Ts untuk build MVP cepat — inti: "tau apa yang TIDAK perlu dibangun", pakai tools yang ada, ship imperfect > polished never launched
- **2026-02-22** | [KittenTTS — Lightweight Open-Source Text-to-Speech](ai-agents/20260222_kittentts_tts_model.md) | #tts #open-source #lightweight #voice-generation #privacy #apache-2.0 | Ultra-lightweight TTS model (15M params, <25MB), 8 voices, CPU-only, perfect for Zuma automation
- **2026-02-21** | [Arscontexta — Skill Graphs > SKILL.md](ai-agents/2026-02-21_twitter_arscontexta-skill-graphs.md) | #skill-graphs #knowledge-management #claude-code-plugin #second-brain #agent-architecture | Claude Code plugin for generating knowledge systems; Skill Graphs = navigable markdown networks vs monolithic SKILL.md
- **2026-02-20** | [Gateway Pairing Issue Fix — Scope Mismatch](dev-tools/2026-02-20_gateway-pairing-fix.md) | #openclaw #gateway #pairing #troubleshooting #whatsapp #device-auth | Device scope mismatch (missing operator.read/write) → pairing required error; fix via device rotation + full scopes
- **2026-02-20** | [Multi-Agent Architecture — Production (Eos Live)](ai-agents/2026-02-20_multi-agent-architecture-production.md) | #multi-agent #nanobot #openclaw #architecture #production | Hybrid OpenClaw (Iris) + Nanobot (Eos) with filesystem bridge communication
- **2026-02-19** | [Botasaurus — All-in-One Web Scraping Framework](dev-tools/2026-02-19_github_botasaurus.md) | #web-scraping #python #anti-bot #cloudflare-bypass #automation | GitHub Research
- **2026-02-19** | [Voicebox — Open-Source Voice Synthesis Studio](dev-tools/2026-02-19_github_voicebox.md) | #tts #voice-cloning #local-ai #qwen3-tts #openclaw-integration #apple-silicon | GitHub research
- **2026-02-19** | [Docker Multi-Agent Architecture](ai-agents/2026-02-19_docker-multi-agent-architecture.md) | #docker #multi-agent #orchestration #isolation #kimi-k2 #gemini-flash #openclaw #a2a-protocol | Research for Iris/OpenClaw multi-worker setup on Mac mini M4
- **2026-02-14** | [SO L2 — Stock Opname Daily Reconciliation](business-ops/2026-02-14_so-l2-stock-opname-daily.md) | #inventory-control #stock-opname #reconciliation #shrinkage-detection | Internal briefing
- **2026-02-14** | [Dieter Rams — Braun Design & Apple Influence](design/2026-02-14_research_dieter-rams-braun.md) | #design #product-design #braun #apple #minimalism | Research request
- **2026-02-14** | [FF/FA/FS Daily Fill Rate Metrics](business-ops/2026-02-14_ff-fa-fs-daily-metrics.md) | #inventory #fill-rate #metrics #automation | Internal briefing
- **2026-02-14** | [OpenClaw Agent "Larry" - TikTok Viral Marketing](ai-agents/2026-02-14_twitter_openclaw-larry-tiktok.md) | #ai-agents #openclaw #tiktok-marketing #automation | Twitter @oliverhenry

---

## By Topic

### AI Agents
- **[AI Town — Autonomous Agent Town Simulator](ai-agents/2026-02-27_github_a16z-ai-town.md)** — a16z starter kit (9.3k ⭐): generative agents with vector memory, perceive→reflect→plan→act loop, Convex real-time backend, agent-to-agent conversations. Reference architecture for Iris memory system and heartbeat evolution
- [Arscontexta — Skill Graphs > SKILL.md](ai-agents/2026-02-21_twitter_arscontexta-skill-graphs.md) — Claude Code plugin: knowledge systems from conversation, Skill Graphs (wikilinked markdown networks), progressive disclosure navigation, 249 research claims, Three-Space architecture
- [Docker Multi-Agent Architecture](ai-agents/2026-02-19_docker-multi-agent-architecture.md) — Supervisor/Worker pattern with Docker Compose, A2A protocol, isolation strategies (Docker/venv/process), cost comparison Kimi K2.5 vs Gemini Flash, Mac mini M4 resource planning, implementation roadmap for OpenClaw
- [OpenClaw Agent "Larry" - TikTok Viral Marketing](ai-agents/2026-02-14_twitter_openclaw-larry-tiktok.md) — AI agent automation for TikTok slideshows, 500K+ views in 5 days

### Business Operations
- [SO L2 — Stock Opname Daily Reconciliation](business-ops/2026-02-14_so-l2-stock-opname-daily.md) — Daily stock vs sales reconciliation, detects shrinkage/theft via selisih calculation
- [FF/FA/FS Daily Fill Rate Metrics](business-ops/2026-02-14_ff-fa-fs-daily-metrics.md) — Automated daily pipeline for store fill rate metrics (Fill Factor, Fill Article, Fill Stock)

### Design
- [Dieter Rams — Braun Design & Apple Influence](design/2026-02-14_research_dieter-rams-braun.md) — Industrial design philosophy, 10 Principles of Good Design, influence on Apple/Jonathan Ive

### Dev Tools
- **[OpenClaw Cost Optimization Playbook](dev-tools/2026-02-28_openclaw-cost-optimization-playbook.md)** — 65-70% cost cut. Model tiering (Opus→Sonnet→Flash), QMD local search (90% token reduction), session memory fix (50kb→8kb), Ollama for free repetitive tasks, heartbeats→Flash. Session fix URGENT for Iris.
- **[Awesome OpenClaw Use Cases](dev-tools/2026-02-28_awesome-openclaw-usecases.md)** — 30 real use cases (11k⭐). Deep dives: Self-healing server (cron+SSH+kubectl), STATE.yaml subagent pattern, multi-agent Telegram team, multi-channel customer service (80% auto), Second Brain. **Security:** AI hardcodes secrets — use TruffleHog + local Gitea.
- **[Clawbox — OpenClaw macOS VMs](dev-tools/2026-02-28_clawbox-macos-vm.md)** — 2-command macOS VM setup for OpenClaw (brew install + clawbox up). Standard/Developer modes, Mutagen bidirectional sync, Playwright/Tailscale/signal-cli optional. Max 2 VMs/Mac host. Low priority for Iris (on VPS).
- **[Qwen3.5-35B-A3B — Local Install Guide](dev-tools/2026-02-28_qwen35-35b-a3b-local-install.md)** — Released Feb 24 2026. 35B total/3B active MoE. Unsloth GGUFs (refreshed Feb 27). Fits 16GB: UD-Q2_K_XL (12.9GB) recommended. Vision+video+tool use. Thinking mode default ON.
- **[Scrapling — Adaptive Web Scraping Framework](dev-tools/2026-02-27_scrapling.md)** — 784x faster than BeautifulSoup, adaptive element relocation (survive redesigns), StealthyFetcher (Cloudflare Turnstile + TLS bypass), concurrent crawling (1000s URLs), MCP-ready for AI agents, BSD-3, 14.1k stars
- **[Public APIs — Curated for Zuma & Iris](dev-tools/2026-02-27_public-apis-zuma-relevant.md)** — 60+ APIs filtered for Zuma retail ops & Iris AI. Tier-1: Google Maps, Sendinblue, NewsAPI, NLP Cloud (Indonesian ✅), Xendit/Midtrans. ⚠️ Sendgrid free tier ended Jul 2025. ⚠️ MercadoPago no IDR.
- **[Public APIs — Verification Summary](dev-tools/2026-02-27_public-apis-verification-summary.md)** — Executive summary: payment gateway comparison, CORS analysis (60% need backend proxy), action items (URGENT: migrate Sendgrid → Sendinblue, MercadoPago → Xendit)
- **[Agent Browser — AI-Optimized Browser Automation](dev-tools/2026-02-27_agent-browser.md)** — 93% less context vs Playwright MCP, 95% first-try success, Rust CLI + Node.js daemon, installed v0.15.1, perfect for token-constrained agent runs
- **[World Monitor — Real-Time Global Intelligence Dashboard](dev-tools/2026-02-25_github_worldmonitor.md)** — OSINT-grade real-time dashboard (geopolitics/tech/finance), 100+ feeds, 3D WebGL globe (deck.gl), 35+ data layers, local LLM (Ollama), native Tauri desktop app, proto-first API (17 typed services), AGPL, free
- **[Vibe Coding 2.0 — 18 Rules](dev-tools/2026-02-25_vibe-coding-2-rules.md)** — Stack: Next.js+Tailwind+shadcn+tRPC+Prisma+Clerk+Stripe+Sentry+Vercel. Core: tau apa yang TIDAK perlu dibangun. 18 DO's + 16 DON'Ts untuk MVP cepat
- [KittenTTS — Lightweight Open-Source TTS](ai-agents/20260222_kittentts_tts_model.md) — Ultra-lightweight TTS (15M params, <25MB nano), 8 voices, CPU-only, Apache-2.0, use cases: WhatsApp voice messages, product VO, customer service automation
- [Gateway Pairing Issue Fix — Scope Mismatch](dev-tools/2026-02-20_gateway-pairing-fix.md) — OpenClaw gateway device pairing troubleshooting, scope diagnosis, token rotation, device auth verification
- [Voicebox — Open-Source Voice Synthesis Studio](dev-tools/2026-02-19_github_voicebox.md) — Local-first voice cloning studio (ElevenLabs alternative), powered by Qwen3-TTS, REST API, MLX-optimized for Apple Silicon
- [Botasaurus — All-in-One Web Scraping Framework](dev-tools/2026-02-19_github_botasaurus.md) — Python scraping framework, bypass Cloudflare/Datadome/Fingerprint, Selenium-based with @browser + @request decorators, built-in Web UI, Kubernetes scaling
- [Exa API Setup](dev-tools/exa-api-setup.md)

### Miscellaneous
<!-- misc/ entries -->

---

## Search Tips

```bash
# Search all knowledge by keyword
grep -r "keyword" knowledge/

# Search by tag
grep -r "#tag-name" knowledge/

# List recent (last 7 days)
find knowledge/ -name "*.md" -mtime -7
```

---

**Last updated:** 2026-02-28 (Awesome OpenClaw Use Cases + Clawbox VM added)

- `dev-tools/2026-02-27_accurate-api-troubleshooting.md` — Accurate API 401/500 debug flow, token regenerate steps, VPS run guide
