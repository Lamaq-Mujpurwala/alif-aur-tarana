# 14 · Companion Voice Prompts (ElevenLabs Voice Design)

Ready-to-paste **Voice Design** prompts to *generate* Alif's and Tarana's voices (our chosen path — your reference voices are public figures, so we capture the *vibe*, not the person; see [`11`](11-voice-identity-and-cloning.md)). Plus audition lines so you can hear whether a generated voice is really *them*.

## How to use (5 minutes)
1. ElevenLabs → **Voices → My Voices → Add a new voice → Voice Design**.
2. Paste a **description** prompt below. For **preview text**, paste one of the *audition lines* (§3) so you hear it speaking Urdu, not generic English.
3. Generate → you get **3 options** → pick the one that feels most like the character.
4. Save it, open it, **copy its `voice_id`**, and put it in `backend/.env`:
   `ALIF_VOICE_ID=...` / `TARANA_VOICE_ID=...`
5. Re-run `uv run python check_keys.py` — the voice lines should flip to **set**.

> Tip: try 2–3 of the prompt variants per companion and keep your favourite. Then run the audition lines with audio tags (§3) to confirm `[sighs]`, `[laughs softly]`, `[gently]` actually land on that voice (tag response varies by voice — [`09 §2`](09-companion-craft-and-prompts.md)).

---

## 1. Alif — soothing, playful, young (3 prompt variants)

**Variant A — intimate & soothing (recommended first try)**
> A warm young man in his mid-twenties, speaking Urdu/Hindustani with a gentle North-Indian accent. Soft, slightly breathy, soothing timbre with an unhurried, intimate delivery — like reciting poetry to a close friend late at night. Tender, romantic, a little dreamy; never harsh, never announcer-like. Natural conversational warmth with subtle emotional rise and fall.

**Variant B — playful & charming**
> A charming, playful Urdu-speaking man in his mid-twenties with a light, youthful North-Indian accent. Bright and mischievous but warm — the friend who teases you affectionately and laughs easily. Expressive and quick, with a soft musical lilt, a hint of flirtation, and an easy smile in the voice. Clear and intimate, not theatrical.

**Variant C — poetic & velvety (balanced)**
> A young Urdu poet's voice, mid-twenties, velvety and warm with a refined North-Indian/Lucknowi accent. Calm, romantic and expressive, with graceful pacing and gentle breathiness — equally able to whisper a couplet and laugh softly. Soulful and sincere, intimate rather than performative.

---

## 2. Tarana — elegant, composed, warm (3 prompt variants)

**Variant A — warm & elegant (recommended first try)**
> An elegant Urdu-speaking woman in her late twenties to early thirties, refined Lucknowi/North-Indian accent. Composed, clear and unhurried, with understated warmth — graceful and articulate, the way a beloved teacher speaks. Gentle authority, precise diction, a soft reassuring quality; never cold, never theatrical.

**Variant B — crisp & precise (the rationalist)**
> A poised, articulate Urdu-speaking woman, early thirties, with a crisp refined North-Indian accent. Calm, exact and intelligent, with measured pacing and elegant clarity — every word deliberate. Quietly confident and dry-witted, with warmth held in reserve and revealed gently.

**Variant C — soft mentor**
> A gentle, elegant Urdu-speaking woman in her early thirties, soft Lucknowi accent. Soothing, patient and encouraging, with a warm low register and unhurried, melodic delivery. The calm, kind voice of someone who makes you feel capable; refined and graceful, with a faint smile in the tone.

---

## 3. Audition lines (use as preview text, and to test the feel)

Paste these as the Voice Design **preview text**, then later test in the app. They mix Hinglish↔Urdu, exercise the audio tags, and include the hard Perso-Arabic sounds ([`10 §3`](10-pronunciation-coaching.md)) so you can hear if the voice carries them.

### Alif — audition lines
- **Romantic (with tags):**
  `[warmly] Aah… aap ko pata hai, 'ishq' aur 'mohabbat' ek nahi hain. [softly] Mohabbat woh narmi hai jo dheere aati hai… [sighs] aur ishq? Ishq woh aag hai jo jala bhi de aur zinda bhi rakhe.`
- **Playful (with tags):**
  `[laughs softly] Khwaab, janab — kabaab nahi, warna main bhookha ho jaaun! [warmly] Woh 'kh' gale se aati hai, halki si… kh-waab. Zara aap kahiye?`
- **Teaching, intimate:**
  `[whispers] Faraz sahib farmate hain — 'ranjish hi sahi, dil hi dukhane ke liye aa.' [sighs] Kya baat hai, na?`

### Tarana — audition lines
- **Etymology (with tags):**
  `[gently] 'Firaaq' — judaai, separation. [warmly] Lekin dhyaan dijiye: ismein sirf doori nahi, intezaar ka dard bhi hai. [thoughtful] Faarsi se aaya lafz hai — isiliye itna naazuk lagta hai.`
- **Gentle correction (hard sound):**
  `[gently] Qareeb hai. Woh pehli aawaaz 'qaaf' hai — thodi gehri, halaq se: q-alam, na ki k-alam. [reassuring] Phir se, aaram se — main yahin hoon.`
- **Warm encouragement:**
  `[smiling] Bohot khoob! Aap ne 'firaaq' bilkul theek pakda. [warmly] Aaj aap ne ek naya lafz apna liya.`

> A neutral 250-char+ preview (more stable per [`09 §2`](09-companion-craft-and-prompts.md)) — good for the first generation:
>
> Alif: `[warmly] Aaiye, baithiye. Aaj main aap ko ek lafz ki kahani sunata hoon — ek aisa lafz jise shayar baar baar istemaal karte hain, kyunki usmein dard bhi hai aur khoobsurati bhi. [softly] Sunne ke liye tayyar hain? [laughs softly] Achha, toh shuru karte hain.`
>
> Tarana: `[gently] Aaiye, hum mil kar Urdu ke ek khoobsurat lafz ko samajhte hain. [warmly] Main jaldi nahi karungi — hum aaram se, lafz dar lafz aage badhenge. [reassuring] Aur agar kuch samajh na aaye, toh bas kahiye, main phir se samjha dungi.`

---

## 4. After you pick the voices
- Put `ALIF_VOICE_ID` / `TARANA_VOICE_ID` in `backend/.env`.
- We then run **T1** (the voice spike): text → Gemini-in-persona → ElevenLabs → you *hear* Alif and Tarana. That's the "haaye" gate.
- Note stability: default **Natural**; try **Creative** for the most emotional signature lines.

Related: [`11-voice-identity-and-cloning.md`](11-voice-identity-and-cloning.md) · [`09-companion-craft-and-prompts.md`](09-companion-craft-and-prompts.md)
