# 03 · Architecture — making a cascade *feel* live

How the pieces from [`02`](02-voice-stack-research.md) wire into a system that delivers the [`01`](01-product-vision.md) experience. The central engineering question: **can a cascade (STT→LLM→TTS) feel as alive as a native speech-to-speech model?** Answer: **yes, if you stream and overlap the stages.**

---

## 1. The decision: cascade, not native S2S (for now)

| | **Cascade (STT → LLM → TTS)** ✅ chosen | **Native S2S (Gemini Live)** |
|---|---|---|
| Control over Urdu voice/accent | **Full** — pick exact ElevenLabs/Azure voice per companion | Low — shared voices, auto-language |
| Persona control | **Full** — system prompt + few-shot per companion | Partial — one model's behaviour |
| Expressiveness | **Full** — ElevenLabs v3 tags, SSML | Good but not directable per-line |
| Swap a component | **Easy** — change one box | All-or-nothing |
| Cost control | **Full** — route/cache per stage | Per-minute, harder to cap |
| Latency | ~1 s with streaming (good enough) | ~300–500 ms (best) |
| Your priority match | **Feel + control + free > speed** ✅ | Optimises the thing you ranked *last* |

Your explicit ranking — **(a) voice/feel/personality > (b) free > (c) tools/memory > (d) live speed** — points unambiguously at the cascade. It maximises the top three priorities and only slightly concedes the fourth, which streaming then largely recovers. ([Realtime vs pipeline trade-offs](https://softcery.com/lab/ai-voice-agents-real-time-vs-turn-based-tts-stt-architecture), [pipeline latency budget](https://www.channel.tel/blog/voice-ai-pipeline-stt-tts-latency-budget))

> **Decision:** Cascade for MVP. Architect it so the LLM and TTS boxes are swappable, and keep **Gemini Live as a drop-in "turbo/live mode"** for Phase 4.

---

## 2. The latency problem — and the fix

A **naive** cascade waits for each stage to fully finish: you stop talking → wait for full transcript → wait for full LLM answer → wait for full audio → hear it. That stacks up to **2–4 seconds of dead air**, which kills the conversational feel ([architecture overview](https://www.bitbytes.io/blog/ai-voice-speech-tools/ai-voice-agent-architecture-pipeline)).

The **fix is streaming overlap** — the stages run concurrently:

```
You:    "…iss sher ka matlab samjhao na" |stop|
        └─ STT streams partial transcripts ──┐
                                             ▼ (LLM starts on partial / on endpoint)
        LLM:  streams tokens ──► "Aah…" "Ahmed" "Faraz" "…" ──┐
                                                              ▼ (TTS starts at first sentence)
        TTS:  sentence-by-sentence audio ──► 🔊 first words play within ~1s of you stopping
```

- **STT** emits partial transcripts while you're still talking.
- **LLM** begins generating the moment your turn ends, and **streams tokens**.
- **TTS** starts synthesising the **first complete sentence** while the LLM is still writing the rest.

With this overlap, production cascades **consistently hit sub-1-second response times** ([latency budget](https://www.channel.tel/blog/voice-ai-pipeline-stt-tts-latency-budget)).

### The latency budget (target)
Natural human turn gaps average ~200 ms; the industry target is **sub-300 ms time-to-first-audio (TTFA)** for "instant" feel ([latency budget](https://www.channel.tel/blog/voice-ai-pipeline-stt-tts-latency-budget)). Our realistic cascade target with free cloud APIs:

| Stage | Budget | Notes |
|-------|--------|-------|
| Endpointing (detect you're done) | 100–300 ms | Semantic VAD, see §3 |
| STT finalise (streaming) | ~100–200 ms | Most work already done during speech |
| LLM time-to-first-token | 200–500 ms | Gemini Flash is fast; local Alif faster on warm GPU |
| TTS time-to-first-audio | 150–400 ms | ElevenLabs/Azure streaming |
| **Total perceived TTFA** | **~0.7–1.2 s** | Feels conversational; matches your "feel > speed" |

> Given your priority order, **~1 s is a feature, not a failure.** A beat before Alif sighs and answers is *more* romantic, not less. We optimise feel first, shave latency later.

---

## 3. Turn-taking — knowing when you've finished

The thing that makes voice agents feel dumb is cutting you off or waiting awkwardly. Two mechanisms:

- **VAD (Voice Activity Detection):** detects sound vs silence (e.g. Silero VAD, runs locally, free).
- **Semantic turn detection:** decides whether you've finished a *thought*, not just paused — so "ranjish hi sahi… [thinks] …dil hi dukhane ke liye aa" isn't chopped at the pause. LiveKit ships a transformer-based semantic turn detector with **sub-75 ms P99 latency** (open, reusable) ([latency budget](https://www.channel.tel/blog/voice-ai-pipeline-stt-tts-latency-budget)).
- **Barge-in:** if you start talking while a companion is speaking, TTS stops immediately. Essential for natural feel and saves TTS spend.

> For a *learning* app specifically: bias the endpointer to be **patient** (learners pause to think and to find words). Better to wait a beat than to interrupt someone hunting for an Urdu word.

---

## 4. The orchestrator — Pipecat (no LangChain)

[`02`](02-voice-stack-research.md) and [`05`](05-tech-stack.md) land on **Pipecat** (open-source, Python) as the pipeline engine. Why it fits:

- **Pipeline-first**: you compose processors (VAD → STT → LLM → TTS) into a graph; audio frames flow through; each processor receives frames, processes, yields frames ([Pipecat vs LiveKit](https://www.f22labs.com/blogs/difference-between-livekit-vs-pipecat-voice-ai-platforms/)).
- **Runs on localhost** with just API keys — mic/file in, speakers out, **no media-server infra to stand up** for dev ([comparison](https://webrtc.ventures/2026/03/choosing-a-voice-ai-agent-production-framework/)).
- **Has the plugins we need**: ElevenLabs, **Sarvam** (STT *and* TTS), Groq (Whisper), OpenAI, Deepgram, Gladia, Cartesia, Play.ht, plus Silero VAD and turn detection.
- **Best DX for a 1:1 voice assistant** — which is exactly what Alif/Tarana are ([comparison](https://www.cekura.ai/blogs/pipecat-vs-livekit-the-real-difference)).

**LiveKit Agents** is the alternative — *infrastructure-first*, WebRTC media server, multi-participant rooms, production-grade transport, and the best turn detector. It's heavier to run (Docker, server) and overkill for 1:1 ([comparison](https://www.f22labs.com/blogs/difference-between-livekit-vs-pipecat-voice-ai-platforms/)).

> **Decision:** **Pipecat** for the agent logic. If/when we need rock-solid WebRTC transport at scale or the "majlis" multi-character room, adopt **LiveKit for transport** (the two compose — Pipecat can run over LiveKit's transport).

---

## 5. Full system diagram

```
┌──────────────────────────── CLIENT (Next.js PWA / RN / extension) ───────────────────────────┐
│  Mic capture ──► WebRTC/WebSocket audio ──►            ◄── streamed TTS audio ──► Speaker      │
│  UI: companion orb, tri-script transcript (Nastaʿlīq / Devanagari / Roman), tap-to-hear        │
└───────────────────────────────────────────────┬───────────────────────────────────────────────┘
                                                 │ (audio in / audio out, streamed)
┌────────────────────────────── BACKEND: FastAPI + Pipecat ─────────────────────────────────────┐
│                                                                                                │
│   [Silero VAD] ─► [Semantic turn detect] ─► [STT: Sarvam Saaras v3 | Whisper(local/Groq)]      │
│                                                     │ partial+final transcript                  │
│                                                     ▼                                           │
│        ┌──────────────────────── AGENT CORE (the "brain") ───────────────────────────┐         │
│        │  Persona layer: Alif / Tarana system prompt + few-shot + Urdu-density dial   │         │
│        │  LLM router → Gemini 2.5 Flash | local Alif-1.0 | Groq/OpenRouter (fallback) │         │
│        │  Tool calls (function-calling):                                              │         │
│        │     • memory.recall / memory.write   (mem0)                                  │         │
│        │     • rekhta.lookup  (local poetry corpus + datasets)                        │         │
│        │     • youtube.transcript  (lyrics / interviews)                              │         │
│        │     • web.search  (Tavily)                                                   │         │
│        └───────────────────────────────────┬──────────────────────────────────────────┘         │
│                                             │ streamed text (sentence by sentence)              │
│                                             ▼                                                   │
│   [TTS router] ─► ElevenLabs v3 (signature/emotion) | Azure (bulk)  ──► cache ──► audio out     │
│                                                                                                │
│   Side-writes: transcript + new vocabulary + session recap ──► Memory store (mem0 + SQLite/pg) │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Tool details in [`04`](04-tools-and-integrations.md); tech/repo in [`05`](05-tech-stack.md).

---

## 6. Key cross-cutting design choices

### 6.1 Tri-script rendering pipeline
Every companion utterance is produced as Urdu text by the LLM, then transliterated to **Devanagari** and **Roman** for display. Options:
- LLM-native (ask Gemini to return all three scripts in a structured JSON field) — simplest, good quality.
- Dedicated transliteration (e.g. `urduhack`, `aksharamukha`, or indic transliteration libs) — deterministic, offline.
> **Pick:** LLM-native for MVP (one call, structured output), validate against a transliteration lib for the *taught* word specifically.

### 6.2 TTS caching (the cost lever)
Hash each `(text, voice, settings)` → if seen before, replay the stored audio. Companion catchphrases, common teaching lines, and repeated words become **free after first generation**. This is what makes ElevenLabs' 10k-char free tier survive contact with real use. (See [`07`](07-execution-roadmap.md) budget.)

### 6.3 The "Urdu-density dial"
A per-user scalar (0–1) in memory that the persona layer injects into the system prompt ("current target: ~40% Urdu vocabulary, explain anything above B1"). The companion raises it gradually and obeys "thoda mushkil/aasaan karo". This is the pedagogy from [`01`](01-product-vision.md) made into a parameter.

### 6.4 Streaming contract
Backend ↔ client speaks a small event protocol over WebSocket: `partial_transcript`, `final_transcript`, `assistant_token`, `assistant_sentence`, `tts_audio_chunk`, `tool_call`, `barge_in`. Keep it tiny and typed (Pydantic models) — no framework needed.

### 6.5 Fallback & degradation ladder
- STT: Sarvam → Groq Whisper → local Whisper.
- LLM: Gemini Flash → Groq/OpenRouter → local Alif-1.0.
- TTS: ElevenLabs (if quota + line needs emotion) → Azure → (paid OpenAI only if both exhausted).
- **Offline mode** (no internet): local Whisper + local Alif-1.0 + … no Urdu TTS locally yet, so degrade to **text-only** with tap-to-hear from cached audio. (A genuine gap; tracked in [`07`](07-execution-roadmap.md) risks.)

---

## 7. Why this satisfies the brief

| Your requirement | How the architecture delivers |
|------------------|-------------------------------|
| (a) Urdu voice, accent, personality | Cascade gives full TTS + persona control; ElevenLabs/Azure Urdu voices |
| Real emotional signals (hmm, pauses, gasps) | ElevenLabs v3 tags + Azure SSML `<break>`; patient turn-taking |
| (b) Free | Free-tier APIs + local fallbacks on your 4060; TTS caching |
| (c) Memory + tools | mem0 + function-calling tools (Rekhta/YouTube/web) in the agent core |
| (d) Live feel | Streaming overlap → ~1 s TTFA; barge-in; semantic turn detection |
| Avoid LangChain | Pipecat + plain Python; no LangChain anywhere |

Next: the tools that give the companions reach → [`04-tools-and-integrations.md`](04-tools-and-integrations.md).

---

### Sources for this document
- [Realtime vs pipeline voice agents](https://softcery.com/lab/ai-voice-agents-real-time-vs-turn-based-tts-stt-architecture)
- [Voice AI pipeline & the 300ms budget](https://www.channel.tel/blog/voice-ai-pipeline-stt-tts-latency-budget)
- [AI voice agent architecture overview](https://www.bitbytes.io/blog/ai-voice-speech-tools/ai-voice-agent-architecture-pipeline)
- [Pipecat vs LiveKit (f22labs)](https://www.f22labs.com/blogs/difference-between-livekit-vs-pipecat-voice-ai-platforms/) · [Choosing a voice framework (WebRTC.ventures)](https://webrtc.ventures/2026/03/choosing-a-voice-ai-agent-production-framework/) · [Pipecat vs LiveKit (Cekura)](https://www.cekura.ai/blogs/pipecat-vs-livekit-the-real-difference)
- [Gemini Live API capabilities](https://ai.google.dev/gemini-api/docs/live-api/capabilities)
