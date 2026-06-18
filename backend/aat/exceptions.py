"""Specific exceptions (never raise/catch bare)."""

from __future__ import annotations


class AatError(Exception):
    """Base class for all Alif Aur Tarana errors."""


class MissingKeyError(AatError):
    """A provider was used without its API key configured."""


class ProviderDownError(AatError):
    """A provider failed transiently (network/5xx) and a fallback should be tried."""


class RateLimitError(ProviderDownError):
    """A provider rejected the request due to rate/quota limits."""


class AllProvidersExhausted(AatError):
    """Every provider in a router's policy failed."""
