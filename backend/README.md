# Alif Aur Tarana — Backend (FastAPI)

The brain + voice loop: a cascade pipeline **STT → LLM → TTS** that gives the companions
Alif and Tarana an expressive Urdu voice. Deploys independently of `../frontend`.

See the design in [`../docs`](../docs) (architecture: `03`, prompts: `09`, build plan: `13`).

## Setup

```bash
# from this folder (backend/)
uv venv                       # create .venv
uv sync                       # install dependencies + lockfile
cp .env.example .env          # then fill keys (docs/12). .env is gitignored.
uv run python check_keys.py   # verify which services are reachable
uv run uvicorn aat.main:app --reload   # API at http://localhost:8000 (health: /healthz)
```

### Optional dependency groups (installed when we reach those steps)
- `uv sync --extra stt-local` — local faster-whisper STT (T2 fallback, runs on the RTX 4060)
- `uv sync --extra voice` — Pipecat voice pipeline (T3)
- `uv sync --extra tools` — YouTube transcript / search tools (T5)
- `uv sync --extra dev` — pytest + ruff

## Layout
```
backend/
├─ aat/
│  ├─ config.py        # env settings
│  ├─ schemas.py       # output contract + WS events
│  ├─ personas/        # Alif & Tarana system prompts (docs/09)
│  ├─ llm/             # Gemini + router (fallback ladder)
│  ├─ tts/             # ElevenLabs + cache + router
│  ├─ stt/             # Sarvam + local Whisper + router
│  ├─ tools/           # rekhta corpus, web search, memory
│  ├─ memory/          # SQLite store
│  └─ main.py          # FastAPI app (added in T0 finish)
├─ check_keys.py
└─ pyproject.toml
```
