"""
Decision Engine

Genesis 13.26
"""


class OpportunityDecisionEngine:


    def decide(
        self,
        score
    ):


        if score >= 85:

            return "BUY"



        if score >= 60:

            return "WATCH"



        return "PASS"

