"""Offline tests for the acknowledgement-cue logic."""

from __future__ import annotations

from aat.cues import CUES, is_summon, pick
from aat.schemas import Companion


def test_is_summon_true_cases():
    assert is_summon("Alif suno")
    assert is_summon("suno")
    assert is_summon("الف")  # Urdu name alone
    assert is_summon("o Tarana")


def test_is_summon_false_cases():
    assert not is_summon("ranjish ka matlab samjhao")
    assert not is_summon("ishq matlab")  # has a content word
    assert not is_summon("")


def test_pick_returns_a_real_phrase():
    assert pick("wake", Companion.ALIF) in CUES["wake"][Companion.ALIF]


def test_pick_varies():
    seen = {pick("thinking", Companion.TARANA) for _ in range(10)}
    assert len(seen) > 1  # not stuck on one phrase


def test_every_category_has_enough_variations():
    for category, per in CUES.items():
        for companion, phrases in per.items():
            assert len(phrases) >= 10, f"{category}/{companion.value} has too few"
