import pytest

from aletheus.constitutional_experience.runtime_realization.engine import (
    RuntimeRealizationEngine,
)
from aletheus.constitutional_experience.runtime_realization.equations import (
    informational_mass,
    poincare_distance,
    spring_damping,
)
from aletheus.constitutional_experience.runtime_realization.models import (
    EvidenceNode,
    RuntimeProfile,
    TelemetryFrame,
)


def test_information_physics():
    n = EvidenceNode("e", 0.9, 0.8, 2, 0.99, 0.2, 0.1)
    assert informational_mass(n) == pytest.approx(1.44)
    assert spring_damping(100, 1, 1) == 20


def test_hyperbolic_distance():
    assert poincare_distance((0, 0, 0), (0.1, 0, 0)) > 0


def test_node_scoring_and_health():
    engine = RuntimeRealizationEngine()
    nodes = [EvidenceNode("a", 1, 1, 1, 0.99), EvidenceNode("b", 0.5, 0.5, 1, 0.5, 0.8)]
    scored = engine.score_nodes(nodes)
    assert scored[0]["node_id"] == "a"
    frame = TelemetryFrame(1, 120, 8.2, 1, 1.0, 0.95, 0.99, 0.98)
    health = engine.runtime_health(frame, RuntimeProfile())
    assert health.status == "healthy"
