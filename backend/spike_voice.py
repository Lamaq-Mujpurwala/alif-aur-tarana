"""T1 voice spike: text -> Gemini (in persona) -> Urdu JSON -> ElevenLabs v3 -> mp3.

Proves the hard part: the companions produce in-character Urdu-script speech that the v3
engine voices with a real Urdu accent. Run: `uv run python spike_voice.py`.
Outputs out/alif.mp3 and out/tarana.mp3 — listen to them.
"""

from __future__ import annotations

import asyncio
import logging
import re
import sys
from pathlib import Path

from aat.config import get_settings
from aat.llm import build_llm_router
from aat.llm.base import LLMMessage
from aat.personas import get_persona
from aat.schemas import Companion, CompanionTurn
from aat.tts import AudioCache, build_tts_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("spike")

# Windows consoles default to cp1252 and choke when printing Urdu; force UTF-8.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

_FENCE = re.compile(r"```(?:json)?|```")


def _parse_turn(raw: str) -> CompanionTurn:
    """Parse the LLM reply into a CompanionTurn, tolerating stray markdown fences."""
    cleaned = _FENCE.sub("", raw).strip()
    return CompanionTurn.model_validate_json(cleaned)


async def run(companion: Companion, user_text: str, out_dir: Path) -> None:
    s = get_settings()
    persona = get_persona(companion)
    llm = build_llm_router(s)
    tts = build_tts_router(s, AudioCache(str(out_dir / "cache")))

    print(f"\n========== {persona.display_name} ==========")
    print(f"user: {user_text}")
    raw = await llm.complete(
        [LLMMessage(role="user", content=user_text)],
        system=persona.system_prompt,
        json_mode=True,
    )
    turn = _parse_turn(raw)
    print("URDU  :", turn.display.urdu)
    print("ROMAN :", turn.display.roman)
    if turn.english_note:
        print("NOTE  :", turn.english_note)
    print("SPEECH:", turn.speech)

    voice_id = persona.voice_id(s)
    if not voice_id:
        print(f"!! no voice id ({persona.voice_setting}); skipping TTS")
        return
    audio = await tts.synthesize(
        turn.speech,
        voice_id=voice_id,
        stability=persona.stability,
        language_code="ur",
        seed=persona.seed(s),
    )
    out_path = out_dir / f"{companion.value}.mp3"
    out_path.write_bytes(audio)
    print(f"OK: saved {len(audio)} bytes -> {out_path}")


async def main() -> None:
    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)
    await run(Companion.TARANA, "tarana 'ranjish' ka matlab samjhao na", out_dir)
    await run(Companion.ALIF, "Alif yaar mujhe kuch romantic sa sunao", out_dir)


if __name__ == "__main__":
    asyncio.run(main())
