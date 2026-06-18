# Inspiration

Automated screenshots of **Pinterest** and **Fontshare** specimens came back blank — both are login/JS-canvas-gated and don't paint in headless capture. So inspiration is documented as **sourced references** rather than images. (The product-side reference snapshots that *did* capture — Rekhta, ElevenLabs, Sarvam, Hume — live in [`../../docs/inspiration/`](../../docs/inspiration/).)

## The well we draw from

- **Mughal & Persian illuminated manuscripts (tazhīb).** Gold leaf on lapis/indigo grounds, jewel tones, the discipline of an illuminated border framing a single column of text. → our *night ground + gold illumination*, the framed mehfil column. (The Met "Mughal painting"; Google Arts & Culture; Walters Art Museum Islamic manuscripts.)
- **Nastaʿlīq calligraphy.** The diagonal ink-flow and thick→thin modulation. → the hero treatment, the *ink-settling* motion, and the high-contrast Latin display pairing.
- **Rekhta.org.** The gold standard for presenting Urdu poetry (reverent, content-first). → we keep the reverence, **invert the palette to night**, and make it *living* + conversational.
- **Candlel"chirāgh" / mehfil.** Warmth, a single source of light, gathering at night. → the breathing lamp as the companion's presence.

## Type references
- Nastaʿlīq: [Gulzar](https://fonts.google.com/specimen/Gulzar) (OFL, contemporary) · [Noto Nastaliq Urdu](https://fonts.google.com/noto/specimen/Noto+Nastaliq+Urdu).
- Latin (beyond Google): [Fontshare](https://www.fontshare.com/) — **Zodiak** (high-contrast didone), **Sentient** (literary serif), **Switzer** (body).
- Devanagari: [Tiro Devanagari Hindi](https://fonts.google.com/specimen/Tiro+Devanagari+Hindi).

## Components to source + re-skin (during build)
- 21st.dev / framer.com: an **amplitude-reactive orb** (→ re-skin as the chirāgh), an **ink/shimmer text reveal**, a **soft cross-fade**. Always restyle to `../tokens.css`; never ship stock looks.

See [`../DESIGN.md`](../DESIGN.md) and [`../tokens.css`](../tokens.css) for the full system.
