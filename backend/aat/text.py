"""Small, dependency-free text helpers (tri-script + audio-tag handling)."""

from __future__ import annotations

import re

# ElevenLabs v3 audio tags look like [sighs], [laughs softly], [warmly], etc.
_AUDIO_TAG_RE = re.compile(r"\[[^\]]{1,40}\]")
_WS_RE = re.compile(r"\s{2,}")


def strip_audio_tags(speech: str) -> str:
    """Remove `[...]` audio tags so spoken text can be shown cleanly on screen.

    A safety net: the LLM should already return a tag-free `display`, but we never
    want a stray `[sighs]` to leak into the tri-script UI.
    """
    cleaned = _AUDIO_TAG_RE.sub("", speech)
    cleaned = _WS_RE.sub(" ", cleaned)
    return cleaned.strip()


def audio_tags(speech: str) -> list[str]:
    """Return the audio tags present in a line, e.g. ['[sighs]', '[warmly]']."""
    return _AUDIO_TAG_RE.findall(speech)
