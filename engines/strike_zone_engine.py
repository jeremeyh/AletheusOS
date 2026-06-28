from engines.valuation_engine import ValuationEngine


class StrikeZoneEngine:
    """Strike Zone™ — determines whether an asset is actionable."""

    @staticmethod
    def is_in_strike_zone(asset):
        roi = ValuationEngine.roi_percent(asset)

        return (
            asset.thorx_score >= 9.0
            and asset.ni_score >= 4.0
            and roi >= 0
        )