"""One-time: synthesise + cache every acknowledgement cue so they play instantly.

Writes into backend/audio_cache (the same cache the API serves from). Safe to re-run —
already-cached phrases are skipped (no re-billing). Run: `uv run python precompute_cues.py`.
"""

from __future__ import annotations

import asyncio
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

from aat.config import get_settings
from aat.cues import iter_all
from aat.personas import get_persona
from aat.tts import AudioCache, build_tts_router


def _quota(settings) -> str:
    from elevenlabs.client import ElevenLabs

    client = ElevenLabs(api_key=settings.elevenlabs_api_key)
    for getter in (
        lambda: client.user.subscription.get(),
        lambda: client.user.get().subscription,
    ):
        try:
            sub = getter()
            return f"{sub.character_count}/{sub.character_limit}"
        except Exception:  # noqa: BLE001
            continue
    return "unknown"


async def main() -> None:
    s = get_settings()
    tts = build_tts_router(s, AudioCache("audio_cache"))
    ok = cached = fail = 0
    for category, companion, phrase in iter_all():
        persona = get_persona(companion)
        already = tts._cache and tts._cache.get(phrase, persona.voice_id(s), persona.stability)
        if already:
            cached += 1
            continue
        try:
            await tts.synthesize(
                phrase,
                voice_id=persona.voice_id(s),
                stability=persona.stability,
                language_code="ur",
                seed=persona.seed(s),
            )
            ok += 1
            print(f"OK   [{category}/{companion.value}] {phrase[:34]}")
        except Exception as exc:  # noqa: BLE001
            fail += 1
            print(f"FAIL [{category}/{companion.value}] {phrase[:24]}: {repr(exc)[:90]}")
    print(f"\nnew={ok}  already-cached={cached}  failed={fail}")
    print("ElevenLabs chars:", _quota(s))


if __name__ == "__main__":
    asyncio.run(main())
