from __future__ import annotations

from .models import ExecutiveIntent


class IntentQueue:
    GENESIS = "7.2"
    VERSION = "0.1.0"

    def __init__(self):
        self._intents: list[ExecutiveIntent] = []

    def add(self, intent: ExecutiveIntent):
        self._intents.append(intent)
        self._intents.sort(key=lambda item: item.priority, reverse=True)
        return intent

    def list(self):
        return list(self._intents)

    def next(self):
        return self._intents[0] if self._intents else None

    def count(self):
        return len(self._intents)

    def health(self):
        return {
            "name": "Intent Queue",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "intents": self.count(),
        }
