"""Canonical Constitutional Mission events."""

from __future__ import annotations

from enum import StrEnum

from aletheus.constitutional_events.registry import (
    ConstitutionalEventRegistry,
    EventTypeDefinition,
)


class MissionEventType(StrEnum):
    MISSION_CREATED = "MissionCreated"
    MISSION_AUTHORIZED = "MissionAuthorized"
    MISSION_STARTED = "MissionStarted"
    MISSION_PARTICIPANT_JOINED = "MissionParticipantJoined"
    MISSION_EVIDENCE_ATTACHED = "MissionEvidenceAttached"
    MISSION_WAITING = "MissionWaiting"
    MISSION_RECOVERY_STARTED = "MissionRecoveryStarted"
    MISSION_COMPLETED = "MissionCompleted"
    MISSION_FAILED = "MissionFailed"
    MISSION_ARCHIVED = "MissionArchived"


def canonical_mission_event_definitions(
) -> tuple[EventTypeDefinition, ...]:
    descriptions = {
        MissionEventType.MISSION_CREATED: (
            "A constitutional mission was created."
        ),
        MissionEventType.MISSION_AUTHORIZED: (
            "A constitutional mission was authorized."
        ),
        MissionEventType.MISSION_STARTED: (
            "A constitutional mission began execution."
        ),
        MissionEventType.MISSION_PARTICIPANT_JOINED: (
            "An institution joined a constitutional mission."
        ),
        MissionEventType.MISSION_EVIDENCE_ATTACHED: (
            "Evidence was attached to a constitutional mission."
        ),
        MissionEventType.MISSION_WAITING: (
            "A mission entered a governed waiting state."
        ),
        MissionEventType.MISSION_RECOVERY_STARTED: (
            "A failed or degraded mission began recovery."
        ),
        MissionEventType.MISSION_COMPLETED: (
            "A constitutional mission completed successfully."
        ),
        MissionEventType.MISSION_FAILED: (
            "A constitutional mission failed."
        ),
        MissionEventType.MISSION_ARCHIVED: (
            "A completed mission was archived."
        ),
    }

    return tuple(
        EventTypeDefinition(
            event_type=event_type,
            description=description,
            constitutional_domain="mission",
            requires_certification=(
                event_type
                in {
                    MissionEventType.MISSION_AUTHORIZED,
                    MissionEventType.MISSION_COMPLETED,
                }
            ),
        )
        for event_type, description in descriptions.items()
    )


def register_mission_event_types(
    registry: ConstitutionalEventRegistry,
) -> ConstitutionalEventRegistry:
    for definition in canonical_mission_event_definitions():
        existing = registry.get(definition.event_type)

        if existing is None:
            registry.register(definition)
            continue

        if (
            existing.event_type.value
            != definition.event_type.value
            or existing.constitutional_domain
            != definition.constitutional_domain
            or existing.requires_certification
            != definition.requires_certification
        ):
            raise ValueError(
                "Conflicting mission event definition for "
                f"{definition.event_type.value!r}."
            )

    return registry
