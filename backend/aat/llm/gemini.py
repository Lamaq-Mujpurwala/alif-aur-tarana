"""Gemini LLM provider (google-genai SDK).

NOTE: verify the exact SDK surface once GEMINI_API_KEY is set and `google-genai` is
installed (`uv sync`). The async path is `client.aio.models.generate_content`.
"""

from __future__ import annotations

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
        return bool(settings.gemini_api_key)

    def _ensure_client(self):
        if self._client is not None:
            return self._client
        if not self._settings.gemini_api_key:
            raise MissingKeyError("GEMINI_API_KEY is not set")
        from google import genai  # imported lazily

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
        )
        try:
            resp = await client.aio.models.generate_content(
                model=self._settings.gemini_model, contents=contents, config=config
            )
        except Exception as exc:  # noqa: BLE001 - mapped to our taxonomy below
            if _is_rate_limit(exc):
                raise RateLimitError(f"gemini rate-limited: {exc}") from exc
            raise ProviderDownError(f"gemini failed: {exc}") from exc
        text = getattr(resp, "text", None)
        if not text:
            raise ProviderDownError("gemini returned empty response")
        return text


def _is_rate_limit(exc: Exception) -> bool:
    text = str(exc).lower()
    return "429" in text or "rate" in text or "quota" in text or "resource_exhausted" in text
