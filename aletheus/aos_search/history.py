from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


def _timestamp() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class SearchHistoryEntry:
    query: str
    intent: str
    plan: str
    timestamp: str = field(default_factory=_timestamp)
    metadata: dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "query": self.query,
            "intent": self.intent,
            "plan": self.plan,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }


class SearchHistory:
    GENESIS = "21.8.3"
    VERSION = "1.0.0"

    def __init__(self):
        self._history: list[SearchHistoryEntry] = []

    def record(
        self,
        query: str,
        intent: str,
        plan: str,
        metadata: dict | None = None,
    ) -> None:

        self._history.append(
            SearchHistoryEntry(
                query=query,
                intent=intent,
                plan=plan,
                metadata=metadata or {},
            )
        )

    def history(self) -> list[SearchHistoryEntry]:
        return list(self._history)

    def clear(self) -> None:
        self._history.clear()

    def statistics(self) -> dict:
        return {
            "queries": len(self._history),
            "genesis": self.GENESIS,
            "version": self.VERSION,
        }


search_history = SearchHistory()
