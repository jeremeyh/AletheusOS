from __future__ import annotations

import time

import pytest

from aletheus.constitutional_cognition import (
    ConstitutionalConvergenceEngine,
    ConstitutionalVirtuesFramework,
    ContributionStance,
    ConvergenceState,
    DuplicateCognitiveParticipantError,
    EngineContribution,
    FunctionalCognitiveParticipant,
    MultiplicitousIntelligenceMesh,
    VirtueContext,
)


ASSERTION = "card.value.increases"


def contribution(
    engine_id: str,
    stance: ContributionStance,
    confidence: float,
    *,
    evidence_count: int = 1,
    weight: float = 1.0,
):
    return EngineContribution(
        engine_id=engine_id,
        assertion_key=ASSERTION,
        stance=stance,
        confidence=confidence,
        evidence_count=evidence_count,
        weight=weight,
        rationale=f"{engine_id} analysis",
        evidence=(
            {
                "source": (
                    f"{engine_id}.evidence"
                ),
            },
        ),
    )


def participant(
    engine_id: str,
    stance: ContributionStance,
    confidence: float,
    *,
    delay: float = 0.0,
):
    def evaluate(payload):
        if delay:
            time.sleep(delay)

        return contribution(
            engine_id,
            stance,
            confidence,
        )

    return FunctionalCognitiveParticipant(
        engine_id=engine_id,
        evaluator=evaluate,
    )


def test_canonical_virtues_pass_when_behavior_is_aligned():
    framework = ConstitutionalVirtuesFramework()

    assessment = framework.evaluate(
        VirtueContext()
    )

    assert assessment.passed
    assert assessment.score == 1.0
    assert len(assessment.findings) == 8


def test_truth_and_humility_fail_observably():
    framework = ConstitutionalVirtuesFramework()

    assessment = framework.evaluate(
        VirtueContext(
            evidence_supported=False,
            uncertainty_disclosed=False,
            fabrication_detected=True,
        )
    )

    violations = {
        finding.virtue.value
        for finding in assessment.violations
    }

    assert "truth" in violations
    assert "humility" in violations
    assert not assessment.passed


def test_convergence_preserves_dissent():
    engine = ConstitutionalConvergenceEngine()

    result = engine.converge(
        assertion_key=ASSERTION,
        contributions=(
            contribution(
                "knowledge",
                ContributionStance.SUPPORT,
                0.95,
            ),
            contribution(
                "reason",
                ContributionStance.SUPPORT,
                0.90,
            ),
            contribution(
                "risk",
                ContributionStance.CHALLENGE,
                0.45,
            ),
        ),
    )

    assert result.state == (
        ConvergenceState.CONVERGED
    )
    assert result.dominant_stance == (
        ContributionStance.SUPPORT
    )
    assert {
        item.engine_id
        for item in result.dissent
    } == {"risk"}


def test_close_division_remains_contested():
    engine = ConstitutionalConvergenceEngine(
        contest_threshold=0.20
    )

    result = engine.converge(
        assertion_key=ASSERTION,
        contributions=(
            contribution(
                "prediction",
                ContributionStance.SUPPORT,
                0.80,
            ),
            contribution(
                "risk",
                ContributionStance.CHALLENGE,
                0.75,
            ),
        ),
    )

    assert result.state == (
        ConvergenceState.CONTESTED
    )
    assert len(result.dissent) == 1


def test_all_abstentions_are_insufficient():
    engine = ConstitutionalConvergenceEngine()

    result = engine.converge(
        assertion_key=ASSERTION,
        contributions=(
            contribution(
                "knowledge",
                ContributionStance.ABSTAIN,
                0.80,
            ),
        ),
    )

    assert result.state == (
        ConvergenceState.INSUFFICIENT
    )
    assert result.confidence == 0.0


def test_mesh_executes_specialized_participants():
    mesh = MultiplicitousIntelligenceMesh()

    mesh.register(
        participant(
            "knowledge",
            ContributionStance.SUPPORT,
            0.90,
        )
    )
    mesh.register(
        participant(
            "reason",
            ContributionStance.SUPPORT,
            0.85,
        )
    )
    mesh.register(
        participant(
            "risk",
            ContributionStance.CHALLENGE,
            0.30,
        )
    )

    report = mesh.execute(
        assertion_key=ASSERTION,
        payload={
            "card_id": "CARD-001",
        },
    )

    assert len(report.contributions) == 3
    assert report.convergence.state == (
        ConvergenceState.CONVERGED
    )
    assert report.virtues.passed
    assert report.successful


def test_mesh_is_parallel_not_sequential():
    mesh = MultiplicitousIntelligenceMesh(
        max_workers=3
    )

    for engine_id in (
        "knowledge",
        "reason",
        "prediction",
    ):
        mesh.register(
            participant(
                engine_id,
                ContributionStance.SUPPORT,
                0.80,
                delay=0.15,
            )
        )

    started = time.perf_counter()

    mesh.execute(
        assertion_key=ASSERTION,
        payload={},
    )

    elapsed = time.perf_counter() - started

    assert elapsed < 0.35


def test_mesh_preserves_participant_failure():
    mesh = MultiplicitousIntelligenceMesh()

    mesh.register(
        participant(
            "knowledge",
            ContributionStance.SUPPORT,
            0.90,
        )
    )

    def fail(payload):
        raise RuntimeError(
            "Prediction model unavailable."
        )

    mesh.register(
        FunctionalCognitiveParticipant(
            engine_id="prediction",
            evaluator=fail,
        )
    )

    report = mesh.execute(
        assertion_key=ASSERTION,
        payload={},
    )

    assert len(report.contributions) == 1
    assert report.failures == (
        {
            "engine_id": "prediction",
            "error": (
                "Prediction model unavailable."
            ),
        },
    )


def test_signals_are_emitted_for_living_instruments():
    observed = []

    mesh = MultiplicitousIntelligenceMesh(
        observer=observed.append
    )

    mesh.register(
        participant(
            "knowledge",
            ContributionStance.SUPPORT,
            0.90,
        )
    )

    report = mesh.execute(
        assertion_key=ASSERTION,
        payload={},
    )

    signal_types = {
        signal.signal_type.value
        for signal in report.signals
    }

    assert "mesh_started" in signal_types
    assert "engine_started" in signal_types
    assert "engine_completed" in signal_types
    assert "convergence_completed" in signal_types
    assert "virtues_evaluated" in signal_types
    assert "mesh_completed" in signal_types

    assert len(observed) == len(
        report.signals
    )


def test_duplicate_participant_is_rejected():
    mesh = MultiplicitousIntelligenceMesh()

    knowledge = participant(
        "knowledge",
        ContributionStance.SUPPORT,
        0.90,
    )

    mesh.register(knowledge)

    with pytest.raises(
        DuplicateCognitiveParticipantError
    ):
        mesh.register(knowledge)
