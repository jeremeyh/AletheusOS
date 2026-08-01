from aletheus.card_hawk.thorx_bridge.engine import Engine
from aletheus.card_hawk.thorx_bridge.models import DeterminationVector


def test_thorx() -> None:
    vector = DeterminationVector(0.95, 1, 0.9, 0.1, 0.9, 0.9, 0.1, 0.92, 0.9)
    result = Engine().adjudicate(vector, 80, 100)
    assert result["decision"] == "BUY"
