from aletheus.constitutional_ui.nuclear_cloud.engine import Engine
from aletheus.constitutional_ui.nuclear_cloud.models import ConstitutionalState


def test_x():
    r = Engine().assess(
        ConstitutionalState(*([0.95] * 10)),
        evidence_mass=0.98,
        analytical_breadth=0.96,
        contradiction_resolution=0.94,
    )
    assert r.reason_density > 0.9 and r.determination_not_fact
