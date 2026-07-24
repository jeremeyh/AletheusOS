from __future__ import annotations

from .institutional_event_store import InstitutionalEventStore
from .institutional_events import (
    InstitutionalLedgerEvent,
    new_institutional_event_id,
)
from .persistence import constitutional_ledger_persistence
from .recorder import ConstitutionalLedgerRecorder
from .registry import ConstitutionalLedgerRegistry
from .retrieval import ConstitutionalLedgerRetrieval
from .search import ConstitutionalLedgerSearch
from .transtemporal import TranstemporalEngine


class ConstitutionalLedger:
    GENESIS = "19.4"
    VERSION = "0.1.0"

    def __init__(self):
        #
        # Decision Ledger
        #
        self.registry = ConstitutionalLedgerRegistry()
        self.recorder = ConstitutionalLedgerRecorder(self.registry)
        self.retrieval = ConstitutionalLedgerRetrieval(self.registry)
        self.searcher = ConstitutionalLedgerSearch(self.registry)
        self.persistence = constitutional_ledger_persistence

        #
        # Institutional Event Ledger
        #
        self.institutional_events = InstitutionalEventStore()
        self.transtemporal = TranstemporalEngine(
            self.institutional_events
        )

        #
        # Legacy compatibility alias
        #
        self.time_travel = self.transtemporal

        self._replays = 0

    #
    # ------------------------------------------------------------------
    # Decision Ledger API
    # ------------------------------------------------------------------
    #

    def record(self, **kwargs):
        return self.recorder.record(**kwargs)

    def get(self, ledger_id: str):
        return self.retrieval.get(ledger_id)

    def by_trace(self, decision_trace_id: str):
        return self.retrieval.by_trace(decision_trace_id)

    def by_certification(self, certification_id: str):
        return self.retrieval.by_certification(
            certification_id
        )

    def by_application(self, application: str):
        return self.retrieval.by_application(application)

    def search(self, query: str):
        return self.searcher.search(query)

    def replay(self, decision_trace_id: str):
        self._replays += 1

        return {
            "decision_trace_id": decision_trace_id,
            "entries": self.by_trace(
                decision_trace_id
            ),
        }

    #
    # ------------------------------------------------------------------
    # Institutional Event Ledger API
    # ------------------------------------------------------------------
    #

    def record_event(self, event: dict):
        normalized = dict(event)

        source_identity = (
            normalized.pop("source_identity", None)
            or normalized.pop("source", None)
            or "unknown"
        )

        effective_at = (
            normalized.pop("effective_at", None)
            or normalized.pop("timestamp", None)
        )

        ledger_event = InstitutionalLedgerEvent(
            event_id=normalized.pop(
                "event_id",
                new_institutional_event_id(),
            ),
            event_type=normalized.pop(
                "event_type",
                "UnknownEvent",
            ),
            source_identity=source_identity,
            effective_at=effective_at,
            payload=normalized.pop(
                "payload",
                {},
            ),
            evidence=tuple(
                normalized.pop(
                    "evidence",
                    (),
                )
            ),
            tags=tuple(
                normalized.pop(
                    "tags",
                    (),
                )
            ),
            correlation_id=normalized.pop(
                "correlation_id",
                None,
            ),
            causation_id=normalized.pop(
                "causation_id",
                None,
            ),
            supersedes=normalized.pop(
                "supersedes",
                None,
            ),
            certified=normalized.pop(
                "certified",
                False,
            ),
            constitution_version=normalized.pop(
                "constitution_version",
                "0.1.0",
            ),
            genesis_version=normalized.pop(
                "genesis_version",
                "12",
            ),
        )

        return self.institutional_events.append(
            ledger_event
        )

    def institutional_event(
        self,
        event_id: str,
    ):
        """
        Return a single institutional event.
        """
        return self.institutional_events.get(
            event_id
        )

    def institutional_history(
        self,
        source_identity: str | None = None,
        *,
        event_type: str | None = None,
        correlation_id: str | None = None,
    ):
        """
        Legacy compatibility API.

        Return institutional events in recorded order.

        Supported filters:
          - source_identity
          - event_type
          - correlation_id

        With no filters, returns the complete history.
        """

        if correlation_id is not None:
            return self.institutional_events.by_correlation(
                correlation_id
            )

        if source_identity is not None:
            return self.institutional_events.by_source(
                source_identity
            )

        if event_type is not None:
            return self.institutional_events.by_type(
                event_type
            )

        return self.institutional_events.all()

    def replay_events(
        self,
        *,
        correlation_id: str | None = None,
        source_identity: str | None = None,
    ):
        self._replays += 1

        return self.transtemporal.replay(
            correlation_id=correlation_id,
            source_identity=source_identity,
        )

    def temporal_search(
        self,
        query: str,
        *,
        source_identity: str | None = None,
        event_type: str | None = None,
    ):
        return self.transtemporal.search(
            query,
            source_identity=source_identity,
            event_type=event_type,
        )

    def temporal_lineage(
        self,
        event_id: str,
    ):
        return self.transtemporal.lineage(
            event_id
        )

    def temporal_provenance(
        self,
        event_id: str,
    ):
        return self.transtemporal.provenance(
            event_id
        )

    def as_of(
        self,
        timestamp: str,
        *,
        source_identity: str | None = None,
    ):
        return self.transtemporal.snapshot(
            timestamp,
            source_identity=source_identity,
        )

    def compare_time(
        self,
        before: str,
        after: str,
        *,
        source_identity: str | None = None,
    ):
        return self.transtemporal.compare(
            before,
            after,
            source_identity=source_identity,
        )

    #
    # ------------------------------------------------------------------
    #

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
            "institutional_events": len(
                self.institutional_events.all()
            ),
            "replays": self._replays,
        }

    def statistics(self):
        return {
            "name": "Constitutional Ledger",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "replays": self._replays,
            **self.registry.statistics(),
            **self.institutional_events.statistics(),
        }


constitutional_ledger = ConstitutionalLedger()
