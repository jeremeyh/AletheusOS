from aletheus.card_hawk.asset_ingress.engine import Engine


def test_ingress() -> None:
    asset = Engine().ingest(
        {
            "asset_id": "a1",
            "player": "Player",
            "sport": "Football",
            "year": 2024,
            "product": "Product",
        }
    )
    assert asset.asset_id == "a1"
