"""Tests for text helpers + the agent's purity/parse helpers (offline, no LLM)."""

from __future__ import annotations

from aat.agent import parse_turn, speech_is_urdu_pure
from aat.text import audio_tags, strip_audio_tags


def test_strip_audio_tags_removes_brackets():
    assert strip_audio_tags("[warmly] آہ [sighs] فراز") == "آہ فراز"


def test_strip_audio_tags_noop_when_none():
    assert strip_audio_tags("just words") == "just words"


def test_audio_tags_lists_them():
    assert audio_tags("[warmly] x [sighs]") == ["[warmly]", "[sighs]"]
    assert audio_tags("none here") == []


def test_pure_urdu_is_pure():
    assert speech_is_urdu_pure("[warmly] رنجش ہی سہی… دل ہی دکھانے کے لیے آ")


def test_english_inside_tags_is_allowed():
    # Latin only inside [tags] must NOT count as impurity.
    assert speech_is_urdu_pure("[laughs softly] محبت اور عشق")


def test_latin_in_speech_is_impure():
    assert not speech_is_urdu_pure("[warmly] رنجش Seekh لو")


def test_devanagari_in_speech_is_impure():
    assert not speech_is_urdu_pure("فراق पडता ہے")


def test_parse_turn_plain_json():
    raw = (
        '{"speech":"[warmly] محبت","display":{"urdu":"محبت","roman":"mohabbat",'
        '"devanagari":"मोहब्बत"},"english_note":"love","teach":null,"actions":[],'
        '"pronunciation_check":null,"urdu_density":0.4}'
    )
    turn = parse_turn(raw)
    assert turn.display.roman == "mohabbat"
    assert turn.urdu_density == 0.4


def test_parse_turn_tolerates_markdown_fences():
    raw = '```json\n{"speech":"x","display":{"urdu":"x","roman":"x","devanagari":"x"}}\n```'
    turn = parse_turn(raw)
    assert turn.speech == "x"
