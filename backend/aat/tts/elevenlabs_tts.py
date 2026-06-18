"""ElevenLabs v3 TTS provider — the expressive Urdu voice (docs/02 §C).

NOTE: verify the exact SDK surface once ELEVENLABS_API_KEY is set and `elevenlabs` is
installed. v3 performs audio tags like [sighs]/[warmly]; stability is creative/natural/
robust. Use 'natural' by default, 'creative' for signature emotional lines (docs/09 §2).
"""

from __future__ import annotations

import logging

from aat.config import Settings
from aat.exceptions import MissingKeyError, ProviderDownError, RateLimitError

logger = logging.getLogger(__name__)

# v3 stability mode -> numeric setting (verify against SDK version).
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
        self, text: str, *, voice_id: str, stability: str = "natural"
    ) -> bytes:
        from elevenlabs import VoiceSettings

        client = self._ensure_client()
        settings = VoiceSettings(stability=_STABILITY.get(stability, 0.5), similarity_boost=0.8)
        try:
            stream = client.text_to_speech.convert(
                voice_id=voice_id,
                model_id=self._settings.elevenlabs_model,
                text=text,
                voice_settings=settings,
            )
            chunks = [chunk async for chunk in stream]
        except Exception as exc:  # noqa: BLE001 - mapped to taxonomy
            if "429" in str(exc) or "quota" in str(exc).lower():
                raise RateLimitError(f"elevenlabs rate-limited: {exc}") from exc
            raise ProviderDownError(f"elevenlabs failed: {exc}") from exc
        return b"".join(chunks)
