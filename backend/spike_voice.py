"""T1/T2 voice spike: text -> agent.respond() (Gemini, persona, purity guard) -> v3 mp3.

Generates several out/*.mp3 examples to audition. Run: `uv run python spike_voice.py`.
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from pathlib import Path

# Windows consoles default to cp1252 and choke on Urdu; force UTF-8.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

# A stale OS-level GROQ_API_KEY (ends dxP5) shadows the valid key in .env (env > .env).
# Drop it so the .env Groq key works as a real fallback during this spike.
os.environ.pop("GROQ_API_KEY", None)

from aat.agent import respond  # noqa: E402 - after env fix-up
from aat.config import get_settings  # noqa: E402
from aat.personas import get_persona  # noqa: E402
from aat.schemas import Companion  # noqa: E402
from aat.tts import AudioCache, build_tts_router  # noqa: E402

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("spike")

# (companion, what the user says, short label) — chosen to PROVOKE wit, sarcasm,
# leg-pulling and honesty (not sycophancy). Friends, not servants.
SAMPLES: list[tuple[Companion, str, str]] = [
    (Companion.ALIF, "main toh Urdu ka ustaad hoon, mujhe sab aata hai", "wit-brag"),
    (Companion.ALIF, "bas jaldi se ek shaayari bata do, mere paas time nahi hai", "wit-lazy"),
    (Companion.ALIF, "Alif tum bade hi romantic ho yaar, kisi pe line maarte ho kya", "wit-flirt"),
    (Companion.TARANA, "Urdu aur Hindi toh bilkul same hain na, koi farq nahi", "wit-challenge"),
    (Companion.TARANA, "maine 'qaaf' ko 'k' bol diya, itna farq thodi padta hai", "wit-cheeky"),
    (Companion.TARANA, "Ghalib ne cricket pe koi sher likha tha kya?", "wit-silly"),
]


async def run(companion: Companion, user_text: str, label: str, out_dir: Path) -> None:
    s = get_settings()
    persona = get_persona(companion)
    tts = build_tts_router(s, AudioCache(str(out_dir / "cache")))

    print(f"\n========== {persona.display_name} / {label} ==========")
    print(f"user: {user_text}")
    turn = await respond(companion, user_text, s)
    print("URDU  :", turn.display.urdu)
    print("ROMAN :", turn.display.roman)
    if turn.english_note:
        print("NOTE  :", turn.english_note)

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
    out_path = out_dir / f"{companion.value}_{label}.mp3"
    out_path.write_bytes(audio)
    print(f"OK: {len(audio)} bytes -> {out_path}")


async def main() -> None:
    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)
    for companion, user_text, label in SAMPLES:
        try:
            await run(companion, user_text, label, out_dir)
        except Exception as exc:  # noqa: BLE001 - keep generating the rest
            logger.error("sample %s failed: %s", label, exc)


if __name__ == "__main__":
    asyncio.run(main())
