from __future__ import annotations

from .models import MemoryRecord


class ConstitutionalMemoryRegistry:
    GENESIS = "19.5"
    VERSION = "0.1.0"

    def __init__(self):
        self._records: dict[str, MemoryRecord] = {}
        self._by_trace: dict[str, str] = {}
        self._by_certification: dict[str, str] = {}
        self._by_application: dict[str, list[str]] = {}

    def add(self, record: MemoryRecord):
        self._records[record.memory_id] = record
        self._by_trace[record.decision_trace_id] = record.memory_id
        self._by_certification[record.certification_id] = record.memory_id
        self._by_application.setdefault(record.application, []).append(record.memory_id)
        return record

    def get(self, memory_id: str):
        return self._records.get(memory_id)

    def by_trace(self, decision_trace_id: str):
        memory_id = self._by_trace.get(decision_trace_id)
        return self._records.get(memory_id) if memory_id else None

    def by_certification(self, certification_id: str):
        memory_id = self._by_certification.get(certification_id)
        return self._records.get(memory_id) if memory_id else None

    def by_application(self, application: str):
        return [
            self._records[memory_id]
            for memory_id in self._by_application.get(application, [])
        ]

    def list(self):
        return [record.to_dict() for record in self._records.values()]

    def count(self):
        return len(self._records)

    def statistics(self):
        return {
            "records": self.count(),
            "applications": sorted(self._by_application.keys()),
            "decision_traces": len(self._by_trace),
            "certifications": len(self._by_certification),
        }
