from __future__ import annotations

from aletheus.time_utils import utc_now, utc_now_iso

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
            "timestamp": utc_now_iso(),
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
