"""Public Constitutional Scenario Surface."""

from __future__ import annotations

from typing import Any

from aletheus.constitutional_cognition import (
    VirtueContext,
)
from aletheus.constitutional_scenarios import (
    AssumptionKind,
    ConstitutionalScenarioEngine,
    ScenarioDefinition,
    create_scenario,
)


class ScenarioSurface:
    """
    Stable application-facing interface to scenario evaluation.

    Applications define explicit assumptions and ask the platform to evaluate
    them through Constitutional Cognition™.
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        engine: ConstitutionalScenarioEngine,
    ) -> None:
        self._engine = engine

    def create(
        self,
        *,
        canonical_name: str,
        assertion_key: str,
        assumptions: dict[str, Any],
        description: str = "",
        horizon: str | None = None,
        parent_scenario_id: str | None = None,
        assumption_kind: (
            AssumptionKind
        ) = AssumptionKind.HYPOTHESIS,
    ) -> ScenarioDefinition:
        return create_scenario(
            canonical_name=canonical_name,
            assertion_key=assertion_key,
            assumptions=assumptions,
            description=description,
            horizon=horizon,
            parent_scenario_id=(
                parent_scenario_id
            ),
            assumption_kind=assumption_kind,
        )

    def register(
        self,
        definition: ScenarioDefinition,
    ) -> ScenarioDefinition:
        return self._engine.register(
            definition
        )

    def create_and_register(
        self,
        *,
        canonical_name: str,
        assertion_key: str,
        assumptions: dict[str, Any],
        description: str = "",
        horizon: str | None = None,
        parent_scenario_id: str | None = None,
        assumption_kind: (
            AssumptionKind
        ) = AssumptionKind.HYPOTHESIS,
    ) -> ScenarioDefinition:
        definition = self.create(
            canonical_name=canonical_name,
            assertion_key=assertion_key,
            assumptions=assumptions,
            description=description,
            horizon=horizon,
            parent_scenario_id=(
                parent_scenario_id
            ),
            assumption_kind=assumption_kind,
        )

        return self.register(definition)

    def get(
        self,
        scenario_id: str,
    ) -> ScenarioDefinition | None:
        return self._engine.registry.get(
            scenario_id
        )

    def require(
        self,
        scenario_id: str,
    ) -> ScenarioDefinition:
        return self._engine.registry.require(
            scenario_id
        )

    def list(
        self,
    ) -> tuple[ScenarioDefinition, ...]:
        return self._engine.registry.list()

    def run(
        self,
        scenario_id: str,
        *,
        context: dict[str, Any] | None = None,
        virtue_context: VirtueContext | None = None,
    ):
        return self._engine.run(
            scenario_id,
            context=context,
            virtue_context=virtue_context,
        )

    def compare(
        self,
        *,
        baseline_scenario_id: str,
        compared_scenario_id: str,
    ):
        return self._engine.compare(
            baseline_scenario_id=(
                baseline_scenario_id
            ),
            compared_scenario_id=(
                compared_scenario_id
            ),
        )

    def outcomes(
        self,
        scenario_id: str,
    ):
        return self._engine.registry.outcomes(
            scenario_id
        )

    def latest_outcome(
        self,
        scenario_id: str,
    ):
        return (
            self._engine
            .registry
            .latest_outcome(
                scenario_id
            )
        )

    def health(self) -> dict[str, Any]:
        return self._engine.health()
