from aletheus.constitutional_ui.projection_protocol.engine import Engine
from aletheus.constitutional_ui.projection_protocol.models import (
    ConstitutionalState,
    ProjectionNode,
)


def test_x():
    s = ConstitutionalState(*([0.9] * 10))
    assert (
        Engine().create(intent="x", state=s, root=ProjectionNode("r", "Field", s))[
            "runtimeProtocol"
        ]
        == "AxiomUX-v1.0"
    )
