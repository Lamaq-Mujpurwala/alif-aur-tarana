"""Sarvam Saarika STT — best for Hinglish/Urdu code-mixed speech (docs/02 §A).

Verified against docs.sarvam.ai: POST multipart to /speech-to-text with the
api-subscription-key header; model "saarika:v2.5"; language_code in BCP-47 (e.g. hi-IN,
ur-IN) or "unknown" for auto-detect. Audio works best at 16 kHz (we feed 16 kHz wav).
"""

from __future__ import annotations

import logging

import httpx

from aat.config import Settings
from aat.exceptions import MissingKeyError, ProviderDownError, RateLimitError

logger = logging.getLogger(__name__)

_ENDPOINT = "https://api.sarvam.ai/speech-to-text"


class SarvamSTT:
    """Sarvam speech-to-text over REST."""

    name = "sarvam"

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def available(self, settings: Settings) -> bool:
        return bool(settings.sarvam_api_key)

    async def transcribe(self, audio: bytes, *, language: str = "ur") -> str:
        if not self._settings.sarvam_api_key:
            raise MissingKeyError("SARVAM_API_KEY is not set")
        lang_code = language if ("-" in language or language == "unknown") else f"{language}-IN"
        headers = {"api-subscription-key": self._settings.sarvam_api_key}
        files = {"file": ("audio.wav", audio, "audio/wav")}
        data = {"model": "saarika:v2.5", "language_code": lang_code}
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(_ENDPOINT, headers=headers, files=files, data=data)
            if resp.status_code == 429:
                raise RateLimitError("sarvam rate-limited")
            resp.raise_for_status()
        except RateLimitError:
            raise
        except httpx.HTTPError as exc:
            raise ProviderDownError(f"sarvam failed: {exc}") from exc
        payload = resp.json()
        return payload.get("transcript", "")
