from aletheus.constitutional_ui.primordial_field.engine import Engine, Potential
from aletheus.constitutional_ui.primordial_field.models import ConstitutionalState


def test_x():
    assert Engine().evaluate(
        Potential("p", "Evaluate", ConstitutionalState(*([0.8] * 10)), ("Surface",))
    )["manifestable"]
