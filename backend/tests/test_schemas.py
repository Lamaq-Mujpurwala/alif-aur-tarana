"""Tests for the companion output-contract schemas."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from aat.schemas import CompanionTurn, TeachItem, TriScript


def _turn(**kw) -> CompanionTurn:
    base = dict(speech="x", display=TriScript(urdu="x", roman="x", devanagari="x"))
    base.update(kw)
    return CompanionTurn(**base)


def test_companion_turn_defaults():
    t = _turn()
    assert t.urdu_density == 0.35
    assert t.english_note == ""
    assert t.actions == []
    assert t.teach is None


def test_teach_item_formality_default():
    assert TeachItem(word="ishq", gloss="love").formality == "neutral"


def test_density_must_be_within_bounds():
    with pytest.raises(ValidationError):
        _turn(urdu_density=2.0)
    with pytest.raises(ValidationError):
        _turn(urdu_density=-0.1)
