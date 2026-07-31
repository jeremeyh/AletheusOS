"""
Market Comparison Engine

Genesis 13.16
"""


class OpportunityComparisonEngine:
    def compare(self, opportunities):

        return sorted(opportunities, key=lambda x: x.thor_score, reverse=True)
