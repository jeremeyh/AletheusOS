"""Contracts for Constitutional Event Bus subscribers."""

from __future__ import annotations

from typing import Protocol

from aletheus.platform_intelligence.events import (
    ConstitutionalEvent,
)


class ConstitutionalEventHandler(Protocol):
    """Callable contract for event subscribers."""

    def __call__(
        self,
        event: ConstitutionalEvent,
    ) -> None:
        ...


class ConstitutionalSubscriber(Protocol):
    """Object-oriented subscriber contract."""

    def handle(
        self,
        event: ConstitutionalEvent,
    ) -> None:
        ...
