from __future__ import annotations

from .models import ExecutiveIntent
from .queue import IntentQueue


class ExecutiveIntentEngine:
    """
    Executive Intent Engine™

    Converts platform observations into prioritized operational intent.
    """

    GENESIS = "7.2"
    VERSION = "0.1.0"

    def __init__(self):
        self.queue = IntentQueue()

    def issue(
        self,
        id: str,
        objective: str,
        priority: int,
        reason: str,
        source: str = "executive",
        metadata: dict | None = None,
    ):
        return self.queue.add(
            ExecutiveIntent(
                id=id,
                objective=objective,
                priority=priority,
                reason=reason,
                source=source,
                metadata=metadata or {},
            )
        )

    def health(self):
        return {
            "name": "Executive Intent Engine",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "queue": self.queue.health(),
        }

    def statistics(self):
        return {
            "intents": self.queue.count(),
            "next_intent": self.queue.next(),
        }


executive_intent_engine = ExecutiveIntentEngine()
