from __future__ import annotations

from .models import SupervisorObservation


class RuntimeSupervisorMonitor:
    GENESIS = "16.1"
    VERSION = "0.1.0"

    def observe(self, event) -> SupervisorObservation:

        return SupervisorObservation(
            event_type=event.get("event_type", "unknown"),
            source=event.get("source", "unknown"),
            severity=event.get("payload", {}).get("severity", "info"),
            message=event.get("payload", {}).get("message", ""),
            payload=event.get("payload", {}),
        )


runtime_supervisor_monitor = RuntimeSupervisorMonitor()
