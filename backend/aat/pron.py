"""Pronunciation coaching (docs/10) — Gemini-audio assessment fused with an STT round-trip.

No off-the-shelf API scores Urdu pronunciation. We combine two free signals:
  1. STT round-trip — transcribe the attempt; if the ASR "hears" a different word than the
     target (e.g. کلم instead of قلم), that's strong evidence of a mispronunciation.
  2. Gemini native-audio judgment — listens and gives kind, phoneme-aware feedback, informed
     by the ASR transcript.
A safety rule downgrades a "correct" verdict when the ASR clearly heard a different word.
"""

from __future__ import annotations

import json
import logging
import re

from aat.config import Settings
from aat.llm.gemini import GeminiProvider
from aat.schemas import PronunciationCheck
from aat.stt import build_stt_router

logger = logging.getLogger(__name__)

_FENCE = re.compile(r"```(?:json)?|```")
_VERDICTS = {"close", "closer", "correct", "unknown"}

_PROMPT = (
    "You are a warm, encouraging Urdu pronunciation coach. The learner is trying to say the "
    'Urdu word "{word}". An automatic speech recognizer heard their attempt as "{heard}" '
    "(possibly imperfect, but a clear consonant swap is meaningful). Listen to the attached "
    "audio and judge how well they said THIS word, focusing on the hard Urdu sounds that "
    "Hindi/English speakers flatten: qaaf (ق) vs kaaf (ک), khe (خ), ghain (غ), ain (ع), and "
    "the z-group (ز ذ ض ظ). If the audio or transcript shows a different sound than the "
    "target, do NOT say correct — name the exact sound kindly. Return STRICT JSON only: "
    '{{"verdict":"correct|closer|close|unknown","feedback":"one short, warm tip in Roman '
    'Hinglish naming the exact sound to fix and how; if truly correct, praise briefly"}}.'
)


def _normalize(text: str) -> str:
    """Strip whitespace + Urdu quotation marks for a loose word comparison."""
    return "".join(ch for ch in (text or "") if not ch.isspace() and ch not in "’‘'\"۔،")


async def assess(
    audio_wav: bytes,
    target_word: str,
    settings: Settings,
    *,
    language: str = "ur",
) -> PronunciationCheck:
    """Assess the learner's pronunciation of `target_word` from their audio (wav)."""
    heard: str | None = None
    try:
        transcript = await build_stt_router(settings).transcribe(audio_wav, language=language)
        heard = transcript.strip() or None
    except Exception as exc:  # noqa: BLE001 - STT round-trip is supplementary
        logger.info("pronunciation STT round-trip skipped: %s", exc)

    verdict, feedback = "unknown", None
    gemini = GeminiProvider(settings)
    if gemini.available(settings):
        try:
            raw = await gemini.analyze_audio(
                audio_wav,
                "audio/wav",
                _PROMPT.format(word=target_word, heard=heard or "(not transcribed)"),
                json_mode=True,
            )
            data = json.loads(_FENCE.sub("", raw).strip())
            verdict = data.get("verdict", "unknown")
            verdict = verdict if verdict in _VERDICTS else "unknown"
            feedback = data.get("feedback")
        except Exception as exc:  # noqa: BLE001 - degrade to 'unknown'
            logger.warning("pronunciation assessment failed: %s", exc)

    # Safety: if the ASR clearly heard a different word, it isn't "correct".
    if heard and verdict == "correct" and _normalize(heard) != _normalize(target_word):
        verdict = "closer"
        feedback = feedback or "Qareeb hai — woh pehli aawaaz dobara, thodi dhyaan se."

    return PronunciationCheck(
        target_word=target_word, heard=heard, verdict=verdict, feedback=feedback
    )
