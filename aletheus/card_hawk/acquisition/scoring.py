"""
Acquisition Opportunity Scoring

Genesis 13.6
"""


class AcquisitionScoringEngine:
    def score(self, target):

        score = 0

        if target.scarcity in ["numbered", "autograph", "patch"]:
            score += 30

        if target.asking_price <= target.target_price:
            score += 30

        score += target.upside_score // 2

        target.confidence = min(score, 100)

        if score >= 75:
            target.recommendation = "BUY"

        elif score >= 50:
            target.recommendation = "WATCH"

        else:
            target.recommendation = "PASS"

        return target
