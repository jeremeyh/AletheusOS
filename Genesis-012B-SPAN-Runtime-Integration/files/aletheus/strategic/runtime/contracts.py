"""Structural contracts for composing SPAN with existing authorities."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class RegistryAuthority(Protocol):
    def register(self, name: str, service: Any) -> Any:
        """Register a service under a stable runtime name."""


@runtime_checkable
class EventAuthority(Protocol):
    def publish(self, event_type: str, payload: Mapping[str, Any]) -> Any:
        """Publish an event through the existing event authority."""


@runtime_checkable
class TelemetryAuthority(Protocol):
    def increment(self, metric: str, value: int = 1) -> Any:
        """Increment a counter."""

    def observe(self, metric: str, value: float) -> Any:
        """Record an observed value."""


@runtime_checkable
class LedgerAuthority(Protocol):
    def append(self, record: Mapping[str, Any]) -> Any:
        """Append an immutable strategic record."""


@runtime_checkable
class CouncilAuthority(Protocol):
    def submit(self, proposal: Mapping[str, Any]) -> Any:
        """Submit an advisory proposal for governance review."""
