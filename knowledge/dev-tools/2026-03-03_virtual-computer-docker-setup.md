# AI Virtual Computer in Docker — Full Technical Guide

> **TL;DR:** How to give an AI agent a real computer (headed Chrome + web desktop + CDP automation + persistent sessions) inside Docker on a VPS, without breaking existing services.

**Date:** 2026-03-03
**Author:** Claude (OpenCode) for Zuma/OpenClaw
**Tags:** #docker #virtual-computer #chrome-cdp #webtop #linuxserver #socat #ai-agent #browser-automation #xfce #headed-chrome

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Failed Approaches (and Why)](#failed-approaches)
3. [Winning Solution: linuxserver/webtop](#winning-solution)
4. [Architecture](#architecture)
5. [The Critical Chrome CDP Bug](#the-critical-chrome-cdp-bug)
6. [Step-by-Step Reproduction](#step-by-step-reproduction)
7. [Auto-Start & Persistence](#auto-start--persistence)
8. [Verification](#verification)
9. [Troubleshooting](#troubleshooting)
10. [Resource Usage](#resource-usage)
12. [Connecting an AI Agent to the Virtual Computer](#connecting-an-ai-agent-to-the-virtual-computer)
13. [Key Lessons Learned](#key-lessons-learned)

---

## Problem Statement

### What We Needed

An AI agent (Iris) needs a **real computer** — not just a headless browser. Specifically:

| Requirement | Why |
|---|---|
| **Headed Chrome** (not headless) | Google blocks headless browsers with CAPTCHA/challenges |
| **Chrome DevTools Protocol (CDP)** endpoint | AI agent automates Chrome programmatically via `ws://host:9222` |
| **Web desktop accessible via browser** | Human operator can spectate/intervene by opening a URL |
| **Persistent sessions** | Gmail login survives container restarts |
| **Full OS** | Install additional tools (file managers, editors, CLI tools) over time |
| **Coexist with existing services** | VPS already runs OpenClaw gateway — must not disrupt it |

### Environment

- **VPS**: 7.8GB RAM, 96GB disk (82GB free), running OpenClaw gateway (~392MB RAM)
- **Existing services**: OpenClaw gateway on PID 862, ports 18789/18792 (localhost only)
- **Docker**: Available, using `docker-compose` v1 (hyphenated, not `docker compose` v2)

---

## Failed Approaches

### 1. browserless/chrome

**What it is:** Purpose-built Docker image for headless Chrome automation.

**Why it failed:** Chrome runs in **headless mode**. Google detects this and blocks with CAPTCHA/security challenges. There's no way to get a visible desktop for human spectating. Headless = no login persistence for Google accounts.

**Lesson:** Any solution involving headless Chrome is a dead end for Google services.

### 2. linuxserver/chromium

**What it is:** LinuxServer's Chromium browser with web UI on port 3000.

**Why it failed:**
- Port 6080 (noVNC) was unreachable despite being configured
- CDP was not exposed
- Web UI only showed Chromium, not a full desktop
- Limited extensibility — just a browser, not a computer

**Lesson:** Browser-only containers are too narrow. We need a full desktop environment.

### 3. Custom Ubuntu Container (inline apt-get)

**What it is:** A vanilla Ubuntu image with Chrome installed via `apt-get` in the Dockerfile, plus a VNC/noVNC server manually configured.

**Why it failed:**
- Chrome kept crashing due to missing dbus socket
- Zombie processes accumulated (no init system)
- X11/display setup was brittle and error-prone
- No proper process supervisor meant services died silently

**Lesson:** Running a desktop environment in Docker requires a proper init system (like s6-overlay) and process supervision. Don't reinvent this wheel.

---

## Winning Solution

### linuxserver/webtop:ubuntu-xfce

**Image:** `lscr.io/linuxserver/webtop:ubuntu-xfce`

**Why this works:**
1. **Full Ubuntu XFCE desktop** — not just a browser, a complete OS with file manager, terminal, etc.
2. **Built-in web access** via KasmVNC/Selkies on port 3000 — zero additional VNC setup
3. **s6-overlay init system** — proper process supervision, no zombies
4. **`/config` persistent volume** — everything in `/config` survives container restarts
5. **`custom-cont-init.d` scripts** — install additional software on container start
6. **Lightweight** — ~400-600MB RAM idle (vs ~800-1.2GB for kasmweb alternatives)
7. **Active maintenance** — LinuxServer community, regular updates

---

## Architecture

```
VPS (76.13.194.103)
├── OpenClaw gateway (PID 862)
│   ├── Port 18789 (localhost only)
│   └── Port 18792 (localhost only)
│
└── Docker: iris-desktop (linuxserver/webtop:ubuntu-xfce)
    │
    ├── Port 3000 → KasmVNC/Selkies web desktop
    │   └── Human opens http://VPS_IP:3000/ in their browser
    │       → Sees full XFCE desktop with Chrome running
    │       → Can interact (click, type) or just watch
    │
    ├── Port 3001 → HTTPS web desktop (optional)
    │
    ├── Port 9222 → socat bridge → Port 9223 (Chrome CDP)
    │   └── AI agent connects: ws://VPS_IP:9222
    │       → Full Chrome DevTools Protocol access
    │       → Navigate pages, click elements, read DOM, etc.
    │
    └── /config/ (persistent Docker volume)
        ├── .chrome-profile/          # Chrome user data (Gmail session, cookies)
        ├── scripts/
        │   └── chrome-cdp-service.sh # Watchdog: keeps Chrome + socat alive
        ├── .config/autostart/
        │   └── chrome-cdp-service.desktop  # XFCE autostart entry
        ├── Desktop/
        │   └── chrome-cdp.desktop    # Desktop shortcut for Chrome
        └── custom-cont-init.d/
            └── 01-install-chrome.sh  # Install Chrome + socat on container start
```

### Data Flow

```
AI Agent                          Human Spectator
   │                                    │
   │ ws://VPS:9222                      │ http://VPS:3000
   │                                    │
   ▼                                    ▼
┌──────────────────────────────────────────┐
│  Docker Container (iris-desktop)          │
│                                          │
│  ┌─────────┐    ┌────────────────────┐   │
│  │  socat   │───▶│  Google Chrome     │   │
│  │ :9222    │    │  :9223 (CDP)       │   │
│  │ bridge   │    │  --user-data-dir=  │   │
│  └─────────┘    │  /config/.chrome-   │   │
│                 │  profile            │   │
│                 │                     │   │
│                 │  Runs on DISPLAY :1 │   │
│                 │  (XFCE desktop)     │   │
│                 └────────────────────┘   │
│                                          │
│  KasmVNC/Selkies renders DISPLAY :1      │
│  → streams to browser on port 3000       │
└──────────────────────────────────────────┘
```

---

## The Critical Chrome CDP Bug

### The Problem

**Chrome M113+ (released ~2023) hardcodes the CDP debug listener to `127.0.0.1`.**

The flag `--remote-debugging-address=0.0.0.0` is **silently ignored** in newer Chrome versions. The Chromium source code (`headless/lib/headless_browser_main_parts.cc`) explicitly hardcodes the bind address to localhost.

This means:
- Chrome listens for CDP on `127.0.0.1:9222` inside the container
- Outside the container (or even from another process binding to `0.0.0.0:9222`) **cannot reach it**
- The Docker port mapping `-p 9222:9222` maps to `0.0.0.0:9222` inside the container, which Chrome never binds to
- **No error is shown** — Chrome silently ignores the flag and binds to localhost anyway

### The Solution: socat Bridge

`socat` creates a TCP proxy that bridges the gap:

```
External :9222 (0.0.0.0) ──socat──▶ Internal :9223 (127.0.0.1)
                                          │
                                     Chrome CDP
```

Chrome binds CDP to `127.0.0.1:9223`. socat listens on `0.0.0.0:9222` and forwards everything to `127.0.0.1:9223`. Docker maps host port 9222 to container port 9222.

**The socat command:**
```bash
socat TCP-LISTEN:9222,fork,reuseaddr TCP:127.0.0.1:9223
```

**Why port 9223 for Chrome (not 9222):**
- socat must listen on 9222 (the Docker-exposed port)
- Chrome must listen on a different port to avoid conflict
- 9223 is the conventional "internal" CDP port

This is a **widely unknown issue**. Most Docker + Chrome CDP guides are outdated (pre-M113) and assume `--remote-debugging-address=0.0.0.0` works. It doesn't anymore.

---

## Step-by-Step Reproduction

### Prerequisites

- A Linux VPS with Docker and docker-compose installed
- At least 2GB free RAM
- Ports 3000, 3001, 9222 available

### Step 1: Create Directory Structure

```bash
mkdir -p ~/iris-vm/config/custom-cont-init.d
mkdir -p ~/iris-vm/config/custom-services.d
```

### Step 2: Create docker-compose.yml

```bash
cat > ~/iris-vm/docker-compose.yml << 'EOF'
services:
  iris-desktop:
    image: lscr.io/linuxserver/webtop:ubuntu-xfce
    container_name: iris-desktop
    security_opt:
      - seccomp:unconfined
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Jakarta
      - CUSTOM_USER=iris
      - PASSWORD=your_password_here
      - TITLE=Iris Virtual Computer
    volumes:
      - ./config:/config
      - ./config/custom-cont-init.d:/custom-cont-init.d
      - ./config/custom-services.d:/custom-services.d
    ports:
      - "3000:3000"
      - "3001:3001"
      - "9222:9222"
    shm_size: "2gb"
    restart: unless-stopped
EOF
```

**Key configuration notes:**
- `seccomp:unconfined` — required for Chrome sandboxing inside Docker
- `shm_size: "2gb"` — Chrome needs shared memory; default 64MB causes crashes
- `PUID/PGID=1000` — LinuxServer convention for file permissions
- **Volume mount for `custom-cont-init.d`** — Newer webtop images expect init scripts at `/custom-cont-init.d/` (root level), NOT `/config/custom-cont-init.d/`. The extra volume mount `./config/custom-cont-init.d:/custom-cont-init.d` handles this.

### Step 3: Create Chrome + socat Install Script

```bash
cat > ~/iris-vm/config/custom-cont-init.d/01-install-chrome.sh << 'SCRIPT'
#!/bin/bash
set -e

echo "=== Installing Google Chrome + socat ==="

# Check if Chrome is already installed
if command -v google-chrome-stable &>/dev/null; then
    echo "Chrome already installed: $(google-chrome-stable --version)"
else
    echo "Installing Chrome via direct .deb download..."
    
    # Direct download is faster and more reliable than apt repo on some VPS
    apt-get update -qq
    apt-get install -y -qq wget socat
    
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
         -O /tmp/chrome.deb
    dpkg -i /tmp/chrome.deb || apt-get install -f -y -qq
    rm /tmp/chrome.deb
    
    echo "Chrome installed: $(google-chrome-stable --version)"
fi

# Ensure socat is installed
if ! command -v socat &>/dev/null; then
    apt-get update -qq && apt-get install -y -qq socat
fi

echo "=== Chrome + socat installation complete ==="
SCRIPT

chmod +x ~/iris-vm/config/custom-cont-init.d/01-install-chrome.sh
```

**Why direct .deb download instead of apt repo:**
On some VPS environments, adding the Google apt repository and running `apt-get update` hangs indefinitely. The direct download from `https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb` is consistently fast and reliable. `dpkg -i` + `apt-get install -f` handles all dependencies.

### Step 4: Start the Container

```bash
cd ~/iris-vm
docker-compose up -d
```

Wait ~2-3 minutes for:
1. Image download (first time only, ~1.5GB)
2. Container init (s6-overlay startup)
3. Chrome installation (first time, ~2 min)
4. XFCE desktop boot

### Step 5: Verify Web Desktop

Open `http://YOUR_VPS_IP:3000/` in a browser. You should see an XFCE desktop login or desktop.

### Step 6: Create the Watchdog Script (inside container)

```bash
docker exec iris-desktop bash -c 'mkdir -p /config/scripts && cat > /config/scripts/chrome-cdp-service.sh << '\''WATCHDOG'\''
#!/bin/bash
# Watchdog: keeps Chrome + socat alive
# Runs via XFCE autostart on desktop login

LOG="/config/scripts/chrome-cdp.log"
echo "$(date): Watchdog starting..." >> "$LOG"

start_chrome() {
    if ! pgrep -f "remote-debugging-port=9223" > /dev/null 2>&1; then
        echo "$(date): Starting Chrome with CDP on :9223..." >> "$LOG"
        google-chrome-stable \
            --remote-debugging-port=9223 \
            --remote-debugging-address=127.0.0.1 \
            --user-data-dir=/config/.chrome-profile \
            --no-first-run \
            --no-default-browser-check \
            --disable-background-networking \
            --disable-sync \
            --disable-features=TranslateUI \
            --start-maximized &
        sleep 3
    fi
}

start_socat() {
    if ! pgrep -f "socat.*TCP-LISTEN:9222" > /dev/null 2>&1; then
        echo "$(date): Starting socat bridge :9222 -> :9223..." >> "$LOG"
        socat TCP-LISTEN:9222,fork,reuseaddr TCP:127.0.0.1:9223 &
        sleep 1
    fi
}

# Initial start
start_chrome
start_socat

# Watchdog loop — check every 30 seconds, restart if dead
while true; do
    start_chrome
    start_socat
    sleep 30
done
WATCHDOG
chmod +x /config/scripts/chrome-cdp-service.sh'
```

**Chrome flags explained:**
- `--remote-debugging-port=9223` — CDP on port 9223 (socat forwards from 9222)
- `--remote-debugging-address=127.0.0.1` — technically ignored by Chrome M113+, but included for documentation
- `--user-data-dir=/config/.chrome-profile` — persistent profile in the Docker volume
- `--no-first-run` — skip Chrome's "Welcome" setup wizard
- `--no-default-browser-check` — skip "set as default browser" prompt
- `--start-maximized` — fills the desktop (better for spectating)

### Step 7: Create XFCE Autostart Entry

```bash
docker exec iris-desktop bash -c 'mkdir -p /config/.config/autostart && cat > /config/.config/autostart/chrome-cdp-service.desktop << '\''DESKTOP'\''
[Desktop Entry]
Type=Application
Name=Chrome CDP Service
Exec=/config/scripts/chrome-cdp-service.sh
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Comment=Start Chrome with CDP and socat bridge on desktop login
DESKTOP'
```

**Why XFCE autostart instead of s6 services:**
LinuxServer's s6-overlay handles `/custom-cont-init.d/` scripts (run once at container start), but does NOT auto-register services from `/custom-services.d/` as persistent s6 services in newer images. The XFCE autostart approach is simpler and more reliable — the watchdog script starts when the desktop session begins and keeps running.

### Step 8: Create Desktop Shortcut (optional)

```bash
docker exec iris-desktop bash -c 'cat > /config/Desktop/chrome-cdp.desktop << '\''SHORTCUT'\''
[Desktop Entry]
Version=1.0
Type=Application
Name=Chrome (CDP Enabled)
Exec=google-chrome-stable --remote-debugging-port=9223 --user-data-dir=/config/.chrome-profile --no-first-run --start-maximized
Icon=google-chrome
Terminal=false
Categories=Network;WebBrowser;
SHORTCUT
chmod +x /config/Desktop/chrome-cdp.desktop'
```

### Step 9: Start Services (first time)

```bash
docker exec iris-desktop bash -c '/config/scripts/chrome-cdp-service.sh &'
```

After a container restart, the XFCE autostart entry will start the watchdog automatically.

---

## Auto-Start & Persistence

### What Survives Container Restarts

Everything under `/config/` persists, which includes:

| Item | Path | Persists? |
|------|------|-----------|
| Chrome user data (Gmail, cookies, history) | `/config/.chrome-profile/` | ✅ |
| Chrome + socat installer | `/config/custom-cont-init.d/01-install-chrome.sh` | ✅ |
| Watchdog script | `/config/scripts/chrome-cdp-service.sh` | ✅ |
| XFCE autostart config | `/config/.config/autostart/` | ✅ |
| Desktop shortcuts | `/config/Desktop/` | ✅ |
| Any files you create | `/config/` | ✅ |

### Restart Flow

1. Container starts → s6-overlay initializes
2. `/custom-cont-init.d/01-install-chrome.sh` runs → installs Chrome + socat (skips if already installed)
3. XFCE desktop boots on DISPLAY :1
4. XFCE autostart triggers → `/config/scripts/chrome-cdp-service.sh` starts
5. Watchdog starts Chrome (with persistent profile) and socat bridge
6. Every 30 seconds: watchdog checks if Chrome or socat died, restarts if needed

**Gmail sessions persist** because Chrome's user data directory (`/config/.chrome-profile/`) is on the persistent volume. After logging into Gmail once via the web desktop, the session survives restarts indefinitely (until Google's session expiry, typically weeks/months).

---

## Verification

### 1. Web Desktop

```bash
curl -s -o /dev/null -w "%{http_code}" http://YOUR_VPS_IP:3000/
# Expected: 200
```

### 2. CDP Endpoint

```bash
curl -s http://YOUR_VPS_IP:9222/json/version
# Expected: JSON with "Browser": "Chrome/1XX.X.XXXX.XXX", "webSocketDebuggerUrl": "ws://..."
```

```bash
curl -s http://YOUR_VPS_IP:9222/json/list
# Expected: JSON array of open Chrome tabs/pages
```

### 3. Container Status

```bash
docker ps --filter name=iris-desktop --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
# Expected: iris-desktop   Up X hours   0.0.0.0:3000->3000/tcp, 0.0.0.0:3001->3001/tcp, 0.0.0.0:9222->9222/tcp
```

### 4. Inside Container

```bash
docker exec iris-desktop pgrep -a chrome
# Expected: google-chrome-stable process(es) running

docker exec iris-desktop pgrep -a socat
# Expected: socat TCP-LISTEN:9222 process running
```

---

## Troubleshooting

### Chrome won't start

**Symptom:** No Chrome process after starting watchdog.

**Check:**
```bash
docker exec iris-desktop google-chrome-stable --version
# If "command not found" → 01-install-chrome.sh didn't run
# Fix: docker exec iris-desktop bash /custom-cont-init.d/01-install-chrome.sh
```

### CDP endpoint returns "Connection refused"

**Symptom:** `curl http://VPS:9222/json/version` fails.

**Check 1:** Is socat running?
```bash
docker exec iris-desktop pgrep -a socat
# If no output → socat not running
# Fix: docker exec iris-desktop socat TCP-LISTEN:9222,fork,reuseaddr TCP:127.0.0.1:9223 &
```

**Check 2:** Is Chrome's CDP listening?
```bash
docker exec iris-desktop curl -s http://127.0.0.1:9223/json/version
# If this works but :9222 doesn't → socat bridge issue
# If this also fails → Chrome not started with --remote-debugging-port=9223
```

### dbus errors in container logs

**Symptom:** Log messages like:
```
dbus[xxx]: ... org.freedesktop.login1 ... Permission denied
dbus[xxx]: ... org.freedesktop.PolicyKit1 ... Permission denied
```

**Verdict: HARMLESS.** These are normal in Docker containers. The desktop environment functions correctly without dbus system services. Ignore these.

### Chrome crashing on start

**Check 1:** Shared memory size
```bash
docker exec iris-desktop df -h /dev/shm
# If < 2GB → add shm_size: "2gb" to docker-compose.yml
```

**Check 2:** seccomp profile
Ensure `security_opt: - seccomp:unconfined` is in docker-compose.yml. Chrome's sandbox needs this in Docker.

### Web desktop shows blank/error

**Check:** Container fully started?
```bash
docker logs iris-desktop --tail 50
# Look for "s6-rc: info: service legacy-services successfully started"
```

The web desktop takes ~30-60 seconds to be ready after container start. Wait and retry.

### apt-get hangs during Chrome install

**Symptom:** `01-install-chrome.sh` hangs at `apt-get update`.

**Fix:** Switch to direct .deb download (which is what our script uses). If it's hanging on the Google apt repo specifically:
```bash
# Remove Google apt repo if added
rm -f /etc/apt/sources.list.d/google-chrome.list
# Use direct download only
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/chrome.deb
dpkg -i /tmp/chrome.deb
apt-get install -f -y
```

---

## Resource Usage

Measured on a 7.8GB RAM VPS with OpenClaw gateway already running:

| Component | RAM (idle) | RAM (active browsing) | CPU (idle) | Disk |
|---|---|---|---|---|
| iris-desktop container | ~600MB | ~900-1200MB | ~3% | ~2.5GB (image + Chrome) |
| Chrome (1-3 tabs) | ~300-500MB | ~500-800MB | ~1-5% | included above |
| socat bridge | ~1MB | ~1MB | ~0% | negligible |

**Total with existing services:** ~1.7GB of 7.8GB used (idle), leaving ~6GB free.

---

## Extending the Virtual Computer

### Installing Additional Software

Add to `/config/custom-cont-init.d/01-install-chrome.sh` (or create a new `02-install-tools.sh`):

```bash
#!/bin/bash
# Example: install common tools
apt-get update -qq
apt-get install -y -qq \
    htop \
    vim \
    python3-pip \
    nodejs \
    npm \
    git
```

Software installed via `custom-cont-init.d` is reinstalled on every container recreate (not restart). For persistence across `docker-compose up --force-recreate`, install to `/config/` or use the init script approach.

### Adding More Services

Create additional autostart entries in `/config/.config/autostart/`:

```ini
[Desktop Entry]
Type=Application
Name=My Service
Exec=/config/scripts/my-service.sh
Hidden=false
X-GNOME-Autostart-enabled=true
```

### Connecting an AI Agent via CDP (Raw)

If your agent framework doesn't have built-in browser profiles, you can connect directly using any CDP library.

Example using Playwright (Node.js):

```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.connectOverCDP('http://VPS_IP:9222');
  const contexts = browser.contexts();
  const page = contexts[0]?.pages()[0] || await contexts[0].newPage();
  
  await page.goto('https://www.google.com');
  console.log('Title:', await page.title());
  
  // Don't close browser — it's persistent!
  // browser.close() would kill Chrome for everyone
})();
```

Example using Puppeteer:

```javascript
const puppeteer = require('puppeteer-core');

(async () => {
  const browser = await puppeteer.connect({
    browserURL: 'http://VPS_IP:9222',
  });
  
  const pages = await browser.pages();
  const page = pages[0] || await browser.newPage();
  await page.goto('https://www.google.com');
  console.log('Title:', await page.title());
})();
```

Example using Python websockets (raw CDP):

```python
import websockets, json, asyncio

async def navigate(url):
    # First, get the page target
    # curl http://VPS_IP:9222/json/list → get webSocketDebuggerUrl
    ws_url = "ws://VPS_IP:9222/devtools/page/PAGE_ID"
    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps({
            "id": 1,
            "method": "Page.navigate",
            "params": {"url": url}
        }))
        result = await ws.recv()
        print("Navigated:", result)

asyncio.run(navigate("https://www.google.com"))
```

---

## Connecting an AI Agent to the Virtual Computer

This is the **most important section** for other AI agents. The Docker setup gives you a virtual computer — but the agent needs to actually *use* it. This section covers the full integration: browser automation, shell access, and making the virtual computer the agent's **primary tool**.

### The Big Picture

The virtual computer is **not just a browser**. It's a full Linux OS that the AI agent can use like a human uses their computer:

```
AI Agent (any location)
  │
  ├── 🌐 Browser Control (CDP WebSocket)
  │   └── ws://VPS_IP:9222
  │       → Navigate, click, type, screenshot, read DOM
  │       → Persistent login sessions (Gmail, etc.)
  │       → Human can spectate simultaneously
  │
  ├── 💻 Shell Access (SSH → docker exec)
  │   └── ssh user@VPS_IP "docker exec iris-desktop [command]"
  │       → Run any Linux command
  │       → Install tools, run scripts, manage files
  │       → Full root access inside container
  │
  └── 👁️ Human Spectating (Web Desktop)
      └── https://VPS_IP:3001/
          → Real-time view of everything the agent does
          → Human can intervene (click, type) if needed
```

### Step 1: Browser Profile (OpenClaw-Specific)

OpenClaw has built-in support for remote CDP browser profiles. This is the cleanest integration:

```bash
# Create a browser profile pointing to the virtual computer's CDP
openclaw browser create-profile \
  --name iris-desktop \
  --cdp-url http://VPS_IP:9222 \
  --color "#00E273"
```

After this, the agent can use `--browser-profile iris-desktop` for any browser command, and it will control Chrome on the virtual computer instead of a local browser.

**Verification:**
```bash
openclaw browser profiles
# Should show:
# iris-desktop: running (N tabs) [remote]
#   cdpUrl: http://VPS_IP:9222, color: #00E273
```

**For non-OpenClaw agents:** Use any CDP client library (Playwright, Puppeteer, raw WebSocket) pointed at `http://VPS_IP:9222`. See the "Connecting an AI Agent via CDP (Raw)" section above.

### Step 2: Shell Access

The agent needs shell access for anything beyond browser automation — installing tools, running scripts, managing files on the virtual computer.

**Pattern: SSH → docker exec**
```bash
# Run a command inside the virtual computer
ssh user@VPS_IP "docker exec iris-desktop [command]"

# Examples:
ssh user@VPS_IP "docker exec iris-desktop uname -a"
ssh user@VPS_IP "docker exec iris-desktop free -h"
ssh user@VPS_IP "docker exec iris-desktop apt-get install -y python3"
ssh user@VPS_IP "docker exec iris-desktop python3 -c 'print(1+1)'"
```

**For interactive sessions:**
```bash
ssh user@VPS_IP "docker exec -it iris-desktop bash"
```

**Important:** The agent needs SSH access to the VPS. Set up SSH keys so the agent can connect without password prompts.

### Step 3: Configure Agent Knowledge

The agent needs to **know** about the virtual computer and **when to use it**. This is the most critical step — without explicit routing rules, the agent will default to whatever browser tool it had before.

**What to add to the agent's configuration/knowledge:**

1. **Virtual computer exists** — endpoint URLs, login credentials, capabilities
2. **When to use it** — routing rules (virtual computer vs lightweight tools)
3. **How to access it** — browser profile name, SSH command patterns

**Example routing decision tree (add to agent config):**

```
Web task received
  │
  ├─ Needs login / session persistence / anti-bot bypass?
  │   └─ YES → Virtual Computer (CDP)
  │        Examples: Gmail, e-commerce seller panels, Google services
  │
  ├─ Simple public page fetch / scrape?
  │   └─ YES → Lightweight tool (Firecrawl, Exa, curl)
  │        Examples: Public articles, API docs, price checks
  │
  └─ Complex multi-step browser automation?
      └─ YES → Virtual Computer (CDP)
           Examples: Fill forms, navigate SPAs, download reports
```

### Step 4: Verification — Test All Three Channels

After setup, verify the agent can use all three access channels:

**Test 1: Browser (CDP)**
```bash
# Ask the agent to navigate to a page
openclaw agent -m "Use browser profile iris-desktop, navigate to https://www.wikipedia.org, tell me the page title"
# Expected: Agent reports Wikipedia page title
```

**Test 2: Persistent Login**
```bash
# After human logs into Gmail via web desktop, ask agent to check
openclaw agent -m "Use browser profile iris-desktop, go to https://mail.google.com, tell me if you're logged in"
# Expected: Agent sees inbox (not login page)
```

**Test 3: Shell Access**
```bash
# Ask the agent to run a command on the virtual computer
openclaw agent -m "SSH to VPS and run: docker exec iris-desktop uname -a && whoami && free -h"
# Expected: Agent returns Linux kernel info, user, and memory stats
```

**Test 4: Human Spectating**
```
1. Human opens https://VPS_IP:3001/ in their browser
2. Ask the agent to navigate to a visible page (e.g., Google Maps)
3. Human should see Chrome navigating in real-time on the web desktop
4. Both channels (agent CDP + human spectating) work simultaneously
```

### What the Agent Can Now Do

With browser + shell + persistent sessions, the agent has capabilities that were previously impossible:

| Capability | How | Example |
|---|---|---|
| **Browse as human** | CDP (headed Chrome, not headless) | Google doesn't block, CAPTCHA-free |
| **Persistent logins** | Chrome profile in Docker volume | Login to Gmail once, stays logged in for weeks |
| **Run any Linux command** | SSH → docker exec | Install Python, run scripts, process files |
| **Install tools** | apt-get / pip / npm inside container | Add ffmpeg, imagemagick, pandoc, whatever needed |
| **Manage files** | Shell + persistent /config volume | Download, process, upload files |
| **Human oversight** | Web desktop at :3001 | Human watches agent in real-time, can intervene |
| **Multi-tool automation** | Combine browser + shell | Scrape a page → process data with Python → email results |

### Security Considerations

- **CDP is unencrypted** — the WebSocket connection between agent and Chrome is plaintext. For production, consider SSH tunneling or a VPN.
- **Container has root access** — the agent can install/delete anything inside the container. The Docker volume boundary prevents escape to the host, but be mindful of what you expose.
- **Web desktop credentials** — the HTTPS web desktop uses basic auth (user/password in docker-compose.yml). Change the default password for production.
- **Port exposure** — ports 3000, 3001, 9222 are open to the internet. Consider firewall rules (ufw/iptables) to restrict access to known IPs.

---

## Key Lessons Learned

### 1. Headless Chrome is Dead for Google Services
Google aggressively detects and blocks headless browsers. Any automation involving Google login (Gmail, Google Workspace, etc.) **must** use headed Chrome with a real display. This is the fundamental reason we need a full desktop environment, not just a headless CDP container.

### 2. Chrome M113+ CDP Localhost Hardcode is Poorly Documented
This is perhaps the most important gotcha in this entire guide. The `--remote-debugging-address=0.0.0.0` flag is silently ignored. You will find hundreds of guides online that recommend it — they're all outdated. The socat bridge is the only reliable workaround that doesn't require patching Chrome.

### 3. LinuxServer Images Changed Init Script Paths
Older documentation shows `/config/custom-cont-init.d/` for init scripts. Newer images expect `/custom-cont-init.d/` at root level. The solution is an extra volume mount: `./config/custom-cont-init.d:/custom-cont-init.d`. This way scripts live in the persistent volume but are mounted where the image expects them.

### 4. s6 Custom Services Don't Auto-Register in Newer Images
The `custom-services.d` directory in newer linuxserver images does NOT auto-register as s6 service directories. Don't waste time creating `run` files in `/custom-services.d/`. Use XFCE autostart with a watchdog script instead — it's simpler and more predictable.

### 5. Direct .deb Download > apt Repository on Some VPS
`apt-get update` with the Google Chrome repository hangs on certain VPS providers. The direct `.deb` download from Google's CDN (`dl.google.com/linux/direct/`) is universally reliable and faster.

### 6. Persistent Profile = Persistent Login
Chrome's `--user-data-dir` flag pointed at a directory inside `/config/` means all browser state (cookies, sessions, localStorage, saved passwords) persists across container restarts. Login to Gmail once, and it stays logged in for weeks.

### 7. docker-compose v1 vs v2 Matters
If your VPS has `docker-compose` (v1, Python-based) vs `docker compose` (v2, Go plugin), use the correct syntax. The hyphenated `docker-compose` is v1. Commands will silently fail or error if you use the wrong one.

### 8. shm_size is Critical for Chrome in Docker
Chrome uses `/dev/shm` for shared memory. Docker defaults to 64MB, which causes Chrome to crash or behave erratically with multiple tabs. Always set `shm_size: "2gb"` (or at minimum "512m").

### 9. seccomp:unconfined for Chrome Sandbox
Chrome's built-in sandbox requires system calls that Docker's default seccomp profile blocks. `seccomp:unconfined` is the simplest fix. For production, you could create a custom seccomp profile that allows only what Chrome needs.

### 10. AI Agent Session Context ≠ File System State

After deploying the virtual computer, the AI agent (Iris) was still referencing **old URLs and container names** from a previous failed approach (port 6080, noVNC, `iris-chrome`) — even though all config files (`AGENTS.md`, `TOOLS.md`, memory files) had already been updated with the correct information.

**Root cause:** AI agents running on frameworks like OpenClaw maintain a **session context** in memory. When the agent's session started, it loaded the old config. Updating files on disk doesn't automatically propagate into the agent's active session — the agent needs to either:

1. **Restart the gateway** (`openclaw gateway stop && openclaw gateway start`) — forces a fresh session that reads updated files
2. **Compact the session** (`/compact`) — summarizes existing context and re-reads files
3. **Explicitly tell the agent** to re-read specific files — works but fragile

**The lesson:** When you change an AI agent's configuration (endpoints, credentials, tool descriptions), the agent won't pick it up until its session reloads. This is analogous to editing a config file but forgetting to restart the service. Always restart/compact after significant config changes.

### 11. HTTPS Required for Modern Web Desktop Streaming

The webtop image serves its web desktop on both HTTP (:3000) and HTTPS (:3001). Some browsers and network configurations will reject the HTTP endpoint with "This application requires a secure connection (HTTPS)." **Always use the HTTPS endpoint (:3001) as the primary URL** for human access. The browser will show a self-signed certificate warning — click through it (Advanced → Proceed).

### 12. Remote CDP Control Works Cross-Network

CDP WebSocket connections work across networks without issues. In our setup, the Mac Mini (local machine) successfully controlled Chrome on the VPS via:

```python
# From Mac Mini → VPS CDP → Chrome
import websockets, json, asyncio

async def navigate():
    ws_url = "ws://VPS_IP:9222/devtools/page/PAGE_ID"
    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps({
            "id": 1,
            "method": "Page.navigate",
            "params": {"url": "https://en.wikipedia.org"}
        }))
        result = await ws.recv()
        print("Navigated:", result)

asyncio.run(navigate())
```

This confirms the full chain works: **AI agent (any location) → CDP WebSocket → socat bridge → Chrome on VPS**. The human can simultaneously watch via the web desktop. Both channels (CDP automation + human spectating) work concurrently without interference.

### 13. OpenClaw Remote Browser Profiles for CDP

OpenClaw's `openclaw browser create-profile --cdp-url http://VPS_IP:9222` creates a browser profile that points to a remote Chrome instance instead of launching a local one. This is the cleanest way to give an OpenClaw agent access to the virtual computer's browser — the agent uses its normal browser tools, but they control Chrome on the VPS instead of locally. The profile shows as `[remote]` in `openclaw browser profiles` and reports the correct tab count from the remote Chrome.

### 14. Virtual Computer = Full OS, Not Just Chrome

The biggest insight: the value of the virtual computer is **not just browser automation**. It's a full Linux OS the agent can SSH into and run arbitrary commands. This transforms the agent from "chatbot that can browse" to "AI with its own computer." Shell access (SSH → docker exec) enables: installing tools (apt-get/pip/npm), running scripts (Python, Node, bash), managing files, and combining browser automation with server-side processing. The browser is the most visible use case, but shell access is what makes this a true virtual computer.
---

## Complete File Listing

```
~/iris-vm/
├── docker-compose.yml                          # Main compose file
└── config/
    ├── custom-cont-init.d/
    │   └── 01-install-chrome.sh                # Installs Chrome + socat
    ├── scripts/
    │   └── chrome-cdp-service.sh               # Watchdog (auto-restart Chrome + socat)
    ├── .config/
    │   └── autostart/
    │       └── chrome-cdp-service.desktop      # XFCE autostart for watchdog
    ├── Desktop/
    │   └── chrome-cdp.desktop                  # Desktop shortcut
    └── .chrome-profile/                        # Chrome persistent user data
        ├── Default/                            # Default Chrome profile
        │   ├── Cookies                         # Session cookies (Gmail, etc.)
        │   ├── Login Data                      # Saved passwords
        │   └── ...
        └── ...
```

---

## Quick Reference Card

| What | How |
|---|---|
| Start container | `cd ~/iris-vm && docker-compose up -d` |
| Stop container | `cd ~/iris-vm && docker-compose down` |
| Restart container | `cd ~/iris-vm && docker-compose restart` |
| View logs | `docker logs iris-desktop --tail 100` |
| Shell into container | `docker exec -it iris-desktop bash` |
| Check Chrome status | `docker exec iris-desktop pgrep -a chrome` |
| Check socat status | `docker exec iris-desktop pgrep -a socat` |
| Check CDP | `curl http://VPS_IP:9222/json/version` |
| Open web desktop | `http://VPS_IP:3000/` |
| Manually start services | `docker exec iris-desktop bash /config/scripts/chrome-cdp-service.sh &` |
| Install more software | Edit `config/custom-cont-init.d/01-install-chrome.sh`, then recreate |
| View watchdog log | `docker exec iris-desktop cat /config/scripts/chrome-cdp.log` |

---

*This guide was written from hands-on experience setting up a virtual computer for the Iris AI agent at Zuma Indonesia, March 2026. The Chrome CDP localhost bug and socat workaround were discovered through systematic debugging after multiple failed approaches.*
