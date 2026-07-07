from __future__ import annotations

from pathlib import Path

from .service import AtlasService


class AtlasAPI:
    """Thin API facade for future runtime/service-bus exposure."""

    def __init__(self, service: AtlasService) -> None:
        self.service = service

    def discover(self, root: str) -> dict:
        report = self.service.discover(Path(root))
        return {
            "subsystem_count": report.snapshot.subsystem_count,
            "family_count": report.snapshot.family_count,
            "findings": report.findings,
            "warnings": report.warnings,
        }

    def health(self) -> dict:
        health = self.service.health()
        return health.__dict__

    def metrics(self) -> dict:
        return self.service.metrics()
