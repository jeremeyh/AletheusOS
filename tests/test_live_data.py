def test_live_data_search():
    from live_data.live_data_service import LiveDataService
    rows = LiveDataService().search("Caleb Williams")
    assert len(rows) > 0

def test_pricing_engine():
    from live_data.pricing.pricing_engine import PricingEngine
    result = PricingEngine.estimate([])
    assert result["count"] == 0
