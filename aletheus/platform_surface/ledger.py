"""Public Constitutional Ledger Surface."""

from __future__ import annotations


class LedgerSurface:
    """Stable read interface over Ledger and Transtemporal capabilities."""

    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        ledger,
    ) -> None:
        self._ledger = ledger

    def history(
        self,
        *,
        correlation_id: str,
    ):
        return self._ledger.replay_events(correlation_id=correlation_id)

    def lineage(
        self,
        event_id: str,
    ):
        return self._ledger.temporal_lineage(event_id)

    def provenance(
        self,
        event_id: str,
    ):
        return self._ledger.temporal_provenance(event_id)

    def statistics(self) -> dict:
        return self._ledger.statistics()

    def health(self) -> dict:
        return self._ledger.health()
