"""Immutable event subscription model."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4

from aletheus.platform_intelligence.events import (
    ConstitutionalEvent,
    ConstitutionalEventKind,
)

from .contracts import ConstitutionalEventHandler


@dataclass(frozen=True, slots=True)
class ConstitutionalSubscription:
    """A bounded subscription to constitutional events."""

    subscription_id: UUID
    handler: ConstitutionalEventHandler
    kinds: frozenset[ConstitutionalEventKind]
    source_prefix: str | None = None
    subject_prefix: str | None = None

    @classmethod
    def create(
        cls,
        *,
        handler: ConstitutionalEventHandler,
        kinds: (
            set[ConstitutionalEventKind]
            | frozenset[ConstitutionalEventKind]
            | None
        ) = None,
        source_prefix: str | None = None,
        subject_prefix: str | None = None,
    ) -> ConstitutionalSubscription:
        return cls(
            subscription_id=uuid4(),
            handler=handler,
            kinds=frozenset(kinds or ()),
            source_prefix=(
                source_prefix.strip().lower()
                if source_prefix
                else None
            ),
            subject_prefix=(
                subject_prefix.strip().lower()
                if subject_prefix
                else None
            ),
        )

    def matches(
        self,
        event: ConstitutionalEvent,
    ) -> bool:
        if self.kinds and event.kind not in self.kinds:
            return False

        if (
            self.source_prefix is not None
            and not str(event.source).startswith(
                self.source_prefix
            )
        ):
            return False

        if (
            self.subject_prefix is not None
            and not str(event.subject).startswith(
                self.subject_prefix
            )
        ):
            return False

        return True
