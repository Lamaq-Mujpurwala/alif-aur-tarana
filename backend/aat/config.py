"""Central configuration, loaded from environment / .env.

All secrets come from the environment (never hardcoded). Missing keys are allowed
so the app can boot and report readiness via `check_keys.py`; individual providers
raise a clear error only when actually used without a key.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings sourced from `.env` / environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # ---- Tier 1 (required for the live cascade) ----
    gemini_api_key: str | None = Field(default=None, alias="GEMINI_API_KEY")
    elevenlabs_api_key: str | None = Field(default=None, alias="ELEVENLABS_API_KEY")
    alif_voice_id: str | None = Field(default=None, alias="ALIF_VOICE_ID")
    tarana_voice_id: str | None = Field(default=None, alias="TARANA_VOICE_ID")
    sarvam_api_key: str | None = Field(default=None, alias="SARVAM_API_KEY")

    # ---- Tier 2 (fallbacks / tools) ----
    groq_api_key: str | None = Field(default=None, alias="GROQ_API_KEY")
    tavily_api_key: str | None = Field(default=None, alias="TAVILY_API_KEY")
    azure_speech_key: str | None = Field(default=None, alias="AZURE_SPEECH_KEY")
    azure_speech_region: str | None = Field(default=None, alias="AZURE_SPEECH_REGION")

    # ---- local services ----
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    whisper_model: str = Field(default="large-v3", alias="WHISPER_MODEL")

    # ---- model selection ----
    gemini_model: str = Field(default="gemini-2.5-flash", alias="GEMINI_MODEL")
    elevenlabs_model: str = Field(default="eleven_v3", alias="ELEVENLABS_MODEL")

    # ---- per-companion TTS seeds (pin for consistency; docs/15 §1) ----
    alif_seed: int = Field(default=101, alias="ALIF_SEED")
    tarana_seed: int = Field(default=202, alias="TARANA_SEED")

    def has(self, *keys: str) -> bool:
        """True if every named setting attribute is set (non-empty)."""
        return all(bool(getattr(self, k, None)) for k in keys)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
