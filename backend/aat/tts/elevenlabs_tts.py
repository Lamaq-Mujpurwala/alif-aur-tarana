"""ElevenLabs v3 TTS provider — the expressive Urdu voice (docs/15).

Key v3 choices (docs/15): generate Urdu *script* text, enforce language_code="ur",
default stability Natural (0.5) / Creative (0.0) for signature lines, and pin a per-
companion seed for consistency. Audio tags like [warmly]/[sighs] are performed inline.
"""

from __future__ import annotations

import logging

from aat.config import Settings
from aat.exceptions import MissingKeyError, ProviderDownError, RateLimitError

logger = logging.getLogger(__name__)

# v3 stability modes -> numeric API value (docs/15 §1).
_STABILITY = {"creative": 0.0, "natural": 0.5, "robust": 1.0}


class ElevenLabsTTS:
    """ElevenLabs text-to-speech (model eleven_v3 by default)."""

    name = "elevenlabs"
    supports_emotion = True

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = None

    def available(self, settings: Settings) -> bool:
        return bool(settings.elevenlabs_api_key)

    def _ensure_client(self):
        if self._client is not None:
            return self._client
        if not self._settings.elevenlabs_api_key:
            raise MissingKeyError("ELEVENLABS_API_KEY is not set")
        from elevenlabs.client import AsyncElevenLabs

        self._client = AsyncElevenLabs(api_key=self._settings.elevenlabs_api_key)
        return self._client

    async def synthesize(
        self,
        text: str,
        *,
        voice_id: str,
        stability: str = "natural",
        language_code: str = "ur",
        seed: int | None = None,
    ) -> bytes:
        from elevenlabs import VoiceSettings

        client = self._ensure_client()
        voice_settings = VoiceSettings(
            stability=_STABILITY.get(stability, 0.5), similarity_boost=0.75
        )
        kwargs: dict = {
            "voice_id": voice_id,
            "text": text,
            "model_id": self._settings.elevenlabs_model,
            "language_code": language_code,
            "voice_settings": voice_settings,
            "output_format": "mp3_44100_128",
        }
        if seed is not None:
            kwargs["seed"] = seed
        try:
            stream = client.text_to_speech.convert(**kwargs)
            chunks = [chunk async for chunk in stream]
        except Exception as exc:  # noqa: BLE001 - mapped to taxonomy
            if "429" in str(exc) or "quota" in str(exc).lower():
                raise RateLimitError(f"elevenlabs rate-limited: {exc}") from exc
            raise ProviderDownError(f"elevenlabs failed: {exc}") from exc
        return b"".join(chunks)
