# 12 · Setup & API Keys — Do This Once, Up Front

Everything to sign up for **before** we start coding, so we never stop mid-build to chase a key. Work top-down: **Tier 1** unblocks the first run; **Tier 2** you'll want within days; **Tier 3** is local installs (no signup); **Tier 4** is later phases.

> 🔑 **Where keys go:** every key lands in a single `apps/api/.env` file (never hardcoded — your global rule). A ready-to-fill template is at the bottom (§6). 💳 = needs a card even for the free tier.

---

## Tier 1 — Required for the first local run

### 1. Google Gemini (the brain) — `GEMINI_API_KEY`
- **For:** the LLM that powers Alif/Tarana + tool-calling. Free: 1,500 req/day, no card.
- **Get it:**
  1. Go to **https://aistudio.google.com/** → sign in with Google.
  2. Click **"Get API key"** (left nav) → **Create API key** → copy it.
- **Card?** No. **Note:** free-tier prompts may be used by Google for training — keep anything private on the local model.

### 2. ElevenLabs (the voice) — `ELEVENLABS_API_KEY`
- **For:** Urdu TTS — Tarana's chosen voice + **Alif via Voice Design**. Free: ~10k chars/mo.
- **Get it:**
  1. Sign up at **https://elevenlabs.io/** (free).
  2. Profile (bottom-left avatar) → **"API Keys"** (or Settings → API Keys) → **Create** → copy.
  3. **Create Alif's voice now:** Voices → **My Voices → Add a new voice → Voice Design** → paste the Alif prompt from [`11 §3`](11-voice-identity-and-cloning.md) → generate → pick → **copy its `voice_id`**.
  4. **Lock Tarana's voice:** open the voice you chose → copy its `voice_id`.
  - Put both in `.env`: `ALIF_VOICE_ID`, `TARANA_VOICE_ID`.
- **Card?** No (free tier). **Note:** free tier = no commercial rights + attribution; fine for MVP/testing.

### 3. Sarvam AI (speech-to-text) — `SARVAM_API_KEY`
- **For:** best Hinglish/Urdu code-mixed transcription (Saaras v3). Free: ₹1,000 credits, no card.
- **Get it:**
  1. Go to **https://dashboard.sarvam.ai/** → sign up.
  2. **API Keys** section → **Create / copy** your key.
- **Card?** No.

> ✅ With Tier 1 + Tier 3 installed, the full cascade (mic → STT → Alif/Tarana → voice) runs locally.

---

## Tier 2 — Get now to avoid back-and-forth

### 4. Groq (fast STT + LLM fallback) — `GROQ_API_KEY`
- **For:** ultra-fast Whisper STT (free 2,000/day) and a fast LLM fallback.
- **Get it:** **https://console.groq.com/** → sign in → **API Keys** → **Create API Key** → copy.
- **Card?** No.

### 5. Azure Speech (bulk Urdu TTS + 4 Urdu voices) — `AZURE_SPEECH_KEY` + `AZURE_SPEECH_REGION`
> **DEFERRED by your decision (18 Jun 2026)** — not needed for the first run; the MVP's TTS uses ElevenLabs' free tier. Set this up *before* real/volume usage.
- **For:** the "volume" Urdu voice (500k chars/mo free, ur-PK/ur-IN voices), and future pronunciation SSML.
- **Get it:**
  1. Create a free Azure account at **https://azure.microsoft.com/free/**.
  2. In the **Azure Portal** → **Create a resource** → search **"Speech"** → **Create** → choose **Free F0** pricing tier, pick a region (e.g., `centralindia` or `eastus`).
  3. Open the resource → **Keys and Endpoint** → copy **KEY 1** and the **Region**.
- **Card?** 💳 **Yes** — Azure requires a card to verify identity even for the free account (F0 won't charge you). *If you'd rather not add a card yet, skip Azure for the very first run — ElevenLabs free covers initial testing — and add it before real usage.*

### 6. Tavily (web search tool) — `TAVILY_API_KEY`
- **For:** the companions' web-search tool (poet facts, song trivia). Free: 1,000 searches/mo.
- **Get it:** **https://app.tavily.com/** → sign up → copy the API key from the dashboard.
- **Card?** No.

---

## Tier 3 — Local installs (no signup, no keys)

These run on your machine (great on your RTX 4060). Install once:

| Tool | For | Install |
|------|-----|---------|
| **Python 3.11+ & uv** | backend runtime | `winget install astral-sh.uv` (or pipx) |
| **Ollama** | local LLM fallback (Alif-1.0 / Gemma) | Download **https://ollama.com/** → then `ollama pull` the model |
| **faster-whisper** | local STT (free, unlimited) | `uv pip install faster-whisper` (downloads model on first run) |
| **ffmpeg** | audio decode for Whisper/yt-dlp | `winget install Gyan.FFmpeg` |
| **Docker Desktop** *(optional)* | Postgres+pgvector for memory | **https://www.docker.com/products/docker-desktop/** |
| **Node.js 20+** | the Next.js web client | **https://nodejs.org/** |

Python libs (installed during build, no signup): `pipecat-ai`, `fastapi`, `uvicorn`, `google-genai`, `elevenlabs`, `sarvam` SDK/`httpx`, `groq`, `youtube-transcript-api`, `yt-dlp`, `ddgs`, `mem0ai`, `pydantic`.

> **Local Alif-1.0 (optional but on-brand):** `ollama pull` the Urdu-specialised model when ready (see [`02 §B`](02-voice-stack-research.md) / [Alif-1.0 GGUF](https://huggingface.co/large-traversaal/Alif-1.0-8B-Instruct)). Not required for the first run — Gemini covers the brain.

---

## Tier 4 — Later phases (don't bother yet)

| Service | For | When |
|---------|-----|------|
| **Supabase** (supabase.com, free, GitHub login, no card) | hosted Postgres + pgvector + auth + audio storage | Phase 2 (persistent memory) — local SQLite/Docker Postgres is fine for MVP |
| **OpenRouter** (openrouter.ai, free models) | extra LLM fallback | optional |
| **YouTube Data API** (Google Cloud Console, free quota) | *searching* videos | when building the YouTube tool (transcripts need no key via `youtube-transcript-api`) |
| **Vercel** (vercel.com, free) | web hosting | when you deploy (not for local MVP) — remember: no `Co-Authored-By` in commits |
| **Supadata** (supadata.ai, 100/mo free) | managed YouTube-transcript fallback | if `youtube-transcript-api` proves flaky |

---

## §6 — `.env` template (drop into `apps/api/.env`)

```dotenv
# ---- Tier 1: required ----
GEMINI_API_KEY=
ELEVENLABS_API_KEY=
ALIF_VOICE_ID=        # from ElevenLabs Voice Design
TARANA_VOICE_ID=      # your chosen ElevenLabs voice
SARVAM_API_KEY=

# ---- Tier 2: recommended now ----
GROQ_API_KEY=
AZURE_SPEECH_KEY=
AZURE_SPEECH_REGION=  # e.g. centralindia
TAVILY_API_KEY=

# ---- Tier 4: later ----
# SUPABASE_URL=
# SUPABASE_KEY=
# OPENROUTER_API_KEY=
# YOUTUBE_API_KEY=

# ---- local services (no keys) ----
OLLAMA_BASE_URL=http://localhost:11434
WHISPER_MODEL=large-v3        # or 'medium' to save VRAM
```

---

## §7 — Checklist (tick before we code)

**Cloud keys**
- [ ] `GEMINI_API_KEY` (aistudio.google.com)
- [ ] `ELEVENLABS_API_KEY` + Alif Voice Design `voice_id` + Tarana `voice_id`
- [ ] `SARVAM_API_KEY` (dashboard.sarvam.ai)
- [ ] `GROQ_API_KEY` (console.groq.com)
- [x] ~~`AZURE_SPEECH_KEY` + `AZURE_SPEECH_REGION`~~ — **deferred by decision** (add before real usage)
- [ ] `TAVILY_API_KEY` (app.tavily.com)

**Local installs**
- [ ] Python 3.11+ & uv · [ ] Node.js 20+ · [ ] ffmpeg
- [ ] Ollama (+ a model pulled) · [ ] faster-whisper (auto on first run)
- [ ] Docker Desktop *(optional, for Postgres)*

**Decisions**
- [x] Alif voice path = **Voice Design** (reference voices are public figures → cloning not allowed)
- [x] Azure = **deferred** until before real usage

> Once the cloud keys + local installs are ticked, we go straight to [`13-mvp-build-plan.md`](13-mvp-build-plan.md) and start building.
