"""Speech-to-text provider interface."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from aat.config import Settings


@runtime_checkable
class STTProvider(Protocol):
    """Transcribe audio bytes to text (Urdu/Hindi/English, code-mixed)."""

    name: str

    def available(self, settings: Settings) -> bool:
        ...

    async def transcribe(self, audio: bytes, *, language: str = "ur") -> str:
        """Return the transcript for the given audio (wav/mp3 bytes)."""
        ...
