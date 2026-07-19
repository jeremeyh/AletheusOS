"""Tetra Institutional Mission Engine™."""

from __future__ import annotations

from typing import Any

from aletheus.constitutional_events import (
    ConstitutionalEvent,
    ConstitutionalEventFabric,
)

from .events import (
    TimeEventType,
    register_time_event_types,
)
from .graph import MissionPhaseGraph
from .models import (
    MissionPhaseState,
    MissionTemporalState,
    PhaseStatus,
)


class InvalidPhaseTransitionError(ValueError):
    pass


class TetraInstitutionalMissionEngine:
    """
    TIME™

    Constitutional relative-time authority for mission sequencing.

    TIME reasons about:
    - causal dependencies,
    - phase eligibility,
    - institutional participation,
    - evidence completion,
    - relative execution position.

    It does not reason about wall-clock time.
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        fabric: ConstitutionalEventFabric,
    ) -> None:
        self.fabric = fabric
        self._graphs: dict[str, MissionPhaseGraph] = {}
        self._states: dict[str, MissionTemporalState] = {}

        register_time_event_types(
            self.fabric.registry
        )

    def attach_graph(
        self,
        *,
        mission_id: str,
        correlation_id: str,
        graph: MissionPhaseGraph,
    ) -> MissionTemporalState:
        if mission_id in self._graphs:
            raise ValueError(
                f"Mission {mission_id!r} already has a phase graph."
            )

        graph.validate()

        state = MissionTemporalState(
            mission_id=mission_id,
            correlation_id=correlation_id,
            phases={
                contract.phase_id: MissionPhaseState(
                    phase_id=contract.phase_id
                )
                for contract in graph.list()
            },
        )

        self._graphs[mission_id] = graph
        self._states[mission_id] = state

        self._publish(
            state,
            TimeEventType.MISSION_PHASE_GRAPH_ATTACHED,
            payload={
                "mission_id": mission_id,
                "graph": [
                    contract.to_dict()
                    for contract in graph.ordered()
                ],
            },
        )

        self._refresh_eligibility(mission_id)
        return state

    def state(
        self,
        mission_id: str,
    ) -> MissionTemporalState:
        try:
            return self._states[mission_id]
        except KeyError as exc:
            raise KeyError(
                f"TIME has no state for mission {mission_id!r}."
            ) from exc

    def graph(
        self,
        mission_id: str,
    ) -> MissionPhaseGraph:
        try:
            return self._graphs[mission_id]
        except KeyError as exc:
            raise KeyError(
                f"TIME has no graph for mission {mission_id!r}."
            ) from exc

    def eligible_phases(
        self,
        mission_id: str,
    ) -> tuple[str, ...]:
        state = self.state(mission_id)
        self._refresh_eligibility(mission_id)

        return tuple(
            contract.phase_id
            for contract in self.graph(mission_id).ordered()
            if state.phases[contract.phase_id].status
            == PhaseStatus.ELIGIBLE
        )

    def join(
        self,
        mission_id: str,
        *,
        phase_id: str,
        institution_id: str,
    ) -> MissionPhaseState:
        graph = self.graph(mission_id)
        state = self.state(mission_id)
        contract = graph.require(phase_id)
        phase = state.phases[phase_id]

        if institution_id not in (
            contract.participating_institutions
        ):
            raise ValueError(
                f"Institution {institution_id!r} is not authorized "
                f"for phase {phase_id!r}."
            )

        if institution_id not in (
            phase.participating_institutions
        ):
            phase.participating_institutions.append(
                institution_id
            )

            event = self._publish(
                state,
                TimeEventType.MISSION_PHASE_PARTICIPANT_JOINED,
                payload={
                    "mission_id": mission_id,
                    "phase_id": phase_id,
                    "institution_id": institution_id,
                },
                source_identity=institution_id,
            )
            phase.event_ids.append(event.event_id)

        return phase

    def start_phase(
        self,
        mission_id: str,
        phase_id: str,
    ) -> MissionPhaseState:
        state = self.state(mission_id)
        contract = self.graph(mission_id).require(phase_id)
        phase = state.phases[phase_id]

        self._refresh_eligibility(mission_id)

        if phase.status != PhaseStatus.ELIGIBLE:
            raise InvalidPhaseTransitionError(
                f"Phase {phase_id!r} is {phase.status.value!r}; "
                "expected 'eligible'."
            )

        missing = set(
            contract.participating_institutions
        ) - set(phase.participating_institutions)

        if missing:
            raise ValueError(
                "Phase cannot start; required institutions "
                "have not joined: "
                + ", ".join(sorted(missing))
            )

        phase.status = PhaseStatus.RUNNING
        phase.attempts += 1

        state.relative_cursor += 1
        phase.relative_position = state.relative_cursor

        event = self._publish(
            state,
            TimeEventType.MISSION_PHASE_STARTED,
            payload={
                "mission_id": mission_id,
                "phase_id": phase_id,
                "relative_position": phase.relative_position,
                "attempt": phase.attempts,
            },
        )
        phase.event_ids.append(event.event_id)

        return phase

    def attach_evidence(
        self,
        mission_id: str,
        *,
        phase_id: str,
        evidence_type: str,
        evidence: dict[str, Any],
        source_identity: str,
    ) -> MissionPhaseState:
        graph = self.graph(mission_id)
        state = self.state(mission_id)
        contract = graph.require(phase_id)
        phase = state.phases[phase_id]

        if evidence_type not in contract.required_evidence_types:
            raise ValueError(
                f"Evidence type {evidence_type!r} is not declared "
                f"for phase {phase_id!r}."
            )

        record = {
            "evidence_type": evidence_type,
            "source_identity": source_identity,
            "evidence": dict(evidence),
        }

        phase.evidence.append(record)

        event = self._publish(
            state,
            TimeEventType.MISSION_PHASE_EVIDENCE_ATTACHED,
            payload={
                "mission_id": mission_id,
                "phase_id": phase_id,
                **record,
            },
            source_identity=source_identity,
        )
        phase.event_ids.append(event.event_id)

        return phase

    def complete_phase(
        self,
        mission_id: str,
        phase_id: str,
    ) -> MissionPhaseState:
        graph = self.graph(mission_id)
        state = self.state(mission_id)
        contract = graph.require(phase_id)
        phase = state.phases[phase_id]

        if phase.status != PhaseStatus.RUNNING:
            raise InvalidPhaseTransitionError(
                f"Phase {phase_id!r} is {phase.status.value!r}; "
                "expected 'running'."
            )

        missing_institutions = set(
            contract.participating_institutions
        ) - set(phase.participating_institutions)

        if missing_institutions:
            raise ValueError(
                "Phase cannot complete; institutional "
                "participation is missing: "
                + ", ".join(sorted(missing_institutions))
            )

        missing_evidence = set(
            contract.required_evidence_types
        ) - phase.evidence_types()

        if missing_evidence:
            raise ValueError(
                "Phase cannot complete; evidence is missing: "
                + ", ".join(sorted(missing_evidence))
            )

        phase.status = PhaseStatus.COMPLETED
        state.completed_order.append(phase_id)

        event = self._publish(
            state,
            TimeEventType.MISSION_PHASE_COMPLETED,
            payload={
                "mission_id": mission_id,
                "phase_id": phase_id,
                "relative_position": phase.relative_position,
                "completion_criteria": (
                    contract.completion_criteria
                ),
            },
        )
        phase.event_ids.append(event.event_id)

        self._refresh_eligibility(mission_id)
        self._publish_sequence_completion_if_ready(
            mission_id
        )

        return phase

    def fail_phase(
        self,
        mission_id: str,
        phase_id: str,
        *,
        reason: str,
    ) -> MissionPhaseState:
        state = self.state(mission_id)
        phase = state.phases[phase_id]

        if phase.status not in {
            PhaseStatus.RUNNING,
            PhaseStatus.ELIGIBLE,
            PhaseStatus.WAITING,
        }:
            raise InvalidPhaseTransitionError(
                f"Phase {phase_id!r} cannot fail from "
                f"{phase.status.value!r}."
            )

        phase.status = PhaseStatus.FAILED
        phase.failures.append(reason)
        state.failed = True

        event = self._publish(
            state,
            TimeEventType.MISSION_PHASE_FAILED,
            payload={
                "mission_id": mission_id,
                "phase_id": phase_id,
                "reason": reason,
            },
        )
        phase.event_ids.append(event.event_id)

        self._refresh_eligibility(mission_id)
        return phase

    def sequence_completed(
        self,
        mission_id: str,
    ) -> bool:
        state = self.state(mission_id)

        return (
            not state.failed
            and bool(state.phases)
            and all(
                phase.status
                in {
                    PhaseStatus.COMPLETED,
                    PhaseStatus.SKIPPED,
                }
                for phase in state.phases.values()
            )
        )

    def history(
        self,
        mission_id: str,
    ) -> tuple[ConstitutionalEvent, ...]:
        state = self.state(mission_id)

        return self.fabric.events(
            correlation_id=state.correlation_id
        )

    def _refresh_eligibility(
        self,
        mission_id: str,
    ) -> None:
        graph = self.graph(mission_id)
        state = self.state(mission_id)

        for contract in graph.ordered():
            phase = state.phases[contract.phase_id]

            if phase.status in {
                PhaseStatus.RUNNING,
                PhaseStatus.COMPLETED,
                PhaseStatus.FAILED,
                PhaseStatus.SKIPPED,
            }:
                continue

            dependency_states = [
                state.phases[dependency].status
                for dependency in contract.dependencies
            ]

            if any(
                status == PhaseStatus.FAILED
                for status in dependency_states
            ):
                if phase.status != PhaseStatus.BLOCKED:
                    phase.status = PhaseStatus.BLOCKED
                    event = self._publish(
                        state,
                        TimeEventType.MISSION_PHASE_BLOCKED,
                        payload={
                            "mission_id": mission_id,
                            "phase_id": contract.phase_id,
                            "dependencies": (
                                contract.dependencies
                            ),
                        },
                    )
                    phase.event_ids.append(event.event_id)

                continue

            eligible = all(
                status
                in {
                    PhaseStatus.COMPLETED,
                    PhaseStatus.SKIPPED,
                }
                for status in dependency_states
            )

            new_status = (
                PhaseStatus.ELIGIBLE
                if eligible
                else PhaseStatus.PENDING
            )

            if (
                new_status == PhaseStatus.ELIGIBLE
                and phase.status != PhaseStatus.ELIGIBLE
            ):
                phase.status = new_status

                event = self._publish(
                    state,
                    TimeEventType.MISSION_PHASE_ELIGIBLE,
                    payload={
                        "mission_id": mission_id,
                        "phase_id": contract.phase_id,
                        "dependencies": contract.dependencies,
                    },
                )
                phase.event_ids.append(event.event_id)
            else:
                phase.status = new_status

    def _publish_sequence_completion_if_ready(
        self,
        mission_id: str,
    ) -> None:
        if not self.sequence_completed(mission_id):
            return

        state = self.state(mission_id)

        existing = self.fabric.events(
            event_type=(
                TimeEventType
                .MISSION_TEMPORAL_SEQUENCE_COMPLETED
            ),
            correlation_id=state.correlation_id,
        )

        if existing:
            return

        self._publish(
            state,
            TimeEventType.MISSION_TEMPORAL_SEQUENCE_COMPLETED,
            payload={
                "mission_id": mission_id,
                "completed_order": list(
                    state.completed_order
                ),
            },
        )

    def _publish(
        self,
        state: MissionTemporalState,
        event_type: TimeEventType,
        *,
        payload: dict[str, Any],
        source_identity: str = "aletheus.time",
    ) -> ConstitutionalEvent:
        correlated_events = self.fabric.events(
            correlation_id=state.correlation_id
        )

        causation_id = (
            correlated_events[-1].event_id
            if correlated_events
            else None
        )

        event = ConstitutionalEvent.create(
            event_type,
            source_identity,
            correlation_id=state.correlation_id,
            causation_id=causation_id,
            payload=payload,
            tags=("time", "relative-time", "mission-phase"),
        )

        self.fabric.publish(event)
        return event

    def health(self) -> dict[str, Any]:
        phase_states = [
            phase
            for state in self._states.values()
            for phase in state.phases.values()
        ]

        return {
            "name": "Tetra Institutional Mission Engine™",
            "abbreviation": "TIME™",
            "version": self.VERSION,
            "status": "online",
            "missions": len(self._states),
            "phases": len(phase_states),
            "completed_phases": sum(
                phase.status == PhaseStatus.COMPLETED
                for phase in phase_states
            ),
            "failed_phases": sum(
                phase.status == PhaseStatus.FAILED
                for phase in phase_states
            ),
            "blocked_phases": sum(
                phase.status == PhaseStatus.BLOCKED
                for phase in phase_states
            ),
        }
