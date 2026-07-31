"""Validation for Constitutional Cases."""

from __future__ import annotations

from dataclasses import dataclass

from .models import CaseContract, ConstitutionalCase


@dataclass(frozen=True, slots=True)
class CaseValidationIssue:
    field: str
    message: str


class CaseValidationError(ValueError):
    def __init__(
        self,
        issues: list[CaseValidationIssue],
    ) -> None:
        self.issues = tuple(issues)

        super().__init__(
            "; ".join(f"{issue.field}: {issue.message}" for issue in issues)
        )


def _duplicates(values: tuple[str, ...]) -> bool:
    normalized = [value.strip().casefold() for value in values]
    return len(normalized) != len(set(normalized))


def validate_contract(
    contract: CaseContract,
) -> CaseContract:
    issues: list[CaseValidationIssue] = []

    if not contract.case_type.strip():
        issues.append(
            CaseValidationIssue(
                "case_type",
                "Case type may not be empty.",
            )
        )

    if not contract.purpose.strip():
        issues.append(
            CaseValidationIssue(
                "purpose",
                "Case purpose may not be empty.",
            )
        )

    fields = {
        "permitted_mission_types": (contract.permitted_mission_types),
        "required_institutions": (contract.required_institutions),
        "required_evidence_types": (contract.required_evidence_types),
        "closure_criteria": contract.closure_criteria,
    }

    for field_name, values in fields.items():
        if not values:
            issues.append(
                CaseValidationIssue(
                    field_name,
                    "At least one entry is required.",
                )
            )

        if any(not value.strip() for value in values):
            issues.append(
                CaseValidationIssue(
                    field_name,
                    "Blank entries are not permitted.",
                )
            )

        if _duplicates(values):
            issues.append(
                CaseValidationIssue(
                    field_name,
                    "Duplicate entries are not permitted.",
                )
            )

    if issues:
        raise CaseValidationError(issues)

    return contract


def validate_case(
    case: ConstitutionalCase,
) -> ConstitutionalCase:
    validate_contract(case.contract)

    issues: list[CaseValidationIssue] = []

    required = {
        "case_id": case.case_id,
        "case_type": case.case_type,
        "canonical_name": case.canonical_name,
        "purpose": case.purpose,
        "authority": case.authority,
        "jurisdiction": case.jurisdiction,
    }

    for field_name, value in required.items():
        if not value.strip():
            issues.append(
                CaseValidationIssue(
                    field_name,
                    "This field may not be empty.",
                )
            )

    if case.case_type != case.contract.case_type:
        issues.append(
            CaseValidationIssue(
                "case_type",
                "Case type must match its contract.",
            )
        )

    if issues:
        raise CaseValidationError(issues)

    return case
