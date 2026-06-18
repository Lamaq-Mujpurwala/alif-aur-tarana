"""Tests for the LLM and TTS fallback routers + TTS caching (offline, fakes)."""

from __future__ import annotations

import pytest

from aat.config import Settings
from aat.exceptions import AllProvidersExhausted, ProviderDownError
from aat.llm.base import LLMMessage
from aat.llm.router import LLMRouter
from aat.tts.cache import AudioCache
from aat.tts.router import TTSRouter


def _settings() -> Settings:
    return Settings(_env_file=None)  # don't read the real .env in tests


# --------------------------------------------------------------------------- #
# LLM router
# --------------------------------------------------------------------------- #
class FakeLLM:
    def __init__(self, name, *, fail=False, available=True, text="ok"):
        self.name = name
        self._fail = fail
        self._available = available
        self._text = text
        self.calls = 0

    def available(self, settings) -> bool:
        return self._available

    async def complete(self, messages, *, system, json_mode=False) -> str:
        self.calls += 1
        if self._fail:
            raise ProviderDownError("boom")
        return self._text


async def test_llm_falls_back_to_next_provider():
    bad, good = FakeLLM("bad", fail=True), FakeLLM("good", text="hi")
    out = await LLMRouter([bad, good], _settings()).complete(
        [LLMMessage(role="user", content="x")], system="s"
    )
    assert out == "hi"
    assert bad.calls == 1 and good.calls == 1


async def test_llm_raises_when_all_fail():
    with pytest.raises(AllProvidersExhausted):
        await LLMRouter([FakeLLM("a", fail=True)], _settings()).complete(
            [LLMMessage(role="user", content="x")], system="s"
        )


async def test_llm_raises_when_none_available():
    with pytest.raises(AllProvidersExhausted):
        await LLMRouter([FakeLLM("a", available=False)], _settings()).complete(
            [LLMMessage(role="user", content="x")], system="s"
        )


async def test_llm_prefer_tries_named_provider_first():
    a, b = FakeLLM("a", text="A"), FakeLLM("b", text="B")
    out = await LLMRouter([a, b], _settings()).complete(
        [LLMMessage(role="user", content="x")], system="s", prefer="b"
    )
    assert out == "B" and b.calls == 1 and a.calls == 0


# --------------------------------------------------------------------------- #
# TTS router + cache
# --------------------------------------------------------------------------- #
class FakeTTS:
    def __init__(self, name, *, emotion=True, available=True, fail=False):
        self.name = name
        self.supports_emotion = emotion
        self._available = available
        self._fail = fail
        self.calls = 0

    def available(self, settings) -> bool:
        return self._available

    async def synthesize(self, text, *, voice_id, stability="natural",
                         language_code="ur", seed=None) -> bytes:
        self.calls += 1
        if self._fail:
            raise ProviderDownError("boom")
        return b"AUDIO:" + text.encode("utf-8")


async def test_tts_cache_hit_avoids_second_call(tmp_path):
    p = FakeTTS("eleven")
    router = TTSRouter([p], _settings(), cache=AudioCache(str(tmp_path / "c")))
    a1 = await router.synthesize("salaam", voice_id="v")
    a2 = await router.synthesize("salaam", voice_id="v")
    assert a1 == a2
    assert p.calls == 1  # second served from cache


async def test_tts_falls_back_on_failure(tmp_path):
    bad, good = FakeTTS("bad", fail=True), FakeTTS("good")
    out = await TTSRouter([bad, good], _settings(), cache=None).synthesize("hi", voice_id="v")
    assert out.startswith(b"AUDIO:") and bad.calls == 1 and good.calls == 1


async def test_tts_prefers_emotion_capable_provider(tmp_path):
    plain, emo = FakeTTS("azure", emotion=False), FakeTTS("eleven", emotion=True)
    await TTSRouter([plain, emo], _settings(), cache=None).synthesize(
        "hi", voice_id="v", needs_emotion=True
    )
    assert emo.calls == 1 and plain.calls == 0
