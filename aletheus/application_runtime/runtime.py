"""Constitutional Application Runtime™."""

from __future__ import annotations

from typing import Any

from .models import ApplicationStatus
from .registry import (
    ConstitutionalApplicationRegistry,
)
from .services import ApplicationServiceResolver


class InvalidApplicationTransitionError(ValueError):
    pass


class ConstitutionalApplicationRuntime:
    """
    Host applications above the stable AletheusOS Platform Surface.

    Applications receive public platform services through injection and never
    construct or access internal constitutional engines directly.
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        platform,
        registry: (
            ConstitutionalApplicationRegistry
            | None
        ) = None,
    ) -> None:
        self.platform = platform
        self.registry = (
            registry
            or ConstitutionalApplicationRegistry()
        )

        self.services = ApplicationServiceResolver(
            platform=platform
        )

        self._starts = 0
        self._stops = 0
        self._failures = 0

    def install(
        self,
        application,
    ):
        return self.registry.install(
            application
        )

    def initialize(
        self,
        application_id: str,
    ):
        record = self.registry.require(
            application_id
        )

        if record.status not in {
            ApplicationStatus.INSTALLED,
            ApplicationStatus.STOPPED,
        }:
            raise InvalidApplicationTransitionError(
                f"Application {application_id!r} "
                f"cannot initialize from "
                f"{record.status.value!r}."
            )

        resolved_services = (
            self.services.resolve_many(
                record.manifest.required_services
            )
        )

        try:
            record.application.initialize(
                resolved_services
            )

        except Exception as exc:
            record.status = ApplicationStatus.FAILED
            record.failures.append(str(exc))
            self._failures += 1
            raise

        record.initialized = True
        record.status = ApplicationStatus.INITIALIZED

        return record

    def start(
        self,
        application_id: str,
    ):
        record = self.registry.require(
            application_id
        )

        if record.status != (
            ApplicationStatus.INITIALIZED
        ):
            raise InvalidApplicationTransitionError(
                f"Application {application_id!r} "
                f"cannot start from "
                f"{record.status.value!r}."
            )

        try:
            record.application.start()

        except Exception as exc:
            record.status = ApplicationStatus.FAILED
            record.failures.append(str(exc))
            self._failures += 1
            raise

        record.started = True
        record.status = ApplicationStatus.RUNNING
        self._starts += 1

        return record

    def stop(
        self,
        application_id: str,
    ):
        record = self.registry.require(
            application_id
        )

        if record.status not in {
            ApplicationStatus.RUNNING,
            ApplicationStatus.SUSPENDED,
        }:
            raise InvalidApplicationTransitionError(
                f"Application {application_id!r} "
                f"cannot stop from "
                f"{record.status.value!r}."
            )

        try:
            record.application.stop()

        except Exception as exc:
            record.status = ApplicationStatus.FAILED
            record.failures.append(str(exc))
            self._failures += 1
            raise

        record.started = False
        record.status = ApplicationStatus.STOPPED
        self._stops += 1

        return record

    def uninstall(
        self,
        application_id: str,
    ):
        record = self.registry.require(
            application_id
        )

        if record.status == ApplicationStatus.RUNNING:
            raise InvalidApplicationTransitionError(
                "Running applications must be stopped "
                "before uninstall."
            )

        removed = self.registry.remove(
            application_id
        )

        removed.status = ApplicationStatus.UNINSTALLED
        return removed

    def application_health(
        self,
        application_id: str,
    ) -> dict[str, Any]:
        record = self.registry.require(
            application_id
        )

        application_health = (
            record.application.health()
        )

        return {
            "application_id": (
                record.manifest.application_id
            ),
            "canonical_name": (
                record.manifest.canonical_name
            ),
            "status": record.status.value,
            "runtime_status": (
                application_health.get(
                    "status",
                    "unknown",
                )
                if isinstance(
                    application_health,
                    dict,
                )
                else "unknown"
            ),
            "details": application_health,
        }

    def health(self) -> dict[str, Any]:
        return {
            "name": (
                "Constitutional Application Runtime™"
            ),
            "version": self.VERSION,
            "status": (
                "degraded"
                if self._failures
                else "online"
            ),
            "starts": self._starts,
            "stops": self._stops,
            "failures": self._failures,
            "registry": self.registry.health(),
            "available_services": (
                self.services.available()
            ),
        }
