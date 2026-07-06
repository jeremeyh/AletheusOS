from __future__ import annotations

from .core import intent_engine


def health() -> dict:
    return intent_engine.health()
