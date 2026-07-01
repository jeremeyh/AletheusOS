from cardhawk.services import AssetService


def test_service():

    service = AssetService()

    assert service is not None

    stats = service.portfolio_statistics()

    assert "count" in stats

    assert "total_purchase_price" in stats

    assert "total_estimated_value" in stats


if __name__ == "__main__":

    test_service()

    print("✔ Card Hawk Asset Service tests passed.")

