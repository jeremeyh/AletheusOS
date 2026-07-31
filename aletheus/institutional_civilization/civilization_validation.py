"""Validation for constitutional civilization records."""

from __future__ import annotations

from dataclasses import dataclass

from .civilization_models import CivilizationRecord


@dataclass(frozen=True, slots=True)
class CivilizationValidationIssue:
    field: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "field": self.field,
            "message": self.message,
        }


class CivilizationValidationError(ValueError):
    """Raised when a Civilization violates constitutional invariants."""

    def __init__(
        self,
        issues: list[CivilizationValidationIssue],
    ) -> None:
        self.issues = tuple(issues)

        detail = "; ".join(f"{issue.field}: {issue.message}" for issue in self.issues)

        super().__init__(f"Invalid civilization record: {detail}")


def _has_duplicates(values: tuple[str, ...]) -> bool:
    normalized = [value.strip().casefold() for value in values]
    return len(normalized) != len(set(normalized))


def validate_civilization(
    record: CivilizationRecord,
) -> CivilizationRecord:
    issues: list[CivilizationValidationIssue] = []

    required_text = {
        "civilization_id": record.civilization_id,
        "canonical_name": record.canonical_name,
        "purpose": record.purpose,
        "authority_domain": record.authority_domain,
    }

    for field_name, value in required_text.items():
        if not value.strip():
            issues.append(
                CivilizationValidationIssue(
                    field_name,
                    "This constitutional field may not be empty.",
                )
            )

    if "." not in record.civilization_id:
        issues.append(
            CivilizationValidationIssue(
                "civilization_id",
                "Use a namespaced identifier such as 'aletheus.civilization.security'.",
            )
        )

    if not record.institution_ids:
        issues.append(
            CivilizationValidationIssue(
                "institution_ids",
                "Every civilization must contain at least one institution.",
            )
        )

    if not record.responsibilities:
        issues.append(
            CivilizationValidationIssue(
                "responsibilities",
                "Every civilization must own at least one responsibility.",
            )
        )

    if not record.non_responsibilities:
        issues.append(
            CivilizationValidationIssue(
                "non_responsibilities",
                "Every civilization must declare at least one boundary.",
            )
        )

    sequence_fields = {
        "institution_ids": record.institution_ids,
        "responsibilities": record.responsibilities,
        "non_responsibilities": record.non_responsibilities,
        "governed_by": record.governed_by,
        "observed_by": record.observed_by,
        "collaborates_with": record.collaborates_with,
        "constitutional_articles": record.constitutional_articles,
        "ontology_tags": record.ontology_tags,
    }

    for field_name, values in sequence_fields.items():
        if any(not item.strip() for item in values):
            issues.append(
                CivilizationValidationIssue(
                    field_name,
                    "Entries may not be blank.",
                )
            )

        if _has_duplicates(values):
            issues.append(
                CivilizationValidationIssue(
                    field_name,
                    "Duplicate entries are not permitted.",
                )
            )

    overlap = set(record.responsibilities).intersection(record.non_responsibilities)

    if overlap:
        issues.append(
            CivilizationValidationIssue(
                "responsibilities",
                "Responsibilities and boundaries conflict: "
                + ", ".join(sorted(overlap)),
            )
        )

    if record.civilization_id in record.collaborates_with:
        issues.append(
            CivilizationValidationIssue(
                "collaborates_with",
                "A civilization may not collaborate with itself.",
            )
        )

    if issues:
        raise CivilizationValidationError(issues)

    return record
