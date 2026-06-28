from dataclasses import dataclass


@dataclass
class DDEFResult:

    recommendation:str
    confidence:int
    rationale:list[str]


class DDEFEngine:
    """
    Dynamic Decision Evaluation Framework™

    Uses market context.
    """

    @staticmethod
    def evaluate(asset,qdef):

        rationale=[]

        confidence=60

        recommendation="Monitor"

        if asset.thorx_score>=9.5:

            confidence+=20

            rationale.append("Exceptional THORᵡ™ score")

        if asset.ni_score>=5:

            confidence+=10

            rationale.append("Maximum NI™")

        if qdef.score>=9:

            confidence+=10

            rationale.append("Elite quantitative profile")

        if confidence>=90:

            recommendation="Aggressive Buy"

        elif confidence>=80:

            recommendation="Buy"

        elif confidence>=70:

            recommendation="Accumulate"

        elif confidence>=60:

            recommendation="Hold"

        else:

            recommendation="Monitor"

        return DDEFResult(
            recommendation,
            min(confidence,100),
            rationale
        )