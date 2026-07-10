"""
Card Hawk Acquisition Workspace

Genesis 13.16
"""


from .opportunity import OpportunityAnalyzer
from .comparison import OpportunityComparisonEngine



class CardHawkAcquisitionWorkspace:


    def __init__(
        self
    ):

        self.analyzer = (
            OpportunityAnalyzer()
        )

        self.comparison = (
            OpportunityComparisonEngine()
        )


        self.queue = []



    def add(
        self,
        opportunity
    ):

        self.queue.append(
            opportunity
        )


        return opportunity



    def review(
        self
    ):

        return [

            self.analyzer.analyze(
                item
            )

            for item

            in self.queue

        ]



    def rank(
        self
    ):

        return self.comparison.compare(
            self.queue
        )

