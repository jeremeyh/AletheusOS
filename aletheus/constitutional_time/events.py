"""Canonical TIME™ relative-phase events."""

from __future__ import annotations

from enum import StrEnum

from aletheus.constitutional_events.registry import (
    ConstitutionalEventRegistry,
    EventTypeDefinition,
)


class TimeEventType(StrEnum):
    MISSION_PHASE_GRAPH_ATTACHED = "MissionPhaseGraphAttached"
    MISSION_PHASE_ELIGIBLE = "MissionPhaseEligible"
    MISSION_PHASE_STARTED = "MissionPhaseStarted"
    MISSION_PHASE_PARTICIPANT_JOINED = "MissionPhaseParticipantJoined"
    MISSION_PHASE_EVIDENCE_ATTACHED = "MissionPhaseEvidenceAttached"
    MISSION_PHASE_COMPLETED = "MissionPhaseCompleted"
    MISSION_PHASE_FAILED = "MissionPhaseFailed"
    MISSION_PHASE_BLOCKED = "MissionPhaseBlocked"
    MISSION_TEMPORAL_SEQUENCE_COMPLETED = "MissionTemporalSequenceCompleted"


def canonical_time_event_definitions() -> tuple[EventTypeDefinition, ...]:
    descriptions = {
        TimeEventType.MISSION_PHASE_GRAPH_ATTACHED: (
            "TIME attached a relative phase graph to a mission."
        ),
        TimeEventType.MISSION_PHASE_ELIGIBLE: (
            "A mission phase became causally eligible."
        ),
        TimeEventType.MISSION_PHASE_STARTED: ("A relative mission phase began."),
        TimeEventType.MISSION_PHASE_PARTICIPANT_JOINED: (
            "An institution joined a relative mission phase."
        ),
        TimeEventType.MISSION_PHASE_EVIDENCE_ATTACHED: (
            "Evidence was attached to a relative mission phase."
        ),
        TimeEventType.MISSION_PHASE_COMPLETED: ("A relative mission phase completed."),
        TimeEventType.MISSION_PHASE_FAILED: ("A relative mission phase failed."),
        TimeEventType.MISSION_PHASE_BLOCKED: (
            "A phase became blocked by a failed dependency."
        ),
        TimeEventType.MISSION_TEMPORAL_SEQUENCE_COMPLETED: (
            "TIME completed the mission phase sequence."
        ),
    }

    return tuple(
        EventTypeDefinition(
            event_type=event_type,
            description=description,
            constitutional_domain="relative_time",
        )
        for event_type, description in descriptions.items()
    )


def register_time_event_types(
    registry: ConstitutionalEventRegistry,
) -> ConstitutionalEventRegistry:
    for definition in canonical_time_event_definitions():
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
                "Conflicting TIME event definition for "
                f"{definition.event_type.value!r}."
            )

    return registry
