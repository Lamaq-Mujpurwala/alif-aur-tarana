"""Local poetry corpus loader + lookup (docs/04 §1).

Backs the `rekhta.lookup` tool. Rekhta has no public API, so we use a local, curated
corpus (open datasets + hand-picked couplets), always crediting Rekhta Foundation.
"""

from __future__ import annotations

import json
import logging
from functools import lru_cache
from pathlib import Path

logger = logging.getLogger(__name__)

# apps/api/aat/content/corpus.py -> repo root is parents[3]
_DEFAULT_CORPUS = Path(__file__).resolve().parents[3] / "data" / "corpus" / "seed.json"


@lru_cache(maxsize=1)
def _load(path: str) -> list[dict]:
    p = Path(path)
    if not p.exists():
        logger.warning("corpus file not found at %s; returning empty corpus", p)
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    return data.get("couplets", [])


def lookup(
    query: str = "",
    *,
    poet: str | None = None,
    theme: str | None = None,
    limit: int = 3,
    corpus_path: str | Path = _DEFAULT_CORPUS,
) -> list[dict]:
    """Return up to `limit` couplets matching the query/poet/theme (simple scoring)."""
    couplets = _load(str(corpus_path))
    q = query.lower().strip()
    poet_l = (poet or "").lower().strip()
    theme_l = (theme or "").lower().strip()

    scored: list[tuple[int, dict]] = []
    for c in couplets:
        score = 0
        if poet_l and poet_l in c.get("poet", "").lower():
            score += 5
        if theme_l and theme_l in [t.lower() for t in c.get("theme", [])]:
            score += 3
        if q:
            haystack = " ".join(
                [c.get("roman", ""), c.get("gloss", ""), c.get("poet", "")]
            ).lower()
            score += sum(1 for tok in q.split() if tok in haystack)
        elif not poet_l and not theme_l:
            score = 1  # no filters: include everything
        if score > 0:
            scored.append((score, c))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [c for _score, c in scored[:limit]]
