"""
AletheusOS
Genesis 49.0

Reason Engine™

Reason Registry
"""

from __future__ import annotations

from .models import (
    ReasonObject,
    ReasonStatus,
)


class ReasonRegistry:
    """
    Canonical registry for constitutional
    reasoning records.

    The registry preserves completed
    reasoning so that it may be inspected,
    audited, replayed, and referenced by
    future Foundation capabilities.
    """

    GENESIS = "49.0"
    VERSION = "1.0.0"

    def __init__(self) -> None:

        self._reasons: dict[str, ReasonObject] = {}

    def register(
        self,
        reason: ReasonObject,
    ) -> ReasonObject:

        self._reasons[reason.reason_id] = reason

        return reason

    def get(
        self,
        reason_id: str,
    ) -> ReasonObject | None:

        return self._reasons.get(reason_id)

    def exists(
        self,
        reason_id: str,
    ) -> bool:

        return reason_id in self._reasons

    def all(self) -> list[ReasonObject]:

        return sorted(
            self._reasons.values(),
            key=lambda reason: reason.created_at,
        )

    def by_identity(
        self,
        identity: str,
    ) -> list[ReasonObject]:

        return [
            reason
            for reason in self._reasons.values()
            if reason.identity == identity
        ]

    def by_intent(
        self,
        intent: str,
    ) -> list[ReasonObject]:

        return [
            reason
            for reason in self._reasons.values()
            if reason.intent == intent
        ]

    def by_status(
        self,
        status: ReasonStatus,
    ) -> list[ReasonObject]:

        return [
            reason
            for reason in self._reasons.values()
            if reason.status == status
        ]

    def health(self) -> dict:

        return {
            "name": "Reason Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
            "registered_reasons": len(self._reasons),
        }

    def statistics(self) -> dict:

        statuses: dict[str, int] = {}

        for reason in self._reasons.values():

            key = reason.status.value

            statuses.setdefault(key, 0)

            statuses[key] += 1

        return {
            "name": "Reason Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "registered_reasons": len(self._reasons),
            "statuses": statuses,
        }


reason_registry = ReasonRegistry()
