"""FastAPI app: health, readiness, a text `/turn` endpoint, and a minimal web UI.

Run: `uv run uvicorn aat.main:app --reload`
  - API:  POST /turn  {companion, text} -> {turn, audio_b64}
  - UI:   http://localhost:8000/ui/
The streamed mic loop (Pipecat) lands in T3; this text turn makes it usable now.
"""

from __future__ import annotations

import base64
import logging
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from aat import __version__
from aat.agent import respond
from aat.config import get_settings
from aat.personas import get_persona
from aat.schemas import Companion
from aat.tts import AudioCache, build_tts_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aat")

app = FastAPI(title="Alif Aur Tarana API", version=__version__)

_STATIC = Path(__file__).resolve().parent.parent / "static"


class TurnRequest(BaseModel):
    """A single text turn from the client."""

    companion: Companion = Companion.TARANA
    text: str


@app.get("/healthz")
def healthz() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok", "version": __version__}


@app.get("/readiness")
def readiness() -> dict[str, bool]:
    """Which services are configured (keys present)."""
    s = get_settings()
    return {
        "gemini": bool(s.gemini_api_key),
        "elevenlabs": bool(s.elevenlabs_api_key),
        "sarvam": bool(s.sarvam_api_key),
        "groq": bool(s.groq_api_key),
        "tavily": bool(s.tavily_api_key),
        "alif_voice": bool(s.alif_voice_id),
        "tarana_voice": bool(s.tarana_voice_id),
    }


@app.post("/turn")
async def turn(req: TurnRequest) -> dict:
    """Produce one in-character companion turn + its voiced audio (base64 mp3)."""
    s = get_settings()
    companion_turn = await respond(req.companion, req.text, s)
    persona = get_persona(req.companion)
    audio_b64 = ""
    voice_id = persona.voice_id(s)
    if voice_id:
        tts = build_tts_router(s, AudioCache(str(_STATIC.parent / "audio_cache")))
        audio = await tts.synthesize(
            companion_turn.speech,
            voice_id=voice_id,
            stability=persona.stability,
            language_code="ur",
            seed=persona.seed(s),
        )
        audio_b64 = base64.b64encode(audio).decode("ascii")
    return {"turn": companion_turn.model_dump(), "audio_b64": audio_b64}


@app.websocket("/ws")
async def ws(socket: WebSocket) -> None:
    """Placeholder echo socket. The full STT->LLM->TTS stream arrives in T3 (docs/03)."""
    await socket.accept()
    try:
        while True:
            msg = await socket.receive_text()
            await socket.send_json({"type": "echo", "data": {"received": msg}})
    except WebSocketDisconnect:
        logger.info("client disconnected")


# Minimal web UI at /ui/ (text chat + audio playback). Mounted last so API routes win.
if _STATIC.exists():
    app.mount("/ui", StaticFiles(directory=str(_STATIC), html=True), name="ui")
