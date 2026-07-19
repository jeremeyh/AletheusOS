"""Public contracts for Constitutional Event Fabric participants."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from .models import ConstitutionalEvent


@runtime_checkable
class ConstitutionalEventSubscriber(Protocol):
    """Institution capable of consuming constitutional events."""

    def handle(self, event: ConstitutionalEvent) -> object:
        """Process one constitutional event."""
        ...


@runtime_checkable
class ConstitutionalEventPublisher(Protocol):
    """Capability capable of publishing constitutional events."""

    def publish(self, event: ConstitutionalEvent) -> object:
        """Publish one constitutional event."""
        ...
