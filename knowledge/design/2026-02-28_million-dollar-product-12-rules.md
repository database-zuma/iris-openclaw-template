# Million Dollar Product — 12 Rules to Building Something Users Love

**Source:** LinkedIn/Blog post (author: founder yang build 50+ MVPs dalam 1 tahun)
**Date:** Feb 2026

## Core Thesis

Stack bukan masalahnya. Next.js vs Remix, Supabase vs Firebase — semua itu tidak relevan kalau tidak ada yang mikir tentang produknya. Dunia sudah penuh "vibe coded look-alikes": buggy, UX buruk, zero retention. Yang membedakan produk yang bertahan adalah **keputusan di setiap layer**, bukan tech stack-nya.

---

## 12 Rules

### 1. Nail Your User Persona Before Writing Code
- "Founders" atau "SMBs" bukan persona — itu kategori
- Persona nyata: daily workflow, specific frustration, current workaround, technical literacy
- **Test:** kalau tidak bisa describe target user dalam 2 kalimat, belum siap build
- Semua keputusan design + UX downstream dari ini

### 2. Articulate What the Product Should FEEL Like Before Figma
- Beda antara *apa yang dilakukan* produk vs *rasanya pakai* produk
- Define UX principles dulu: fast & minimal (power users) vs guided & hand-holdy (beginners)?
- Map critical user journey: dari landing → **"aha moment"** (first value experience)
- **Aha moment = momen terpenting di seluruh produk.** Engineering everything to reach it ASAP
- UX bukan design decision. Ini **product decision**.

### 3. Build Brand Foundation Before First Component
- Brand bukan logo/warna — brand adalah **sum of every decision your product makes in front of a user**
- Elemen brand: product name, tagline, brand pillars (2-3 core values), positioning statement
- **Voice & tone paling kritis:** setiap label, button text, empty state, error message adalah brand decision
  - "Scaling your focus" ≠ "Choose a plan"
  - "Work, Draft" ≠ "Untitled document 3"
- Micro-decisions ini compound jadi trust atau confusion

### 4. Map Information Architecture Before Any Screens
- IA = skeleton produk — hampir tidak ada yang mikir ini sebelum build
- Map setiap page, section, user flow di kertas dulu
- Define navigation model: sidebar, top nav, atau bottom tabs? (masing-masing communicate hal berbeda)
- **Prinsip krusial: group features by USER INTENT, not by how you built them**
  - Developer organize by codebase structure; user organize by what they want to accomplish
  - Hampir selalu berbeda

### 5. Layout Consistency Across Roles is Non-Negotiable
- Role-based access? Setiap role harus experience same logic, bahkan kalau lihat data berbeda
- Same component behaviour, same visual hierarchy, same interaction patterns across all roles
- Define master layout grid — jangan pernah break it across pages
- User tidak boleh merasa "switch products" saat switch role atau navigate antar section

### 6. Build Design System Before First Screen
- Build token system dulu (bukan langsung components):
  - Spacing scale → defined before anything placed on page
  - Type scale → locked before any text styled
  - Colour tokens → named variables carrying meaning across entire product
- Kemudian build component library: buttons, inputs, cards, modals, navigation
- **Setiap component harus punya SEMUA states:** default, hover, active, disabled, error
- Ini perbedaan terbesar antara produk yang terasa $500 vs $50,000

### 7. Colour Palette is a Retention Decision
- Filter yang salah: warna yang kamu suka
- Filter yang benar: **warna yang user percaya**
- Fintech ≠ children's app — emotional & psychological associations berbeda
- Token set yang harus didefinisikan:
  - Primary & secondary brand colours
  - **Semantic colours (paling sering diabaikan):** success, warning, error, informational
  - Neutral scale (carries lebih banyak UI dari yang founder realise)
- Colour communicates trust, urgency, safety, delight — sebelum satu kata pun dibaca

### 8. Every Product State Needs to Be Designed
- **95% vibe coded products hanya design happy path.** Di sini mereka gugur.
- States yang harus didesign:
  - **Loading state** — saat data di-fetch
  - **Empty state / Zero data state** — state yang SETIAP new user encounter pertama kali → paling diabaikan
  - **Error state** — harus bilang apa yang harus dilakukan, bukan cuma apa yang salah
  - **Edit state** — saat content dimodifikasi
  - **Success state** — saat action completed
- "Something went wrong" bukan error message — itu **abandonment trigger**
- Zero data state menentukan apakah user kembali di hari kedua

### 9. Onboarding: Collect Just Enough
- Kesalahan terbesar: coba learn everything di hari pertama
- Satu pertanyaan: **apa minimum information untuk deliver first valuable session?**
- Lebih dari itu = friction = user yang hilang sebelum experience produk
- Prinsip: **Progressive disclosure** — ask for what you need at start, ask for more as trust is earned
- Jangan gate produk behind 10-step setup flow
- Goal onboarding = get user to **first value moment as fast as possible**. Itu saja.

### 10. Performance is a Product Feature
- Define load time targets **before you build**, bukan setelah ship
- Standard: **< 2 seconds untuk any core user action**
- Lazy load everything yang tidak immediately visible
- **Skeleton screens > spinners** — perceived performance matters sama dengan actual performance
  - Skeleton screen: "content is coming" (brain registers progress)
  - Spinner: "I am waiting" (brain registers delay)
- Users tidak blame internet connection. Mereka blame produk.

### 11. Micro Interactions Are the Difference
- Layer yang hampir semua vibe coder skip — layer yang bikin user bilang "this just feels good" tanpa bisa explain kenapa
- Setiap: button click, form submission, page transition = perlu feedback/signal
- **Sweet spot animation duration: 150ms – 300ms**
  - Cukup cepat untuk feel snappy
  - Cukup lambat untuk brain register that something happened
- Micro interactions bukan dekoratif — **functional**: tell user their action was received
- Perbedaan antara produk yang terasa "smooth" vs "clunky" meski functionality identik

### 12. Build for the Second Session, Not the First
- Siapapun bisa buat first impression yang baik. Metric sesungguhnya: **apakah user kembali di hari 3?**
- Setiap produk punya **activation event** — specific action yang, once completed, strongly predicts long-term retention
- Tugas: identify activation event → engineer first session experience around reaching it ASAP
- Pertanyaan yang benar bukan "how do we look impressive on first launch?" tapi "how do we get users to the moment where they **cannot imagine not having this product**?"
- Day one retention = easy. Day three retention = real test.
- Kalau users tidak kembali: **produk yang gagal. Bukan marketing. Bukan distribusi. Produknya.**

---

## The Full Checklist

- [ ] Clear user persona
- [ ] Defined UX feel (not just what it does, but how it feels)
- [ ] Solid brand foundation (name, tagline, pillars, voice/tone)
- [ ] Tight information architecture (grouped by user intent)
- [ ] Consistent layout system across roles
- [ ] Design tokens (spacing, type, colour) before components
- [ ] Colour palette your user trusts (semantic tokens!)
- [ ] Every state designed (loading, empty, error, edit, success)
- [ ] Minimal friction onboarding (progressive disclosure)
- [ ] Fast performance (< 2s target, skeleton screens)
- [ ] Intentional micro interactions (150–300ms)
- [ ] Built for second session (identify & engineer to activation event)

## Takeaways

1. **Stack adalah distraksi** — founders debate Next.js vs Remix tapi tidak mikirin siapa usernya
2. **Aha moment adalah momen terpenting** — engineering everything around reaching it ASAP
3. **Zero data / empty state = state pertama setiap new user encounter** — hampir universally ignored
4. **Brand adalah micro-decisions yang compound** — bukan logo, tapi setiap button text dan error message
5. **Skeleton screens > spinners** — perceived performance sama pentingnya dengan actual performance
6. **Day 3 retention, bukan day 1** — activation event adalah metric yang sebenarnya
7. **IA: group by user intent, bukan codebase structure** — ini selalu berbeda dan hampir selalu salah
8. **Micro interactions = functional, bukan dekoratif** — 150–300ms sweet spot

## Relevansi untuk Zuma / Codex

Langsung applicable kalau Codex build dashboard/web app untuk Zuma:
- **Empty state** di reports/dashboard saat belum ada data
- **Skeleton screens** di data-heavy pages (sales reports, stock queries)
- **Error messages yang actionable** bukan "something went wrong"
- **Activation event** tiap app Zuma — apa yang harus dilakukan user agar kembali?
- **Progressive disclosure** di onboarding tools operasional

## Tags

#product-design #ux #retention #onboarding #design-system #brand #information-architecture #micro-interactions #performance #activation-event #mvp #product-management #codex-reference
