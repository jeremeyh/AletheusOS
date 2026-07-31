"""Multiplicitous Intelligence Mesh™."""

from __future__ import annotations

from collections.abc import Callable
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)
from typing import Any, Protocol

from .convergence import (
    ConstitutionalConvergenceEngine,
)
from .models import (
    CognitiveSignal,
    CognitiveSignalType,
    EngineContribution,
    MeshExecutionReport,
    VirtueContext,
    new_cognition_id,
)
from .virtues import (
    ConstitutionalVirtuesFramework,
)


class CognitiveParticipant(Protocol):
    """Contract implemented by specialized cognitive participants."""

    engine_id: str

    def evaluate(
        self,
        payload: dict[str, Any],
    ) -> EngineContribution: ...


SignalObserver = Callable[
    [CognitiveSignal],
    None,
]


class DuplicateCognitiveParticipantError(ValueError):
    pass


class MultiplicitousIntelligenceMesh:
    """
    Execute specialized cognitive participants cooperatively and in parallel.

    The mesh does not force agreement. It gathers independent contributions,
    preserves failures and dissent, and delegates synthesis to Constitutional
    Convergence™.
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        convergence: (ConstitutionalConvergenceEngine | None) = None,
        virtues: (ConstitutionalVirtuesFramework | None) = None,
        max_workers: int | None = None,
        observer: SignalObserver | None = None,
    ) -> None:
        self.convergence = convergence or ConstitutionalConvergenceEngine()

        self.virtues = virtues or ConstitutionalVirtuesFramework()

        self.max_workers = max_workers
        self.observer = observer

        self._participants: dict[
            str,
            CognitiveParticipant,
        ] = {}

        self._executions = 0
        self._participant_failures = 0

    def register(
        self,
        participant: CognitiveParticipant,
        *,
        replace: bool = False,
    ) -> CognitiveParticipant:
        engine_id = participant.engine_id

        if engine_id in self._participants and not replace:
            raise DuplicateCognitiveParticipantError(
                f"Cognitive participant {engine_id!r} is already registered."
            )

        self._participants[engine_id] = participant

        return participant

    def get(
        self,
        engine_id: str,
    ) -> CognitiveParticipant | None:
        return self._participants.get(engine_id)

    def list(
        self,
    ) -> tuple[CognitiveParticipant, ...]:
        return tuple(self._participants.values())

    def execute(
        self,
        *,
        assertion_key: str,
        payload: dict[str, Any],
        virtue_context: VirtueContext | None = None,
    ) -> MeshExecutionReport:
        cognition_id = new_cognition_id()
        signals: list[CognitiveSignal] = []

        self._emit(
            signals,
            CognitiveSignal(
                signal_type=(CognitiveSignalType.MESH_STARTED),
                cognition_id=cognition_id,
                message=("Multiplicitous cognition began."),
                payload={
                    "assertion_key": assertion_key,
                    "participants": sorted(self._participants),
                },
            ),
        )

        contributions: list[EngineContribution] = []

        failures: list[dict[str, str]] = []

        worker_count = self.max_workers or max(
            1,
            len(self._participants),
        )

        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            futures = {}

            for participant in self._participants.values():
                self._emit(
                    signals,
                    CognitiveSignal(
                        signal_type=(CognitiveSignalType.ENGINE_STARTED),
                        cognition_id=cognition_id,
                        engine_id=(participant.engine_id),
                        message=("Cognitive participant started."),
                    ),
                )

                future = executor.submit(
                    participant.evaluate,
                    dict(payload),
                )

                futures[future] = participant

            for future in as_completed(futures):
                participant = futures[future]

                try:
                    contribution = future.result()

                except Exception as exc:
                    self._participant_failures += 1

                    failure = {
                        "engine_id": (participant.engine_id),
                        "error": str(exc),
                    }

                    failures.append(failure)

                    self._emit(
                        signals,
                        CognitiveSignal(
                            signal_type=(CognitiveSignalType.ENGINE_FAILED),
                            cognition_id=(cognition_id),
                            engine_id=(participant.engine_id),
                            message=str(exc),
                            payload=failure,
                        ),
                    )

                    continue

                if contribution.engine_id != participant.engine_id:
                    raise ValueError(
                        "Participant contribution engine_id "
                        "does not match the registered participant."
                    )

                contributions.append(contribution)

                self._emit(
                    signals,
                    CognitiveSignal(
                        signal_type=(CognitiveSignalType.ENGINE_COMPLETED),
                        cognition_id=cognition_id,
                        engine_id=(participant.engine_id),
                        magnitude=(contribution.confidence),
                        message=("Cognitive participant completed."),
                        payload={
                            "stance": (contribution.stance.value),
                            "confidence": (contribution.confidence),
                            "evidence_count": (contribution.evidence_count),
                        },
                    ),
                )

        ordered_contributions = tuple(
            sorted(
                contributions,
                key=lambda item: item.engine_id,
            )
        )

        self._emit(
            signals,
            CognitiveSignal(
                signal_type=(CognitiveSignalType.CONVERGENCE_STARTED),
                cognition_id=cognition_id,
                message=("Constitutional convergence began."),
            ),
        )

        convergence = self.convergence.converge(
            assertion_key=assertion_key,
            contributions=ordered_contributions,
        )

        self._emit(
            signals,
            CognitiveSignal(
                signal_type=(CognitiveSignalType.CONVERGENCE_COMPLETED),
                cognition_id=cognition_id,
                magnitude=convergence.confidence,
                message=convergence.explanation,
                payload={
                    "state": convergence.state.value,
                    "dominant_stance": (
                        convergence.dominant_stance.value
                        if convergence.dominant_stance
                        else None
                    ),
                    "dissent_count": len(convergence.dissent),
                },
            ),
        )

        resolved_virtue_context = virtue_context or self._derive_virtue_context(
            contributions=(ordered_contributions),
            failures=tuple(failures),
            convergence_confidence=(convergence.confidence),
        )

        virtue_assessment = self.virtues.evaluate(resolved_virtue_context)

        self._emit(
            signals,
            CognitiveSignal(
                signal_type=(CognitiveSignalType.VIRTUES_EVALUATED),
                cognition_id=cognition_id,
                magnitude=(virtue_assessment.score),
                message=("Constitutional virtues evaluated."),
                payload={
                    "passed": (virtue_assessment.passed),
                    "violations": [
                        item.virtue.value for item in (virtue_assessment.violations)
                    ],
                },
            ),
        )

        self._emit(
            signals,
            CognitiveSignal(
                signal_type=(CognitiveSignalType.MESH_COMPLETED),
                cognition_id=cognition_id,
                magnitude=(convergence.confidence),
                message=("Multiplicitous cognition completed."),
            ),
        )

        self._executions += 1

        return MeshExecutionReport(
            cognition_id=cognition_id,
            assertion_key=assertion_key,
            contributions=ordered_contributions,
            failures=tuple(failures),
            convergence=convergence,
            virtues=virtue_assessment,
            signals=tuple(signals),
        )

    def _derive_virtue_context(
        self,
        *,
        contributions: tuple[
            EngineContribution,
            ...,
        ],
        failures: tuple[
            dict[str, str],
            ...,
        ],
        convergence_confidence: float,
    ) -> VirtueContext:
        evidence_supported = bool(contributions) and any(
            contribution.evidence_count > 0 or contribution.evidence
            for contribution in contributions
        )

        provenance_complete = all(
            all(
                bool(evidence.get("source") or evidence.get("provenance"))
                for evidence in contribution.evidence
            )
            for contribution in contributions
            if contribution.evidence
        )

        return VirtueContext(
            evidence_supported=(evidence_supported),
            provenance_complete=(provenance_complete),
            uncertainty_disclosed=(convergence_confidence < 1.0 or not failures),
            human_impact_considered=True,
            communication_respectful=True,
            enduring_good_considered=True,
            rules_applied_consistently=True,
            long_term_consequences_considered=True,
            fabrication_detected=False,
            metadata={
                "derived": True,
                "participant_failures": len(failures),
            },
        )

    def _emit(
        self,
        signals: list[CognitiveSignal],
        signal: CognitiveSignal,
    ) -> None:
        signals.append(signal)

        if self.observer is not None:
            self.observer(signal)

    def health(self) -> dict:
        return {
            "name": ("Multiplicitous Intelligence Mesh™"),
            "version": self.VERSION,
            "status": ("degraded" if self._participant_failures else "online"),
            "participants": len(self._participants),
            "participant_ids": sorted(self._participants),
            "executions": self._executions,
            "participant_failures": (self._participant_failures),
            "convergence": (self.convergence.health()),
            "virtues": self.virtues.health(),
        }
