"""Tests for the local poetry corpus lookup (grounding source)."""

from __future__ import annotations

from aat.content import lookup


def test_lookup_by_poet():
    hits = lookup(poet="Faraz", limit=2)
    assert hits and any("Faraz" in c["poet"] for c in hits)


def test_lookup_by_query_token():
    hits = lookup("ranjish", limit=2)
    assert any("ranjish" in c["roman"].lower() for c in hits)


def test_lookup_miss_returns_empty():
    assert lookup("zzqq_nonexistent_token") == []


def test_lookup_respects_limit():
    assert len(lookup("ghalib", limit=1)) <= 1


def test_grounded_couplets_have_urdu():
    # Every seeded couplet must carry Urdu text so spoken quotes can render.
    for c in lookup(poet="Ghalib", limit=5):
        assert c.get("urdu")
