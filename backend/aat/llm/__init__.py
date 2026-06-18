"""LLM package: provider factory + router."""

from __future__ import annotations

from aat.config import Settings
from aat.llm.base import LLMMessage, LLMProvider
from aat.llm.gemini import GeminiProvider
from aat.llm.groq_llm import GroqProvider
from aat.llm.router import LLMRouter


def build_llm_router(settings: Settings) -> LLMRouter:
    """Assemble the default LLM fallback ladder.

    Order: Gemini Flash -> Groq -> (future: OpenRouter, local Alif-1.0).
    Providers that lack a key are skipped at call time.
    """
    providers: list[LLMProvider] = [GeminiProvider(settings), GroqProvider(settings)]
    # TODO: append OllamaProvider(alif-1.0) for the offline/Urdu-specialist path.
    return LLMRouter(providers, settings)


__all__ = [
    "LLMMessage",
    "LLMProvider",
    "LLMRouter",
    "GeminiProvider",
    "GroqProvider",
    "build_llm_router",
]
