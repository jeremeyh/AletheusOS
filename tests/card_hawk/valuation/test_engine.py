from aletheus.card_hawk.valuation.engine import Engine
from aletheus.card_hawk.valuation.models import CardIdentity, MarketObservation


def test_valuation() -> None:
    asset = CardIdentity("a1", "Player", "Football", 2024, "Product")
    observations = (
        MarketObservation("s1", "SOLD", 100.0, "2026-01-01", True, 0.99),
        MarketObservation("s2", "SOLD", 110.0, "2026-01-02", True, 0.95),
    )
    result = Engine().determine(
        asset,
        observations,
        scarcity=0.8,
        saturation=0.2,
        momentum=0.7,
        portfolio_fit=0.9,
        downside_risk=0.2,
    )
    assert result["fairValueMid"] > 100
