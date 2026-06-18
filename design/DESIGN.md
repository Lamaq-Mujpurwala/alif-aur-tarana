# DESIGN.md — Alif Aur Tarana

The complete, implementation-ready design system. Source of truth alongside [`tokens.css`](tokens.css).
Concept: **Shab-e-Mehfil** — an illuminated manuscript brought to life by candlelight. See [`README.md`](README.md) for the essence and the rationale.

---

## 1. Principles

1. **Silence is a material.** Negative space is the room. Crowding is the enemy of adab — when in doubt, remove, enlarge, and let it breathe.
2. **The script is the hero.** Nastaʿlīq leads; Latin and Devanagari serve as glosses. Never shrink the Urdu to fit chrome.
3. **Light, not lines.** Hierarchy is built with warmth, glow, and gold — not boxes, borders, and grids you can see.
4. **Loud in one place.** All boldness lives in the **chirāgh + living Nastaʿlīq** signature. Everything else is quiet and exact.
5. **Two souls, one light.** The room is tinted by whoever you're with. The shift between Alif and Tarana is felt, not just clicked.
6. **Never neutral.** Every colour, weight, and easing is a choice with a reason (per impeccable.style).

---

## 2. Colour

A warm **night-ink** ground, **gold-leaf** illumination, and two companion glows. All values are in `tokens.css`.

### Core (the room)
| Token | Hex | Use |
|-------|-----|-----|
| `--shab` | `#16120E` | App background — warm, candlelit near-black. |
| `--shab-2` | `#1C160F` | Subtle vertical gradient partner for depth. |
| `--raqam` | `#221A13` | Raised "leaf" / panel surface (reading cards, input). |
| `--parchment` | `#ECE0CB` | Primary text — ink-on-night (inverted manuscript). |
| `--parchment-dim` | `#A1907B` | Secondary text, glosses, captions. |
| `--hairline` | `rgba(236,224,203,.10)` | The faintest divider; prefer space over lines. |

### Gold (illumination — the one accent that's always present)
| Token | Hex | Use |
|-------|-----|-----|
| `--tila` | `#C8A24A` | Gold leaf — wordmark accent, dividers' glint, focus ring, key emphasis. |
| `--tila-glint` | `#E7CB7E` | Highlights, hover lift, small sparks. |
| `--tila-ink` | `#5A4A2E` | Dim gold for borders on dark / disabled gold. |

### Companion glows (theming — see §7)
| Token | Hex | Companion |
|-------|-----|-----------|
| `--gulaab` | `#C66A6A` | **Alif** — dusky rose (ishq). |
| `--shama` | `#E0A35A` | **Alif** — candle amber. |
| `--chaand` | `#8FB3AE` | **Tarana** — moon-jade. |
| `--noor` | `#C7D0D4` | **Tarana** — moon-silver. |

`--accent` / `--glow` are **runtime aliases** set to the active companion (default Alif). All interactive accents (buttons, the chirāgh, highlights, the taught-word) reference `--accent`/`--glow`, so the entire room re-tints when you switch companions.

### Contrast & rules
- `--parchment` on `--shab` ≈ 12:1 — well above AA for body.
- `--tila` on `--shab` ≈ 6.6:1 — fine for large/medium text and UI; for small gold text use `--tila-glint`.
- Gold is **accent, not body** — never set long paragraphs in gold.
- Companion glows are for **light and emphasis**, not body text (they don't all meet AA at small sizes).

---

## 3. Typography

Nastaʿlīq is the soul. Latin goes **beyond Google** (Fontshare / Indian Type Foundry). See `README.md §2` for rationale; load details in §11.

### Roles
| Role | Face | Notes |
|------|------|-------|
| **Urdu display** (hero) | **Gulzar** (Nastaʿlīq) → fallback *Noto Nastaliq Urdu* | The companion's spoken line. Large, `direction: rtl`, very generous `line-height` (Nastaʿlīq needs ~2.0+). |
| **Urdu inline** | Noto Nastaliq Urdu | Small Urdu in cards/labels where Gulzar is too ornate. |
| **Latin display** | **Zodiak** (Fontshare) → *Sentient* alt | Wordmark, rare big headings. Use with restraint. |
| **Roman gloss** | **Zodiak Italic** / Sentient Italic | The transliteration line — handwritten-marginalia feel. |
| **Body / UI** | **Switzer** (Fontshare) → system-ui | Buttons, status, English notes, controls. |
| **Devanagari gloss** | **Tiro Devanagari Hindi** → Noto Serif Devanagari | The Hindi line. |
| **Label / eyebrow** | Switzer, small-caps, `letter-spacing:.18em`, `--parchment-dim` | Quiet metadata ("aaj ka lafz", companion name). |

### Scale (fluid, `clamp()` — in tokens.css)
- `--fs-nastaliq` : `clamp(2.4rem, 6vw, 4.5rem)` — the hero line (Gulzar runs visually small; size it up).
- `--fs-display` : `clamp(2rem, 5vw, 3.5rem)` — Latin display.
- `--fs-roman` : `clamp(1.05rem, 2.2vw, 1.35rem)` — the Roman gloss.
- `--fs-deva` : `1rem` · `--fs-body` : `1rem` · `--fs-note` : `.9rem` · `--fs-label` : `.72rem`.
- **Line-height:** Nastaʿlīq `2.05`; Latin display `1.05`; body `1.6`.

### Typographic rules
- Nastaʿlīq is **never** justified or letter-spaced; never all-caps (it has no case). Emphasis in Urdu = the taught word in `--accent`.
- Roman gloss in **italic**, `--parchment-dim`; the **taught word** within it lifts to `--tila`/`--accent`.
- The wordmark sets **الف اور ترانہ** (Gulzar) as primary, with a small Latin "Alif aur Tarana" (Switzer small-caps) beneath — Urdu leads.
- One display moment per view. Don't stack big Latin and big Nastaʿlīq competing for the eye — Nastaʿlīq wins.

---

## 4. Spacing & layout

### Space scale (8-based, calm)
`--space-1:4px --space-2:8px --space-3:12px --space-4:16px --space-5:24px --space-6:32px --space-7:48px --space-8:64px --space-9:96px --space-10:140px`. Default section rhythm is **large** (`--space-8`/`--space-9`).

### The mehfil column
A single centred column, **max-width `--measure` (≈ 640px)**, lots of air. Not a dashboard, not columns.

```
            ┌───────────────────────────────────┐   ← warm night ground (full bleed),
            │            الف اور ترانہ            │     a faint gold tazhīb hairline frames
            │      ·  Alif    ◐    Tarana  ·      │     the column on wide screens
            │                                     │
            │            (  chirāgh  )            │   ← breathing lamp, tinted to companion
            │                                     │
            │      رنجش ہی سہی دل ہی دکھانے…        │   ← HERO: living Nastaʿlīq (Gulzar)
            │     Ranjish hi sahi, dil hi…        │   ← Roman gloss (italic)
            │     रंजिश ही सही, दिल ही…           │   ← Devanagari gloss
            │     ┌ ranjish — a tender resentment ┐ │ ← English note, faint margin gloss
            │                                     │
            │   ╭─────────────────────────────╮   │   ← qalam input (one line)
            │   │ kahiye… ya "Alif suno"   🪶 ▸ │   │
            │   ╰─────────────────────────────╯   │
            └───────────────────────────────────┘
```

- **Header**: slim, low-weight. Wordmark left or centred; the two companion sigils as the switch.
- **Stage** (centre): chirāgh → Nastaʿlīq → Roman → Devanagari → note. Vertical, centred, staggered reveal.
- **Foot**: the **qalam** input — a single quiet field with a mic (🪶 feather/qalam) and send. The **cue whisper** appears just above it.
- **Wide screens**: keep the column centred; let the night ground (with a faint gold *tazhīb* frame and a soft radial vignette behind the chirāgh) hold the sides. Do **not** widen into multiple columns.
- **Mobile**: same column at full width with `--space-5` gutters; chirāgh scales down; glosses stack tighter.

---

## 5. Motion

Motion mimics **ink and lamplight** — nothing springy or techy. Tokens: `--ease-ink: cubic-bezier(.22,.61,.36,1)` (settle), `--ease-soft: cubic-bezier(.4,0,.2,1)`; durations `--dur-1:160ms --dur-2:320ms --dur-3:600ms --dur-4:1200ms`.

| Moment | Motion |
|--------|--------|
| **Ink reveal** (new line) | Nastaʿlīq fades in + rises 8px + **blur 6px→0** over `--dur-3` (`--ease-ink`) — "ink settling on the page." Optional RTL mask-wipe. |
| **Gloss unfold** | Roman, then Devanagari, then note — each fades up, staggered **90ms**. |
| **Chirāgh breathing** | Idle: opacity `.85↔1` + scale `1↔1.03` over **5s**, infinite, `--ease-soft`. |
| **Chirāgh — speaking** | Glow radius + brightness track audio amplitude (rAF). Listening (mic on): a slow, deeper pulse. |
| **Cue acknowledgement** | A single gentle flare of the chirāgh + the cue text shimmers in (gold sheen sweep) for ~`--dur-2`. |
| **Companion switch** | The room's `--accent`/`--glow` **cross-fade** rose⇄jade over `--dur-3`; the chirāgh hue lerps. "Changing the lamp." |
| **Hover (controls)** | Lift to `--tila-glint`, `--dur-1`. No scale-bounce. |

**Reduced motion** (`prefers-reduced-motion: reduce`): replace blur/rise/breathing with plain ~120ms opacity fades; chirāgh becomes a static soft glow; companion switch is an instant tint change. Keep amplitude-glow only if subtle.

---

## 6. Components

Build these as the kit. Most are custom (the lamp feel can't be bought); a few can be *sourced and re-skinned* (noted).

- **Chirāgh** (the companion presence / voice orb). A layered radial-gradient pool of light on the night ground (core `--glow`, soft outer bloom, faint gold rim). States: *idle* (breathing), *listening* (slow deep pulse), *speaking* (amplitude-reactive), *thinking* (a slow shimmer). *Source candidate:* an audio-visualiser/orb from 21st.dev — strip its chrome, drive it with our `--glow`. The lamp **is** the brand mascot; keep it abstract (light), not a literal diya illustration.
- **Tri-script line** (the teaching block). Nastaʿlīq (hero) + Roman (italic) + Devanagari + English note. The **taught word** is highlighted in `--accent` across all scripts and is **tap-to-hear** (replays cached audio). This is the core learning unit.
- **Companion switch** (sigils). Two restrained marks: **Alif → "ا"** set in Gulzar inside a rose-amber halo; **Tarana → a crescent "◐"** in a jade-silver halo. Active sigil glows; switching cross-fades the room (§7). Not a generic toggle.
- **Qalam input.** One line, `--raqam` surface, soft radius, gold focus ring. A **feather/qalam mic button** and a quiet send (▸). Placeholder is in-world copy (§8).
- **Cue whisper.** The acknowledgement text (e.g., *"جی، فرمائیے"*) shown faint + italic above the input while its cached audio plays; gold shimmer in, fade out.
- **Manuscript leaf** (card/surface). When panels are needed (history, word list), use a warm `--raqam` leaf with a faint gold *tazhīb* hairline and soft, uneven (paper-like) radius — not a flat material card.
- **Buttons.** *Primary*: filled `--accent` on `--shab`, parchment label. *Quiet*: gold-outline (`--tila-ink`) → fills on hover. *Ghost*: text + gold underline-on-hover. Radius `--radius-2`. No drop shadows; use glow.
- **Tazhīb frame / dividers.** Instead of plain `<hr>`, a centred gold motif (a small diamond/▒ flanked by hairlines) — illumination, used sparingly.

States to design for every component: default, hover, focus-visible (gold ring), active, disabled, loading, error, empty.

---

## 7. Companion theming (one room, two souls)

A single CSS class on `<body>` (`.with-alif` / `.with-tarana`) sets the runtime aliases:

```
.with-alif   { --accent: var(--gulaab); --glow: var(--shama);  --accent-soft:#3a211c; }
.with-tarana { --accent: var(--chaand); --glow: var(--noor);   --accent-soft:#1e2a29; }
```

What changes when you switch (cross-faded over `--dur-3`):
- The **chirāgh** hue and the radial vignette behind it.
- All **accent** uses: buttons, focus rings, the taught-word highlight, the active sigil.
- A barely-there shift in the ground gradient warmth (Alif a touch warmer).

What never changes: the night ground, parchment text, gold-leaf structural accents, type, layout. **Gold is the shared thread; the glow is the personality.**

Personality cues in *behaviour* (not just colour): Alif's chirāgh flickers a touch more (candle); Tarana's is steadier (moon). Alif's reveals can carry a hair more overshoot; Tarana's are perfectly settled.

---

## 8. Copy & voice (microcopy)

In-world, warm, bilingual, lower-case calm. The interface speaks like a gracious host, never like a system.

- **Input placeholder:** `kahiye… ya "Alif suno" keh kar bulaaiye` (and the Urdu beside it).
- **Listening status:** `sun rahe hain…` (Alif) / `sun rahi hain…` (Tarana).
- **Thinking (when not covered by a voice cue):** `soch rahe hain…`
- **Empty / first open:** an invitation, not a form — a couplet and *"kisi lafz ko mehsoos karne ke liye, bas kahiye."*
- **Error (TTS/quota):** in-voice, kind — `abhi aawaaz nahi aa paa rahi — alfaaz haazir hain.` (text shown; audio later). Never an apology, never a stack trace.
- **Companion names** are always written with respect; the app never refers to them as "bots" or "assistants."
- Buttons say what happens: `bhejiye` (send), `phir se` (again/replay), `dheere` (slower).

---

## 9. Accessibility & quality floor

- **Contrast:** body parchment ≥ 12:1; never set body in gold/glow. Provide a high-contrast check for the taught-word highlight.
- **Focus:** visible **gold focus ring** (`--tila`, 2px, 2px offset) on every interactive element; never remove outlines.
- **Reduced motion:** honoured (§5).
- **RTL:** Urdu blocks are `dir="rtl"`; the rest is LTR. Don't mirror the whole app — mirror the Urdu text only.
- **Type fallbacks:** Nastaʿlīq must always fall back to Noto Nastaliq Urdu → serif; never let Urdu render in a non-Nastaʿlīq face. Preload the Nastaʿlīq + display fonts; `font-display: swap` for the rest.
- **Tap-to-hear** works by keyboard (Enter/Space on the focused word).
- **Performance:** Nastaʿlīq fonts are large — subset to the glyphs used where possible; lazy-load Devanagari.

---

## 10. The signature (the one thing it's remembered by)

> **The Chirāgh & the self-writing Nastaʿlīq.**
>
> On a warm night ground, a soft lamp breathes in the companion's colour. When they speak, their line **arrives as gold-ink Nastaʿlīq, blooming from blur into focus** as if just written by a qalam; the Roman and Devanagari glosses unfold beneath like a scholar's margin notes; the one **taught word glows** and can be touched to hear again. Call "Alif suno" and the lamp flares instantly with *"جی، فرمائیے"* before a single thought is computed. Switch to Tarana and the whole room cools to moonlight.

Everything else in the system stays quiet so this moment lands. That is the brief — *ishq* and *adab* — made visible.

---

## 11. Implementation notes

- **Stack:** the real client is the planned **Next.js `frontend/`** (split from backend for deploy). Motion via **Framer Motion**; tokens via CSS variables imported from `tokens.css` (mapped to Tailwind theme if Tailwind is used). The current `backend/static/index.html` can adopt `tokens.css` immediately as a faithful interim.
- **Fonts:** Gulzar + Noto Nastaliq Urdu via Google Fonts/`@fontsource`; Zodiak/Sentient/Switzer from **Fontshare** (free for commercial — download + self-host); Tiro Devanagari Hindi via Google. Self-host for performance; preload Gulzar + the active display face.
- **Audio cue ↔ chirāgh:** the `/converse` stream already sends `cue` then `reply`; the chirāgh flares on `cue`, settles, then performs the ink-reveal on `reply`. The design and the pipeline already fit.
- **Source/refine components** (21st.dev, framer.com) for: the amplitude orb (→ chirāgh), an ink/shimmer text reveal, a smooth cross-fade. Re-skin everything to these tokens; never ship a component in its stock look.

Keep this file and `tokens.css` updated as the system evolves — they are the contract every surface integrates against.

---

## 12. Component sourcing & libraries (researched 19 Jun 2026)

**Hand-build the signature.** The chirāgh, Nastaʿlīq ink-reveal, tri-script block, and companion cross-fade are built with **Framer Motion + CSS** — too bespoke (RTL Nastaʿlīq, our tokens, audio-reactivity) for drop-ins, and control matters most here.

**Framer Marketplace** (`framer.com/community/marketplace` — *Templates · Components · Vectors · Plugins*; free **and** paid). Items are made for the Framer no-code tool, **but importable into our Next.js app**:
- **`unframer`** — free OSS CLI that downloads a Framer component as React/JS (SSR-ready, emits `"use client"`). The pragmatic bridge.
- React-Export plugins (Proofly, Tommy D. Rossi) — paid, for unlimited exports.
- Relevant component categories: **Backgrounds (524)** — a grain / aurora / gradient-mesh for the night ground; **Typography (603)** — text reveals (`stack-text-reveal`, `dualwavetext`) as *inspiration* for the ink-reveal; **Interactions (1.8K)**. **Vectors** skew generic/Western (Icons/Shapes/`stars-and-sparkles` for gold glints) — **not** a good source for tazhīb ornament, so hand-draw simple gold ornaments as SVG.

**21st.dev** — preferred for **direct copy-paste React/Tailwind/Framer-Motion** components (e.g. an audio visualiser → re-skin as the chirāgh; a shimmer-text reveal). Cleanest for code.

**Rule:** never ship a sourced component in its stock look — always re-skin to `tokens.css`. Reach for the marketplace only when a bespoke build would be materially worse (e.g. a complex WebGL background).
