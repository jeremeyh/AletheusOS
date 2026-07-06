from __future__ import annotations

from aletheus.platform_events import platform_events


class EventClient:
    def __init__(self, app):
        self.app = app
        self._handlers: dict[str, list] = {}

    def on(self, event_type: str):
        def decorator(func):
            self._handlers.setdefault(event_type, []).append(func)
            return func

        return decorator

    def emit(self, event_type: str, payload: dict):
        event = platform_events.publish(
            event_type,
            source=self.app.name,
            payload=payload,
        )

        for handler in self._handlers.get(event_type, []):
            handler(event)

        return event
