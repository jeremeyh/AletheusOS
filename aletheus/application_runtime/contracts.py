"""Contracts for hosted AletheusOS applications."""

from __future__ import annotations

from typing import Any, Protocol

from .models import ApplicationManifest


class ConstitutionalApplication(Protocol):
    """Protocol implemented by applications hosted by AletheusOS."""

    manifest: ApplicationManifest

    def initialize(
        self,
        services: dict[str, Any],
    ) -> None:
        ...

    def start(self) -> None:
        ...

    def stop(self) -> None:
        ...

    def health(self) -> dict[str, Any]:
        ...
