# 05 · Tech Stack & Repository Design

The concrete build: languages, frameworks, why each, the repo layout, and the **explicit answer to "why not LangChain."** Aligned to your comfort zone (Python, FastAPI, Next.js) and your global preferences (Python 3.11+, uv, type hints, pytest, no hardcoded secrets).

---

## 1. The stack at a glance

| Layer | Choice | Why |
|-------|--------|-----|
| **Backend language** | **Python 3.11+** (uv, .venv) | Your primary; best voice-AI ecosystem (Pipecat, faster-whisper, all SDKs) |
| **Backend framework** | **FastAPI** | Async, WebSocket-native, Pydantic typing, your comfort zone |
| **Voice orchestration** | **Pipecat** | Pipeline-first voice agent; no LangChain ([`03`](03-architecture.md)) |
| **Agent/tool layer** | **Plain Python + Pydantic** function-calling | Lean, debuggable, no heavy framework |
| **Local inference** | **Ollama** (Alif-1.0 / Gemma) + **faster-whisper** | Free, private, on your RTX 4060 |
| **Memory store** | **mem0** + **Postgres + pgvector** | Persistent + semantic recall |
| **Frontend (web)** | **Next.js (App Router) PWA + TypeScript + Tailwind** | One codebase, installable, your comfort zone |
| **Realtime transport** | **WebSocket** (MVP) → **WebRTC/LiveKit** (scale) | Simple first, robust later |
| **Mobile** | **PWA first** → **Expo / React Native** | Fastest path, then native |
| **Extension** | **WXT** (or plain MV3) + TypeScript | Modern web-extension framework |
| **Auth** | **Clerk** or **Supabase Auth** (free tiers) | Don't build auth from scratch |
| **DB / storage** | **Supabase** (Postgres + pgvector + storage, free tier) | One free backend for DB, vectors, file (audio cache) |
| **Hosting (backend)** | **Fly.io / Render / Railway** free-ish; or your own box | Python WS apps; GPU work stays local |
| **Hosting (web)** | **Vercel** (Next.js) | Note: keep commits clean — no `Co-Authored-By` (your Vercel-Hobby rule) |

---

## 2. Why **not** LangChain (your explicit constraint, honoured)

You asked to avoid LangChain unless absolutely necessary. It is **not** necessary here, and avoiding it is the right call for this project:

- **Weight vs. need.** A voice companion's "agent" is a tight loop: *transcript → (maybe tool calls) → response*. Modern LLM SDKs (Gemini, OpenAI, Groq) have **native function-calling**; you describe tools as JSON schemas and the model returns structured calls. LangChain adds layers (chains, agents, callbacks, abstractions) over what is, honestly, ~150 lines of your own code.
- **Latency & control.** In a *voice* pipeline every millisecond and every token of streaming control matters ([`03`](03-architecture.md)). Pipecat already owns the streaming pipeline; bolting LangChain on top fights it.
- **Debuggability.** When Alif says something off, you want a flat, readable call stack — not to trace through framework indirection.
- **Dependency risk.** LangChain's surface area and churn is large; for a long-lived personal project, fewer moving parts wins.

**What we use instead (the "lean agent"):**
```python
# Pseudocode — the entire "agent" is this small.
tools = [rekhta_lookup, youtube_transcript, web_search, memory_recall, memory_write]
schemas = [to_json_schema(t) for t in tools]          # native function-calling schemas

async def agent_turn(user_text, persona, ctx):
    msgs = build_messages(persona, ctx, user_text)     # system prompt + memory + history
    while True:
        resp = await llm.stream(msgs, tools=schemas)   # Gemini/Groq/local via a thin router
        if resp.tool_calls:
            results = await run_tools(resp.tool_calls)  # plain async dispatch
            msgs += tool_messages(results)
            continue
        async for sentence in resp.sentences():         # stream to TTS as sentences complete
            yield sentence
        break
```
That's the whole orchestration philosophy: **the LLM SDK's function-calling + a dictionary of Python functions.** No LangChain, no LangGraph. (If we ever need durable, branching multi-step workflows, revisit with something minimal like **PydanticAI** — typed, light — before ever reaching for LangChain.)

---

## 3. The model router (also tiny, also no framework)

A ~50-line module that picks STT/LLM/TTS providers by policy (quota, capability, latency) and fails over gracefully ([`02 §F`](02-voice-stack-research.md), [`03 §6.5`](03-architecture.md)):
```python
class LLMRouter:
    # order: gemini_flash -> groq -> openrouter -> local(alif)
    async def complete(self, msgs, *, need="general"):
        for provider in self.policy(need):     # e.g. "urdu_phrasing" prefers local Alif
            try: return await provider.stream(msgs)
            except (RateLimit, Down): continue
        raise AllProvidersExhausted
```
Same pattern for `TTSRouter` (ElevenLabs↔Azure by "needs emotion?" + quota) and `STTRouter` (Sarvam↔Groq↔local).

---

## 4. Repository layout (monorepo)

```
alif-aur-tarana/
├─ apps/
│  ├─ api/                      # FastAPI + Pipecat backend
│  │  ├─ main.py                # app, WS endpoints
│  │  ├─ pipeline/              # Pipecat pipeline assembly (VAD, STT, LLM, TTS)
│  │  ├─ agent/
│  │  │  ├─ personas/           # alif.py, tarana.py (system prompts + few-shot)
│  │  │  ├─ router_llm.py  router_tts.py  router_stt.py
│  │  │  └─ tools/              # rekhta.py youtube.py web.py memory.py
│  │  ├─ content/               # poetry corpus loader (datasets + curated)
│  │  ├─ memory/                # mem0 wiring + pgvector
│  │  ├─ schemas.py             # Pydantic models (WS events, tool I/O)
│  │  └─ tests/                 # pytest (RED→GREEN→REFACTOR)
│  ├─ web/                      # Next.js PWA (companion UI, tri-script, mic)
│  └─ extension/                # WXT MV3 YouTube extension (Phase 3)
├─ packages/
│  ├─ shared-types/             # TS types mirrored from Pydantic (event protocol)
│  └─ tri-script/               # transliteration helpers (shared)
├─ data/
│  └─ corpus/                   # curated ghazals/songs (tri-script + metadata)
├─ infra/                       # docker-compose (pg+pgvector), env templates
├─ pyproject.toml               # uv-managed
└─ docs/                        # ← these documents
```

Mobile (Expo) is added as `apps/mobile/` in Phase 4, reusing `packages/shared-types`.

---

## 5. Local-on-your-4060 dev setup (free, private)

Your hardware (i7-13HX, 16 GB RAM, RTX 4060 8 GB) is enough to run the whole loop *except* expressive Urdu TTS:

| Component | Local tool | Footprint | Status |
|-----------|-----------|-----------|--------|
| STT | faster-whisper large-v3 int8 | ~2.5 GB VRAM, ~7× RT | ✅ runs great |
| LLM | Alif-1.0-8B (4-bit) or Gemma-3 via Ollama | ~5–6 GB VRAM | ✅ runs (mind the 8 GB ceiling — don't run STT+LLM at full size simultaneously; 16 GB system RAM is the tighter constraint for batching) |
| TTS | — | — | ❌ no production Urdu TTS locally → use Azure/ElevenLabs (cloud) even in dev |
| Memory/DB | Postgres + pgvector (Docker) | small | ✅ |

> Practical note: with 8 GB VRAM, prefer **either** local STT **or** local LLM hot at a time, or use the int8/4-bit quants noted; for the live loop during dev, run **local Whisper + Gemini Flash (cloud)** to keep VRAM free, and reserve local Alif-1.0 for offline/eval runs.

---

## 6. Secrets, config, quality (your global rules, applied)

- **Secrets:** `.env` + `os.environ` only; never hardcoded. Keys: `GEMINI_API_KEY`, `SARVAM_API_KEY`, `ELEVENLABS_API_KEY`, `AZURE_SPEECH_KEY`/`REGION`, `TAVILY_API_KEY`, `GROQ_API_KEY`, DB URL. Provide `.env.example`.
- **Types:** annotations on all public signatures; Pydantic for all I/O boundaries (WS events, tool args).
- **Logging:** `logging` module, never `print()`.
- **Errors:** specific exceptions (`RateLimitError`, `ProviderDownError`), never bare `except`.
- **Tests:** pytest, TDD on the router/tool/agent logic; fixtures + parametrize for provider mocks; target 80%+ on core.
- **Style:** PEP 8, functions ≤50 lines, files ≤800 lines, pathlib, EAFP, context managers for audio/streams.
- **Commits:** conventional commits; **no `Co-Authored-By` trailer** (your Vercel-Hobby deploy rule).

---

## 7. Build/runtime cost of the stack itself

Everything here is **open-source or free-tier**:
- Pipecat, faster-whisper, Ollama, mem0, FastAPI, Next.js, WXT, pgvector — all free/OSS.
- Supabase, Vercel, Tavily, Gemini, Sarvam, Azure, Groq, ElevenLabs — all have free tiers we live within ([`07`](07-execution-roadmap.md)).
- Paid only if we *choose* scale: backend host upgrade, ElevenLabs/Azure overages, Supabase Pro.

Next: how this runs everywhere → [`06-cross-platform.md`](06-cross-platform.md).

---

### Sources for this document
- [Pipecat vs LiveKit](https://www.f22labs.com/blogs/difference-between-livekit-vs-pipecat-voice-ai-platforms/) (orchestration choice)
- [mem0 (open-source memory)](https://vectorize.io/articles/mem0-vs-letta)
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) · [Alif-1.0-8B (Ollama/GGUF)](https://huggingface.co/large-traversaal/Alif-1.0-8B-Instruct)
- [Gemini function-calling/pricing](https://ai.google.dev/gemini-api/docs/pricing) (native tool-calling → no LangChain needed)
