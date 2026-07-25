from live_data.pricing.pricing_engine import PricingEngine


class CompEngine:
    """Comparable sales/listing engine."""

    @staticmethod
    def build(query, listings):
        estimate = PricingEngine.estimate(listings)
        bands = PricingEngine.value_band(estimate["average"])
        return {
            "query": query,
            "estimate": estimate,
            "bands": bands,
            "listings": [getattr(x, "__dict__", x) for x in listings or []],
        }
