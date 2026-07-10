from __future__ import annotations

from datetime import datetime


class GovernanceHistory:

    VERSION = "1.0.0"


    def __init__(self):
        self.events = []


    def record(
        self,
        event_type: str,
        payload: dict,
    ):

        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event_type,
            "payload": payload,
        }

        self.events.append(event)

        return event


    def history(self):

        return {
            "version": self.VERSION,
            "count": len(self.events),
            "events": self.events,
        }
