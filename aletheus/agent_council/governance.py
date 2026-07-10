"""
Council Governance

Genesis 13.29
"""


class CouncilGovernance:


    def authorize(
        self,
        decision
    ):


        return {


            "approved":

                decision["confidence"] >= 70,


            "decision":

                decision

        }

