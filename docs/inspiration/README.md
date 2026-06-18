# Inspiration — Design & UX References

Snapshots collected on **18 June 2026** with Playwright (full-page captures, 1440px viewport). Each entry notes *what it is*, *what's notable*, and *the specific lesson for Alif Aur Tarana*. These inform the UI direction in [`../01-product-vision.md §6`](../01-product-vision.md) and the surfaces in [`../06-cross-platform.md`](../06-cross-platform.md).

> File note: images are full-page JPEGs, so they're tall — open them directly to study a section.

---

## 0. The original brief (your whiteboard)
**File:** [`WhatsApp Image 2026-06-18 at 2.41.23 PM.jpeg`](WhatsApp%20Image%202026-06-18%20at%202.41.23%20PM.jpeg)

The source-of-truth requirements photo. Decoded: name *Alif Aur Tarana*; "Requirements: nvidia?"; (1) live natural conv — urdu voice, accent; (2) multiling LLM (gemini/sarvam); (3) friend+teacher personality; (4) conv history, web search, rekhta, yt + similar sources; (5) multiling transcription; (6) personality, wit, sarcasm. The whole research pass traces back to these six lines.

---

## 1. Rekhta — home
**File:** [`rekhta-home.jpeg`](rekhta-home.jpeg) · Source: <https://www.rekhta.org/>

- **What:** The world's largest Urdu-poetry archive — our single most important *content* reference (and the spiritual sibling of this product).
- **Notable:** Calm, literary, content-first; brand maroon on cream/white; a global **script switcher** (Urdu / Devanagari / Roman) that re-renders all poetry; categories by poet, theme, form (ghazal/nazm/sher); "sher of the day" energy.
- **Lesson for us:** This is the gold standard for *presenting* Urdu poetry — but it's **passive** (you read/look up). Our opening is to make that same content **conversational**. Borrow their tri-script discipline and reverence for typography; add the living companion they don't have.

## 2. Rekhta — poet page (Mirza Ghalib)
**File:** [`rekhta-poet-ghalib.jpeg`](rekhta-poet-ghalib.jpeg) · Source: <https://www.rekhta.org/poets/mirza-ghalib>

- **What:** A single poet's complete works, organised by form (Ghazal, Marsiya, Qita, Rubai, Qisse, Sehra), plus Books, **Image Shayari**, Videos, Audios, Related Blog, Similar Poets.
- **Notable:**
  - **Couplets centered, line-by-line**, defaulting to Roman transliteration here — exactly the rhythm we want for "sher unpacking."
  - **"Image Shayari"** = couplets as shareable cards (Urdu calligraphy on dark backgrounds). A beautiful, viral-friendly format.
  - **Similar Poets** as circular B&W portraits — a clean discovery pattern.
  - Multi-media per poet (video/audio) — confirms our YouTube/audio integration is on-theme.
- **Lesson for us:** (a) Adopt the **centered, line-by-line couplet layout** for the teaching view. (b) Steal **"Image Shayari" cards** as a share/export feature ("share this sher Alif taught you"). (c) Their per-poet media hub validates [`../04`](../04-tools-and-integrations.md)'s poet-stories tool.

## 3. ElevenLabs — home
**File:** [`elevenlabs-home.jpeg`](elevenlabs-home.jpeg) · Source: <https://elevenlabs.io/>

- **What:** The voice provider we chose for the "feel" ([`../02 §C`](../02-voice-stack-research.md)); their site doubles as a voice-agent product showcase.
- **Notable:** Confident dark/minimal aesthetic; **interactive voice demos right on the page** (type → hear); voice library framing; "Agents" platform positioning.
- **Lesson for us:** (a) **Let people hear a voice immediately** — our landing should let a visitor tap and hear Alif/Tarana say one gorgeous line (cached audio = free). The "try it instantly" pattern converts. (b) Their emphasis on *expressive* voices reinforces leaning into v3 audio tags for the companions' emotion.

## 4. ElevenLabs — Urdu TTS page
**File:** [`elevenlabs-urdu-tts.jpeg`](elevenlabs-urdu-tts.jpeg) · Source: <https://elevenlabs.io/text-to-speech/urdu>

- **What:** Proof + demo of ElevenLabs' Urdu voice support, the scarce capability our whole architecture hinges on.
- **Notable:** A dedicated Urdu TTS try-box; framing around accents and natural delivery.
- **Lesson for us:** This is the literal demo surface to **A/B our companion voices** against Azure in Phase 0 ([`../07`](../07-execution-roadmap.md)). Keep this page bookmarked as the "is the Urdu good enough?" gut-check.

## 5. Sarvam — home
**File:** [`sarvam-home.jpeg`](sarvam-home.jpeg) · Source: <https://www.sarvam.ai/>

- **What:** Our STT pick (Saaras v3) and a strong Indic-LLM option ([`../02`](../02-voice-stack-research.md)); positioned as "India's full-stack sovereign AI."
- **Notable:** India-first identity, language-coverage messaging, developer-API framing, clean product-led layout.
- **Lesson for us:** Their **India-first, language-pride positioning** is tonally close to ours. Good reference for how to talk about regional-language AI with respect rather than as a novelty. Confirms Sarvam as a culturally-aligned partner for the code-mixed speech layer.

## 6. Hume AI — home
**File:** [`hume-home.jpeg`](hume-home.jpeg) · Source: <https://www.hume.ai/>

- **What:** Empathic Voice Interface lab — the emotion-in-voice reference point ([`../02 §D`](../02-voice-stack-research.md)).
- **Notable:** Research-lab elegance; emotion/prosody as the hero concept; restrained, premium visual tone; the "voice that understands feeling" narrative.
- **Lesson for us:** Even though Hume's Urdu support is unconfirmed (so not in our stack), their **product narrative — "a voice that feels with you" — is exactly our pitch.** Borrow the *emotional* framing and the calm, premium restraint, not the tech.

---

## Synthesis — the design direction these point to

Pulling the threads together for Alif Aur Tarana's UI:

1. **Content-first calm (from Rekhta):** white/cream space, reverent typography, the poetry is the hero — not chrome. A proper **Nastaʿlīq** face for Urdu + clean Devanagari + Roman.
2. **Centered, line-by-line couplets with a tri-script toggle (from Rekhta):** our signature teaching view.
3. **Hear-it-instantly (from ElevenLabs):** the landing and every taught word should be one tap from audio; an expressive, emotional voice is the wow.
4. **Emotional, premium restraint (from Hume):** the companion *feels*; the UI gets out of the way.
5. **Language-pride, not novelty (from Sarvam):** treat Urdu with dignity and love in copy and visuals.
6. **Shareable "Image Shayari" cards (from Rekhta):** built-in growth loop — export the beautiful line you just learned.

The missing thing in *all* of these references — and therefore our opening — is a **living companion you talk to**. Rekhta has the content but no voice; ElevenLabs/Hume have the voice but no Urdu-learning soul; Sarvam has the language tech but no consumer character. **Alif Aur Tarana is the combination none of them ships.**

---

### How these were captured
Full-page screenshots via Playwright (Chromium, 1440×900 viewport, JPEG q90) on 18 June 2026. To refresh: re-run the same navigations and save into this folder. Live pricing/feature claims should always be re-checked against the linked sources in [`../02-voice-stack-research.md`](../02-voice-stack-research.md).
