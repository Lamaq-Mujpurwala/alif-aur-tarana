"""Offline tests for pronunciation comparison helper (the assess() path needs an LLM)."""

from __future__ import annotations

from aat.pron import _normalize


def test_normalize_ignores_whitespace_and_marks():
    assert _normalize("  قلم ۔") == _normalize("قلم")


def test_normalize_distinguishes_qaaf_from_kaaf():
    # The downgrade rule depends on this: قلم (qalam) != کلم (kalam).
    assert _normalize("قلم") != _normalize("کلم")
