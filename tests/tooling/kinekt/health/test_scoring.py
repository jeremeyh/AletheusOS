from aletheus.tooling.kinekt.health.scoring import (
    build_dimensions,
    readiness,
    total_score,
)


def test_health_scoring() -> None:
    dimensions = build_dimensions(
        {"total_score": 80},
        {"isolated": ["a"], "modules": ["a", "b", "c", "d"]},
        {"unresolved_modules": ["x"], "nodes": [{}, {}, {}, {}], "findings": []},
        {"average_score": 75},
        {"findings": []},
    )

    score = total_score(dimensions)

    assert 0 <= score <= 100
    assert readiness(score, dimensions) in {"ready", "conditional", "not_ready"}
