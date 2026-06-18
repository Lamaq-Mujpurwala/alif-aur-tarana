# 07 · Execution Roadmap, Free-Tier Strategy, Cost & Risks

The plan to go from zero to a loved product, the strategy to **spend ₹0 on the MVP**, what it costs if it grows, and what could go wrong.

---

## 1. Phased roadmap

Each phase ends with something you can *use*, not just code that exists.

### Phase 0 — Spike the voice (1 weekend) — *prove the feel*
**Goal:** hear Alif speak one beautiful Urdu line, well.
- Get keys: Gemini, Sarvam, ElevenLabs, Azure (all free).
- Script (no UI): text → Gemini (Alif persona) → ElevenLabs v3 (with `[sighs]`) → play.
- Generate the [`01 §9`](01-product-vision.md) Faraz demo line in both ElevenLabs and Azure; **compare the feel.**
- **Exit:** you have an audio file that makes you go "haaye". This decides the demo voice.

### Phase 1 — The talking companion (2–3 weeks) — *the core loop*
**Goal:** real-time-ish spoken conversation with one companion.
- FastAPI + Pipecat pipeline: VAD → STT (Sarvam / local Whisper) → Gemini (persona) → TTS (Eleven/Azure), streamed.
- Next.js PWA: mic (push-to-talk), companion orb, **tri-script transcript**, tap-to-hear.
- One companion (start with **Tarana** — her measured style is more forgiving of latency; or **Alif** if you want max charm first).
- **Exit:** you talk, she answers in voice, ~1s, tri-script on screen. The product is real.

### Phase 2 — Memory + tools (2–3 weeks) — *it becomes a friend*
**Goal:** it remembers you and reaches beyond itself.
- Add second companion + companion switch/handoff.
- Wire tools: `memory` (mem0), `rekhta.lookup` (local corpus), `youtube.transcript`, `web.search`.
- Implement the **Urdu-density dial** + session recaps.
- Build the **starter poetry corpus** (your favourite poets) + tri-script.
- **Exit:** "samjhao yeh gaana" works end-to-end; Alif recalls a word from last session.

### Phase 3 — YouTube extension (2 weeks) — *learn while watching*
- MV3/WXT extension: detect video, "explain this line", overlay companion, same backend.
- **Exit:** watch a ghazal on YouTube, get it taught to you live.

### Phase 4 — Native mobile + live mode (3–4 weeks) — *everywhere, faster*
- Expo app: background audio, **share-sheet** ("share song → companion").
- Optional **Gemini Live "turbo mode"** for those who want lowest latency ([`02 §D`](02-voice-stack-research.md)).
- **Exit:** a real phone app; share any song to a companion.

### Phase 5 — Android power mode + polish (ongoing)
- Android now-playing detection + floating bubble over YT Music; Spotify connect ([`06 §5`](06-cross-platform.md)).
- Voice cloning for *signature* Alif/Tarana voices (ElevenLabs paid, if you want unique IP voices).
- Multi-character "majlis" mode (both companions, ElevenLabs multi-speaker).

> **Realistic solo/duo pace:** a usable Phase 1 in ~2–3 weeks of focused evenings; a genuinely delightful Phase 2 product in ~6–8 weeks total. You and Vedant can parallelise (one on backend/voice, one on web UI/corpus).

---

## 2. The "spend ₹0" free-tier strategy

The core insight: **stack independent free tiers + local fallbacks so no single quota can block you.**

| Component | Free allowance | What it covers | When it runs out → |
|-----------|----------------|----------------|--------------------|
| **Gemini 2.5 Flash** | 1,500 req/day, 1M TPM, no card ([rate limits](https://ai.google.dev/gemini-api/docs/rate-limits)) | The brain, all day | → Groq/OpenRouter → **local Alif-1.0** (unlimited) |
| **Sarvam** | ₹1,000 free credits ([pricing](https://docs.sarvam.ai/api-reference-docs/pricing)) | Best STT for Hinglish | → Groq Whisper (2,000/day) → **local Whisper** (unlimited) |
| **Groq Whisper** | Free, 2,000 req/day ([rate limits](https://console.groq.com/docs/rate-limits)) | Fast STT + YouTube batch | → local Whisper |
| **ElevenLabs** | 10k chars/mo (~10 min) ([pricing](https://elevenlabs.io/pricing)) | *Signature* emotional lines | → **Azure** for bulk; **cache** everything |
| **Azure Speech** | 500k chars/mo ([pricing](https://azure.microsoft.com/en-us/pricing/details/speech/)) | Everyday Urdu voice (50× Eleven's quota) | → cache; throttle; (paid only if huge) |
| **Tavily** | 1,000 searches/mo ([search APIs](https://brave.com/learn/best-search-api-2026/)) | Web search tool | → DuckDuckGo `ddgs` (free) |
| **Supabase** | Free tier (DB + pgvector + storage) | Memory, audio cache, auth | → self-host Postgres |
| **Vercel** | Hobby free | Web hosting | → any static/Node host |
| **Your RTX 4060** | Free forever | STT + LLM locally | the ultimate backstop |

**The three multipliers that make free actually last:**
1. **TTS caching** — identical `(text, voice)` never re-bills. Companion catchphrases, common teaching lines, repeated words = free after first play. This is the single biggest saver for your #1-priority layer.
2. **Two-tier TTS routing** — ElevenLabs only for lines that *need* maximum emotion; Azure (50× the quota) for the rest. A per-utterance check + a monthly quota guard.
3. **Local fallbacks** — when a cloud quota trips, STT and LLM transparently fall to your GPU. You can develop and demo **all day** without spending.

> **Net: the MVP (Phases 0–3) costs ₹0.** The only thing that could force spend is *heavy ElevenLabs use* — and caching + Azure routing neutralise that.

---

## 3. Cost projection *if* it grows (eyes open)

When/if you outgrow free tiers (real users, lots of audio):

| Driver | Free-tier ceiling | First paid step | Approx cost |
|--------|-------------------|-----------------|-------------|
| **TTS (the big one)** | Azure 500k chars/mo (~8–9 hrs speech); Eleven 10 min/mo | ElevenLabs Creator ~$22/mo (~100 min Eleven) or Azure pay-go ~$15–16/1M chars (neural) | scales with spoken minutes — **caching cuts this hard** |
| **LLM** | Gemini 1,500 req/day | Gemini paid tier / Groq paid | cheap (Flash is inexpensive); local = free |
| **STT** | Sarvam credits, Groq 2k/day | Sarvam ~₹30/10k chars; Groq ~$0.04/hr (turbo) | small; local = free |
| **Search** | Tavily 1k/mo | Tavily ~$0.008/req | negligible |
| **Infra** | Supabase/Vercel free | Supabase Pro $25/mo; backend host ~$5–10/mo | low |
| **Realtime S2S (if Phase 4 turbo)** | Gemini Live free tier | OpenAI Realtime $0.18–0.46/min ([cost](https://hackernoon.com/openai-realtime-api-pricing-in-2026-real-world-data-from-4000-measured-sessions)) | **avoid paid S2S** unless monetised |

**Rule of thumb:** for a personal/small-beta product, you can likely stay **under ~$25/month** even past free tiers, *if* caching + Azure-routing are in place. The cost villain is always **uncached premium TTS** — architect against it from day one.

---

## 4. Risk register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| **Urdu TTS quality not "good enough"** | Med | High (it's priority #1) | Phase 0 exists *precisely* to test this early; ElevenLabs v3 is SOTA for expressive Urdu; fall back to Azure's 4 voices; revisit if open Urdu TTS matures |
| **Free tiers shrink/change** (Google already cut some in '25–26) | Med | Med | Multi-provider routers + **local fallbacks** mean no single change blocks you ([Google cut limits](https://www.howtogeek.com/gemini-slashed-free-api-limits-what-to-use-instead/)) |
| **`youtube-transcript-api` breaks** (undocumented internals) | Med | Med | yt-dlp+Whisper fallback; Supadata managed backup ([guide](https://www.notelm.ai/blog/youtube-transcript-api)) |
| **Rekhta content licensing** | Low-Med | Med | Use open datasets + curated corpus, credit Rekhta, email for partnership; avoid live scraping ([FAQ](https://www.rekhta.org/CMS/FAQ)) |
| **Persona drift** (LLM → bland assistant) | Med | High (it's the soul) | Strong system prompts + few-shot + in-character evals ([`01 §8`](01-product-vision.md)) |
| **Latency feels sluggish** | Low-Med | Med (you ranked it last) | Streaming overlap, sentence-level TTS, barge-in; ~1s is acceptable per your priorities ([`03`](03-architecture.md)) |
| **8 GB VRAM ceiling** for local models | Med | Low | int8/4-bit quants; run local STT *or* LLM, not both hot; cloud for the live loop |
| **Poetry mistranslation** (trust killer) | Med | High | Ground in corpus, cite, let Tarana flag ambiguity; never free-hallucinate beloved text |
| **Gemini trains on free-tier prompts** | High (it's policy) | Low-Med (privacy) | Keep sensitive/personal content on **local** model; note in privacy policy |
| **Scope creep** (5 platforms!) | High | Med | Strict phase gates; **don't** start Phase 3+ until Phase 2 is loved |

---

## 5. Definition of done for the MVP

The MVP (end of Phase 2) is "done" when:
- [ ] You can hold a 5-minute spoken conversation with Alif **and** Tarana, in Hinglish-Urdu, and it feels in-character and warm.
- [ ] Replies are accurate, beautifully voiced (Urdu), and shown tri-script with tap-to-hear.
- [ ] It **remembers** you across sessions (a word, a poet, your level).
- [ ] "Samjhao yeh gaana/sher" pulls real content (YouTube/corpus) and teaches it.
- [ ] It runs within free tiers; local fallbacks proven.
- [ ] Latency ~1s; barge-in works; "phir se / dheere" works.
- [ ] At least one moment per session where you *feel* you now own a new Urdu word.

That last bullet is the real metric. Everything else serves it.

---

### Sources for this document
- [Gemini rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) · [Gemini free-tier shrinkage](https://www.howtogeek.com/gemini-slashed-free-api-limits-what-to-use-instead/)
- [Sarvam pricing/credits](https://docs.sarvam.ai/api-reference-docs/pricing) · [Groq rate limits](https://console.groq.com/docs/rate-limits)
- [ElevenLabs pricing](https://elevenlabs.io/pricing) · [Azure Speech pricing](https://azure.microsoft.com/en-us/pricing/details/speech/) · [Tavily/search](https://brave.com/learn/best-search-api-2026/)
- [OpenAI Realtime real-world cost](https://hackernoon.com/openai-realtime-api-pricing-in-2026-real-world-data-from-4000-measured-sessions)
- [youtube-transcript-api reliability](https://www.notelm.ai/blog/youtube-transcript-api) · [Rekhta FAQ](https://www.rekhta.org/CMS/FAQ)
