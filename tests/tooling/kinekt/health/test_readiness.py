from aletheus.tooling.kinekt.health.models import HealthDimension
from aletheus.tooling.kinekt.health.scoring import readiness


def test_ready_requires_no_critical_dimension() -> None:
    dimensions = [
        HealthDimension(
            name="integrity",
            score=95,
            weight=1.0,
            status="healthy",
        )
    ]

    assert readiness(95, dimensions) == "ready"
