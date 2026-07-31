"""Constitutional Scenario Engine™."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from aletheus.constitutional_cognition import (
    ConvergenceState,
    MultiplicitousIntelligenceMesh,
    VirtueContext,
)

from .comparison import (
    compare_scenario_outcomes,
)
from .instrumentation import (
    ScenarioInstrumentPublisher,
)
from .models import (
    ScenarioComparison,
    ScenarioDefinition,
    ScenarioOutcome,
    ScenarioStatus,
    new_scenario_run_id,
    utc_now,
)
from .registry import (
    ConstitutionalScenarioRegistry,
)

MetricProjector = Callable[
    [
        ScenarioDefinition,
        dict[str, Any],
        Any,
    ],
    dict[str, float],
]


class ConstitutionalScenarioEngine:
    """
    Evaluate explicit hypothetical branches through Constitutional Cognition™.

    Scenarios never represent certainty. Assumptions remain explicit, dissent
    remains visible, and confidence remains bounded by available evidence.
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        mesh: MultiplicitousIntelligenceMesh,
        registry: (ConstitutionalScenarioRegistry | None) = None,
        instruments: (ScenarioInstrumentPublisher | None) = None,
        metric_projector: (MetricProjector | None) = None,
    ) -> None:
        self.mesh = mesh

        self.registry = registry or ConstitutionalScenarioRegistry()

        self.instruments = instruments

        self.metric_projector = metric_projector or self._default_metric_projector

        self._runs = 0
        self._failures = 0

    def register(
        self,
        definition: ScenarioDefinition,
    ) -> ScenarioDefinition:
        return self.registry.register(definition)

    def run(
        self,
        scenario_id: str,
        *,
        context: dict[str, Any] | None = None,
        virtue_context: (VirtueContext | None) = None,
    ) -> ScenarioOutcome:
        definition = self.registry.require(scenario_id)

        run_id = new_scenario_run_id()
        started_at = utc_now()

        if self.instruments is not None:
            self.instruments.started(
                scenario_id=scenario_id,
                run_id=run_id,
            )

        payload = {
            "scenario": definition.to_dict(),
            "assumptions": (definition.assumption_map()),
            "context": dict(context or {}),
        }

        try:
            report = self.mesh.execute(
                assertion_key=(definition.assertion_key),
                payload=payload,
                virtue_context=virtue_context,
            )

            metrics = self.metric_projector(
                definition,
                payload,
                report,
            )

            status = self._status_from_report(report)

            outcome = ScenarioOutcome(
                scenario_id=scenario_id,
                run_id=run_id,
                status=status,
                assertion_key=(definition.assertion_key),
                confidence=(report.convergence.confidence),
                dominant_stance=(
                    report.convergence.dominant_stance.value
                    if (report.convergence.dominant_stance is not None)
                    else None
                ),
                dissent_count=len(report.convergence.dissent),
                virtue_score=(report.virtues.score),
                metrics=metrics,
                report=report,
                started_at=started_at,
                completed_at=utc_now(),
                metadata={
                    "horizon": (definition.horizon),
                    "assumption_count": len(definition.assumptions),
                },
            )

            self.registry.record_outcome(outcome)

            if self.instruments is not None:
                self.instruments.completed(outcome)

            self._runs += 1
            return outcome

        except Exception:
            self._failures += 1
            raise

    def compare(
        self,
        *,
        baseline_scenario_id: str,
        compared_scenario_id: str,
    ) -> ScenarioComparison:
        baseline_definition = self.registry.require(baseline_scenario_id)

        compared_definition = self.registry.require(compared_scenario_id)

        baseline_outcome = self.registry.latest_outcome(baseline_scenario_id)

        compared_outcome = self.registry.latest_outcome(compared_scenario_id)

        if baseline_outcome is None:
            raise ValueError("Baseline scenario has not been run.")

        if compared_outcome is None:
            raise ValueError("Compared scenario has not been run.")

        return compare_scenario_outcomes(
            baseline_definition=(baseline_definition),
            baseline_outcome=(baseline_outcome),
            compared_definition=(compared_definition),
            compared_outcome=(compared_outcome),
        )

    @staticmethod
    def _status_from_report(
        report,
    ) -> ScenarioStatus:
        state = report.convergence.state

        if state == ConvergenceState.CONTESTED:
            return ScenarioStatus.CONTESTED

        if state == ConvergenceState.INSUFFICIENT:
            return ScenarioStatus.INSUFFICIENT

        if state == ConvergenceState.FAILED:
            return ScenarioStatus.FAILED

        if not report.virtues.passed:
            return ScenarioStatus.CONTESTED

        return ScenarioStatus.COMPLETED

    @staticmethod
    def _default_metric_projector(
        definition: ScenarioDefinition,
        payload: dict[str, Any],
        report,
    ) -> dict[str, float]:
        return {
            "confidence": (report.convergence.confidence),
            "virtue_alignment": (report.virtues.score),
            "dissent_count": float(len(report.convergence.dissent)),
            "assumption_count": float(len(definition.assumptions)),
        }

    def health(self) -> dict:
        return {
            "name": ("Constitutional Scenario Engine™"),
            "version": self.VERSION,
            "status": ("degraded" if self._failures else "online"),
            "runs": self._runs,
            "failures": self._failures,
            "registry": (self.registry.health()),
            "mesh": self.mesh.health(),
            "instrumentation": (
                self.instruments.health() if self.instruments else None
            ),
        }
