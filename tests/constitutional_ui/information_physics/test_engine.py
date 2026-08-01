from aletheus.constitutional_ui.information_physics.engine import Engine
from aletheus.constitutional_ui.information_physics.models import ConstitutionalState


def test_x():
    assert Engine().solve(ConstitutionalState(*([0.9] * 10))).mass > 0
