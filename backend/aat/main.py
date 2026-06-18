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

from aat import __version__, cues
from aat.agent import respond
from aat.audio import to_wav
from aat.config import get_settings
from aat.memory import MemoryStore
from aat.personas import get_persona
from aat.pron import assess as assess_pronunciation
from aat.schemas import Companion
from aat.stt import build_stt_router
from aat.tts import AudioCache, build_tts_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aat")

app = FastAPI(title="Alif Aur Tarana API", version=__version__)

_STATIC = Path(__file__).resolve().parent.parent / "static"
_MEMORY = MemoryStore(str(_STATIC.parent / "aat.db"))


class TurnRequest(BaseModel):
    """A single text turn from the client."""

    companion: Companion = Companion.TARANA
    text: str


class AudioTurnRequest(BaseModel):
    """A spoken turn: base64-encoded audio from the client's mic."""

    companion: Companion = Companion.TARANA
    audio_b64: str
    language: str = "hi"  # the user speaks Hindi/Hinglish; STT transcribes that


class PronounceRequest(BaseModel):
    """A pronunciation attempt: the target Urdu word + the learner's recorded audio."""

    target_word: str  # ideally the Urdu-script word the learner is attempting
    audio_b64: str
    companion: Companion = Companion.TARANA
    language: str = "ur"


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
    companion_turn = await respond(req.companion, req.text, s, memory=_MEMORY)
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


@app.post("/turn-audio")
async def turn_audio(req: AudioTurnRequest) -> dict:
    """Voice turn: client mic audio -> STT (Sarvam/Whisper) -> companion -> voiced reply."""
    s = get_settings()
    wav = await to_wav(base64.b64decode(req.audio_b64))
    transcript = await build_stt_router(s).transcribe(wav, language=req.language)
    companion_turn = await respond(req.companion, transcript, s, memory=_MEMORY)
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
    return {"transcript": transcript, "turn": companion_turn.model_dump(), "audio_b64": audio_b64}


@app.post("/pronounce")
async def pronounce(req: PronounceRequest) -> dict:
    """Assess the learner's pronunciation of a word + return a correct spoken reference."""
    s = get_settings()
    wav = await to_wav(base64.b64decode(req.audio_b64))
    check = await assess_pronunciation(wav, req.target_word, s, language=req.language)
    persona = get_persona(req.companion)
    reference_audio_b64 = ""
    voice_id = persona.voice_id(s)
    if voice_id:
        tts = build_tts_router(s, AudioCache(str(_STATIC.parent / "audio_cache")))
        audio = await tts.synthesize(
            req.target_word,
            voice_id=voice_id,
            stability=persona.stability,
            language_code="ur",
            seed=persona.seed(s),
        )
        reference_audio_b64 = base64.b64encode(audio).decode("ascii")
    return {"check": check.model_dump(), "reference_audio_b64": reference_audio_b64}


def _b64(audio: bytes) -> str:
    return base64.b64encode(audio).decode("ascii") if audio else ""


# Queries that likely need a lookup get a "searching" filler; others get "thinking".
_SEARCH_HINTS = {
    "sher", "shayari", "shaayari", "gaana", "gana", "song", "kaun", "kab", "kahan",
    "kahaan", "youtube", "dhoond", "dhundo", "khoj", "search", "poet", "shayar", "news",
}


def _filler_category(text: str) -> str:
    low = text.lower()
    return "searching" if any(h in low for h in _SEARCH_HINTS) else "thinking"


async def _try_cue(category: str, companion: Companion, settings, tts) -> tuple[str, str]:
    """Serve a cached cue; best-effort (returns empty on any failure)."""
    try:
        audio, text = await cues.serve(category, companion, settings, tts)
        return _b64(audio), text
    except Exception as exc:  # noqa: BLE001 - cues are optional flourish
        logger.info("cue '%s' unavailable: %s", category, exc)
        return "", ""


@app.websocket("/converse")
async def converse(socket: WebSocket) -> None:
    """Streaming loop with instant cues (docs/03): summon -> wake-ack; else filler -> reply."""
    await socket.accept()
    s = get_settings()
    tts = build_tts_router(s, AudioCache(str(_STATIC.parent / "audio_cache")))
    stt = build_stt_router(s)
    try:
        while True:
            msg = await socket.receive_json()
            companion = Companion(msg.get("companion", "tarana"))

            # 1. Resolve the user's turn to text (transcribe audio if needed).
            if msg.get("type") == "audio":
                wav = await to_wav(base64.b64decode(msg["audio_b64"]))
                transcript = (await stt.transcribe(wav, language=msg.get("language", "hi"))).strip()
                await socket.send_json({"type": "transcript", "text": transcript})
            else:
                transcript = (msg.get("text") or "").strip()
            if not transcript:
                continue

            # 2. Bare summon ("Alif", "suno") -> instant wake-cue, no LLM.
            if cues.is_summon(transcript):
                audio_b64, text = await _try_cue("wake", companion, s, tts)
                await socket.send_json(
                    {"type": "cue", "role": "wake", "text": text, "audio_b64": audio_b64}
                )
                continue

            # 3. Instant filler cue (cached) while the real reply is produced.
            category = _filler_category(transcript)
            audio_b64, text = await _try_cue(category, companion, s, tts)
            if audio_b64:
                await socket.send_json(
                    {"type": "cue", "role": category, "text": text, "audio_b64": audio_b64}
                )

            # 4. The real, grounded, in-character reply.
            turn = await respond(companion, transcript, s, memory=_MEMORY)
            persona = get_persona(companion)
            reply_b64 = ""
            voice_id = persona.voice_id(s)
            if voice_id:
                try:
                    audio = await tts.synthesize(
                        turn.speech, voice_id=voice_id, stability=persona.stability,
                        language_code="ur", seed=persona.seed(s),
                    )
                    reply_b64 = _b64(audio)
                except Exception as exc:  # noqa: BLE001 - still send text if TTS fails
                    logger.warning("reply TTS failed: %s", exc)
            await socket.send_json(
                {
                    "type": "reply",
                    "display": turn.display.model_dump(),
                    "english_note": turn.english_note,
                    "audio_b64": reply_b64,
                }
            )
    except WebSocketDisconnect:
        logger.info("converse client disconnected")


# Minimal web UI at /ui/ (text chat + audio playback). Mounted last so API routes win.
if _STATIC.exists():
    app.mount("/ui", StaticFiles(directory=str(_STATIC), html=True), name="ui")
