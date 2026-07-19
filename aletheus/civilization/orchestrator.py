"""Civilization Orchestrator™ with TIME-driven mission execution."""

from __future__ import annotations

from typing import Any

from aletheus.constitutional_cases import (
    ConstitutionalCaseEngine,
    create_security_incident_case,
)
from aletheus.constitutional_events import ConstitutionalEvent
from aletheus.constitutional_events.security import (
    SecurityEventType,
)
from aletheus.constitutional_ledger import ConstitutionalLedger
from aletheus.constitutional_missions import (
    ConstitutionalMissionEngine,
    create_security_containment_mission,
)
from aletheus.constitutional_time import (
    TetraInstitutionalMissionEngine,
    security_containment_phase_graph,
)
from aletheus.mission_runtime import (
    ConstitutionalMissionRuntime,
)

from .models import CivilizationResponse


class CivilizationOrchestrator:
    """
    Coordinates Cases, Missions, TIME™, execution, and history.

    Domain events describe what happened constitutionally.

    TIME™ events describe how mission execution progressed.

    TIME™ owns phase eligibility and progression.
    Mission Runtime owns institutional dispatch.
    Case and Mission engines retain their bounded ownership.
    """

    VERSION = "0.2.1"

    def __init__(
        self,
        *,
        ledger: ConstitutionalLedger,
        case_engine: ConstitutionalCaseEngine,
        mission_engine: ConstitutionalMissionEngine,
        time: TetraInstitutionalMissionEngine,
        mission_runtime: ConstitutionalMissionRuntime,
    ) -> None:
        self.ledger = ledger
        self.case_engine = case_engine
        self.mission_engine = mission_engine
        self.time = time
        self.mission_runtime = mission_runtime

        self._responses = 0
        self._failures = 0

    def respond_to_integrity_finding(
        self,
        *,
        entity_id: str,
        severity: str,
        finding: dict[str, Any],
    ) -> CivilizationResponse:
        """
        Execute a complete TIME-driven Security Civilization response.

        The Security Incident Case owns the shared correlation identity for:

        - Case lifecycle events
        - Mission lifecycle events
        - Security domain events
        - TIME™ phase events
        - Evidence events
        - Ledger and Transtemporal history
        """

        case = create_security_incident_case(
            entity_id=entity_id,
            severity=severity,
        )

        mission = create_security_containment_mission(
            entity_id=entity_id,
            severity=severity,
        )

        mission.case_id = case.case_id
        mission.correlation_id = case.correlation_id

        try:
            self.case_engine.detect(case)
            self.case_engine.open(case.case_id)
            self.case_engine.investigate(case.case_id)

            # Preserve the canonical Security Civilization domain event.
            #
            # This event represents the originating constitutional fact.
            # It is distinct from TIME™ phase events, which describe how
            # execution progresses after the finding has been created.
            integrity_event = ConstitutionalEvent.create(
                SecurityEventType.INTEGRITY_FINDING_CREATED,
                "aletheus.watch_tower",
                correlation_id=case.correlation_id,
                causation_id=(
                    case.event_ids[-1]
                    if case.event_ids
                    else None
                ),
                payload={
                    "case_id": case.case_id,
                    "mission_id": mission.mission_id,
                    "entity_id": entity_id,
                    "severity": severity,
                    "finding": dict(finding),
                },
                evidence=(dict(finding),),
                tags=(
                    "security",
                    "integrity",
                    severity.casefold(),
                    "civilization-orchestration",
                ),
            )

            self.time.fabric.publish(integrity_event)

            self.mission_engine.create(mission)
            self.mission_engine.authorize(
                mission.mission_id
            )

            for institution_id in (
                mission.contract.required_institutions
            ):
                self.mission_engine.join(
                    mission.mission_id,
                    institution_id,
                )

                if (
                    institution_id
                    not in case.participating_institutions
                ):
                    case.participating_institutions.append(
                        institution_id
                    )

            self.case_engine.attach_mission(
                case.case_id,
                mission_id=mission.mission_id,
                mission_type=mission.mission_type,
            )

            self.mission_engine.start(
                mission.mission_id
            )

            self.time.attach_graph(
                mission_id=mission.mission_id,
                correlation_id=case.correlation_id,
                graph=security_containment_phase_graph(),
            )

            temporal_state = self.mission_runtime.execute(
                mission_id=mission.mission_id,
                case_id=case.case_id,
                context={
                    "entity_id": entity_id,
                    "severity": severity,
                    "finding": dict(finding),
                    "integrity_event_id": (
                        integrity_event.event_id
                    ),
                },
            )

            # Project phase evidence into both the bounded Mission
            # and the durable Case.
            for phase_id in temporal_state.completed_order:
                phase = temporal_state.phases[phase_id]

                for record in phase.evidence:
                    evidence_type = record[
                        "evidence_type"
                    ]
                    source_identity = record[
                        "source_identity"
                    ]
                    evidence = record["evidence"]

                    self.mission_engine.attach_evidence(
                        mission.mission_id,
                        evidence_type=evidence_type,
                        evidence=evidence,
                        source_identity=source_identity,
                    )

                    self.case_engine.attach_evidence(
                        case.case_id,
                        evidence_type=evidence_type,
                        evidence=evidence,
                        source_identity=source_identity,
                    )

            self.case_engine.contain(case.case_id)

            self.mission_engine.complete(
                mission.mission_id
            )

            self.case_engine.resolve(case.case_id)
            self.case_engine.verify(case.case_id)
            self.case_engine.close(case.case_id)

            history = self.ledger.replay_events(
                correlation_id=case.correlation_id
            )

            self._responses += 1

            return CivilizationResponse(
                case_id=case.case_id,
                mission_id=mission.mission_id,
                security_case_id=case.case_id,
                correlation_id=case.correlation_id,
                case_status=case.status.value,
                mission_status=mission.status.value,
                security_status=(
                    "stabilized"
                    if self.time.sequence_completed(
                        mission.mission_id
                    )
                    else "incomplete"
                ),
                evidence_count=len(case.evidence),
                event_count=len(history),
                metadata={
                    "entity_id": entity_id,
                    "severity": severity,
                    "integrity_event_id": (
                        integrity_event.event_id
                    ),
                    "case_missions": list(
                        case.mission_ids
                    ),
                    "institutions": list(
                        case.participating_institutions
                    ),
                    "phase_order": list(
                        temporal_state.completed_order
                    ),
                },
            )

        except Exception:
            self._failures += 1

            current = self.mission_engine.registry.get(
                mission.mission_id
            )

            if (
                current is not None
                and current.status.value
                not in {
                    "completed",
                    "archived",
                    "failed",
                }
            ):
                self.mission_engine.fail(
                    mission.mission_id,
                    (
                        "TIME-driven civilization "
                        "orchestration failed."
                    ),
                )

            raise

    def history(
        self,
        correlation_id: str,
    ):
        """Return authoritative correlated Ledger history."""

        return self.ledger.replay_events(
            correlation_id=correlation_id
        )

    def provenance(
        self,
        event_id: str,
    ):
        """Return Transtemporal provenance for one event."""

        return self.ledger.temporal_provenance(
            event_id
        )

    def health(self) -> dict[str, Any]:
        """Return composed Civilization Orchestrator health."""

        return {
            "name": "Civilization Orchestrator™",
            "version": self.VERSION,
            "status": (
                "degraded"
                if self._failures
                else "online"
            ),
            "responses": self._responses,
            "failures": self._failures,
            "case_engine": self.case_engine.health(),
            "mission_engine": self.mission_engine.health(),
            "time": self.time.health(),
            "mission_runtime": (
                self.mission_runtime.health()
            ),
        }
