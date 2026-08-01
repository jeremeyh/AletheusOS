from aletheus.nimble.core.engine import Engine
from aletheus.nimble.core.models import PrimitiveDefinition


def test_core_validation() -> None:
    assert (
        Engine()
        .validate((PrimitiveDefinition("Surface", "structure", "surface"),))
        .valid
    )
