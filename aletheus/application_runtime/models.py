"""Canonical models for the Constitutional Application Runtime™."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class ApplicationStatus(StrEnum):
    INSTALLED = "installed"
    VALIDATED = "validated"
    INITIALIZED = "initialized"
    RUNNING = "running"
    SUSPENDED = "suspended"
    STOPPED = "stopped"
    FAILED = "failed"
    UNINSTALLED = "uninstalled"


@dataclass(frozen=True, slots=True)
class ApplicationManifest:
    application_id: str
    canonical_name: str
    version: str
    owner: str
    purpose: str

    required_services: tuple[str, ...] = ()
    provided_capabilities: tuple[str, ...] = ()
    required_capabilities: tuple[str, ...] = ()
    permissions: tuple[str, ...] = ()

    genesis: str = "16"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ApplicationRecord:
    manifest: ApplicationManifest
    application: Any
    status: ApplicationStatus = ApplicationStatus.INSTALLED

    initialized: bool = False
    started: bool = False

    failures: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "manifest": self.manifest.to_dict(),
            "status": self.status.value,
            "initialized": self.initialized,
            "started": self.started,
            "failures": list(self.failures),
            "metadata": dict(self.metadata),
        }
