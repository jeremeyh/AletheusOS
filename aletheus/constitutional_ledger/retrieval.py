from __future__ import annotations

from .registry import ConstitutionalLedgerRegistry


class ConstitutionalLedgerRetrieval:
    GENESIS = "19.4"
    VERSION = "0.1.0"

    def __init__(self, registry: ConstitutionalLedgerRegistry):
        self.registry = registry

    def get(self, ledger_id: str):
        entry = self.registry.get(ledger_id)
        return entry.to_dict() if entry else None

    def by_trace(self, decision_trace_id: str):
        return [
            entry.to_dict()
            for entry in self.registry.by_trace(decision_trace_id)
        ]

    def by_certification(self, certification_id: str):
        entry = self.registry.by_certification(certification_id)
        return entry.to_dict() if entry else None

    def by_application(self, application: str):
        return [
            entry.to_dict()
            for entry in self.registry.by_application(application)
        ]

    def all(self):
        return self.registry.list()
