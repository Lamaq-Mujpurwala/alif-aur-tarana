"""STT package: provider factory + router."""

from __future__ import annotations

from aat.config import Settings
from aat.stt.base import STTProvider
from aat.stt.local_whisper import LocalWhisperSTT
from aat.stt.router import STTRouter
from aat.stt.sarvam import SarvamSTT


def build_stt_router(settings: Settings) -> STTRouter:
    """Assemble the STT ladder: Sarvam (cloud, best Hinglish) -> local Whisper (free)."""
    providers: list[STTProvider] = [SarvamSTT(settings), LocalWhisperSTT(settings)]
    # TODO(T2): insert GroqWhisperSTT(settings) between Sarvam and local for speed.
    return STTRouter(providers, settings)


__all__ = ["STTProvider", "STTRouter", "SarvamSTT", "LocalWhisperSTT", "build_stt_router"]
