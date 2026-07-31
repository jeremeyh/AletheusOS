from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from typing import Any

from aletheus.time_utils import utc_now, utc_now_iso


def utc_now():
    return utc_now_iso()


@dataclass
class Event:
    event_id: str
    topic: str
    payload: dict[str, Any]

    publisher: str = "runtime"

    timestamp: str = field(default_factory=utc_now)

    priority: str = "normal"

    metadata: dict[str, Any] = field(default_factory=dict)


class AletheusEventBus:
    VERSION = "3.3.0"

    def __init__(self):

        self.subscribers: dict[str, list[str]] = {}

        self.events: list[Event] = []

        self.dead_letter_queue: list[Event] = []

    @property
    def version(self):
        return self.VERSION

    # -----------------------------------------------------

    def bootstrap(self):

        return self.statistics()

    # -----------------------------------------------------

    def publish(
        self,
        topic,
        payload,
        publisher="runtime",
        priority="normal",
        source=None,
        **kwargs,
    ):

        event = Event(
            event_id=str(uuid.uuid4()),
            topic=topic,
            payload=payload,
            publisher=publisher,
            priority=priority,
        )

        self.events.append(event)

        return asdict(event)

    # -----------------------------------------------------

    def subscribe(self, topic, subscriber):

        self.subscribers.setdefault(topic, [])

        if subscriber not in self.subscribers[topic]:
            self.subscribers[topic].append(subscriber)

        return {
            "topic": topic,
            "subscriber": subscriber,
            "subscriber_count": len(self.subscribers[topic]),
        }

    # -----------------------------------------------------

    def unsubscribe(self, topic, subscriber):

        if topic in self.subscribers:
            if subscriber in self.subscribers[topic]:
                self.subscribers[topic].remove(subscriber)

        return {
            "topic": topic,
            "subscriber": subscriber,
        }

    # -----------------------------------------------------

    def history(self, topic=None):

        if topic:
            return [asdict(event) for event in self.events if event.topic == topic]

        return [asdict(event) for event in self.events]

    # -----------------------------------------------------

    def replay(self, topic):

        return {
            "topic": topic,
            "events": self.history(topic),
        }

    # -----------------------------------------------------

    def statistics(self):

        return {
            "version": self.VERSION,
            "events": len(self.events),
            "topics": len(self.subscribers),
            "subscribers": sum(len(v) for v in self.subscribers.values()),
            "dead_letters": len(self.dead_letter_queue),
            "health": "healthy",
        }


event_bus_core = AletheusEventBus()
