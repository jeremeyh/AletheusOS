from __future__ import annotations

from .core import foundation_service_bus


def health() -> dict:
    return foundation_service_bus.health()
