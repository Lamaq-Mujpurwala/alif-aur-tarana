"""TTSRouter: emotion-aware provider selection + caching + fallback.

ElevenLabs (emotion) for signature lines; Azure (volume) for the rest — see docs/02 §C.
Azure is deferred for the MVP, so today the ladder is just ElevenLabs + cache.
"""

from __future__ import annotations

import logging

from aat.config import Settings
from aat.exceptions import AllProvidersExhausted, ProviderDownError
from aat.tts.base import TTSProvider
from aat.tts.cache import AudioCache

logger = logging.getLogger(__name__)


class TTSRouter:
    """Pick a TTS provider per utterance, with caching and graceful fallback."""

    def __init__(
        self,
        providers: list[TTSProvider],
        settings: Settings,
        cache: AudioCache | None = None,
    ) -> None:
        if not providers:
            raise ValueError("TTSRouter needs at least one provider")
        self._providers = providers
        self._settings = settings
        self._cache = cache

    def _order(self, needs_emotion: bool) -> list[TTSProvider]:
        if not needs_emotion:
            return self._providers
        # Prefer emotion-capable providers (ElevenLabs) for expressive lines.
        emotive = [p for p in self._providers if p.supports_emotion]
        plain = [p for p in self._providers if not p.supports_emotion]
        return emotive + plain

    async def synthesize(
        self,
        text: str,
        *,
        voice_id: str,
        stability: str = "natural",
        language_code: str = "ur",
        seed: int | None = None,
        needs_emotion: bool = True,
    ) -> bytes:
        if self._cache is not None:
            cached = self._cache.get(text, voice_id, stability)
            if cached is not None:
                logger.debug("TTS cache hit (%d bytes)", len(cached))
                return cached

        last_error: Exception | None = None
        tried = False
        for provider in self._order(needs_emotion):
            if not provider.available(self._settings):
                continue
            tried = True
            try:
                audio = await provider.synthesize(
                    text,
                    voice_id=voice_id,
                    stability=stability,
                    language_code=language_code,
                    seed=seed,
                )
            except ProviderDownError as exc:
                logger.warning("TTS provider '%s' failed: %s", provider.name, exc)
                last_error = exc
                continue
            if self._cache is not None:
                self._cache.put(text, voice_id, stability, audio)
            return audio

        if not tried:
            raise AllProvidersExhausted("no TTS provider configured (set ELEVENLABS_API_KEY)")
        raise AllProvidersExhausted("all TTS providers failed") from last_error
