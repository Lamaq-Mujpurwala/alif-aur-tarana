# 02 · Voice Stack Research (STT · LLM · TTS · Speech-to-Speech)

This is the evidence base. Every component the pipeline needs, every credible candidate, with **Urdu support, free vs paid, latency, expressiveness, and a verdict.** Claims are linked to sources inline.

> **Reading guide:** ✅ = supports Urdu / good · ⚠️ = partial / caveats · ❌ = no Urdu / unsuitable. "Free" = usable free tier exists today (June 2026).

---

## 0. The finding that frames everything: Urdu TTS is scarce

Before the tables, the headline. I checked every major voice provider for **Urdu text-to-speech** specifically:

| Provider | Urdu TTS? | Source |
|----------|-----------|--------|
| ElevenLabs | ✅ Yes | [elevenlabs.io/text-to-speech/urdu](https://elevenlabs.io/text-to-speech/urdu) |
| Microsoft Azure | ✅ Yes (4 voices) | [Azure Urdu voices](https://json2video.com/ai-voices/azure/languages/urdu/) |
| Google **Gemini** native audio | ✅ Yes (in 9 Indic langs) | [Gemini Live Indic languages](https://www.geosquare.in/how-to-use-google-gemini-live-in-9-indian-languages-282189865573-news/) |
| OpenAI (TTS / Realtime) | ✅ Yes | [TTS comparison noting Urdu](https://lushbinary.com/blog/ai-voice-tts-api-comparison-deepgram-cartesia-openai/) |
| **Sarvam Bulbul** (TTS) | ❌ No (11 Indic langs, Urdu excluded) | [Bulbul v2 languages](https://www.analyticsvidhya.com/blog/2025/05/bulbul-v2-by-sarvam/) |
| **Google Cloud TTS** (Chirp 3/Neural2/WaveNet) | ❌ No (no ur-IN/ur-PK in voice list) | [Cloud TTS voice list](https://docs.cloud.google.com/text-to-speech/docs/list-voices-and-types) |
| **NVIDIA Magpie** TTS | ❌ No (7 langs, no Urdu) | [Magpie model card](https://build.nvidia.com/nvidia/magpie-tts-multilingual) |
| **Deepgram Aura** | ❌ No (English/Spanish only) | [Aura languages](https://developers.deepgram.com/docs/tts-models) |
| **Cartesia Sonic** | ⚠️ Hindi yes, Urdu unlisted | [Cartesia Sonic](https://www.cartesia.ai/sonic/) |

> **Implication:** "Nvidia?" on your whiteboard — NVIDIA's hosted TTS (Magpie) **cannot speak Urdu today**, so it's out for the *voice*. Sarvam — your other front-runner — is excellent for STT and as an LLM, but its **Bulbul TTS does not do Urdu either.** The Urdu *voice* must come from **ElevenLabs, Azure, Gemini, or OpenAI.** This is the most important architectural constraint in the project.

---

## A. Speech-to-Text (transcription) — "it hears us"

Requirements: understands **Urdu + Hindi + English + code-mixed (Hinglish)** the way you actually talk; low latency for streaming; free.

| Option | Urdu | Code-mix (Hinglish) | Free tier | Latency / speed | Verdict |
|--------|------|---------------------|-----------|-----------------|---------|
| **Sarvam Saaras v3 / Saarika** | ✅ ur-IN | ✅ **Built for it** (Hinglish/Tanglish, diarization, word timestamps) | ₹1,000 free credits on signup, no card | Real-time capable; tuned for Indian speech | **Primary pick** — purpose-built for *how you speak* |
| **Local faster-whisper (large-v3, int8)** | ✅ (`ur`) | ⚠️ decent | **Free forever** (your GPU) | ~7× real-time on RTX 4060, ~2.5 GB VRAM | **Best fallback** — unlimited, private, no rate limits |
| **Groq Whisper large-v3 / turbo** | ✅ (`ur`) | ⚠️ decent | **Free**, 2,000 req/day | **164× real-time** (fastest hosted) | Excellent hot-swap; great for batch (YouTube) |
| **ElevenLabs Scribe** | ✅ | ⚠️ | Part of 10k free credits | Good | Fine if already on ElevenLabs |
| **Gemini (built-in to Live API)** | ✅ | ✅ | Free tier | Native in S2S path | Only relevant if you go native S2S |
| **Deepgram Nova** | ⚠️ limited Indic | ⚠️ | $200 credit | Very fast | Weaker on Indic vs Sarvam |

**Why Sarvam for STT:** Saaras v3 was trained on **1M+ hours of real Indian speech**, reports **19.31% WER on IndicVoices** and is claimed to **outperform GPT-4o Transcribe, Gemini 3 Pro, Deepgram Nova-3 and Scribe v2 on Indian-language accuracy**, with explicit **code-mixing (Hinglish/Tanglish)** support ([Sarvam ASR blog](https://www.sarvam.ai/blogs/asr), [STT API](https://www.sarvam.ai/apis/speech-to-text)). That code-mix handling is *exactly* the "understand how we talk" requirement from your brief.

**Why local Whisper as the safety net:** on your RTX 4060 (8 GB), faster-whisper runs **large-v3 at ~7× real-time using only ~2.5 GB VRAM** with int8 quantization ([faster-whisper](https://github.com/SYSTRAN/faster-whisper), [setup/benchmarks](https://localaimaster.com/blog/faster-whisper-guide)). That means **free, private, unlimited dev transcription** — you can build all day without touching a quota.

> **STT recommendation:** Sarvam Saaras v3 in production for the live mic (best code-mix accuracy), **local faster-whisper** for development and for the YouTube/batch transcription tool, **Groq Whisper** wired as an instant fallback.

---

## B. The LLM (the brain) — "it thinks in Urdu/Hindi/English"

Requirements: genuinely understands **Urdu + Hindi + English code-mix**, holds a persona, calls tools (function-calling), generous free tier.

| Option | Urdu/Hindi quality | Tool/function calling | Free tier | Runs on your 4060? | Verdict |
|--------|--------------------|-----------------------|-----------|--------------------|---------|
| **Gemini 2.5 Flash** | ✅ strong multilingual | ✅ native | **1,500 req/day, 15 RPM, 1M TPM, no card** | n/a (cloud) | **Primary brain** — best free quota + quality combo |
| **Gemini 2.5 Pro** | ✅ strongest | ✅ | ⚠️ ~50 req/day free | n/a | For hard/poetry tasks, sparingly |
| **Alif-1.0-8B-Instruct** (Traversaal) | ✅ **Urdu-specialised**, beats Llama-3.1-8B & Gemma-2-9B on Urdu | ⚠️ via prompt | **Free (open weights)** | ✅ 4-bit (~5–6 GB) | **Local Urdu specialist** — private, unlimited |
| **Sarvam-M (24B)** | ✅ Indic-tuned (Mistral-Small base) | ✅ | Free credits via API; weights open | ❌ too big for 8 GB | Strong Indic API option |
| **Groq-hosted Llama/Qwen** | ✅ Qwen3 multilingual | ✅ | Free, fast | n/a | Fast cloud fallback |
| **OpenRouter free models** (DeepSeek, Llama, Qwen) | ✅ varies | ✅ | Free rotating models | n/a | Convenient multi-model fallback |
| **Gemma 3 (local)** | ✅ decent multilingual | ⚠️ | Free | ✅ small sizes | Generic local option |

**On Gemini Flash free tier:** widely reported at **1,500 requests/day, 15 requests/minute, 1M tokens/minute, no credit card, no expiry** ([rate limits](https://ai.google.dev/gemini-api/docs/rate-limits), [free-tier guide](https://tokenmix.ai/blog/gemini-api-free-tier-limits)). Note: Google **may use free-tier prompts for training** — keep anything sensitive on the local model. Note also free limits have fluctuated in 2025–26 ([Google cut some limits](https://www.howtogeek.com/gemini-slashed-free-api-limits-what-to-use-instead/)), so keep a fallback wired.

**On Alif-1.0 (the namesake):** open weights at [large-traversaal/Alif-1.0-8B-Instruct](https://huggingface.co/large-traversaal/Alif-1.0-8B-Instruct) (also a 3B). Available as **GGUF for Ollama/LM Studio/llama.cpp**; 4-bit quant fits your 8 GB GPU. Trained via multilingual synthetic-data distillation for "culturally aligned, high-performance Urdu understanding" ([blog](https://blog.traversaal.ai/announcing-alif-1-0-our-first-urdu-llm-outperforming-other-open-source-llms/), [paper](https://arxiv.org/html/2510.09051v1)). **Caveat:** an 8B model is weaker at general reasoning/tool-use than Gemini Flash — best used for *Urdu phrasing/teaching* tasks, or as the offline brain, not necessarily the orchestrator.

> **LLM recommendation:** **Gemini 2.5 Flash** as the default brain (quota + quality + tool-calling). Wire **local Alif-1.0-8B (via Ollama)** as both an offline fallback *and* a specialist you can call for "give me the most natural Urdu phrasing of X." Keep **Groq/OpenRouter** as a third fallback. A thin model-router (your own ~50 lines, no LangChain) picks among them — see [`05`](05-tech-stack.md).

---

## C. Text-to-Speech (the voice) — **the scarce, decisive layer**

Requirements (your #1 priority): **beautiful Urdu, controllable accent, distinct personalities, real emotional signals** (hmm, pauses, gasps, laughs), streaming. Only 4 providers can speak Urdu at all — so the table is short and decisive.

| Option | Urdu | Expressiveness (emotion/tags) | Free tier | Latency | Distinct voices | Verdict |
|--------|------|-------------------------------|-----------|---------|-----------------|---------|
| **ElevenLabs (v3)** | ✅ | ✅✅✅ **Best** — audio tags `[laughs] [sighs] [whispers] [excited] [sad] [clears throat] [x accent]`, multi-character | **10k chars/mo (~10 min)**, 2.5k/request, *no commercial rights, attribution required* | Low (streaming) | ✅ huge library + cloning | **The "feel" voice** — unmatched emotion |
| **Microsoft Azure** | ✅ **4 voices**: ur-PK-Uzma(F)/Asad(M), ur-IN-Gul(F)/Salman(M) | ✅ SSML styles, prosody, `<break>`, emphasis | **500k chars/mo (F0)**, throttles after | Low | ✅ 4 Urdu + styles | **The "volume" voice** — best free quota |
| **Google Gemini** native audio | ✅ (auto language) | ✅✅ emotion-aware, reacts to *your* emotion, interruptible; 30 voices | Free tier (preview) | Very low (S2S) | ⚠️ shared 30 voices, **can't force language code** in native-audio out | Great for native S2S, less *control* |
| **OpenAI** TTS / Realtime | ✅ | ✅✅ steerable ("speak warmly") | ❌ no free tier (paid) | Low–med | limited preset voices | Capable but **paid** → deprioritise |
| Sarvam Bulbul | ❌ | — | — | — | — | **No Urdu** |
| Google Cloud TTS | ❌ | — | — | — | — | **No Urdu** |
| NVIDIA Magpie | ❌ | — | — | — | — | **No Urdu** |
| Deepgram Aura | ❌ | — | — | — | — | **No Urdu** |
| Cartesia Sonic | ⚠️ Hindi only | ✅✅ (~40 ms, laughter/emotion) | small | **fastest (~40 ms TTFA)** | many | Hindi fallback only; no confirmed Urdu |

### Why ElevenLabs is the "feel" voice
Eleven v3 introduced **audio tags** — bracketed directives the model performs: `[laughs]`, `[laughs harder]`, `[whispers]`, `[sighs]`, `[exhales]`, `[excited]`, `[sad]`, `[angry]`, `[sorrowful]`, `[clears throat]`, even `[x accent]` and **multi-character dialogue** ([v3 audio tags](https://elevenlabs.io/blog/v3-audiotags), [emotional context](https://elevenlabs.io/blog/eleven-v3-audio-tags-expressing-emotional-context-in-speech)). This is *exactly* the "hmm, pauses, reactions, gasps, real emotional signals" from your brief. **No other Urdu-capable provider gives this level of performance control.**

**The catch:** the free tier is **10,000 characters/month (~10 minutes of audio), max 2,500 chars/request, no commercial usage rights, and requires attribution** ([pricing](https://elevenlabs.io/pricing), [char limits](https://help.elevenlabs.io/hc/en-us/articles/13298164480913)). That's enough for crafting *demo* lines and the companions' signature phrases, not for all-day free conversation.

### Why Azure is the "volume" voice
Azure's free **F0 tier gives 500,000 characters/month** ([Azure Speech pricing](https://azure.microsoft.com/en-us/pricing/details/speech/)) — **50× ElevenLabs' free quota** — and has **four real Urdu neural voices**: `ur-PK-UzmaNeural` (F), `ur-PK-AsadNeural` (M), `ur-IN-GulNeural` (F), `ur-IN-SalmanNeural` (M) ([Urdu voices](https://json2video.com/ai-voices/azure/languages/urdu/)). Expressiveness is via **SSML** (styles, `<break>` for pauses, `<emphasis>`, prosody rate/pitch) — less magical than ElevenLabs' tags but very serviceable, and it covers both Pakistani and Indian Urdu accents (nice: Alif could lean ur-IN, Tarana ur-PK, or vice-versa).

### The hybrid that makes the economics work
Use a **two-tier voice strategy** (detail in [`07`](07-execution-roadmap.md)):
- **ElevenLabs** for the *signature* moments — the demo, the companions' catchphrases, the emotionally-loaded lines — and **cache them** (same line → reuse the audio file, never re-bill).
- **Azure** for the *bulk* of everyday generated speech (its 500k/mo free quota absorbs real usage).
- A tiny **TTS router** picks per-utterance based on "does this line need maximum emotion?" + remaining quota.

> **TTS recommendation:** **ElevenLabs v3 (feel) + Azure (volume), with aggressive caching.** This is the single most important decision in the build. Revisit only if an open Urdu TTS matures enough to self-host (none is production-ready for expressive Urdu today).

---

## D. All-in-one Speech-to-Speech (native) — the alternative architecture

Instead of cascading STT→LLM→TTS, these models take audio in and emit audio out directly. Lower latency, more natural interruptions/emotion — but you lose fine control over the Urdu voice/accent and persona separation.

| Option | Urdu | Free | Strengths | Why not (for us, now) |
|--------|------|------|-----------|------------------------|
| **Gemini Live (native audio)** | ✅ | ✅ free tier | Emotion-aware, interruptible, ~real-time, single API | **Auto-detects/chooses language** (can't pin a fixed Urdu accent), shared voices, less persona/voice control ([Live API](https://ai.google.dev/gemini-api/docs/live-api/capabilities), [native audio](https://blog.google/technology/google-deepmind/gemini-2-5-native-audio/)) |
| **ElevenLabs Conversational AI (Agents)** | ✅ | ⚠️ ~15 min/mo free | Best voice + turn-taking, managed | Free minutes tiny (~15 min/mo); paid scales fast ([Agents pricing](https://elevenlabs.io/pricing/agents), [cost article](https://pxlpeak.com/blog/ai-tools/elevenlabs-pricing-guide)) |
| **OpenAI Realtime (gpt-realtime)** | ✅ | ❌ paid only | Very natural | **No free tier**; ~$0.18–0.46/min uncached ([pricing](https://openai.com/api/pricing/), [real-world cost](https://hackernoon.com/openai-realtime-api-pricing-in-2026-real-world-data-from-4000-measured-sessions)) |
| **Hume EVI 3 / 4-mini** | ⚠️ Hindi yes, **Urdu unconfirmed** | ✅ free tier | Empathic, prosody-aware emotion | Urdu not in listed langs (Hindi/Arabic are) ([EVI](https://www.hume.ai/empathic-voice-interface)) |

> **S2S recommendation:** **Not for the MVP.** Native S2S optimises *latency*, which you explicitly ranked last. It also *reduces* control over the Urdu voice and persona — the opposite of your #1 priority. **Keep Gemini Live as a Phase-4 "turbo/live mode" option** once the cascade product is loved. ElevenLabs Agents is the closest managed all-in-one but its free minutes are too small to live on.

---

## E. The "Nvidia?" question from your whiteboard — answered

You flagged NVIDIA on the board. Findings:
- **NVIDIA Magpie TTS (hosted on build.nvidia.com, free API key): does NOT support Urdu** — only en/es/fr/de/zh/vi/it ([Magpie](https://build.nvidia.com/nvidia/magpie-tts-multilingual)). So NVIDIA is **out for the voice.**
- NVIDIA's relevance is **as compute**: your **RTX 4060 is itself NVIDIA hardware** that runs faster-whisper (STT) and Alif-1.0/Gemma (LLM) locally and free. That's the right way to "use NVIDIA" here — local inference, not their hosted TTS.
- (NVIDIA Riva can be self-hosted for STT but adds heavy Docker/infra for no Urdu-TTS payoff — skip.)

---

## F. Component-level verdicts (carried into the architecture)

| Layer | Production pick | Fallback(s) | Local (free, on your 4060) |
|-------|-----------------|-------------|----------------------------|
| **STT** | Sarvam Saaras v3 | Groq Whisper | faster-whisper large-v3 |
| **LLM** | Gemini 2.5 Flash | Groq / OpenRouter | Alif-1.0-8B / Gemma 3 (Ollama) |
| **TTS** | ElevenLabs v3 (feel) + Azure (volume) | OpenAI (paid, last resort) | — (no production-ready open Urdu TTS) |
| **(later) S2S** | Gemini Live "turbo mode" | ElevenLabs Agents | — |

Next: how these wire together so a cascade *feels* live → [`03-architecture.md`](03-architecture.md).

---

### Sources for this document
- ElevenLabs: [Urdu TTS](https://elevenlabs.io/text-to-speech/urdu) · [pricing](https://elevenlabs.io/pricing) · [v3 audio tags](https://elevenlabs.io/blog/v3-audiotags) · [emotional context tags](https://elevenlabs.io/blog/eleven-v3-audio-tags-expressing-emotional-context-in-speech) · [char limits](https://help.elevenlabs.io/hc/en-us/articles/13298164480913) · [Agents pricing](https://elevenlabs.io/pricing/agents) · [Agents cost guide](https://pxlpeak.com/blog/ai-tools/elevenlabs-pricing-guide)
- Azure: [Speech pricing](https://azure.microsoft.com/en-us/pricing/details/speech/) · [language support](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support) · [Urdu voices](https://json2video.com/ai-voices/azure/languages/urdu/)
- Google Gemini: [native audio](https://blog.google/technology/google-deepmind/gemini-2-5-native-audio/) · [Live API capabilities](https://ai.google.dev/gemini-api/docs/live-api/capabilities) · [pricing](https://ai.google.dev/gemini-api/docs/pricing) · [rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) · [free-tier guide](https://tokenmix.ai/blog/gemini-api-free-tier-limits) · [9 Indic langs incl Urdu](https://www.geosquare.in/how-to-use-google-gemini-live-in-9-indian-languages-282189865573-news/)
- Google Cloud TTS (no Urdu): [voice list](https://docs.cloud.google.com/text-to-speech/docs/list-voices-and-types) · [Chirp 3 HD](https://docs.cloud.google.com/text-to-speech/docs/chirp3-hd)
- Sarvam: [TTS](https://www.sarvam.ai/apis/text-to-speech) · [STT](https://www.sarvam.ai/apis/speech-to-text) · [Saaras v3 ASR](https://www.sarvam.ai/blogs/asr) · [pricing](https://docs.sarvam.ai/api-reference-docs/pricing) · [Bulbul v2 languages](https://www.analyticsvidhya.com/blog/2025/05/bulbul-v2-by-sarvam/) · [Sarvam-M / open models](https://www.sarvam.ai/blogs/sarvam-30b-105b)
- Groq: [speech-to-text](https://console.groq.com/docs/speech-to-text) · [rate limits](https://console.groq.com/docs/rate-limits) · [pricing](https://www.eesel.ai/blog/groq-pricing)
- NVIDIA: [Magpie TTS](https://build.nvidia.com/nvidia/magpie-tts-multilingual) · [Magpie card](https://huggingface.co/nvidia/magpie_tts_multilingual_357m)
- OpenAI: [API pricing](https://openai.com/api/pricing/) · [Realtime real-world cost](https://hackernoon.com/openai-realtime-api-pricing-in-2026-real-world-data-from-4000-measured-sessions)
- Cartesia: [Sonic](https://www.cartesia.ai/sonic/) · [TTS comparison (OpenAI Urdu note)](https://lushbinary.com/blog/ai-voice-tts-api-comparison-deepgram-cartesia-openai/)
- Hume: [EVI](https://www.hume.ai/empathic-voice-interface)
- Deepgram: [TTS models/languages](https://developers.deepgram.com/docs/tts-models) · [pricing](https://deepgram.com/pricing)
- Local: [faster-whisper](https://github.com/SYSTRAN/faster-whisper) · [faster-whisper guide](https://localaimaster.com/blog/faster-whisper-guide) · [Alif-1.0-8B](https://huggingface.co/large-traversaal/Alif-1.0-8B-Instruct) · [Alif announcement](https://blog.traversaal.ai/announcing-alif-1-0-our-first-urdu-llm-outperforming-other-open-source-llms/) · [Alif paper](https://arxiv.org/html/2510.09051v1)
