from marketplace.comp_engine import CompEngine

class PricingService:
    def summarize(self, comps):
        return {
            "average": CompEngine.average(comps),
            "high": CompEngine.high(comps),
            "low": CompEngine.low(comps),
            "count": len(comps)
        }
