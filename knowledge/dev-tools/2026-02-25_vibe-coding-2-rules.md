# Vibe Coding 2.0 — 18 Rules to Be the Top 1% Builder

**Source:** X (Twitter) / Article by @Hartdrawss
**Date Fetched:** 2026-02-25
**Link:** https://x.com/Hartdrawss/status/2026198305362083910
**Author:** Founder/contractor — shipped 50+ MVPs across US, India, Dubai, Australia

---

## Key Points

### Core Thesis
> "The best vibe coders aren't the ones who know the most. They're the ones who know what NOT to build."

Waktu = aset utama. Setiap jam rebuild sesuatu yang sudah ada = jam yang dicuri dari fitur yang benar-benar penting. Vibe coding works hanya ketika kamu percaya tools yang sudah exist.

---

### DO's — 18 Rules

| # | Area | Tool/Approach | Why |
|---|---|---|---|
| 1 | Auth | Clerk / Supabase Auth | 2 minggu → 2 jam. Users tidak peduli auth |
| 2 | UI | Tailwind + shadcn/ui | Figma → working UI dalam 2-3 jam. Consistent, no raw CSS |
| 3 | State | Zustand + Server Components | No Redux. No Context 6 layers deep. Simple = ship |
| 4 | API | tRPC + Server Actions | End-to-end type safety, zero boilerplate |
| 5 | Deploy | Vercel one-click | Push to main = done. No SSH, no server config |
| 6 | DB | Prisma + Managed Postgres | Typed ORM, easy migration, no server management |
| 7 | Forms | Zod + React Hook Form | Validation predictable, data clean, no broken DB inputs |
| 8 | Payments | Stripe | 45 menit integrasi. PCI compliance gratis. Never DIY |
| 9 | Error tracking | Sentry | Setup hari 1. Tau apa yang broke sebelum user lapor |
| 10 | Analytics | PostHog / Plausible | Setup sebelum launch. Data dari hari pertama |
| 11 | Secrets | .env files + Doppler/Vercel | Jangan hardcode. Add to .gitignore. Selalu |
| 12 | File uploads | UploadThing / Cloudinary | Storage + CDN + security solved dalam satu integrasi |
| 13 | Preview deploys | Vercel auto PR preview | Test sebelum hit production. Catch broken UI |
| 14 | UI components | Radix + shadcn/ui | Accessible primitives + styled. Hampir semua UI pattern covered |
| 15 | README | Tulis dari hari 1 | 20 menit sekarang = hemat 4 jam confusion nanti |
| 16 | Folder structure | Clean + modular | Messy folder = 30% waktu navigasi. Components/hooks/utils/types |
| 17 | Onboarding | Empty states + tooltips | Confused users don't convert. They leave |
| 18 | Performance | Lighthouse audit | Score <70 = red flag. Fix before launch |

---

### DON'Ts — Pembuang Waktu

- ❌ Build auth dari scratch (biggest time killer)
- ❌ Raw CSS untuk segalanya (Tailwind covers 99%)
- ❌ Over-engineer state (Redux untuk 12 users)
- ❌ Custom REST API sebelum validasi (0 users don't need full API infra)
- ❌ Manual deployment (human error + slow)
- ❌ Raw SQL everywhere (Prisma exists)
- ❌ Build payment system sendiri (PCI compliance alone = months)
- ❌ DIY file uploads (breaks in prod in ways you won't predict)
- ❌ Push langsung ke main (feature branches + preview deploys)
- ❌ Build realtime sendiri (Supabase Realtime / Pusher exist)
- ❌ Skip monitoring (blind deployment = dying silently)
- ❌ Hardcode API keys (GitHub scans repos, AWS revokes keys instantly)
- ❌ DIY search engine (Algolia/Typesense/Meilisearch >> anything you build)
- ❌ Anggap user bakal ngerti sendiri (onboarding is mandatory)
- ❌ Tunda refactor selamanya (technical debt compounds)
- ❌ Obsesi perfect sebelum ship (MVP goal = learn, not perfect)

---

## Key Takeaways

1. **Keputusan paling mahal dibuat sebelum nulis kode** — bukan di kodenya
2. **Tau apa yang TIDAK perlu dibangun** = skill #1 builder cepat
3. **Stack yang disarankan (2026):** Next.js + Tailwind + shadcn + tRPC + Prisma + Supabase + Vercel + Clerk + Stripe + Sentry + PostHog
4. **Shipped imperfect > polished never launched** — selalu
5. **Energi yang hemat dari tools** → masuk ke fitur yang actually matters: UX, distribusi, nilai produk

---

## Tags

#vibe-coding #mvp #development-workflow #nextjs #tailwind #shadcn #clerk #supabase #stripe #sentry #vercel #prisma #best-practices #ship-fast #founder-tips
