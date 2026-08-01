from aletheus.constitutional_ui.core.engine import Engine
from aletheus.constitutional_ui.core.models import ConstitutionalState, ProjectionNode


def test_x():
    s = ConstitutionalState(*([0.9] * 10))
    r = ProjectionNode("r", "Field", s)
    assert "constitutionalSignature" in Engine().envelope(r, "Proceed")
