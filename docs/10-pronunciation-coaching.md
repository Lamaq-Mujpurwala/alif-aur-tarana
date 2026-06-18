# 10 · Pronunciation Coaching — Experience & Architecture

Your point #2: speaking Urdu *well* means getting pronunciation right, and the companions must catch mispronunciations, push back kindly, and coach until it's correct. Here's the honest reality, the approach, and the architecture.

---

## 1. The honest reality: no off-the-shelf Urdu pronunciation scorer

The mature, phoneme-level "pronunciation assessment" APIs **do not support Urdu**:
- **Azure Pronunciation Assessment** — gives per-phoneme accuracy + fluency + prosody + completeness, but only for **33 locales, and Urdu is not among them** ([supported languages](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support), [how-to](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-pronunciation-assessment)). (Microsoft offers an intake form for unlisted languages.)
- **SpeechAce / SpeechSuper** — strong phoneme scoring, but English/Mandarin/European-focused; **no Urdu/Hindi** ([SpeechSuper](https://www.speechsuper.com/), [SpeechAce](https://www.speechace.com/)).

So we **cannot** buy a "score this Urdu phoneme" black box. We build pronunciation coaching ourselves — and because our companions are LLM-driven and audio-capable, we actually can, pragmatically and for free.

> Bonus: doing it ourselves lets us target the *Urdu-specific* sounds that generic scorers ignore — and those are exactly the sounds Hindi-speakers miss and Urdu-lovers care about most.

---

## 2. The approach — a three-signal hybrid

We combine three free signals; no single one is perfect, but together they catch real errors and let the companion coach convincingly.

### Signal 1 — STT round-trip ("did it come through?")
When the user repeats a target word, transcribe their audio (Sarvam/Whisper) and compare to the expected word.
- If the ASR **mishears** it (transcribes a different/garbled word), that's a strong, language-agnostic signal the pronunciation was off. (If the model trained on millions of hours can't hear it as `khwaab`, a listener won't either.)
- Compare via **phonetic/transliteration distance** (e.g., normalise to Roman, Levenshtein/Soundex-style distance) to gauge *how* far off.
- **Free, fast, deterministic.** Great first filter.

### Signal 2 — Gemini audio-in as the nuanced judge
Send the user's short audio clip **plus** the target word + a reference to **Gemini 2.5** (it natively accepts audio input and reasons about speech — recognises pronunciation, emotion, intent) ([multimodal audio](https://googlecloudplatform.github.io/applied-ai-engineering-samples/genai-on-vertex-ai/gemini/prompting_recipes/multimodal/multimodal_prompting_audio/)). Ask for *specific, kind, phoneme-aware* feedback:
> "The learner is attempting the Urdu word **خواب (khwaab)**. Here is their audio. Identify the specific sound they got wrong (e.g., the خ 'khe'), describe it simply, and rate close/closer/correct. Be encouraging."
- Gemini gives the *teacherly* feedback ("the خ comes from the back of the throat, softer than a 'k'") that a score alone can't.
- **Free on the Gemini tier.** This is the heart of the coaching.

### Signal 3 — Reference + "repeat after me" loop
The companion always provides the *correct* model:
- TTS the word (ElevenLabs/Azure), with a **slow/syllable-broken** version available (Azure SSML `<prosody rate="-40%">` and phoneme `<break>`s; ElevenLabs slow delivery).
- Loop: **companion says it → user repeats → signals 1+2 assess → companion coaches → repeat until "correct".**
- Tap-to-hear-slow on any word, always.

> **Verdict:** Signal 1 gates (cheap), Signal 2 coaches (smart), Signal 3 models (always). The companion narrates all of it in-character — never "Score: 72%", always "[gently] qareeb hai — woh 'qaaf' thodi gehri…".

---

## 3. The Urdu hard-sounds curriculum (our edge)

Hindi-speakers systematically flatten the Perso-Arabic sounds — and *that* flattening is exactly what separates "speaking Hindi words" from "speaking Urdu". The companions watch for these specifically:

| Sound | Letter | Common error (Hindi-speaker) | Coaching anchor |
|-------|--------|------------------------------|-----------------|
| **qaaf** | ق | becomes hard 'k' (kalam vs qalam) | "from deep in the throat, behind 'k'" |
| **khe** | خ | becomes 'kh'/'k' (khwaab→kawaab) | "soft scrape at the back, like clearing gently" |
| **ghain** | غ | becomes 'g' (gham→gam) | "a soft gargle, voiced version of خ" |
| **ain** | ع | dropped/glottal (ishq, ilm) | "a catch in the throat before the vowel" |
| **z-cluster** | ز ذ ض ظ | all flattened to 'j'/'z' | "all 'z', never 'j' — zindagi not jindagi" |
| **noon-ghunna** | ں | nasalisation lost | "let it ring through the nose" |
| **fe vs phe** | ف | 'ph' instead of 'f' (firaaq) | "f from the lip+teeth, not a puff" |

This table seeds both the coaching logic *and* a future "sound of the day" feature. Tarana owns this (precision); Alif makes it playful ("kabaab nahi, khwaab! [laughs]").

---

## 4. The experience (how it feels, in-character)

**In-conversation, gentle:** when Signal 1 flags a mishearing on an Urdu word mid-chat, the companion doesn't interrupt the flow harshly — it lands a light touch: *"[warmly] chhoti si baat — woh lafz 'firaaq' hai, zara 'f' ke saath… firaaq. Bilkul."*

**Dedicated "repeat after me":** the user (or companion) starts a focus loop on a word. Companion models → user tries → coach → retry. Celebrates the win loudly: *"[excited] haan! ab woh 'qaaf' bilkul saheeh! [warmly] sun ke maza aa gaya."*

**Never discouraging:** errors are framed as *closeness* ("qareeb hai", "bas zara sa aur"), never failure. Adab applies here too — the companion is a patient ustaad, never a strict examiner.

**Progress that's felt, not graded:** no scores shown. Instead, memory tracks the user's "sounds to work on" and the companion notices growth ("[smiling] aap ka 'kh' pehle se kitna behtar ho gaya hai").

---

## 5. Architecture & data

```
"Repeat after me" loop:
  companion.say(word)  ──► TTS reference (+ slow variant cached)
        │
  user audio ─► STT (Sarvam/Whisper) ─► Signal 1: expected vs heard (phonetic distance)
        │                                   │ if far → likely error
        └─► Gemini(audio + target) ─────────┴─► Signal 2: which phoneme, how to fix (kind, specific)
        │
  companion coaches in-character ─► retry until "correct" ─► memory.write(pron_progress)
```

**Memory schema addition** ([extends `04 §4`](04-tools-and-integrations.md)):
```
pron_progress:  sound (e.g. "qaaf"), words_attempted[], status (working/improving/solid),
                last_practiced, notes ("drops the ain in 'ishq'")
```

**Tooling:**
- `pron.assess(audio, target_word) -> {heard, distance, phoneme_feedback, verdict}` — wraps Signals 1+2.
- `tts.reference(word, slow=False)` — cached correct model (also feeds tap-to-hear).
- Phonetic distance: small util in `packages/tri-script` (Roman-normalise + edit distance); no new heavy dep.

**MVP scope note:** for the very first local MVP ([`13`](13-mvp-build-plan.md)), pronunciation can be a **thin version** — reference audio + Gemini-audio feedback on an explicit "check my pronunciation" request. The full STT-round-trip loop + sounds-tracking is a fast-follow once the core conversation works.

---

### Sources for this document
- Azure Pronunciation Assessment (no Urdu): [language support](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support) · [how-to](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-pronunciation-assessment) · [language-learning use](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-learning-with-pronunciation-assessment)
- Alternatives (no Urdu/Hindi): [SpeechSuper](https://www.speechsuper.com/) · [SpeechAce](https://www.speechace.com/)
- Gemini audio understanding: [multimodal audio prompting](https://googlecloudplatform.github.io/applied-ai-engineering-samples/genai-on-vertex-ai/gemini/prompting_recipes/multimodal/multimodal_prompting_audio/) · [Gemini 2.5 native audio](https://blog.google/technology/google-deepmind/gemini-2-5-native-audio/)
- STT for the round-trip: [Sarvam Saaras](https://www.sarvam.ai/apis/speech-to-text) · [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
