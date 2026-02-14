# How OpenClaw Agent "Larry" Got Millions of TikTok Views in One Week

**Source:** Twitter/X Thread  
**Author:** @oliverhenry (Oliver Henry + Larry the AI agent)  
**Date:** 2026-02-14  
**Link:** https://x.com/oliverhenry (thread paste)

---

## Key Points

- **AI agent "Larry"** (running on old gaming PC via OpenClaw) fully automates TikTok slideshow creation — 500K+ views in 5 days, top post 234K views
- **Zero manual work** for image creation or caption writing — user only adds trending music (60 seconds/post)
- **TikTok photo carousels** (6-slide format) get 2.9x more comments, 1.9x more likes, 2.6x more shares vs video in 2026
- **Revenue impact:** $588 MRR from app subscriptions, $4K+ from meme coin community around Larry
- **Cost:** ~$0.50/post API costs ($0.25 with OpenAI Batch API) — trivial compared to time saved
- **Hook formula breakthrough:** `[Another person] + [conflict/doubt] → showed them AI → changed their mind` = consistent 100K+ views
- **Key failure:** Self-focused hooks ("See your room in 12 styles") = dead (<3K views). Story-driven hooks = viral.

---

## Technical Details

### Architecture

**Hardware:**
- Old gaming PC (NVIDIA 2070 Super GPU) running Ubuntu under desk
- Alternative: Raspberry Pi, cheap VPS, Mac Mini — minimal requirements (2GB RAM, 1-2 vCPU, 20GB SSD)

**Stack:**
- **OpenClaw** (open source AI agent framework) — gives Claude persistent identity, memory, tool access
- **Claude (Anthropic)** — primary AI model
- **OpenAI gpt-image-1.5** — image generation API ($0.50/post, $0.25 with Batch API)
- **Postiz** — social media scheduling tool with TikTok API (uploads slideshows as drafts)
- **WhatsApp** — human ↔ agent communication channel

**Agent Capabilities:**
- Persistent personality & memory (skill files + memory files)
- File read/write access
- Image generation (OpenAI API)
- Code execution (Python overlays for text on images)
- TikTok posting via Postiz API
- RevenueCat analytics access (subscription metrics, MRR, churn)
- X browsing (via Bird skill from @steipete)

### Image Generation Workflow

**Challenge:** Room transformations need consistency — SAME room across 6 slides, only style changes

**Solution: Lock the architecture**
- Write ONE hyper-detailed room description (dimensions, window position, door location, camera angle, furniture size, ceiling height, floor type)
- Copy-paste exact description into all 6 prompts
- ONLY change style variables (wall color, bedding, decor, lighting)

**Prompt Engineering Example:**
```
iPhone photo of a small UK rental kitchen. Narrow galley style kitchen, 
roughly 2.5m x 4m. Shot from the doorway at the near end, looking straight 
down the length. Countertops along the right wall with base cabinets and 
wall cabinets above. Small window on the far wall, centered, single pane, 
white UPVC frame, about 80cm wide. Left wall bare except for a small fridge 
freezer near the far end. Vinyl flooring. White ceiling, fluorescent strip 
light. Natural phone camera quality, realistic lighting. Portrait orientation. 

**Beautiful modern country style. Sage green painted shaker cabinets with 
brass cup handles. Solid oak butcher block countertop. White metro tile 
splashback in herringbone. Small herb pots on the windowsill...**
```
(Bold section = only part that changes per slide)

**Why gpt-image-1.5:**
1. Matches app output (Snugly uses same model) — marketing IS the product, no bait-and-switch
2. Photorealistic with "iPhone photo" + "realistic lighting" prompts — looks like real phone photos, not AI renders

**Failed Approach:** Stable Diffusion (local GPU) — free but uncanny/AI-looking output, engagement killer

### Posting Workflow

**Automated (Larry):**
1. Generate 6 images via OpenAI API (locked architecture + varying styles)
2. Add text overlays via Python code (hook on slide 1)
3. Write story-style caption + max 5 hashtags
4. Upload to TikTok as draft via Postiz API (`privacy_level: "SELF_ONLY"`)
5. Send caption to user via WhatsApp

**Manual (Oliver — 60 seconds):**
1. Open TikTok drafts
2. Pick trending sound (can't automate via API)
3. Paste caption
4. Publish

**Scheduling:** Cron jobs at peak engagement times, can pre-generate via OpenAI Batch API (50% cheaper) overnight

### Skill Files & Memory System

**Skill files** (markdown, 500+ lines for TikTok):
- Every rule, formatting spec, lesson learned from failures
- Image sizes (1024x1536 portrait, always)
- Prompt templates with locked architecture
- Text overlay rules (6.5% font size, positioning, line length limits to avoid compression)
- Caption formulas, hashtag strategy
- Hook formats that work
- Failure log (never repeat mistakes)

**Memory files** (long-term persistence):
- Every post, view count, performance insight logged
- Referenced for brainstorming hooks (not guessing, data-driven)
- Compounds over time — every failure → rule, every success → formula

**Skill sources:**
- Custom-written for TikTok workflow
- RevenueCat skill (from Clawhub, made by @jeiting) — subscription analytics, MRR, churn tracking
- Bird skill (from Clawhub, made by @steipete) — X browsing

---

## Takeaways

### What Works

**Hook Formula (The Breakthrough):**
```
[Another person] + [conflict/doubt] → showed them AI → they changed their mind
```

Examples that cleared 100K+ views:
- "My landlord said I can't change anything so I showed her what AI thinks it could look like" → 234K
- "I showed my mum what AI thinks our living room could be" → 167K
- "My landlord wouldn't let me decorate until I showed her these" → 147K

**Why it works:** Creates mini-story before swipe. Human moment, not product pitch. Picture the landlord's face, the mum being impressed.

**Slideshow Format (2026 TikTok Algorithm):**
- 6 slides exactly (TikTok's sweet spot)
- Text overlay on slide 1 (hook)
- Story caption that relates to hook + mentions app naturally
- Max 5 hashtags (TikTok's current limit)
- Trending music (manual, can't automate)

**Image Quality Rules:**
- Portrait 1024x1536 (landscape causes black bars → kills engagement)
- Photorealistic = "iPhone photo" + "realistic lighting" in prompt
- No people (didn't work)
- Signs of life in "before" rooms (TV, mugs, remote) — avoid empty show home look

**Text Overlays:**
- 6.5% font size minimum (5% = unreadable on mobile)
- Position considering TikTok status bar (don't hide behind UI)
- Line length limits to avoid horizontal compression

### What Failed

**Hooks (Self-Focused → Dead):**
- "Why does my flat look like a student loan" → 905 views
- "See your room in 12+ styles before you commit" → 879 views
- "The difference between $500 and $5000 taste" → 2,671 views

**Why:** Talking about "us", "our problems", "our app features" — nobody cares. Need other person's reaction + conflict.

**Image Generation:**
- Vague prompts → different rooms per slide → looks fake
- Landscape orientation → black bars
- Adding people → didn't work

**Text:**
- Too small font (5%)
- Positioned too high (hidden by status bar)
- Long lines → horizontal compression

### Lessons for AI Agent Systems

**1. Skill files are everything**
- "The agent is only as good as its memory"
- Document every mistake immediately so agent never repeats
- Include examples, be obsessively specific
- Compounds over time (20+ rewrites in first week)

**2. Start bad, iterate fast**
- First posts will be embarrassing (wrong sizes, unreadable text, flopping hooks)
- Log failures → update skill files → repeat
- Every failure becomes a rule, every success becomes a formula

**3. Agent + human collaboration sweet spot**
- Agent: 95% of work (generation, research, posting automation)
- Human: 5% finishing touch that can't automate (trending music selection, final hook approval)

**4. API costs are negligible vs time saved**
- Tried local Stable Diffusion (free) but quality gap massive
- OpenAI API = $0.50/post ($0.25 batch) — tiny cost for photorealistic output
- Don't optimize for wrong thing (free generation vs quality/time)

**5. Agent learns from real metrics**
- RevenueCat integration → track MRR, subscriptions, churn
- Performance data logging → data-driven hook brainstorming
- Not guessing, referencing actual results

### Application to Zuma

**Potential use cases:**
- **Product launch content** — T8 new releases, seasonal collections (Merci series, etc.)
- **Store opening announcements** — TikTok slideshows for new branch launches
- **Before/after transformations** — "My wardrobe before/after discovering Zuma" hooks
- **Customer testimonials automation** — Agent generates story-driven content from review data
- **Trend monitoring** — Agent browses TikTok/X for trending formats, suggests adaptations

**Implementation considerations:**
- Hardware: VPS agent (Atlas/Apollo) or dedicated Raspberry Pi
- Image generation: Product photos → styled slideshows (similar to room transformations)
- Hook formula adaptation: Customer stories, stylist reactions, family moments
- Posting workflow: Draft → manual music selection → publish (same 60-second manual step)

**Cost-benefit:**
- $0.50/post trivial vs content creation time
- 1 viral post (100K+ views) = brand awareness boost >> ad spend
- Agent compounds learning (skill files improve with every post)

**Risk:**
- Over-automation → loss of brand authenticity (need human touch on hooks)
- TikTok algorithm changes (format that works today may not work in 6 months)
- Requires active iteration & monitoring (not set-and-forget)

---

## Tags

#ai-agents #openclaw #tiktok-marketing #automation #viral-content #claude-ai #social-media #content-generation #image-ai #openai #marketing-automation #skill-files #persistent-memory

---

**Apps mentioned:**
- **Snugly** — AI room redesign app (iOS)
- **Liply** — AI lip filler preview app (iOS)

**Tools mentioned:**
- OpenClaw (open source AI agent framework)
- Postiz (social media scheduling + TikTok API)
- OpenAI gpt-image-1.5 (image generation)
- RevenueCat (subscription analytics)
- Clawhub (skill repository)

**Follow:**
- Oliver: @oliverhenry (X)
- Larry: @LarryClawerence (X)
