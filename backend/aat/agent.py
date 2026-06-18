"""The lean agent: turn user text into a CompanionTurn (LLM -> parsed reply).

No LangChain. The agent:
  1. injects MEMORY (what we know about the user) + VERIFIED COUPLETS (corpus grounding,
     so poetry is never invented/misattributed) into the system prompt,
  2. calls the LLM router, parses the JSON, and enforces Urdu-script purity (retry once),
  3. persists newly taught vocabulary + the density dial to memory.
Full agentic function-calling (web/youtube tools) layers on later.
"""

from __future__ import annotations

import logging
import re

from aat.config import Settings
from aat.content import lookup as corpus_lookup
from aat.llm import build_llm_router
from aat.llm.base import LLMMessage
from aat.memory import MemoryStore
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


def _context_block(user_text: str, memory: MemoryStore | None, user_id: str) -> str:
    """Build the MEMORY + VERIFIED COUPLETS context injected into the system prompt."""
    parts: list[str] = []

    if memory is not None:
        try:
            profile = memory.get_profile(user_id)
            vocab = memory.recall_vocab(user_id, limit=8)
        except Exception as exc:  # noqa: BLE001 - memory is best-effort
            logger.warning("memory recall failed: %s", exc)
            profile, vocab = None, []
        lines: list[str] = []
        if profile and profile.get("name"):
            lines.append(f"- Their name: {profile['name']}")
        if vocab:
            words = ", ".join(v["word"] for v in vocab)
            lines.append(
                "- Words you've already taught them (re-surface naturally when relevant; "
                f"don't re-explain from scratch): {words}"
            )
        if lines:
            parts.append("== WHAT YOU REMEMBER ABOUT THEM ==\n" + "\n".join(lines))

    hits = [c for c in corpus_lookup(user_text, limit=2) if c.get("urdu")]
    if hits:
        couplets = "\n".join(
            f'- {c["poet"]}: «{c["urdu"]}» (roman: {c.get("roman", "")}; meaning: {c.get("gloss", "")})'
            for c in hits
        )
        parts.append(
            "== VERIFIED COUPLETS (the ONLY couplets you may quote this turn; quote the Urdu "
            "exactly as given and attribute to the named poet; if none truly fits the moment, "
            "do NOT quote — speak of the meaning instead) ==\n" + couplets
        )
    return "\n\n".join(parts)


async def respond(
    companion: Companion,
    user_text: str,
    settings: Settings,
    *,
    user_id: str = "local",
    memory: MemoryStore | None = None,
    history: list[LLMMessage] | None = None,
) -> CompanionTurn:
    """Produce one in-character companion turn (memory- and corpus-grounded, Urdu-pure)."""
    persona = get_persona(companion)
    llm = build_llm_router(settings)

    system = persona.system_prompt
    context = _context_block(user_text, memory, user_id)
    if context:
        system = f"{system}\n\n{context}"

    messages = list(history or []) + [LLMMessage(role="user", content=user_text)]
    turn = parse_turn(await llm.complete(messages, system=system, json_mode=True))

    if not speech_is_urdu_pure(turn.speech):
        logger.info("speech had non-Urdu script; retrying once for purity")
        retry_messages = messages + [LLMMessage(role="user", content=_PURITY_NUDGE)]
        try:
            retry = parse_turn(
                await llm.complete(retry_messages, system=system, json_mode=True)
            )
            if speech_is_urdu_pure(retry.speech):
                turn = retry
        except Exception as exc:  # noqa: BLE001 - keep the first turn if retry fails
            logger.warning("purity retry failed (%s); keeping original", exc)

    if memory is not None:
        try:
            if turn.teach and turn.teach.word:
                memory.write_vocab(user_id, turn.teach.word, turn.teach.gloss)
            memory.set_profile(user_id, urdu_density=turn.urdu_density)
        except Exception as exc:  # noqa: BLE001 - memory is best-effort
            logger.warning("memory write failed: %s", exc)

    return turn
