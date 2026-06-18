# Alif Aur Tarana

A voice-first companion app to **learn Urdu through the content and feelings you already love** — with two AI companions, **Alif** (the hopeless romantic) and **Tarana** (the elegant rationalist).

> 📚 **All research, design, and the build plan live in [`docs/`](docs/).** Start at [`docs/README.md`](docs/README.md).
> 🛠️ **Setup / API keys:** [`docs/12-setup-and-api-keys.md`](docs/12-setup-and-api-keys.md) · **Build plan:** [`docs/13-mvp-build-plan.md`](docs/13-mvp-build-plan.md)

---

## Repo layout

```
alif-aur-tarana/
├─ apps/
│  ├─ api/        # FastAPI + Pipecat backend (the brain + voice loop)
│  └─ web/        # Next.js client (added in T4)
├─ docs/          # research, design, plan
└─ data/          # local poetry corpus (seed)
```

## Quick start (backend)

> Prereqs: Python 3.11+, [uv](https://docs.astral.sh/uv/), ffmpeg. See `docs/12`.

```bash
cd apps/api
uv sync                      # install dependencies
cp .env.example .env         # then fill in your keys (docs/12)
uv run python check_keys.py  # verify which services are ready
uv run uvicorn aat.main:app --reload   # start the API (health at /healthz)
```

The MVP is built **locally** (no deployment) to prove the voice loop works end-to-end. See the build sequence T0→T6 in `docs/13`.

## Status

Pre-MVP. T0 (bootstrap) scaffolding in progress; voice loop (T1–T3) begins once API keys are in `apps/api/.env`.
