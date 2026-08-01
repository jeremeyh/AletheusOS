from aletheus.card_hawk.application_runtime.engine import Engine
from aletheus.card_hawk.application_runtime.models import (
    CardDetermination,
    CardIdentity,
    DeterminationVector,
)


def test_runtime() -> None:
    asset = CardIdentity("a1", "Player", "Football", 2024, "Product")
    vector = DeterminationVector(0.9, 1, 0.8, 0.2, 0.7, 0.8, 0.2, 0.85, 0.82)
    determination = CardDetermination(asset, 90, 100, 110, "BUY", vector)
    result = Engine().run(determination, asking_price=80, user_goal="Core Asset")
    assert result["application"] == "CARD_HAWK"
