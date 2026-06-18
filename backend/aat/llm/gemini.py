"""Gemini LLM provider (google-genai SDK).

Verified working with google-genai 2.8 via `client.aio.models.generate_content`.
We set a generous max_output_tokens and no other length constraint (docs/15).
"""

from __future__ import annotations

import asyncio
import logging

from aat.config import Settings
from aat.exceptions import MissingKeyError, ProviderDownError, RateLimitError
from aat.llm.base import LLMMessage

logger = logging.getLogger(__name__)

# Gemini chat roles: user content is "user", model output is "model".
_ROLE_MAP = {"user": "user", "assistant": "model", "tool": "user", "system": "user"}


class GeminiProvider:
    """Google Gemini via the google-genai SDK."""

    name = "gemini"

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = None  # lazily created so import never requires a key

    def available(self, settings: Settings) -> bool:
        if settings.gemini_use_vertex:
            return bool(settings.gcp_project)
        return bool(settings.gemini_api_key)

    def _ensure_client(self):
        if self._client is not None:
            return self._client
        from google import genai  # imported lazily

        if self._settings.gemini_use_vertex:
            if not self._settings.gcp_project:
                raise MissingKeyError("GOOGLE_CLOUD_PROJECT is not set for Vertex mode")
            # Uses Application Default Credentials (gcloud ADC); no API key, no RPD cap.
            self._client = genai.Client(
                vertexai=True,
                project=self._settings.gcp_project,
                location=self._settings.gcp_location,
            )
        else:
            if not self._settings.gemini_api_key:
                raise MissingKeyError("GEMINI_API_KEY is not set")
            self._client = genai.Client(api_key=self._settings.gemini_api_key)
        return self._client

    async def complete(
        self,
        messages: list[LLMMessage],
        *,
        system: str,
        json_mode: bool = False,
    ) -> str:
        from google.genai import types

        client = self._ensure_client()
        contents = [
            types.Content(role=_ROLE_MAP.get(m.role, "user"), parts=[types.Part(text=m.content)])
            for m in messages
        ]
        config = types.GenerateContentConfig(
            system_instruction=system,
            response_mime_type="application/json" if json_mode else "text/plain",
            temperature=0.9,  # companions should feel human, not robotic
            # Generous headroom so longer, flourishing replies + tri-script JSON never
            # truncate. We deliberately do NOT constrain length tightly (docs/15).
            max_output_tokens=4096,
        )
        resp = None
        for attempt in range(3):  # retry transient 503/UNAVAILABLE with backoff
            try:
                resp = await client.aio.models.generate_content(
                    model=self._settings.gemini_model, contents=contents, config=config
                )
                break
            except Exception as exc:  # noqa: BLE001 - mapped to our taxonomy below
                if _is_rate_limit(exc):
                    raise RateLimitError(f"gemini rate-limited: {exc}") from exc
                if _is_transient(exc) and attempt < 2:
                    await asyncio.sleep(1.5 * (attempt + 1))
                    logger.warning("gemini transient error, retrying (%d): %s", attempt + 1, exc)
                    continue
                raise ProviderDownError(f"gemini failed: {exc}") from exc
        text = getattr(resp, "text", None)
        if not text:
            raise ProviderDownError("gemini returned empty response")
        return text

    async def analyze_audio(
        self, audio: bytes, mime_type: str, prompt: str, *, json_mode: bool = True
    ) -> str:
        """Send audio + a text prompt to Gemini (e.g. pronunciation assessment)."""
        from google.genai import types

        client = self._ensure_client()
        audio_part = types.Part.from_bytes(data=audio, mime_type=mime_type)
        config = types.GenerateContentConfig(
            response_mime_type="application/json" if json_mode else "text/plain",
            temperature=0.3,
            max_output_tokens=1024,
        )
        resp = None
        for attempt in range(3):
            try:
                resp = await client.aio.models.generate_content(
                    model=self._settings.gemini_model,
                    contents=[prompt, audio_part],
                    config=config,
                )
                break
            except Exception as exc:  # noqa: BLE001 - mapped to taxonomy
                if _is_rate_limit(exc):
                    raise RateLimitError(f"gemini audio rate-limited: {exc}") from exc
                if _is_transient(exc) and attempt < 2:
                    await asyncio.sleep(1.5 * (attempt + 1))
                    continue
                raise ProviderDownError(f"gemini audio failed: {exc}") from exc
        text = getattr(resp, "text", None)
        if not text:
            raise ProviderDownError("gemini audio returned empty response")
        return text


def _is_rate_limit(exc: Exception) -> bool:
    text = str(exc).lower()
    return "429" in text or "rate" in text or "quota" in text or "resource_exhausted" in text


def _is_transient(exc: Exception) -> bool:
    text = str(exc).lower()
    return "503" in text or "unavailable" in text or "overloaded" in text or "500" in text
