from aletheus.card_hawk.marketplace_hydration.engine import Engine
from aletheus.card_hawk.marketplace_hydration.models import MarketObservation


def test_hydration() -> None:
    observations = (
        MarketObservation("s1", "SOLD", 100.0, "2026-01-01", True, 0.99),
        MarketObservation("s2", "LISTING", 120.0, "2026-01-02", False, 0.8),
    )
    assert Engine().hydrate(observations)["medianVerifiedSale"] == 100.0
