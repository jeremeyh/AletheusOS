from __future__ import annotations

from collections.abc import Callable

from aletheus.platform_subscriptions import platform_subscriptions

from .models import PlatformEvent


class PlatformEventEngine:
    GENESIS = "15.5"
    VERSION = "0.2.0"

    def __init__(self):
        self._events: list[PlatformEvent] = []
        self._subscribers: list[Callable[[PlatformEvent], None]] = []

    def publish(self, event_type: str, source: str, payload: dict | None = None):
        event = PlatformEvent(
            event_type=event_type,
            source=source,
            payload=payload or {},
        )

        event_dict = event.to_dict()

        self._events.append(event)

        dispatch_result = platform_subscriptions.dispatch(event_dict)

        return {
            "event": event_dict,
            "dispatch": dispatch_result,
        }

    def subscribe(self, callback: Callable[[PlatformEvent], None]):
        self._subscribers.append(callback)
        return {
            "subscribers": len(self._subscribers),
        }

    def history(self):
        return [event.to_dict() for event in self._events]

    def health(self):
        return {
            "name": "Platform Event Engine",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "events": len(self._events),
            "subscribers": len(self._subscribers),
        }

    def statistics(self):
        return {
            "events": len(self._events),
            "subscribers": len(self._subscribers),
        }


platform_events = PlatformEventEngine()
