"""Text-to-speech provider interface."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from aat.config import Settings


@runtime_checkable
class TTSProvider(Protocol):
    """Synthesise speech audio (bytes) from tagged/plain text."""

    name: str
    supports_emotion: bool  # True for ElevenLabs v3 audio tags

    def available(self, settings: Settings) -> bool:
        ...

    async def synthesize(
        self, text: str, *, voice_id: str, stability: str = "natural"
    ) -> bytes:
        """Return audio bytes (mp3/wav) for the given text and voice."""
        ...
