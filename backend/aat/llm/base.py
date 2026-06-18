"""LLM provider interface + the message/result types used across providers."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from pydantic import BaseModel

from aat.config import Settings


class LLMMessage(BaseModel):
    """A single chat message."""

    role: str  # "system" | "user" | "assistant" | "tool"
    content: str


@runtime_checkable
class LLMProvider(Protocol):
    """A minimal LLM provider. Streaming + tool-calling arrive in T3."""

    name: str

    def available(self, settings: Settings) -> bool:
        """True if this provider is configured (has its key / is reachable)."""
        ...

    async def complete(
        self,
        messages: list[LLMMessage],
        *,
        system: str,
        json_mode: bool = False,
    ) -> str:
        """Return the assistant's text reply (JSON string if json_mode)."""
        ...
