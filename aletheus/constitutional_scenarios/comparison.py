"""Scenario comparison for Constitutional Scenarios™."""

from __future__ import annotations

from .models import (
    ScenarioComparison,
    ScenarioDefinition,
    ScenarioMetricDelta,
    ScenarioOutcome,
)


def compare_assumptions(
    baseline: ScenarioDefinition,
    compared: ScenarioDefinition,
) -> dict[str, dict]:
    baseline_values = baseline.assumption_map()
    compared_values = compared.assumption_map()

    keys = set(baseline_values) | set(compared_values)

    changed: dict[str, dict] = {}

    for key in sorted(keys):
        baseline_value = baseline_values.get(key)
        compared_value = compared_values.get(key)

        if baseline_value == compared_value:
            continue

        changed[key] = {
            "baseline": baseline_value,
            "scenario": compared_value,
        }

    return changed


def compare_scenario_outcomes(
    *,
    baseline_definition: ScenarioDefinition,
    baseline_outcome: ScenarioOutcome,
    compared_definition: ScenarioDefinition,
    compared_outcome: ScenarioOutcome,
) -> ScenarioComparison:
    metric_names = set(baseline_outcome.metrics) | set(compared_outcome.metrics)

    deltas = []

    for metric in sorted(metric_names):
        baseline_value = float(
            baseline_outcome.metrics.get(
                metric,
                0.0,
            )
        )

        scenario_value = float(
            compared_outcome.metrics.get(
                metric,
                0.0,
            )
        )

        absolute_delta = scenario_value - baseline_value

        percentage_delta = (
            round(
                (absolute_delta / baseline_value) * 100.0,
                4,
            )
            if baseline_value != 0
            else None
        )

        deltas.append(
            ScenarioMetricDelta(
                metric=metric,
                baseline_value=baseline_value,
                scenario_value=scenario_value,
                absolute_delta=round(
                    absolute_delta,
                    4,
                ),
                percentage_delta=(percentage_delta),
            )
        )

    return ScenarioComparison(
        baseline_scenario_id=(baseline_definition.scenario_id),
        compared_scenario_id=(compared_definition.scenario_id),
        confidence_delta=round(
            (compared_outcome.confidence - baseline_outcome.confidence),
            4,
        ),
        virtue_delta=round(
            (compared_outcome.virtue_score - baseline_outcome.virtue_score),
            4,
        ),
        metric_deltas=tuple(deltas),
        changed_assumptions=(
            compare_assumptions(
                baseline_definition,
                compared_definition,
            )
        ),
    )
