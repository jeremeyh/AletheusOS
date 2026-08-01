from aletheus.a3ye.experience_integration.engine import Engine
from aletheus.a3ye.experience_integration.models import (
    A3yeResponse,
    DeterminationVector,
)


def test_x() -> None:
    response = A3yeResponse(
        "r", "Proceed", DeterminationVector(0.9, 0.9, 0.8, 0.9, 0.1, 0.85)
    )
    assert (
        Engine().hydrate(response, ("VOICE", "AXIOMUX_FIELD"))[
            "projectionNeutralityPreserved"
        ]
        is True
    )
