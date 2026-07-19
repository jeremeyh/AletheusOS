"""Registry for constitutional scenarios."""

from __future__ import annotations

from .models import (
    ScenarioDefinition,
    ScenarioOutcome,
)


class DuplicateScenarioError(ValueError):
    pass


class ConstitutionalScenarioRegistry:
    VERSION = "0.1.0"

    def __init__(self) -> None:
        self._definitions: dict[
            str,
            ScenarioDefinition,
        ] = {}

        self._outcomes: dict[
            str,
            list[ScenarioOutcome],
        ] = {}

    def register(
        self,
        definition: ScenarioDefinition,
        *,
        replace: bool = False,
    ) -> ScenarioDefinition:
        scenario_id = definition.scenario_id

        if (
            scenario_id in self._definitions
            and not replace
        ):
            raise DuplicateScenarioError(
                f"Scenario {scenario_id!r} "
                "is already registered."
            )

        self._definitions[
            scenario_id
        ] = definition

        return definition

    def get(
        self,
        scenario_id: str,
    ) -> ScenarioDefinition | None:
        return self._definitions.get(
            scenario_id
        )

    def require(
        self,
        scenario_id: str,
    ) -> ScenarioDefinition:
        scenario = self.get(scenario_id)

        if scenario is None:
            raise KeyError(
                f"Unknown scenario: "
                f"{scenario_id!r}."
            )

        return scenario

    def list(
        self,
    ) -> tuple[ScenarioDefinition, ...]:
        return tuple(
            self._definitions.values()
        )

    def record_outcome(
        self,
        outcome: ScenarioOutcome,
    ) -> ScenarioOutcome:
        self.require(outcome.scenario_id)

        self._outcomes.setdefault(
            outcome.scenario_id,
            [],
        ).append(outcome)

        return outcome

    def outcomes(
        self,
        scenario_id: str,
    ) -> tuple[ScenarioOutcome, ...]:
        self.require(scenario_id)

        return tuple(
            self._outcomes.get(
                scenario_id,
                (),
            )
        )

    def latest_outcome(
        self,
        scenario_id: str,
    ) -> ScenarioOutcome | None:
        outcomes = self.outcomes(
            scenario_id
        )

        return (
            outcomes[-1]
            if outcomes
            else None
        )

    def statistics(self) -> dict:
        return {
            "scenarios": len(
                self._definitions
            ),
            "outcomes": sum(
                len(items)
                for items
                in self._outcomes.values()
            ),
            "scenario_ids": sorted(
                self._definitions
            ),
        }

    def health(self) -> dict:
        return {
            "name": (
                "Constitutional Scenario Registry™"
            ),
            "version": self.VERSION,
            "status": "online",
            **self.statistics(),
        }
