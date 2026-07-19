from aletheus.strategic.span import (
    AnalysisRequest,
    Evidence,
    build_span,
)
from aletheus.strategic.spartan import DomainContext, build_spartan


def test_span_evaluates_and_records_recommendation() -> None:
    spartan = build_spartan()
    span = build_span(spartan=spartan)
    span.start()

    request = AnalysisRequest(
        subject="runtime.core",
        question="Should responsibility be extracted from the composition root?",
        requested_by="test-suite",
    )
    evidence = (
        Evidence(
            source="architecture-review",
            claim="runtime.core has increasing responsibility density",
            confidence=0.92,
        ),
    )

    recommendation = span.evaluate(request, evidence)

    assert recommendation.analysis.request_id == request.request_id
    assert recommendation.confidence >= 0.70
    assert span.memory.get(recommendation.recommendation_id) is not None

    span.stop()
    assert not span.is_started


def test_spartan_runs_registered_domains() -> None:
    network = build_spartan(("architecture", "runtime"))
    network.start()

    result = network.analyze(
        DomainContext(
            subject="AletheusOS",
            question="What should evolve next?",
        )
    )

    assert len(result.domain_analyses) == 2
    assert result.recursive_cycle.completed_stages
    assert result.confidence == 0.50
