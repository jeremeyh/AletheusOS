from aletheus.a3ye.esp.engine import Engine
from aletheus.a3ye.esp.models import SignalEnvelope


def test_x() -> None:
    result = Engine().process(SignalEnvelope("s", "text", {"ssn": "123"}, True))
    assert result.content["ssn"] == "[REDACTED]"
