"""Local faster-whisper STT — free, unlimited, private on the RTX 4060 (docs/02 §A).

The ultimate fallback: no key, no quota. Uses int8 to fit the 8GB GPU (~2.5GB VRAM).
"""

from __future__ import annotations

import asyncio
import io
import logging

from aat.config import Settings
from aat.exceptions import ProviderDownError

logger = logging.getLogger(__name__)


class LocalWhisperSTT:
    """faster-whisper running locally (CUDA if available, else CPU)."""

    name = "whisper-local"

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._model = None

    def available(self, settings: Settings) -> bool:
        try:
            import faster_whisper  # noqa: F401
        except ImportError:
            return False
        return True

    def _ensure_model(self):
        if self._model is not None:
            return self._model
        from faster_whisper import WhisperModel

        # device='cuda', compute_type='int8' for the 4060; falls back to CPU if no GPU.
        try:
            self._model = WhisperModel(
                self._settings.whisper_model, device="cuda", compute_type="int8"
            )
        except Exception:  # noqa: BLE001 - CPU fallback for machines without CUDA
            logger.info("CUDA unavailable; loading whisper on CPU")
            self._model = WhisperModel(
                self._settings.whisper_model, device="cpu", compute_type="int8"
            )
        return self._model

    async def transcribe(self, audio: bytes, *, language: str = "ur") -> str:
        def _run() -> str:
            model = self._ensure_model()
            segments, _info = model.transcribe(io.BytesIO(audio), language=language)
            return " ".join(seg.text for seg in segments).strip()

        try:
            return await asyncio.to_thread(_run)
        except Exception as exc:  # noqa: BLE001 - mapped to taxonomy
            raise ProviderDownError(f"local whisper failed: {exc}") from exc
