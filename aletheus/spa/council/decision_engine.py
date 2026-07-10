"""
SPA Council Decision Engine

Genesis 155
"""


class DecisionEngine:


    def decide(self, review, risk, constitution):

        if constitution["approved"]:

            return {

                "decision":
                "approved",

                "confidence":
                95

            }


        return {

            "decision":
            "rejected"

        }

