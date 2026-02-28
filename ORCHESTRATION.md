# ORCHESTRATION.md — Delegation & Response Protocol

_Read this BEFORE spawning any sub-agent._
_For agent roster, nanobot exec syntax, and pipeline patterns → see `AGENTS.md` (this workspace)._
_For skill routing → see `SKILLS_INDEX.md`._
_Last updated: 2026-02-28 (added Step 2b Plan-Review-Execute Gate, Step 4b Retry Policy, reasoning annotations cross-ref)_

---

## Step 0 — Message Isolation & Context Tagging (SEBELUM APAPUN)

🚨 **Ini adalah langkah PERTAMA setiap kali ada pesan masuk. Tanpa ini, task result bisa salah kirim.**

### 0a. Catat Sender Context

```
origin_phone   = {phone number or group ID from incoming message}
origin_channel = whatsapp | telegram | discord
origin_name    = {display name / contact name}
timestamp      = {HH:MM WIB}
```

### 0b. Isolation Rules

1. **SETIAP delegasi** ke sub-agent/nanobot HARUS include `origin_phone` + `origin_name` di prompt
2. **SETIAP heartbeat entry** HARUS di-tag dengan `origin_phone`
3. **SETIAP delivery** HARUS di-crosscheck:
   - "Apakah ini phone/group yang BENAR?"
   - "Apakah task ini memang diminta oleh user ini?"
4. **JANGAN PERNAH** kirim hasil task user A ke user B
5. **JANGAN PERNAH** campur konteks percakapan antar user
6. **Kalau ragu** channel mana → JANGAN kirim. Tahan dan tanya Wayan.

### 0c. Context Tracking (In-Memory)

Selama session, Iris HARUS maintain mental map:
```
active_contexts = {
  "+628983539659": {
    "name": "Wayan",
    "current_topic": "RO Request Royal Plaza",
    "pending_tasks": ["RO Box"],
    "last_msg": "14:30 WIB"
  },
  "+6285101726716": {
    "name": "Nisa",
    "current_topic": "Sales report",
    "pending_tasks": [],
    "last_msg": "14:25 WIB"
  }
}
```
Setiap pesan masuk → update `active_contexts`. Setiap delivery → crosscheck dengan context.

### 0d. Heartbeat Template (Per-User)

```markdown
# Pending Tasks for {+62812345678}
## User: {Nama}
## Channel: whatsapp

- [ ] **{Task Name}** — delegated to {agent}, started: {HH:MM WIB}, ETA: ~{X}m
  - Origin: {+62812345678}
  - Origin Name: {Nama}
  - Check: {outbox path or session_id}
  - Deliver TO: {+62812345678 via whatsapp} ← HANYA ke nomor ini
  - Content: {apa yang dikirim — summary/file/link}
```

**CRITICAL:** Field `Deliver TO` HARUS ada dan HARUS match `Origin`. Tanpa field ini, Iris bisa salah kirim.
---

## Step 1 — Pick the Right Agent

The full agent roster and execution priority is in `AGENTS.md § Task Delegation`. Quick routing:

| Request Type | Indonesian Keywords | Agent |
|---|---|---|
| Stock, inventory, sisa stok | "cek stok", "berapa sisa", "inventory" | **Argus** (nanobot) |
| Sales data, omzet, revenue | "sales", "penjualan", "omzet", "revenue" | **Argus** (nanobot) |
| Report, laporan, rekap | "laporan", "rekap", "summary" | **Argus** → **Eos** |
| PPT, deck, presentasi | "PPT", "deck", "slide", "presentasi" | **Argus** → **Eos** (ALWAYS via Argus first) |
| Dashboard, web app | "dashboard", "web", "app", "visualisasi" | **Argus** → **Codex** |
| Script, kode, automasi | "script", "kode", "bikin", "automasi" | **Daedalus** (sessions_spawn) |
| Research, cari info, baca link | "cari info", "research", "baca link ini" | **Hermes** (sessions_spawn) |
| SQL planning, analisis kompleks | "analisis", "breakdown", "planning" | **Metis** (sessions_spawn) |
| Strategy, keputusan besar | "saran", "gimana baiknya", "strategi" | **Oracle** (advisory only) |

**Ambiguous?** Ask: _"Is this data, visuals, code, or advice?"_
- Data → Argus | Visuals/PPT → Argus then Eos | Code → Daedalus | Research → Hermes | Advice → Oracle

---

## Step 2 — Write a Good Prompt

Every prompt MUST have these **6 parts**. Missing any = agent guesses wrong.

**1. TASK** — One atomic action. Not "help with stocks". Yes: "Query active stock per series for Jatim, return total pairs."

**2. CONTEXT** — Always include:
- Wayan = System Developer at Zuma Indonesia, no IT background
- Zuma = footwear retail, 6 branches (Jatim, Jakarta, Sumatra, Sulawesi, Batam, Bali)
- DB = PostgreSQL VPS `167.71.198.86:5432`, database `openclaw_ops`
- What Wayan ACTUALLY wants (not just what he typed)

**2b. SKILL INJECTION** (NEW — 2026-02-28) — **WAJIB. Bukan opsional.**

Sebelum nulis prompt, Iris HARUS:
1. Identifikasi skill yang relevan dari `SKILLS_INDEX.md`
2. `read` SKILL.md tersebut
3. Extract critical domain facts (filters, column names, business rules)
4. Masukkan ke prompt sebagai `[Skill Reference]` + `[Critical Facts]`

Skills sekarang AUTO-DISCOVERED oleh OpenClaw di `workspace/skills/`. Subagent bisa `read` skill sendiri. Tapi Iris TETAP harus extract critical facts — jangan harap subagent baca sendiri.

```
[Skill Reference]: Baca `skills/{name}/SKILL.md` untuk detail lengkap.
[Critical Facts from Skill]:
- Filter toko: `branch = 'Bali'` di portal.store (BUKAN ILIKE nama)
- Exclude: category IN ('WHOLESALE','NON-RETAIL','EVENT')
- Sales: core.sales_with_product, filter is_intercompany = FALSE
```

**Kenapa wajib:** Tanpa skill injection, subagent ngarang domain knowledge → data salah. Contoh nyata: Bali deck pakai `ILIKE '%bali%'` → hanya 4/35 toko. Skill `zuma-branch` punya filter yang benar.

**Quick reference — skill selection:**
| Task domain | Load skill |
|------------|-----------|
| Toko/branch/store | `zuma-branch` |
| SQL/query/data | `zuma-data-analyst-skill` |
| PPT/deck | `eos-visual-skill` + `zuma-ppt-design` |
| SKU/produk | `zuma-sku-context` |
| Stok/gudang/RO | `zuma-warehouse-and-stocks` |

**3. DATA** — Where is the input? Be specific:
- Stock → `portal.v_stock_summary` or `mart.sku_portfolio_size`
- Sales → `portal.v_sales_detail` or `mart.sku_portfolio`
- Planogram → `portal.temp_portal_plannogram`
- Files → `~/.openclaw/workspace/` (outputs to `outbox/`)

**4. OUTPUT** — What format, saved where:
- Data → CSV to `~/.openclaw/workspace/outbox/filename_YYYY-MM-DD.csv`
- Summary → Markdown reply back to Iris (1-line status)
- Visual → Eos deploys to Vercel, returns URL
- Report → GDrive upload, share link (`--anyone --role writer`)

**5. CONSTRAINTS** — What NOT to do:
- Never contact anyone (WA, email) — reply to Iris only
- Never commit/push unless explicitly told
- Exclude intercompany (UBB/MBB) unless asked
- ALWAYS GROUP BY `kodemix`, never filter single `kode_besar`
- NEVER use `var_year_qty` for mid-year YoY

### Bad vs Good

❌ BAD: _"tolong cek stok surabaya"_
Argus doesn't know: which view, which branch_id, what filter, what format, where to save.

✅ GOOD:
```
Query portal.v_stock_summary WHERE branch_id = 'JATIM' AND is_active = TRUE.
Group by series. Return: series, total_qty, total_pairs. Exclude intercompany.
Save CSV to ~/.openclaw/workspace/outbox/stock_jatim_2026-02-22.csv.
Reply to Iris with 1-line summary when done.
```

❌ BAD (no skill injection): _"Query revenue Branch Bali 2025. Filter stores dengan nama mengandung 'Bali'."_
Ngarang filter sendiri tanpa baca skill → miss 31/35 toko.

✅ GOOD (with skill injection):
```
[Task]: Query total revenue + units + ASP Branch Bali 2025 vs 2024 YoY
[Skill Reference]: Baca skills/zuma-branch/SKILL.md + skills/zuma-data-analyst-skill/SKILL.md
[Critical Facts from Skill]:
- Toko Bali = portal.store WHERE branch = 'Bali' AND category = 'RETAIL' (35+ toko)
- BUKAN filter ILIKE '%bali%' (itu cuma match 4 mall stores)
- Sales: core.sales_with_product, JOIN matched_store_name, is_intercompany = FALSE
[Output]: Markdown summary ke Iris. Save detail CSV ke outbox/
[Constraints]: Exclude wholesale, konsinyasi, event. Include ruko stores.
```

---

## Step 2b — Plan-Review-Execute Gate (Complex Tasks)

🚨 **Untuk task kompleks (5+ steps atau cross-system), Iris WAJIB generate plan dan minta approval dari USER sebelum execute.**

### Kapan Gate Ini Aktif?

| Kondisi | Gate? | Contoh |
|---------|-------|--------|
| Simple query/lookup (<3 steps) | ❌ Skip | "cek stok Jatim" |
| Standard pipeline (3-4 steps, known pattern) | ❌ Skip | "buat PPT sales" (Argus→Eos = known) |
| Complex task (5+ steps) | ✅ **WAJIB** | "migrasi planogram semua toko" |
| Cross-system impact (DB + files + deploy) | ✅ **WAJIB** | "update semua RO + deploy dashboard" |
| Destructive/irreversible action | ✅ **WAJIB** | "hapus data lama", "reset planogram" |
| Ambiguous goal (multiple interpretations) | ✅ **WAJIB** | "improve the store performance" |

### Flow

```
COMPLEX TASK DETECTED (5+ steps / cross-system / destructive / ambiguous)
    │
    ├─ Step 1: Iris generates plan
    │   - Break goal into numbered steps
    │   - Identify which agent handles each step
    │   - Estimate total time
    │   - List risks/edge cases
    │   - Note what's IRREVERSIBLE
    │
    ├─ Step 2: Send plan to REQUESTING USER (bukan Wayan)
    │   Format:
    │   "Ini rencananya:
    │    1. [step] → [agent] (~Xm)
    │    2. [step] → [agent] (~Xm)
    │    ...
    │    Total estimasi: ~Ym
    │    ⚠️ [risks/notes]
    │    Lanjut?"
    │
    ├─ Step 3: WAIT for user approval
    │   - User says "lanjut" / "ok" / "gas" → Execute
    │   - User modifies plan → Update plan, re-confirm
    │   - User cancels → Stop, acknowledge
    │   - User silent >30 min → Remind once, then park task
    │
    └─ Step 4: Execute approved plan
        - Follow steps as approved
        - If deviation needed mid-execution → pause, inform user, get approval
        - On completion → report result back to user
```

### Plan Message Template (WhatsApp-friendly)

```
Ini rencananya buat [goal]:

1️⃣ [Step 1 description] → [Agent] (~Xm)
2️⃣ [Step 2 description] → [Agent] (~Xm)
3️⃣ [Step 3 description] → [Agent] (~Xm)
...

Total: ~Y menit
⚠️ [Catatan penting / risiko kalau ada]

Lanjut? 👍
```

### Rules
- **Approval dari USER yang request** — BUKAN dari Wayan (kecuali task menyangkut system/infra)
- **Kalau user = Wayan** — tetap tanya approval (Wayan juga mau review plan)
- **Jangan over-plan simple tasks** — "cek stok" tidak perlu plan. Gate ini HANYA untuk complex tasks.
- **Plan harus actionable** — tiap step harus jelas agent-nya dan estimasi waktunya
- **Mid-execution deviation** — kalau ada yang berubah (error, data tidak sesuai), PAUSE dan inform user sebelum lanjut


## Step 3 — Non-Blocking Response Protocol

🚨 **Iris WAJIB respond dalam <5 detik. JANGAN PERNAH block.**

### Response Flow (SETIAP message masuk)

```
PESAN MASUK
    │
    ├─ Step 0: Tag sender context
    │
    ├─ Cek: Apakah bisa dijawab langsung (<2 detik)?
    │   ├─ YA (info/memory/simple) → Jawab langsung ✅
    │   └─ TIDAK (perlu agent/script/query)
    │       │
    │       ├─ ACKNOWLEDGE dulu:
    │       │   "Oke, aku proses ya. Estimasi ~{X} menit."
    │       │   atau "Siap, lagi dibuatin. Nanti aku kabarin."
    │       │
    │       ├─ DELEGATE (background)
    │       │   - Nanobot: exec background: true
    │       │   - Sub-agent: sessions_spawn
    │       │
    │       ├─ HEARTBEAT (WAJIB — sebelum ngapa-ngapain lagi)
    │       │   Tulis ke heartbeat/{phone}.md
    │       │
    │       └─ READY for next message ✅
    │
    └─ Iris siap terima pesan berikutnya
```

### Non-Blocking Rules (HARD)

1. **Nanobot = ALWAYS `background: true`** — ZERO tolerance untuk synchronous calls
2. **Sub-agent = ALWAYS `sessions_spawn`** — dan JANGAN tunggu hasilnya
3. **Oracle = ALWAYS async** — spawn dan cek via heartbeat nanti
4. **Multi-step pipeline = acknowledge dulu** →  delegate → heartbeat → move on
5. **Sub-agent gagal = jangan retry inline** — Log ke heartbeat, retry di heartbeat berikutnya
6. **Result > 500 words = summarize** — 3 bullet points max, tawarkan "Mau detail lengkap?"

### Acknowledge Templates (pakai yang natural)

- "Oke, lagi diproses ya. ~5 menit."
- "Siap, aku buatkan dulu. Nanti aku kabarin hasilnya."
- "Noted! Lagi aku kerjain, bentar ya."
- "On it 👍 Estimasi ~{X} menit."

**JANGAN:** Diam sampai task selesai. JANGAN: Bilang "aku cek dulu" lalu menghilang 10 menit.

---

## Step 4 — Heartbeat & Proactive Follow-Up

🚨 **INI YANG PALING SERING GAGAL. Iris lupa follow-up = user menunggu tanpa kabar.**

### Heartbeat Protocol

Setelah delegate task apapun yang takes >30 detik, IMMEDIATELY tulis ke:
`~/.openclaw/workspace/heartbeat/{phone_or_group_id}.md`

**Rules:**
- Tulis heartbeat SEBELUM melakukan hal lain (sebelum baca message lain, sebelum delegate task lain)
- Per-user file di `heartbeat/` folder — BUKAN global `HEARTBEAT.md` (race condition)
- File harus punya format lengkap termasuk `Deliver TO` dan `Origin Name`

### Heartbeat Polling (SETIAP 5 menit)

```
SETIAP HEARTBEAT POLL:
    │
    ├─ List semua file di heartbeat/ folder
    │
    ├─ Untuk SETIAP file (per user):
    │   │
    │   ├─ Baca pending tasks
    │   │
    │   ├─ Untuk SETIAP task:
    │   │   │
    │   │   ├─ Poll status:
    │   │   │   - Nanobot: cek outbox/ folder
    │   │   │   - Sub-agent: session_status atau cek outbox
    │   │   │
    │   │   ├─ Status = SELESAI?
    │   │   │   ├─ YA:
    │   │   │   │   1. Format result (summarize jika >500 words)
    │   │   │   │   2. CROSSCHECK: Deliver TO == Origin phone? ← WAJIB
    │   │   │   │   3. Kirim ke user via channel yang benar
    │   │   │   │   4. Hapus entry dari heartbeat file
    │   │   │   │   5. Log ke memory/{date}.md
    │   │   │   │
    │   │   │   └─ BELUM:
    │   │   │       ├─ <10 menit → biarkan, cek lagi nanti
    │   │   │       ├─ 10-15 menit → update user: "Task X masih diproses, ~Y menit lagi"
    │   │   │       └─ >15 menit → ESKALASI:
    │   │   │           1. Cek error logs
    │   │   │           2. Retry 1x
    │   │   │           3. Jika masih gagal → report ke Wayan
    │   │   │
    │   │   └─ Status = ERROR?
    │   │       1. Log error
    │   │       2. Retry 1x (different approach jika bisa)
    │   │       3. Jika retry gagal → report ke user: "Maaf, ada error. Aku coba lagi / eskalasi ke Wayan."
    │   │
    │   └─ Jika semua tasks done → hapus file heartbeat
    │
    └─ Selesai polling, siap terima messages lagi
```

### Proactive Update Rules

| Elapsed | Action |
|---------|--------|
| 0-5 min | Tunggu (normal processing time) |
| 5-10 min | Poll status. Jika progress, tunggu. |
| 10-15 min | **WAJIB update user:** "Task X masih diproses, estimasi ~Y menit lagi." |
| >15 min | **WAJIB eskalasi:** Retry atau report error ke user + Wayan |
| >30 min | **HARD STOP:** Kirim apology ke user, cancel task, report ke Wayan |

### Anti-Pattern: Lupa Follow-Up

**Root cause yang sudah terjadi:**
- Iris delegate ke Argus → tidak tulis heartbeat → lupa → user menunggu 10+ menit tanpa kabar
- Iris delegate ke Daedalus → Daedalus selesai → Iris tidak poll → result stuck di outbox
- Iris terima message dari User B → konteks switch → lupa task User A masih pending

**Prevention:**
1. **heartbeat/ = source of truth** — Kalau tidak ada di heartbeat file, Iris PASTI lupa
2. **Tulis heartbeat SEBELUM context switch** — Sebelum handle user B, pastikan task user A sudah di-heartbeat
3. **Heartbeat polling = MANDATORY** — Bahkan kalau tidak ada pesan baru, poll heartbeat tiap 5 menit
---

## Step 4b — Retry Policy (Exponential Backoff)

🚨 **Retry WAJIB systematic, bukan asal coba lagi. Pattern: exponential backoff + max attempts + escalation.**

### Retry Table

| Failure Type | Max Retries | Backoff | Escalation |
|-------------|-------------|---------|------------|
| **Network timeout** (API, DB connection) | 3 | 2s → 4s → 8s | Report ke user, coba lagi di heartbeat berikutnya |
| **Rate limit** (429, quota exceeded) | 3 | 30s → 60s → 120s | Switch model/fallback jika ada, atau tunggu reset |
| **Sub-agent error** (Daedalus/Hermes/Metis gagal) | 2 | 0s (langsung retry dgn perbaikan prompt) | Retry 1x dgn different approach, lalu report ke user |
| **Nanobot error** (Argus/Eos/Codex gagal) | 2 | 5s → 15s | Switch ke fallback model (OpenRouter), lalu report |
| **Model error** (500, overloaded, context too long) | 2 | 10s → 30s | Fallback ke next model in chain, lalu report |
| **Auth error** (401, expired token) | 0 | — | Langsung report ke Wayan (butuh re-auth manual) |
| **Data error** (wrong schema, missing table) | 0 | — | Langsung report ke user + Wayan (butuh fix manual) |
| **Permission error** (403, read-only) | 0 | — | Langsung report ke Wayan |

### Retry Rules

1. **ALWAYS non-blocking** — Retry terjadi di heartbeat cycle, BUKAN inline. Jangan block user lain.
2. **Log setiap retry** — Tulis di heartbeat entry: `Retry #N at HH:MM — [reason]`
3. **Different approach on retry** — Jangan ulangi prompt yang sama persis. Ubah: simplify query, reduce data scope, switch agent, atau tambah context.
4. **Max 2 retries untuk agent errors** — Setelah 2x gagal dengan approach berbeda, STOP dan report ke user:
   "Maaf, task [X] gagal setelah 2x percobaan. Error: [summary]. Mau coba pendekatan lain atau eskalasi ke Wayan?"
5. **Transient vs Permanent** — Bedakan:
   - Transient (timeout, rate limit, 500) → retry with backoff
   - Permanent (auth, permission, schema) → DON'T retry, langsung escalate
6. **Fallback chain** — Untuk model errors:
   - OpenClaw: primary model → kimi-coding/k2p5 → google/gemini-3-flash-preview
   - Nanobot: primary → OpenRouter (env override)

### Heartbeat Entry Format (with Retry Tracking)

```markdown
- [ ] **{Task Name}** — delegated to {agent}, started: {HH:MM WIB}, ETA: ~{X}m
  - Origin: {phone}
  - Deliver TO: {phone via channel}
  - Status: RETRY #1 at 14:35 — timeout, retrying with smaller data scope
  - Previous attempts:
    - #0 (14:30): Failed — network timeout on DB query (portal.v_stock_summary)
    - #1 (14:35): Retrying — added LIMIT 1000, split by branch
```

### Anti-Pattern

- ❌ Retry prompt yang sama persis (definition of insanity)
- ❌ Retry synchronous / inline (blocks other users)
- ❌ Retry auth/permission errors (waste of time, needs manual fix)
- ❌ Retry >3x tanpa inform user (user thinks Iris disappeared)


---

## Step 5 — Nanobot Exec (Quick Reference)

```bash
# Argus
NANOBOT_CONFIG_PATH=~/.nanobot/config-argus.json nanobot agent -m "[task prompt]"

# Eos
NANOBOT_CONFIG_PATH=~/.nanobot/config-eos.json nanobot agent -m "[task prompt]"

# Codex
NANOBOT_CONFIG_PATH=~/.nanobot/config-codex.json nanobot agent -m "[task prompt]"
```

⚠️ **Always use `exec` with `background: true`** — never synchronous (blocks other users' queue).

For fallback models when Gemini rate-limited → see `AGENTS.md § Nanobot Agents`.
---

## Reference: DB Tables

| Use Case | Table |
|---|---|
| Stock summary per branch | `portal.v_stock_summary` |
| Stock by size (planogram) | `mart.sku_portfolio_size` |
| Sales detail | `portal.v_sales_detail` |
| Sales per article (aggregated) | `mart.sku_portfolio` |
| Planogram targets | `portal.temp_portal_plannogram` |
| Store info & branch mapping | `portal.store` (ALWAYS JOIN — never assume from name) |
| Monthly sales targets | `portal.store_monthly_target` |

DB: `167.71.198.86:5432` / `openclaw_ops` — credentials in TOOLS.md (hardcode in terminal, never .env)

Critical: GROUP BY `kodemix` | JOIN `portal.store` for location | Same-period YoY only

---

## Reference: Branch IDs

| Branch | branch_id |
|---|---|
| Jawa Timur | JATIM |
| Jakarta | JAKARTA |
| Sumatra | SUMATRA |
| Sulawesi | SULAWESI |
| Batam | BATAM |
| Bali | BALI |

---

## Reference: File Paths

| Purpose | Path |
|---|---|
| Iris workspace | `~/.openclaw/workspace/` |
| Output files (agent handoffs) | `~/.openclaw/workspace/outbox/` |
| Per-user heartbeat tracking | `~/.openclaw/workspace/heartbeat/{phone}.md` |
| Argus outbox | `~/.openclaw/workspace-argus-nanobot/outbox/` |
| Eos outbox | `~/.openclaw/workspace-eos-nanobot/outbox/` |
| Codex outbox | `~/.openclaw/workspace-codex-nanobot/outbox/` |

---

## Reference: Common Request Patterns (with Heartbeat)

### "Cek stok [branch]"
1. Tag sender (Step 0)
2. Acknowledge: "Oke, aku cek dulu ya."
3. Map branch name → branch_id
4. Call Argus with full 5-part prompt (background: true)
5. **Write to `heartbeat/{phone}.md`** ← MANDATORY before continuing
6. On heartbeat poll: check Argus outbox → format as text → deliver to **ORIGIN phone** → clear entry

### "Buat laporan/rekap/PPT"
1. Tag sender (Step 0)
2. Acknowledge: "Siap, aku buatkan ya. Estimasi ~10 menit."
3. Call Argus: gather data → save handoff JSON to Argus outbox (background: true)
4. **Write to `heartbeat/{phone}.md`** ← MANDATORY
5. On heartbeat when Argus done → call Eos with handoff path (background: true)
6. **Update `heartbeat/{phone}.md`** with Eos task (KEEP origin_phone sama!)
7. On heartbeat when Eos done → deliver Vercel URL to **ORIGIN phone** → clear entry

### "RO Request"
1. Tag sender (Step 0)
2. Acknowledge: "Oke, aku buatkan RO Request-nya ya."
3. **DEFAULT: Gunakan `step3-zuma-ro-surplus-skills`** (Surplus + Restock flow)
4. Load skill file: `zuma-business-skills/ops/zuma-plano-ro-skills/step3-zuma-ro-surplus-skills/SKILL.md`
5. Script: `build_ro_request.py` (di folder yang sama)
6. Data source: `portal.temp_portal_plannogram` (planogram) + `core.stock_with_product` (stok)
7. Load dependencies:
   - `zuma-business-skills/ops/zuma-data-analyst-skill/SKILL.md` (DB connection rules)
   - `zuma-business-skills/ops/zuma-sku-context/SKILL.md` (tier system, kode_mix)
   - `zuma-business-skills/ops/zuma-warehouse-and-stocks/SKILL.md` (gudang, RO flow)
8. Delegate ke **Daedalus** (script execution) — include semua skill content di prompt
9. **Write to `heartbeat/{phone}.md`** ← MANDATORY
10. When Daedalus done → GDrive upload → deliver link to **ORIGIN phone** → clear entry

   > **Alternatif EXPERIMENTAL (jika diminta box-only / Jatim saja):**
   > Load `zuma-business-skills/ops/zuma-plano-ro-skills/zuma-ro-box-only/SKILL.md` instead

### "Buat web/dashboard"
1. Tag sender (Step 0)
2. Acknowledge: "Siap, aku bikin dulu ya. Estimasi ~15 menit."
3. Call Argus: data schema → Argus outbox (background: true)
4. **Write to `heartbeat/{phone}.md`** ← MANDATORY
5. When Argus done → call Codex (background: true) → **update `heartbeat/{phone}.md`** (KEEP origin_phone!)
6. When Codex done → deliver Vercel URL to **ORIGIN phone** → clear entry

Full Pipeline steps (Pattern A/B/C) and handoff JSON schema → `AGENTS.md § Multi-Agent Pipeline Protocol`

---

## Checklist: Sebelum Respond ke User (SELF-CHECK)

Sebelum kirim APAPUN ke user, tanya diri sendiri:

- [ ] Apakah ini phone/group yang BENAR? (crosscheck origin_phone)
- [ ] Apakah task ini memang diminta oleh user ini? (crosscheck heartbeat)
- [ ] Apakah result ini sudah di-summarize? (jangan wall of text)
- [ ] Apakah ada task lain yang pending untuk user ini? (cek heartbeat)
- [ ] Apakah ada task pending dari user LAIN yang belum di-follow up? (cek semua heartbeat files)

---

_Update this file when new patterns are discovered or when AGENTS.md routing rules change._
