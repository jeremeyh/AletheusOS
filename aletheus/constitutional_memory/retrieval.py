from __future__ import annotations

from .registry import ConstitutionalMemoryRegistry


class ConstitutionalMemoryRetrieval:
    GENESIS = "19.5"
    VERSION = "0.1.0"

    def __init__(self, registry: ConstitutionalMemoryRegistry):
        self.registry = registry

    def get(self, memory_id: str):
        record = self.registry.get(memory_id)
        return record.to_dict() if record else None

    def by_trace(self, decision_trace_id: str):
        record = self.registry.by_trace(decision_trace_id)
        return record.to_dict() if record else None

    def by_certification(self, certification_id: str):
        record = self.registry.by_certification(certification_id)
        return record.to_dict() if record else None

    def by_application(self, application: str):
        return [
            record.to_dict() for record in self.registry.by_application(application)
        ]

    def all(self):
        return self.registry.list()
