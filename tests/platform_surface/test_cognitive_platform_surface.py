from __future__ import annotations

from aletheus.constitutional_cognition import (
    ContributionStance,
    EngineContribution,
    FunctionalCognitiveParticipant,
)
from aletheus.constitutional_scenarios import (
    SCENARIO_ACTIVITY_ID,
    SCENARIO_CONFIDENCE_ID,
)
from aletheus.platform_surface import (
    build_aletheus_platform,
)


ASSERTION = "card.future_value.increases"


def participant(
    engine_id: str,
    stance: ContributionStance,
    confidence: float,
):
    def evaluate(payload):
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


def build_cognitive_platform():
    platform = build_aletheus_platform()

    platform.cognition.register(
        participant(
            "knowledge",
            ContributionStance.SUPPORT,
            0.90,
        )
    )

    platform.cognition.register(
        participant(
            "prediction",
            ContributionStance.SUPPORT,
            0.85,
        )
    )

    platform.cognition.register(
        participant(
            "risk",
            ContributionStance.CHALLENGE,
            0.25,
        )
    )

    return platform


def test_platform_exposes_cognitive_surfaces():
    platform = build_aletheus_platform()

    assert platform.cognition is not None
    assert platform.instrumentation is not None
    assert platform.scenarios is not None


def test_cognition_surface_drives_instrumentation():
    platform = build_cognitive_platform()

    report = platform.cognition.execute(
        assertion_key=ASSERTION,
        payload={
            "card_id": "CARD-001",
        },
    )

    confidence = (
        platform
        .instrumentation
        .state(
            "aletheus.instrument.confidence"
        )
    )

    truth = (
        platform
        .instrumentation
        .state(
            "aletheus.instrument.truth"
        )
    )

    assert confidence.current_value == (
        report.convergence.confidence
    )

    assert truth.current_value == 1.0


def test_scenario_surface_runs_through_platform():
    platform = build_cognitive_platform()

    scenario = (
        platform
        .scenarios
        .create_and_register(
            canonical_name=(
                "Card PSA 10 Scenario"
            ),
            assertion_key=ASSERTION,
            assumptions={
                "grade": "PSA 10",
                "horizon_years": 4,
            },
            horizon="4 years",
        )
    )

    outcome = platform.scenarios.run(
        scenario.scenario_id
    )

    assert outcome.scenario_id == (
        scenario.scenario_id
    )
    assert outcome.confidence > 0
    assert outcome.virtue_score == 1.0


def test_scenario_execution_updates_instruments():
    platform = build_cognitive_platform()

    scenario = (
        platform
        .scenarios
        .create_and_register(
            canonical_name=(
                "Instrumented Scenario"
            ),
            assertion_key=ASSERTION,
            assumptions={
                "grade": "PSA 9",
            },
        )
    )

    outcome = platform.scenarios.run(
        scenario.scenario_id
    )

    confidence = (
        platform
        .instrumentation
        .state(
            SCENARIO_CONFIDENCE_ID
        )
    )

    activity = (
        platform
        .instrumentation
        .state(
            SCENARIO_ACTIVITY_ID
        )
    )

    assert confidence.current_value == (
        outcome.confidence
    )
    assert activity.current_value == 0.0
    assert activity.status.value == "stable"


def test_platform_snapshot_contains_cognitive_state():
    platform = build_cognitive_platform()

    platform.cognition.execute(
        assertion_key=ASSERTION,
        payload={},
    )

    snapshot = platform.snapshot()

    assert snapshot.status == "healthy"
    assert "cognition" in snapshot.details
    assert "instrumentation" in snapshot.details
    assert "scenarios" in snapshot.details

    assert (
        snapshot.details[
            "cognition"
        ]["executions"]
        == 1
    )

    assert (
        snapshot.details[
            "instrumentation"
        ][
            "aletheus.instrument.confidence"
        ]["current_value"]
        is not None
    )
