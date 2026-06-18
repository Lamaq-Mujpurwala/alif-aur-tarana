# 08 · Master Decision Matrix

Every option for every component in one place, with **advantages, disadvantages, free/paid, and a verdict.** This is the "set of all options" reference. Evidence and sourcing live in [`02`](02-voice-stack-research.md)–[`05`](05-tech-stack.md); this is the at-a-glance decision sheet.

**Legend:** 🟢 chosen for MVP · 🟡 fallback / later · 🔴 rejected · 💰 paid · 🆓 free tier exists

---

## 1. Text-to-Speech (the Urdu voice) — *the decisive layer*

| Option | Urdu | Free/Paid | Advantages | Disadvantages | Verdict |
|--------|------|-----------|------------|---------------|---------|
| **ElevenLabs v3** | ✅ | 🆓 10k chars/mo, then 💰 | Best-in-class emotion (audio tags `[laughs]/[sighs]/[whispers]`), multi-character, voice cloning, streaming | Tiny free quota (~10 min), no commercial use on free, attribution required, 2.5k chars/req | 🟢 **Signature/demo voice** |
| **Azure Speech** | ✅ 4 voices | 🆓 500k chars/mo, then 💰 | Huge free quota (50× Eleven), ur-PK + ur-IN accents, SSML styles/pauses, reliable | Less "magical" emotion than Eleven; SSML is fiddlier than tags | 🟢 **Bulk/everyday voice** |
| **Gemini native audio** | ✅ | 🆓 | Emotion-aware, reacts to your emotion, ~realtime, single API | Auto-language (can't pin accent), shared voices, less per-line control | 🟡 **Phase-4 live mode** |
| **OpenAI TTS/Realtime** | ✅ | 💰 only | Very natural, steerable | **No free tier**; per-minute cost adds up | 🔴 for MVP (paid) |
| **Cartesia Sonic** | ⚠️ Hindi | 🆓 small | Fastest (~40 ms), laughter/emotion | **Urdu unconfirmed** | 🔴 (no confirmed Urdu) |
| **Sarvam Bulbul** | ❌ | 🆓 | Great for Indic | **No Urdu** | 🔴 |
| **Google Cloud TTS** | ❌ | 🆓 1M chars | Cheap, many voices | **No Urdu** | 🔴 |
| **NVIDIA Magpie** | ❌ | 🆓 | Free hosted, voice cloning | **No Urdu** (7 langs) | 🔴 (answers your "Nvidia?") |
| **Deepgram Aura** | ❌ | 🆓 $200 | Fast | **No Urdu** | 🔴 |

---

## 2. Speech-to-Text (transcription)

| Option | Urdu | Hinglish code-mix | Free/Paid | Advantages | Disadvantages | Verdict |
|--------|------|-------------------|-----------|------------|---------------|---------|
| **Sarvam Saaras v3** | ✅ | ✅ built for it | 🆓 ₹1,000 credits | Best Indian-speech accuracy, diarization, timestamps, beats GPT-4o/Gemini/Deepgram on Indic | Credits finite; India-focused | 🟢 **Production STT** |
| **faster-whisper (local)** | ✅ | ⚠️ ok | 🆓 forever (your GPU) | Unlimited, private, ~7× RT on 4060, no quota | You run it; ~2.5 GB VRAM | 🟢 **Dev + fallback** |
| **Groq Whisper v3/turbo** | ✅ | ⚠️ ok | 🆓 2,000/day | 164× realtime (fastest hosted), free | Generic Whisper (less Indic-tuned) | 🟡 **Hot-swap fallback** |
| **ElevenLabs Scribe** | ✅ | ⚠️ | 🆓 (shared credits) | Convenient if on Eleven | Eats Eleven credits | 🟡 |
| **Deepgram Nova** | ⚠️ | ⚠️ | 🆓 $200 | Very fast | Weaker Indic | 🔴 (Sarvam better) |
| **AssemblyAI** | ⚠️ | ⚠️ | 🆓 small | Good English features | Weaker Urdu | 🔴 |

---

## 3. The LLM (the brain)

| Option | Urdu/Hindi | Tool-calling | Free/Paid | Local on 4060? | Advantages | Disadvantages | Verdict |
|--------|-----------|--------------|-----------|----------------|------------|---------------|---------|
| **Gemini 2.5 Flash** | ✅ | ✅ | 🆓 1,500/day | n/a | Best free quota + quality + tools | May train on prompts; limits fluctuate | 🟢 **Primary** |
| **Alif-1.0-8B** (local) | ✅ Urdu-specialist | ⚠️ prompt | 🆓 open weights | ✅ 4-bit | Private, unlimited, Urdu-tuned, *namesake* | 8B reasoning < Flash; you host | 🟢 **Local specialist/fallback** |
| **Gemini 2.5 Pro** | ✅ strongest | ✅ | 🆓 ~50/day | n/a | Best quality for hard poetry | Tiny free quota | 🟡 sparingly |
| **Groq (Llama/Qwen)** | ✅ | ✅ | 🆓 fast | n/a | Very fast cloud | Quotas | 🟡 fallback |
| **OpenRouter free models** | ✅ varies | ✅ | 🆓 rotating | n/a | Many models, one key | Availability varies | 🟡 fallback |
| **Sarvam-M (24B)** | ✅ Indic | ✅ | 🆓 credits | ❌ too big | Strong Indic API | Too big to self-host on 8 GB | 🟡 API option |
| **Gemma 3 (local)** | ✅ ok | ⚠️ | 🆓 | ✅ small | Generic local | Not Urdu-specialised | 🟡 |
| **OpenAI GPT** | ✅ | ✅ | 💰 | n/a | Strong | Paid; no need | 🔴 (paid, unneeded) |

---

## 4. Architecture pattern

| Option | Free/Paid | Advantages | Disadvantages | Verdict |
|--------|-----------|------------|---------------|---------|
| **Cascade (STT→LLM→TTS)** | 🆓 | Full control of voice/persona/cost, swappable, matches your priorities | ~1s latency (vs ~400ms) | 🟢 **MVP** |
| **Native S2S (Gemini Live)** | 🆓 | Lowest latency, natural interruptions | Less voice/accent/persona control; optimises your *lowest* priority | 🟡 **Phase-4 turbo** |
| **Managed S2S (ElevenLabs Agents)** | 🆓 ~15 min/mo, 💰 | Best voice, turn-taking, all-in-one | Free minutes tiny; paid scales fast | 🟡 evaluate later |
| **Managed S2S (OpenAI Realtime)** | 💰 | Very natural | No free tier | 🔴 MVP |

---

## 5. Voice orchestration framework

| Option | Free/Paid | Advantages | Disadvantages | Verdict |
|--------|-----------|------------|---------------|---------|
| **Pipecat** | 🆓 OSS | Pipeline-first, best 1:1 DX, runs on localhost, Sarvam/Eleven plugins, no LangChain | You manage transport at scale | 🟢 **Chosen** |
| **LiveKit Agents** | 🆓 OSS (+cloud 💰) | Production WebRTC transport, multi-participant, best turn detector | Heavier (Docker/server), overkill for 1:1 | 🟡 **Transport at scale / majlis mode** |
| **Vapi / Retell** (managed) | 💰 | Fastest to ship, hosted | Paid, less control, vendor lock | 🔴 (control + cost) |
| **LangChain / LangGraph** | 🆓 OSS | Big ecosystem | **Heavy, latency, indirection** — you asked to avoid | 🔴 **Explicitly avoided** |
| **Roll-your-own (no framework)** | 🆓 | Max control | Reinvent streaming/VAD plumbing | 🟡 (Pipecat saves this) |

---

## 6. Conversation memory

| Option | Free/Paid | Advantages | Disadvantages | Verdict |
|--------|-----------|------------|---------------|---------|
| **mem0** | 🆓 OSS self-host | Drop-in memory layer, Python+JS, semantic recall, 48k★ | Pro features (graph) gated | 🟢 **Chosen** |
| **Postgres + pgvector** | 🆓 | Zero new framework, full control | You write the recall logic | 🟢 **Barebones alt / backing store** |
| **Letta (MemGPT)** | 🆓 self-host | Tiered self-editing memory | Wants to *be* the runtime — too much | 🟡 |
| **Zep** | 🆓/💰 | Best benchmark recall, temporal graph | More infra | 🟡 at scale |

---

## 7. Tools

| Need | Option | Free/Paid | Advantages | Disadvantages | Verdict |
|------|--------|-----------|------------|---------------|---------|
| **Poetry (Rekhta)** | Local corpus (open datasets + curated) | 🆓 | Fast, offline, controlled, legal-cleaner | Snapshot; manual curation | 🟢 |
| | Live scrape rekhta.org | 🆓 | Complete, live | Fragile, ToS/ethics, no API exists | 🔴 MVP |
| | Email Rekhta for partnership | 🆓 | Official blessing possible | Uncertain/slow | 🟡 pursue |
| **YouTube** | `youtube-transcript-api` | 🆓 | No key, simple | Fragile internals | 🟢 |
| | yt-dlp + Whisper | 🆓 | Works when no captions | Slower | 🟢 fallback |
| | Supadata | 🆓 100/mo | AI fallback, reliable | Quota/key | 🟡 backup |
| **Web search** | Tavily | 🆓 1,000/mo | LLM-optimised, cited | Quota | 🟢 |
| | Brave Search API | 💰 ($5 credit/mo) | Best agent score/latency | No real free tier now | 🟡 |
| | DuckDuckGo (`ddgs`) | 🆓 | Zero cost | Less reliable | 🟡 fallback |

---

## 8. Platform / client

| Surface | Option | Free/Paid | Advantages | Disadvantages | Verdict |
|---------|--------|-----------|------------|---------------|---------|
| **Web** | Next.js PWA | 🆓 | One codebase, installable, fast to ship | iOS PWA mic/bg limits | 🟢 **Phase 1** |
| **Mobile** | Expo / React Native | 🆓 | Native bg audio, share-sheet, store presence | More work | 🟡 **Phase 4** |
| | Capacitor wrap of PWA | 🆓 | Reuse PWA for stores | Less native feel | 🟡 alt |
| **Extension** | WXT (MV3) | 🆓 | Modern DX, YouTube learn-while-watch | Desktop only; MV3 quirks | 🟢 **Phase 3** |
| **YT Music (phone)** | Share-sheet | 🆓 | Reliable, cross-OS, simple | Manual per-song; needs native app | 🟢 **Phase 4** |
| | Android now-playing + bubble | 🆓 | "Magic" auto-context | Android-only, sensitive perms | 🟡 **Phase 5 power mode** |
| | Spotify Web API connect | 🆓 | Auto now-playing (easier than YT Music) | Spotify-only | 🟡 nice add |

---

## 9. The one-line recommendation per layer

| Layer | Build with |
|-------|-----------|
| **Voice (TTS)** | **ElevenLabs v3** (feel) + **Azure** (volume) + caching |
| **STT** | **Sarvam Saaras v3** + **local Whisper** fallback |
| **Brain (LLM)** | **Gemini 2.5 Flash** + **local Alif-1.0** fallback |
| **Architecture** | **Cascade**, streamed; Gemini Live later for turbo |
| **Orchestration** | **Pipecat** (no LangChain) |
| **Memory** | **mem0** over Postgres/pgvector |
| **Tools** | Local Rekhta corpus · youtube-transcript-api · Tavily |
| **Frontend** | **Next.js PWA** → Expo → YouTube extension |
| **Cost** | **₹0 MVP** via free tiers + local fallbacks + TTS caching |

> Full reasoning and sources: [`02-voice-stack-research.md`](02-voice-stack-research.md). Architecture: [`03-architecture.md`](03-architecture.md). Plan: [`07-execution-roadmap.md`](07-execution-roadmap.md).
