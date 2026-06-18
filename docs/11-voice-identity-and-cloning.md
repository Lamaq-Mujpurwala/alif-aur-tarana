# 11 · Voice Identity & Cloning — Giving Alif His Voice

Your point #3: Tarana's voice is sorted (a good ElevenLabs voice), but Alif needs a **soothing, playful, young** voice that isn't in the stock library, and you have **real-life reference people** whose voices you'd want to clone. Here's exactly how cloning works, **the one rule that changes the plan**, and the recommended path.

---

## 1. The rule that changes everything (read this first)

> **On ElevenLabs you cannot freely clone a reference person's voice.** Two hard constraints:
> - **Professional Voice Cloning (PVC) is *your own voice only*.** It requires a **voice-captcha**: you read a prompt aloud within ~10s and the system matches it against your uploaded samples. *"You can only create a Professional Voice Clone of your own voice. Even with their consent, you cannot clone someone else's voice."* ([ElevenLabs](https://help.elevenlabs.io/hc/en-us/articles/36842751624209-Can-I-create-a-Professional-Voice-Clone-of-someone-else-s-voice))
> - **Instant Voice Cloning (IVC) requires explicit consent/rights** from the voice owner; cloning a celebrity/public figure or anyone without permission **violates the Terms of Service** and can carry legal consequences ([consent rules](https://margabagus.com/elevenlabs-voice-cloning-consent/), [voice cloning docs](https://elevenlabs.io/docs/eleven-api/concepts/voice-cloning)).

**What this means for your "reference real-life people":**
- If they are **people you know who will consent** (a friend, family member, a willing voice actor) → ✅ cloning is possible (paths C/D below).
- If they are **celebrities / singers / actors / public figures** → ❌ not allowed on ElevenLabs (ToS + captcha). For those, we **approximate the *vibe*** with Voice Design instead (path A) — we capture "young, soothing, playful" without copying a specific protected voice.

This is both a compliance reality and, honestly, the ethical line — Alif should have a voice that's *his*, not an impersonation.

---

## 2. The five ways to give Alif a voice (ranked for our case)

| Path | What | Audio needed | Plan / cost | Consent issue | Quality | Verdict |
|------|------|--------------|-------------|---------------|---------|---------|
| **A. Voice Design (text→voice)** | Describe the voice in words; get 3 generated options; pick one | none | Free tier (costs only preview credits) | **None** — synthetic, original | Good; can vary by prompt | 🟢 **MVP pick for Alif** |
| **B. Voice Library** | Browse thousands of community voices for a match | none | Free | None (pre-cleared) | Varies | 🟢 quick stop-gap / Tarana-style |
| **C. IVC of a consenting person** | Few-shot clone from a friend/voice-actor who consents | **1–5 min** clean audio | **Starter $5/mo** | Need documented consent | Good | 🟡 if you have a willing voice |
| **D. PVC (own voice / owner self-clones)** | Fine-tuned, near-perfect clone | **30 min min, ~3 hr optimal** | **Creator $22/mo+** | Own-voice only (captcha) | **Best** | 🟡 later, for the *signature* Alif |
| **E. Keep a stock voice for now** | Use any decent stock male voice temporarily | none | Free | None | OK | 🟢 fallback to unblock the MVP |

Sources: [IVC vs PVC](https://help.elevenlabs.io/hc/en-us/articles/13313681788305-What-is-the-difference-between-Instant-Voice-Cloning-IVC-and-Professional-Voice-Cloning-PVC), [Voice Design](https://elevenlabs.io/voice-design), [voice cloning overview](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning).

---

## 3. Recommended plan for Alif

### For the MVP (now): **Voice Design** (path A)
Describe Alif precisely and generate his voice — no consent issues, no paid plan, available immediately, and it's a *unique* voice we own as IP. A starting prompt to iterate on:

> *"A warm, young Urdu-speaking man in his mid-twenties. Soft, slightly breathy, soothing timbre with a playful, romantic lilt. Unhurried, intimate delivery — like reciting poetry to a close friend late at night. Natural North-Indian/Urdu accent, gentle and expressive, never harsh or announcer-like."*

Generate 3, pick the closest, then test it against our audio-tag vocabulary ([`09 §2`](09-companion-craft-and-prompts.md)) — confirm `[sighs]`, `[laughs softly]`, `[whispers]` land well (tag effectiveness varies by voice). Iterate the prompt until Alif *sounds* like Alif.

### For the signature release (later): **PVC** (path D)
When you want the definitive Alif, do a Professional Voice Clone. Because PVC is **own-voice-only**, the path is:
- **Option D1:** one of you (or a friend) whose natural voice fits "young/soothing/playful" records **30 min–3 hr** of clean Urdu/Hinglish speech and runs the PVC under *their own* account (they pass the captcha). That clone becomes Alif. Fully ToS-compliant.
- **Option D2:** if your reference person consents, **they** create the PVC themselves and share access (since it must be their captcha-verified voice).

### If you have a willing voice now: **IVC** (path C)
A friend/voice-actor with the perfect Alif voice + documented consent → record 1–5 min pristine audio → Instant Clone on **Starter ($5/mo)**. Faster than PVC, lower (but good) quality, a nice middle step.

> **Net recommendation:** ship the MVP on **Voice Design Alif** (free, unblocked, ToS-clean). Pursue **PVC** only when you've locked the character and have a consenting voice to immortalise. Don't let the perfect voice block proving the product.

---

## 4. Recording guide (for when you do clone — C or D)

If/when you record a real voice for IVC/PVC ([best practices](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning)):
- **Clean signal:** no reverb, no background noise/music, **one speaker only**. PVC clones *everything* it hears, including flaws and room noise.
- **Gear:** a decent cardioid mic (e.g., Audio-Technica AT2020 / Rode NT1) into an audio interface; quiet, soft-furnished room. A good USB mic + treated corner is fine to start.
- **Content:** natural, expressive Urdu/Hinglish speech across moods (warm, playful, wistful) — not monotone reading — so the clone captures Alif's *range*. For PVC aim 30 min–3 hr; for IVC 1–5 min of the *best* clean audio.
- **Consent record:** keep a signed/recorded consent statement from the voice owner. For PVC, the owner must do the captcha themselves.

---

## 5. Decision needed from you (to plan the cloning phase)

The MVP is unblocked (Voice Design). But to plan Alif's *final* voice, one fork matters:

- **Are your reference people personal contacts who would consent** (friend / family / willing voice actor)? → we plan **IVC or owner-led PVC**.
- **Or are they public figures** (a singer/actor whose voice you admire)? → we **cannot clone them**; we use **Voice Design to capture the vibe**, and optionally find a real consenting person with a similar voice for PVC later.

> **DECISION (locked 18 Jun 2026):** the reference voices are *public figures* (singers/actors), which ElevenLabs **cannot** clone (ToS + voice-captcha). Alif's voice will therefore be built with **Voice Design** to capture the vibe (young / soothing / playful) — see §3. Cloning is off the table unless a *consenting* real person with the right voice appears later.

---

## 6. Tarana's voice
You've already found a good ElevenLabs voice for Tarana — lock it in `apps/api/agent/personas/tarana.py` as `voice_id`, set stability **Natural**, and run the same audio-tag check ([`09 §2`](09-companion-craft-and-prompts.md): `[gently]`, `[softly]`, `[warmly]`, `[smiling]`). Keep the chosen `voice_id`s in `.env`, not hardcoded.

---

### Sources for this document
- [PVC is own-voice-only](https://help.elevenlabs.io/hc/en-us/articles/36842751624209-Can-I-create-a-Professional-Voice-Clone-of-someone-else-s-voice) · [IVC vs PVC](https://help.elevenlabs.io/hc/en-us/articles/13313681788305-What-is-the-difference-between-Instant-Voice-Cloning-IVC-and-Professional-Voice-Cloning-PVC)
- [Voice cloning overview & requirements](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning) · [how it works](https://elevenlabs.io/docs/eleven-api/concepts/voice-cloning)
- [Voice Design](https://elevenlabs.io/voice-design) · [Voice Design docs](https://elevenlabs.io/docs/eleven-creative/voices/voice-design)
- [Consent rules & compliance (2026)](https://margabagus.com/elevenlabs-voice-cloning-consent/) · [ethical cloning practices](https://prateeksha.com/blog/ethical-voice-cloning-elevenlabs-permissions-scripts-best-practices)
