"""Validation for constitutional applications."""

from __future__ import annotations

from dataclasses import dataclass

from .models import ApplicationManifest


@dataclass(frozen=True, slots=True)
class ApplicationValidationIssue:
    field: str
    message: str


class ApplicationValidationError(ValueError):
    def __init__(
        self,
        issues: list[ApplicationValidationIssue],
    ) -> None:
        self.issues = tuple(issues)

        super().__init__(
            "; ".join(
                f"{issue.field}: {issue.message}"
                for issue in issues
            )
        )


def _has_duplicates(values: tuple[str, ...]) -> bool:
    normalized = [
        value.strip().casefold()
        for value in values
    ]

    return len(normalized) != len(set(normalized))


def validate_manifest(
    manifest: ApplicationManifest,
) -> ApplicationManifest:
    issues: list[ApplicationValidationIssue] = []

    required = {
        "application_id": manifest.application_id,
        "canonical_name": manifest.canonical_name,
        "version": manifest.version,
        "owner": manifest.owner,
        "purpose": manifest.purpose,
    }

    for field_name, value in required.items():
        if not value.strip():
            issues.append(
                ApplicationValidationIssue(
                    field_name,
                    "This field may not be empty.",
                )
            )

    sequences = {
        "required_services": manifest.required_services,
        "provided_capabilities": (
            manifest.provided_capabilities
        ),
        "required_capabilities": (
            manifest.required_capabilities
        ),
        "permissions": manifest.permissions,
    }

    for field_name, values in sequences.items():
        if any(not value.strip() for value in values):
            issues.append(
                ApplicationValidationIssue(
                    field_name,
                    "Blank entries are not permitted.",
                )
            )

        if _has_duplicates(values):
            issues.append(
                ApplicationValidationIssue(
                    field_name,
                    "Duplicate entries are not permitted.",
                )
            )

    if issues:
        raise ApplicationValidationError(issues)

    return manifest
