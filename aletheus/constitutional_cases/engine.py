"""Constitutional Case Engine."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from aletheus.constitutional_events import (
    ConstitutionalEvent,
    ConstitutionalEventFabric,
)

from .events import (
    CaseEventType,
    register_case_event_types,
)
from .models import CaseStatus, ConstitutionalCase
from .registry import ConstitutionalCaseRegistry


def _timestamp() -> str:
    return datetime.now(UTC).isoformat()


class InvalidCaseTransitionError(ValueError):
    pass


class ConstitutionalCaseEngine:
    """
    Governs durable case state across one or more missions.

    Missions perform work.
    Cases preserve the constitutional context for that work.
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        fabric: ConstitutionalEventFabric,
        registry: ConstitutionalCaseRegistry | None = None,
    ) -> None:
        self.fabric = fabric
        self.registry = registry or ConstitutionalCaseRegistry()

        register_case_event_types(self.fabric.registry)

    def detect(
        self,
        case: ConstitutionalCase,
    ) -> ConstitutionalCase:
        self.registry.register(case)

        self._publish(
            case,
            CaseEventType.CASE_DETECTED,
            source_identity="aletheus.case_engine",
            payload={
                "case": case.to_dict(),
            },
        )

        return case

    def open(
        self,
        case_id: str,
    ) -> ConstitutionalCase:
        case = self.registry.require(case_id)
        self._require_status(case, CaseStatus.DETECTED)

        case.status = CaseStatus.OPEN
        case.opened_at = _timestamp()

        self._publish(
            case,
            CaseEventType.CASE_OPENED,
            source_identity="aletheus.case_engine",
            payload={
                "case_id": case.case_id,
            },
        )

        return case

    def investigate(
        self,
        case_id: str,
    ) -> ConstitutionalCase:
        case = self.registry.require(case_id)
        self._require_status(case, CaseStatus.OPEN)

        case.status = CaseStatus.INVESTIGATING

        self._publish(
            case,
            CaseEventType.CASE_INVESTIGATION_STARTED,
            source_identity="aletheus.case_engine",
            payload={
                "case_id": case.case_id,
            },
        )

        return case

    def attach_mission(
        self,
        case_id: str,
        *,
        mission_id: str,
        mission_type: str,
    ) -> ConstitutionalCase:
        case = self.registry.require(case_id)

        if mission_type not in case.contract.permitted_mission_types:
            raise ValueError(
                f"Mission type {mission_type!r} is not permitted "
                f"for case type {case.case_type!r}."
            )

        if mission_id not in case.mission_ids:
            case.mission_ids.append(mission_id)

            self._publish(
                case,
                CaseEventType.CASE_MISSION_ATTACHED,
                source_identity="aletheus.case_engine",
                payload={
                    "case_id": case.case_id,
                    "mission_id": mission_id,
                    "mission_type": mission_type,
                },
            )

        return case

    def attach_evidence(
        self,
        case_id: str,
        *,
        evidence_type: str,
        evidence: dict[str, Any],
        source_identity: str,
    ) -> ConstitutionalCase:
        case = self.registry.require(case_id)

        if evidence_type not in case.contract.required_evidence_types:
            raise ValueError(
                f"Evidence type {evidence_type!r} is not declared by the case contract."
            )

        record = {
            "evidence_type": evidence_type,
            "source_identity": source_identity,
            "evidence": dict(evidence),
        }

        case.evidence.append(record)

        self._publish(
            case,
            CaseEventType.CASE_EVIDENCE_ATTACHED,
            source_identity=source_identity,
            payload={
                "case_id": case.case_id,
                **record,
            },
        )

        return case

    def contain(
        self,
        case_id: str,
    ) -> ConstitutionalCase:
        case = self.registry.require(case_id)

        if case.status not in {
            CaseStatus.OPEN,
            CaseStatus.INVESTIGATING,
        }:
            raise InvalidCaseTransitionError(
                "Only open or investigating cases may be contained."
            )

        case.status = CaseStatus.CONTAINED

        self._publish(
            case,
            CaseEventType.CASE_CONTAINED,
            source_identity="aletheus.conclave",
            payload={
                "case_id": case.case_id,
            },
        )

        return case

    def resolve(
        self,
        case_id: str,
        *,
        authority: str = "aletheus.council",
    ) -> ConstitutionalCase:
        case = self.registry.require(case_id)

        if case.status not in {
            CaseStatus.CONTAINED,
            CaseStatus.RECOVERING,
            CaseStatus.INVESTIGATING,
        }:
            raise InvalidCaseTransitionError("Case is not eligible for resolution.")

        evidence_types = {item["evidence_type"] for item in case.evidence}

        missing = set(case.contract.required_evidence_types) - evidence_types

        if missing:
            raise ValueError(
                "Case cannot resolve; evidence is missing: "
                + ", ".join(sorted(missing))
            )

        case.status = CaseStatus.RESOLVED
        case.resolved_at = _timestamp()

        self._publish(
            case,
            CaseEventType.CASE_RESOLVED,
            source_identity=authority,
            payload={
                "case_id": case.case_id,
                "closure_criteria": (case.contract.closure_criteria),
            },
            certified=True,
        )

        return case

    def verify(
        self,
        case_id: str,
        *,
        authority: str = "aletheus.watch_tower",
    ) -> ConstitutionalCase:
        case = self.registry.require(case_id)
        self._require_status(case, CaseStatus.RESOLVED)

        case.status = CaseStatus.VERIFIED
        case.verified_at = _timestamp()

        self._publish(
            case,
            CaseEventType.CASE_VERIFIED,
            source_identity=authority,
            payload={
                "case_id": case.case_id,
            },
            certified=True,
        )

        return case

    def close(
        self,
        case_id: str,
        *,
        authority: str = "aletheus.council",
    ) -> ConstitutionalCase:
        case = self.registry.require(case_id)
        self._require_status(case, CaseStatus.VERIFIED)

        case.status = CaseStatus.CLOSED
        case.closed_at = _timestamp()

        self._publish(
            case,
            CaseEventType.CASE_CLOSED,
            source_identity=authority,
            payload={
                "case_id": case.case_id,
            },
            certified=True,
        )

        return case

    def history(
        self,
        case_id: str,
    ) -> tuple[ConstitutionalEvent, ...]:
        case = self.registry.require(case_id)

        return self.fabric.events(correlation_id=case.correlation_id)

    def _publish(
        self,
        case: ConstitutionalCase,
        event_type: CaseEventType,
        *,
        source_identity: str,
        payload: dict[str, Any],
        certified: bool = False,
    ) -> ConstitutionalEvent:
        causation_id = case.event_ids[-1] if case.event_ids else None

        event = ConstitutionalEvent.create(
            event_type,
            source_identity,
            correlation_id=case.correlation_id,
            causation_id=causation_id,
            payload=payload,
            certified=certified,
            tags=("case", case.case_type),
        )

        case.event_ids.append(event.event_id)
        self.fabric.publish(event)
        return event

    @staticmethod
    def _require_status(
        case: ConstitutionalCase,
        expected: CaseStatus,
    ) -> None:
        if case.status != expected:
            raise InvalidCaseTransitionError(
                f"Case {case.case_id!r} is "
                f"{case.status.value!r}; expected "
                f"{expected.value!r}."
            )

    def health(self) -> dict[str, Any]:
        return {
            "name": "Constitutional Case Engine™",
            "version": self.VERSION,
            "status": "online",
            **self.registry.statistics(),
        }
