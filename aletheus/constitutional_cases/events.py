"""Canonical Constitutional Case events."""

from __future__ import annotations

from enum import StrEnum

from aletheus.constitutional_events.registry import (
    ConstitutionalEventRegistry,
    EventTypeDefinition,
)


class CaseEventType(StrEnum):
    CASE_DETECTED = "CaseDetected"
    CASE_OPENED = "CaseOpened"
    CASE_INVESTIGATION_STARTED = "CaseInvestigationStarted"
    CASE_MISSION_ATTACHED = "CaseMissionAttached"
    CASE_EVIDENCE_ATTACHED = "CaseEvidenceAttached"
    CASE_CONTAINED = "CaseContained"
    CASE_RECOVERY_STARTED = "CaseRecoveryStarted"
    CASE_RESOLVED = "CaseResolved"
    CASE_VERIFIED = "CaseVerified"
    CASE_CLOSED = "CaseClosed"
    CASE_ARCHIVED = "CaseArchived"
    CASE_GOVERNANCE_ESCALATED = "CaseGovernanceEscalated"


def canonical_case_event_definitions() -> tuple[EventTypeDefinition, ...]:
    descriptions = {
        CaseEventType.CASE_DETECTED: ("A constitutional case was detected."),
        CaseEventType.CASE_OPENED: ("A constitutional case was opened."),
        CaseEventType.CASE_INVESTIGATION_STARTED: (
            "Investigation of a constitutional case began."
        ),
        CaseEventType.CASE_MISSION_ATTACHED: (
            "A mission was attached to a constitutional case."
        ),
        CaseEventType.CASE_EVIDENCE_ATTACHED: (
            "Evidence was attached to a constitutional case."
        ),
        CaseEventType.CASE_CONTAINED: ("A constitutional case entered containment."),
        CaseEventType.CASE_RECOVERY_STARTED: (
            "Recovery for a constitutional case began."
        ),
        CaseEventType.CASE_RESOLVED: ("A constitutional case was resolved."),
        CaseEventType.CASE_VERIFIED: (
            "Resolution of a constitutional case was verified."
        ),
        CaseEventType.CASE_CLOSED: ("A constitutional case was closed."),
        CaseEventType.CASE_ARCHIVED: ("A constitutional case was archived."),
        CaseEventType.CASE_GOVERNANCE_ESCALATED: (
            "A constitutional case was escalated for governance."
        ),
    }

    certified = {
        CaseEventType.CASE_RESOLVED,
        CaseEventType.CASE_VERIFIED,
        CaseEventType.CASE_CLOSED,
    }

    return tuple(
        EventTypeDefinition(
            event_type=event_type,
            description=description,
            constitutional_domain="case",
            requires_certification=event_type in certified,
        )
        for event_type, description in descriptions.items()
    )


def register_case_event_types(
    registry: ConstitutionalEventRegistry,
) -> ConstitutionalEventRegistry:
    for definition in canonical_case_event_definitions():
        existing = registry.get(definition.event_type)

        if existing is None:
            registry.register(definition)
            continue

        if (
            existing.event_type.value != definition.event_type.value
            or existing.constitutional_domain != definition.constitutional_domain
            or existing.requires_certification != definition.requires_certification
        ):
            raise ValueError(
                "Conflicting case event definition for "
                f"{definition.event_type.value!r}."
            )

    return registry
