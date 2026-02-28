# Clawbox — OpenClaw-Ready macOS VMs

**Source:** https://github.com/joshavant/clawbox  
**Date:** 2026-02-28  
**Tags:** #openclaw #macos #vm #virtualization #tart #mutagen #developer-tools #ios  
**Stars:** 363 ⭐ | **Version:** v1.2.3 (Feb 18 2026) | **Language:** Python 96.8%

---

## What It Is

Clawbox is a tool for deploying OpenClaw-ready macOS VMs on a Mac host. Each OpenClaw instance runs in its own isolated VM. Built on **Tart** (Apple Silicon macOS virtualization).

Two audiences:
- **Standard users:** want one simple command to spin up OpenClaw in a VM
- **Developer users:** want multiple concurrent VMs with bidirectional host sync for OpenClaw development

---

## Quick Start

```bash
brew install joshavant/tap/clawbox
clawbox image build   # one-time, large download, takes several minutes
clawbox up
# Login with password: clawbox
# Then inside VM:
openclaw onboard --install-daemon
```

---

## Standard Mode

Install latest official OpenClaw in a macOS VM:

```bash
clawbox up

# With optional services:
clawbox up \
  --add-playwright-provisioning \
  --add-tailscale-provisioning \
  --add-signal-cli-provisioning

# SSH into clawbox:
ssh clawbox-1@$(clawbox ip 1)
# password: clawbox
```

---

## Developer Mode (Advanced)

For OpenClaw contributors or custom payload workflows:
- Syncs local OpenClaw source + payload into VM via **Mutagen** (bidirectional)
- Each VM can use different source/payload copies for concurrent testing
- Synced checkouts become the VM's `openclaw` command

```bash
# Single VM:
clawbox up --developer \
  --openclaw-source ~/Developer/openclaw-1 \
  --openclaw-payload ~/Developer/openclaw-payloads/clawbox-1

# Two VMs (Apple allows max 2 concurrent macOS VMs per host):
clawbox up --developer --number 1 \
  --openclaw-source ~/Developer/openclaw-1 \
  --openclaw-payload ~/Developer/openclaw-payloads/clawbox-1

clawbox up --developer --number 2 \
  --openclaw-source ~/Developer/openclaw-2 \
  --openclaw-payload ~/Developer/openclaw-payloads/clawbox-2
```

**Dev loop inside VM:**
```bash
cd ~/Developer/openclaw
pnpm gateway:watch  # hot-reload as host source changes
```

Note: `dist/` excluded from sync so build artifacts stay VM-local.

---

## Optional Provisioning Flags

| Flag | What it installs |
|------|-----------------|
| `--add-tailscale-provisioning` | Tailscale (requires interactive approval after VM creation) |
| `--add-playwright-provisioning` | Playwright + browsers |
| `--add-signal-cli-provisioning` | signal-cli (with optional payload sync) |

**signal-cli payload sync (Developer-only):**
```bash
clawbox up --developer \
  --openclaw-source ~/Developer/openclaw-1 \
  --openclaw-payload ~/Developer/openclaw-payloads/clawbox-1 \
  --add-signal-cli-provisioning \
  --signal-cli-payload ~/.local/share/signal-cli
```
Single-writer locking enforced for signal payload paths.

---

## VM Lifecycle Commands

| Command | What it does |
|---------|-------------|
| `clawbox up` | Create + provision + launch VM |
| `clawbox down` | Stop VM |
| `clawbox delete` | Delete VM |
| `clawbox recreate 1` | down + delete + up with same original flags |
| `clawbox status` | Show all clawbox-* VMs |
| `clawbox status <number>` | Detail for single VM |
| `clawbox ip <number>` | Get VM IP address |
| `clawbox image build` | Build base macOS image (one-time) |
| `clawbox image rebuild` | Rebuild base image |

---

## What Clawbox Installs in Each VM

- Homebrew
- Node.js
- Mutagen (for bidirectional file sync)
- OpenClaw
- Terminal.app desktop shortcut
- SSH access (`clawbox-<number>`, password: `clawbox`)
- macOS defaults (dark mode, Siri off, Setup Assistant suppressed, lobster-toned wallpaper 🦞)
- Tart Guest Agent (clipboard sharing)
- Optional: Tailscale, Playwright, signal-cli

---

## Key Technical Details

- **Virtualization backend:** [Tart](https://tart.run/) — Apple Silicon macOS VMs
- **File sync:** [Mutagen](https://mutagen.io/) — bidirectional host↔VM sync
- **macOS VM limit:** Apple allows max **2 concurrent** macOS VMs per Apple host (EULA)
- **Infrastructure as code:** Ansible for provisioning, Packer for image builds
- **CI:** Cirrus CI (`.cirrus.yml`)
- **Language:** Python (96.8%), Shell (2.4%)

---

## Use Cases / Why This Matters

1. **Isolation:** Run OpenClaw in its own VM, separate from host environment
2. **Multiple concurrent instances:** Run 2 OpenClaw VMs simultaneously (e.g., separate agents for different tasks or clients)
3. **Clean testing environment:** Developer mode for testing OpenClaw changes without affecting host
4. **Playwright in VM:** Heavy browser automation isolated from host
5. **Tailscale:** VPN-accessible OpenClaw from anywhere
6. **signal-cli:** Signal messaging integration for OpenClaw

---

## Relevance for Iris/Zuma

**Low immediate priority** (Iris is already running on VPS). But relevant if:
- Want to run multiple isolated OpenClaw instances on Mac Mini M4
- Need to isolate Playwright browser from host
- Testing/developing OpenClaw modifications
- Want Tailscale-accessible agent without VPS dependency

**Mac Mini M4 note:** Supports up to 2 concurrent macOS VMs. Each VM would need its own memory allocation — on 16GB, this limits VM RAM significantly. More practical to use Docker or VPS for additional instances.

---

## Installation

```bash
# Via Homebrew tap:
brew install joshavant/tap/clawbox

# Or install from source:
git clone https://github.com/joshavant/clawbox
cd clawbox
pip install -e .
```

GitHub: https://github.com/joshavant/clawbox  
Latest: v1.2.3 (2026-02-18)
