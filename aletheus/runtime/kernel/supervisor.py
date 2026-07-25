from __future__ import annotations

from typing import Any

from aletheus.time_utils import utc_now, utc_now_iso


def utc_now() -> str:
    return utc_now_iso()


class IntelligenceSupervisor:
    VERSION = "4.0.0"

    def __init__(self) -> None:
        self.health_events: list[dict[str, Any]] = []

    def check(self, runtime: Any) -> dict[str, Any]:
        event = {
            "timestamp": utc_now(),
            "runtime_version": getattr(runtime, "version", "unknown"),
            "status": getattr(runtime, "status", "unknown"),
            "health": "healthy",
        }

        self.health_events.append(event)
        return event

    def statistics(self) -> dict[str, Any]:
        return {
            "version": self.VERSION,
            "health_events": len(self.health_events),
            "health": "healthy",
        }


intelligence_supervisor = IntelligenceSupervisor()
