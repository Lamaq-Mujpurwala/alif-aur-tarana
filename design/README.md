# Alif Aur Tarana — Design System

> *"Lafz sirf maani nahi rakhte… roshni rakhte hain."* — Words don't only carry meaning; they carry light.

This folder is the **visual soul** of Alif Aur Tarana. Every later UI integration (web, mobile, the YouTube extension) draws from here. It is intentionally opinionated — built from the world of Urdu itself, not from a template.

| File | What's inside |
|------|----------------|
| **README.md** (this) | The essence, the design concept, the brainstorm token-plan, and the critique that kept us off the AI defaults. |
| [`DESIGN.md`](DESIGN.md) | The full system: palette, typography, spacing, layout, motion, components, companion theming, copy/voice, accessibility, and the signature element. |
| [`tokens.css`](tokens.css) | Ready-to-import CSS custom properties (colour, type, space, motion) — the single source of truth for implementation. |
| [`inspiration/`](inspiration/) | Reference notes (Pinterest/Fontshare were login/JS-gated for screenshots, so inspiration is documented as sourced references + the tradition it draws on). |

---

## 1. The essence (what we are designing for)

Alif Aur Tarana is not an ed-tech app; it is a **mehfil** — a candlelit gathering where two friends make you fall in love with Urdu. The interface must feel like **an illuminated manuscript brought to life at night**: ink and gold on a warm dark ground, the Nastaʿlīq script flowing like the real thing, a single lamp of presence, and a great deal of *silence* around the words so each one can be felt.

Three non-negotiables, straight from the product:
- **Adab (refinement).** Restraint, generous space, nothing loud or crude. Elegance is the brand.
- **Ishq (love) & the beauty of the script.** The **Nastaʿlīq calligraphy is the hero**, not a label. It should stop you.
- **Two souls, one light.** **Alif** (hopeless romantic — rose & candle) and **Tarana** (elegant rationalist — moon & jade) are distinct presences; the whole room's light should change depending on who you're sitting with.

**The design concept: _Shab-e-Mehfil_ (an evening gathering).** A warm night-ink canvas, gold-leaf *tazhīb* illumination, the companion as a breathing **chirāgh** (lamp), and the spoken line **writing itself in Nastaʿlīq like ink from a qalam**, with Roman + Devanagari glosses unfolding beneath like a scholar's marginalia.

---

## 2. Brainstorm — the token plan (pass 1)

**Colour (warm-ink night + gold illumination + two companion glows):**
- `shab` (ground) `#16120E` — warm near-black, candlelit, never cold.
- `raqam` (raised panel / "leaf") `#221A13`.
- `parchment` (primary text) `#ECE0CB` — ink-on-night, inverted manuscript.
- `tila` (gold leaf, the illumination accent) `#C8A24A`; glint `#E7CB7E`.
- `gulaab` (Alif: rose) `#C66A6A` + `shama` (amber/candle) `#E0A35A`.
- `chaand` (Tarana: moon-jade) `#8FB3AE` + `noor` (silver) `#C7D0D4`.

**Type (Nastaʿlīq is the soul; Latin goes *beyond* Google):**
- **Display Urdu** → **Gulzar** (Nastaʿlīq, OFL) — flowing, contemporary, the hero. Fallback Noto Nastaliq Urdu.
- **Display Latin** → **Zodiak** (Fontshare/ITF) — a high-contrast didone whose thick/thin echoes Nastaʿlīq's modulation. Literary alternate: **Sentient**.
- **Body / UI** → **Switzer** (Fontshare) — a refined, warm neo-grotesque.
- **Roman transliteration (the gloss)** → an *italic* of the display serif — feels like handwritten marginalia.
- **Devanagari gloss** → **Tiro Devanagari Hindi** (harmonises with a matching Latin).
- **Labels/eyebrows** → Switzer small-caps, widely tracked.

**Layout:** a single, centred, vertical *mehfil* column with luxurious negative space. Lamp + living Nastaʿlīq at heart; a quiet **qalam** input at the foot; companion sigils to switch (and the room's light cross-fades).

**Signature:** **the Chirāgh + the self-writing Nastaʿlīq line.** A breathing pool of light (rose-amber for Alif, jade-silver for Tarana) under which the companion's words appear in gold-ink Nastaʿlīq, glosses unfolding below. The boldness lives here; everything else stays disciplined.

---

## 3. Critique — staying off the defaults (pass 2)

The skill warns about three AI-default looks. Here's how we consciously avoid each:

| Default | Why we don't | What we do instead |
|---------|--------------|--------------------|
| **Cream + high-contrast serif + terracotta** (our *old* placeholder was literally this) | It's the generic "literary" answer and reads templated | **Inverted**: parchment-and-gold ink on a *warm night* ground. The warmth comes from candlelight, not a cream page. |
| **Near-black + one acid accent** | Cold, techy, soulless — the opposite of adab | Our dark is a **warm ink** (#16120E), and the accent is **gold leaf**, not neon — illumination, not voltage. |
| **Broadsheet hairlines / zero-radius / dense columns** | Newspaper ≠ mehfil; density kills the silence | **Single intimate column**, soft radii like worn paper edges, generous space so each couplet can breathe. |

Two more checks:
- **Numbered markers (01/02/03)?** Rejected — our content is a *conversation*, not a sequence. Structure is encoded by *light and script*, not numerals.
- **The hero.** Not a big-number stat. The hero is the **most characteristic thing in the subject's world**: living Nastaʿlīq under lamplight. That is the thesis of the page.

**The one real risk we're taking:** making **Nastaʿlīq (a script most users can't yet read) the visual hero**, on a *dark* ground, with the meaning carried by glosses around it. Justification: the product's entire premise is falling in love with the *feeling* of Urdu before you can read it — so the script must seduce first, and the glosses teach second. The dark ground makes gold ink glow the way it does on a real illuminated leaf.

---

## 4. Inspiration (sourced references)

Pinterest and Fontshare specimens were login/JS-gated and wouldn't render in automated screenshots, so inspiration is documented as references rather than captures. The well of ideas:
- **Mughal & Persian illuminated manuscripts** (*tazhīb*): gold leaf on lapis/indigo grounds, jewel tones, the discipline of the illuminated border. (Met Museum, Google Arts & Culture "Mughal painting".)
- **Nastaʿlīq calligraphy**: the diagonal ink-flow, the thick→thin modulation — the model for our motion and our Latin display choice.
- **Rekhta.org** (see `../docs/inspiration/`): the gold standard for *presenting* Urdu poetry — we borrow its reverence, invert its palette to night, and make it *living* and conversational.
- **Type**: [Gulzar](https://fonts.google.com/specimen/Gulzar) (Nastaʿlīq) · [Fontshare](https://www.fontshare.com/) — Zodiak, Sentient, Switzer · [Tiro Devanagari](https://fonts.google.com/specimen/Tiro+Devanagari+Hindi).
- **Components/motion to source during build** (21st.dev, framer.com): an amplitude-reactive voice visualiser (re-skinned as the chirāgh), a text "ink-reveal/shimmer", a soft cross-fade for companion switching. See [`DESIGN.md` §Components](DESIGN.md).

> Implementation note: the design adopts the **impeccable.style** working principle — *"loud or restrained, never neutral,"* purposeful motion, and a living `DESIGN.md` as the source of truth — and its loop of *plan → build → review → refine*.
