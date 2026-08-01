from aletheus.card_hawk.experience_projection.engine import Engine
from aletheus.card_hawk.experience_projection.models import (
    CardDetermination,
    CardIdentity,
    DeterminationVector,
)


def test_projection() -> None:
    asset = CardIdentity("a1", "Player", "Football", 2024, "Product")
    vector = DeterminationVector(0.9, 1, 0.8, 0.2, 0.7, 0.8, 0.2, 0.85, 0.82)
    determination = CardDetermination(asset, 90, 100, 110, "BUY", vector)
    result = Engine().compile(determination, ("CARD_DETAIL", "VOICE"))
    assert result["semanticEquivalencePreserved"] is True
