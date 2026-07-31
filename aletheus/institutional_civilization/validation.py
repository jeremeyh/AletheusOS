"""Constitutional validation for institutional definitions."""

from __future__ import annotations

from dataclasses import dataclass

from .models import InstitutionRecord


@dataclass(frozen=True, slots=True)
class InstitutionValidationIssue:
    field: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "field": self.field,
            "message": self.message,
        }


class InstitutionValidationError(ValueError):
    """Raised when an institution violates constitutional invariants."""

    def __init__(self, issues: list[InstitutionValidationIssue]):
        self.issues = tuple(issues)
        detail = "; ".join(f"{issue.field}: {issue.message}" for issue in self.issues)
        super().__init__(f"Invalid institution record: {detail}")


def _has_duplicates(values: tuple[str, ...]) -> bool:
    normalized = [value.strip().casefold() for value in values]
    return len(normalized) != len(set(normalized))


def validate_institution(record: InstitutionRecord) -> InstitutionRecord:
    """Validate and return a constitutional institution record."""

    issues: list[InstitutionValidationIssue] = []

    if not record.institution_id.strip():
        issues.append(
            InstitutionValidationIssue(
                "institution_id",
                "A canonical institution identifier is required.",
            )
        )

    if "." not in record.institution_id:
        issues.append(
            InstitutionValidationIssue(
                "institution_id",
                "Use a namespaced identifier such as 'aletheus.spa'.",
            )
        )

    required_text = {
        "canonical_name": record.canonical_name,
        "purpose": record.purpose,
        "authority": record.authority,
        "jurisdiction": record.jurisdiction,
        "owner": record.owner,
    }

    for field_name, value in required_text.items():
        if not value.strip():
            issues.append(
                InstitutionValidationIssue(
                    field_name,
                    "This constitutional field may not be empty.",
                )
            )

    if not record.responsibilities:
        issues.append(
            InstitutionValidationIssue(
                "responsibilities",
                "Every institution must own at least one responsibility.",
            )
        )

    if not record.non_responsibilities:
        issues.append(
            InstitutionValidationIssue(
                "non_responsibilities",
                "Every institution must declare at least one boundary.",
            )
        )

    sequence_fields = {
        "responsibilities": record.responsibilities,
        "non_responsibilities": record.non_responsibilities,
        "consumes": record.consumes,
        "produces": record.produces,
        "dependencies": record.dependencies,
        "observed_by": record.observed_by,
        "governed_by": record.governed_by,
        "certified_by": record.certified_by,
        "repository_locations": record.repository_locations,
        "ontology_tags": record.ontology_tags,
        "constitutional_articles": record.constitutional_articles,
    }

    for field_name, values in sequence_fields.items():
        if any(not value.strip() for value in values):
            issues.append(
                InstitutionValidationIssue(
                    field_name,
                    "Entries may not be blank.",
                )
            )

        if _has_duplicates(values):
            issues.append(
                InstitutionValidationIssue(
                    field_name,
                    "Duplicate entries are not permitted.",
                )
            )

    if record.institution_id in record.dependencies:
        issues.append(
            InstitutionValidationIssue(
                "dependencies",
                "An institution may not depend directly on itself.",
            )
        )

    overlap = set(record.responsibilities).intersection(record.non_responsibilities)
    if overlap:
        issues.append(
            InstitutionValidationIssue(
                "responsibilities",
                "Responsibilities and boundaries conflict: "
                + ", ".join(sorted(overlap)),
            )
        )

    if issues:
        raise InstitutionValidationError(issues)

    return record
