from aletheus.constitutional_experience.information_physics.engine import Engine
from aletheus.constitutional_experience.models import EvidenceSignal, VeracityPhase


def test_physics():
    s = EvidenceSignal("e", 0.9, 0.8, 1, 0.99)
    assert round(Engine().informational_mass(s), 12) == 0.72
    assert Engine().phase(s.veracity) is VeracityPhase.CRYSTALLINE
