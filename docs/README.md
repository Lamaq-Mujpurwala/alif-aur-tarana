# Alif Aur Tarana — Project Documentation

> A conversational, voice-first companion app to **learn Urdu through the content and feelings you already love** — music, poetry, prose and the people behind them. Two AI companions, **Alif** (the hopeless romantic) and **Tarana** (the elegant rationalist), act as friends *and* teachers who meet you exactly where you are (Hindi + English + a little Urdu) and pull you deeper into the language.

**Document date:** 18 June 2026 · **Status:** Research & planning (pre-MVP) · **Author:** Research pass by Claude (Voice-Agent build specialist mode)

> ⚠️ **Pricing/limits caveat:** Every price, free-tier quota and language-support claim below was sourced on/around 18 June 2026 and is linked to its source. Voice-AI pricing changes *fast* — re-verify the linked pages before committing money or architecture.

---

## 0. How to read these docs

| # | Doc | What's inside |
|---|-----|----------------|
| — | **README.md** (this file) | Executive summary, the headline recommendation, the single most important finding, and the index. |
| 01 | [`01-product-vision.md`](01-product-vision.md) | The product, the two companions' personas & "writers' bible", the pedagogy (how do you actually *learn* from this), UX principles, what makes it different. |
| 02 | [`02-voice-stack-research.md`](02-voice-stack-research.md) | The deep research: every STT, LLM and TTS option, with Urdu support, free vs paid, latency, expressiveness and pros/cons. This is the evidence base. |
| 03 | [`03-architecture.md`](03-architecture.md) | Cascade vs native speech-to-speech, the chosen pipeline, the latency budget, streaming, turn-taking, and how to make a cascade *feel* live. |
| 04 | [`04-tools-and-integrations.md`](04-tools-and-integrations.md) | The agent's tools: Rekhta, YouTube, web search, and conversation memory — options and recommendations. |
| 05 | [`05-tech-stack.md`](05-tech-stack.md) | Backend, frontend, infra, repo layout, and the explicit "why not LangChain" answer. |
| 06 | [`06-cross-platform.md`](06-cross-platform.md) | Web PWA, mobile app, the YouTube browser extension, and how to hook into YouTube Music on a phone. |
| 07 | [`07-execution-roadmap.md`](07-execution-roadmap.md) | The phased build plan, milestones, the "spend ₹0 for the MVP" strategy, cost projections and risks. |
| 08 | [`08-decision-matrix.md`](08-decision-matrix.md) | The master options matrix — every component, every candidate, advantage/disadvantage/cost in one place. |
| 09 | [`09-companion-craft-and-prompts.md`](09-companion-craft-and-prompts.md) | Adab/respect doctrine, ElevenLabs v3 audio-tag flow, and the full **dense system prompts** for Alif & Tarana. |
| 10 | [`10-pronunciation-coaching.md`](10-pronunciation-coaching.md) | How the companions catch & coach pronunciation (experience + architecture); the Urdu hard-sounds curriculum. |
| 11 | [`11-voice-identity-and-cloning.md`](11-voice-identity-and-cloning.md) | Giving Alif a voice — Voice Design vs cloning, and the ElevenLabs **consent rules** that change the plan. |
| 12 | [`12-setup-and-api-keys.md`](12-setup-and-api-keys.md) | **One-time** guide to every service signup + API key (do this before building). |
| 13 | [`13-mvp-build-plan.md`](13-mvp-build-plan.md) | The **local MVP** build sequence, lean tech choices, and the to-do checklist. |
| 14 | [`14-companion-voice-prompts.md`](14-companion-voice-prompts.md) | Ready-to-paste ElevenLabs **Voice Design** prompts for Alif & Tarana + lines to audition them. |
| 15 | [`15-elevenlabs-v3-mastery.md`](15-elevenlabs-v3-mastery.md) | Deep ElevenLabs v3 guide (stability, tags, language/accent, consistency) + the **final Urdu-script prompts**. |
| — | [`inspiration/`](inspiration/) | Design & UX snapshots collected from reference products, with notes. |

---

## 1. Executive summary (the TL;DR)

**The single most important finding of this research:**

> **Urdu text-to-speech is a *narrow* field. Most of the famous voice providers do not support Urdu at all.** Of every provider checked, only **ElevenLabs**, **Microsoft Azure**, **Google Gemini (native audio)** and **OpenAI** can speak Urdu. **Sarvam (Bulbul TTS), Google Cloud TTS, NVIDIA Magpie, Deepgram Aura and Cartesia Sonic cannot speak Urdu** (see [`02`](02-voice-stack-research.md) for the receipts). Since your #1 priority is *"Urdu voice, accent and personality,"* this fact drives the entire architecture: **the voice (TTS) layer is the scarce, decisive resource — pick it first, build everything else around it.**

The good news: the two providers that *can* speak Urdu beautifully are also the two with the best expressive control and a usable free tier — **ElevenLabs** (best-in-class emotion via "v3 audio tags" like `[laughs]`, `[sighs]`, `[whispers]`) and **Azure** (4 Urdu neural voices + the most generous free quota at 500,000 characters/month).

### The headline recommendation

Build a **cascade pipeline** (Speech-to-Text → LLM → Text-to-Speech), *not* a native speech-to-speech model, for the MVP. Your stated priority — *"a well-thought answer with the perfect feel beats a fast answer"* — is exactly what a cascade is good at: it gives you full, independent control over the Urdu voice, the accent, the personality prompt, and the expression. Native speech-to-speech (Gemini Live) trades that control for latency you said you don't need yet.

| Layer | MVP pick (free) | Why | Upgrade path |
|-------|-----------------|-----|--------------|
| **Speech-to-Text** | **Sarvam Saaras v3** (free credits) for Hinglish/Urdu code-mixing, **or local faster-whisper** on your RTX 4060 (free forever) | Sarvam is purpose-built for Indian code-mixed speech (how you actually talk); local Whisper is unlimited & private | Groq Whisper (free, ultra-fast) as a hot-swap |
| **LLM (brain)** | **Gemini 2.5 Flash** free tier (1,500 req/day, no card) | Understands Urdu+Hindi+English, huge free quota, function-calling for tools | Local **Alif-1.0-8B** (Urdu-specialised) on your GPU; Sarvam-M API |
| **Text-to-Speech (the voice)** | **ElevenLabs v3** for the "wow" demo voice + **Azure** for everyday volume | ElevenLabs = the feeling; Azure = 500k free chars so you don't burn ElevenLabs' 10k | Self-host an open Urdu TTS later if volume explodes |
| **Orchestration** | **Pipecat** (open-source, Python) | Pipeline-first, best 1:1 voice-agent DX, has Sarvam + ElevenLabs plugins, no LangChain needed | LiveKit for production WebRTC transport at scale |
| **Tools** | `youtube-transcript-api` + Tavily (1k searches/mo free) + a **local Rekhta corpus** (no official API exists) | All free; Rekhta has no API so we use open datasets + curated content | Supadata/Firecrawl fallbacks |
| **Memory** | **mem0** (open-source, self-host) over SQLite/pgvector | Gives "it remembers us" cheaply; swappable | Postgres + pgvector at scale |
| **Backend** | **FastAPI** (Python) | Your comfort zone, async, websocket-native, perfect for Pipecat | — |
| **Frontend** | **Next.js PWA** first | One codebase → installable on web *and* phone | Expo/React Native for a true native app + the YouTube extension |

**This entire MVP stack costs ₹0** within free tiers, with local-on-your-4060 fallbacks for STT and the LLM so you are never blocked by a rate limit. Full cost analysis in [`07`](07-execution-roadmap.md).

### The one fun coincidence worth knowing

There is already an open-source, Urdu-specialised LLM **literally named "Alif"** — [Alif-1.0-8B-Instruct](https://huggingface.co/large-traversaal/Alif-1.0-8B-Instruct) by Traversaal AI (Feb 2026), which beats Llama-3.1-8B and Gemma-2-9B on Urdu tasks and runs (4-bit quantised) on your RTX 4060. We can literally power the companion *Alif* with a model *named* Alif. ([announcement](https://blog.traversaal.ai/announcing-alif-1-0-our-first-urdu-llm-outperforming-other-open-source-llms/), [paper](https://arxiv.org/html/2510.09051v1))

---

## 2. What "success" looks like (restating your goals)

From your brief and the whiteboard photo, in **your** priority order:

1. **(a) Urdu voice, accent & personality** — supersedes raw speed. The feeling is the product.
2. **(b) Free** — maximise every provider's free tier; spend ₹0 on the MVP unless 1000% unavoidable.
3. **(c) Conversation history + web search + tools** — so it remembers you and can reach beyond its own knowledge (especially via Rekhta & YouTube).
4. **(d) Live, instant conversation feel** — nice to have, pursued *after* the above.

Two distinct, witty, sarcasm-capable personalities (**Alif** & **Tarana**) who teach like friends, understand Hinglish, and never feel like a textbook. They consume the media *you* want to consume (a song, a ghazal, a poet's interview) and turn it into a lesson and a conversation.

**Explicit constraint you set:** avoid **LangChain** (too heavy). Honoured throughout — see [`05`](05-tech-stack.md) for the lean alternative.

---

## 3. The 30-second architecture picture

```
                 ┌──────────────────────────────────────────────────────────┐
   You speak ──► │  STT  ─►  LLM (Alif/Tarana brain + tools)  ─►  TTS  ─► 🔊  │
 (Hinglish/Urdu) │ Sarvam   Gemini 2.5 Flash / local Alif-1.0    ElevenLabs   │
                 │ /Whisper  + tools: Rekhta · YouTube · Web · Memory  /Azure  │
                 └──────────────────────────────────────────────────────────┘
                        ▲ streamed end-to-end so it feels live (~1s) ▲
```

Details, latency budget and the streaming trick that makes a cascade feel instant: [`03-architecture.md`](03-architecture.md).

---

## 4. Open decisions for you (not blocking)

These are choices where your taste matters more than research; defaults chosen so work can start now:

- **Demo-first voice:** ElevenLabs (max feeling, tiny free quota) vs Azure (good feeling, huge free quota). *Default: prototype both, ship the demo on ElevenLabs.*
- **Local vs cloud brain:** Gemini Flash (zero setup) vs local Alif-1.0 on your 4060 (private, unlimited, but you manage it). *Default: Gemini Flash for MVP, wire local as fallback.*
- **First surface:** Web PWA vs the YouTube extension. *Default: Web PWA first (fastest path to a talking companion), extension in Phase 3.*

See [`08-decision-matrix.md`](08-decision-matrix.md) for the full trade-off tables.

---

## 5. Master source list

All external claims across these docs are linked inline at point of use. The most load-bearing sources:

- ElevenLabs — [Urdu TTS](https://elevenlabs.io/text-to-speech/urdu) · [pricing](https://elevenlabs.io/pricing) · [v3 audio tags](https://elevenlabs.io/blog/v3-audiotags) · [Agents pricing](https://elevenlabs.io/pricing/agents)
- Azure Speech — [pricing](https://azure.microsoft.com/en-us/pricing/details/speech/) · [language support](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support) · [Urdu voices](https://json2video.com/ai-voices/azure/languages/urdu/)
- Google Gemini — [native audio](https://blog.google/technology/google-deepmind/gemini-2-5-native-audio/) · [Live API](https://ai.google.dev/gemini-api/docs/live-api/capabilities) · [pricing](https://ai.google.dev/gemini-api/docs/pricing) · [rate limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- Sarvam — [TTS](https://www.sarvam.ai/apis/text-to-speech) · [STT](https://www.sarvam.ai/apis/speech-to-text) · [pricing](https://docs.sarvam.ai/api-reference-docs/pricing) · [Saaras v3 ASR](https://www.sarvam.ai/blogs/asr) · [open models](https://www.sarvam.ai/blogs/sarvam-30b-105b)
- Groq — [speech-to-text](https://console.groq.com/docs/speech-to-text) · [rate limits](https://console.groq.com/docs/rate-limits)
- Local — [faster-whisper](https://github.com/SYSTRAN/faster-whisper) · [Alif-1.0-8B](https://huggingface.co/large-traversaal/Alif-1.0-8B-Instruct)
- Frameworks — [Pipecat vs LiveKit](https://www.f22labs.com/blogs/difference-between-livekit-vs-pipecat-voice-ai-platforms/) · [mem0 vs Letta](https://vectorize.io/articles/mem0-vs-letta)
- Tools — [Rekhta](https://www.rekhta.org/) · [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) · [Tavily/Brave search](https://brave.com/learn/best-search-api-2026/)
- Architecture — [voice pipeline latency budget](https://www.channel.tel/blog/voice-ai-pipeline-stt-tts-latency-budget) · [realtime vs pipeline](https://softcery.com/lab/ai-voice-agents-real-time-vs-turn-based-tts-stt-architecture)
