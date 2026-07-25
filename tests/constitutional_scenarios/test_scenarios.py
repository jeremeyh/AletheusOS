from __future__ import annotations

import pytest

from aletheus.constitutional_cognition import (
    ContributionStance,
    EngineContribution,
    FunctionalCognitiveParticipant,
    MultiplicitousIntelligenceMesh,
)
from aletheus.constitutional_instrumentation import (
    build_cognition_instrumentation,
)
from aletheus.constitutional_scenarios import (
    SCENARIO_ACTIVITY_ID,
    SCENARIO_CONFIDENCE_ID,
    SCENARIO_VIRTUE_ID,
    ConstitutionalScenarioEngine,
    DuplicateScenarioError,
    ScenarioInstrumentPublisher,
    ScenarioStatus,
    create_scenario,
)

ASSERTION = "card.future_value.increases"


def participant(
    engine_id: str,
    stance: ContributionStance,
    confidence_resolver,
):
    def evaluate(payload):
        confidence = confidence_resolver(
            payload
        )

        return EngineContribution(
            engine_id=engine_id,
            assertion_key=ASSERTION,
            stance=stance,
            confidence=confidence,
            evidence_count=1,
            evidence=(
                {
                    "source": (
                        f"{engine_id}.evidence"
                    ),
                },
            ),
        )

    return FunctionalCognitiveParticipant(
        engine_id=engine_id,
        evaluator=evaluate,
    )


def build_engine():
    bus, bridge = (
        build_cognition_instrumentation()
    )

    mesh = MultiplicitousIntelligenceMesh(
        observer=bridge
    )

    def grade_confidence(payload):
        grade = payload[
            "assumptions"
        ].get("grade")

        return {
            "raw": 0.55,
            "PSA 8": 0.65,
            "PSA 9": 0.80,
            "PSA 10": 0.95,
        }.get(grade, 0.50)

    mesh.register(
        participant(
            "prediction",
            ContributionStance.SUPPORT,
            grade_confidence,
        )
    )

    mesh.register(
        participant(
            "market",
            ContributionStance.SUPPORT,
            lambda payload: 0.85,
        )
    )

    mesh.register(
        participant(
            "risk",
            ContributionStance.CHALLENGE,
            lambda payload: 0.25,
        )
    )

    publisher = ScenarioInstrumentPublisher(
        bus=bus
    )

    def project_metrics(
        definition,
        payload,
        report,
    ):
        grade = payload[
            "assumptions"
        ].get("grade")

        projected_value = {
            "raw": 900.0,
            "PSA 8": 1050.0,
            "PSA 9": 1450.0,
            "PSA 10": 2400.0,
        }[grade]

        return {
            "projected_value": (
                projected_value
            ),
            "confidence": (
                report.convergence.confidence
            ),
            "dissent_count": float(
                len(
                    report.convergence.dissent
                )
            ),
        }

    engine = ConstitutionalScenarioEngine(
        mesh=mesh,
        instruments=publisher,
        metric_projector=project_metrics,
    )

    return engine, bus


def test_registers_explicit_scenario():
    engine, _ = build_engine()

    scenario = create_scenario(
        canonical_name="PSA 10 Scenario",
        assertion_key=ASSERTION,
        assumptions={
            "grade": "PSA 10",
            "horizon_years": 4,
        },
        horizon="4 years",
    )

    engine.register(scenario)

    stored = engine.registry.require(
        scenario.scenario_id
    )

    assert (
        stored.assumption_map()["grade"]
        == "PSA 10"
    )


def test_duplicate_scenario_is_rejected():
    engine, _ = build_engine()

    scenario = create_scenario(
        canonical_name="Raw Scenario",
        assertion_key=ASSERTION,
        assumptions={
            "grade": "raw",
        },
    )

    engine.register(scenario)

    with pytest.raises(
        DuplicateScenarioError
    ):
        engine.register(scenario)


def test_scenario_runs_through_cognition():
    engine, _ = build_engine()

    scenario = create_scenario(
        canonical_name="PSA 9 Scenario",
        assertion_key=ASSERTION,
        assumptions={
            "grade": "PSA 9",
            "horizon_years": 4,
        },
    )

    engine.register(scenario)

    outcome = engine.run(
        scenario.scenario_id
    )

    assert outcome.status == (
        ScenarioStatus.COMPLETED
    )

    assert (
        outcome.metrics[
            "projected_value"
        ]
        == 1450.0
    )

    assert outcome.confidence > 0
    assert outcome.virtue_score == 1.0
    assert outcome.dissent_count == 1


def test_grade_scenarios_produce_different_outcomes():
    engine, _ = build_engine()

    raw = create_scenario(
        canonical_name="Raw Scenario",
        assertion_key=ASSERTION,
        assumptions={
            "grade": "raw",
        },
    )

    psa_10 = create_scenario(
        canonical_name="PSA 10 Scenario",
        assertion_key=ASSERTION,
        assumptions={
            "grade": "PSA 10",
        },
    )

    engine.register(raw)
    engine.register(psa_10)

    raw_outcome = engine.run(
        raw.scenario_id
    )

    psa_10_outcome = engine.run(
        psa_10.scenario_id
    )

    assert (
        psa_10_outcome.metrics[
            "projected_value"
        ]
        > raw_outcome.metrics[
            "projected_value"
        ]
    )

    assert (
        psa_10_outcome.confidence
        > raw_outcome.confidence
    )


def test_scenario_comparison_exposes_deltas():
    engine, _ = build_engine()

    raw = create_scenario(
        canonical_name="Raw Scenario",
        assertion_key=ASSERTION,
        assumptions={
            "grade": "raw",
            "horizon_years": 4,
        },
    )

    psa_10 = create_scenario(
        canonical_name="PSA 10 Scenario",
        assertion_key=ASSERTION,
        assumptions={
            "grade": "PSA 10",
            "horizon_years": 4,
        },
    )

    engine.register(raw)
    engine.register(psa_10)

    engine.run(raw.scenario_id)
    engine.run(psa_10.scenario_id)

    comparison = engine.compare(
        baseline_scenario_id=(
            raw.scenario_id
        ),
        compared_scenario_id=(
            psa_10.scenario_id
        ),
    )

    deltas = {
        item.metric: item
        for item in (
            comparison.metric_deltas
        )
    }

    assert (
        deltas[
            "projected_value"
        ].absolute_delta
        == 1500.0
    )

    assert (
        comparison
        .changed_assumptions["grade"]
        == {
            "baseline": "raw",
            "scenario": "PSA 10",
        }
    )


def test_scenario_instruments_update():
    engine, bus = build_engine()

    scenario = create_scenario(
        canonical_name="PSA 10 Scenario",
        assertion_key=ASSERTION,
        assumptions={
            "grade": "PSA 10",
        },
    )

    engine.register(scenario)

    outcome = engine.run(
        scenario.scenario_id
    )

    confidence = bus.state(
        SCENARIO_CONFIDENCE_ID
    )

    virtues = bus.state(
        SCENARIO_VIRTUE_ID
    )

    activity = bus.state(
        SCENARIO_ACTIVITY_ID
    )

    assert confidence.current_value == (
        outcome.confidence
    )

    assert virtues.current_value == (
        outcome.virtue_score
    )

    assert activity.current_value == 0.0
    assert activity.status.value == "stable"


def test_scenario_registry_preserves_run_history():
    engine, _ = build_engine()

    scenario = create_scenario(
        canonical_name="Repeated Scenario",
        assertion_key=ASSERTION,
        assumptions={
            "grade": "PSA 9",
        },
    )

    engine.register(scenario)

    first = engine.run(
        scenario.scenario_id
    )

    second = engine.run(
        scenario.scenario_id
    )

    history = engine.registry.outcomes(
        scenario.scenario_id
    )

    assert len(history) == 2
    assert history[0].run_id == first.run_id
    assert history[1].run_id == second.run_id
