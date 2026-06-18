"""Local SQLite memory — 'it remembers us' without any infra (docs/04 §4).

MVP-grade: a single file DB. Swap for mem0 / Postgres+pgvector later without changing
the tool interface. Stores the user profile, learned vocabulary, and pronunciation
progress so the companions can re-surface words and notice growth.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

_SCHEMA = """
CREATE TABLE IF NOT EXISTS profile (
    user_id TEXT PRIMARY KEY,
    name TEXT,
    urdu_density REAL DEFAULT 0.35,
    preferred_companion TEXT,
    updated_at TEXT
);
CREATE TABLE IF NOT EXISTS learned_vocab (
    user_id TEXT,
    word TEXT,
    gloss TEXT,
    first_seen TEXT,
    last_surfaced TEXT,
    times_used INTEGER DEFAULT 1,
    PRIMARY KEY (user_id, word)
);
CREATE TABLE IF NOT EXISTS pron_progress (
    user_id TEXT,
    sound TEXT,
    status TEXT,
    notes TEXT,
    last_practiced TEXT,
    PRIMARY KEY (user_id, sound)
);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class MemoryStore:
    """Thin, synchronous SQLite wrapper (calls are fast; wrap in to_thread if needed)."""

    def __init__(self, db_path: Path | str = "aat.db") -> None:
        self._path = str(db_path)
        self._conn = sqlite3.connect(self._path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    # ---- profile ----
    def get_profile(self, user_id: str) -> dict | None:
        row = self._conn.execute(
            "SELECT * FROM profile WHERE user_id = ?", (user_id,)
        ).fetchone()
        return dict(row) if row else None

    def set_profile(self, user_id: str, **fields: object) -> None:
        current = self.get_profile(user_id) or {"user_id": user_id, "urdu_density": 0.35}
        current.update(fields)
        self._conn.execute(
            """INSERT INTO profile (user_id, name, urdu_density, preferred_companion, updated_at)
               VALUES (:user_id, :name, :urdu_density, :preferred_companion, :updated_at)
               ON CONFLICT(user_id) DO UPDATE SET
                 name=excluded.name, urdu_density=excluded.urdu_density,
                 preferred_companion=excluded.preferred_companion, updated_at=excluded.updated_at""",
            {
                "user_id": user_id,
                "name": current.get("name"),
                "urdu_density": current.get("urdu_density", 0.35),
                "preferred_companion": current.get("preferred_companion"),
                "updated_at": _now(),
            },
        )
        self._conn.commit()

    # ---- vocabulary ----
    def write_vocab(self, user_id: str, word: str, gloss: str) -> None:
        now = _now()
        self._conn.execute(
            """INSERT INTO learned_vocab (user_id, word, gloss, first_seen, last_surfaced)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(user_id, word) DO UPDATE SET
                 last_surfaced=excluded.last_surfaced,
                 times_used = learned_vocab.times_used + 1""",
            (user_id, word, gloss, now, now),
        )
        self._conn.commit()

    def recall_vocab(self, user_id: str, limit: int = 10) -> list[dict]:
        rows = self._conn.execute(
            "SELECT word, gloss, times_used FROM learned_vocab WHERE user_id = ? "
            "ORDER BY last_surfaced DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
        return [dict(r) for r in rows]

    def close(self) -> None:
        self._conn.close()
