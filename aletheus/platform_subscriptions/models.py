from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Subscription:

    event_type: str
    subscriber: str
    callback: callable

    def to_dict(self):

        return {
            "event_type": self.event_type,
            "subscriber": self.subscriber,
        }
