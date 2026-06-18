"""Persona registry: resolve a Companion to its full prompt + voice/TTS config."""

from __future__ import annotations

from dataclasses import dataclass, field

from aat.config import Settings
from aat.personas.alif import ALIF_BODY
from aat.personas.shared import compose
from aat.personas.tarana import TARANA_BODY
from aat.schemas import Companion


@dataclass(frozen=True)
class Persona:
    """Everything the runtime needs to make a companion speak in character."""

    companion: Companion
    display_name: str
    system_prompt: str
    voice_setting: str  # Settings attribute holding the ElevenLabs voice id
    seed_setting: str  # Settings attribute holding this companion's fixed TTS seed
    stability: str = "natural"  # ElevenLabs v3: 'natural' | 'creative' | 'robust'
    favored_tags: tuple[str, ...] = field(default_factory=tuple)

    def voice_id(self, settings: Settings) -> str | None:
        """Resolve this persona's configured voice id from settings (may be None)."""
        return getattr(settings, self.voice_setting, None)

    def seed(self, settings: Settings) -> int | None:
        """Resolve this persona's fixed TTS seed (for consistent voice across takes)."""
        return getattr(settings, self.seed_setting, None)


_REGISTRY: dict[Companion, Persona] = {
    Companion.ALIF: Persona(
        companion=Companion.ALIF,
        display_name="Alif",
        system_prompt=compose(ALIF_BODY),
        voice_setting="alif_voice_id",
        seed_setting="alif_seed",
        stability="natural",
        favored_tags=(
            "[warmly]", "[sighs]", "[laughs softly]", "[whispers]",
            "[excited]", "[mischievously]", "[dreamily]",
        ),
    ),
    Companion.TARANA: Persona(
        companion=Companion.TARANA,
        display_name="Tarana",
        system_prompt=compose(TARANA_BODY),
        voice_setting="tarana_voice_id",
        seed_setting="tarana_seed",
        stability="natural",
        favored_tags=(
            "[gently]", "[warmly]", "[softly]", "[thoughtful]",
            "[reassuring]", "[curious]",
        ),
    ),
}


def get_persona(companion: Companion) -> Persona:
    """Return the Persona for a companion."""
    return _REGISTRY[companion]


__all__ = ["Persona", "get_persona"]
