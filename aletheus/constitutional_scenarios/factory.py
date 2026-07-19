"""Factories for constitutional scenarios."""

from __future__ import annotations

from typing import Any

from .models import (
    AssumptionKind,
    ScenarioAssumption,
    ScenarioDefinition,
    new_scenario_id,
)


def create_scenario(
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
    return ScenarioDefinition(
        scenario_id=new_scenario_id(),
        canonical_name=canonical_name,
        assertion_key=assertion_key,
        assumptions=tuple(
            ScenarioAssumption(
                key=key,
                value=value,
                kind=assumption_kind,
            )
            for key, value
            in assumptions.items()
        ),
        description=description,
        horizon=horizon,
        parent_scenario_id=(
            parent_scenario_id
        ),
    )
