from engines.ni_engine import NIEngine
from engines.strike_zone_engine import StrikeZoneEngine


class ThorxEngine:
    """THORᵡ™ — Treasured High-Order Relixᵡ Intelligence Engine."""

    @staticmethod
    def score(asset):
        score = 0

        if asset.print_run and asset.print_run <= 10:
            score += 2
        elif asset.print_run and asset.print_run <= 25:
            score += 1.5
        elif asset.print_run and asset.print_run <= 99:
            score += 1

        if asset.autograph:
            score += 1.25

        if asset.memorabilia:
            score += 0.75

        if asset.rookie:
            score += 1

        if asset.current_value and asset.purchase_price:
            if asset.current_value >= asset.purchase_price * 2:
                score += 1
            elif asset.current_value >= asset.purchase_price:
                score += 0.5

        score = min(round(score + 4.0, 2), 10)

        asset.thorx_score = score
        asset.ni_score = NIEngine.score(asset)
        asset.strike_zone = StrikeZoneEngine.is_in_strike_zone(asset)

        return asset