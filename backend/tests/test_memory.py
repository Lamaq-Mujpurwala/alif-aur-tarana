"""Tests for the SQLite memory store (offline)."""

from __future__ import annotations

from aat.memory import MemoryStore


def test_vocab_write_and_recall(tmp_path):
    m = MemoryStore(str(tmp_path / "m.db"))
    m.write_vocab("u1", "firaaq", "separation")
    vocab = m.recall_vocab("u1")
    assert vocab and vocab[0]["word"] == "firaaq"


def test_vocab_times_used_increments(tmp_path):
    m = MemoryStore(str(tmp_path / "m.db"))
    m.write_vocab("u1", "ishq", "love")
    m.write_vocab("u1", "ishq", "love")
    row = next(v for v in m.recall_vocab("u1") if v["word"] == "ishq")
    assert row["times_used"] == 2


def test_profile_set_and_get(tmp_path):
    m = MemoryStore(str(tmp_path / "m.db"))
    m.set_profile("u1", name="Lamaq", urdu_density=0.5)
    prof = m.get_profile("u1")
    assert prof["name"] == "Lamaq"
    assert abs(prof["urdu_density"] - 0.5) < 1e-6


def test_recall_scoped_per_user(tmp_path):
    m = MemoryStore(str(tmp_path / "m.db"))
    m.write_vocab("a", "alif", "first letter")
    assert m.recall_vocab("b") == []
