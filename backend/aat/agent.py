"""The lean agent: turn user text into a CompanionTurn (LLM -> parsed reply).

No LangChain — just the LLM router + the persona system prompt + JSON parsing, plus a
script-purity guard (the spoken Urdu must not contain Latin/Devanagari/Cyrillic, which
would wreck the v3 accent — docs/15). Tool-calling plugs in here in T5.
"""

from __future__ import annotations

import logging
import re

from aat.config import Settings
from aat.llm import build_llm_router
from aat.llm.base import LLMMessage
from aat.personas import get_persona
from aat.schemas import Companion, CompanionTurn

logger = logging.getLogger(__name__)

_FENCE = re.compile(r"```(?:json)?|```")
_TAG = re.compile(r"\[[^\]]*\]")
# Disallowed in spoken Urdu: Latin, Cyrillic, Devanagari letters (outside [audio tags]).
_NON_URDU = re.compile(r"[A-Za-zЀ-ӿऀ-ॿ]")

_PURITY_NUDGE = (
    "(System reminder: your previous 'speech' contained non-Urdu letters. Rewrite the "
    "WHOLE reply as valid JSON with 'speech' in 100% Urdu script — no Latin, Devanagari "
    "or other scripts anywhere except inside [audio tags]. Transliterate any English word "
    "into Urdu.)"
)


def parse_turn(raw: str) -> CompanionTurn:
    """Parse the LLM's JSON reply into a CompanionTurn (tolerating stray fences)."""
    return CompanionTurn.model_validate_json(_FENCE.sub("", raw).strip())


def speech_is_urdu_pure(speech: str) -> bool:
    """True if the spoken line (minus [tags]) has no Latin/Devanagari/Cyrillic letters."""
    return not _NON_URDU.search(_TAG.sub("", speech))


async def respond(
    companion: Companion,
    user_text: str,
    settings: Settings,
    history: list[LLMMessage] | None = None,
) -> CompanionTurn:
    """Produce a single in-character companion turn; retry once if speech isn't pure Urdu."""
    persona = get_persona(companion)
    llm = build_llm_router(settings)
    messages = list(history or []) + [LLMMessage(role="user", content=user_text)]

    raw = await llm.complete(messages, system=persona.system_prompt, json_mode=True)
    turn = parse_turn(raw)
    if speech_is_urdu_pure(turn.speech):
        return turn

    logger.info("speech had non-Urdu script; retrying once for purity")
    retry_messages = messages + [LLMMessage(role="user", content=_PURITY_NUDGE)]
    try:
        retry = parse_turn(
            await llm.complete(retry_messages, system=persona.system_prompt, json_mode=True)
        )
    except Exception as exc:  # noqa: BLE001 - keep the first turn if retry fails
        logger.warning("purity retry failed (%s); keeping original", exc)
        return turn
    return retry if speech_is_urdu_pure(retry.speech) else turn
