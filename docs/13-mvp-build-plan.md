# 13 · MVP Build Plan (Local) & To-Do

**Goal of this MVP:** prove the hard part works — that *we speak, and Alif/Tarana answer in a beautiful, in-character Urdu voice with real feeling, accurately, tri-script.* **"Local" = runs on your machine, no deployment** (it does NOT mean local-only models; we use the best cloud APIs from [`12`](12-setup-and-api-keys.md)).

> Success = the [`01 §9`](01-product-vision.md) Faraz moment, live from your mic, ~1s, in-character, with adab. Nothing more. We resist scope creep hard.

---

## 1. In scope / out of scope

**In (MVP):**
- The cascade loop: **mic → STT (Sarvam) → LLM (Gemini, persona+adab) → TTS (ElevenLabs) → playback**, streamed.
- **Both companions** selectable (Alif via Voice Design, Tarana via her voice).
- **Tri-script output** (Roman/Urdu/Devanagari) on screen, taught-word highlighted.
- **Thin memory** (SQLite): name, learned words, density dial — enough that it remembers within & across a couple of sessions.
- **One tool wired** end-to-end (start with `rekhta.lookup` over a tiny local corpus, or `web.search`) to prove tool-calling.
- **Thin pronunciation**: "check my pronunciation" → reference audio + Gemini-audio feedback ([`10 §2`](10-pronunciation-coaching.md)).

**Out (deferred):** deployment, auth, YouTube extension, mobile app, full mem0/pgvector, multi-character "majlis", live-S2S turbo, pronunciation full loop, the big curated corpus.

---

## 2. Build sequence (each step independently testable)

### Step 0 — Bootstrap (½ day)
- Create monorepo skeleton ([`05 §4`](05-tech-stack.md)): `apps/api` (FastAPI) + `apps/web` (Next.js). `uv` env, `.env` from [`12 §6`](12-setup-and-api-keys.md).
- Health-check endpoint; confirm every key loads (a tiny `check_keys.py` that pings each service once).

### Step 1 — Voice spike, no mic (½ day) — *prove the feel first*
- Script: hardcoded text → Gemini (Alif persona, [`09 §4.1`](09-companion-craft-and-prompts.md)) → ElevenLabs v3 (Alif `voice_id`, Natural stability, with audio tags) → save/play WAV.
- Generate the Faraz demo line; **listen.** Tune Voice Design prompt + tags until Alif *sounds right*. Repeat for Tarana.
- ✅ Gate: "haaye" test passes — the voices feel real and respectful.

### Step 2 — STT in (½ day)
- Mic capture (Python `sounddevice`, push-to-talk) → Sarvam Saaras → text. Verify Hinglish/Urdu transcription quality; wire **local faster-whisper** + **Groq** as fallbacks behind a tiny `STTRouter`.
- ✅ Gate: you speak Hinglish, get accurate text.

### Step 3 — Full loop via Pipecat (1–2 days) — *the core*
- Assemble Pipecat pipeline: VAD (Silero) → STT → LLM (persona) → TTS → playback, **streamed** (sentence-level TTS).
- Implement the **output contract** ([`09 §3`](09-companion-craft-and-prompts.md)): `speech` (tagged) to TTS, `display` (tri-script, clean) returned to client.
- Barge-in + patient endpointing ([`03 §3`](03-architecture.md)).
- ✅ Gate: real spoken back-and-forth with one companion, ~1s, in-character, adab intact.

### Step 4 — Minimal web client (1–2 days)
- Next.js page: companion picker (Alif/Tarana), mic button (push-to-talk), **animated orb**, **tri-script transcript** with taught-word highlight + tap-to-hear. WebSocket to the API.
- ✅ Gate: the [`01 §9`](01-product-vision.md) demo works in the browser.

### Step 5 — Memory + one tool + thin pronunciation (1–2 days)
- SQLite memory: store name, `learned_vocab`, `urdu_density`; inject recall into the system prompt; re-surface a word.
- Wire **one** tool via Gemini function-calling (`rekhta.lookup` over a ~20-poem local JSON, or `web.search`) — prove the agent loop ([`05 §2`](05-tech-stack.md), no LangChain).
- Thin pronunciation: "check my pronunciation of X" → reference TTS + Gemini-audio feedback.
- ✅ Gate: it remembers a word across a restart; "samjhao yeh sher" pulls from the corpus; a pronunciation nudge works.

### Step 6 — Polish & in-character eval (ongoing)
- Run the adab/persona eval set ([`09 §5`](09-companion-craft-and-prompts.md)): zero "tu", zero broken character, zero disrespect, no answer-dumps.
- Add TTS caching ([`03 §6.2`](03-architecture.md)) so repeated lines stop billing.
- ✅ Gate: a 5-minute conversation feels like Alif/Tarana, not an LLM.

> **Realistic timeline:** a believable end-to-end MVP in **~1.5–2 weeks** of focused evenings (you + Vedant can split api/voice vs web/corpus). Steps 1 and 3 are where the magic is proven — don't rush them.

---

## 3. Tech choices for the *local* MVP (lean)

| Concern | MVP choice | Why |
|---------|-----------|-----|
| Loop engine | **Pipecat**, local (no media server) | best 1:1 DX, runs on localhost ([`03 §4`](03-architecture.md)) |
| Transport | WebSocket (FastAPI) | simplest; WebRTC later |
| STT | Sarvam → Groq → local Whisper (router) | accuracy + free fallback |
| LLM | Gemini 2.5 Flash (Ollama/Alif optional) | quota + tools |
| TTS | ElevenLabs v3 (Alif design + Tarana) | the feel; Azure added when card ready |
| Memory | **SQLite** (file) | zero infra; swap to mem0/pgvector later |
| Web | Next.js (one page) | fast |

> Note: for the *very first* loop you can even skip the web client and prove Steps 1–3 from a Python script — fastest path to hearing it work.

---

## 4. The To-Do (canonical checklist)

These are mirrored into the live task list. **Before any of this: complete the key checklist in [`12 §7`](12-setup-and-api-keys.md).**

- [ ] **T0** Bootstrap monorepo + `.env` + `check_keys.py` (all services ping OK)
- [ ] **T1** Voice spike (text→Gemini-persona→ElevenLabs); tune Alif Voice Design + Tarana; pass "haaye" gate
- [ ] **T2** Mic→STT (Sarvam) with Whisper/Groq fallback router
- [ ] **T3** Pipecat full streamed loop + output contract (speech/display) + barge-in
- [ ] **T4** Next.js client: companion picker, mic, orb, tri-script transcript + tap-to-hear
- [ ] **T5** SQLite memory (recall a word) + one function-calling tool + thin pronunciation check
- [ ] **T6** Adab/persona eval set + TTS caching + polish

---

## 5. Definition of done (this MVP)
- [ ] Speak from the mic → a companion replies in voice, ~1s, **in-character with adab** (never "tu", never disrespect a poet).
- [ ] Reply is accurate Urdu, **tri-script** on screen, taught word highlighted + tap-to-hear.
- [ ] Both companions selectable; each sounds distinct (Alif soothing/playful, Tarana elegant).
- [ ] It remembers at least one thing about you across a restart.
- [ ] One tool call works end-to-end; one pronunciation nudge works.
- [ ] Runs entirely locally within free tiers.

That's the proof. Once it's real, we pick the next surface from [`06`](06-cross-platform.md).

---

### Related
- Keys first: [`12-setup-and-api-keys.md`](12-setup-and-api-keys.md)
- The voices/prompts it runs on: [`09-companion-craft-and-prompts.md`](09-companion-craft-and-prompts.md)
- Architecture it implements: [`03-architecture.md`](03-architecture.md)
