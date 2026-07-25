import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TimelineEvent:
    subject_id: str
    event_type: str
    title: str
    detail: str = ""
    payload: dict = field(default_factory=dict)
    timeline_id: str = field(default_factory=lambda: f"TL-{uuid.uuid4().hex[:10].upper()}")
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

class IntelligenceTimelineService:
    """CardHawk OS™ 6.0C Intelligence Timeline™."""
    _events = []

    @classmethod
    def record(cls, subject_id, event_type, title, detail="", payload=None):
        event = TimelineEvent(subject_id, event_type, title, detail, payload or {})
        cls._events.append(event)
        return event

    @classmethod
    def for_subject(cls, subject_id):
        return [e for e in cls._events if str(e.subject_id) == str(subject_id)]

    @classmethod
    def latest(cls, limit=50):
        return cls._events[-limit:]
