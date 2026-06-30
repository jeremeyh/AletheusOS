from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List
import uuid

@dataclass
class RuntimeEvent:
    event_type: str
    payload: Dict[str, Any]
    source: str = "system"
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    def to_dict(self) -> Dict[str, Any]: return {"event_id": self.event_id, "event_type": self.event_type, "source": self.source, "payload": self.payload, "created_at": self.created_at}

class EventBus:
    def __init__(self) -> None:
        self.events: List[RuntimeEvent] = []
        self.subscribers: Dict[str, List[Callable[[RuntimeEvent], None]]] = {}
    def publish(self, event_type: str, payload: Dict[str, Any], source: str = "system") -> RuntimeEvent:
        event = RuntimeEvent(event_type=event_type, payload=payload, source=source)
        self.events.append(event)
        for handler in self.subscribers.get(event_type, []): handler(event)
        for handler in self.subscribers.get('*', []): handler(event)
        return event
    def subscribe(self, event_type: str, handler: Callable[[RuntimeEvent], None]) -> None: self.subscribers.setdefault(event_type, []).append(handler)
    def recent(self, limit: int = 100) -> List[Dict[str, Any]]: return [event.to_dict() for event in self.events[-limit:]]
    def count(self) -> int: return len(self.events)
