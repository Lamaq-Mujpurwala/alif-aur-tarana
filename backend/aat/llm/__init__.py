"""LLM package: provider factory + router."""

from __future__ import annotations

from aat.config import Settings
from aat.llm.base import LLMMessage, LLMProvider
from aat.llm.gemini import GeminiProvider
from aat.llm.router import LLMRouter


def build_llm_router(settings: Settings) -> LLMRouter:
    """Assemble the default LLM fallback ladder.

    Order: Gemini Flash -> (future: Groq, OpenRouter) -> (future: local Alif-1.0).
    Providers that lack a key are simply skipped at call time.
    """
    providers: list[LLMProvider] = [GeminiProvider(settings)]
    # TODO(T1+): append GroqProvider, OllamaProvider(alif-1.0) as they're wired.
    return LLMRouter(providers, settings)


__all__ = ["LLMMessage", "LLMProvider", "LLMRouter", "GeminiProvider", "build_llm_router"]
