"""
Constitutional Application Registry™.

Provides the canonical object-oriented registry used by the
Constitutional Application Runtime while preserving the earlier
functional registry API for compatibility.
"""

from __future__ import annotations

from typing import Any

from .models import (
    ApplicationManifest,
    ApplicationRecord,
)
from .validation import validate_manifest


class DuplicateApplicationError(ValueError):
    """Raised when an application ID is already installed."""


class ApplicationNotFoundError(KeyError):
    """Raised when an application ID is not installed."""


class ConstitutionalApplicationRegistry:
    """
    Registry of applications hosted by the Constitutional Application Runtime.

    Applications are indexed by the canonical application ID declared in their
    manifest. Installation validates the manifest and protects existing
    registrations from accidental replacement.
    """

    VERSION = "0.1.0"

    def __init__(self) -> None:
        self._records: dict[str, ApplicationRecord] = {}

    @staticmethod
    def _normalize_application_id(
        application_id: str,
    ) -> str:
        normalized = application_id.strip()

        if not normalized:
            raise ValueError(
                "Application ID cannot be empty."
            )

        return normalized

    def install(
        self,
        application: Any,
    ) -> ApplicationRecord:
        manifest = getattr(
            application,
            "manifest",
            None,
        )

        if not isinstance(
            manifest,
            ApplicationManifest,
        ):
            raise TypeError(
                "Applications must expose an "
                "ApplicationManifest through "
                "the 'manifest' attribute."
            )

        validate_manifest(manifest)

        application_id = (
            self._normalize_application_id(
                manifest.application_id
            )
        )

        if application_id in self._records:
            raise DuplicateApplicationError(
                f"Application is already installed: "
                f"{application_id}"
            )

        record = ApplicationRecord(
            manifest=manifest,
            application=application,
        )

        self._records[application_id] = record
        return record

    def get(
        self,
        application_id: str,
    ) -> ApplicationRecord | None:
        normalized = (
            self._normalize_application_id(
                application_id
            )
        )

        return self._records.get(normalized)

    def require(
        self,
        application_id: str,
    ) -> ApplicationRecord:
        normalized = (
            self._normalize_application_id(
                application_id
            )
        )

        try:
            return self._records[normalized]

        except KeyError as exc:
            raise ApplicationNotFoundError(
                f"Application is not installed: "
                f"{normalized}"
            ) from exc

    def remove(
        self,
        application_id: str,
    ) -> ApplicationRecord:
        normalized = (
            self._normalize_application_id(
                application_id
            )
        )

        try:
            return self._records.pop(normalized)

        except KeyError as exc:
            raise ApplicationNotFoundError(
                f"Application is not installed: "
                f"{normalized}"
            ) from exc

    def list_records(
        self,
    ) -> tuple[ApplicationRecord, ...]:
        return tuple(
            self._records[application_id]
            for application_id
            in sorted(self._records)
        )

    def list_application_ids(
        self,
    ) -> tuple[str, ...]:
        return tuple(sorted(self._records))

    def __len__(self) -> int:
        return len(self._records)

    def __contains__(
        self,
        application_id: object,
    ) -> bool:
        if not isinstance(application_id, str):
            return False

        normalized = application_id.strip()

        if not normalized:
            return False

        return normalized in self._records

    def health(self) -> dict[str, Any]:
        records = self.list_records()

        status_counts: dict[str, int] = {}

        for record in records:
            status = record.status.value
            status_counts[status] = (
                status_counts.get(status, 0) + 1
            )

        return {
            "name": (
                "Constitutional Application Registry™"
            ),
            "version": self.VERSION,
            "status": "online",
            "applications": len(records),
            "application_ids": list(
                self.list_application_ids()
            ),
            "status_counts": status_counts,
        }


# ---------------------------------------------------------------------------
# Legacy functional application registry
# ---------------------------------------------------------------------------
#
# Retained for compatibility with code that predates the Constitutional
# Application Runtime registry. This registry is intentionally separate from
# ConstitutionalApplicationRegistry instances.

APPLICATIONS: dict[str, Any] = {}


def register_application(
    name: str,
    application: Any,
    *,
    replace: bool = False,
) -> Any:
    """
    Register an application in the legacy functional registry.
    """

    normalized_name = name.strip().lower()

    if not normalized_name:
        raise ValueError(
            "Application name cannot be empty."
        )

    if (
        normalized_name in APPLICATIONS
        and not replace
    ):
        raise ValueError(
            "Application already registered: "
            f"{normalized_name}"
        )

    APPLICATIONS[normalized_name] = application
    return application


def get_application(
    name: str,
) -> Any:
    """
    Return an application from the legacy functional registry.
    """

    normalized_name = name.strip().lower()

    try:
        return APPLICATIONS[normalized_name]

    except KeyError as exc:
        raise KeyError(
            "Application is not registered: "
            f"{normalized_name}"
        ) from exc


def has_application(
    name: str,
) -> bool:
    """
    Return whether an application exists in the legacy registry.
    """

    return (
        name.strip().lower()
        in APPLICATIONS
    )


def list_applications() -> list[str]:
    """
    Return names registered in the legacy functional registry.
    """

    return sorted(APPLICATIONS)


__all__ = [
    "APPLICATIONS",
    "ApplicationNotFoundError",
    "ConstitutionalApplicationRegistry",
    "DuplicateApplicationError",
    "get_application",
    "has_application",
    "list_applications",
    "register_application",
]
