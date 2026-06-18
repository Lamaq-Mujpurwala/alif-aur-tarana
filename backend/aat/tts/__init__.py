"""TTS package: provider factory + router."""

from __future__ import annotations

from aat.config import Settings
from aat.tts.base import TTSProvider
from aat.tts.cache import AudioCache
from aat.tts.elevenlabs_tts import ElevenLabsTTS
from aat.tts.router import TTSRouter


def build_tts_router(settings: Settings, cache: AudioCache | None = None) -> TTSRouter:
    """Assemble the TTS ladder. ElevenLabs now; Azure added when its key is set."""
    providers: list[TTSProvider] = [ElevenLabsTTS(settings)]
    # TODO(post-MVP): append AzureTTS(settings) for the 500k-chars/mo bulk voice.
    return TTSRouter(providers, settings, cache=cache or AudioCache())


__all__ = ["TTSProvider", "TTSRouter", "ElevenLabsTTS", "AudioCache", "build_tts_router"]
