"""
Compatibility interface for the former Time Travel™ engine name.

Canonical engine:
    Transtemporal Engine™

`TimeTravel` remains available temporarily so existing imports and callers
continue to function during constitutional migration.
"""

from __future__ import annotations

from .transtemporal import (
    TemporalDifference,
    TemporalSnapshot,
    TranstemporalEngine,
)


class TimeTravel(TranstemporalEngine):
    """
    Deprecated compatibility alias for TranstemporalEngine.

    Prefer:
        TranstemporalEngine
    """


__all__ = [
    "TemporalDifference",
    "TemporalSnapshot",
    "TimeTravel",
    "TranstemporalEngine",
]
