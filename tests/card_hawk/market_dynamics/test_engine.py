from aletheus.card_hawk.market_dynamics.engine import Engine


def test_dynamics() -> None:
    result = Engine().evaluate(
        known_population=100,
        active_listings=5,
        sales_velocity_30d=12,
        price_change_90d=0.2,
    )
    assert result["scarcity"] > 0.9
