from aletheus.card_hawk.evidence_graph.engine import Engine
from aletheus.card_hawk.evidence_graph.models import MarketObservation


def test_graph() -> None:
    observation = MarketObservation("source", "SOLD", 100.0, "2026-01-01", True, 0.99)
    result = Engine().build((observation,))
    assert result["nodes"][0]["topology"] == "CRYSTALLINE_SOLID"
