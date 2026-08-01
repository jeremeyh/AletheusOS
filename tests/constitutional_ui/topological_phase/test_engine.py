from aletheus.constitutional_ui.topological_phase.engine import Engine, Topology
from aletheus.constitutional_ui.topological_phase.models import ConstitutionalState


def test_x():
    s = ConstitutionalState(0.99, 0.99, 1, 1, 0, 0.1, 1, 0.8, 0.2, 0.99)
    assert Engine().compute(s).topology is Topology.CRYSTALLINE_SOLID
