"""Groq LLM provider — fast cloud fallback brain (docs/02 §B).

Used when Gemini is rate-limited/unavailable. Groq's JSON mode requires the word "json"
to appear in the messages — our system prompt already specifies a JSON contract.
"""

from __future__ import annotations

import logging

from aat.config import Settings
from aat.exceptions import MissingKeyError, ProviderDownError, RateLimitError
from aat.llm.base import LLMMessage

logger = logging.getLogger(__name__)

_MODEL = "llama-3.3-70b-versatile"  # current multilingual Groq model


class GroqProvider:
    """Groq-hosted LLM via the official async SDK."""

    name = "groq"

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = None

    def available(self, settings: Settings) -> bool:
        return bool(settings.groq_api_key)

    def _ensure_client(self):
        if self._client is not None:
            return self._client
        if not self._settings.groq_api_key:
            raise MissingKeyError("GROQ_API_KEY is not set")
        from groq import AsyncGroq

        self._client = AsyncGroq(api_key=self._settings.groq_api_key)
        return self._client

    async def complete(
        self,
        messages: list[LLMMessage],
        *,
        system: str,
        json_mode: bool = False,
    ) -> str:
        client = self._ensure_client()
        payload = [{"role": "system", "content": system}]
        payload += [{"role": m.role, "content": m.content} for m in messages]
        kwargs: dict = {"model": _MODEL, "messages": payload, "temperature": 0.9}
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        try:
            resp = await client.chat.completions.create(**kwargs)
        except Exception as exc:  # noqa: BLE001 - mapped to taxonomy
            if "429" in str(exc) or "rate" in str(exc).lower():
                raise RateLimitError(f"groq rate-limited: {exc}") from exc
            raise ProviderDownError(f"groq failed: {exc}") from exc
        return resp.choices[0].message.content or ""
