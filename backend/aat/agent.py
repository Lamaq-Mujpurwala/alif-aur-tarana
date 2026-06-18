"""The lean agent: turn user text into a CompanionTurn (LLM -> parsed reply).

No LangChain — just the LLM router + the persona system prompt + JSON parsing.
Tool-calling (memory / rekhta / web) plugs in here in T5.
"""

from __future__ import annotations

import re

from aat.config import Settings
from aat.llm import build_llm_router
from aat.llm.base import LLMMessage
from aat.personas import get_persona
from aat.schemas import Companion, CompanionTurn

_FENCE = re.compile(r"```(?:json)?|```")


def parse_turn(raw: str) -> CompanionTurn:
    """Parse the LLM's JSON reply into a CompanionTurn (tolerating stray fences)."""
    return CompanionTurn.model_validate_json(_FENCE.sub("", raw).strip())


async def respond(
    companion: Companion,
    user_text: str,
    settings: Settings,
    history: list[LLMMessage] | None = None,
) -> CompanionTurn:
    """Produce a single in-character companion turn for the given user text."""
    persona = get_persona(companion)
    llm = build_llm_router(settings)
    messages = list(history or []) + [LLMMessage(role="user", content=user_text)]
    raw = await llm.complete(messages, system=persona.system_prompt, json_mode=True)
    return parse_turn(raw)
