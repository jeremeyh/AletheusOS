from __future__ import annotations

from .models import LedgerEntry


class ConstitutionalLedgerRegistry:
    GENESIS = "19.4"
    VERSION = "0.1.0"

    def __init__(self):
        self._entries: dict[str, LedgerEntry] = {}
        self._by_trace: dict[str, list[str]] = {}
        self._by_certification: dict[str, str] = {}
        self._by_application: dict[str, list[str]] = {}

    def append(self, entry: LedgerEntry):
        if entry.ledger_id in self._entries:
            raise ValueError(f"Ledger entry already exists: {entry.ledger_id}")

        self._entries[entry.ledger_id] = entry

        self._by_trace.setdefault(entry.decision_trace_id, []).append(entry.ledger_id)
        self._by_certification[entry.certification_id] = entry.ledger_id
        self._by_application.setdefault(entry.application, []).append(entry.ledger_id)

        return entry

    def get(self, ledger_id: str):
        return self._entries.get(ledger_id)

    def by_trace(self, decision_trace_id: str):
        return [
            self._entries[ledger_id]
            for ledger_id in self._by_trace.get(decision_trace_id, [])
        ]

    def by_certification(self, certification_id: str):
        ledger_id = self._by_certification.get(certification_id)
        return self._entries.get(ledger_id) if ledger_id else None

    def by_application(self, application: str):
        return [
            self._entries[ledger_id]
            for ledger_id in self._by_application.get(application, [])
        ]

    def list(self):
        return [entry.to_dict() for entry in self._entries.values()]

    def count(self):
        return len(self._entries)

    def statistics(self):
        return {
            "entries": self.count(),
            "decision_traces": len(self._by_trace),
            "certifications": len(self._by_certification),
            "applications": sorted(self._by_application.keys()),
        }
