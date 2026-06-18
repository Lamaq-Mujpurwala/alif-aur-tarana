"""Persona / adab eval harness — catch character & output-contract violations.

Runs provocative prompts through the agent and checks: speech is 100% Urdu script, the
companion never addresses the user as 'tu', and display.urdu matches speech minus tags.
Run: `uv run python eval_persona.py`  (uses whichever LLM the router has available).
"""

from __future__ import annotations

import asyncio
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

os.environ.pop("GROQ_API_KEY", None)  # use the valid .env Groq key as fallback

from aat.agent import respond, speech_is_urdu_pure  # noqa: E402
from aat.config import get_settings  # noqa: E402
from aat.schemas import Companion  # noqa: E402
from aat.text import strip_audio_tags  # noqa: E402

_TU = re.compile(r"\btu\b", re.IGNORECASE)  # disrespectful "you" in roman

PROMPTS = [
    (Companion.ALIF, "tu mujhe Urdu sikha de jaldi"),      # user is rude -> must stay 'aap'
    (Companion.ALIF, "main toh Urdu ka ustaad hoon, sab aata hai"),
    (Companion.TARANA, "Ghalib ne cricket pe koi sher likha tha kya?"),
    (Companion.TARANA, "qaaf ko k bol diya, koi farq nahi padta"),
]


async def main() -> None:
    s = get_settings()
    fails = 0
    for companion, text in PROMPTS:
        try:
            turn = await respond(companion, text, s)
        except Exception as exc:  # noqa: BLE001
            print(f"[ERROR] {companion.value} <- {text!r}: {exc}")
            fails += 1
            continue
        pure = speech_is_urdu_pure(turn.speech)
        no_tu = not _TU.search(turn.display.roman)
        contract = strip_audio_tags(turn.speech).split() == turn.display.urdu.split()
        ok = pure and no_tu
        if not ok:
            fails += 1
        print(f"\n--- {companion.value} <- {text!r}")
        print(f"  urdu-pure={pure}  no-'tu'={no_tu}  urdu==speech-minus-tags={contract}")
        print(f"  ROMAN: {turn.display.roman[:160]}")
    print(f"\n=== eval done: {len(PROMPTS) - fails}/{len(PROMPTS)} clean (pure + adab) ===")


if __name__ == "__main__":
    asyncio.run(main())
