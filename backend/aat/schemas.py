"""Typed boundaries: the companion output contract and the client<->server events.

These mirror docs/09 §3 (output contract) and docs/03 §6.4 (streaming event protocol).
Keeping every boundary typed (Pydantic) is what lets us avoid a heavy agent framework.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


# --------------------------------------------------------------------------- #
# Companion output contract (what the LLM returns each turn)
# --------------------------------------------------------------------------- #
class TriScript(BaseModel):
    """One line rendered in all three scripts for the UI (no audio tags)."""

    roman: str
    urdu: str
    devanagari: str


class TeachItem(BaseModel):
    """A word/phrase the companion is teaching this turn (for highlight + memory)."""

    word: str
    gloss: str
    formality: Literal["casual", "poetic", "formal", "neutral"] = "neutral"


class ToolAction(BaseModel):
    """A side-effect the agent asks the runtime to perform (e.g. write memory)."""

    tool: str
    kind: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)


class PronunciationCheck(BaseModel):
    """Result of a 'repeat after me' / pronunciation nudge (docs/10)."""

    target_word: str
    heard: str | None = None
    verdict: Literal["close", "closer", "correct", "unknown"] = "unknown"
    feedback: str | None = None


class Companion(str, Enum):
    ALIF = "alif"
    TARANA = "tarana"


class CompanionTurn(BaseModel):
    """The structured reply for a single companion turn (docs/09 §3).

    `speech` carries ElevenLabs v3 audio tags and is sent to TTS.
    `display` is tag-free and shown on screen in three scripts.
    """

    speech: str
    display: TriScript
    english_note: str = ""  # short meaning shown on screen, never spoken (keeps accent clean)
    teach: TeachItem | None = None
    actions: list[ToolAction] = Field(default_factory=list)
    pronunciation_check: PronunciationCheck | None = None
    urdu_density: float = Field(default=0.35, ge=0.0, le=1.0)


# --------------------------------------------------------------------------- #
# Streaming event protocol (client <-> server over WebSocket)
# --------------------------------------------------------------------------- #
class EventType(str, Enum):
    PARTIAL_TRANSCRIPT = "partial_transcript"
    FINAL_TRANSCRIPT = "final_transcript"
    ASSISTANT_SENTENCE = "assistant_sentence"
    TTS_AUDIO_CHUNK = "tts_audio_chunk"
    TOOL_CALL = "tool_call"
    BARGE_IN = "barge_in"
    TURN_COMPLETE = "turn_complete"
    ERROR = "error"


class ServerEvent(BaseModel):
    """A single message streamed from server to client."""

    type: EventType
    data: dict[str, Any] = Field(default_factory=dict)


class StartTurn(BaseModel):
    """Client asks to begin a turn with a chosen companion."""

    companion: Companion = Companion.TARANA
    text: str | None = None  # optional: text input instead of audio
