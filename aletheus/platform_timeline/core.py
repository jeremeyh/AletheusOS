from __future__ import annotations

from .models import TimelineEntry


class PlatformTimeline:
    GENESIS = "15.3"
    VERSION = "0.1.0"

    def __init__(self):
        self._entries: list[TimelineEntry] = []

    def record(
        self,
        event_type: str,
        source: str,
        message: str = "",
        payload: dict | None = None,
    ):
        entry = TimelineEntry(
            event_type=event_type,
            source=source,
            message=message,
            payload=payload or {},
        )

        self._entries.append(entry)

        return entry.to_dict()

    def entries(self):
        return [entry.to_dict() for entry in self._entries]

    def latest(self, limit: int = 10):
        return [entry.to_dict() for entry in self._entries[-limit:]]

    def clear(self):
        self._entries.clear()
        return {"cleared": True}

    def health(self):
        return {
            "name": "Platform Timeline",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "entries": len(self._entries),
        }

    def statistics(self):
        return {
            "entries": len(self._entries),
        }


platform_timeline = PlatformTimeline()
