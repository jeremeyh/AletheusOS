from __future__ import annotations

from .indexing import constitutional_memory_indexer
from .precedent import constitutional_precedent_engine
from .registry import ConstitutionalMemoryRegistry
from .retrieval import ConstitutionalMemoryRetrieval
from .similarity import constitutional_similarity_engine


class ConstitutionalMemory:
    GENESIS = "19.5"
    VERSION = "0.1.0"

    def __init__(self):
        self.registry = ConstitutionalMemoryRegistry()
        self.retrieval = ConstitutionalMemoryRetrieval(self.registry)
        self._recalls = 0
        self._similarity_searches = 0

    def index_ledger_entry(
        self,
        entry: dict,
        *,
        tags: list[str] | None = None,
        keywords: list[str] | None = None,
        entities: list[str] | None = None,
        precedent_weight: str = "LOW",
    ):
        record = constitutional_memory_indexer.from_ledger_entry(
            entry,
            tags=tags,
            keywords=keywords,
            entities=entities,
            precedent_weight=precedent_weight,
        )

        self.registry.add(record)

        return record.to_dict()

    def recall(self, query_terms: list[str], limit: int = 10):
        self._recalls += 1
        self._similarity_searches += 1

        return constitutional_similarity_engine.search(
            query_terms,
            self.retrieval.all(),
            limit=limit,
        )

    def strongest_precedent(self, application: str | None = None):
        records = (
            self.retrieval.by_application(application)
            if application
            else self.retrieval.all()
        )

        return constitutional_precedent_engine.strongest(records)

    def get(self, memory_id: str):
        return self.retrieval.get(memory_id)

    def by_trace(self, decision_trace_id: str):
        return self.retrieval.by_trace(decision_trace_id)

    def by_certification(self, certification_id: str):
        return self.retrieval.by_certification(certification_id)

    def health(self):
        stats = self.registry.statistics()

        return {
            "name": "Constitutional Memory",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "records": stats["records"],
            "precedents": len(
                constitutional_precedent_engine.filter_by_weight(
                    self.retrieval.all(),
                    minimum="LOW",
                )
            ),
            "recalls": self._recalls,
            "similarity_searches": self._similarity_searches,
        }

    def statistics(self):
        return {
            "name": "Constitutional Memory",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "recalls": self._recalls,
            "similarity_searches": self._similarity_searches,
            **self.registry.statistics(),
        }


constitutional_memory = ConstitutionalMemory()
