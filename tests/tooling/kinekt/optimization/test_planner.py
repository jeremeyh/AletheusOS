from aletheus.tooling.kinekt.optimization.models import OptimizationCandidate
from aletheus.tooling.kinekt.optimization.planner import build_work_packages


def test_work_package_grouping() -> None:
    candidate = OptimizationCandidate(
        candidate_id="one",
        category="ownership",
        title="Normalize ownership",
        severity="high",
        effort="low",
        risk="low",
        confidence=0.9,
        expected_health_gain=5.0,
        priority_score=100.0,
    )
    packages = build_work_packages([candidate])
    assert len(packages) == 1
    assert packages[0].phase == 1
