"""Tiny on-disk TTS cache: identical (text, voice, stability) is never re-billed.

This is the cost lever from docs/03 §6.2 / docs/07 §2 — companion catchphrases and
repeated words become free after first synthesis.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


class AudioCache:
    """Content-addressed audio cache on the local filesystem."""

    def __init__(self, directory: Path | str = "audio_cache") -> None:
        self._dir = Path(directory)
        self._dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _key(text: str, voice_id: str, stability: str) -> str:
        raw = f"{voice_id}|{stability}|{text}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()[:32]

    def _path(self, key: str) -> Path:
        return self._dir / f"{key}.mp3"

    def get(self, text: str, voice_id: str, stability: str) -> bytes | None:
        path = self._path(self._key(text, voice_id, stability))
        return path.read_bytes() if path.exists() else None

    def put(self, text: str, voice_id: str, stability: str, audio: bytes) -> None:
        self._path(self._key(text, voice_id, stability)).write_bytes(audio)
