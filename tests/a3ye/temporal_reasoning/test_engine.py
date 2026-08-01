from aletheus.a3ye.temporal_reasoning.engine import Engine
from aletheus.a3ye.temporal_reasoning.models import TemporalFrame


def test_x() -> None:
    assert (
        Engine().analyze(TemporalFrame({}, {}, {}, ("x",)))["futureIsProjection"]
        is True
    )
