from __future__ import annotations

from .core import foundation_service_bus


def statistics() -> dict:
    return foundation_service_bus.statistics()
