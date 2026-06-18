"""Ping every configured service once and report readiness.

Run: `uv run python check_keys.py`  (from backend/, with .env filled).
Safe to run anytime — it makes one tiny call per service and never prints secrets.
"""

from __future__ import annotations

import logging

import httpx

from aat.config import Settings, get_settings

logging.basicConfig(level=logging.WARNING)


def check_gemini(s: Settings) -> str:
    if not s.gemini_api_key:
        return "- no key"
    try:
        from google import genai

        client = genai.Client(api_key=s.gemini_api_key)
        resp = client.models.generate_content(model=s.gemini_model, contents="Reply with: pong")
        return f"OK ({(resp.text or '').strip()[:24]!r})"
    except Exception as exc:  # noqa: BLE001 - report any failure plainly
        return f"FAIL: {exc}"


def check_elevenlabs(s: Settings) -> str:
    if not s.elevenlabs_api_key:
        return "- no key"
    try:
        from elevenlabs.client import ElevenLabs

        client = ElevenLabs(api_key=s.elevenlabs_api_key)
        voices = client.voices.get_all()
        count = len(getattr(voices, "voices", []) or [])
        return f"OK ({count} voices in library)"
    except Exception as exc:  # noqa: BLE001
        return f"FAIL: {exc}"


def check_groq(s: Settings) -> str:
    if not s.groq_api_key:
        return "- no key"
    try:
        from groq import Groq

        client = Groq(api_key=s.groq_api_key)
        models = client.models.list()
        return f"OK ({len(models.data)} models)"
    except Exception as exc:  # noqa: BLE001
        return f"FAIL: {exc}"


def check_tavily(s: Settings) -> str:
    if not s.tavily_api_key:
        return "- no key"
    try:
        resp = httpx.post(
            "https://api.tavily.com/search",
            json={"query": "ping", "max_results": 1},
            headers={"Authorization": f"Bearer {s.tavily_api_key}"},
            timeout=20,
        )
        resp.raise_for_status()
        return f"OK ({len(resp.json().get('results', []))} results)"
    except Exception as exc:  # noqa: BLE001
        return f"FAIL: {exc}"


def main() -> None:
    s = get_settings()
    print("Alif Aur Tarana - service readiness")
    print("=" * 44)
    rows = [
        ("Gemini (brain)", check_gemini(s)),
        ("ElevenLabs (voice)", check_elevenlabs(s)),
        ("Groq (fallback)", check_groq(s)),
        ("Tavily (search)", check_tavily(s)),
        ("Sarvam (STT)", "key present (live check at T2)" if s.sarvam_api_key else "- no key (needed for T2)"),
    ]
    for name, res in rows:
        print(f"{name:<22} {res}")
    print("-" * 44)
    print(f"{'Alif voice id':<22} {'set' if s.alif_voice_id else '- MISSING (Voice Design)'}")
    print(f"{'Tarana voice id':<22} {'set' if s.tarana_voice_id else '- MISSING (Voice Design)'}")


if __name__ == "__main__":
    main()
