"""TIME-driven Constitutional Mission Runtime™."""

from __future__ import annotations

from typing import Any

from aletheus.constitutional_events import (
    ConstitutionalEvent,
)
from aletheus.constitutional_time import (
    TetraInstitutionalMissionEngine,
)

from .contracts import PhaseExecutionRequest
from .registry import InstitutionExecutorRegistry


class MissionRuntimeExecutionError(RuntimeError):
    pass


class ConstitutionalMissionRuntime:
    """
    Execute eligible TIME™ phases through institutional executors.

    TIME™ owns:
    - phase eligibility,
    - dependency progression,
    - evidence gates,
    - phase completion.

    Mission Runtime owns:
    - executor resolution,
    - institutional invocation,
    - semantic domain-event publication,
    - evidence return to TIME™.
    """

    VERSION = "0.2.0"

    def __init__(
        self,
        *,
        time: TetraInstitutionalMissionEngine,
        executors: InstitutionExecutorRegistry,
    ) -> None:
        self.time = time
        self.executors = executors

        self._missions_executed = 0
        self._phases_executed = 0
        self._domain_events_published = 0
        self._failures = 0

    def execute(
        self,
        *,
        mission_id: str,
        case_id: str,
        context: dict[str, Any],
    ):
        state = self.time.state(mission_id)
        graph = self.time.graph(mission_id)

        accumulated_evidence: dict[
            str,
            dict[str, Any],
        ] = {}

        while not self.time.sequence_completed(mission_id):
            eligible = self.time.eligible_phases(mission_id)

            if not eligible:
                self._failures += 1

                raise MissionRuntimeExecutionError(
                    "TIME has no eligible phase and the mission sequence is incomplete."
                )

            for phase_id in eligible:
                contract = graph.require(phase_id)

                if len(contract.participating_institutions) != 1:
                    self._failures += 1

                    raise MissionRuntimeExecutionError(
                        f"Phase {phase_id!r} currently "
                        "requires exactly one execution "
                        "institution."
                    )

                institution_id = contract.participating_institutions[0]

                self.time.join(
                    mission_id,
                    phase_id=phase_id,
                    institution_id=institution_id,
                )

                self.time.start_phase(
                    mission_id,
                    phase_id,
                )

                executor = self.executors.require(institution_id)

                request = PhaseExecutionRequest(
                    mission_id=mission_id,
                    case_id=case_id,
                    correlation_id=(state.correlation_id),
                    phase_id=phase_id,
                    institution_id=institution_id,
                    inputs={
                        **dict(context),
                        **dict(accumulated_evidence),
                    },
                    context=dict(context),
                )

                try:
                    result = executor.execute(request)

                except Exception as exc:
                    self.time.fail_phase(
                        mission_id,
                        phase_id,
                        reason=str(exc),
                    )

                    self._failures += 1
                    raise

                if not result.successful:
                    reason = result.message or "Institution execution failed."

                    self.time.fail_phase(
                        mission_id,
                        phase_id,
                        reason=reason,
                    )

                    self._failures += 1

                    raise MissionRuntimeExecutionError(reason)

                domain_event = self._publish_domain_event(
                    request=request,
                    result=result,
                )

                evidence = dict(result.evidence)

                if domain_event is not None:
                    evidence["domain_event_id"] = domain_event.event_id
                    evidence["domain_event_type"] = domain_event.event_type.value

                self.time.attach_evidence(
                    mission_id,
                    phase_id=phase_id,
                    evidence_type=(result.evidence_type),
                    evidence=evidence,
                    source_identity=(result.institution_id),
                )

                self.time.complete_phase(
                    mission_id,
                    phase_id,
                )

                accumulated_evidence[result.evidence_type] = evidence

                self._phases_executed += 1

        self._missions_executed += 1
        return state

    def _publish_domain_event(
        self,
        *,
        request: PhaseExecutionRequest,
        result,
    ) -> ConstitutionalEvent | None:
        """
        Publish the semantic event produced by the institution.

        This occurs before TIME™ evidence attachment and phase completion so
        the constitutional history reflects:

        Institution execution
            → semantic domain event
            → evidence attachment
            → phase completion
        """

        if not result.domain_event_type:
            return None

        correlated_events = self.time.fabric.events(
            correlation_id=(request.correlation_id)
        )

        causation_id = correlated_events[-1].event_id if correlated_events else None

        event = ConstitutionalEvent.create(
            result.domain_event_type,
            result.institution_id,
            correlation_id=(request.correlation_id),
            causation_id=causation_id,
            payload={
                "case_id": request.case_id,
                "mission_id": request.mission_id,
                "phase_id": request.phase_id,
                "institution_id": (result.institution_id),
                "evidence_type": (result.evidence_type),
                "evidence": dict(result.evidence),
                "entity_id": (request.context.get("entity_id")),
                "severity": (request.context.get("severity")),
            },
            evidence=(
                {
                    "evidence_type": (result.evidence_type),
                    "evidence": dict(result.evidence),
                },
            ),
            tags=(
                "institution-execution",
                request.phase_id,
                *result.domain_event_tags,
            ),
        )

        self.time.fabric.publish(event)
        self._domain_events_published += 1

        return event

    def health(self) -> dict[str, Any]:
        return {
            "name": ("Constitutional Mission Runtime™"),
            "version": self.VERSION,
            "status": ("degraded" if self._failures else "online"),
            "missions_executed": (self._missions_executed),
            "phases_executed": (self._phases_executed),
            "domain_events_published": (self._domain_events_published),
            "failures": self._failures,
            "time": self.time.health(),
            "executors": (self.executors.health()),
        }
