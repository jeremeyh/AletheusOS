from aletheus.card_hawk.nuclear_cloud.engine import Engine
from aletheus.card_hawk.nuclear_cloud.models import DeterminationVector


def test_cloud() -> None:
    vector = DeterminationVector(0.95, 1, 0.9, 0.1, 0.9, 0.9, 0.1, 0.99, 0.9)
    assert Engine().project(vector)["topology"] == "CRYSTALLINE_SOLID"
