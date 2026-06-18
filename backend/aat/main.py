"""FastAPI app: health + readiness now; the streamed voice loop lands in T3.

Run: `uv run uvicorn aat.main:app --reload`
"""

from __future__ import annotations

import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from aat import __version__
from aat.config import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aat")

app = FastAPI(title="Alif Aur Tarana API", version=__version__)


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
