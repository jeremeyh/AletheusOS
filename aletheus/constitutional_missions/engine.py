"""Constitutional Mission Engine."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from aletheus.constitutional_events import (
    ConstitutionalEvent,
    ConstitutionalEventFabric,
)

from .events import (
    MissionEventType,
    register_mission_event_types,
)
from .models import (
    ConstitutionalMission,
    MissionStatus,
)
from .registry import ConstitutionalMissionRegistry


def _timestamp() -> str:
    return datetime.now(UTC).isoformat()


class InvalidMissionTransitionError(ValueError):
    pass


class ConstitutionalMissionEngine:
    """
    Governs mission identity, participation, evidence, and outcomes.

    TIME™ will later own relative phase progression.
    Hour Glass™ will later own absolute scheduling.
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        fabric: ConstitutionalEventFabric,
        registry: ConstitutionalMissionRegistry | None = None,
    ) -> None:
        self.fabric = fabric
        self.registry = (
            registry or ConstitutionalMissionRegistry()
        )

        register_mission_event_types(
            self.fabric.registry
        )

    def create(
        self,
        mission: ConstitutionalMission,
    ) -> ConstitutionalMission:
        self.registry.register(mission)

        self._publish(
            mission,
            MissionEventType.MISSION_CREATED,
            source_identity="aletheus.mission_engine",
            payload={
                "mission": mission.to_dict(),
            },
        )

        return mission

    def authorize(
        self,
        mission_id: str,
        *,
        authority: str = "aletheus.council",
    ) -> ConstitutionalMission:
        mission = self.registry.require(mission_id)

        self._require_status(
            mission,
            MissionStatus.PLANNED,
        )

        mission.status = MissionStatus.AUTHORIZED
        mission.authorized_at = _timestamp()

        self._publish(
            mission,
            MissionEventType.MISSION_AUTHORIZED,
            source_identity=authority,
            payload={
                "mission_id": mission.mission_id,
                "authority": authority,
            },
            certified=True,
        )

        return mission

    def join(
        self,
        mission_id: str,
        institution_id: str,
    ) -> ConstitutionalMission:
        mission = self.registry.require(mission_id)

        if institution_id not in mission.contract.required_institutions:
            raise ValueError(
                f"Institution {institution_id!r} is not authorized "
                f"for mission type {mission.mission_type!r}."
            )

        if institution_id not in mission.participating_institutions:
            mission.participating_institutions.append(
                institution_id
            )

            self._publish(
                mission,
                MissionEventType.MISSION_PARTICIPANT_JOINED,
                source_identity=institution_id,
                payload={
                    "mission_id": mission.mission_id,
                    "institution_id": institution_id,
                },
            )

        return mission

    def start(
        self,
        mission_id: str,
    ) -> ConstitutionalMission:
        mission = self.registry.require(mission_id)

        self._require_status(
            mission,
            MissionStatus.AUTHORIZED,
        )

        missing = set(
            mission.contract.required_institutions
        ) - set(mission.participating_institutions)

        if missing:
            raise ValueError(
                "Mission cannot start; required institutions "
                "have not joined: "
                + ", ".join(sorted(missing))
            )

        mission.status = MissionStatus.RUNNING
        mission.started_at = _timestamp()

        self._publish(
            mission,
            MissionEventType.MISSION_STARTED,
            source_identity="aletheus.mission_engine",
            payload={
                "mission_id": mission.mission_id,
            },
        )

        return mission

    def attach_evidence(
        self,
        mission_id: str,
        *,
        evidence_type: str,
        evidence: dict[str, Any],
        source_identity: str,
    ) -> ConstitutionalMission:
        mission = self.registry.require(mission_id)

        if evidence_type not in mission.contract.required_evidence_types:
            raise ValueError(
                f"Evidence type {evidence_type!r} is not declared "
                "by the mission contract."
            )

        record = {
            "evidence_type": evidence_type,
            "source_identity": source_identity,
            "evidence": dict(evidence),
        }

        mission.evidence.append(record)

        self._publish(
            mission,
            MissionEventType.MISSION_EVIDENCE_ATTACHED,
            source_identity=source_identity,
            payload={
                "mission_id": mission.mission_id,
                **record,
            },
        )

        return mission

    def complete(
        self,
        mission_id: str,
    ) -> ConstitutionalMission:
        mission = self.registry.require(mission_id)

        self._require_status(
            mission,
            MissionStatus.RUNNING,
        )

        evidence_types = {
            item["evidence_type"]
            for item in mission.evidence
        }

        missing = set(
            mission.contract.required_evidence_types
        ) - evidence_types

        if missing:
            raise ValueError(
                "Mission cannot complete; evidence is missing: "
                + ", ".join(sorted(missing))
            )

        mission.status = MissionStatus.COMPLETED
        mission.completed_at = _timestamp()

        self._publish(
            mission,
            MissionEventType.MISSION_COMPLETED,
            source_identity="aletheus.mission_engine",
            payload={
                "mission_id": mission.mission_id,
                "success_criteria": (
                    mission.contract.success_criteria
                ),
                "evidence_count": len(mission.evidence),
            },
            certified=True,
        )

        return mission

    def fail(
        self,
        mission_id: str,
        reason: str,
    ) -> ConstitutionalMission:
        mission = self.registry.require(mission_id)

        if mission.status in {
            MissionStatus.COMPLETED,
            MissionStatus.ARCHIVED,
        }:
            raise InvalidMissionTransitionError(
                "Completed or archived missions may not fail."
            )

        mission.status = MissionStatus.FAILED
        mission.failures.append(reason)
        mission.completed_at = _timestamp()

        self._publish(
            mission,
            MissionEventType.MISSION_FAILED,
            source_identity="aletheus.mission_engine",
            payload={
                "mission_id": mission.mission_id,
                "reason": reason,
            },
        )

        return mission

    def history(
        self,
        mission_id: str,
    ) -> tuple[ConstitutionalEvent, ...]:
        mission = self.registry.require(mission_id)

        return self.fabric.events(
            correlation_id=mission.correlation_id
        )

    def _publish(
        self,
        mission: ConstitutionalMission,
        event_type: MissionEventType,
        *,
        source_identity: str,
        payload: dict[str, Any],
        certified: bool = False,
    ) -> ConstitutionalEvent:
        causation_id = (
            mission.event_ids[-1]
            if mission.event_ids
            else None
        )

        event = ConstitutionalEvent.create(
            event_type,
            source_identity,
            correlation_id=mission.correlation_id,
            causation_id=causation_id,
            payload=payload,
            certified=certified,
            tags=("mission", mission.mission_type),
        )

        mission.event_ids.append(event.event_id)
        self.fabric.publish(event)
        return event

    @staticmethod
    def _require_status(
        mission: ConstitutionalMission,
        expected: MissionStatus,
    ) -> None:
        if mission.status != expected:
            raise InvalidMissionTransitionError(
                f"Mission {mission.mission_id!r} is "
                f"{mission.status.value!r}; expected "
                f"{expected.value!r}."
            )

    def health(self) -> dict[str, Any]:
        return {
            "name": "Constitutional Mission Engine™",
            "version": self.VERSION,
            "status": "online",
            **self.registry.statistics(),
        }
