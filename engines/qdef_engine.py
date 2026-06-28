from dataclasses import dataclass


@dataclass
class QDEFResult:
    score: float
    scarcity: float
    quality: float
    conviction: str
    notes: list[str]


class QDEFEngine:
    """
    Quantitative Decision Evaluation Framework™

    Objective scoring only.
    """

    @staticmethod
    def evaluate(asset):

        scarcity = 0

        if asset.print_run:
            if asset.print_run <= 10:
                scarcity = 10
            elif asset.print_run <= 25:
                scarcity = 9
            elif asset.print_run <= 50:
                scarcity = 8
            elif asset.print_run <= 99:
                scarcity = 7
            else:
                scarcity = 5

        quality = 0

        if asset.rookie:
            quality += 2

        if asset.autograph:
            quality += 2

        if asset.memorabilia:
            quality += 1

        if asset.grade:
            quality += 2

        quality = min(quality,10)

        score = round((scarcity + quality)/2,2)

        if score >= 9:
            conviction = "Elite"

        elif score >= 8:
            conviction = "Strong"

        elif score >= 7:
            conviction = "Good"

        else:
            conviction = "Average"

        return QDEFResult(
            score,
            scarcity,
            quality,
            conviction,
            []
        )