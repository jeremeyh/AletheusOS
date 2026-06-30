class RecommendationEngine:
    """
    DEF Recommendation Engine™
    """

    @staticmethod
    def recommend(final_score, qdef_score, ddef_score):
        if final_score >= 92 and qdef_score >= 85:
            return "STRIKE"

        if final_score >= 82:
            return "BUY"

        if final_score >= 70:
            return "HOLD"

        if final_score >= 58:
            return "WATCH"

        return "PASS"

    @staticmethod
    def confidence(qdef_score, ddef_score):
        gap = abs(qdef_score - ddef_score)

        confidence = 95 - gap

        return round(max(50, min(confidence, 99)), 2)
