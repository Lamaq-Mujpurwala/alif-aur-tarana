"""STTRouter: Sarvam (best Hinglish) -> Groq Whisper -> local Whisper (docs/02 §A)."""

from __future__ import annotations

import logging

from aat.config import Settings
from aat.exceptions import AllProvidersExhausted, ProviderDownError
from aat.stt.base import STTProvider

logger = logging.getLogger(__name__)


class STTRouter:
    """Ordered STT providers with graceful fallback to local Whisper."""

    def __init__(self, providers: list[STTProvider], settings: Settings) -> None:
        if not providers:
            raise ValueError("STTRouter needs at least one provider")
        self._providers = providers
        self._settings = settings

    def available_providers(self) -> list[str]:
        return [p.name for p in self._providers if p.available(self._settings)]

    async def transcribe(self, audio: bytes, *, language: str = "ur") -> str:
        last_error: Exception | None = None
        tried = False
        for provider in self._providers:
            if not provider.available(self._settings):
                continue
            tried = True
            try:
                return await provider.transcribe(audio, language=language)
            except ProviderDownError as exc:
                logger.warning("STT provider '%s' failed: %s", provider.name, exc)
                last_error = exc
                continue
        if not tried:
            raise AllProvidersExhausted(
                "no STT provider available (set SARVAM_API_KEY or install faster-whisper)"
            )
        raise AllProvidersExhausted("all STT providers failed") from last_error
