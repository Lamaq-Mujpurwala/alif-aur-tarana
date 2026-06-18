"""Audio helpers: transcode arbitrary client audio (webm/ogg/mp3) to WAV for STT.

Browsers record webm/opus; Sarvam wants clean wav. ffmpeg (already installed) normalises
everything to 16 kHz mono PCM, which both Sarvam and faster-whisper handle well.
"""

from __future__ import annotations

import asyncio
import logging

from aat.exceptions import ProviderDownError

logger = logging.getLogger(__name__)


async def to_wav(audio: bytes, *, sample_rate: int = 16000) -> bytes:
    """Transcode arbitrary audio bytes to 16 kHz mono PCM WAV via ffmpeg."""
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error",
        "-i", "pipe:0", "-ar", str(sample_rate), "-ac", "1", "-f", "wav", "pipe:1",
    ]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, err = await proc.communicate(input=audio)
    if proc.returncode != 0:
        raise ProviderDownError(f"ffmpeg transcode failed: {err.decode(errors='ignore')[:200]}")
    return out
