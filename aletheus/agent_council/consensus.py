"""
Consensus Engine

Genesis 13.29
"""


class ConsensusEngine:


    def decide(
        self,
        opinions
    ):


        scores = {}


        for opinion in opinions:


            decision = (
                opinion.recommendation
            )


            scores.setdefault(
                decision,
                0
            )


            scores[decision] += (
                opinion.confidence
            )



        result = max(

            scores,

            key=scores.get

        )


        return {

            "decision":
                result,

            "confidence":
                scores[result]

        }

