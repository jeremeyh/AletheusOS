"""
Opportunity Ranking Engine

Genesis 13.25
"""


class OpportunityRankingEngine:
    def rank(self, opportunities):

        return sorted(
            opportunities, key=lambda item: item.get("confidence", 0), reverse=True
        )
