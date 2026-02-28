# OpenClaw Multi-Instance pada Mac Mini M4 — Research Notes

**Date:** 2026-02-28  
**Tags:** #openclaw #multi-instance #docker #mac-mini #isolation #infrastructure #iris  
**Context:** Iris running on VPS. Plan: host multiple OpenClaw instances on Mac Mini M4 16GB.

---

## Koreksi Asumsi Awal

> ❌ "OpenClaw tidak bisa jalan di Docker karena butuh macOS"

Ini **salah**. OpenClaw punya official Docker image: `openclaw/openclaw:latest` dan bisa jalan di Linux container.

**Yang tidak bisa di Docker:**
- iMessage / AppleScript / Cocoa GUI integrations
- macOS Keychain native access
- Calendar AppleScript

**Yang tetap bisa di Docker (relevan untuk Iris):**
- WhatsApp gateway ✅
- Telegram ✅
- Discord, Slack ✅
- Web search, file operations, SQL ✅
- Skills berbasis HTTP API ✅

→ **Untuk use case Iris (WhatsApp/Telegram), Docker sepenuhnya viable.**

---

## 5 Opsi Multi-Instance

### Opsi 1: Docker (Linux Containers) ⭐ RECOMMENDED untuk 3+ instances

**Cara kerja:** Setiap OpenClaw instance jalan dalam Docker container sendiri.  
Docker Desktop di macOS menggunakan hidden Linux VM internally — jadi tidak terkena limit macOS VM.

```bash
# Quick start per instance
docker run -d \
  --name openclaw-iris \
  --restart unless-stopped \
  -p 18800:3001 \
  -m 512m \
  --cpus=1 \
  -v openclaw-iris-data:/app/data \
  -e OPENCLAW_GATEWAY_TOKEN=iris-unique-token \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  openclaw/openclaw:latest
```

**Docker Compose untuk multiple instances:**
```yaml
version: '3.8'
services:
  openclaw-iris:
    image: openclaw/openclaw:latest
    restart: unless-stopped
    ports: ["18800:3001"]
    volumes: [iris_data:/app/data]
    environment:
      - OPENCLAW_GATEWAY_TOKEN=iris-token
      - ANTHROPIC_API_KEY=${IRIS_API_KEY}
    deploy:
      resources:
        limits: { memory: 512M, cpus: '1.0' }
        reservations: { memory: 256M, cpus: '0.25' }

  openclaw-agent2:
    image: openclaw/openclaw:latest
    restart: unless-stopped
    ports: ["18801:3001"]
    volumes: [agent2_data:/app/data]
    environment:
      - OPENCLAW_GATEWAY_TOKEN=agent2-token
      - ANTHROPIC_API_KEY=${AGENT2_API_KEY}
    deploy:
      resources:
        limits: { memory: 512M, cpus: '1.0' }
        reservations: { memory: 256M, cpus: '0.25' }

volumes:
  iris_data:
  agent2_data:
```

**Resource per container:**
| Workload | RAM Limit | CPU Limit |
|---------|-----------|-----------|
| Light (chat only) | 384MB | 0.5 CPU |
| Standard (Telegram/WA + skills) | 512MB | 1.0 CPU |
| Heavy (Playwright/browser) | 1024MB | 2.0 CPU |

**Idle RAM per container: ~200-300MB. Active: 400-600MB.**

**Kapasitas Mac Mini M4 16GB:**
- ~6GB untuk macOS host + Docker Desktop VM overhead
- ~10GB tersedia untuk containers
- Pada 512MB limit: **~15-20 containers secara teori**
- **Realistis dengan beban campuran: 5-8 instances comfortably**
- Overcommit 1.5x aman karena tidak semua active bersamaan

**Port allocation:**
```
18800 → Instance 1 (Iris/main)
18801 → Instance 2
18802 → Instance 3
...
18899 → Instance 100 max
```

**Security hardening (recommended):**
```bash
docker run -d \
  --read-only \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  --security-opt no-new-privileges \
  ...
```

**Pros:** Full isolation, easy scaling, no macOS VM limit, resource caps per instance  
**Cons:** Kehilangan macOS-native features (iMessage, Keychain, Calendar AppleScript)

---

### Opsi 2: Clawbox (macOS VMs via Tart) — Max 2

**Kapan pakai:** Butuh full macOS environment (iMessage, native Keychain)

```bash
brew install joshavant/tap/clawbox
clawbox image build  # one-time, download large

# VM 1
clawbox up --number 1

# VM 2  
clawbox up --number 2

# VM 3+ → ❌ Apple EULA limit exceeded
# Error: VZError.Code.virtualMachineLimitExceeded
```

**Apple EULA Section 2.B.iii:** max 2 additional macOS VM instances per Apple-branded computer. Ini **hardware-enforced** di level Virtualization.framework — bukan software limit yang bisa di-bypass.

**RAM per macOS VM (Tart):**
- Base macOS install: ~4-5GB
- + OpenClaw process: ~500MB
- Total per VM: **~5-6GB minimum**
- Pada 16GB: hanya cukup untuk **1 VM** dengan nyaman (2 VM akan sangat cramped)

**Pros:** Full macOS, Keychain, iMessage, semua native features  
**Cons:** Max 2, sangat makan RAM, slow startup

---

### Opsi 3: Multiple Processes (Same macOS User) — Lightweight

Jalankan beberapa `openclaw` process dengan payload directory berbeda, di macOS host langsung.

```bash
# Instance 1 (default payload)
openclaw --install-daemon

# Instance 2 (custom payload)
OPENCLAW_PAYLOAD=~/.openclaw-instance2 openclaw gateway --port 3002

# Instance 3
OPENCLAW_PAYLOAD=~/.openclaw-instance3 openclaw gateway --port 3003
```

**Pros:** Zero overhead, instant start, full macOS features  
**Cons:** Tidak ada process isolation (satu crash bisa affect lain), shared Keychain/filesystem namespace, tidak clean untuk production

**Cocok untuk:** Development/testing multiple configs, bukan production multi-tenant

---

### Opsi 4: Multiple macOS User Accounts

Buat user account macOS terpisah per instance. Setiap user punya:
- Isolated `~/.openclaw/` directory
- Separate Keychain
- Separate launchd services

```bash
# Buat user baru
sudo dscl . -create /Users/openclaw-agent2
sudo dscl . -create /Users/openclaw-agent2 UserShell /bin/zsh
sudo dscl . -passwd /Users/openclaw-agent2 password

# Switch user dan setup
su - openclaw-agent2
openclaw onboard --install-daemon
```

**Manage via launchctl (switch user context):**
```bash
sudo launchctl asuser $(id -u openclaw-agent2) launchctl list | grep openclaw
```

**Pros:** Full macOS isolation, separate Keychains, production-grade  
**Cons:** Setup kompleks, tidak ada web UI untuk manage, susah update semua sekaligus

---

### Opsi 5: Split VPS + Mac Mini (Current Setup, Extended)

Pertahankan arsitektur sekarang tapi tambah instances di VPS:
- Mac Mini: Iris main (native macOS untuk iMessage dll)
- VPS: 1-3 instances Docker OpenClaw untuk task-based agents (Daedalus, Argus, dll)

**Pros:** Best of both worlds — native macOS di Mac Mini, scalable Docker di VPS  
**Cons:** Dua infrastruktur untuk di-maintain

---

## Rekomendasi untuk Iris/Zuma

### Untuk use case saat ini (WhatsApp/Telegram/API-based):

**→ Docker di Mac Mini adalah cara paling praktis**

```bash
# Install Docker Desktop
brew install --cask docker

# Buat docker-compose.yml dengan instances yang dibutuhkan
# Port 18800: Iris main
# Port 18801: Daedalus-style coding agent
# Port 18802: Argus-style data agent
```

**Setup yang disarankan (Mac Mini M4 16GB):**
- 1 Iris (main, existing) — bisa tetap native di Mac Mini atau migrate ke Docker
- 2-3 additional agents Docker — tiap 512MB = ~2GB total
- Total Docker overhead: ~3-4GB (Docker Desktop VM + containers)
- Host macOS tetap punya ~8-9GB free untuk native processes

### Kalau mau tetap native macOS untuk Iris:

Kombinasikan: **Iris tetap native + additional agents pakai Docker**

Iris native di Mac Mini (full macOS features) sambil additional specialized agents jalan di Docker container untuk isolation dan easy management.

---

## Docker Multi-Instance — Quick Reference Card

```bash
# Check running instances
docker ps

# Resource usage per container
docker stats --no-stream

# Logs per instance
docker logs --tail 50 openclaw-iris

# Restart specific instance
docker restart openclaw-iris

# Scale up: tambah instance baru
docker run -d --name openclaw-new \
  -p 18803:3001 \
  -m 512m --cpus=1 \
  -v openclaw-new-data:/app/data \
  -e OPENCLAW_GATEWAY_TOKEN=new-token \
  -e ANTHROPIC_API_KEY=${API_KEY} \
  openclaw/openclaw:latest

# Update semua ke latest
docker pull openclaw/openclaw:latest
docker compose up -d --force-recreate
```

---

## Monitoring Health Check (cron-based)

```bash
# Tambah ke crontab untuk auto-heal
*/5 * * * * docker ps --filter "status=exited" --format "{{.Names}}" | xargs -r docker start

# Alert kalau container mati
*/1 * * * * docker inspect --format='{{.State.Health.Status}}' openclaw-iris | grep -v healthy && \
  curl -s "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage?chat_id=${CHAT_ID}&text=openclaw-iris+unhealthy!"
```

---

## Sources

- ClawTank — Multi-Tenant Docker Guide: https://clawtank.dev/blog/openclaw-multi-tenant-docker-guide
- ClawCloud — Docker Security for OpenClaw: https://www.clawcloud.dev/news/how-to-set-up-openclaw-with-docker-isolation-for-security
- Apple EULA Section 2.B.iii — macOS VM limit: confirmed 2 VMs max, hardware-enforced
- Tart / Clawbox: max 2 concurrent macOS VMs (Apple Virtualization.framework)
- OpenClaw official Docker image: `openclaw/openclaw:latest` (port 3001)
- OpenClaw docs: https://docs.openclaw.ai/deployment/docker
- Apple Silicon VM limit deep dive: https://khronokernel.com/macos/2023/08/08/AS-VM.html
