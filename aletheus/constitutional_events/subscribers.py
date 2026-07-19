"""Canonical adapters for Constitutional Event Fabric subscribers."""

from __future__ import annotations

from typing import Any

from aletheus.constitutional_ledger import ConstitutionalLedger

from .models import ConstitutionalEvent


class LedgerEventSubscriber:
    """
    Records every constitutional event as authoritative institutional history.

    This connects Event Fabric directly to Ledger and Time Travel™.
    """

    def __init__(
        self,
        ledger: ConstitutionalLedger,
    ) -> None:
        self.ledger = ledger
        self.recorded = 0

    def handle(
        self,
        event: ConstitutionalEvent,
    ) -> dict[str, Any]:
        record = self.ledger.record_event(event.to_dict())
        self.recorded += 1
        return record.to_dict()

    def health(self) -> dict[str, Any]:
        return {
            "name": "Ledger Event Subscriber",
            "status": "online",
            "recorded": self.recorded,
        }


class EventCollector:
    """Simple inspectable subscriber useful for proofs and diagnostics."""

    def __init__(self) -> None:
        self.events: list[ConstitutionalEvent] = []

    def handle(
        self,
        event: ConstitutionalEvent,
    ) -> dict[str, str]:
        self.events.append(event)
        return {
            "event_id": event.event_id,
            "status": "collected",
        }
