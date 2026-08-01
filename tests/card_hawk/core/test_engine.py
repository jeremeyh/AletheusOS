from aletheus.card_hawk.core.engine import Engine
from aletheus.card_hawk.core.models import (
    CardDetermination,
    CardIdentity,
    DeterminationVector,
)


def test_core() -> None:
    asset = CardIdentity("a1", "Player", "Football", 2024, "Product")
    vector = DeterminationVector(0.9, 1, 0.8, 0.2, 0.7, 0.8, 0.2, 0.85, 0.82)
    result = Engine().envelope(CardDetermination(asset, 90, 100, 110, "BUY", vector))
    assert "signature" in result
