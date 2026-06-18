"""TTS-only spike: voice the companions from hardcoded Urdu lines (no LLM needed).

Validates the docs/15 finding: Urdu-script text + language_code='ur' + v3 = real accent.
Run: `uv run python spike_tts.py` -> out/alif_tts.mp3, out/tarana_tts.mp3.
"""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from aat.config import get_settings
from aat.personas import get_persona
from aat.schemas import Companion
from aat.tts import AudioCache, build_tts_router

logging.basicConfig(level=logging.INFO)

LINES: dict[Companion, str] = {
    Companion.TARANA: (
        "[gently] ’رنجش‘… یعنی گلہ، ایک نرم سی ناراضگی۔ "
        "[warmly] فرازؔ صاحب فرماتے ہیں… ’رنجش ہی سہی، دل ہی دکھانے کے لیے آ‘۔"
    ),
    Companion.ALIF: (
        "[warmly] آپ کے لیے؟ [softly] ’تم مخاطب بھی ہو، قریب بھی ہو… "
        "تم کو دیکھوں کہ تم سے بات کروں‘۔ [sighs] فرازؔ صاحب نے آپ کا دل پڑھ لیا، لگتا ہے۔"
    ),
}


async def main() -> None:
    s = get_settings()
    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)
    tts = build_tts_router(s, AudioCache(str(out_dir / "cache")))
    for companion, line in LINES.items():
        persona = get_persona(companion)
        voice_id = persona.voice_id(s)
        if not voice_id:
            print(f"!! no voice id for {companion.value}")
            continue
        audio = await tts.synthesize(
            line,
            voice_id=voice_id,
            stability=persona.stability,
            language_code="ur",
            seed=persona.seed(s),
        )
        out_path = out_dir / f"{companion.value}_tts.mp3"
        out_path.write_bytes(audio)
        print(f"{persona.display_name}: saved {len(audio)} bytes -> {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
