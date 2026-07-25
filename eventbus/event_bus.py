import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CardHawkEvent:
    event_type: str
    message: str
    source: str = "CardHawk OS™"
    payload: dict = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: f"EVT-{uuid.uuid4().hex[:10].upper()}")
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

class EventBus:
    """Universal Event Bus™ for Alpha 1.0."""
    _events = []
    _subscribers = {}

    @classmethod
    def emit(cls, event_type, message, source="CardHawk OS™", payload=None):
        event = CardHawkEvent(event_type, message, source, payload or {})
        cls._events.append(event)
        for fn in cls._subscribers.get(event_type, []):
            try:
                fn(event)
            except Exception:
                pass
        return event

    @classmethod
    def subscribe(cls, event_type, handler):
        cls._subscribers.setdefault(event_type, []).append(handler)

    @classmethod
    def latest(cls, limit=50):
        return cls._events[-limit:]

    @classmethod
    def all(cls):
        return cls._events
