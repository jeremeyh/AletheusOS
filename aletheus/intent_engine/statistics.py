from __future__ import annotations

from .core import intent_engine


def statistics() -> dict:
    return intent_engine.statistics()
