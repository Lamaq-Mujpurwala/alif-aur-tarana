"""LLMRouter: try providers in order, fall back on rate-limit / outage.

This is the "tiny model router, no LangChain" from docs/05 §3. Fully testable with a
fake provider — no network required.
"""

from __future__ import annotations

import logging

from aat.config import Settings
from aat.exceptions import AllProvidersExhausted, ProviderDownError
from aat.llm.base import LLMMessage, LLMProvider

logger = logging.getLogger(__name__)


class LLMRouter:
    """Ordered set of LLM providers with graceful fallback."""

    def __init__(self, providers: list[LLMProvider], settings: Settings) -> None:
        if not providers:
            raise ValueError("LLMRouter needs at least one provider")
        self._providers = providers
        self._settings = settings

    def _order(self, prefer: str | None) -> list[LLMProvider]:
        if not prefer:
            return self._providers
        preferred = [p for p in self._providers if p.name == prefer]
        rest = [p for p in self._providers if p.name != prefer]
        return preferred + rest

    def available_providers(self) -> list[str]:
        return [p.name for p in self._providers if p.available(self._settings)]

    async def complete(
        self,
        messages: list[LLMMessage],
        *,
        system: str,
        json_mode: bool = False,
        prefer: str | None = None,
    ) -> str:
        """Return the first successful provider's reply, else raise."""
        last_error: Exception | None = None
        tried = False
        for provider in self._order(prefer):
            if not provider.available(self._settings):
                continue
            tried = True
            try:
                return await provider.complete(messages, system=system, json_mode=json_mode)
            except ProviderDownError as exc:
                logger.warning("LLM provider '%s' failed, falling back: %s", provider.name, exc)
                last_error = exc
                continue
        if not tried:
            raise AllProvidersExhausted("no LLM provider is configured (set GEMINI_API_KEY)")
        raise AllProvidersExhausted("all LLM providers failed") from last_error
