class DEFEngine:
    """Decision Engine Framework™ — turns scores into decision language."""

    @staticmethod
    def recommendation(score, ni, risk):
        if score >= 9.5 and ni >= 4.5:
            return "Aggressive Buy"
        if score >= 9.0:
            return "Buy"
        if score >= 8.0:
            return "Accumulate / Watch"
        if score >= 7.0:
            return "Hold / Monitor"
        return "Pass"

    @staticmethod
    def classification(score):
        if score >= 9.7:
            return "THORᵡ Vault Candidate"
        if score >= 9.0:
            return "Qualified Kill Shot"
        if score >= 8.0:
            return "Cultivation Asset"
        if score >= 7.0:
            return "Liquidity Asset"
        return "Reject"

    @staticmethod
    def strike_zone(score, ni, market_strength, scarcity):
        return bool(score >= 9.0 and ni >= 4.0 and scarcity >= 8.0 and market_strength >= 7.0)
