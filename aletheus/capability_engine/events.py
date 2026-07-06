from __future__ import annotations


class CapabilityEventBus:
    """
    Lightweight event recorder for Capability Engine events.

    This will later connect to the full AletheusOS platform event bus.
    """

    GENESIS = "21.6"
    VERSION = "1.0.0"

    def __init__(self):
        self._events: list[dict] = []

    def publish(
        self,
        event_type: str,
        payload: dict | None = None,
    ):
        event = {
            "event_type": event_type,
            "payload": payload or {},
        }

        self._events.append(event)
        return event

    def all(self):
        return list(self._events)

    def statistics(self):
        return {
            "events": len(self._events),
            "genesis": self.GENESIS,
            "version": self.VERSION,
        }

    def health(self):
        return {
            "status": "healthy",
            **self.statistics(),
        }


capability_events = CapabilityEventBus()
