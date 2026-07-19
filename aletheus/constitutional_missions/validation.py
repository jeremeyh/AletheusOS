"""Validation for Constitutional Missions."""

from __future__ import annotations

from dataclasses import dataclass

from .models import ConstitutionalMission, MissionContract


@dataclass(frozen=True, slots=True)
class MissionValidationIssue:
    field: str
    message: str


class MissionValidationError(ValueError):
    def __init__(
        self,
        issues: list[MissionValidationIssue],
    ) -> None:
        self.issues = tuple(issues)

        super().__init__(
            "; ".join(
                f"{issue.field}: {issue.message}"
                for issue in issues
            )
        )


def _duplicates(values: tuple[str, ...]) -> bool:
    normalized = [
        value.strip().casefold()
        for value in values
    ]
    return len(normalized) != len(set(normalized))


def validate_contract(
    contract: MissionContract,
) -> MissionContract:
    issues: list[MissionValidationIssue] = []

    if not contract.mission_type.strip():
        issues.append(
            MissionValidationIssue(
                "mission_type",
                "Mission type may not be empty.",
            )
        )

    if not contract.purpose.strip():
        issues.append(
            MissionValidationIssue(
                "purpose",
                "Mission purpose may not be empty.",
            )
        )

    required_sequences = {
        "required_institutions": contract.required_institutions,
        "required_evidence_types": contract.required_evidence_types,
        "success_criteria": contract.success_criteria,
        "failure_criteria": contract.failure_criteria,
    }

    for field_name, values in required_sequences.items():
        if not values:
            issues.append(
                MissionValidationIssue(
                    field_name,
                    "At least one entry is required.",
                )
            )

        if any(not value.strip() for value in values):
            issues.append(
                MissionValidationIssue(
                    field_name,
                    "Blank entries are not permitted.",
                )
            )

        if _duplicates(values):
            issues.append(
                MissionValidationIssue(
                    field_name,
                    "Duplicate entries are not permitted.",
                )
            )

    if issues:
        raise MissionValidationError(issues)

    return contract


def validate_mission(
    mission: ConstitutionalMission,
) -> ConstitutionalMission:
    validate_contract(mission.contract)

    issues: list[MissionValidationIssue] = []

    required = {
        "mission_id": mission.mission_id,
        "mission_type": mission.mission_type,
        "canonical_name": mission.canonical_name,
        "purpose": mission.purpose,
        "authority": mission.authority,
        "jurisdiction": mission.jurisdiction,
    }

    for field_name, value in required.items():
        if not value.strip():
            issues.append(
                MissionValidationIssue(
                    field_name,
                    "This field may not be empty.",
                )
            )

    if mission.mission_type != mission.contract.mission_type:
        issues.append(
            MissionValidationIssue(
                "mission_type",
                "Mission type must match its contract.",
            )
        )

    if issues:
        raise MissionValidationError(issues)

    return mission
