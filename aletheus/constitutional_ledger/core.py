from __future__ import annotations

from .persistence import constitutional_ledger_persistence
from .recorder import ConstitutionalLedgerRecorder
from .registry import ConstitutionalLedgerRegistry
from .retrieval import ConstitutionalLedgerRetrieval
from .search import ConstitutionalLedgerSearch


class ConstitutionalLedger:
    GENESIS = "19.4"
    VERSION = "0.1.0"

    def __init__(self):
        self.registry = ConstitutionalLedgerRegistry()
        self.recorder = ConstitutionalLedgerRecorder(self.registry)
        self.retrieval = ConstitutionalLedgerRetrieval(self.registry)
        self.searcher = ConstitutionalLedgerSearch(self.registry)
        self.persistence = constitutional_ledger_persistence
        self._replays = 0

    def record(self, **kwargs):
        return self.recorder.record(**kwargs)

    def get(self, ledger_id: str):
        return self.retrieval.get(ledger_id)

    def by_trace(self, decision_trace_id: str):
        return self.retrieval.by_trace(decision_trace_id)

    def by_certification(self, certification_id: str):
        return self.retrieval.by_certification(certification_id)

    def by_application(self, application: str):
        return self.retrieval.by_application(application)

    def search(self, query: str):
        return self.searcher.search(query)

    def replay(self, decision_trace_id: str):
        self._replays += 1

        return {
            "decision_trace_id": decision_trace_id,
            "entries": self.by_trace(decision_trace_id),
        }

    def save(self, path: str):
        return self.persistence.save(
            self.retrieval.all(),
            path,
        )

    def health(self):
        stats = self.registry.statistics()

        return {
            "name": "Constitutional Ledger",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "entries": stats["entries"],
            "certifications": stats["certifications"],
            "replays": self._replays,
        }

    def statistics(self):
        return {
            "name": "Constitutional Ledger",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "replays": self._replays,
            **self.registry.statistics(),
        }


constitutional_ledger = ConstitutionalLedger()
