"""Bootstrap SPAN into an existing registry authority."""

from __future__ import annotations

from typing import Any

from .service import SPANRuntimeService


def install_span_runtime(
    registry: Any,
    *,
    events: Any | None = None,
    telemetry: Any | None = None,
    ledger: Any | None = None,
    council: Any | None = None,
    auto_start: bool = True,
) -> SPANRuntimeService:
    """Create, register, and optionally start the SPAN runtime service."""
    service = SPANRuntimeService(
        events=events,
        telemetry=telemetry,
        ledger=ledger,
        council=council,
    )
    registry.register(service.service_name, service)
    service.initialize()
    if auto_start:
        service.start()
    return service
